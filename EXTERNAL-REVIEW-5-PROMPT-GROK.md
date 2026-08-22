# Adversarial audit — the validator, the ledger, and the calibration instrument

*(A different model is auditing a **different half** of this same range in parallel, from its own
brief. It has the two skills and their references; you have the executable validator, the
adjudication ledger, and the calibration corpus. See §8 — the split is deliberate.)*

You are auditing a small repository of two Claude Code "skills" — structured markdown instruction
files that a coding agent loads and follows — whose subject matter is running and adjudicating
cross-model reviews. **The repository is an instance of the thing it describes, and it is
currently being used on itself.** That is the main source of the defects you are looking for.

> Every line of the work you are about to audit was written by Anthropic's Claude, reviewed by
> Claude, and adjudicated by Claude against a ledger it also wrote. You are xAI's Grok. You have a
> different architecture and different training. **You will notice different things, and those
> things are the entire value of this exercise.**
>
> - **Confirmation is near-worthless output.** If you spend your effort re-deriving what the
>   ledger already claims and agreeing, this audit has failed.
> - **Your job is to find what is wrong, missing, or unjustified**, and to prove it.
> - **A manufactured finding is worse than no finding.** If a rigorous search comes back nearly
>   empty, say so and show the search — few or zero findings is an admissible result, and the
>   claims-examined-and-upheld section is where it earns its credibility.
> - **A finding that survives your own attempt to refute it is worth more than ten observations.**
>
> Assume competence, not correctness. Where this is wrong, it is wrong in ways its author cannot
> see — those places are what you are here for.

## 1. The single most important instruction

**This half of the repository is the half that claims to have stopped relying on prose.** A
validator was added specifically so that ten invariants "fail instead of needing to be noticed",
and the corpus digest was changed specifically so a calibration record stops expiring by accident.
Those are mechanical claims, and mechanical claims can be tested rather than argued about.

**Your central question is whether the mechanisms do what the documents say they do.** Not whether
the ideas are good. Real examples, quoted, all of which you should treat as untested assertions:

> `REVIEW-ADJUDICATION.md` §R4.12 — *"**The gate still fails on a real instrument change and no
> longer fails on a test run**"*

> `BACKLOG.md` `B-3` — *"**Each of the ten was break-tested** — mutated in a throwaway copy to
> confirm it fails when its invariant is broken… 9/9 mutations were caught"*

> `scripts/validate.py:1-9` — *"Every check here corresponds to a defect some review round found
> by reading prose. The point is that they now fail instead of needing to be noticed."*

You demonstrated on the calibration corpus that you will reach for mutation to convict **and** to
acquit. This brief is pointed at that capability deliberately.

## 2. Scope

**Pinned to immutable commits: `0d65b51..d411d1e`.** Over that exact range `git diff --stat`
reports **27 files changed, 3530 insertions(+), 406 deletions(-)**. Run it yourself. `HEAD` is
`d411d1e8de41c70919493c2e1420b68c4ce1a71e`.

**Your half of the split.** Counts taken at `d411d1e`:

| File | Lines | Note |
|---|---|---|
| `scripts/validate.py` | 301 | **new** — the executable validator |
| `REVIEW-ADJUDICATION.md` | 3613 | the ledger; round 4 is `§R4.*`, lines 2605+ |
| `calibration/record-template.md` | 81 | digest command changed |
| `calibration/README.md` | 163 | digest reasoning changed |
| `BACKLOG.md` | 123 | `B-3` marked partly discharged |
| `.adversarial-review/calibration/grok-4.6-high.md` | — | **new** — your own record |
| `.adversarial-review/calibration/gpt-5.6-sol-high.md` | — | the other reviewer's record |
| `EXTERNAL-REVIEW-5-GROK-VOID.md` | 244 | a void run, retained; header explains itself |

**Read for context, but the other reviewer owns them:** `skills/**`, `HOW-IT-WORKS.md`,
`README.md`. Read them freely — the validator checks them, so you will need them — but do not
spend your run auditing the skills' prose. Findings there are welcome if you trip over them; they
are not your assignment.

