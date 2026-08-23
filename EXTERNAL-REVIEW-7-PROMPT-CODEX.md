# Adversarial audit — `scripts/validate.py`, the validator that certified its own rewrite

You are auditing the single executable in a small repository of two Claude Code "skills" —
structured markdown instruction files that a coding agent loads and follows. The skills' subject
matter is running and adjudicating cross-model reviews, and **the repository is an instance of the
thing it describes, currently being used on itself.**

`scripts/validate.py` is the mechanical gate for that process. It went from 354 lines to 519 in the
range you are auditing.

> Every line of the code you are about to audit was written by Anthropic's Claude, reviewed by
> Claude, and adjudicated by Claude against a ledger it also wrote. It currently reads as complete
> and passing: `12 of 12 checks pass (2 warning(s))`, exit 0.
>
> That is exactly the problem. A model validating its own work carries the same blind spots into
> the review that it had while writing — the same misreadings, the same unexamined assumptions, the
> same things it never thought to test because it never thought of them at all. This work was
> written by Anthropic's Claude. You are OpenAI's GPT-5.6. You have a different architecture and
> different training. **You will notice different things, and those things are the entire value of
> this exercise.**
>
> - **Confirmation is near-worthless output.** If you spend your effort re-deriving what is already
>   claimed correct and agreeing, this audit has failed.
> - **Your job is to find what is wrong, missing, or unjustified**, and to prove it.
> - **A manufactured finding is worse than no finding.** If a rigorous search comes back nearly
>   empty, say so and show the search — few or zero findings is an admissible result, and the
>   claims-examined-and-upheld section is where it earns its credibility.
> - **A finding that survives your own attempt to refute it is worth more than ten observations.**
>   Try to break your own findings before reporting them.
>
> Assume competence, not correctness. The validator is carefully built. Where it is wrong, it is
> wrong in ways its author cannot see — those places are what you are here for.

## 0. Read this first — the conflict you are here to resolve

**Every change in your audit range was written, tested and certified by one Claude session, which
then wrote the ledger recording that it worked.** That session:

- ruled on 15 external findings and raised 7 more of its own,
- rewrote roughly half of `scripts/validate.py` in response,
- **ran its own 29-probe mutation suite against the result**,
- reported `18 of 18 must-fail caught, 11 of 11 must-pass clean`,
- and wrote `REVIEW-ADJUDICATION.md` §R6.16 saying so.

The ledger's own §R6.19 states the problem in the author's words:

> *"This session wrote 27 changes to the validator and the skills, then certified them with the
> validator it had just rewritten, then wrote this ledger saying they worked. … Nothing in §R6.16,
> §R6.18 or §R6.19 should be read as independently verified."*

**That admission is not a substitute for the check. It is the reason you are here.** Your job is
to find what that suite missed. It was written by the same mind that wrote the code, so it tests
the failure modes that mind imagined.

**Two defects in those fixes were already found by running them, and both are recorded.** They tell
you the shape of what to hunt: (1) the first version of the cell-splitting fix split rows on
*escaped* pipes, shifting every column after one and mis-reading both ledger axes; (2) the row
counter mis-classified auxiliary IDs and counted 57 rows where 27 were stated. **Both are
off-by-one-assumption parsing bugs in markdown-table handling, and both survived the author's first
review of its own code.** Assume there are more.

## 1. The single most important instruction

**This repository's prose asserts its own correctness constantly, and every such assertion is a
claim by the party under review, never evidence.** A docstring saying what a check catches, a
ledger row reading `✔ executed`, and a `BACKLOG.md` line reporting a mutation score are all the
author talking.

Quoted, and all to be treated as untested assertions:

> `REVIEW-ADJUDICATION.md` §R6.16 — *"**18 of 18 must-fail cases caught** … **11 of 11 must-pass
> cases clean**"*

> `BACKLOG.md` `B-3` — *"**Every check was re-broken after the round-6 fixes**, both to confirm it
> fails on its invariant and to confirm it stays quiet on correct work"*

> `scripts/validate.py:189-196` — the `row_cells` docstring, asserting that splitting on unescaped
> pipes is the correct cell boundary rule

**The gap between "the docstring states the rule" and "the code implements the rule" is the seam
this audit runs along.** The previous round found four checks silent on the invariant they were
named for and two firing on correct work. Those were fixed. **Find the next four.**

## 2. Scope

**Pinned to immutable commits: `2565c08..d610112`.** `HEAD` is `d610112`. Over that range
`git diff --stat` restricted to the work (excluding review artifacts) reports **15 files changed,
491 insertions(+), 171 deletions(-)**. Run it yourself.

**Your target is `scripts/validate.py` as it stands at `d610112` — the whole file, not only the
delta.** It has never been read by anyone outside the family that wrote it.

