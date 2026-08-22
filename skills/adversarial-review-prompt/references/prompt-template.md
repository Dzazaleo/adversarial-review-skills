# Prompt skeleton

Section order below is load-bearing: framing before facts, facts before targets. Adapt the
headings to the work; keep the sequence.

Text in `«guillemets»` is an instruction to you. Everything else is register to preserve —
the phrasings marked **verbatim-worthy** did the heaviest lifting in practice.

---

## Title + provenance blockquote

```markdown
# Adversarial Independent Audit — «target»

> **Prompt for an external reviewer («model»).** Hand this file to a model that did **not**
> write the «code/plan» under review. Everything below is written to be read by that
> reviewer, not by the author.
```

## 1. Why you are here

Name the self-review problem concretely. State the current green status with real numbers
(tests passing, verification score, open threats) and then turn it into the reason for doubt.

Verbatim-worthy — except that the provenance sentence is a factual claim: verify it before
keeping it. Where the target contains inherited code, human edits, or third-party work,
state the actual provenance instead — a false "every line" primes the reviewer to distrust
evidence on a fabricated basis:

> Every line of the code you are about to audit was written by one model, reviewed by that
> same model, and then verified by that same model against tests it also wrote. It currently
> reads as complete and passing: «numbers».
>
> That is exactly the problem. A model validating its own work carries the same blind spots
> into the review that it had while writing — the same misreadings of the spec, the same
> unexamined assumptions, the same things it never thought to test because it never thought
> of them at all. You have a different architecture and different training. **You will notice
> different things, and those things are the entire value of this exercise.**
>
> - **Confirmation is near-worthless output.** If you spend your effort re-deriving what is
>   already claimed correct and agreeing, this audit has failed.
> - **Your job is to find what is wrong, missing, or unjustified**, and to prove it.
> - **A manufactured finding is worse than no finding.** If a rigorous search comes back
>   nearly empty, say so and show the search — few or zero findings is an admissible
>   result, and the claims-examined-and-upheld section is where it earns its credibility.
> - **A finding that survives your own attempt to refute it is worth more than ten
>   observations.** Try to break your own findings before reporting them.
>
> Assume competence, not correctness. The «work» is carefully built. Where it is wrong, it
> is wrong in ways its author cannot see — those places are what you are here for.

## 2. The single most important instruction

The comments-as-claims reframing. Quote 4–6 **real** self-asserting comments pulled from the
source in §3 of the skill — real quotes make the instruction concrete and prove you read it.

Verbatim-worthy:

> **This codebase's comments argue for their own correctness. Treat every one of them as a
> claim by the party under review, never as evidence.**
>
> «4–6 real quoted comments»
>
> For any that is load-bearing to your audit: **open the test, read what it actually asserts,
> and check whether it would fail if the claim were false.** A test whose name matches a
> guarantee is not a test of that guarantee. An anti-vacuity comment is not an anti-vacuity
> check.
>
> Where a comment's claim is false, overstated, or unfalsifiable by the test it cites, that
> is itself a finding — arguably a severe one, because the comments are what a future
> maintainer (and the next audit) will trust.

For a plan or design doc, the equivalent target is confident prose: "proven", "industry
standard", "this obviously scales", cited versions and benchmarks. Same treatment.

## 3. Environment and how to run things

A small table (repo root, OS and its relevant semantics, runtime, install command) plus the
exact commands. «Every count in that table — how many files of what kind, how many lines — is
**enumerated** with a command at authoring time, never described from recall. You have just read
this work and you will remember its shape wrongly: the count you carry is of the files you thought
about, and the tree holds the ones you did not. A reviewer that trusts an undercount audits half of
what you meant to hand it and reports the coverage as complete.