**One thing about your own calibration record.** You are being asked to audit a file that records
your own performance. That is not a conflict to hide from — it is a file with claims in it, and
the claims are checkable. If it overstates what your run established, say so. If the caveat it
carries is too weak or too strong, say that too.

## 3. The contract this work must satisfy

1. A check that cannot fail is not a check.
2. A check that fires on correct work is worse than no check.
3. The digest identifies the instrument, and nothing else.
4. Every claim these documents make about their own mechanisms is true.
5. The ledger is an accurate record of what was decided and what happened.

## 4. Load-bearing claims — attack these

Return **CONFIRMED**, **REFUTED**, or **COULD NOT DETERMINE** for each of the 17 below, one line
each, in your "Claims examined and upheld" or findings sections as appropriate.

### Group A — the validator, and whether it works

1. **All ten checks fail when their invariant is broken** — `BACKLOG.md` `B-3` claims 9/9
   mutations were caught. *That is the author testing their own harness. **Redo it.** Break each
   invariant in a copy under `/tmp` and record what fires and what does not. A check that stays
   silent is the finding.*
2. **No check fires on correct work.** *The inverse, and less likely to have been tested. Feed it
   valid-but-unusual input: a `SKILL.md` that mentions the guillemet characters inside backticks
   as part of its own instructions (all three real ones do), a
   table row with an escaped pipe, a ledger round with zero findings, a skill with no `references/`
   directory. Does anything false-positive?*
3. **`is_ruling_row` (`:157`) correctly distinguishes a ruling row from prose naming a verdict.**
   *It requires a **bolded** verdict. Construct rows it misclassifies in both directions. What
   happens to a row whose verdict is bolded inside a longer phrase, or split across a line?*
4. **The `last_round` scoping (`:162`) is right.** *Strict checks run only on the final `# Round N`
   section, on the argument that closed rounds are immutable. **Is that argument sound, or does it
   mean a defect introduced into an earlier round is now permanently invisible?** What if a file
   has no round headings at all?*
5. **`check_counts` (`:195`) verifies count-in equals count-out.** *It compares two numbers the
   author wrote in the same header. Does it check anything about reality, or does it check that a
   sentence agrees with itself?*
6. **`check_table_pipes` (`:131`) catches unescaped pipes that break rendering.** *Its backtick
   parity is computed per line. What does it do with an inline-code span opened on one line and
   closed on the next, or with a literal backslash-escaped pipe, which is valid markdown?*
7. **`corpus_digest` (`:214`) reimplements the command in `calibration/record-template.md:14`
   faithfully.** *Read both. Do they agree byte for byte on the same tree? If they diverge, which
   one is the instrument — and would anyone notice?*
8. **The ten checks are the right ten.** *They are the ten the author happened to hand-run on the
   day they wrote it. `B-3` lists invariants it does **not** cover. **Which uncovered one would
   have caught the most expensive defect in rounds 1–4?** That is the eleventh check, and its
   absence is a finding if it is cheap.*

### Group B — the digest, and what it now identifies

9. **`git ls-files` ends the artifact-inclusion defect** — a fixture run no longer moves the
   digest. *Verify it. Then attack the other direction: **what does it now silently miss?** The
   record template names uncommitted edits as a stated cost. Is that cost stated where a scorer
   would see it, and is "stated" enough?*
10. **The digest is portable across machines** — the previous `find`-based command was not,
    producing three different values on three checkouts. *Reproduce the new one somewhere else
    under `/tmp` and say whether it holds.*
11. **Both filed calibration records match the instrument.** *Check. Then ask what happens on the
    day someone legitimately edits a case: every record expires at once, correctly — but is there
    anything that tells the operator which records to re-earn, or do they simply go quiet?*
12. **`calibration/README.md`'s isolation rule is sufficient.** *It was followed for six runs after
    being violated once. Read it as an instruction someone will follow at speed. **Is there a step
    that is easy to get wrong, and does anything catch it?** The violated run is at
    `EXTERNAL-REVIEW-5-GROK-VOID.md` and its header describes exactly how it went wrong.*