| File | Lines at `d610112` | Note |
|---|---|---|
| `scripts/validate.py` | **519** | **your assignment** — was 354 before this range |
| `REVIEW-ADJUDICATION.md` | 5234 | the ledger the checks operate on; §R6.2 and §R6.16 are the author's own mutation records |
| `BACKLOG.md` | 159 | `B-3` and `B-4` record what the validator is claimed to buy |
| `skills/review-adjudication/SKILL.md` | 496 (`wc -l`) / **497** (`split("\n")`) | the checks read this; note the two counts differ and the gate uses the second |
| `skills/adversarial-review-prompt/SKILL.md` | 493 / **494** | same |
| `calibration/record-template.md` | 83 | carries the digest command `corpus_digest()` mirrors |
| `.adversarial-review/calibration/*.md` | 2 records | the digest and expiry checks read these |

**A second reviewer is auditing the prose half in parallel** — the skills, the ledger's content, the
backlog and the calibration documentation, under `EXTERNAL-REVIEW-7-PROMPT-GROK.md`. **You are not
reading that brief and it is not reading yours.** Findings outside your half are welcome if you trip
over them; do not go looking.

## 3. The contract this work must satisfy

1. A check that cannot fail is not a check.
2. A check that fires on correct work is worse than no check.
3. A check's behaviour matches what its name, its docstring and `--list` say it does.
4. The run's final line is a true statement about what was verified.
5. Nothing the validator reports depends on which machine it runs on.

## 4. Load-bearing claims — attack these

Return **CONFIRMED**, **REFUTED**, or **COULD NOT DETERMINE** for each of the 20 below.

### Group A — markdown-table parsing, where both known bugs lived

1. **`row_cells` (`:186-196`) identifies table cells correctly.** `CELL_SPLIT_RE` is
   `(?<!\\)\|` — split on any pipe not preceded by a backslash. *A markdown cell ending in a
   literal backslash is written `\\` and is then followed by a real `|` delimiter. What does the
   lookbehind do there?* Construct the row and say what happens to every column after it.
2. **`ruling_cells` (`:198-211`) finds the verdict and disposition columns.** It takes `cells[-2]`
   and `cells[-1]` and skips rows with fewer than three cells. *What happens to a ruling row that
   ends with a trailing empty cell, or a table whose disposition is not the last column?* The
   ledger contains tables of 3, 4 and 5 columns — check all three shapes against real rows.
3. **`BARE_VERDICT_RE` (`:173`) catches a half-filled skeleton row.** It is `^\**(VERDICT…)`.
   *Does `^\**` admit `***CONFIRMED`? Does a verdict cell that opens with the word in prose —
   `CONFIRMED by execution, but see the row above` — get read as a ruling?* Both directions.
4. **`declared_disposition` (`:177-184`) returns what a row commits to, not what it mentions.** It
   returns the **first** bolded term that is a known disposition. *What does it return for
   `**PENDING OWNER — proposed: NO ACTION**`, or for a cell that quotes another row's disposition
   before stating its own?*
5. **`DISPOSITION_RE` (`:174`) matches disposition tokens.** It is `\*\*([A-Z][A-Z ,'-]*?)\*\*` —
   uppercase, spaces, commas, apostrophes, hyphens, non-greedy. *That character class was widened
   in this range to admit a comma. What else does it now admit, and what legitimate bolded text in
   a ledger cell does it swallow or split?*
6. **`table_rows` (`:138-141`) skips separator rows and yields real ones.** The skip pattern is
   `^\|[\s:|-]+\|?$`. *Is there a real content row it discards?* Consider a row whose cells are all
   dashes or colons.

### Group B — the row count, which is the check the last round was bought to fix

7. **`AUX_ID_RE` (`:286`) separates auxiliary series from numbered findings.** It is
   `^(CNV|[PDUACXQ])[0-9]*(-|$)` applied to `bare_id`, which strips emphasis and a leading round
   prefix. *Seven single uppercase letters are reserved. What happens to a numbered finding whose
   reviewer tag begins with one of them* — a reviewer tagged `C`, `Q`, `D`, or a finding id like
   `A1-3`? Findings that match are silently excluded from the count.
8. **`count_finding_rows` (`:307-318`) counts the numbered findings and nothing else.** *Does it?*
   Run it against every round in the ledger and compare with each round's stated `Rows out`.
9. **`check_counts` (`:320-351`) verifies the stated count against reality.** The row count runs
   **only on the current round**; closed rounds get the header-against-header check alone. *The
   defect this check was rewritten to close was a dropped row with a consistent header. Can a row
   still be dropped from a closed round without the validator noticing?* If yes, say what the fix
   actually bought.
