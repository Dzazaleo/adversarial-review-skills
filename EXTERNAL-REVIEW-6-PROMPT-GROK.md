# Adversarial audit — the validator, the ledger, and the calibration instrument

You are auditing a small repository of two Claude Code "skills" — structured markdown instruction
files that a coding agent loads and follows — whose subject matter is running and adjudicating
cross-model reviews. **The repository is an instance of the thing it describes, and it is
currently being used on itself.** That is the main source of the defects you are looking for.

> Every line of the work you are about to audit was written by Anthropic's Claude, reviewed by
> Claude, and adjudicated by Claude against a ledger it also wrote. You are xAI's Grok 4.6. You
> have a different architecture and different training. **You will notice different things, and
> those things are the entire value of this exercise.**
>
> - **Confirmation is near-worthless output.** If you spend your effort re-deriving what the
>   ledger already claims and agreeing, this audit has failed.
> - **Your job is to find what is wrong, missing, or unjustified**, and to prove it.
> - **A manufactured finding is worse than no finding.** If a rigorous search comes back nearly
>   empty, say so and show the search.
> - **A finding that survives your own attempt to refute it is worth more than ten observations.**
>
> Assume competence, not correctness. Where this is wrong, it is wrong in ways its author cannot
> see — those places are what you are here for.

## 0. Read this part first — it is unusual and it matters

**This half of the repository has never been audited by anyone.** Five rounds of external review
have run here; every one of them was pointed at the two skills and their prose. A round-5 brief
was written for this half and, through an operator error, was never delivered — the cover note for
the *other* half was pasted into the reviewing session instead, so that reviewer read the wrong
brief, audited the wrong half, and wrote its report to the other reviewer's path, destroying it.
The full account is in `REVIEW-ADJUDICATION.md` §R5.1 and `P-1`.

So: `scripts/validate.py`, `REVIEW-ADJUDICATION.md` and `calibration/**` are the only parts of
this project with **no external review at all**, and everything anyone believes about them is the
author's own testimony.

**Second thing, and it is a conflict you should exploit rather than tiptoe around.** The most
recent commit in your audit range was written by the same Claude session that adjudicated round 5,
authorized itself against its own queue, executed nineteen fixes, and then wrote the ledger
sections claiming those fixes worked. **That session also extended the validator you are auditing,
and then used that same validator to certify its own output.** It reported one instance of the
validator catching its own regression, and presented that as evidence the validator earns its
place. That report is a claim by the party under review. Test it.

## 1. The single most important instruction

**This repository's prose asserts its own correctness constantly, and every such assertion is a
claim by the party under review, never evidence.** The tells are a ledger row reading `✔ executed`,
a `B-3` line saying a check was break-tested, and a section describing what a fix accomplished.

Real examples, quoted, all of which you should treat as untested assertions:

> `BACKLOG.md` `B-3` — *"**Each of the ten was break-tested** — mutated in a throwaway copy to
> confirm it fails when its invariant is broken… 9/9 mutations were caught"*

> `REVIEW-ADJUDICATION.md` §R5.15 — *"**All nineteen queued items landed.**"*

> `REVIEW-ADJUDICATION.md` §R5.15 — *"the mechanical check caught it where four rounds of reading
> had not"*

**The gap between "the document says the rule" and "the rule holds" is the seam this audit runs
along.**

## 2. Scope

**Pinned to immutable commits: `2565c08..c62ca24`.** `HEAD` is
`c62ca2491f13cae22459eb0ed75d6874002107dd`. Over that range `git diff --stat` reports
**13 files changed, 1144 insertions(+), 95 deletions(-)**. Run it yourself.

**One honest note about that commit.** `c62ca24` is a snapshot commit created so this audit has an
immutable range to work against; in the author's own checkout the same changes are still
uncommitted. The tree you have is the real one and the range is stable for your run. Nothing turns
on the hash except reproducibility.

**Your target is the whole half as it stands at `c62ca24`, not only the delta** — because none of
it has ever been reviewed. The delta is simply the newest and least-tested part.