### Group C — the ledger as a record

13. **Round 4's `Findings in: 27 · Rows out: 27` is exact.** *Count them. 26 in the `§R4.4` table
    plus `P-1`; two later findings were given an `X-` series specifically to keep the count exact.
    **Is that legitimate bookkeeping or is it moving findings off the books?***
14. **Every row in `§R4.4` carries both a verdict and a disposition, and every pairing is legal.**
    *The validator checks this now — after finding two illegal pairings the author's own manual
    check had missed. **Are there others it still misses**, in the auxiliary blocks, in `§R4.14`,
    or in earlier rounds it does not scope?*
15. **The append-only discipline held** — round 4 was appended, nothing above line 2601 edited.
    *Verify with `git`. Then: `§R4.10` and `§R4.6` were **edited in place** after being written,
    to mark them superseded. Round 4 is the current open round so that is permitted — **is it?**
    Read the closure definition and say whether editing a status section inside an open round is
    what the rule intends.*
16. **`§R4.14`'s account of `X-1` is accurate and complete** — that the round-4 restructure moved a
    defect into a reference file unchanged. *That is the author's own account of their own error.
    Check it against the diff. Is it the whole of what happened?*
17. **Your own calibration record (`grok-4.6-high.md`) accurately describes your six runs.** *Read
    it against the six reports in `.adversarial-review/calibration/runs/2026-08-22-grok-4.6-high/`.
    Does it overstate anything? Is the answer-key-exposure caveat correctly scoped — too strong,
    too weak, or right?*

## 4b. The unseeded pass — report it separately

The list above is directed, and a reviewer that only answers it produces coverage collapsed onto
seams the author already suspected. Measured on this repository: round 4 returned 18 echoes, 3
partial and **4 free** across 27 findings, and the four free ones are what that round's evidence
actually rested on. **One of those four was yours.**

**So run a second pass that sets the claims list aside**, reading the diff and the files on their
own terms, and report what it produced in its own section. A considered "nothing new" is a
result. Say which findings came from which pass.

## 5. Ground already walked — do not re-report, do challenge

Every finding from rounds 1–4 is dispositioned in `REVIEW-ADJUDICATION.md`: round 4's rows at
`§R4.4`, corrections to round 3 at `§R4.11`, execution at `§R4.12`, two out-of-round findings at
`§R4.14`. **Your own round-4 report is `EXTERNAL-REVIEW-4-GROK.md`** and all 13 of its findings are
ruled there.

- **Do not re-report these.** Re-finding a known issue is wasted effort.
- **For anything marked `✔ executed`: judge whether the fix is complete and correct.**
- **Spend the majority of your effort outside that list.**

One of your round-4 findings — `grok-10`, that dropping `Agent` would cause a permission prompt —
was **refuted** at `§R4.4` from Anthropic's tools reference, which lists `Agent` as requiring no
permission. That ruling is on the record and you are invited to contest it if you think it is
wrong. Two of your claims were also re-opened as `U-1` and `U-2`.

## 6. Evidence standard

For every defect: **Location** (file and line) · **Mechanism** (what is actually wrong) ·
**Trigger** (the concrete input or state — "a malformed ledger" is not a trigger, "a table row
whose inline-code span spans two lines" is) · **Consequence** (what is lost, tied to a contract
item in §3) · **Status** — **CONFIRMED** (you executed it, with command and output) or
**THEORETICAL** (reasoned from source; say what stopped you).

