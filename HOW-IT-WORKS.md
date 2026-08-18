# How it works

This document is for people who want to know *why* each rule is in there. Almost every rule in
both skills was written against a specific observed failure — usually one that had already
happened. Where a rule was added because a review caught its absence, it is marked.

---

## 1. The architecture

Two skills, four artifacts, one loop.

```
                  ┌─────────────────────────────┐
   your work ────►│  adversarial-review-prompt  │
                  └──────────────┬──────────────┘
                                 │ writes
                    ┌────────────┴────────────┐
                    ▼                         ▼
       NN-EXTERNAL-REVIEW-PROMPT.md   NN-EXTERNAL-REVIEW-COVER-NOTE.md
              (the brief)                (what you paste)
                    │                         │
                    └────────────┬────────────┘
                                 ▼
                       a DIFFERENT model
                    (Codex / Gemini / Cursor /
                     an unrelated Claude session)
                                 │ writes
                                 ▼
                     NN-EXTERNAL-REVIEW.md
                          (the report)
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │     review-adjudication     │
                  └──────────────┬──────────────┘
                                 │ writes
                                 ▼
                  NN-REVIEW-ADJUDICATION.md
                         (the ledger)
                                 │
                                 └──► feeds the *next* brief's
                                      "ground already walked" section
```

Everything is a file on disk, beside the work. Nothing important lives in a chat window. That
is a design constraint, not an aesthetic one — see §4.

`NN` mirrors whatever prefix the surrounding work uses (a phase number, a PR number). For a
target with no such structure — a skill, a bare repo — the files drop the prefix and sit beside
the report. *Beside the report* is the invariant; the prefix is not. (Added after round 2 of the
self-audit: the reciprocal discovery rule in the sibling skill only globbed for the prefixed
form, so the standalone ledger the skill actually produced was invisible to the next brief.)

---

## 2. Why "ask another model" isn't enough

The naive version of this — paste code into a second model, ask for a review — reliably fails,
in a specific way. The reviewer re-derives the author's reasoning, finds it sound, and returns a
summary of the author's own beliefs dressed as an independent check. You end up *more* confident
and no better informed.

`adversarial-review-prompt` uses three levers against that.

### Lever 1 — name the condition, not the contents

You cannot tell the reviewer what the blind spots are. If you could see them they wouldn't be
blind, and finding them is the reviewer's entire job. What you *can* state — because it's a fact
about the process, not about the work — is:

> Every line of this was written by one model, reviewed by that same model, and verified by that
> same model against tests it also wrote. It currently reads as complete and passing. That is
> exactly the problem. You have a different architecture and different training. You will notice
> different things, and those things are the entire value of this exercise.
>
> Confirmation is near-worthless output. A manufactured finding is worse than no finding. A
> finding that survives your own attempt to refute it is worth more than ten observations.

Two guards live inside that framing:

- **The provenance sentence is a factual claim and gets verified before it ships.** If the target
  contains inherited code, human edits, or vendored work, "every line was written by one model"
  is false, and a reviewer that discovers it is false starts distrusting the rest of the brief.
- **A zero-finding audit must stay admissible.** An early draft made "find what is wrong" so
  central that returning nothing read as non-compliance — which is a machine for manufacturing
  findings. *(Codex, finding 1.)* The brief now says explicitly that few or zero findings is a
  legitimate result, and gives it a place to land: a "claims examined and upheld" section where
  an empty audit earns its credibility.

### Lever 2 — demote the author's assertions to claims

The single highest-yield instruction in the whole brief:

> This codebase's comments argue for their own correctness. Treat every one of them as a claim by
> the party under review, never as evidence.

Followed by four to six **real comments quoted from the source** — which both makes the
instruction concrete and proves the brief's author actually read the code. Then:

> For any that is load-bearing: open the test, read what it actually asserts, and check whether
> it would fail if the claim were false. A test whose name matches a guarantee is not a test of
> that guarantee.

For a plan or design document the equivalent target is confident prose — "proven", "industry
standard", "this obviously scales", cited benchmarks.

### Lever 3 — hand over a target list, not a codebase

"Audit this" spreads a reviewer thin across a whole tree. Instead the brief enumerates 15–25
**load-bearing claims** — the specific assertions the work's "it's correct" status rests on —
each with a `file:line` citation and an italic sub-question aimed at the seam:

