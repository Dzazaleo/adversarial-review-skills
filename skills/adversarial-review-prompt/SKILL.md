---
name: adversarial-review-prompt
description: "Generate a targeted adversarial review prompt to hand to a different AI model — for independent audits, cross-model code review, red-teaming a plan or design, or second-opinion verification of work Claude itself produced. Use when the user asks for an external/independent/adversarial review, a prompt for another model (Codex, Gemini, GPT, Qwen, Cursor), something to paste into another model's chat box, a red-team of their own code, or wants their work attacked rather than confirmed. Produces an audit brief plus a paste-ready cover note that tells the reviewer to write its report to a file — never a review."
argument-hint: "<target: phase N | path | PR | diff | plan file> [--reviewer <model>] [--writes]"
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

<objective>
Produce a single self-contained markdown prompt that a **different model** — one that did not
write the work — can be handed with no other context, and that maximizes the chance it finds
real defects instead of agreeing with the author.

You are writing the prompt. You are **not** performing the review. Do not review the work,
do not fix anything, do not summarize findings you noticed while reading. The deliverable is
two files: the audit brief, and a short paste-ready cover note that hands it over.
</objective>

<why_this_is_hard>
The failure mode is not a badly-formatted prompt. It is a prompt that produces confirmation.
A reviewer given "please review this code" will re-derive what the author already claimed,
agree, and return a polite summary of the author's own beliefs. That output is worthless and
worse than nothing, because it launders self-review as independent review.

Everything in this skill exists to defeat that. Three levers do most of the work:

1. **Name the *condition*, not the contents.** You cannot list the blind spots — if you could
   see them they would not be blind, and finding them is the reviewer's entire job. What you
   can state, because it is a fact about the process rather than about the work, is that one
   model wrote this, reviewed it, and verified it against tests it also wrote; that a reviewer
   with a different architecture notices different things; and that agreement is therefore a
   failed outcome. Never imply you know what was missed. Where you genuinely do suspect
   something, that is a *known* unknown — it is held out of the prompt entirely and handed
   to the user for post-review comparison (§10), never written into the prompt.
2. **Demote the author's assertions to claims.** Every confident comment, test name, and
   "verified/measured/guaranteed" note is a testable assertion by the party under review,
   never evidence. This single reframing produces more findings than any checklist.
3. **Hand over a target list, not a codebase.** You cannot point at the blind spot, but you
   can point at what is carrying weight. An enumerated list of load-bearing claims — each of
   which must come back CONFIRMED / REFUTED / COULD NOT DETERMINE — puts the reviewer's
   different eyes where an unseen defect would be expensive, instead of scattered thin across
   the whole tree by a generic "audit this."
</why_this_is_hard>

<process>

## 1. Fix the target and the reviewer

Resolve from `$ARGUMENTS` (ask only if genuinely ambiguous):

- **Target** — a phase, directory, file set, PR, diff range, or a plan/design doc. Get an
  exact file list with line counts; a reviewer needs to know the size of the job.
- **Reviewer** — which model/CLI receives this. Adjust only the mechanics (how it runs
  commands, what it can access), never the adversarial framing.
- **Artifact kind** — code, or a plan/design. For a plan there is nothing to execute, so the
  evidence standard shifts from CONFIRMED-by-execution to "cite the source that contradicts
  it"; the brief's §6 becomes assumptions and one-way doors rather than runtime claims.
- **Write access** — beyond its own report file, which is always authorized (§6), read-only
  unless the user passed `--writes` or asked for mutation testing in words. This decides which
  write boundary the prompt's envelope gets (§7 below); never grant more on your own initiative.
- **Delivery route** — chat box or terminal. Default to the chat box: the cover note (§8) is
  what the user pastes, and the brief stays on disk for the reviewer to open.

## 2. Read the actual work — never write the prompt from memory or from a summary

Read the source, the tests, the spec, and the prior review documents. Then run enough
commands to state facts, not guesses:

- File list + line counts for the in-scope set
- The test/typecheck/build commands and what a *passing* run actually prints
- Anything environment-dependent: gitignored datasets, env-var-gated test gates, untracked
  files, OS-specific semantics (Windows symlink/junction/permission behavior is a recurring
  source of real defects)
