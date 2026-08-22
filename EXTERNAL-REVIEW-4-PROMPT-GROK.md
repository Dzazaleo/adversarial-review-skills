# Adversarial audit — the ten fixes applied from external review 3

*(Second-reviewer edition. A different model is auditing the same range in parallel from its own copy of this brief. See "What you must not read" in §8 — it is the one instruction here that protects the value of your report.)*

You are auditing a small repository of two Claude Code "skills" — structured markdown instruction
files that a coding agent loads and follows — plus a calibration corpus and the accumulated
adjudication history of three prior review rounds. The skills' subject matter is running and
adjudicating cross-model reviews, which means **this repository is an instance of the thing it
describes**, and it is currently being used on itself. That is not a curiosity; it is the main
source of the defects you are looking for.

> Every line of the work you are about to audit was written by one model, reviewed by that same
> model, and adjudicated by that same model against a ledger it also wrote. The ten changes under
> review currently read as complete: every one is marked `✔ executed` in the ledger with a
> description of what landed, and the repository's only test suite reports `8 passed`.
>
> That is exactly the problem. A model validating its own work carries the same blind spots into
> the review that it had while writing — the same misreadings, the same unexamined assumptions, the
> same things it never thought to check because it never thought of them at all. This work was
> written by Anthropic's Claude. You are xAI's Grok. You have a different architecture and
> different training. **You will notice different things, and those things are the entire value
> of this exercise.**
>
> - **Confirmation is near-worthless output.** If you spend your effort re-deriving what the ledger
>   already claims and agreeing, this audit has failed.
> - **Your job is to find what is wrong, missing, or unjustified**, and to prove it.
> - **A manufactured finding is worse than no finding.** If a rigorous search comes back nearly
>   empty, say so and show the search — few or zero findings is an admissible result, and the
>   claims-examined-and-upheld section is where it earns its credibility.
> - **A finding that survives your own attempt to refute it is worth more than ten observations.**
>
> Assume competence, not correctness. Where this is wrong, it is wrong in ways its author cannot
> see — those places are what you are here for.

## 1. The single most important instruction

**This repository's prose asserts its own correctness constantly, and every such assertion is a
claim by the party under review, never evidence.** In a code audit the tell is a confident comment;
here the tells are a ledger row that says `✔ executed`, a description of what a fix accomplished,
and an invariant that states a rule as though stating it enforced it.

Real examples, quoted, all of which you should treat as untested assertions:

> `REVIEW-ADJUDICATION.md` — *"**✔ executed 2026-08-22** — two edits… the blindness claim is
> narrowed from 'never sees the report' to 'is never *handed* the report'"*

> `review-adjudication/SKILL.md:32` — *"**Write boundary.** The only files this skill creates or
> edits are the ledger, `FIX LATER` backlog artifacts, and… the report file materialized from it.
> Never the code, the plans, or an existing review, **whatever the tool grants allow.**"*

> `adversarial-review-prompt/SKILL.md:41` — *"**Never overwrite an existing brief or cover note.**"*

> `REVIEW-ADJUDICATION.md` §R3.14 — *"**pass** — both `<invariants>` blocks well above the
> recomputed cut band"*

Each states that something is true. None demonstrates it. **The gap between "the document says the
rule" and "the rule holds" is the seam this entire audit runs along.** A fix that consists of
adding a sentence saying the defect is now handled has not necessarily handled it, and the ledger
cannot tell the difference because the ledger is written by the same author as the sentence.

**Do not uphold any claim on the strength of the ledger's description of it.** Open the file, read
the actual text at the actual line, and decide for yourself.

**One more source of confident error, specific to you.** Several claims below turn on what
**Claude Code specifically** does — whether `allowed-tools` grants or restricts, whether
`disallowed-tools` exists, how much of a skill survives auto-compaction. Agentic coding tools
have converged on similar-looking skill formats, and yours may implement something that looks
like the thing described here. **That is not evidence.** Answer those claims from Anthropic's
published documentation with the URL cited, or return `COULD NOT DETERMINE`. A confident answer
derived from how your own harness behaves is the single most expensive wrong finding this brief
can produce, because it will read as authoritative and I am poorly placed to catch it.

## 2. Environment and how to run things

- Repository root: the directory containing `README.md`, `HOW-IT-WORKS.md`, `skills/`,
  `calibration/`. No build, no CI, no task runner, no linter — verified absent.