**Enumerate against the pinned commit, and re-enumerate on every refresh.** Run the count over the
scoped paths at the commit the range pins (`git show <commit>:<path> | wc -l`), not against the
working tree and not against your last draft. **A brief that is refreshed re-runs the whole table**
— the recurring failure is not an author who never counted, it is an author who counted once,
corrected one number on the second pass and carried the rest forward. That is exactly how a pinned
418-line file was handed over as 416 lines in two successive versions of the same brief while its
neighbour was corrected in the same edit.» The audit range goes here as **immutable commit IDs** («`abc1234^..def5678`,
observed `N files, +A/−B` from `git diff --stat` run at authoring time — never "N commits ahead
of `main`" or `main..HEAD`, which can be empty by the time the reviewer runs it; list any
documentation-only commits above the range separately so `HEAD` being ahead reads as
expected, not as a discrepancy. **Do not assert that an endpoint "is `HEAD`"** — that is a branch
relation smuggled back into a pinned range, and it is false the moment one more commit lands, which
on a live branch is usually before the reviewer opens the file. If you mention `HEAD` at all,
produce it by running `git rev-parse HEAD` as you write, and name what sits above the range»). Then every trap:

- Gitignored or machine-local datasets, with absolute paths «redact machine-identifying
  components — usernames, home directories — unless the reviewer genuinely needs them; this
  prompt may be pasted into an external service»
- Test gates that self-skip on a missing env var — show both invocations and both result
  lines side by side, and point out that the skipping one is the default
- Untracked files to leave alone
- Oracles / reference implementations, with the line ranges that matter and which of their
  behaviors are deliberately **not** goals

«For a plan or design target there is nothing to run. Replace this section with the
governing sources: the spec or requirements the plan answers to, its hard constraints, what
stage the decision is at, and how each of its claims can be checked on paper.»

## 4. Scope

In scope: the file list with line counts, one line of purpose each, total LOC.
Out of scope: named explicitly — "do not review absent work and do not propose features."

Then the one-way doors, with the downstream consumers named:

> A design flaw in these «contracts» is worth far more, found now, than any implementation
> bug. If the published shape will not survive its declared downstream uses, say so plainly
> and say why.

## 5. The contract the work must satisfy

- Numbered success criteria, quoted from the source of truth, with exact expected values
- A table of locked decisions (`ID | decision`) — these are what "correct" means here
- Any frozen spec (hash format, exit codes with precedence, schema shape) in a code block

## 6. Load-bearing claims — attack these

The heart of the prompt. Grouped, numbered, each with `file:line` and an italic
sub-question pointing at the seam.

> These are the assertions the phase's "complete" status rests on. Each is a target. For each
> one you engage, state whether you **confirmed** it, **refuted** it, or **could not
> determine** it, and show your work. Engaging a claim means doing the work its adjudication
> needs — reading its entry here is not engagement, and a claim you only read belongs in
> your could-not-verify list, not your coverage count. If effort runs short, spend it on
> independent defect search first, then the highest-risk claims here.
>
> **Confirming a claim takes what refuting one takes.** A comment, a test name, or a docstring is
> the code asserting itself — it is what the claim rests on, never what settles it. Quote one and
> you have located the claim, not checked it; that is a could-not-determine. And if you reach a
> real defect and conclude the author meant it, report it and say why you think so. Do not close it
> on the work's own say-so. Dismissing a real bug and writing down a reason costs more than never
> spotting it: the next reader inherits the bug and the argument together.

15–25 items. Suggested groups: rule/arithmetic correctness · published contracts (one-way
doors) · robustness and process behavior · supply chain and hygiene.

«Where a sub-question here is one of your own residual doubts — the normal case, since both come
out of the same reading — keep it sharp and declare the overlap at hand-off (§11 below). Never
blunt a claim to protect a doubt.»

### 6b. The unseeded pass — required whenever §6 exists

«A brief this directed buys confirmed defects and almost no independent coverage. Two measured
rounds on this repository: 10 of 15 findings were echoes of §6's own sub-questions, then 6 of 9,
with exactly one finding reached without the brief pointing at it. Every one of those findings was
real. What was worth nothing was the reviewer's **silence** — outside the seams named here, the
review established nothing either way, which is the one thing a calibrated reviewer's silence was
supposed to buy.

So ask for both, and keep them separate:»