- Current git state, so you can tell the reviewer what "clean" looks like
- **The audit range, pinned to immutable commit IDs — never to a branch relation.** State the
  work under review as explicit commits (`abc1234^..def5678`, or a list) with the file count
  and `+N/−M` from `git diff --stat` over that exact range, and run that command while
  authoring the brief so the numbers are observed, not remembered. Never write "N commits
  ahead of `main`" or "`git diff main..HEAD` is the work" — `main` and the branch converge and
  re-diverge as work lands (a local fast-forward is one command), and on 2026-08-16 a brief
  said "2 commits ahead of `main`" three minutes *after* `main` had been fast-forwarded onto
  the branch, so the prescribed range was empty at authoring time; the reviewer had to
  reconstruct the scope itself and correctly ranked the empty range as a process finding.
  Where documentation-only commits sit on top of the code under review (the brief itself is
  usually one), name them separately so the reviewer knows `HEAD` will be ahead of the pinned
  range and that this is expected.

A prompt containing a wrong path, a stale line number, or a test command that fails burns
the reviewer's first ten minutes and its trust in the rest of the document.

## 3. Mine the load-bearing claims — this is the core work

Hunt the places where the work asserts its own correctness. High-yield searches:

```bash
grep -rniE "measured|verified|guaranteed|immune|cannot|never|asserted by|mutation|by construction|NOT assumed" src/ scripts/
```

Also collect: comments citing a test as proof of a guarantee, comments citing an oracle or
spec by line number, frozen/published contract declarations, threshold and comparison-operator
choices flagged as deliberate (`>=` vs `>`, inclusive vs exclusive bounds), coupled constants
said to be enforced by a test, and any claim of determinism across machines.

Turn each into a numbered, attackable item with the citation and — critically — an embedded
sub-question that points at the seam:

> `below * 100 <= maxPct * total` (integer form, `classifier.ts:44`) is exact and immune to
> float drift at the boundary, versus Python's `100.0 * below / total <= 0.5`.
> *The CLI accepts arbitrary decimal `--borderline-max-pct` values — does the guarantee
> survive that?*

Group them (rule/arithmetic correctness · published contracts · robustness and process
behavior · supply chain and hygiene). Aim for 15–25 items. Fewer means you did not read
enough; many more means you are padding with things that cannot produce a wrong result.

## 4. Inventory the ground already walked

List every prior finding — internal review, code review, CI, earlier audits — with its
severity label and its **disposition**. Check beside each report for its adjudication ledger
first — `NN-REVIEW-ADJUDICATION.md` in a phase directory, or bare `REVIEW-ADJUDICATION.md` for a
standalone target (a skill, a repo with no phase structure) — its rows *and its ruled auxiliary
entries* (process, could-not-verify, prior-review disagreements) are the dispositions, verdict
and outcome per finding. Undispositioned findings are the richest seam:
a warning that was found and left, and that can produce a *wrong result that looks right* or
a *green test run that proves nothing*, is a blocker wearing a warning label.

Give the reviewer three explicit instructions on this list:
- Do not re-report these; re-finding known issues is wasted effort.
- For anything already "fixed": judge whether the fix is complete, correct, and whether it
  opened a *new* path to the very failure it closed.
- Spend the majority of effort **outside** this list. The most valuable return is a defect
  the prior review had no category for.

Include any candid corrections already on record (a premise that did not reproduce, a fix
kept for other reasons) and ask whether the surrounding reasoning was sound. Honesty here
buys credibility for the whole document.

If no prior review exists, do not silently drop this section from the prompt — state it in
one line ("no prior review has been performed; you are the first reviewer"). An absent
section reads as withheld history, not as absence of history.

## 5. Mark the one-way doors

Identify what becomes expensive to change once downstream consumers exist — published
schemas, hashes, file formats, wire protocols, exit codes, public APIs. State who will
consume them and why a design flaw found now is worth more than any implementation bug.
This is where you tell the reviewer to spend disproportionate attention.

## 6. Write the prompt file

Follow [references/prompt-template.md](references/prompt-template.md) for section order and
the exact framing language. A full worked example — the one this skill was distilled from —
may be present at [references/example-audit-prompt.md](references/example-audit-prompt.md);
it is optional, so skip it without comment if absent. Read it when you need to see the
register and level of specificity, not to copy its content.

Non-negotiables while writing:

- **Address the reviewer in second person throughout.** It reads the file directly.
- **Self-contained.** No "as discussed", no reference to this conversation, no assumption it
  can see the user's screen or prior sessions.
- **Every claim carries `file:line`.** Unlocatable claims get skipped.
- **State the evidence standard**: Location · Mechanism · Trigger (concrete input or state —
  "a malformed PNG" is not a trigger, "a greyscale PNG with a tRNS chunk" is) · Consequence
  tied to a stated criterion · Status **CONFIRMED** (executed, with command and output) or
  **THEORETICAL** (reasoned from source, say what stopped you). Forbid blurring the two.
