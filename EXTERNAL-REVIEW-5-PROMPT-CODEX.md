# Adversarial audit — the round-4 fixes, and the restructure that carried them

*(A different model is auditing a **different half** of this same range in parallel, from its own
brief. You have the two skills and their references; it has the validator, the ledger and the
calibration corpus. See §8 — the split is deliberate and the boundary matters.)*

You are auditing a small repository of two Claude Code "skills" — structured markdown instruction
files that a coding agent loads and follows — whose subject matter is running and adjudicating
cross-model reviews. **The repository is an instance of the thing it describes, and it is
currently being used on itself.** That is the main source of the defects you are looking for.

> Every line of the work you are about to audit was written by Anthropic's Claude, reviewed by
> Claude, and adjudicated by Claude against a ledger it also wrote. You are OpenAI's GPT-5.6
> (Sol). You have a different architecture and different training. **You will notice different
> things, and those things are the entire value of this exercise.**
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

**This repository's prose asserts its own correctness constantly, and every such assertion is a
claim by the party under review, never evidence.** The tells here are a ledger row reading
`✔ executed`, a description of what a fix accomplished, and an invariant that states a rule as
though stating it enforced it.

Real examples, quoted, all of which you should treat as untested assertions:

> `REVIEW-ADJUDICATION.md` §R4.12 — *"**pass** — 484 and 498, from 529 and 587"*

> `skills/review-adjudication/SKILL.md:32` — *"**Write boundary, and append rather than rewrite.**… Add
> to the ledger's end and prove it"*

> `REVIEW-ADJUDICATION.md` §R4.12 — *"**The gate still fails on a real instrument change and no
> longer fails on a test run**"*

Each states that something is true. **The gap between "the document says the rule" and "the rule
holds" is the seam this entire audit runs along.**

## 2. What happened in this range, told straight

Four rounds of external review have been run on this repository. Round 4 was a dual audit — you
and an xAI Grok session, working from near-identical briefs — which returned 27 findings. **24
were confirmed and 24 changes were applied**, along with three owner decisions, in the range you
are about to audit.

Then two things happened that you should know before you start, because they bear on what to
suspect:

1. **A mis-scoped Grok run found two defects that had survived all 24 fixes.** One of them
   (`X-1`) was a defect the round-4 **restructure had moved into a reference file unchanged** —
   relocated, not repaired, by the session doing the repairing. The ledger records this at
   §R4.14 with the conclusion *"extracted text does not get re-read on the way out."*
2. **While writing this brief, the author found a third:** `§R4.10` of the ledger was a stale
   status section still claiming round 3 was open and listing closure requirements that had been
   met — the exact defect (`codex-13`) that round 4 confirmed against round 3, reproduced one day
   later. It is now marked superseded rather than rewritten.

**Both are the same shape: a change that reached one site of something living at several.** Treat
that as the highest-yield hypothesis in this audit rather than as background.

## 3. Scope

**Pinned to immutable commits: `0d65b51..d411d1e`.** Over that exact range `git diff --stat`
reports **27 files changed, 3530 insertions(+), 406 deletions(-)**. Run it yourself. `HEAD` is
`d411d1e8de41c70919493c2e1420b68c4ce1a71e`.

**Your half of the split** — the two skills and everything they load. Counts taken at `d411d1e`:

| File | Lines | Note |
|---|---|---|
| `skills/adversarial-review-prompt/SKILL.md` | 484 | was 529; restructured |
| `skills/review-adjudication/SKILL.md` | 498 | was 587; restructured |
| `skills/adversarial-review-prompt/references/prompt-template.md` | 486 | edited |
| `skills/review-adjudication/references/ledger-template.md` | 229 | edited |
| `skills/adversarial-review-prompt/references/why-this-is-hard.md` | 108 | **new — extracted** |
| `skills/review-adjudication/references/why-this-is-hard.md` | 34 | **new — extracted** |
| `skills/review-adjudication/references/inputs-and-calibration.md` | 98 | **new — extracted** |
| `skills/review-adjudication/references/verification-standard.md` | 126 | **new — extracted** |
| `skills/review-adjudication/references/second-opinion.md` | 54 | **new — extracted** |
| `HOW-IT-WORKS.md` | 795 | design doc; edited |
| `README.md` | 278 | edited |

