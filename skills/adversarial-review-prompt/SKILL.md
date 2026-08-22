---
name: adversarial-review-prompt
description: "Generate a targeted adversarial review prompt to hand to a different AI model — for independent audits, cross-model code review, red-teaming a plan or design, or second-opinion verification of work Claude itself produced. Use when the user asks for an external/independent/adversarial review, a prompt for another model (Codex, Gemini, GPT, Qwen, Cursor), something to paste into another model's chat box, a red-team of their own code, or wants their work attacked rather than confirmed. Produces an audit brief plus a paste-ready cover note that tells the reviewer to write its report to a file — never a review."
argument-hint: "<target: phase N | path | PR | diff | plan file> [--reviewer <model>] [--writes]"
allowed-tools:
  - Read
  - Grep
  - Glob
---

<objective>
Produce a single self-contained markdown prompt that a **different model** — one that did not
write the work — can be handed with no other context, and that maximizes the chance it finds
real defects instead of agreeing with the author.

You are writing the prompt. You are **not** performing the review. Do not review the work,
do not fix anything, do not summarize findings you noticed while reading. The deliverable is
two files: the audit brief, and a short paste-ready cover note that hands it over.
</objective>

<invariants>
**These hold for the whole task.** After an auto-compaction Claude Code re-attaches only the
**first 5,000 tokens** of this skill, so a later part of it can vanish mid-task with no signal.
**Estimated** cut: around line 221, from a measured ~3.1 characters per token on this file's
prose — an estimate, not a tokenizer run, and biased late if anything. Each rule below is stated
in full in its own section; this block is the copy that survives.

1. **You write the prompt. You do not perform the review.** The deliverable is two files —
   except for a reviewer with no filesystem, which gets the brief alone and no cover note.
   (objective, §6)
2. **The reviewer's identity is a required input and is never inferred.** It decides the
   calibration lookup, the envelope, and the independence framing. Ask when `$ARGUMENTS` is
   silent. (§1)
3. **Declare the operating envelope, and make brief and cover note agree exactly** — brief
   path, report path, and every permission. Disagreement between the two is the defect the
   reviewer will spend its run on. (§7, §8)
4. **The report is a file the reviewer creates as it works** — never a ship/no-ship verdict.
   The one exception is a reviewer with no filesystem: it returns the report in chat, the user
   saves it, and the hand-off must say so **and** tell the user to send one word to continue if
   the output stops at a section boundary. (§6, §7, §10)
5. **The residual-doubts *list* stays out of the brief and the cover note** — but a
   load-bearing claim that happens to overlap a doubt stays **sharp**, because the overlap is
   the normal case and blunting the claim spends the brief's whole value. §9's search then
   records what leaked. Where a query finds nothing the words are **"no line found —
   unverified"**; never "held back", "withheld", or "excluded from the brief". (§5, §9)
6. **Never overwrite an existing brief, cover note or report** — the report path you *name*
   for the reviewer counts, since a reviewer told to write an occupied path destroys it on your
   instruction. Check each with `ls`/`Glob`, take the next free name, bind the suffixes (a `-2`
   brief names a `-2` report), and say which you used. (§6, §8)
7. **Never claim independence you have not established.** The "different architecture"
   framing is conditional on the reviewer's identity **and the work's author provenance**,
   in four branches, each carrying its own payoff line. (§1, template §1)
</invariants>

<why_this_is_hard>
A brief is only worth what its reviewer can act on, and four things reliably destroy that value:

1. **Writing from memory or a summary** instead of the work — every unlocatable claim wastes a
   reviewer's run and teaches it the brief is unreliable.
2. **Claiming independence you have not established** — "you have a different architecture" is
   false when the brief goes to another session of the same family, and it inflates exactly the
   findings this exercise is least able to check.
3. **Leaking your own doubts into the brief and then banking the agreement as corroboration** —
   the reviewer answers the question you asked and you score it as a discovery.
4. **An envelope the cover note and brief state differently** — the reviewer spends its run on
   the contradiction instead of the work.

Each is stated in full, with the history behind it, in
[references/why-this-is-hard.md](references/why-this-is-hard.md).
</why_this_is_hard>

<process>

## 1. Fix the target and the reviewer

Resolve from `$ARGUMENTS` (ask only if genuinely ambiguous). **The reviewer is the one exception
to that parenthesis: it is a required input, and you never infer it.**

- **Target** — a phase, directory, file set, PR, diff range, or a plan/design doc. Get an
  exact file list with line counts; a reviewer needs to know the size of the job.