- **List anti-patterns explicitly** — output that will be discarded: style and naming
  opinions, "consider adding X" with no defect behind it, restating a comment as
  verification, proposing out-of-scope features, severity inflation, hedged findings that
  commit to nothing, praise beyond one paragraph.
- **Specify the deliverable shape** — a coverage line, findings in a strict ranked order,
  claims examined and upheld (one line each, as coverage evidence), could-not-verify (an
  unstated gap reads as a pass), and any mutation results.
- **Name the report's destination inside the prompt, and make the reviewer write it.** The
  report is a file the *reviewer* creates — `<phase-dir>/NN-EXTERNAL-REVIEW.md`, beside the
  brief — not a chat message the user copies out afterwards. Instruct it to create the file
  early — title and identity — and append each finding as it confirms it, rather than holding
  the report in memory; the coverage line and the final ranked order are set in a closing
  pass, since findings arrive in discovery order and coverage is only knowable at the end.
  Say the closing pass is expected and is not composing-at-the-end — what is forbidden is a
  report that exists only in memory. A chat-only report is one dropped message, one
  truncated reply, or one closed tab away from losing the entire audit, and a report that
  exists only after the last token is a report that does not exist if the run is cut short.
  Ask for a short summary in the chat reply — coverage line, ranked finding titles with impact
  levels, the file path — and all detail in the file. This one write is authorized even under
  an otherwise read-only envelope; state the authorization and the read-only rule in the same
  breath (§7) so they cannot read as contradictory instructions.
- **Never ask the reviewer for a verdict.** Whether the work ships or is marked complete is
  the owner's call, and a reviewer that commits to YES or NO up front bends its own findings
  to stay consistent with it. What the verdict was buying is commitment, and forced ranking
  buys it better: order the findings by the cost of leaving each unfixed — blast radius ×
  likelihood the trigger is reached — with no ties and a one-clause justification for each
  position. Each finding carries an **Impact** level (critical/high/medium/low) as an
  attribute; severity is never a section heading — buckets are how a reviewer avoids saying
  which of six "criticals" it would fix first. Evidence status is not impact: a THEORETICAL
  data-loss defect outranks a CONFIRMED cosmetic one. Per-claim CONFIRMED / REFUTED / COULD
  NOT DETERMINE adjudication (§3) is evidence about a claim, not a verdict, and stays.
- **Author's residual doubts stay out of the prompt entirely.** A reviewer that reads them
  is anchored by them — demotion disclaimers do not survive contact — while a suspicion the
  reviewer reaches blind is independent corroboration, the strongest evidence this exercise
  can produce. Collect 3–5, each a question with a mechanism and the `file:line` it is about,
  and put them in the hand-off summary (§10) for the user to compare against the returned
  review. They stay out of the cover note too (§8) — it is read first, so anchoring there is
  worse, not better.
- **Where a load-bearing claim's sub-question is one of your own doubts, keep it sharp and
  declare it.** Doubts and claims come out of the same reading, so the overlap is the normal
  case, not a slip. Do not blunt a claim to protect a doubt: that spends the brief's main value
  to buy a corroboration credit which is not yours to grant in the first place (§9).

Before saving, verify the prompt against reality: open every `file:line` you cited and
confirm the quoted text is still on that line, and re-run the exact commands the prompt
prints to confirm they produce the output it promises. Then grep the saved draft for `«`
or `»` — a single leftover guillemet means an instruction meant for you is about to be
read by the reviewer; fail closed and fix it before handing anything off. The prompt is
itself a set of testable claims, and the reviewer will treat one stale citation as
evidence about all the others.

Save it beside the work being reviewed (e.g. `<phase-dir>/NN-EXTERNAL-REVIEW-PROMPT.md`),
not in a scratch directory — it is a durable artifact that the resulting review is read
against.

## 7. Declare the reviewer's operating envelope — and disclose it

State the envelope explicitly in the prompt, as its own block. An unstated envelope fails in
both directions: a reviewer that assumes it may not execute returns THEORETICAL findings it
could have CONFIRMED, and a reviewer that assumes it may do anything takes actions you did
not intend. Cover all six axes, even when the answer is "no":