- The only executable tests are two fixtures inside the calibration corpus:
  ```
  python3 -m pytest -q calibration/cases/clean-wordcount calibration/cases/trap-unfalsifiable-test
  ```
  A passing run prints `8 passed` and nothing else of note. **These test the fixtures, not the
  skills.** Nothing in this repository tests the skills, which is a known and already-deferred
  finding (`BACKLOG.md` `B-3`) — do not re-report it, but see claim 20.
- `git status` at audit start is clean apart from two untracked `__pycache__/` directories, which
  are pre-existing pytest droppings and are not part of the work.
- **The audit range is pinned to immutable commits: `fe9bbac..540c60a`** — a single commit,
  `540c60a`, *"Adjudicate external review 3 and apply the ten fixes it earned"*. Over that exact
  range, `git diff --stat` reports **7 files changed, 951 insertions(+), 19 deletions(-)**. Run it
  yourself and say so if those numbers differ.
- **`HEAD` may be ahead of `540c60a`.** This brief is itself a file being added on top of the
  reviewed range, and the ledger has one appended correction section written after the commit.
  That is expected, not a finding — but the *content* of that appended correction is in scope, and
  is claim 21.
- YAML frontmatter can be checked with:
  ```
  python3 -c "import yaml,io,glob;[print(f,yaml.safe_load(io.open(f).read().split('---\n')[1])) for f in sorted(glob.glob('skills/*/SKILL.md'))]"
  ```

## 3. Scope

**In scope — the seven files touched by `540c60a`, at that commit:**

| File | Lines at `540c60a` |
|---|---|
| `skills/review-adjudication/SKILL.md` | 572 |
| `skills/adversarial-review-prompt/SKILL.md` | 497 |
| `skills/adversarial-review-prompt/references/prompt-template.md` | 467 |
| `calibration/README.md` | 162 |
| `BACKLOG.md` | 93 |
| `REVIEW-ADJUDICATION.md` (the round-3 section and its appended correction) | 2,466 total |
| `EXTERNAL-REVIEW-3.md` (the report being answered — read as input, not as work) | 119 |

**Also read, as context and as the standard the work is measured against, but not itself under
review:** `skills/review-adjudication/references/ledger-template.md` (217),
`skills/adversarial-review-prompt/references/cover-note-template.md` (91), `README.md`,
`HOW-IT-WORKS.md`, and the round-1 and round-2 sections of `REVIEW-ADJUDICATION.md`.

**Explicitly out of scope:** the calibration corpus cases themselves, `EXTERNAL-REVIEW.md` and
`EXTERNAL-REVIEW-2.md` (spent reports, history), and `examples/`.

## 4. The contract this work must satisfy

The ten changes were made to close eleven findings from an unscoped audit. The contract is:

1. **Each fix actually closes the finding it names** — not merely mentions it, restates it, or
   relocates it into a different file.
2. **No fix opens a new path to the failure it closed**, or to a different failure.
3. **The skills remain internally consistent** — an invariant hoisted to the top must not
   contradict, or silently drift from, the full rule it summarizes.
4. **Claims about enforcement are true.** Where the prose says a boundary holds, either a mechanism
   holds it or the prose says plainly that it does not.
5. **The ledger is an accurate record.** A row saying `✔ executed` must describe what actually
   landed, and a round marked closed must satisfy the closure definition the skill states.

## 5. Load-bearing claims — attack these

Return **CONFIRMED**, **REFUTED**, or **COULD NOT DETERMINE** for each of the 24 below, one line
each, in your report's "Claims examined and upheld" or findings sections as appropriate. Each names
the file and line where it lives.

### Group A — the permission fix (`R3-F1`)

1. **Both skills' grants are now `Read, Write, Grep, Glob`** (`adversarial-review-prompt/SKILL.md:5-10`,
   `review-adjudication/SKILL.md:5-10`), and this closes the finding that the skills pre-approved
   unrestricted `Bash`. *Does it? `Write` is still granted unconditionally to any path. The finding
   was that a prose write envelope sat over a broad permission grant — is that still exactly the
   situation, one notch smaller?*
2. **The adjudication ledger identified `disallowed-tools` as a real in-frontmatter restriction and
   it was deliberately not adopted** (`REVIEW-ADJUDICATION.md` §R3.13 Q1). *The write boundary at
   `review-adjudication/SKILL.md:32` is stated as absolute — "whatever the tool grants allow". Is
   there any mechanism behind it now, or is invariant 1 a wish? What would `disallowed-tools` have
   cost here that the ledger did not weigh?*