- **Reviewer** — which model/CLI receives this. **If `$ARGUMENTS` does not name it, ask, before
  anything else in this section.** The answer decides three things at once: which calibration
  record gets looked up, what file access the envelope may assume, and whether the same-family
  warning fires. None of the three can be resolved without it.

  **A habit is not an answer.** What this project used last time, what its history suggests,
  what is installed, what the docs were written around, what most users run — all inference, each
  producing a confident wrong answer as readily as a right one.

  **What a wrong guess costs:** the calibration lookup is keyed on identity, so a wrong name
  returns a different model's record — very possibly a `PASS` — and the hand-off then reports
  *this* reviewer as calibrated when it has never been tested. Nothing downstream catches it. A
  **missing** record costs one honest sentence; a **wrong** one is an error no later step can
  see. One question removes the second risk entirely.

  Once you have been told: adjust only the mechanics (how it runs commands, what it can
  access), never the adversarial framing. Name its **model family**, and
  say at hand-off when that family is the one that wrote the work. The whole return on this
  exercise is the architecture difference (lever 1) — a same-family reviewer buys much less of
  it, and a great many review tools are thin layers over a small pool of base models, so the
  product's name tells you nothing about whose eyes you are actually getting. Whether to proceed
  anyway is the user's call; leaving the lineage unnamed is not.
- **Calibration** — whether this reviewer has ever been shown to find anything. Look for
  `.adversarial-review/calibration/<reviewer-id>.md` under the project root, keyed on family,
  product and version, effort, and self-report; filename `<identity>-<effort>.md`. **List the
  directory before concluding there is no record.** Read its result, expiry, **and corpus
  digest** — recompute the digest with the command the record names and compare, because that is
  the only check that notices the instrument changing; where you lack the corpus, say staleness
  was unknowable rather than treating the record as current. Missing, expired or `FAIL` is normal
  and never a reason to refuse: run the review anyway. It changes one thing, said at hand-off
  (§10) — **an untested reviewer's findings still count, and its silence does not.** Its upheld
  list is not coverage and nothing it "cleared" may enter the next brief's §7. The corpus and its
  20-minute procedure live in the source repository, not the installed skill, so point at the URL
  once and do not campaign:
  https://github.com/Dzazaleo/adversarial-review-skills/tree/main/calibration

- **Author provenance — who wrote the work under review.** A required input, like the reviewer,
  and for the same reason: the independence sentence (template §1) is written from *both* sides
  and there is no truthful sentence to write without this half. Establish which model family
  authored it, or that it is human-written, mixed human/AI, written by several model families, or
  simply undetermined. **Ask when `$ARGUMENTS` and the target's own history are silent** — a
  repository's commit trailers usually settle it in one command. Do not infer it from the fact
  that Claude is reading it now: Claude reading a file is not Claude having written it, and that
  substitution is exactly how the unconditional "different architecture" claim got emitted for
  years.
- **Artifact kind** — code, or a plan/design. For a plan there is nothing to execute, so the
  evidence standard shifts from CONFIRMED-by-execution to "cite the source that contradicts
  it"; the brief's §6 becomes assumptions and one-way doors rather than runtime claims.
- **Write access** — beyond its own report file, which is always authorized (§6), read-only
  unless the user passed `--writes` or asked for mutation testing in words. This decides which
  write boundary the prompt's envelope gets (§7 below); never grant more on your own initiative.
- **Delivery route** — chat box or terminal. This follows from the reviewer you were told about,
  never from a default. Where the reviewer runs with filesystem access, the cover note (§8) is
  what the user pastes and the brief stays on disk for the reviewer to open. Where it is a
  browser chat window with no filesystem — which a great many are — a brief "on disk" names a
  file the reviewer cannot reach and the instruction to write its report to a file is inert.
  That case does not get a cover note at all: follow the **"Reviewer has no filesystem access"**
  variant in `references/cover-note-template.md`, which routes the brief to the reviewer as an
  attachment where the chat accepts uploads and has the user save the returned report
  themselves. Getting this wrong does not fail loudly. It produces a chat-window summary in
  place of a report file, which is the one artifact §10 tells the user not to trust. Where the
  reviewer's access is not obvious from what you were told, ask that too.

## 2. Read the actual work — never write the prompt from memory or from a summary

Read the source, the tests, the spec, and the prior review documents. Then run enough
commands to state facts, not guesses:

- File list + line counts for the in-scope set. **Produce every count by running the command
  in the session that writes the brief, and never carry one forward from a previous round's
  brief** — a stale inventory number sends the reviewer to audit the wrong size of file, and it
  has now shipped in three separate briefs here. Where the brief pins a range, take the counts
  at the pinned commit (`git show <sha>:<path> | wc -l`), not from the working tree
- The test/typecheck/build commands and what a *passing* run actually prints. **Check each one
  against the write envelope you are about to declare (§7).** A command that writes into the
  repository — a bare `pytest` leaving `__pycache__`, a snapshot-updating runner, a cache-writing
  build — contradicts "modify nothing else" the moment the reviewer obeys both. Where one does,
  say in the brief where to run it instead (a copy under `/tmp`) rather than leaving the reviewer
  to invent a resolution. Two reviewers independently inventing the same workaround is what this
  costs when it is left unstated
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