10. **`rounds` (`:295-305`) slices the file into rounds.** When there is no `# Round N` heading it
    returns a single section named `(no round heading)`. *Trace what `check_counts` does to a ledger
    with no round headings, and to one whose last round has no header numbers at all.*

### Group C — the current-round boundary and the closed-round warnings

11. **`reporter` (`:230-240`) errors inside the current round and warns before it.** The test is
    `i > cur_line` where `cur_line` comes from `current_round_line`. *Check the boundary: the first
    table row after a `# Round N` heading, and a row on the heading line itself.* Off-by-one here
    silently moves a defect from error to warning.
12. **`current_round_line` and `last_round` (`:218-228`) agree on where the current round starts.**
    They are separate functions computing the same thing from the same regex. *Do they agree for
    every input, including a file whose only round heading is at byte 0?*
13. **Closed-round violations warn and never fail the build.** *Confirm, then attack the other
    direction: is there a defect class that should error and now only warns because it happens to
    sit in the closed prefix?*

### Group D — the checks that read files outside the ledger

14. **`check_calibration_digests` (`:369-396`) fails a stale or expired record.** It errors on a
    missing digest row, a mismatched digest, a missing `**Expires**` row, and a past date. *The
    expiry comparison is a string comparison of ISO dates against
    `__import__("datetime").date.today().isoformat()`. Is that sound? What does it do to a record
    whose Expires row is present but not in the exact pipe-table form the regex expects?* A record
    that legitimately documents a different window would now hard-fail the build.
15. **`corpus_digest` (`:357-367`) still reproduces `calibration/record-template.md`'s command
    byte for byte.** Read both. Run both. *Do they agree on this tree — and does the Python half
    depend on anything the shell half does not?*
16. **`check_frontmatter` (`:46-80`) catches a write-capable grant however it is spelled.** A
    string-valued `allowed-tools` is coerced by `raw.replace(",", " ").split()`. *What other legal
    YAML spellings of that key exist, and does the coercion handle them?* Consider a quoted string,
    a block scalar, a nested list, and a null value.
17. **`check_links` (`:109-124`) resolves every relative link and does not fire on valid ones.** It
    takes `parts[0]` of the captured path. *CommonMark also permits an angle-bracket destination
    and a path containing balanced parentheses. What does this do with each?*
18. **`check_retired_wordings` (`:413-446`) catches a retired rule through markup.** It strips
    footnote markers, then normalizes whitespace, then strips `*`, `_` and backticks. *The footnote
    strip runs before whitespace normalization — what happens to a footnote marker broken across a
    line break?* Also: stripping `_` changes `snake_case` identifiers. Does any retired phrase
    contain one?