3. **Dropping `Agent` from `review-adjudication`'s grant went beyond the owner's locked decision and
   is recorded as such** (`REVIEW-ADJUDICATION.md` §R3.3 row `R3-F1`). *The skill mandates a
   subagent second opinion for high-impact refutations (`:439`). Does that escalation now require a
   permission prompt at precisely the moment it is most needed, and does an adjudicator facing a
   prompt reach for the documented fallback — `COULD NOT DETERMINE` — instead of the check?*
4. **Removing `Bash` does not prevent the skills doing their job, it only prompts.** *
   `review-adjudication` §5 is almost entirely `Bash`-driven re-verification. Is there a plausible
   behavioural regression here — an adjudicator running fewer checks because each one prompts? The
   ledger raises this itself in §R3.14 and explicitly declines to rule on it. Rule on it.*

### Group B — the compaction fix (`R3-F2`)

5. **An `<invariants>` block now sits at `adversarial-review-prompt/SKILL.md:22-45` and
   `review-adjudication/SKILL.md:26-50`, above the point where auto-compaction truncates.**
   *Claude Code re-attaches only the first 5,000 tokens of an invoked skill after compaction. Has
   anyone tokenized these files, or is "well above the cut band" derived from a word-count
   heuristic? Where does 5,000 tokens actually land in each file?*
6. **The fix made both files longer — 463→497 and 523→572 lines — and the ledger records this as a
   cost** (`REVIEW-ADJUDICATION.md` §R3.14). *Is this a net improvement or a net regression?
   Quantify: what fraction of each file fell past the cut before the change, and what fraction
   falls past it now? `review-adjudication` is now 72 lines past the documented 500-line guidance.*
7. **The invariants summarize rules stated in full later, and do not contradict them.** *Check each
   of the six/seven against its full section. Specifically: invariant 4 says a `FIX LATER` artifact
   is "created **before** the ledger is written" — does §6 say the same? Invariant 5 says the second
   opinion "was not handed the report" — does `:439` say the same, or something stronger?*
8. **Invariant 4 was violated by the very ledger that introduced it** — `REVIEW-ADJUDICATION.md`
   §R3.3 row `R3-F6` records that `BACKLOG.md` `B-3` was written *after* the ledger row rather than
   before. *Is a rule its own author breaks in the adjacent paragraph an impractical rule, a
   mis-stated one, or simply one that was missed? Does the recorded slip actually matter, given the
   artifact exists and is complete?*

### Group C — the residual-doubts fix (`R3-F3`)

9. **`review-adjudication/SKILL.md:145-155` makes the author's residual doubts a named step-1
   input.** *The finding was that no durable source exists. The fix says to ask the user to paste
   the hand-off. Does that close the finding or restate the dependency it named? `README.md`
   still tells the operator nothing depends on keeping the authoring session open — check whether
   that line was updated.*
10. **The fallback — "where unavailable, record that and score no finding as independent
    corroboration" — is safe.** *Does it hand an adjudicator a cheap exit? Declaring the doubts
    unavailable is one sentence and removes an entire obligation. Is there anything that makes the
    declaration costly or checkable?*

### Group D — the subagent-isolation fix (`R3-F4`, and owner decision Q4)

11. **The blindness claim at `review-adjudication/SKILL.md:269-277` is now narrowed to "is never
    *handed* the report", with an explicit statement that this is not the same as being unable to
    read it.** *Now grep the whole file for every remaining use of "blind" and "never saw". Line
    `439` reads: "**That same verdict also requires a second opinion that never saw the report.**"
    Is that the qualified claim or the original one? Did the fix reach every site, or only the one
    the reviewer cited?*
12. **The escalation at `:467-476` requires the ledger to record, beside the verdict, that the
    verifier could have read the report** (owner decision Q4(b)). *Does `ledger-template.md` have a
    field for it? `:31` has a "Reviewer isolation" line — is that the same thing, or is it about
    external reviewers rather than the subagent? If there is no field, will the requirement survive
    contact with the template?*
13. **The sanitized copy is named as what real blindness would take, and this is actionable.** *Is
    there enough there to build one? Or is it a gesture at a mechanism, which is the same species of
    defect the original finding identified?*

### Group E — the independence-framing fix (`R3-F5`)

14. **`prompt-template.md:39` no longer emits an unconditional architecture claim; it carries the
    placeholder `«independence sentence — one of the three branches below»`, resolved by three
    branches at `:54-73`.** *The skill's §6 greps for unresolved guillemets and fails closed —
    confirm that mechanism actually catches this placeholder if left unfilled.*