> **An unseeded pass, reported separately.** Set this brief's claim list aside and search the range
> on your own reading of it. Report what that pass found under its own heading, including "nothing"
> — a considered nothing from an unseeded pass is a result this brief cannot get any other way, and
> it is not a failure to produce one. Findings that are also in the claim list belong under the
> claim they answer, not here; this heading is only for what you reached without being pointed at
> it.

«Score the two passes separately when the report comes back. The adjudicator's echo audit will do
this anyway — it probes every finding against this brief using the finding's own identifiers — but
a reviewer that was asked for an unseeded pass produces the evidence directly instead of leaving it
to be reconstructed. Do not drop §6 in favour of this: both rounds above suggest the directed
questions are where the confirmed defects come from.»

## 7. Ground already walked — do not re-report, do challenge

Prior findings with severity labels and dispositions — sourced from the adjudication ledger
beside each report where one exists (`NN-REVIEW-ADJUDICATION.md` in a phase directory, bare
`REVIEW-ADJUDICATION.md` for a standalone target); its rows and its ruled auxiliary entries are
the dispositions. Split into:

- **Fixed** — table of `ID | issue | fix commit`. Task: is each fix complete, correct, and
  free of new defects — and did any of them open a new path to the failure it closed?
- **Never dispositioned** — the titles, verbatim, plus the note that they appear nowhere
  outside the review document: no ruling, no acceptance, no deferral, no tracking issue.

> What we want from you on these: not restatement. Tell us if **any** of them is materially
> more severe than its assigned label — in particular whether any can produce a *wrong result
> that looks right*, or a *green test run that proves nothing*. Silence on the rest is fine.
>
> **Spend the majority of your effort outside this list.** The most valuable thing you can
> return is a defect the internal review had no category for.

Include candid corrections already on record and ask whether the reasoning around them holds.

«If no prior review exists, keep the section but reduce it to one line — "No prior review
has been performed; you are the first reviewer." Do not omit it: an unstated absence reads
as withheld history.»

## 8. Evidence standard

> A finding is admissible only with all of:
> 1. **Location** — `path/to/file:line`.
> 2. **Mechanism** — why the code does the wrong thing, in terms of the code's own logic.
> 3. **Trigger** — a concrete input, filesystem state, argv, or environment that reaches it.
>    "A malformed PNG" is not a trigger; "a greyscale PNG with a tRNS chunk" is.
> 4. **Consequence** — what the user, the output, or the exit code gets wrong. Tie it to a
>    success criterion or documented guarantee.
> 5. **Status** — **CONFIRMED** (you executed something and observed the failure; include
>    command and output) or **THEORETICAL** (reasoned from source; say what stopped you).
>    Do not blur these. A CONFIRMED finding is worth several THEORETICAL ones — worth
>    meaning credibility and the effort you should spend confirming, never rank, which
>    impact alone decides — and mislabelling one destroys the value of the whole report.

«For a plan or design doc there is nothing to execute — restate CONFIRMED as "cited and
quoted a source that settles it: the spec, the oracle, the library's documentation, a
benchmark" and THEORETICAL as "reasoned without a source." The five-part structure stays.»

«When the work under review makes claims about how models behave under instruction, admit a
third status — SELF-REPORT: the reviewer's introspective account of its own processing,
stated as introspection with its limits, never dressed up as CONFIRMED.»

Then one standing instruction, verbatim:

> If this prompt is itself defective — a citation that does not match the file, two
> instructions that contradict each other, a leaked authoring placeholder — report that at
> the top of your reply and do not guess at the intended scope or permissions. A defect in
> the prompt is a finding about the process, and it is wanted.

## 8b. What you may and may not do

Its own headed block, so the reviewer cannot miss it. Fill every row even when the answer is
"no" — an omission reads as permission to one model and as prohibition to another.

```markdown
## What you may and may not do

| | |
|---|---|
| **Read** | «in-scope set». You may also read «lockfiles, CI config, sibling project» for context |
| **Write** | Your report at `«path/to/NN-EXTERNAL-REVIEW.md»` — create and append to it as you work. «Nothing else: do not modify any other file» / «plus throwaway probes under «dir» only» |
| **Execute** | «npm test, npm run typecheck, npm run cli -- …». «Note slow/destructive ones» |
| **Network / installs** | «No. Do not install packages or fetch anything; the lockfile is part of what you are auditing» |
| **Your own tools** | «Web search allowed for CVEs and upstream library behavior — cite the URL for any finding sourced that way. No subagents.» |
| **Effort** | «Depth over breadth. Five CONFIRMED findings beat thirty observations.» |
```