19. **`check_placeholders` (`:93-107`) catches an unresolved guillemet outside inline code.** It
    removes inline code with `` `[^`]*` `` before scanning. *What does it do with a fenced code
    block containing guillemets, and with an unclosed backtick?* The previous round's mutation table
    records fences as passing — establish whether that is by design or by accident.

### Group E — what the run says about itself

20. **`main` (`:488-520`) prints a true statement.** It reports `{len(passed)} of {len(unique fns)}
    checks pass`, excludes skipped checks from the numerator, and `--list` prints the named
    invariants plus a line reconciling names to implementations. *Is the reconciliation arithmetic
    right when three names share one function? Is there any path where a check raises, is never
    added to `ran`, and the totals still read as a clean run?* Trace an exception inside any check.

## 4b. The unseeded pass — report it separately

The list above is directed, and a reviewer that only answers it produces coverage collapsed onto
seams the author already suspected. **Measured on this repository twice: 10 of 15 findings were
echoes of the brief's sub-questions in the last round, and 6 of 9 the round before.** The two free
findings in the last round are the reason it was worth running.

**So run a second pass that sets the claims list aside**, reading `scripts/validate.py` on its own
terms as a program. A considered "nothing new" is a result. Say which findings came from which pass.

## 5. Ground already walked — do not re-report, do challenge

Every finding from rounds 1–6 is dispositioned in `REVIEW-ADJUDICATION.md`. Round 6 is `§R6.*`; its
adjudication table is `§R6.4`, its own findings `§R6.6`, its execution record `§R6.16`, and its
statement of what it could not establish `§R6.19`.

**Specifically already found and fixed in your range** — do not re-report these, do judge whether
each fix is complete and whether it opened a new path to the failure it closed:

- `check_counts` compared two header numbers and counted nothing
- both ledger axes were read by scanning the whole line, producing two false positives and a false
  negative
- the strict checks ran only on the last round, so closed-round defects were invisible
- digest mismatch was a warning; expiry was not checked at all
- valid GFM escaped pipes and valid titled markdown links failed the build
- a `Write` grant via a YAML string was invisible; a skipped check counted as a passing one
- retired wordings were silent through emphasis, code spans and footnote markers

**Spend the majority of your effort outside that list.** The most valuable finding is one the ledger
has no category for.

**Two things the author already knows and does not need told again:** that the validator checks form
rather than truth (recorded as a measured bound in `B-3`), and that summary faithfulness — whether a
`(§N)` back-reference *describes* its section — is not mechanically decidable (recorded as `A-3`,
reopened). Naming a *specific* invariant that is mechanically checkable and is not checked **is** a
finding.

## 6. Evidence standard

For every defect: **Location** (file and line) · **Mechanism** · **Trigger** (the concrete input or
state under which it bites — "a malformed row" is not a trigger, "a row whose penultimate cell ends
in a literal backslash" is) · **Consequence** (tied to a contract item in §3) · **Status** —
**CONFIRMED** (you ran it, with the command and output) or **THEORETICAL** (reasoned from source;
say what stopped you).

**You may not uphold a claim on the work's own word.** A docstring, a ledger row reading
`✔ executed`, or `B-3`'s mutation score is the party under review talking. Confirming a claim takes
what refuting one takes: execution, or a primary source outside the work. `COULD NOT DETERMINE` is
honest and costs one line.

**If you reach a defect and conclude the author meant it, report it anyway** with a note saying why
you think it is deliberate. A finding with a note is useful; a dismissal on the authority of a
nearby comment leaves the next reader both the bug and a written case for keeping it.

**Mutation testing is the point of this audit.** The question is not "does the validator pass" but
"would it fail if the thing it checks were wrong, and stay quiet when the thing is right." Break
each check deliberately in a copy and record both directions.

Rank findings by the cost of leaving each unfixed — blast radius × likelihood the trigger is
reached — **strict order, no ties**, one clause of justification per position. Each carries an
**Impact** level (critical/high/medium/low) as an attribute, never as a section heading. Evidence
status is not impact: a THEORETICAL wrong-result defect outranks a CONFIRMED cosmetic one.

## 7. What you may and may not do

| | |
|---|---|
| **Read** | Everything in this repository, `.git` history included |
| **Write** | **Your report at `EXTERNAL-REVIEW-7-CODEX.md` in the repository root — create it early and append as you work.** Nothing else in the repository |
| **Execute** | `git` read commands, `grep`/`find`/`shasum`/`wc`, `python3 scripts/validate.py`, and **anything at all under `/tmp` — including copying this whole repository there and mutating it freely**, which is how the validator should be tested |
| **Network** | No installs. Web search is allowed; cite the URL for anything sourced that way |
| **Your own tools** | Subagents and MCP servers as you see fit |
| **Effort budget** | Depth over breadth. Roughly 8–15 findings expected. One CONFIRMED finding is worth several THEORETICAL ones |

**One gotcha:** `calibration/cases/clean-wordcount/` and `trap-unfalsifiable-test/` contain pytest
fixtures that write `__pycache__` into the corpus if run in-tree. `__pycache__` is gitignored so it
will not move the digest, but copy them to `/tmp` before running anything.

**A second gotcha:** the repository currently prints two `WARN disposition` lines for
`REVIEW-ADJUDICATION.md:2383` and `:2384`. **Those are deliberate and permanent** — two rows written
in round 3 under a rule that has since changed, retained as history under an append-only invariant.
They are not defects to report and not defects to repair. §R6.15 documents them.

## 8. Anti-patterns — output that will be discarded

Style and naming opinions. "Consider adding X" with no defect behind it. Restating a docstring as
verification. Proposing out-of-scope features. Severity inflation. Hedged findings that commit to
nothing. Praise beyond one paragraph. Re-reporting anything in §5.

**And one specific to this target:** "the validator only checks form, not truth" is already recorded
as a known bound. Saying it again is not a finding. Naming a *specific* mechanically-checkable
invariant that is not checked **is**.

## 9. Deliverable

**Write your report to `EXTERNAL-REVIEW-7-CODEX.md` in the repository root, as you go.** Create it
early with a title and your identity — model family, product and version, reasoning effort, and your
served model alias verbatim — then append each finding as you confirm it. Do not hold the report in
memory; if the run is cut short, half a report on disk beats none. The coverage line and the final
ranked order are set in a closing pass, which is expected and is not composing-at-the-end.

Structure:

```
# External Review 7 (Codex) — scripts/validate.py
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

**In your chat reply, return only a short summary** — your coverage line, the ranked finding titles
with impact levels, and the file path. Keep all detail in the file.

**Do not give a ship/no-ship verdict.** Rank by what it would cost to leave each finding unfixed.
And if any two instructions in this brief contradict each other, report that as a process finding;
every previous round has found good ones.