| Axis | State plainly |
|---|---|
| **Reading** | The in-scope set from the prompt's Scope section, and whether it may read outside it (usually yes for context, e.g. lockfiles, CI config, sibling projects — say so) |
| **Writing** | Its own report file, always — that is the deliverable (§6). Everything else read-only by default; if further writes are authorized, exactly which paths, and the restore obligation |
| **Executing** | Which commands it may run — the test/typecheck/build commands, ad-hoc scripts, a REPL. Name the ones that are slow or destructive |
| **Network + installs** | Almost always **no**: no `npm install` of new packages, no fetching. If the project forbids network at runtime, that prohibition is itself a claim to audit — say which |
| **Its own tools** | Whether it may use web search, MCP servers, or subagents. Web search is usually worth allowing for CVEs and upstream library behavior; say if a finding sourced that way must cite the URL |
| **Effort budget** | Roughly how much time or how many findings you expect, and that depth beats breadth — one CONFIRMED finding is worth several THEORETICAL ones (credibility, never rank: impact alone decides rank) |

**Default to read-only-plus-the-report.** Say so in the prompt as one sentence, not two
scattered ones: read, run the test suite, write your report to `NN-EXTERNAL-REVIEW.md`, modify
nothing else. Stating the report write anywhere other than beside the read-only rule invites
the reviewer to resolve the apparent conflict on its own — usually by declining to write the
file, which loses the deliverable. For a plan or design target there is nothing to run: read,
write the report, modify nothing else.

Mutation testing is the one case that genuinely earns write access, because the real question
is not "do the tests pass" but "would they fail if the code were wrong." Deliberately invert
a comparison, drop a guard, remove a normalization step, and see whether the suite notices —
every silent survival is a guarantee with no enforcement behind it. Nothing else answers that
question. When you authorize it, bound it: throwaway probes in an obviously temporary
location, commit nothing, restore `src/` and `tests/` and any untracked files exactly as
found, report the tree clean at the end.

**Then tell the user.** The summary you give the user must contain one explicit line naming
every path the reviewer may write and every capability it is granted — the report file
included, plus any probe location, install, or exec permission. Not buried in the prompt file:
in the message. The user is not against an external model changing files — they want to be told
when you are allowing it, not to discover it mid-run. Silence here is the defect.

## 8. Write the paste-ready cover note

Assume the user does not drive a terminal. What they do is paste a message into the reviewer's
chat box, so give them exactly that message — a short cover note that points the reviewer at
the brief on disk. Do not expect them to paste a 400-line brief: a long markdown file through a
chat box arrives with its fences and tables mangled, and its opening instruction buried.

Follow [references/cover-note-template.md](references/cover-note-template.md).

Four decisions before you write it:

1. **Can the reviewer read the repo?** An agentic session rooted in or above the project
   (Codex CLI or its IDE extension, Cursor, Claude Code, Gemini CLI) can open the brief by
   path, and that is the case the cover note is for. A plain web chat cannot open a path and
   cannot write a report file — for that reviewer, do not emit a cover note at all. Say so in
   the hand-off: attach the brief as a file if the chat accepts uploads — most do, and an
   attachment preserves the structure a paste mangles — paste it whole only as a last resort,
   and the user saves the returned report by hand. Never emit an instruction the receiving
   model has no way to obey.
2. **The path as the reviewer will see it.** Write it relative to the directory that session is
   rooted at, and name that directory in the hand-off so the user can check. Where the project
   root and the session's working directory differ — a repo inside a parent folder is the
   common case — this is the single most likely thing to be wrong, and a brief the reviewer
   cannot open loses the run before it starts.
3. **What goes in — four parts and nothing else.** Context and authorization in the user's own
   register (what the software is, who it runs for, its actual exposure, that the user owns it
   and it is unreleased, and which class of defect they care about); the pointer to the brief;
   the two delivery instructions — write the report to `NN-EXTERNAL-REVIEW.md` as you go,
   return only a short summary in chat; and any host gotcha that would otherwise read as a
   finding (on Windows, `npm.cmd` rather than `npm` — the execution policy blocks the `npm.ps1`
   shim and it fails before npm starts, which looks exactly like a failing test suite).
   The authorization paragraph is load-bearing, not courtesy: a brief that opens with *attack
   this, find what is wrong, prove it* and no provenance reads like a request to break into
   someone else's system, and an unsure reviewer spends its output on hedges.
4. **What stays out.** The residual doubts (§10), because the cover note is read first and
   anchors hardest. The adversarial framing, because the brief carries it in full and a
   compressed restatement here both dilutes it and risks contradicting it.

Write the cover note **after** the brief, then check the two against each other: the brief
path, the report path, and every permission must agree exactly. The brief instructs the
reviewer to report contradictory instructions as a process finding — a cover note that says
read-only while the brief authorizes mutation will spend the run on that instead of on the
code. Repeating the delivery instructions in both places is deliberate; disagreeing in the two
places is the defect.