**Read for context, but the other reviewer owns them:** `scripts/validate.py`,
`REVIEW-ADJUDICATION.md`, `calibration/**`, `BACKLOG.md`. Read them freely — you will need the
ledger to know what was claimed — but do not spend your run auditing the validator's logic or the
corpus. Findings there are welcome if you trip over them; they are not your assignment.

## 4. The contract this work must satisfy

1. A fix closes the finding it was applied for, at **every** site of the claim, not one.
2. An extraction preserves meaning and does not relocate a defect out of view.
3. What survives auto-compaction is the set of rules that must survive it.
4. Every claim the documents make about themselves is true.
5. The two skills do not contradict each other, their own references, or the design doc.

## 5. Load-bearing claims — attack these

Return **CONFIRMED**, **REFUTED**, or **COULD NOT DETERMINE** for each of the 18 below, one line
each, in your "Claims examined and upheld" or findings sections as appropriate.

### Group A — the restructure (owner decision `R4-Q2`, the largest change here)

1. **~9,300 characters of rationale were moved from the two `SKILL.md` files into five new
   `references/` files, and the move preserved meaning.** *`X-1` proves at least one extraction
   carried a defect through unchanged. **Read all five new files against what they replaced**
   (`git diff 0d65b51..d411d1e -- skills/`). Is there other text that was moved and should have
   been fixed? Is there anything in a reference file that is actually an instruction, and so is
   now outside the file the agent reads?*
2. **Both `SKILL.md` files are now under the documented 500-line guidance** — 484 and 498.
   *They are 16 and 2 lines under. Is a limit met by 2 lines met, or is this the shape of a
   number tuned to a threshold? Check whether anything was moved out purely to clear it.*
3. **The obligations added in round 4 now sit above the compaction cut** — the verifier-exposure
   rule and the append-not-rewrite rule are in `skills/review-adjudication/SKILL.md`'s `<invariants>`
   block at `:32-35` and `:49`. *Verify they are there and that they say what the full rule says.
   An invariant that summarizes the opposite of its own section is a defect round 4 found twice.*
4. **The cut estimates are now labelled as estimates** — `skills/adversarial-review-prompt/SKILL.md:24`
   says *"around line 221"* and `skills/review-adjudication/SKILL.md:28` says *"around line 214"*, both
   *"from a measured ~3.1 characters per token."* *That rate came from your own round-4
   measurements, back-computed. **If you can tokenize these files, do it and say where 5,000
   rendered tokens actually lands.** If the estimate is wrong, which rules are past the real cut?*

### Group B — fixes that had to reach several sites

5. **The blindness claim was aligned everywhere** — `skills/review-adjudication/SKILL.md:439` now reads
   "was not handed the report", and `HOW-IT-WORKS.md` likewise. *Grep the whole repository for
   every remaining variant — "blind", "never saw", "never seen", "not handed". Did it reach every
   site this time, including the five new reference files?*
6. **The unconditional architecture sentence is gone from every emit path.** `prompt-template.md`
   resolves it in four branches; `HOW-IT-WORKS.md:80` now carries the same placeholder. *That
   second copy was found by an outside run, not by round 4. **Is there a third?** Search for the
   claim, not for the files you were told about.*
7. **The overwrite guard now covers brief, cover note and report**
   (`skills/adversarial-review-prompt/SKILL.md:327` and invariant 6). *Does the guard's own instruction
   — "Check each with `ls`/`Glob`" — actually bind, given the skill no longer grants `Write` at
   all? And what about the ledger, which `review-adjudication` §7 says to append to?*
8. **The `FIX LATER` ordering contradiction is resolved** — invariant 4 at `:44` and §6 at `:420`
   both now say *"before the row receives its `FIX LATER` disposition."* *Is that satisfiable
   under step 2's skeleton-first rule? Read both and say.*
9. **The residual-doubts dependency is now disclosed rather than denied** — `README.md` tells the
   operator to keep the hand-off, and `ledger-template.md:42-47` makes a doubts line **required**.
   *Does the required field actually make absence visible, or is it another sentence? What stops
   an adjudicator writing "unavailable" and moving on?*

### Group C — the independence machinery