> `below * 100 <= maxPct * total` (integer form, `classifier.ts:44`) is exact and immune to float
> drift at the boundary, versus Python's `100.0 * below / total <= 0.5`.
> *The CLI accepts arbitrary decimal `--borderline-max-pct` values — does the guarantee survive
> that?*

They're mined by grepping for self-assertion (`measured|verified|guaranteed|immune|cannot|never|
by construction`), plus comments citing a test as proof, frozen contract declarations, deliberate
threshold and operator choices, and any claim of cross-machine determinism.

Each comes back CONFIRMED / REFUTED / COULD NOT DETERMINE. That is per-claim evidence, not a
verdict on the work (§5). And "engaging" a claim means doing the work its adjudication needs —
a claim the reviewer only *read* belongs in its could-not-verify list, not its coverage count.

### The anti-anchoring rule

The author's own residual suspicions are **held out of the brief entirely**, and out of the cover
note too — the cover note is read first, so anchoring there is worse. They go to you instead, in
the hand-off, as 3–5 questions-with-mechanisms.

The reason is asymmetric value. A suspicion you plant is echoed back at you; a suspicion the
reviewer reaches blind is independent corroboration, the strongest evidence the exercise can
produce. Demotion disclaimers ("I suspect X but don't let that bias you") do not survive contact.

What the author may *not* do is certify that a doubt stayed out. Doubts and load-bearing claims
come from one reading of one body of work, so a doubt is usually about a claim you just wrote and
the sub-question pointing at that seam is the doubt. The claim stays sharp — that sharpness is the
brief's main value — and the overlap gets declared instead. The hand-off carries, per doubt, the
brief items a doubt-derived search lands on, plus the raw search output; where nothing turns up
the words are "no line found — unverified", never "held back".

That split exists because the softer version failed three times running, the third time after a
mandatory search had been added *and performed*: the author picks the queries, and picks them from
the half of the doubt the brief does not contain. Across all three occurrences every wrong label
was a claim of absence, and not one claim of presence was ever wrong. Absence in a document you
wrote is not a judgement you are positioned to make.

So the ruling lives on the other side. The adjudicator searches the brief itself, records what it
found per doubt, and only then may a rediscovered doubt count as corroboration — and where a doubt
did leak, the reviewer's agreement is discounted as an echo and re-verified from primary sources.
That rule exists because it happened: four of fourteen findings in the self-audit were seeded that
way, and all four had to be re-established on primary evidence alone.

---

## 3. The operating envelope

Six axes, stated in the brief as its own headed block, filled in even when the answer is "no" —
because an omission reads as permission to one model and as prohibition to another.

| Axis | What gets stated |
|---|---|
| **Read** | The in-scope set, and whether reading outside it is allowed (usually yes, for context) |
| **Write** | Its own report file, always. Everything else read-only by default; if more, exactly which paths and the restore obligation |
| **Execute** | The precise commands, with the slow or destructive ones named |
| **Network / installs** | Almost always no — and if the project forbids network at runtime, that prohibition is itself a claim to audit |
| **Its own tools** | Web search, MCP servers, subagents. Web search usually allowed, with a cite-the-URL requirement |
| **Effort** | Depth over breadth, and roughly how much |

Three non-obvious rules:

**The report authorization and the read-only rule go in the same sentence.** Split across two
paragraphs they read as contradictory, and a model resolving a contradiction conservatively
declines to write the file — which loses the only output that matters.

**"Read-only" is not the same as "non-mutating."** Authorized commands can write: snapshot-updating
test runners, cache-writing builds, `git` subcommands that alter state. The envelope says so, and
tells the reviewer to withhold such a command and report what it withheld. *(Codex, finding 10.)*

**Mutation testing is the one thing that genuinely earns write access,** because the real question
is not "do the tests pass" but "would they fail if the code were wrong." When authorized, it's
bounded: throwaway probes in an obviously temporary location, commit nothing, restore the tree,
report it clean. And a surviving mutant is a finding *only* if the reviewer shows the mutation
changed required, reachable, observable behaviour — equivalent mutants and dead code prove
nothing. An earlier draft said every silent survival was a finding, which is a false-positive
generator. *(Codex, finding 3.)*

**You get told.** The hand-off to you must contain one explicit line naming every path the
reviewer may write and every capability it was granted. Not buried in the brief — in the message.
The objection is never "an external model touched files," it's "an external model touched files
and I found out afterwards."

The envelope is an instruction, not a sandbox. Where a boundary actually matters, enforce it with
the receiving CLI's own permission flags too.

---

## 4. Why the report is a file, written as you go

The brief instructs the reviewer to create its report file *before its first finding* — title and
identity only — and append each finding as it confirms it, then do a closing pass that sets the
final ranking and the coverage line (which is only knowable at the end).

The closing pass is expected. What's forbidden is a report that exists only in memory.

The reason is mundane and expensive: a chat-only report is one dropped message, one truncated
reply, or one closed tab from losing the entire audit. A partial file is recoverable; an
interrupted composition is not. The chat reply is deliberately reduced to a summary — coverage
line, ranked titles with impact levels, and the file path — with a standing instruction not to
paste the report twice, because a duplicate that drifts from the file is worse than no duplicate.

The **cover note** exists for the same reason in reverse: a 400-line markdown brief pasted into a
chat box arrives with its fences mangled and its opening instruction buried. So the note is ~25
lines of plain prose that points at the brief on disk, and it carries exactly four things:

1. **Context and authorization**, in your voice — what the software is, who it runs for, its real
   exposure, that you own it. This is load-bearing, not courtesy: a brief that opens with *attack
   this, prove it's wrong* and no provenance reads like a request to break into someone else's
   system, and an unsure reviewer spends its output on hedges.
2. **The pointer** — the brief's path, written as the reviewer's session will see it.
3. **Delivery** — write the report to a file as you go; summarize in chat.
4. **Host gotchas** — only the ones that would otherwise read as findings. (The recurring one:
   on Windows PowerShell, `npm.cmd` rather than `npm`, because the execution policy blocks the
   `npm.ps1` shim and it fails *before* npm starts, which looks exactly like a failing suite.)

If the reviewer is a browser-only chat with no filesystem, no cover note is emitted at all — a
path it cannot open and a file it cannot write are instructions it has no way to obey. You get
told to attach the brief and save the returned report yourself.

The brief and the cover note are checked against each other before hand-off: brief path, report
path, and every permission must agree exactly. The brief tells the reviewer to report contradictory
instructions as a process finding, so a cover note saying "read-only" against a brief authorizing
mutation burns the run on that instead of on the code.

---

## 5. No verdict — forced ranking instead

The brief never asks "should this ship?" Two reasons:

- It is the owner's call, not a reviewer's.
- A model that commits to YES or NO early bends every finding underneath it to stay consistent.

But a review with no commitment is just observations. What the verdict was really buying is
*commitment*, and a **strict total order** buys it better: rank the findings by the cost of
leaving each unfixed — blast radius × likelihood the trigger is reached — with no ties and a
one-clause justification for each position. "These are all equally important" is a refusal to do
the one piece of judgement being asked for.

Two distinctions the brief enforces:

- **Impact is an attribute, never a section heading.** Severity buckets are how a reviewer avoids
  saying which of six "criticals" it would fix first.
- **Evidence status is not impact.** A THEORETICAL data-loss defect outranks a CONFIRMED cosmetic
  one. "A CONFIRMED finding is worth more" refers to *credibility and effort*, never to rank.
  Earlier drafts blurred these, and the phrasing was still competing with impact after the first
  round of patches — it took a second verification pass to fix. *(Codex, finding 2.)*

Every admissible finding carries five parts: **Location** (`file:line`) · **Mechanism** (why the
code does the wrong thing, in its own logic) · **Trigger** (a concrete input — "a malformed PNG"
is not a trigger, "a greyscale PNG with a tRNS chunk" is) · **Consequence** (tied to a stated
criterion) · **Status** (CONFIRMED, with command and output, or THEORETICAL, saying what stopped
it). For a plan or design target, CONFIRMED becomes "cited and quoted a source that settles it."

And the brief invites findings *about itself* — a citation that doesn't match, two instructions
that contradict, a leaked authoring placeholder. Which is why the brief is verified before
hand-off: every `file:line` reopened and checked, every printed command re-run, and the saved
draft grepped for the `«guillemets»` that mark author-only instructions in the templates. One
leftover guillemet means an instruction meant for the brief's author is about to be read by the
reviewer, and it fails closed.

---

## 6. Adjudication: the four forces

The naive framing of "decide what's worth implementing" is the failure mode, not the goal. Four
forces push toward wrongly disposing of real findings.

**1. You are usually mid-task and want it closed.** Dismissal is the cheapest path, and it wears
good clothes: "pre-existing", "out of scope", "scaffold only", "will handle later." *A finding you
just found and immediately deferred is the tell.* So deferral has to cost something: `FIX LATER`
requires a backlog artifact that exists on disk **before the ledger is written**, carrying the
finding's Location, Mechanism and Consequence copied into it — the ledger row alone doesn't
contain them, and a bare-path stub is a drop wearing a deferral label. *(Content requirement added
after round 2: the original rule checked that the file existed, not that it said anything.)*

**2. Rejection is held to a lower evidence standard than accusation.** The brief made the reviewer
produce five parts for every finding; a refutation typically arrives as a paragraph of reading.
That asymmetry is where false REFUTEDs come from. **The refutation carries the same burden as the
finding.** For anything about runtime behaviour, a static read plus a reassuring comment is not
evidence — *the comment is the party under review talking*. Reconstruct and run the actual path,
with production's entry point, production's defaults, and the real population.

**3. Self-review re-enters through the back door.** If you wrote the code, your refutation of a
finding about that code is self-review again, carrying the same blind spots that produced the
defect. So: a REFUTED verdict on anything the reviewer rated high or critical, in code you
authored, requires execution evidence. Without it the verdict is `COULD NOT DETERMINE`, and you
say what would settle it.

**4. And running the other way — relitigation is real damage.** A reviewer can't see your settled
decisions and will reopen arguments you closed months ago. Screening for that is legitimate, so
it's a step — but it's the channel dismissal will try to use, so it's gated twice: a
`SETTLED ALREADY` verdict requires the decision quoted with its `file:line`, and a finding that
brings **new evidence the settled decision never considered** is not settled. It's reopened, and
it goes to you.

Three structural rules do the rest of the work:

- **Enumerate before judging.** Every finding goes into the ledger skeleton — ID, verbatim title,
  reviewer's impact — and the skeleton is written to disk *before any verdict is formed*. This is
  the guard against the most common real-world drift: the easy findings get fixed, the hard ones
  get forgotten, and the ledger records only what was convenient.
- **Count in = count out.** One row per numbered finding, with auxiliary populations counted
  separately in the header. A finding with no row is the defect the whole skill exists to prevent.
- **Split by class.** Machine-checkable (settle it by running something) · owner judgement (turns
  on what the product should do, what risk is acceptable — hand it up as one decidable question
  with options and costs) · process/prompt (about the brief or the method; its fix lands there,
  not in the code). *A machine-checkable finding you resolve by reasoning is an unforced error; an
  owner-judgement finding you resolve yourself is you taking a call that isn't yours.*

There's also a specific check for false-green gates: when a finding says a test proves nothing,
the question is not "does the suite pass" but "would it fail if the thing were wrong." Break it
deliberately — in a throwaway copy outside the working tree — and see.

---

## 7. Why two axes

Every row carries a **verdict** and a **disposition**, and they answer different questions.

| Verdict — is the claim true? | |
|---|---|
| `CONFIRMED` | The defect is real. Evidence in the ledger. |
| `CONFIRMED (partial)` | Mechanism real; some part — usually prevalence or blast radius — unestablished. Say which. |
| `REFUTED` | False, with evidence at the finding's own standard. |
| `COULD NOT DETERMINE` | An honest, available outcome. Say precisely what would settle it. |
| `SETTLED ALREADY` | Relitigates a locked decision. Citation required. |
| `OWNER RULING REQUIRED` | Not the adjudicator's to rule on. |

| Disposition — what happens now? | |
|---|---|
| `FIX NOW` | Queued for execution. Name the minimal fix. |
| `FIX LATER` | Requires the backlog artifact, path quoted, content verified. |
| `ACCEPTED AS-IS` | Real, and shipping anyway. **Requires the owner's words, quoted.** May be proposed, never issued. |
| `NO ACTION` | Available only under `REFUTED` or `SETTLED ALREADY`. |
| `VERIFY` | Pairs with `COULD NOT DETERMINE`: the concrete check, and whether it blocks. |
| `PENDING OWNER` | Pairs with **any** verdict — truth and state are independent. |

**Never a bare "ACCEPTED."** It means both "we accept the finding is real" and "we accept the risk
and are shipping" — opposite dispositions from one word. That word was what the pre-existing
ledgers in the corpus this skill was derived from actually used, 21 times.

The vocabulary is not decorative, and it was not complete on the first try. The first real run of
this skill — auditing itself — produced two rows that *had no legal form*: a CONFIRMED finding
awaiting an owner disposition, and a COULD NOT DETERMINE with nothing to pair with. Both holes
fired live, inside the ledger that was diagnosing them. `PENDING OWNER`-with-any-verdict and
`VERIFY` were added in response. *(Fable, findings 1 and 2.)*

Two more rules on the accepted pile:

- **The fix must be the minimal one that closes the finding.** Where a real finding's suggested fix
  would harden throwaway scaffolding or ratchet complexity, the disposition stays `FIX NOW` with a
  *simpler* fix named, or becomes `ACCEPTED AS-IS` with sign-off. It never quietly becomes
  `NO ACTION` — "the fix is too heavy" is a statement about the fix, not about the defect.
- **A cheap fix in a site the work already touches is not deferrable,** even if the defect predates
  it. Split by cost, not by origin.

---

## 8. Rounds, closure, and the append-only rule

A ledger accumulates rounds. Completed rounds are immutable: a superseded ruling gets a **new row
citing the row it supersedes**, and the original stays as written. The record of having been
wrong is part of what the ledger is for.

But "completed" needs a definition, and the obvious one is wrong. Closure is defined over
**obligations, not cell presence**: every numbered row *and* every auxiliary entry carries both
axes, no `PENDING OWNER` is unresolved, no blocking `VERIFY` is open, and every executed `FIX NOW`
row has been backfilled with its execution reference. A round that isn't closed — an interrupted
skeleton, an unexecuted queue, an unanswered question — is the *current* round, and filling it in
place is required, not a violation.

Without that definition the append-only rule traps an interrupted run forever: the skeleton is
written first by design, so a run killed midway leaves titles with empty verdicts that the
immutability rule then forbids anyone from filling. *(Fable, finding 6; refined again in round 2
when "complete" was found to freeze provisional rows before their required backfill.)*

The **auxiliary populations** get the same two axes as table rows, each with a stable ID:

- `P-n` — process and prompt defects. The brief invites these; their fix lands in the brief or the
  skill, not the code, so they get their own block.
- `CNV-n` — the reviewer's could-not-verify list. That list is the reviewer being honest about a
  gap. Dropping it re-hides the gap, and downstream it reads as a pass.
- `D-n` — disagreements with a prior internal review.

Where two reviewers contradict each other on the same code, neither is presumed right — by
seniority or by order of arrival — and the item is re-verified before either is ruled on. Where a
reviewer's stated figures fail to reproduce, that's recorded: a reviewer whose numbers reproduce
exactly has earned weight on its unverifiable claims, and one whose numbers drift has not.

---

## 9. The boundaries the adjudicator does not cross

- **It does not fix.** The deliverable is the ledger. Fixing is a separate, explicit act
  afterwards, executed *against* the ledger.
  There is one sanctioned bridge, added because the strict rule contradicted 3-of-3 real-world
  practice: the hand-off's offer to execute, **once you accept it**, is the separate act — your
  acceptance is recorded verbatim in the ledger, and the same session may then execute and
  backfill. Whoever lands a `FIX NOW` change updates that row; a ledger still saying "queued"
  after the work landed is a false record. *(Fable, finding 7.)*
- **It does not decide whether the work ships.** The sibling skill refuses to let the reviewer
  issue a verdict; the refusal doesn't lapse because the reader is now Claude.
- **It writes almost nothing.** The only files it creates or edits are the ledger, the `FIX LATER`
  backlog artifacts, and — when the review arrived only as a chat transcript — the report file
  materialized from it, saved before adjudication begins. Never the code, the plans, or an
  existing review, whatever the tool grants technically allow.
- **Its re-verification is hygienic.** Only commands verified not to rewrite repository files or
  external state; the throwaway copy for deliberate breakage lives in a scratch directory, never
  the working tree; and the step ends by reporting the tree clean — or, on a target with no
  repository, by naming the only files the session wrote and showing the directory otherwise
  unchanged. *(The non-repository branch was added in round 2, after a run against a directory
  that had no git at all was required to report `git status` clean.)*

---

## 10. Provenance

Neither skill was designed in the abstract. `adversarial-review-prompt` was distilled from a real
audit brief that worked; `review-adjudication` was derived from three real ledgers in a working
project, then tested by retrodiction against them — does the rule, applied to what actually
happened, produce what the ledger actually says?

Then both were pointed at themselves.

| Round | Target | Reviewer | Result |
|---|---|---|---|
| 1 | `prompt-template.md` | OpenAI Codex (GPT-5) | 24/24 claims engaged, **10 findings** — including that the framing made a zero-finding audit noncompliant, that "every surviving mutation is a finding" manufactures false positives, and that evidence status was masquerading as importance |
| 1b | the patches | Codex again | 8 of 10 amendments verified implemented; **2 found to have diverged** and were fixed |
| 2 | `review-adjudication` | Claude Fable 5 | 22/22 claims engaged, **14 findings**, 2 brief defects, 5 could-not-verify items. Two findings fired *live against the ledger diagnosing them* |
| 3 | `review-adjudication`, post-amendment | OpenAI Codex (GPT-5) | 22/22 claims engaged, **8 findings** on the round-2 fixes — including two amendments that contradicted rules elsewhere in the skill |

The round-2 adjudication was itself run by a session deliberately kept blind to the authoring
conversation, so the author's design arguments could not be used to wave findings away. Two of
them survived anyway and became owner questions.

Every artifact from those rounds is in [`examples/`](examples/), unedited except for local paths
and one private project name. The round-2 ledger is worth reading in full: it contains a recorded
count-convention deviation, an owner-supplied independence discount applied to four of its own
rows, and two owner questions that the adjudicator explicitly refused to answer itself.

### Borrowed from code review cadre

Four rules here came from reading [VibeCodyH/code-review-cadre](https://github.com/VibeCodyH/code-review-cadre)
(MIT), which asks a different question — *which set of reviewers should I seat*, graded against
answer keys mined from fix commits — but whose rubric had measured failures this pair was not
guarding against:

- **Spotting a defect and then arguing it away does more damage than never spotting it.** Cadre
  scores that outcome in its own right and disqualifies a reviewer for it. Here it became two
  rules: the brief forbids signing off a claim on the authority of a nearby comment, and the
  ledger spot-checks the upheld-claims list rather than copying it over.
- **A report that is not a review must not be adjudicated as a clean one.** Cadre has stored
  artifacts that were counted as finished reviews while being nothing of the kind, with every file
  they never mentioned read as approved. Adjudication now classifies before it enumerates.
- **A reviewer that stopped early has approved nothing.** Directly relevant because the
  file-as-you-go rule *produces* partial reports on purpose; nothing downstream was reading them
  as partial.
- **Agreement between reviewers who can read each other is not agreement.** Cadre prevents it
  structurally, by keeping one reviewer's output out of any tree the next one can reach. This pair
  puts everything in one directory deliberately, so it is recorded and discounted instead.

Also taken, smaller: the settled-ground check breaks toward *not settled*, findings true of the
whole repo are separated from findings about the work, reviewer lineage is named at hand-off, and a
public target's own issue tracker is treated as a leak of its answers.

---

## 11. Known limits

- **Skill firing is unverified for one path.** Whether the description reliably triggers on
  natural-language phrasing ("close out the review") rather than an explicit `/name` invocation
  has never been tested live; every recorded run invoked by name. It's in the ledger as an open
  could-not-verify item, not quietly assumed to work.
- **These reduce self-confirmation; they don't eliminate it.** A second model with correlated
  training can still miss what the first one missed. The value comes from architectural
  difference, so the more different the reviewer, the better the return.
- **The envelope is an instruction, not a sandbox.** Enforce boundaries that matter with the
  receiving tool's permission system.
- **Cost.** A serious brief is 400–600 lines, and reading the work properly to write it is not
  cheap. This is for work where being wrong is expensive.
- **The adjudication ledger is only as good as its re-verification.** The rules push hard toward
  executing things, but a lazy run can still produce a plausible ledger full of prose. The
  countermeasure is in the template: every command and its real output, verbatim, and expectations
  pre-registered *beside the command before running it* — so a surprise surfaces mechanically
  rather than by recall.

---

## 12. Adapting them

Both skills are prose. Edit them.

Things worth changing for your own setup: the artifact filenames and where they land; the
grep patterns used to mine load-bearing claims (they're tuned for TypeScript comments); the
"settled ground" sources in adjudication step 3, which currently look for a `CLAUDE.md`
do-not-relitigate block, locked decision IDs, and prior ledgers; and the backlog artifact
requirement in `FIX LATER`, which assumes your project has somewhere durable to put one.

The parts to keep, because they're where the value is: the reviewer never issues a verdict;
residual doubts never enter the brief, and the author never certifies that they didn't; the report
is a file written as you go; refutation carries the same burden as accusation; enumerate before
judging; and every finding leaves with both a verdict and a disposition.