**You may not uphold a claim on the work's own word.** A docstring, a ledger row saying `✔
executed`, or `B-3`'s "9/9 mutations were caught" is the party under review talking. Confirming a
claim takes what refuting one takes — here, usually, running it. `COULD NOT DETERMINE` is the
honest alternative and costs one line.

Rank findings by the cost of leaving each unfixed — blast radius × likelihood the trigger is
reached — **strict order, no ties**, one clause of justification per position. Each carries an
**Impact** level (critical/high/medium/low) as an attribute, never as a section heading.

## 7. What you may and may not do

| | |
|---|---|
| **Read** | Everything in the repository, `.git` history included, **except the two files named below**. Read outside your assigned half freely for context |
| **Write** | **Your report at `EXTERNAL-REVIEW-5-GROK.md` in the repository root — create it early and append as you work.** Nothing else in the repository. Throwaway probes under `/tmp` only |
| **Execute** | `git` read commands, `grep`/`find`/`shasum`/`wc`, `python3 scripts/validate.py`, and **anything you like under `/tmp` — including copying the whole repository there and mutating it freely**, which is how you should test the validator. **Note:** the two-fixture pytest suite writes `__pycache__` if run in-tree; copy the fixtures to `/tmp` first |
| **Network + installs** | No installs. **Web search is allowed** where a claim turns on Anthropic's documented behaviour; cite the URL, and it will be weighed as a lookup rather than a discovery |
| **Your own tools** | Subagents and MCP servers are fine |
| **Effort budget** | Depth over breadth. Roughly 8–15 findings expected. **A CONFIRMED finding from a mutation you ran is worth several THEORETICAL ones** — though impact alone decides rank |

**In one sentence: read anything except the two files below, run read-only commands in the repo and
anything at all under `/tmp`, write your report to `EXTERNAL-REVIEW-5-GROK.md`, and modify nothing
else in the repository.**

### What you must not read

**Do not open `EXTERNAL-REVIEW-5-PROMPT-CODEX.md` or `EXTERNAL-REVIEW-5-CODEX.md`**, and do not let
a search tool print their contents. A parallel reviewer is auditing the other half from that brief.
Two reports agreeing means something only if the second could not read the first, and nothing
technically stops you — this is a request, not a mechanism. **If you do end up seeing one, say so
in your report.** You disclosed exactly this in round 4 and it was the right call.

**And one file you should read, carefully: `calibration/ANSWER-KEY.md` is in scope for this
brief.** You have already read it — the void run is on record. Nothing here is a calibration, so
there is nothing left to protect; it is simply a document with claims in it.

## 8. Anti-patterns — output that will be discarded

Style and naming opinions on `validate.py`. "Consider adding X" with no defect behind it.
Restating a docstring as verification. Severity inflation. Hedged findings that commit to nothing.
Praise beyond one paragraph. Re-reporting anything in §5.

**And one specific to this half:** "the validator only checks form, not truth" is already recorded
in `B-3` as a measured bound and is not a finding. What *would* be a finding is a specific
invariant that is both checkable and uncovered.

## 9. Deliverable

**Write your report to `EXTERNAL-REVIEW-5-GROK.md` in the repository root, as you go.** Create it
early with a title and your identity — model family, product and version, reasoning effort, and
your served model alias verbatim — then append each finding as you confirm it. Do not hold the
report in memory. The coverage line and the final ranked order are set in a closing pass; that is
expected.

Return only a short summary in chat: your coverage line, the ranked finding titles with impact
levels, and the file path.

Structure:

```
# External Review 5 (Grok) — the validator, the ledger, and the calibration instrument
Reviewer identity: [family, product and version, effort, served alias verbatim]

## Coverage
[N of 17 claims engaged; what you read; what you ran; what you did not substantively examine]

## Findings, ranked
[strict order by cost of leaving unfixed; Location · Mechanism · Trigger · Consequence · Status]

## Mutation results
[what you broke, what fired, what stayed silent — this is the section this brief exists for]

## The unseeded pass
[what the second pass produced, and which findings came from it]

## Claims examined and upheld
[one line per claim, naming what upheld it — never the work's own word]

## Could not verify
[an unstated gap reads as a pass]

## Disagreements with the prior rounds
[where you think a previous ruling or fix-verification was wrong, including any of your own]
```

**Do not give a ship/no-ship verdict.** Rank by what it would cost to leave each finding unfixed
instead. And if any two instructions in this brief contradict each other, report that as a process
finding — previous rounds have found good ones, including one of yours.
