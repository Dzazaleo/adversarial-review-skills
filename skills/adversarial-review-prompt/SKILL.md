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
**first 5,000 tokens** of this skill; where several skills were invoked they share a 25,000-token
budget and an older one can be dropped **entirely**. Treat everything past **line ~205** as gone —
**an estimate back-computed at ~3.1 characters per token, not a tokenizer run, and deliberately
early** — and re-invoke this skill after a compaction. Each rule is stated in full in its section.

**The references, and when to open each.** `prompt-template.md` before writing any part of the
brief — **it is the authority on the framing block and its four branches** ·
`cover-note-template.md` before writing the cover note, including the no-filesystem variant ·
`example-audit-prompt.md` for a worked brief **where it exists — it ships absent by default, so
skip it without comment** · `why-this-is-hard.md` is background only —
**this file and the template override it wherever they differ.**

1. **You write the prompt. You do not perform the review.** The deliverable is two files —
   except for a reviewer with no filesystem, which gets the brief alone and no cover note.
   (objective, §6)
2. **The reviewer's identity, its reasoning effort, and how many reviewers there are are
   required inputs, never inferred.** Identity keys the calibration lookup, the envelope and the
   independence framing; effort is that key's other half and survives in no report; and with
   several reviewers, what you vary between them is what their agreement is later worth. Ask when
   `$ARGUMENTS` is silent. (§1)
3. **Declare the operating envelope, and make brief and cover note agree exactly** — brief
   path, report path, and every permission. Disagreement between the two is the defect the
   reviewer will spend its run on. (§7, §8)
4. **The report is a file the reviewer creates as it works** — never a ship/no-ship verdict.
   The one exception is a reviewer with no filesystem: it returns the report in chat, the user
   saves it, and the hand-off must say so **and** tell the user to send one word to continue if
   the output stops at a section boundary. (§6, §7, §10)
5. **Residual doubts are formed in §9, *after* the brief is saved — never alongside the
   claims, and never inside the brief or the cover note.** Collected while mining claims they
   are a copy of the claims: five of five leaked, most recently 2026-08-23. §9's search buckets
   each as **SEEDED** (the brief asks it — never corroboration, though a calibrated reviewer's
   silence on it is evidence) or **UNSEEDED** (the only corroboration-eligible bucket). Never
   blunt a claim to move a doubt. Where a query finds nothing the words are **"no line found —
   unverified"**; never "held back", "withheld", or "excluded from the brief". (§6, §9, §10)
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
**writing from memory or a summary** instead of the work, so unlocatable claims waste the run and
teach the reviewer the brief is unreliable · **claiming independence you have not established**,
false for a same-family reviewer and inflating exactly the findings this exercise can least check ·
**forming your doubts out of the same reading that wrote the brief**, so the reviewer answers the
question you asked and you bank it as a discovery · **an envelope the cover note and brief state
differently**, which the reviewer spends its run on instead of the work.

Each in full, with its history: [references/why-this-is-hard.md](references/why-this-is-hard.md).
</why_this_is_hard>

<process>

## 1. Fix the target and the reviewer

Resolve from `$ARGUMENTS` (ask only if genuinely ambiguous). **The reviewer is the one exception
to that parenthesis: it is a required input, and you never infer it.**

- **Target** — a phase, directory, file set, PR, diff range, or a plan/design doc. Get an
  exact file list with line counts; a reviewer needs to know the size of the job.