**Then ask for an unseeded pass beside them** — the template's §6b, and it is not optional whenever
a claims list exists. A list this directed is where the confirmed defects come from, and it is also
why a reviewer's coverage collapses to the seams you named: measured twice on this repository,
10 of 15 findings and then 6 of 9 were echoes of the sub-questions, with one finding in nine
reached unprompted. Requiring a separately-reported pass that sets the list aside is what stops the
next adjudicator having to discount the whole report's silence to nothing. A considered "nothing"
from that pass is a result, not a failure.

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
may be present at `references/example-audit-prompt.md` (named, deliberately not linked —
it ships absent by default); it is optional, so skip it without comment if absent. Read it when you need to see the
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
- **Forbid upholding a claim on the author's own word.** A comment, a test name, or a docstring
  is the party under review talking (lever 2) — it is what the claim rests on, never what
  confirms it. Say plainly that confirming a claim takes what refuting one takes, execution or a
  primary source outside the work, and that COULD NOT DETERMINE is the honest alternative. The
  shape to name as unacceptable is the reviewer that gets as far as a defect and then decides the
  work meant it, on the authority of a nearby comment or of a test written around the behavior as
  it stands. Rank that below missing the defect outright: it leaves the next reader both the bug
  and a written case for keeping it. If the reviewer got that far it reports the finding and says
  why it thinks the behavior is deliberate — a finding with a note, never a dismissal.
- **Specify the deliverable shape** — a coverage line, findings in a strict ranked order,
  claims examined and upheld (one line each, naming what upheld it), could-not-verify (an
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

**Never overwrite an existing brief, cover note or report.** All three, not just the two you
are about to write: the report path you *name* for the reviewer is the third artifact in the same
evidence chain, and a reviewer told to write an occupied path will destroy it on your instruction.
Run the check rather than intending it — `ls <path>` or `Glob` on each of the three — and where a
file is already there, take the next free name (`-2`, `-3` for a later round over the same target,
`-<reviewer>` for a second reviewer in the same round). **Bind the suffixes: a `-2` brief names a
`-2` report, a `-grok` brief names a `-grok` report.** Say in the hand-off which names you used and
what was already occupying the first. A spent brief is not scratch: the
adjudication ledger's echo audit is scored *against* it, and the next brief's "ground already
walked" section is read out of it. Destroying one silently deletes the evidence later rounds
are graded on, and nothing downstream can tell that it happened.

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
| **Its own tools** | Whether it may use web search, MCP servers, or subagents. Web search is usually worth allowing for CVEs and upstream library behavior; say if a finding sourced that way must cite the URL. Where the target is public, its issue tracker and PR prose can state a defect outright — a finding lifted from there is a lookup, not a discovery, so require the URL and say it will be weighed as one |
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

Save it as `<phase-dir>/NN-EXTERNAL-REVIEW-COVER-NOTE.md` — **under §6's no-overwrite rule,
which applies to this file too**, and carrying the same suffix as its brief, since a `-2` brief
with an unsuffixed cover note stops the pair being findable. Grep it for `«` and `»` along
with the brief. Then reproduce it **verbatim in the hand-off message**, inside a single fenced
block, so the user can copy it in one gesture.

## 9. Cross-check the doubts against the saved brief — and do not rule on the result yourself

Because doubts and claims come from one reading of one body of work, a doubt is normally *about*
a claim you just wrote, and the sub-question pointing at that seam is the doubt. The damage is not
in the brief — it is in the hand-off, where the doubt gets reported as held back, the reviewer
raises it because the brief asked, and the agreement is then banked as independent corroboration.
This has happened in every round that recorded it — most recently *after* the search was made
mandatory and duly performed, because the author chose queries its own brief did not contain.
**So do not choose the queries: take them from the doubt's own text** — its citations, its
identifiers, the exact strings it quotes — and search the brief **and the cover note**, not just
the claims list. Record per doubt the query and what it found. The case histories are in
[references/why-this-is-hard.md](references/why-this-is-hard.md).

Keep the doubts and the queries in the session scratchpad, never beside the brief — there they are
one `ls` away from the reviewer.

## 10. Hand off

Report to the user, briefly:
- The two file paths: the brief, and the cover note
- The cover note itself, verbatim in one fenced block, ready to paste
- Which directory the reviewer's session must be rooted at for the path in it to resolve
- The brief's scope and the number of load-bearing claims the reviewer must adjudicate
- The reviewer's model family, and plainly whether it is the same family that wrote the work
- Its calibration state in one sentence — passing and until when, or that there is none on file.
  Where there is none, say what it costs and nothing more: if this reviewer comes back with
  findings you adjudicate them exactly as you would any other, and if it comes back clean that
  result is inconclusive rather than an all-clear. Point once at the calibration URL above — six
  cases, about twenty minutes, and it is per model rather than per review, so it is paid once.
  Do not hold up the hand-off over it or repeat the recommendation
- The capability line from §7 — every path the reviewer may write, the report file included
- Where the report will land, and that they should check that file exists when the run ends
  rather than trusting the chat reply: the chat reply is a summary by design now
- **Only for a reviewer with no filesystem: that they must send a single "continue" if the
  report stops at a section boundary.** The brief tells the reviewer to stop there and wait; the
  reviewer cannot resume itself, so if this never reaches the user a truncated report gets filed
  as a complete one — which is the whole failure the instruction exists to prevent
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