Then the write boundary in prose — one of:

- **Read-only apart from the report:** "Read, run the test suite, and write your report to
  `«path/to/NN-EXTERNAL-REVIEW.md»`. Modify nothing else — that one file is the only write
  you are authorized to make, and it is authorized. Run only commands verified not to rewrite
  repository files or external state — snapshot-updating test runners and cache-writing builds
  count as writes; where a command would mutate, do not run it and say what was withheld.
  Where a finding needs execution to confirm and you cannot get it without writing, mark it
  THEORETICAL and say exactly what would settle it. Commit nothing."
«For a plan or design target there is nothing to run: the Execute row is "nothing," and the
sentence reduces to "Read, write your report to «path», modify nothing else."»

«Keep the report authorization and the do-not-modify rule in the same sentence. Split across
two paragraphs they read as a contradiction, and the reviewer resolves contradictions
conservatively — by not writing the file, which is the one output that matters.»

- **Mutation authorized:** "**Mutation testing is the highest-value technique available to you
  here**, because the central question is not 'do the tests pass' but 'would they fail if the
  code were wrong.' Break something deliberately — invert a comparison, drop a guard, change
  `>=` to `>` — and see whether the suite notices. A silent survival is a finding only when
  you show the mutation changes required, reachable, observable behaviour while the tests
  stay green — equivalent mutants, unreachable code, and behaviour outside the contract
  prove nothing. You may write throwaway probes. Put them somewhere
  obviously temporary, commit nothing, leave «paths» as you found them, and report the tree
  clean when you finish."

«If you tell the reviewer what the closing `git status` should look like, **produce that listing by
running the command as you write this brief** — never from memory of what you changed. The tree
almost always holds things you did not think of, this brief and its cover note among them once you
save them, and a reviewer told "any other line is a finding against you" against a list you
reconstructed will find your own untracked files sitting in it. Either paste the real current
output and name which lines the reviewer is expected to add, or ask only that the tree be reported
and judge it yourself.»

## 9. Anti-patterns — output that will be discarded

- Style, naming, formatting, or comment-density opinions. Not wanted.
- "Consider adding X" with no defect behind it. A suggestion is not a finding.
- Restating a code comment as though verifying it. See §2.
- Proposing out-of-scope functionality.
- Impact inflation. If it cannot produce a wrong result, lost data, a wrong exit code, or a
  false-green test, it is not critical — mark it low and rank it accordingly.
- A flat or tied ranking. "These are all equally important" is a refusal to do the one piece
  of judgement being asked for. Order them.
- Hedged findings that commit to nothing. If unsure, say "could not determine" and say what
  would settle it.
- A defect you found and then talked yourself out of, on the authority of a nearby comment or of
  a test written around the behavior as it stands. Report it, with your reasoning for thinking it
  deliberate. Silence here is the most expensive output in this list.
- Praise. One short paragraph at most, and only for things you actually verified.

## 10. Deliverable

**The report is a file the reviewer writes, not a message it sends.** State this first in the
section, before the skeleton, and state it as a mechanic rather than a preference:

> **Write your report to `«path/to/NN-EXTERNAL-REVIEW.md»` as you go.** Create the file early —
> before your first finding — with the title and your identity, and append each finding to it
> as you confirm it. Findings arrive in discovery order, so finish with a closing pass that
> re-orders them into the strict rank the skeleton below demands and fills in the coverage
> line — only then do you know what you covered. That closing pass is expected, and it is not
> composing at the end: what is forbidden is holding the report only in memory.
> «Where it has actually happened, one line of why: a previous run of this brief was told to
> return its report in chat, that message never reached the author, and because nothing was on
> disk the whole audit was lost.» A partial file is recoverable; an interrupted composition is
> not. Writing that one file is authorized — see the permissions block above.
>
> **In your chat reply, give a short summary only:** your coverage line, the ranked finding
> titles with their impact levels, and the path to the file. Keep every detail — mechanisms,
> triggers, commands, outputs, suggested fixes — in the file. Do not paste the report into the
> reply as well; a duplicate that drifts from the file is worse than no duplicate.