- **Reviewer** — which model/CLI receives this, **at what reasoning effort, and how many of
  them**. **If `$ARGUMENTS` does not name all three, ask, before anything else in this section.**
  Identity decides the calibration lookup, what file access the envelope may assume, and whether
  the same-family warning fires.

  **A habit is not an answer** — last time's reviewer, what is installed, what the docs assume:
  all inference. **And a wrong guess costs more than no answer**, because a wrong name returns a
  *different* model's record, very possibly a `PASS`, and the hand-off then reports this reviewer
  as calibrated when it was never tested. Nothing downstream catches it.

  Once you have been told: adjust only the mechanics (how it runs commands, what it can
  access), never the adversarial framing. Name its **model family**, and
  say at hand-off when that family is the one that wrote the work. The whole return on this
  exercise is the architecture difference (lever 1) — a same-family reviewer buys much less of
  it, and a great many review tools are thin layers over a small pool of base models, so the
  product's name tells you nothing about whose eyes you are actually getting. Whether to proceed
  anyway is the user's call; leaving the lineage unnamed is not.

  **Effort is the other half of the calibration key and appears in no report**, so the brief is
  the last chance to record it — until 2026-08-24 no brief ever did, leaving two rounds
  adjudicated unverified on it. Put it in the brief's identity line; `not exposed` where the
  reviewer has no such setting.

  **And where there are several reviewers, vary something real between them.** Two handed the same
  brief are not independent (`review-adjudication` §5) — in round 1, 3 of 27 findings across three
  reviewers were free of the brief's direction. Split the **scope** (disjoint file sets, the union
  is the audit) or the **directed set** (one gets §3's claims list, another the same ground with
  only the template's §6b unseeded pass). Varying nothing is legitimate and buys corroboration on
  nothing; either way say at hand-off which reviewer received which, because the adjudicator rules
  independence off that line alone.
- **Calibration** — whether this reviewer has ever been shown to find anything. Look for
  `.adversarial-review/calibration/<reviewer-id>.md` **in two places — project root first, then
  `~/`** — keyed on family, product and version, effort and self-report; filename
  `<identity>-<effort>.md`. **`ls` both before concluding there is none** (2026-08-23: a passing
  reviewer reported as untested because only the project root was checked), and name at hand-off
  which you read. **Project-local wins on location, not freshness**, so a stale pin shadows a
  better home copy: open both, and flag any disagreement beyond the result. Read result, expiry
  **and corpus digest** — recompute it with the command the record names, the only check that
  notices the instrument changing. **A mismatch is not proof the corpus moved**: rule out
  collation, `shasum`'s platform-dependent output mode, and a CRLF checkout — that closed list and
  nothing else — before recording stale; without the corpus, staleness is unknowable, not current.
  Missing, expired or `FAIL` is normal and never a reason to refuse: run the review anyway. It
  changes one thing, said at hand-off (§10) — **an untested reviewer's findings still count, and
  its silence does not.** Its upheld list is not coverage and nothing it "cleared" may enter the
  next brief's §7. Corpus and 20-minute procedure, pointed at once and never campaigned for:
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
- **Delivery route** — chat box or terminal, following from the reviewer you were told about and
  never from a default; ask where its access is not obvious. With filesystem access, the cover
  note (§8) is what the user pastes and the brief stays on disk for the reviewer to open. In a
  browser chat window with none — which a great many are — a brief "on disk" names a file the
  reviewer cannot reach and "write your report to a file" is inert, so that case gets no cover
  note at all: follow the **"Reviewer has no filesystem access"** variant in
  `references/cover-note-template.md`, which attaches the brief where the chat accepts uploads and
  has the user save the returned report. Getting this wrong does not fail loudly; it produces a
  chat-window summary in place of a report file, the one artifact §10 tells the user not to trust.

## 2. Read the actual work — never write the prompt from memory or from a summary

Read the source, the tests, the spec, and the prior review documents. Then run enough
commands to state facts, not guesses:

- File list + line counts for the in-scope set. **Produce every count by running the command
  in the session that writes the brief, and never carry one forward from a previous round's
  brief** — a stale inventory number sends the reviewer to audit the wrong size of file, and it
  has now shipped in three separate briefs here. **The rule covers every carried-forward fact,
  not counts alone** — a `file:line` from the last round points into a file that has moved
  underneath it, and on 2026-08-24 two of three stale citations caught in a round-2 draft arrived
  exactly that way. Where the brief pins a range, take the counts
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
  authoring the brief so the numbers are observed, not remembered. **Any other size you quote —
  "it went from N lines to M" — is computed the same way and the command is shown beside it**
  (`git show «commit»:«path» \| wc -l`); round 7 shipped a brief asserting a 354-line baseline for
  a file that was 301 at the pinned commit, and the reviewer had to spend a finding on it. Never write "N commits
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

**Then ask for an unseeded pass beside them** — the template's §6b, never optional once a claims
list exists. A list this directed is where the confirmed defects come from, and also why a
reviewer's coverage collapses to the seams you named: measured twice here, 10 of 15 findings then
6 of 9 were echoes of the sub-questions, one in nine reached unprompted. A separately-reported pass
that sets the list aside is what stops the next adjudicator discounting the report's whole silence
to nothing, and a considered "nothing" from it is a result, not a failure.

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

Identify what becomes expensive to change once downstream consumers exist — published schemas,
hashes, file formats, wire protocols, exit codes, public APIs. State who will consume them, why a
design flaw found now beats any implementation bug, and that this is where to spend attention.

## 6. Write the prompt file

Follow [references/prompt-template.md](references/prompt-template.md) for section order and the
exact framing language. A worked example may sit at `references/example-audit-prompt.md` (named,
not linked — it ships absent by default, so skip it without comment); read it for register and
level of specificity, never to copy its content.

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
- **Never ask the reviewer for a verdict.** Whether the work ships is the owner's call, and a
  reviewer that commits to YES or NO up front bends its findings to stay consistent. Forced
  ranking buys the commitment better: order findings by the cost of leaving each unfixed — blast
  radius × likelihood the trigger is reached — no ties, one clause per position. **Impact**
  (critical/high/medium/low) is an attribute, never a section heading: buckets are how a reviewer
  avoids saying which of six "criticals" it would fix first. Evidence status is not impact — a
  THEORETICAL data-loss defect outranks a CONFIRMED cosmetic one. Per-claim adjudication (§3) is
  evidence about a claim, not a verdict, and stays.
- **Your own suspicions appear nowhere in the prompt, nor in the cover note (§8), which is read
  first and anchors hardest.** Write this file as if you held none: every seam you can see belongs
  in §3's claims list, **sharp**. Do not collect a doubts list here either — that is §9's job, and
  it runs *after* this file is saved, precisely so the doubts are formed against what the brief
  turned out to ask rather than out of the same reading that wrote it.

Before saving, verify the prompt against reality: open every `file:line` you cited and
confirm the quoted text is still on that line, and re-run the exact commands the prompt
prints to confirm they produce the output it promises. Then grep the saved draft for `«`
or `»` — a single leftover guillemet means an instruction meant for you is about to be
read by the reviewer; fail closed and fix it before handing anything off. The prompt is
itself a set of testable claims, and the reviewer will treat one stale citation as
evidence about all the others.

Save it beside the work being reviewed (e.g. `<phase-dir>/NN-EXTERNAL-REVIEW-PROMPT.md`), not in a
scratch directory — it is a durable artifact that the resulting review is read against.

**Never overwrite an existing brief, cover note or report.** All three, not just the two you are
about to write: the report path you *name* is the third artifact in the same evidence chain, and a
reviewer told to write an occupied path destroys it on your instruction. Run the check rather than
intending it — `ls <path>` or `Glob` on each — and where a file is there take the next free name
(`-2`, `-3` for a later round over the same target, `-<reviewer>` for a second reviewer in the same
round). **Bind the suffixes: a `-2` brief names a `-2` report.** Say in the hand-off which names
you used and what occupied the first. A spent brief is not scratch — the adjudication ledger's echo
audit is scored *against* it and the next brief's "ground already walked" is read out of it, so
destroying one deletes the evidence later rounds are graded on, silently.

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

Assume the user does not drive a terminal: what they do is paste a message into the reviewer's
chat box, so give them exactly that — a short cover note pointing at the brief on disk. Never
expect them to paste a 400-line brief; through a chat box its fences and tables arrive mangled and
its opening instruction buried.

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

## 9. Now form the residual doubts — against the saved brief, not from the reading that wrote it

**Order is the fix here, not a sharper search.** Doubts mined alongside the claims are a copy of
the claims — same reading, same seams — and every round that measured it found them already in the
brief: 5 of 5, 4 of 4, 2 of 3, then 5 of 5 again on 2026-08-23 with the search correctly run *and*
correctly reported. So brief and cover note reach disk first, then this.

**Re-read the saved brief — the file, not your memory of writing it** — and only then ask what you
still doubt, aimed at what the brief turned out *not* to ask: a seam dropped for space, ground §5
deprioritized, the assumption under a claim rather than the claim. Up to five, each a question
with a mechanism and its `file:line` — fewer is fine, and none is itself a result.

**Then classify each by search, with no discretion in it.** Queries come from the doubt's own text
— its citations, identifiers, the exact strings it quotes — never from your sense of what it is
really about; author-chosen queries defeated this check on 2026-08-17. Search the brief **and the
cover note** — the brief alone where the reviewer gets none (§8) — whitespace-normalized. Each
doubt lands in exactly one bucket:

- **SEEDED** — the query hit. The brief asks it, so agreement can never be corroboration. It still
  belongs in the hand-off: a **calibrated** reviewer pointed at a seeded doubt and silent on it is
  evidence — about the doubt, or about the reviewer.
- **UNSEEDED** — no line found. The only corroboration-eligible bucket, and even then only once an
  adjudicator runs its *own* search and rules it absent. Yours is a report, never a ruling.

**Never blunt or drop a claim to move a doubt into UNSEEDED**; that spends the brief's main value
for a credit which was not yours to grant. Where one lands SEEDED, try once for an unseeded
successor — what would still worry you if the brief's question came back answered — and where there
is none, say so: **"no unseeded doubts" is a result**, an unlabelled empty list is not.

Record per doubt the query and its verbatim output, in the session scratchpad and never beside the
brief, where it is one `ls` away from the reviewer. Search loop and case histories:
[references/why-this-is-hard.md](references/why-this-is-hard.md).

## 10. Hand off

Report to the user, briefly:
- The brief's path — and, **for a reviewer with a filesystem**, the cover note's path too
- **For a reviewer with a filesystem:** the cover note itself, verbatim in one fenced block, ready
  to paste. **For a reviewer without one:** no cover note exists — tell the user to attach the
  brief to the chat, and that the report comes back in chat for them to save
- Which directory the reviewer's session must be rooted at for the path in it to resolve
- The brief's scope and the number of load-bearing claims the reviewer must adjudicate
- The reviewer's model family **and the effort it runs at** (§1), and plainly whether that family
  wrote the work — effort appears in no report the adjudicator will later read
- **With several reviewers: what you varied, and which received which** (§1). "The same brief to
  all" is legitimate and must be given in those words; an unstated split reads as arranged
  independence
- Its calibration state in one sentence — passing and until when, **and which of the two
  locations the record came from** (`~/` or this project), or that there is none on file *after
  listing both*. Where there is none, say what it costs and nothing more: findings are adjudicated
  exactly as any other reviewer's, and a clean result is inconclusive rather than an all-clear.
  Point once at the calibration URL above — six cases, twenty minutes, filed at `~/` and so paid
  once per reviewer, not once per project. Do not hold up the hand-off or repeat it
- The capability line from §7 — every path the reviewer may write, the report file included
- Where the report will land. **For a reviewer with a filesystem**, that they should check that
  file exists when the run ends rather than trusting the chat reply, which is a summary by design.
  **For one without**, that the user is the one who saves it
- **Only for a reviewer with no filesystem: that they must send a single "continue" if the
  report stops at a section boundary.** The brief tells the reviewer to stop there and wait; the
  reviewer cannot resume itself, so if this never reaches the user a truncated report gets filed
  as a complete one — which is the whole failure the instruction exists to prevent
- **Last in the hand-off, in its own copy-ready block: §9's doubts, under two headings —
  `SEEDED (n)` and `UNSEEDED (n)`.** Both headings every round, even at zero: a missing heading
  and a zero count must never read the same. Under each doubt give its text, the query §9 ran, and
  that query's verbatim output — by id and line ("claim 7 at `:301`") or **"no line found —
  unverified"** — so the label can be checked instead of believed. **Chat-only, never written to
  disk**, because a file is one `ls` away from a reviewer session rooted more broadly than you
  expected. Tell the user to keep the message until the adjudicator asks for it, and that if the
  window is lost the list is lost. **There is no durable channel and inventing one is not yours to
  do**: do not write the list to disk, fold it into the brief, or arrange any other route the
  adjudicator could read without the user. Losing the window costs one round's corroboration
  scoring; leaking it costs the corroboration itself. None of it is a ruling — an UNSEEDED doubt becomes corroboration only once an
  adjudicator runs its own search and says so.
- One line, only if they use a terminal: the brief can also be piped —
  `codex exec "$(cat path/to/PROMPT.md)"` (bash/zsh) or
  `codex exec (Get-Content path/to/PROMPT.md -Raw)` (PowerShell). The cover note is the
  default path; this is the alternative, not the instruction.
- That the envelope is an instruction, not a sandbox: where a boundary matters (network, writes
  beyond the report file), the user should also enforce it with the receiving CLI's own
  permission flags

Do not offer to perform the review yourself.

</process>