| File | Lines | Note |
|---|---|---|
| `scripts/validate.py` | 354 | the executable validator; **two checks added in this range** |
| `REVIEW-ADJUDICATION.md` | 4101 | the ledger; round 5 is `§R5.*`, from line 3627 |
| `BACKLOG.md` | 123 | `B-3` records the break-testing claim |
| `calibration/README.md` | 163 | the protocol |
| `calibration/record-template.md` | 81 | carries the digest command |
| `calibration/ANSWER-KEY.md` · `calibration/cases/**` | — | the instrument itself |
| `.adversarial-review/calibration/grok-4.6-high.md` | — | **your own record** |
| `.adversarial-review/calibration/gpt-5.6-sol-high.md` | — | the other reviewer's record |
| `.adversarial-review/calibration/runs/2026-08-22-grok-4.6-high/` | 6 reports | your own six runs |
| `EXTERNAL-REVIEW-5-GROK-VOID.md` | 244 | a void run, retained; its header explains itself |

**Read for context, but they are not your assignment:** `skills/**`, `HOW-IT-WORKS.md`,
`README.md`. The validator checks them, so you will need them. Findings there are welcome if you
trip over them.

**You are being asked to audit your own calibration record.** `.adversarial-review/calibration/grok-4.6-high.md`
records how your six runs scored. That is not a conflict to hide from — it is a file with claims in
it, and the claims are checkable against the six reports filed beside it. If it overstates what
your run established, or gets its caveat wrong in either direction, that is a finding.

## 3. The contract this work must satisfy

1. A check that cannot fail is not a check.
2. A check that fires on correct work is worse than no check.
3. The digest identifies the instrument, and nothing else.
4. Every claim these documents make about their own mechanisms is true.
5. The ledger is an accurate record of what was decided and what happened.

## 4. Load-bearing claims — attack these

Return **CONFIRMED**, **REFUTED**, or **COULD NOT DETERMINE** for each of the 20 below.

### Group A — the validator, and whether it works

1. **All twelve checks fail when their invariant is broken.** `BACKLOG.md` `B-3` claims 9/9 for the
   original ten — the author testing their own harness. **Redo it for all twelve.** Break each
   invariant in a copy under `/tmp` and record what fires and what stays silent. A silent check is
   the finding.
2. **The two checks added in this range were break-tested.** *They were not.* §R5.15 reports that
   `check_retired_wordings` fired once, by accident, on the author's own regression — that is not a
   break-test, it is an anecdote. **Break both deliberately** and say what you find.
3. **No check fires on correct work.** The inverse, and less likely to have been tested. Feed it
   valid-but-unusual input: a `SKILL.md` naming the guillemet characters inside backticks, a table
   row with a backslash-escaped pipe, a ledger round with zero findings, a skill with no
   `references/` directory, a file with CRLF line endings.
4. **`check_retired_wordings` (`:264`) does what §R5.15 claims.** *It normalizes whitespace so a
   rule wrapped across a line break is still caught — the corrected form of a remedy that
   previously found 2 of 3 sites.* **Does normalization actually cover the cases that matter?**
   What about a retired phrase broken by a markdown emphasis marker, a footnote, or an inline code
   span mid-phrase? What about the same rule restated in different words — which is the failure the
   check was built for and may not touch at all?
5. **`check_retired_wordings`'s file scoping is right.** It exempts the ledger, the external
   reports and `examples/` so they can quote retired wordings as history. **Is that exemption
   sound, or does it mean the ledger can carry a stale rule forever?** The ledger is read by the
   next brief's author.
6. **`check_invariant_backrefs` (`:294`) is worth its line count.** It checks that `§N` in an
   invariants block names a section that exists. **Can it ever fail on this repository?** If a
   check cannot fail on the work it ships with, contract item 1 applies to it.
7. **The registry says thirteen and the program says twelve.** `CHECKS` holds 13 tuples;
   `--list` prints 13 names; the run prints "All 12 checks pass", because two registry entries
   share one function and `main()` dedupes. **Which number is a lie, and to whom?**
8. **`is_ruling_row` (`:157`) distinguishes a ruling row from prose naming a verdict.** It requires
   a bolded verdict. Construct rows it misclassifies in both directions.