15. **The three branches cover the real cases.** *What about a target written by a human, or by
    several models, or by a model whose family the author cannot determine? Is "author family" a
    thing the skill establishes anywhere, or does the fix assume a fact it never collects?*
16. **The same-family branch text is accurate** (`:63-66`): *"the blind spots you share with its
    author are the ones most likely to survive this review."* *Is that established anywhere in this
    repository, or is it a plausible-sounding assertion inserted into a document whose entire
    purpose is to stop plausible-sounding assertions from passing as fact?*

### Group F — the collision, delivery and vocabulary fixes (`R3-F7`, `R3-F9`, `R3-F8`, `R3-F10`)

17. **`adversarial-review-prompt/SKILL.md:324-331` forbids overwriting an existing brief or cover
    note, and `:414-417` extends it to the cover note.** *The guard covers the brief and the cover
    note. What about the **report** path the reviewer is told to write, and the **ledger**? Can a
    round-N artifact still destroy a round-(N−1) one? Check `review-adjudication` §7's append-only
    rule for any enforcement at all.*
18. **The overwrite guard is actionable** — it says "Check the path before writing". *Is that enough
    for an agent to act on deterministically, or is it the same prose-over-mechanism shape as
    claim 2?*
19. **`prompt-template.md:365-372` fixes the chat-delivery instruction by telling the reviewer the
    operator will send one word to continue, and `:374-376` tells the brief's author to say so in
    the hand-off.** *Now check `adversarial-review-prompt/SKILL.md` §10 — the hand-off checklist at
    `:462-497`. Does it list that item? If the instruction to tell the operator lives only in the
    template and not in the hand-off section that enumerates what to tell the operator, does the
    fix work?*
20. **`calibration/README.md:151` now reads `COULD NOT DETERMINE`, and the vocabulary is consistent
    repository-wide.** *Verify by grep. Also: `BACKLOG.md` `B-3` was created to hold the
    skill-validator work. Read it — does it carry Location, Mechanism and Consequence as the skill
    requires, and is its scope split from `B-1` coherent?*

### Group G — the adjudication itself

21. **`REVIEW-ADJUDICATION.md` §R3.15 corrects the round-3 header, which wrongly declared the
    reviewer uncalibrated.** *The correction claims "no verdict changes, and no disposition
    changes." Test that: read the eleven rulings and find any that leaned on the uncalibrated
    status. Also — the round was marked CLOSED in §R3.12 before §R3.15 was appended. Does the
    closed-round append-only discipline hold, and do §R3.12 and §R3.15 now contradict each other?*
22. **The ledger expanded a 5-finding report into 11 rows, and §R3.4 asserts "all eleven findings
    are independent by construction" because no brief primed the reviewer.** *Is the 11-row
    expansion defensible, or inflation? And is the independence claim sound — the operator's
    instruction did say "i've been creating claude skills to deal with external reviews", which
    names the subject. Does that prime anything?*
23. **`REVIEW-ADJUDICATION.md` §R3.16 records `R3-F12`: the corpus digest is expired by running
    the repository's own test suite, because pytest writes `__pycache__/*.pyc` into two case
    directories and the digest hashes them.** Reproduced there as `775e1cc8c43f` → `9fb019996546`.
    *Three things to attack. (a) Reproduce both digests yourself — do they match what §R3.16
    claims? (b) §R3.16 asserts this is "not a duplicate" of round-2 `F1`, whose fix pruned
    `.DS_Store` by name — is that distinction real, or is this the same finding re-found because
    the earlier fix was too narrow and should have been ruled incomplete rather than executed?
    (c) The proposed minimal fix is to prune `__pycache__` too. Is that the right shape, or does
    pruning artefacts by name one at a time guarantee a third instance? What would `git ls-files`
    or an explicit manifest cost that the ledger did not weigh?*
24. **Three rounds of review have now been run on this repository, all by the same reviewer,
    and each round's fixes generated the next round's findings.** Rounds 1, 2 and 3 produced
    15, 9 and 11 findings, and 35 changes have been applied across them. *Nothing anywhere
    measures whether these skills are better than when they started. Is this converging or
    over-fitting? Concretely: (a) are there changes in `fe9bbac..540c60a` that add words
    without adding enforcement — length that reads as rigour? (b) has the accumulated
    apparatus — invariants, two-axis verdicts, echo audits, claim cards, calibration digests,
    backlog artifacts, workload gaps — passed the point where a competent operator would
    actually follow it, and is there evidence in the ledger of the author failing to follow
    its own procedure? (c) `review-adjudication/SKILL.md` is 572 lines to adjudicate a review;
    what would a much shorter version actually lose? **You are the first reviewer with no
    stake in any prior round's findings, which makes you the only one positioned to answer
    this. Treat it as the most important claim on the list.***