10. **Author provenance is now a required input** (`skills/adversarial-review-prompt/SKILL.md:117`).
    *Is it actually collected before the sentence that needs it, or is it stated as required and
    then never used? Trace it to the branch selection.*
11. **Four branches now cover the real authorship cases** and each carries its own payoff line
    (`prompt-template.md:54`). *Read the emitted block at `:35-41` and each branch. Does any
    branch still promise something the branch above it denies? Does the fourth branch exist for
    a case the skill can actually detect?*
12. **The same-family blind-spot assertion was downgraded to a caution** rather than sourced.
    *Is the new wording a caution, or an assertion with a hedge in front of it?*

### Group D — the skills' own coherence

13. **Neither skill pre-approves any write-capable tool** — both are `Read, Grep, Glob`.
    *So both skills now produce their deliverables through tools they have not pre-approved.
    **Does either skill still work end to end?** Nobody has run one since the change. Read the
    procedures and say where a permission stop now lands, and whether any instruction assumes a
    write that will not happen.*
14. **The no-filesystem route is now consistent with the invariants** — invariants 1 and 4 carry
    the exception, and §10 has the continuation item. *Follow that route end to end through the
    skill as written. Does it produce a coherent set of instructions?*
15. **The five new reference files are reachable and used.** *Every `references/` link resolves —
    that is checked mechanically. But is each file **pointed at from the place the reader needs
    it**, or are there orphans a reader would never open?*
16. **`HOW-IT-WORKS.md` matches the skills it describes.** *It is 795 lines and was edited twice
    in this range, both times reactively. Read it against the skills and find what else drifted.*
17. **`README.md`'s new permissions section is accurate** (`:139-170`). *It claims `Edit(path)`
    rules are consulted for writes and `Write(path)` rules are not. Check the current Anthropic
    documentation and say whether the snippet it offers would actually do what it says.*
18. **The ledger's `§R4.14` conclusion is right** — *"extracted text does not get re-read on the
    way out."* *Is that the correct lesson from `X-1`, or is the real lesson something else the
    author would rather not have concluded?*

## 5b. The unseeded pass — report it separately

The list above is directed, and a reviewer that only answers it produces coverage collapsed onto
seams the author already suspected. Measured on this repository: round 4 returned 18 echoes, 3
partial and **4 free** across 27 findings, and the four free ones are what that round's evidence
actually rested on.

**So run a second pass that sets the claims list aside**, reading the diff and the files on their
own terms, and report what it produced in its own section. A considered "nothing new" is a
result. Say which findings came from which pass.

## 6. Ground already walked — do not re-report, do challenge

Every finding from rounds 1–4 is dispositioned in `REVIEW-ADJUDICATION.md`. Round 4's rows are
§R4.4; its corrections to round 3 are §R4.11; the two out-of-round findings are §R4.14.

- **Do not re-report these.** Re-finding a known issue is wasted effort.
- **For anything marked `✔ executed`: judge whether the fix is complete, correct, and whether it
  opened a new path to the failure it closed.**
- **Spend the majority of your effort outside that list.** The most valuable finding is one the
  ledger has no category for.

Two candid corrections already on record, offered because judging them is useful: §R4.12 records
that the restructure *"moved ~9,300 characters of motivating history out of the two skills"* and
calls it *"a trade, not a clean win"*; §R4.14 records that the same restructure relocated `X-1`
rather than fixing it. **Ask whether the surrounding reasoning was sound**, and whether the trade
was correctly described.

## 7. Evidence standard

For every defect: **Location** (file and line) · **Mechanism** (what is actually wrong) ·
**Trigger** (the concrete condition under which it bites — "a compacted session" is not a trigger,
"a session that invokes the skill, compacts once, and reaches step 5" is) · **Consequence** (what
is lost, tied to a contract item in §4) · **Status** — **CONFIRMED** (you checked it, with the
command and output) or **THEORETICAL** (reasoned from source; say what stopped you).