9. **The `last_round` scoping (`:162`) is right.** Strict checks run only on the final `# Round N`
   section, on the argument that closed rounds are immutable. **Is that argument sound, or does it
   mean a defect introduced into an earlier round is permanently invisible?** Round 5 appended a
   new round while marking rows inside it — trace what the scoping did during that.
10. **`check_counts` (`:195`) verifies count-in equals count-out.** It compares two numbers the
    author wrote in the same header. Does it check anything about reality?
11. **`check_table_pipes` (`:131`) catches unescaped pipes.** Backtick parity is computed per line.
    What does it do with a code span opened on one line and closed on the next, or a valid
    backslash-escaped pipe? Three warnings currently fire on closed rounds — are they real?
12. **`corpus_digest` (`:214`) reimplements `record-template.md:14` faithfully.** Read both. Do
    they agree byte for byte on the same tree? If they diverge, which one is the instrument?
13. **The twelve checks are the right twelve.** `B-3` lists invariants they do not cover. **Which
    uncovered one would have caught the most expensive defect in rounds 1–5?**

### Group B — the digest, and what it identifies

14. **`git ls-files` ended the artifact-inclusion defect** — a fixture run no longer moves the
    digest. Verify it, then attack the other direction: **what does it now silently miss?**
15. **The digest is portable across machines.** Reproduce it somewhere else under `/tmp`.
16. **Both filed calibration records match the instrument, and the isolation rule is sufficient.**
    Read `calibration/README.md` as an instruction someone will follow at speed. **Is there a step
    that is easy to get wrong, and does anything catch it?** The violated run is at
    `EXTERNAL-REVIEW-5-GROK-VOID.md`.
17. **Your own record (`grok-4.6-high.md`) accurately describes your six runs.** Read it against
    the six reports in `.adversarial-review/calibration/runs/2026-08-22-grok-4.6-high/`. Does it
    overstate anything? Is the answer-key-exposure caveat correctly scoped?

### Group C — the ledger as a record, and round 5 in particular

18. **Round 5's header arithmetic is exact** — *"Findings in: 22 · Rows out: 22 · +3 process
    (P-3 withdrawn), +7 CNV, +8 prior-review disagreements ruled"*, and *"18 sampled · 4
    re-opened"*. **Count them.** `P-3` was withdrawn mid-adjudication after the validator rejected
    its verdict/disposition pairing. **Is withdrawing an ID legitimate bookkeeping, or is it moving
    a finding off the books?** The same question was asked of round 4's `X-` series and answered
    one way; check whether the answers are consistent.
19. **Round 5's append discipline held.** §R5 claims the first 3623 lines are byte-identical and
    proves it with a `head | diff`. **Verify with `git`.** Then: rows *inside* round 5 were edited
    in place afterwards to add `✔ executed` markers, under a rule the same session had just
    rewritten to permit exactly that. **Read the rewritten rule and say whether the rewrite was a
    genuine correction or a session widening a rule it was about to violate.** This is the sharpest
    question in this brief.
20. **§R5.15's account of the execution is accurate and complete.** It claims all nineteen items
    landed, that `review-adjudication/SKILL.md` went 499→497 lines while absorbing four fixes, and
    that the compression came from duplicated background whose full text survives in a reference.
    **Check the diff.** Was anything lost that was not duplicated? Is "no behaviour changed" true
    given `scripts/validate.py` gained two checks?

## 4b. The unseeded pass — report it separately

The list above is directed, and a reviewer that only answers it produces coverage collapsed onto
seams the author already suspected. Measured here: round 5 returned **19 echoes and 3 free findings
across 22**, and one of the three free ones was the process finding that exposed the whole
mis-pairing. **One of round 4's four free findings was also yours.**

**So run a second pass that sets the claims list aside**, reading the diff and the files on their
own terms. A considered "nothing new" is a result. Say which findings came from which pass.

## 5. Ground already walked — do not re-report, do challenge

Every finding from rounds 1–5 is dispositioned in `REVIEW-ADJUDICATION.md`. Round 5 is `§R5.*`;
its adjudication table is `§R5.4`, its process findings `§R5.5`, its corrections to round 4
`§R5.8`, and its execution record `§R5.15`.