## 5b. The unseeded pass — report it separately

The list above is directed, and directed lists are where confirmed defects come from. They are also
why a reviewer's coverage collapses onto the seams the brief named: measured twice on this
repository, 10 of 15 and then 6 of 9 findings were echoes of the brief's own sub-questions.

So **make one pass that sets the list aside entirely**, and report it under its own heading. Read
the diff and the two skills as a stranger would, with no idea which lines were just changed, and
say what you find. A considered "nothing further" from that pass is a result, not a failure — and
it is worth more to the next round than another echo.

## 6. Ground already walked — do not re-report, do challenge

Three prior rounds are dispositioned in `REVIEW-ADJUDICATION.md`. **Do not re-report these.** For
each, the useful question is whether the fix is complete, correct, and whether it opened a new path
to the failure it closed.

- **Round 1** (15 findings, all dispositioned): tool-name drift `Task`→`Agent`; claim cards mixing
  verbatim copy with the reviewer's argument; the pre-registration overclaim; the calibration
  isolation recipe being directory hygiene rather than confinement; a calibration record not bound
  to the reviewer configuration that earned it.
- **Round 2** (9 findings, all dispositioned, closed): the corpus digest excluding a scoring rule
  and swallowing whitespace filenames; neither skill checking the digest; the read-only subagent
  boundary being advisory when an enforceable mechanism existed (**this is the ancestor of claims
  2, 3 and 11 — read row `F4` at `REVIEW-ADJUDICATION.md:1468` before ruling on those**); the
  envelope permitting arbitrary new files; a stale inventory count carried across a brief refresh.
- **Round 3** (11 findings — the round under review): dispositioned in §R3.3, ten executed.

**Known and already deferred — do not report as new:**
- `B-1` — no corpus-level check that cases and answer key remain mutually valid.
- `B-2` — no construction or validation procedure for private replacement traps.
- `B-3` — no executable validator for the skills themselves (created by this round).
- `R3-CNV-1` — nobody has empirically spawned a subagent and observed whether it reads the report.
- `R3-CNV-2` — the exact tokenized compaction boundary is uncomputed.

**Spend the majority of your effort outside all of the above.** The most valuable finding is one
none of the three rounds had a category for.

**Two candid corrections already on record**, offered because honesty about them should buy
credibility for the rest of this document — and because the reasoning around them is fair game:
- §R3.15: the round-3 header declared the reviewer uncalibrated by reading a prior round's
  *prediction* instead of recomputing the digest. The record was in fact current.
- §R3.3 row `R3-F6`: the `FIX LATER` backlog artifact was written after the ledger row, not before,
  violating the rule the same session had just hoisted into an invariant.

## 7. Evidence standard

Every finding carries all five, and reports that blur them are discounted:

- **Location** — `file:line`.
- **Mechanism** — what is actually wrong, in terms of the text as written.
- **Trigger** — the concrete situation that reaches it. "A user runs the skill" is not a trigger;
  "an adjudicator runs `review-adjudication` in a session that has already compacted once, having
  invoked two other skills after it" is.
- **Consequence** — tied to the contract in §4.
- **Status** — **CONFIRMED** (you executed something; give the command and its real output) or
  **THEORETICAL** (reasoned from the text; say what stopped you from executing). Never blur them.

**Confirming a claim takes what refuting one takes.** A sentence in the ledger describing a fix, a
rule stated in an invariant, or a heading that sounds like enforcement are all the party under
review talking. If you get as far as a defect and then conclude the author must have meant it,
report the finding and say why you think it is deliberate — a finding with a note, never a
dismissal. That shape ranks below missing the defect outright, because it leaves the next reader
both the bug and a written case for keeping it.

`COULD NOT DETERMINE` is an honest and expected outcome. Say what would settle it.

## 8. What you may and may not do