«If several reviewers receive this same brief, give each a distinct path —
`NN-EXTERNAL-REVIEW-<reviewer>.md` — and say the file is theirs alone, so the second run
cannot overwrite the first.»

**Do not ask the reviewer for a verdict.** Whether the work ships, or is marked complete, is
the owner's call and not the reviewer's — and a model that commits to YES or NO early will
bend the findings underneath it to stay consistent with itself. What the verdict was really
buying is *commitment*, and a strictly ordered findings list buys it better: forced ranking
with no ties is a judgement the reviewer cannot hedge its way out of.

Give the exact markdown skeleton you want back:

```markdown
# Independent Audit — «target»
**Reviewer:** <model/version>   **Date:** <date>
**Coverage:** «N of M load-bearing claims engaged; what you read; what you ran; what you
did not substantively examine»

## Findings, ranked
Most important first, strict order, no ties. If two seem equal, decide which you would fix
first and say why. Rank by the cost of leaving it unfixed: blast radius of the wrong
behaviour × likelihood its trigger is actually reached. Evidence status is not impact — a
THEORETICAL data-loss defect outranks a CONFIRMED cosmetic one. Where you could not execute
a trigger, say what would settle it instead of demoting the finding.

Do not judge whether this work should ship or be marked complete — that is not your call, and
a position you commit to up front will distort everything below it. Report what is wrong and
what it costs; the ordering is your judgement.

### 1. <one-line title>
- **Class** — wrong result / data loss / broken published contract / false-green test /
  robustness / hygiene «plan/design targets add: invalid assumption / omitted alternative /
  irreversible design constraint»
- **Impact** — critical / high / medium / low, judged from the stated consequence and how
  readily the trigger is reached
- **Location / Mechanism / Trigger / Consequence / Status** (+ command & output if CONFIRMED)
- **Why it ranks here** — one clause
- **Suggested fix** — minimal, specific, no redesign

### 2. <one-line title>
…

## Claims examined and upheld
Short list, one line each, naming what upheld it — what you ran, or the primary source outside the
work. A claim you only backed with a nearby comment or a matching test name belongs in "could not
verify" instead. Coverage evidence, no elaboration.

## Could not verify
What you could not check and why. Be explicit: an unstated gap reads as a pass.

## Mutation results   «include only when mutation testing was authorized»
What you broke, whether the suite caught it. Table is fine.

## Disagreements with the internal review   «include only when a prior review exists»
Where you think its findings, severities, or non-dispositions are wrong.
```

The per-claim adjudication in §6 is unaffected by this — CONFIRMED / REFUTED / COULD NOT
DETERMINE on a single load-bearing claim is evidence about that claim, not a verdict on the
work, and it stays.

## 11. The author's own residual doubts — kept out, and not certified by you

Do not put your residual suspicions anywhere in the prompt, or in the cover note that hands it
over — the cover note is read first, so anchoring there is worse. A reviewer that reads them is
anchored by them, and demotion disclaimers do not survive contact. Collect 3–5, each phrased as a
question with a mechanism and the `file:line` it is about, and put them in the hand-off summary to
the user instead.

They will usually overlap the §6 claims — same reading, same seams. Where they do, the claim stays
sharp and the overlap is declared. What you must not do is report a doubt as *held back*: that is
a claim of absence in a document you wrote, it has been false on every occasion it has been made,
and it turns an echo into "independent corroboration". Run the skill's §9 cross-check, report the
brief items it lands on, and leave the ruling to whoever adjudicates the returned review.

The prompt itself ends after the deliverable. Close it with:

> Go find what none of this anticipated.

---

The prompt is one of two artifacts. The message that hands it to the reviewer has its own
skeleton: [cover-note-template.md](cover-note-template.md).