- **Do not re-report these.** Re-finding a known issue is wasted effort.
- **For anything marked `✔ executed`: judge whether the fix is complete, correct, and whether it
  opened a new path to the failure it closed.**
- **Spend the majority of your effort outside that list.** The most valuable finding is one the
  ledger has no category for.

## 6. Evidence standard

For every defect: **Location** (file and line) · **Mechanism** · **Trigger** (the concrete
condition under which it bites) · **Consequence** (tied to a contract item in §3) · **Status** —
**CONFIRMED** (you checked it, with the command and output) or **THEORETICAL** (reasoned from
source; say what stopped you).

**You may not uphold a claim on the work's own word.** A ledger row saying `✔ executed`, or
`B-3`'s "9/9 mutations were caught", is the party under review talking. Confirming a claim takes
what refuting one takes. `COULD NOT DETERMINE` is honest and costs one line.

**Mutation testing is the point of this half.** You demonstrated in calibration that you break a
suite to convict and break one to acquit. That is exactly the capability this brief needs.

Rank findings by the cost of leaving each unfixed — blast radius × likelihood the trigger is
reached — **strict order, no ties**, one clause of justification per position. Each carries an
**Impact** level (critical/high/medium/low) as an attribute, never as a section heading.

## 7. What you may and may not do

| | |
|---|---|
| **Read** | Everything in this repository, `.git` history included |
| **Write** | **Your report at `EXTERNAL-REVIEW-6-GROK.md` in the repository root — create it early and append as you work.** Nothing else in the repository |
| **Execute** | `git` read commands, `grep`/`find`/`shasum`/`wc`, `python3 scripts/validate.py`, and **anything at all under `/tmp` — including copying this whole repository there and mutating it freely**, which is how the validator should be tested |
| **Network** | No installs. Web search allowed; cite URLs |
| **Effort budget** | Depth over breadth. Roughly 8–15 findings expected. One CONFIRMED finding is worth several THEORETICAL ones |

**One gotcha:** the two-fixture pytest suite writes `__pycache__` into the corpus if run in-tree,
which is exactly the artifact-inclusion problem claim 14 is about. Copy it to `/tmp` first.

**There is no parallel reviewer this time and nothing is withheld from you.** Read anything.

## 8. Anti-patterns — output that will be discarded

Style and naming opinions. "Consider adding X" with no defect behind it. Restating a ledger row as
verification. Proposing out-of-scope features. Severity inflation. Hedged findings that commit to
nothing. Praise beyond one paragraph. Re-reporting anything in §5.

**And one specific to this half:** "the validator only checks form, not truth" is already recorded
in the ledger as a known bound. Saying it again is not a finding. Naming a *specific* invariant
that is mechanically checkable and is not checked **is**.

## 9. Deliverable

**Write your report to `EXTERNAL-REVIEW-6-GROK.md` in the repository root, as you go.** Create it
early with a title and your identity — model family, product and version, reasoning effort, and
your served model alias verbatim — then append each finding as you confirm it. Do not hold the
report in memory. The coverage line and final ranked order are set in a closing pass.

Structure:

```
# External Review 6 (Grok) — the validator, the ledger, and the calibration instrument
Reviewer identity: [family, product and version, effort, served alias verbatim]

## Coverage
[N of 20 claims engaged; what you read; what you ran; what you did not examine]

## Findings, ranked
[strict order by cost of leaving unfixed; Location · Mechanism · Trigger · Consequence · Status]

## Mutation results
[per check: what you broke, what fired, what stayed silent — a table is fine]

## The unseeded pass
[what the second pass produced, and which findings came from it]

## Claims examined and upheld
[one line per claim, naming what upheld it — never the work's own word]

## Could not verify
[an unstated gap reads as a pass]

## Disagreements with the prior rounds
[where you think a previous ruling or fix-verification was wrong]
```

**Do not give a ship/no-ship verdict.** Rank by what it would cost to leave each finding unfixed.
And if any two instructions in this brief contradict each other, report that as a process finding;
every previous round has found good ones.