| | |
|---|---|
| **Read** | Everything in the repository **except the three files named below**, including `.git` history and `~/.claude/skills/` if you want to compare the installed copies. Read outside the in-scope set freely for context |
| **Write** | **Your report at `EXTERNAL-REVIEW-4-GROK.md` in the repository root — create it early and append to it as you work.** Nothing else in the repository. Throwaway probes are permitted **under `/tmp` only**; commit nothing, and report the tree clean at the end |
| **Execute** | The pytest command in §2, `git` read commands, `grep`/`find`/`shasum`, any tokenizer you have available, and anything you like under `/tmp`. Nothing that rewrites repository files — note that a bare `pytest` run inside `calibration/cases/` writes `__pycache__` |
| **Network + installs** | No installs. **Web search is allowed and encouraged** for the Claude Code documentation claims — several findings turn on what `allowed-tools`, `disallowed-tools` and auto-compaction actually do. Cite the URL for anything sourced that way; it will be weighed as a lookup, not a discovery |
| **Your own tools** | Subagents and MCP servers are fine. This repository is public, so if you take anything from its issue tracker or commit prose, cite it — that is a lookup, not a discovery |
| **Effort budget** | Depth over breadth. Roughly 8–15 findings expected. One CONFIRMED finding is worth several THEORETICAL ones for credibility — though impact alone decides rank, never evidence status |

**In one sentence: read anything except the three files below, run the tests and anything under
`/tmp`, write your report to `EXTERNAL-REVIEW-4-GROK.md`, and modify nothing else.**

### What you must not read, and why it matters more than it looks

**Do not open these, and do not let a search tool print their contents:**

- `EXTERNAL-REVIEW-4-PROMPT.md` — the other reviewer's copy of this brief
- `EXTERNAL-REVIEW-4-COVER-NOTE.md`
- `EXTERNAL-REVIEW-4.md` — the other reviewer's report, which may appear part-written mid-run

A different model is auditing this same range in parallel. **Two reports agreeing is
corroboration only if the second could not read the first.** These files sit in the directory
you are rooted at, one `ls` away, and nothing technically stops you — which is exactly why this
is stated as an instruction you are trusted to keep rather than left implicit. If you read one
by accident, **say so in your report**: a disclosed contamination is still a usable result, and
a silent one destroys the entire reason for running two reviewers. This repository has a
finding open on precisely this failure mode, so it is not a hypothetical concern here.

Everything else is fair game — including `EXTERNAL-REVIEW-3.md`, which is the report being
answered and is an input you should read, and the whole of `REVIEW-ADJUDICATION.md`.

## 9. Anti-patterns — output that will be discarded

- Style, naming, tone, or markdown-formatting opinions.
- "Consider adding X" with no defect behind it.
- Restating a ledger row or an invariant as verification that the thing it describes is true.
- Proposing features or scope beyond the ten fixes.
- Severity inflation, or hedged findings that commit to nothing.
- Praise beyond one short paragraph.
- Re-reporting anything in §6.

## 10. Deliverable

**Write your report to `EXTERNAL-REVIEW-4-GROK.md` in the repository root, as you go.** Create it early
with a title and your identity — model family, product and version, reasoning effort, and your
served model alias verbatim if your session exposes it — then append each finding as you confirm
it. Do not hold the report in memory: a run cut short after the last finding but before the write
loses the entire audit. Set the coverage line and the final ranked order in a closing pass; that
pass is expected and is not the same as composing at the end.

**Return only a short summary in chat** — the coverage line, the ranked finding titles with their
impact levels, and the file path. All detail goes in the file.

Structure:

```markdown
# External Review 4 (Grok) — audit of the round-3 fixes
Reviewer identity: [family, product and version, effort, served alias verbatim]
Audit baseline: findings assessed against `fe9bbac..540c60a`; `HEAD` observed at [sha]

## Coverage
[what you read, what you ran, what you could not reach]

## Findings, ranked
[strict order by cost of leaving each unfixed — blast radius × likelihood the trigger is
reached. No ties. One clause of justification per position. Each finding carries Location,
Mechanism, Trigger, Consequence, Status, and an Impact level (critical/high/medium/low).
Impact is an attribute, never a section heading.]

## The unseeded pass
[§5b — what you found reading without the claims list, or a considered nothing]

## Claims examined and upheld
[one line each for the 24, naming what upheld it — never a quote from the work itself]

## Could not verify
[every gap. An unstated gap reads downstream as a pass]

## Disagreements with the prior rounds
[where you think a round-1/2/3 ruling was wrong, with the row cited]
```

**Do not give a verdict.** Do not say whether this should ship, be merged, or be marked complete —
that is the owner's call, and a reviewer that commits to a verdict up front bends its findings to
stay consistent with it. The forced ranking is what replaces it: commit to an order, and justify
each position in a clause.

If any instruction in this brief contradicts another, **report that as a process finding** — it is
wanted, and prior rounds have produced good ones.