Save it as `<phase-dir>/NN-EXTERNAL-REVIEW-COVER-NOTE.md`, and grep it for `«` and `»` along
with the brief. Then reproduce it **verbatim in the hand-off message**, inside a single fenced
block, so the user can copy it in one gesture.

## 9. Cross-check the doubts against the saved brief — and do not rule on the result yourself

Because doubts and claims come from one reading of one body of work, a doubt is normally *about*
a claim you just wrote, and the sub-question pointing at that seam is the doubt. The damage is not
in the brief — it is in the hand-off, where the doubt gets reported as held back, the reviewer
raises it because the brief asked, and the agreement is then banked as independent corroboration.
This has now happened three times: 2026-08-10 (five doubts of five were in the brief), 2026-08-15
(four of four, reported as "deliberately excluded"), 2026-08-17 (two of three) — the last of these
*after* a search of the saved brief was made mandatory, and duly performed. It failed because the
author chose the queries: for a doubt whose own text quoted `unitScale && (rotation === 0 ||
isoBone)`, the recorded search was `packed`/`original`/`whitespace`/`strip`, none of which the
brief contained, while `isoBone` sat in claim 7. The one collision the search did surface was then
ruled "generic" by hand.

So take this literally: **you cannot certify absence in a document you wrote.** Over those three
runs, every wrong label was a claim of absence, and not one claim of presence — "prompted by claim
N" — was wrong. Presence is provable by pointing at a line. Absence is a claim about all six
hundred of them, made by the person who wrote them. Point, and let the adjudicator rule.

Run the search with no discretion in it. The queries come **from the doubt's own text** — every
`file:line` it cites, every backticked identifier, every SHOUTED term — never from your sense of
what the doubt is really about. One per line in a scratch file, then:

```bash
while IFS= read -r q; do printf '\n--- %s\n' "$q"
  grep -nF -- "$q" path/to/NN-EXTERNAL-REVIEW-PROMPT.md path/to/NN-EXTERNAL-REVIEW-COVER-NOTE.md \
    || echo '  no line'
done < queries.txt
```

A line citation often sits inside a range on the brief's side — the doubt says `:154`, the claim
cites `:129-155` — so when a citation query misses, run the bare path as well and read what cites
it. Then name, per doubt, the brief items the hits land in — "claim 7 at `:301`", "one-way door 1
at `:173`" — from anywhere in the brief, not only the claims list: on 2026-08-17 half the leak was
in the one-way doors, which the then-current rule did not cover. Where the queries turn up
nothing, the words are **"no line found — unverified"**. Never "held back", "withheld", or
"excluded from the brief": they assert what you are not in a position to know, they are the
signature of all three failures, and the adjudicator greps the hand-off for them.

Keep the doubts and the queries in the session scratchpad, never beside the brief — there they are
one `ls` away from the reviewer.

## 10. Hand off

Report to the user, briefly:
- The two file paths: the brief, and the cover note
- The cover note itself, verbatim in one fenced block, ready to paste
- Which directory the reviewer's session must be rooted at for the path in it to resolve
- The brief's scope and the number of load-bearing claims the reviewer must adjudicate
- The capability line from §7 — every path the reviewer may write, the report file included
- Where the report will land, and that they should check that file exists when the run ends
  rather than trusting the chat reply: the chat reply is a summary by design now
- Your 3–5 residual doubts, kept out of both the prompt and the cover note by design. For each
  one: the doubt, and what §9's search landed on — the brief items by id and line ("claim 7 at
  `:301`") or **"no line found — unverified"** — with the search output itself in one fenced
  block, so the labels can be checked instead of believed. Say plainly that none of it is a
  ruling: a doubt becomes independent corroboration only once an adjudicator has searched the
  brief and said so (`review-adjudication` does exactly that). Until then, a doubt the reviewer
  raised is a lead rather than a confirmation, a doubt it refuted is settled either way, and a
  doubt it never touched is still open
- One line, only if they use a terminal: the brief can also be piped —
  `codex exec "$(cat path/to/PROMPT.md)"` (bash/zsh) or
  `codex exec (Get-Content path/to/PROMPT.md -Raw)` (PowerShell). The cover note is the
  default path; this is the alternative, not the instruction.
- That the envelope is an instruction, not a sandbox: where a boundary matters (network, writes
  beyond the report file), the user should also enforce it with the receiving CLI's own
  permission flags

Do not offer to perform the review yourself.

</process>