**You may not uphold a claim on the work's own word.** A comment, a ledger row saying `✔
executed`, or a heading is the party under review talking. Confirming a claim takes what refuting
one takes. `COULD NOT DETERMINE` is the honest alternative and costs one line.

**The shape to name as unacceptable is the reviewer that reaches a defect and then decides the
work meant it**, on the authority of a nearby sentence. That is ranked below missing it outright:
it leaves the next reader the bug plus a written case for keeping it. If you get that far, report
the finding and say why you think it is deliberate — a finding with a note, never a dismissal.

Rank findings by the cost of leaving each unfixed — blast radius × likelihood the trigger is
reached — **strict order, no ties**, one clause of justification per position. Each carries an
**Impact** level (critical/high/medium/low) as an attribute, never as a section heading. Evidence
status is not impact.

## 8. What you may and may not do

| | |
|---|---|
| **Read** | Everything in the repository, `.git` history included, **except the two files named below**. Read outside your assigned half freely for context |
| **Write** | **Your report at `EXTERNAL-REVIEW-5-CODEX.md` in the repository root — create it early and append as you work.** Nothing else in the repository. Throwaway probes under `/tmp` only |
| **Execute** | `git` read commands, `grep`/`find`/`shasum`/`wc`, any tokenizer you have, `python3 scripts/validate.py`, and anything under `/tmp`. **Note:** the two-fixture pytest suite writes `__pycache__` into the corpus if run in-tree — copy the fixtures to `/tmp` and run them there if you want them |
| **Network + installs** | No installs. **Web search is allowed and encouraged** for the Claude Code documentation claims — several turn on what `allowed-tools`, `Edit(path)` rules and auto-compaction actually do. Cite the URL; it will be weighed as a lookup, not a discovery |
| **Your own tools** | Subagents and MCP servers are fine |
| **Effort budget** | Depth over breadth. Roughly 8–15 findings expected. One CONFIRMED finding is worth several THEORETICAL ones for credibility — though impact alone decides rank |

**In one sentence: read anything except the two files below, run read-only commands and anything
under `/tmp`, write your report to `EXTERNAL-REVIEW-5-CODEX.md`, and modify nothing else.**

### What you must not read

**Do not open `EXTERNAL-REVIEW-5-PROMPT-GROK.md` or `EXTERNAL-REVIEW-5-GROK.md`**, and do not let
a search tool print their contents. A parallel reviewer is auditing the other half from that
brief. Two reports agreeing means something only if the second could not read the first, and
nothing technically stops you — this is a request, not a mechanism. **If you do end up seeing
one, say so in your report.** That is still useful; quietly reading one is not.

Everything else, including `EXTERNAL-REVIEW-5-GROK-VOID.md`, is fair game — that file is a void
calibration run, retained because it found `X-1` and `X-2`, and its header explains itself.

## 9. Anti-patterns — output that will be discarded

Style and naming opinions. "Consider adding X" with no defect behind it. Restating a comment or a
ledger row as verification. Proposing out-of-scope features. Severity inflation. Hedged findings
that commit to nothing. Praise beyond one paragraph. Re-reporting anything in §6.

**And one specific to this repository:** "this is very long" is not a finding. `review-adjudication`
is 498 lines because four rounds of review put rules in it. If length costs something, name the
rule that gets lost and the run that loses it.

## 10. Deliverable

**Write your report to `EXTERNAL-REVIEW-5-CODEX.md` in the repository root, as you go.** Create it
early with a title and your identity — model family, product and version, reasoning effort, and
your served model alias verbatim — then append each finding as you confirm it. Do not hold the
report in memory. The coverage line and the final ranked order are set in a closing pass; that is
expected and is not composing-at-the-end.

Return only a short summary in chat: your coverage line, the ranked finding titles with impact
levels, and the file path.

Structure:

```
# External Review 5 (Codex) — the round-4 fixes and the restructure
Reviewer identity: [family, product and version, effort, served alias verbatim]

## Coverage
[N of 18 claims engaged; what you read; what you ran; what you did not substantively examine]

## Findings, ranked
[strict order by cost of leaving unfixed; Location · Mechanism · Trigger · Consequence · Status]

## The unseeded pass
[what the second pass produced, and which findings came from it]

## Claims examined and upheld
[one line per claim, naming what upheld it — never the work's own word]

## Could not verify
[an unstated gap reads as a pass]

## Disagreements with the prior rounds
[where you think a previous ruling or fix-verification was wrong]
```

**Do not give a ship/no-ship verdict.** Rank by what it would cost to leave each finding unfixed
instead. And if any two instructions in this brief contradict each other, report that as a process
finding — previous rounds have found good ones.
