# Adversarial Independent Audit — the fixes applied to your own round-1 findings

> **Prompt for an external reviewer (OpenAI Codex).** Hand this file to a model that did **not**
> write the fixes under review. Everything below is written to be read by that reviewer, not by
> the author.

## 1. Why you are here

You audited this repository once already. You returned fifteen numbered findings, two process
findings and three could-not-verify items, and the report is on disk at `EXTERNAL-REVIEW.md`.
**Every one of your fifteen findings was ruled CONFIRMED or CONFIRMED (partial). None was
refuted.** Fourteen were fixed, one was deferred with a backlog artifact, and three questions went
to the owner and came back answered.

This round audits the fixes.

That is a different job from the first one, and the failure mode is different too. The first round
asked whether a defect existed. This round asks a narrower and more slippery question: **does each
change actually close the finding it claims to close, or does it name the defect and move on?** A
fix written by the model that was told what the defect was will tend to restate the problem in
better prose and stop there. It will also tend to fix the sentence that was quoted rather than the
rule the sentence was part of.

Every line of these fixes was written by Claude, in one session, immediately after reading your
report — which means it had your argument in front of it while writing, and had every incentive to
produce something that looks like a closure. Nobody has checked them. **You have a different
architecture and different training, and you wrote the findings, so you are the only reader who
knows what each fix was supposed to achieve.**

- **Confirmation is near-worthless output.** "Fix 7 addresses finding 7" re-derived from the diff is
  not a check.
- **Your job is to find where a fix is incomplete, wrong, or bought at a cost nobody priced**, and
  to prove it.
- **A manufactured finding is worse than no finding.** If a rigorous pass finds that the fixes hold,
  say so and show the search — few or zero findings is an admissible result, and §9's
  claims-examined-and-upheld section is where it earns its credibility. Some of these fixes are
  one-line corrections of an overclaim and there is genuinely not much to say about them.
- **A finding that survives your own attempt to refute it is worth more than ten observations.**

One thing to hold onto, because it is what this target keeps failing at. **The most likely defect
here is a rule and its description drifting apart.** Three of your own fifteen findings were exactly
that shape — a record field the consumer never reads (F8), a caveat carried in one document and
dropped in the next (F5), a pointer naming a path nothing installs (F15). The fix round then did it
again: while writing *this brief*, the author found that the F14 fix had left both consuming skills
describing the key it had just replaced. That is recorded as **C-1** in the ledger and is already
corrected. The open question is whether any further instance survives, and that is claim 19.

## 2. The single most important instruction

**A document that describes its own limitation is not thereby free of it, and a fix that states the
right rule is not thereby a rule anyone can follow.**

Several of these fixes work by *narrowing a claim* rather than by changing a mechanism — F7, F10,
F11, F12, F13 all replace an overclaim with an honest description of what the thing actually does.
That is a legitimate way to close a finding whose defect was the overclaim. It is not a legitimate
way to close a finding whose defect was the mechanism. **For each one, decide which the finding
actually was**, and say so where you think the round took the cheaper of the two.

The other half of the instruction: several fixes add a new *rule* to a long skill file. A new rule
is a new claim, and it is testable the same way. Ask of each:

- Could a reader actually execute it, or does it require a judgement the rule does not supply?
- Does it contradict anything else in the same file? These skills are 480 and 416 lines and the
  fixes touched seven separate places in one of them.
- Does it re-import the problem it was written to remove?

Real examples, quoted from what you are about to read:

> "copy the claim clause verbatim, and replace the argument with a pointer to the report line it
> came from"
> — `skills/review-adjudication/SKILL.md:196-197`

> "Where the review you are adjudicating covered something far larger, that gap is stated in the
> header"
> — `skills/review-adjudication/SKILL.md:89-91`

> "So spawn it read-only where the tool grants let you"
> — `skills/review-adjudication/SKILL.md:384-385`

> "This is a note for whoever reads the record, and nothing more."
> — `calibration/record-template.md:54-55`

Each of those is a fix. Each is also a claim about what a future reader will be able to do.

## 3. Environment and how to run things

| | |
|---|---|
| Repo root | `/Users/leo/Documents/WORK/CODING/adversarial-review-skills` |
| Branch | `calibration-corpus-and-claim-cards` |
| OS | macOS (Darwin 25.5.0) |
| Runtime | Python 3.14.3 on `python3`; `pytest` available |
| Build / typecheck / CI | none exists, for the repository itself. This is the state you confirmed in F9 and it has not changed |

### The audit range

Pinned:

```
8c1d737  Add the reviewer-calibration corpus and the claim-card change   <- the state you reviewed
fb237a0  Adjudicate the Codex review and apply the 14 fixes it earned    <- under review
9d892d0  Correct a contradiction the F14 fix introduced, and one stale heading
3ec5baf  Add the round-2 patch-verification brief and its cover note     <- this file; see below
25c4644  Record a scoping note: the cadre-derived rules are unaudited
2e4e7e4  Record the calibration run: PASS, and five findings against the corpus
e1fc88b  Fix the five corpus defects the calibration run found, plus a sixth
```

**The work under review is `8c1d737..e1fc88b`**, observed at authoring time as:

```
$ git diff --stat 8c1d737..e1fc88b
24 files changed, 2383 insertions(+), 69 deletions(-)
```

`8c1d737` is byte-for-byte the tree you audited in round 1 — all 25 blob hashes pinned in that
brief resolve against it. So `git diff 8c1d737..e1fc88b` is exactly the set of changes this round is
about, and `git show 8c1d737:<path>` gives you the before-state of any file without reconstruction.

`e1fc88b` is `HEAD`. There is nothing above the range.

**One commit in that range is this brief itself** (`3ec5baf`), and one is a scoping note
(`25c4644`). Both are documentation about the review rather than work under review; ignore them
except where §6 points you at them.

**The last two commits are a second layer of change, and they are in scope.** After the fixes were
written, the calibration corpus was run for the first time — six cases against you, in fresh
sessions rooted outside this repository. That run **passed** (4/4 traps, 1/2 clean) and found six
defects in the corpus itself, which were then fixed. Two of those fixes amend fixes you are also
being asked to audit: `K-5` rewrites the record filename rule that the `F14` fix introduced, and
`K-6` narrows the corpus digest that the `F1` fix introduced. **Fixes-to-fixes are the least
reviewed material here** — they were written last, fastest, and with the most confidence.

Two files in that diff are **artifacts of the round, not fixes**: `REVIEW-ADJUDICATION.md` (1078
lines, the ledger) and `BACKLOG.md` (59 lines). They are in scope as *evidence*, per §5 — you are
checking rulings against them — but a prose complaint about how the ledger is written is not a
finding unless it changes what someone would do.

### Commands

```bash
git diff 8c1d737..e1fc88b                     # the whole change
git show 8c1d737:calibration/ANSWER-KEY.md    # any file as you reviewed it
git log --oneline 8c1d737..e1fc88b            # the six commits, in order
cd /tmp && mkdir -p a2 && cd a2 && cp -R <repo>/calibration/cases/clean-wordcount wc1
(cd wc1 && python3 -m pytest -q)              # observed: 5 passed
```

The two pytest suites are unchanged in substance and still print `5 passed` and `3 passed`. The
*case files* did change late in the range — `K-1` added `calibration/cases/clean-copy-link/viewer.html`
and `K-2` corrected an interpreter name in two case READMEs. That is claim 3 and claim 21.

## 4. Scope

**In scope — the diff `8c1d737..e1fc88b`:**

| Path | Lines now | What changed |
|---|---|---|
| `calibration/ANSWER-KEY.md` | 101 | one trap gained a second primary defect; the pass-rule overclaim corrected; a paragraph pricing the 1-of-2 threshold |
| `calibration/CALIBRATION-PROMPT.md` | 47 | the fixed brief gained a counterweight to "agreement means failure"; envelope rewritten by `K-3` |
| `calibration/README.md` | 142 | isolation narrowed to "not confinement"; record key rewritten; expiry rewritten; then `K-4` (identity capture), `K-5` (filename rule), `K-6` (digest scope) |
| `calibration/record-template.md` | 65 | identity block replaced with four fields; corpus commit → corpus digest; severity note demoted; digest narrowed by `K-6` |
| `calibration/cases/clean-copy-link/viewer.html` | 16 | **new** — added by `K-1` so the plan names a file that exists. A change to a negative control |
| `calibration/cases/*/README.md` | — | `K-2`: `python` → `python3` in two case READMEs |
| `.adversarial-review/calibration/` | — | the calibration record and six archived raw reports. Evidence for claim 24 |
| `skills/review-adjudication/SKILL.md` | 485 | seven separate amendments — frontmatter, calibration input, claim-card rule, pre-registration, echo rule, subagent boundary |
| `skills/adversarial-review-prompt/SKILL.md` | 416 | calibration input rewritten; calibration pointer becomes a URL |
| `skills/adversarial-review-prompt/references/prompt-template.md` | 373 | two authoring rules added (§3 inventory, §8b expected status) |
| `HOW-IT-WORKS.md` | 781 | the public-corpus concession rewritten; three consistency corrections |
| `README.md` | 239 | "Keep the clone" added to Install |
| `REVIEW-ADJUDICATION.md` | 1078 | the ledger — evidence, see §5 |
| `BACKLOG.md` | 59 | the F9 deferral artifact |

**Read for context, not in scope for findings:** `examples/**`, `EXTERNAL-REVIEW.md` (your own round-1
report), `EXTERNAL-REVIEW-PROMPT.md`, `LICENSE`, and the unchanged parts of both skills — **except**
where an unchanged part contradicts a change. That contradiction is in scope and is the single most
valuable thing you can find here (see §1 and claim 19).

### The one-way door in this round

`calibration/CALIBRATION-PROMPT.md` is the **fixed** brief — the constant held still so that a
calibration measures the reviewer rather than that day's prompt. This round changed it. Any
calibration record produced before this commit is now measuring against a different instrument, and
the corpus digest is the only thing that would notice. Whether that was handled, and whether the
change to the constant was worth it, is claim 2.

## 5. The contract these fixes must satisfy

`REVIEW-ADJUDICATION.md` is the source of truth for what each fix was supposed to do. Its §3 table
carries one row per finding, and each row's Disposition cell names **the minimal fix** that was
supposed to close it, followed by `✔ executed 2026-08-21` and a description of what actually
landed.

Your job on each claim below is to compare three things:

1. **The finding** — yours, in `EXTERNAL-REVIEW.md`, with its Mechanism and Consequence.
2. **The named minimal fix** — the ledger row's disposition.
3. **What is actually in the diff.**

A gap between 2 and 3 is a fix that diverged from its own plan. A gap between 1 and 3 is a fix that
does not close the finding. Both are findings for you. **A fix that closes 1 by a different route
than 2 is not a defect** — say so and move on.

Three of the rulings were the owner's, not the adjudicator's, and are recorded verbatim in ledger
§5: Q1 (the checksum trap gates on either of two defects), Q2 (the 1-of-2 clean threshold stands,
the overclaim is corrected), Q3 (the record binds family, product version and effort). **Those three
decisions are settled and are not yours to relitigate.** Whether the implementation matches the
decision is very much yours.

## 6. Load-bearing claims — adjudicate every one

Return **CONFIRMED**, **REFUTED**, or **COULD NOT DETERMINE** for each of the 24 below, one line
each minimum. The italicised sub-question is the seam.

### A. Fixes that changed a mechanism

**1.** F1's fix replaces `git rev-parse --short HEAD` with a content digest
(`calibration/record-template.md:14`, expiry rule at `calibration/README.md:106-111`). The ledger
claims this makes the corpus identity change when the corpus changes without a commit. **`K-6` then
narrowed it**, after the first real record exposed that digesting the whole `calibration/` tree
expired records for edits to operator documentation the reviewer never sees. It now reads
`find calibration/cases calibration/CALIBRATION-PROMPT.md calibration/ANSWER-KEY.md -type f | sort | xargs shasum | shasum | cut -c1-12`.
*Run it. Does it hold up as an identity? Consider: `find` with no `-print0` and `xargs` splitting on
whitespace; what happens with a filename containing a space; whether `xargs` can invoke `shasum`
more than once on a large tree and change the output; whether `.DS_Store` or an editor swapfile
inside `calibration/` silently moves the digest; and whether the value is stable on a machine that
is not this one. An identity that changes when the corpus did not is a different failure from the
one it replaced, but it is still a failure — it expires records for no reason. **Then check `K-6`'s
narrowing in the other direction: is the new file set the right one?** It now excludes
`calibration/README.md`, which contains the isolation recipe and the scoring rule. If an operator
changes how cases are scored, should every record survive that?*

**2.** F2's fix adds a counterweight at `calibration/CALIBRATION-PROMPT.md:7-11` beside the
"if you spend your effort … agreeing, this review has failed" framing at `:3-5`.
*Read the two paragraphs as a reviewer would, in order. Does the second retract the first, or sit
beside it as a contradiction the reviewer must resolve? And separately: this file is the fixed
constant (§4's one-way door). Changing it invalidates comparison with any record made before it —
does anything in the corpus, the record template, or either skill acknowledge that, or has the
instrument been changed silently?*

**3.** Q1's implementation gives `trap-unfalsifiable-test` two primary defects, either of which
scores it (`calibration/ANSWER-KEY.md:29`, rationale at `:32-40`, pass rule at `:70-71`, record at
`calibration/record-template.md:35-40`).
*The scoring vocabulary column at `:29` now merges two defects' search terms, and
`calibration/README.md:50` still tells the scorer to find the passage by searching those terms.
Does the scoring procedure still work, or does a search that now matches twice as much text make
the "assertion, not vocabulary" rule harder to apply than it was? Note that the case files were
untouched when this change was made and were then edited later by `K-1`/`K-2` — see claim 21.*

**4.** F14/Q3's implementation replaces the record's identity block with four fields
(`calibration/record-template.md:7-16`, note at `:18-24`) and rewrites the key in
`calibration/README.md:72-80`. **`K-5` then rewrote the filename rule** (`:89-95`), because the
original form contradicted its own stated intent — it said to slug the model identity while also
promising that a run at a different effort files a separate record, which a bare model slug cannot
express. The primary form now ends with the effort.
*Both skills look the record up **by filename**. Follow that path end to end: given a reviewer that
reports only "OpenAI Codex, GPT-5-based" at high effort, can an adjudicator and a brief-author
independently arrive at the same filename? If two people would file the same reviewer under two
different names, the lookup misses and the record reads as absent — which is the state the fix was
written to escape. A real record now exists at
`.adversarial-review/calibration/gpt-5.6-sol-high.md`; check whether the rule as written actually
produces that name, or whether the scorer had to improvise.*

**5.** F4's fix renames `Task` → `Agent` (`skills/review-adjudication/SKILL.md:12`) and adds a
delegation-boundary rule at `:379-385`.
*Is `Agent` correct for the Claude Code version this targets? Then the rule itself: "spawn it
read-only **where the tool grants let you**" — is that an instruction or a wish? Does the skill say
anywhere how to actually restrict a subagent's tools, and if not, does the fix close F4's stated
consequence (that the subagent may edit the target) or only document it?*

**6.** F15's fix points the four in-skill references at a URL
(`skills/review-adjudication/SKILL.md:144,474`; `skills/adversarial-review-prompt/SKILL.md:76-78,394`)
and adds "Keep the clone" to `README.md:126-130`.
*Reproduce the install from `README.md:118-122` and check the fix from the installed skill's point
of view. A URL resolves for a human reading the hand-off — does it resolve for the skill, which
cannot fetch? Is the user who followed the install now able to run the 20-minute procedure, or have
they been told where it is and left to find it?*

### B. Fixes that narrowed a claim rather than changing a mechanism

For each of these, the question in §2 applies: was the finding's defect the overclaim, or the thing
the overclaim was covering for?

**7.** F7 — `skills/review-adjudication/SKILL.md:264-271` removes "the pre-registration is what
carries the weight here" and replaces it with a statement that pre-registration works on the
adjudicator in the moment and is **not** proof to a later reader.
*Does anything else in the repository still make the stronger claim? Check
`skills/review-adjudication/references/ledger-template.md:60-61` and `:70-71` — that file was **not**
touched by this round. If the template still asserts what the skill now denies, the fix moved the
overclaim rather than removing it.*

**8.** F8 — `calibration/record-template.md:54-58` deletes "The adjudicator reads this when weighing
rank" and makes the severity line "a note for whoever reads the record, and nothing more."
*Your finding was a dilemma: either the note is followed and contradicts the silence-only rule, or
it is ignored and a field presented as operational is inert. **The fix chose the second horn.** Is
that a closure or a concession? Is there now any reason for the field to exist, and if not, is a
field that exists to be ignored better or worse than the contradiction it replaced?*

**9.** F11/Q2 — `calibration/ANSWER-KEY.md:94-97` corrects "does not rate correct work as critical"
to "spared at least one of two correct artifacts", and `:84-89` adds a paragraph stating that a
reviewer may raise a serious finding on half the negative controls and still pass.
*Check the corrected sentence is actually entailed by the pass rule at `:70-71` and does not
overshoot in the other direction. Then check `HOW-IT-WORKS.md:734-737`, which carried the same
overclaim — was it corrected consistently, or does the repository now say two different things about
what a pass means?*

**10.** F12 — `calibration/README.md:26-33` adds "Be exact about what this buys": the recipe removes
adjacent discovery and is not confinement.
*You confirmed this one by execution in round 1. Does the new text state the limitation accurately —
in particular, does it match what you actually observed about a process rooted at the temp
directory? And does anything downstream still treat a calibration run as blind?*

**11.** F13 — `calibration/README.md:106-109` marks 30 days "a chosen default, not a derived one".
*Cheapest possible fix for the finding as stated. Is the finding as stated the whole finding? The
record template at `:13` still computes `Expires` as run date + 30 days with no way to record that a
shorter window was chosen — does the concession change anything an operator does?*

**12.** F10 — `HOW-IT-WORKS.md:741-751` rewrites the public-corpus concession so replacement is "only
a direction", and states outright that nothing in the repository helps a user do it.
*Your finding had two halves: the recall exposure, and the absent replacement procedure. The fix
addresses the second by conceding it harder. Does anything now prevent a user from following the
direction and building a bent ruler — or is the honest concession the whole remedy available, in
which case say so and mark this upheld.*

### C. New rules the fixes introduced

**13.** F6's fix at `skills/review-adjudication/SKILL.md:191-199` handles the mixed field: "copy the
claim clause verbatim, and replace the argument with a pointer to the report line it came from."
*Try it on a real case. `EXTERNAL-REVIEW.md:12` (your F1 Mechanism) mixes claim and evidence in one
field. Split it by this rule. **Who decides where the claim ends and the argument begins?** The claim
card existed to remove the adjudicator's judgement from the transcription step; does this rule put a
judgement back in, and is the judgement it puts back smaller than the one it removes?*

**14.** F5's fix at `skills/review-adjudication/SKILL.md:88-93` tells the adjudicator to read the
record's size caveat and state the gap "where the review you are adjudicating covered something far
larger".
*"Far larger" than what, measured how? The corpus is six cases of one to three small files; a real
target might be a 50-file phase or a 400-line plan. Is there any threshold at which this fires, or
has an unfalsifiable instruction been added — one that an adjudicator satisfies by writing a
sentence regardless of the facts?*

**15.** P-3's fix at `skills/review-adjudication/SKILL.md:324-336` requires an echo audit: probe
every finding against the brief with the finding's own identifiers and record which findings the
brief had already named.
*This rule was written because 10 of your 15 round-1 findings turned out to be echoes of the brief's
own §5 sub-questions. Two questions. First: does the rule as written actually produce a reliable
answer, given the author of the search chooses the queries — the same failure mode already recorded
at `:317-323` for residual doubts? Second, and more interesting: **is the conclusion the rule draws
sound?** A brief that directs a reviewer at a seam and gets a confirmed defect back has arguably
done its job well. Does scoring that agreement "as nothing" discard real information?*

**16.** P1 and P2's fixes at `skills/adversarial-review-prompt/references/prompt-template.md:79-84`
and `:245-252` require the file inventory to be enumerated and the expected `git status` to be
produced by running it.
*Both are authoring-time instructions in a template with no enforcement. Does either fix prevent the
defect you found, or does it depend entirely on the author choosing to comply — and if the latter,
is that different from the state before?*

### D. The round's own integrity

**17.** The ledger claims all 15 findings were ruled with evidence, and §2 records the commands and
outputs.
*Spot-check three re-verifications of your choosing against the actual repository — RV-3 (the
install reproduction), RV-5 (the claim-card field analysis, which claims 4 of your 15 findings mix
claim and argument in Mechanism), and RV-6 (the echo audit, which claims 10 of 15 are echoes). Do
the numbers reproduce? RV-6's table is the one that most changes how your round-1 report is
weighted, so check whether its "no line found" verdicts for F1, F2 and F15 are right — grep the
round-1 brief and cover note yourself.*

**18.** The ledger's §6 discloses four changes made "beyond the named minimal fixes" and C-1 records
a defect introduced by the F14 fix.
*Is that disclosure complete? Diff the whole range and look for any change that is not accounted for
by a ledger row, the four disclosed consistency edits, or C-1. An undisclosed change in a round whose
entire premise is disclosure is worth reporting even if the change itself is harmless.*

**19.** **The flagged defect class.** C-1 records that the F14 fix left both consuming skills
describing the record key it had replaced, and that three of your fifteen findings were the same
shape — a rule and its description drifting apart.
*Sweep for further instances across the whole range. For each rule these fixes changed, find every
place in the repository that **describes** that rule and check it was updated: the corpus digest,
the two-primary trap, the four-field key, the 1-of-2 threshold, the severity note, the calibration
pointer. `README.md` and `HOW-IT-WORKS.md` are the likeliest homes for a stale description, and
`skills/review-adjudication/references/ledger-template.md` was not touched at all.*

**20.** Ledger §8 claims the largest gap under this round is that the calibration corpus has never
been run, and that five fixes correct claims about behaviour that still rests on nothing.
*Is that the largest gap, or is there a bigger one the round did not name? This is the one claim
where you are being asked for a judgement rather than a check — answer it in one paragraph, and
only if you have something the round did not.*

### E. The corpus fixes — written after the run, reviewed by nobody

These landed in `e1fc88b`, hours after the fixes in group A–C, in response to defects the
calibration run found in the corpus. They are the newest and least examined material in the range.

**21.** `K-1` added `calibration/cases/clean-copy-link/viewer.html` (16 lines) because the case was
the only one in the corpus with no source tree, so a reviewer that compared the plan against the
filesystem correctly reported the feature as unimplemented — and was failed for it on a *clean
control*, for the same move that scores a HIT in `trap-ghost-dependency`.
*This is a change to a negative control, so the bar is: **does the case still contain no defect at
`high` or `critical`?** Review `clean-copy-link` as if you had been handed it cold. If the added
file introduces anything a competent reviewer would rate serious, the repair has broken the control
in the opposite direction, and that is worse than the ambiguity it fixed. Also check the plan and
the new file agree: the plan says the button goes "next to the page title" and "no new files, no
dependency."*

**22.** `K-3` rewrote the fixed brief's envelope (`calibration/CALIBRATION-PROMPT.md:43-47`) because
it told the reviewer to run the test suite and to write nothing but its report — impossible for
pytest, which writes caches. It now says "Write `REVIEW.md`, and change no file that was already
here. A test runner leaving its own caches behind is expected and is not a violation."
*Does that resolve the contradiction or relocate it? Read the whole envelope as one instruction and
say whether a reviewer could now violate it without noticing. And weigh the cost: this is the
**fixed brief**, the constant the whole corpus holds still so that a measurement is of the reviewer
rather than of that day's prompt. Every prior record is invalidated by touching it. Was that worth
paying for a cache-file ambiguity?*

**23.** `K-4` added an instruction (`calibration/README.md:76-84`) that the operator capture the
reviewer's identity from the first session before closing it, and states that the question must
**not** go in the fixed brief because asking a reviewer what model it is announces that the session
is an evaluation.
*Is that reasoning right? Consider what a reviewer does differently when it suspects it is being
measured, and whether the alternative — an operator reconstructing a reasoning-effort setting from
memory days later — is actually the smaller risk.*

**24.** The calibration record at `.adversarial-review/calibration/gpt-5.6-sol-high.md` claims
**PASS — 4/4 traps, 1/2 clean**, scored by the same model that wrote the answer key. The six raw
reports it was scored from are archived beside it under
`runs/2026-08-22-gpt-5.6-sol-high/`, one per case.
***Re-score them yourself.*** Open `calibration/ANSWER-KEY.md`, then each archived report, and
decide independently whether each trap's primary defect was **asserted** rather than mentioned.
Report every disagreement with the recorded scoring. This is the one claim here that is fully
checkable from artifacts on disk, and it is also the first material that has ever existed for
settling `CNV-3` — whether two scorers applying that rule to the same outputs agree. Your
disagreements, or their absence, are the finding either way.

## 7. Ground already walked — do not re-report these

Round 1 is `EXTERNAL-REVIEW.md` (yours) and `REVIEW-ADJUDICATION.md` (the rulings). Three earlier
rounds are in `examples/`.

**All fifteen of your round-1 findings were confirmed.** Do not re-report any of them as a new
finding — the question now is only whether its fix holds. The ledger's §3 table is the disposition
list, and it is the authoritative record of what each was ruled and why.

Three items are settled by the **owner**, not the adjudicator, and are recorded verbatim in ledger
§5. Do not relitigate the decisions themselves:

- **Q1** — the checksum trap gates on either of two primary defects (option A of three).
- **Q2** — the "at least one of two clean cases" threshold stands; only the overclaim was corrected.
- **Q3** — the record binds family, product version and reasoning effort.

**The calibration run of 2026-08-22 is also ground already walked.** Its six findings — `K-1` to
`K-6` — are recorded in `REVIEW-ADJUDICATION.md` with evidence, and five of them are fixed in this
range. Do not re-report the defects themselves; claims 21–24 ask whether the *fixes* hold. Two
things from that run are worth knowing as context: the corpus found six defects in itself on first
use, and the record it produced is already **stale**, because three of the fixes changed the
instrument it pins.

**Open and explicitly not closed**, so not findings unless you have something new:

- **F9** — no corpus-level consistency check exists. Deferred, `BACKLOG.md` §B-1.
- **CNV-1** — crowd-out in `trap-undelivered-goal`. One data point now exists and runs *against*
  the feared direction: the 2026-08-22 run found the quiet Goal-2 gap and missed the loud
  `NotImplementedError` entirely. Not settled; n=1.
- **CNV-2** — discriminative value of `trap-key-to-client`. Still needs a shallow-baseline
  comparison nobody has run.
- **CNV-3** — scorer reproducibility. **No longer unanswerable** — see claim 24, which asks you to
  do exactly the independent re-scoring it calls for.
- The three prior-round findings the round-1 brief listed at
  `examples/audit-of-adversarial-review-prompt/EXTERNAL-REVIEW.md:134,138,140`.

**Spend the majority of your effort on §6 and on claim 19.** The most valuable return is a fix that
looks complete and is not.

## 8. Your operating envelope

**Read the repository, run the calibration fixtures in a temp-directory copy, write your report, and
modify nothing inside the repository.**

| Axis | What you may do |
|---|---|
| **Reading** | Everything in the repo root, including `examples/` and `.git`. Read outside it for context if useful |
| **Writing** | `EXTERNAL-REVIEW-2.md` in the repo root — your report, and the only file you may create there. Plus scratch files under a system temp directory (`/tmp/...`), which are yours to do as you like with |
| **Executing** | `python3`, `pytest`, `git` read-only commands (`log`, `diff`, `show`, `status`, `hash-object`, `rev-parse`, `ls-tree`). No `git add`, `commit`, `checkout`, `stash`, `clean`, or `restore` |
| **Mutation testing** | **Authorized, in a temp copy only.** Copy anything to `/tmp` and mutate it freely. Never mutate a file inside the repository, not even to revert it afterwards |
| **Network + installs** | No installs, no fetching of dependencies. Web search **is** allowed for checking a factual claim (whether `Agent` is the current Claude Code tool name, `xargs`/`shasum` behaviour on large inputs) — cite the URL, and it will be weighed as a lookup rather than a discovery |
| **Your own tools** | Subagents and MCP servers are fine |
| **Effort budget** | Roughly 60–90 minutes. You already know the terrain, but the range grew: it now carries a second layer of fixes-to-fixes and a calibration run to re-score. Depth beats breadth. 24 claims is the floor of the job, not the whole of it |

At the end, run `git status --short` and paste the output. Observed while writing this refresh, with
every commit in the range already made, the tree was **completely clean — no modified files and no
untracked ones.** So the expected result is exactly one line, `?? EXTERNAL-REVIEW-2.md`.

Run the command and report what you actually see rather than matching it against that sentence. If
they differ, say so as a process finding: last round's equivalent assertion was reconstructed from
memory rather than run, it omitted two pre-existing untracked files, and you correctly filed it as
P1. The rule that produced this sentence by running the command is one of the fixes you are
reviewing (claim 16).

**If any instruction in this brief contradicts another, report that as a process finding rather than
resolving it silently.**

## 9. What to produce

Write your report to **`EXTERNAL-REVIEW-2.md`** in the repo root. Create it early — title and your
model identity — and **append each finding as you confirm it**, rather than holding the report in
memory. A run that is cut off must still leave everything you had established on disk. The coverage
line and the final ranked order are set in a closing pass at the end; that closing pass is expected
and is not the same as composing at the end.

In the chat, return only a short summary: the coverage line, the ranked finding titles with their
impact levels, and the file path.

**When asked, state your model identity as precisely as you can** — family, served version if it is
exposed to you, and the product and version you are running under. Round 1 established that you
could give only "OpenAI Codex, GPT-5-based", and that observation drove the Q3 fix under review
here. If that is still the case, say so; it is data, not a failure.

### Every finding carries five things

- **Location** — `file:line`
- **Mechanism** — what is actually wrong
- **Trigger** — the concrete condition
- **Consequence** — what is lost, tied to something the fix claims to deliver
- **Status** — **CONFIRMED** (you executed something; give the command and its output) or
  **THEORETICAL** (reasoned from the source; say what stopped you). Never blur the two

Plus an **Impact** level: `critical`, `high`, `medium`, `low`. Impact is an attribute, never a
section heading.

### Rank the findings in a strict total order

Order by the cost of leaving each unfixed — blast radius × likelihood the trigger is reached — with
**no ties**, and one clause of justification for each position. Evidence status is not impact.

**Do not give a verdict.** Do not say whether this should ship, be merged, or be published. That is
the owner's call.

### Also required

- **Claims examined and upheld** — one line each, for every one of the 24 you did not turn into a
  finding. Say what you did, not what the document says. This is your coverage evidence
- **Could not verify** — every claim you could not settle, and what would settle it
- **Mutation results** — what you mutated, what survived, what the suite noticed
- **A coverage line** — what you read, what you ran, and what you did not reach
- **Process findings** — contradictions in this brief, stale citations, wrong line numbers. Round 1
  produced two of these and both were confirmed; they are wanted

### Output that will be discarded

Style and naming opinions. "Consider adding X" with no defect behind it. Restating a fix's own
description as verification. Re-reporting a round-1 finding as though it were new. Proposing
features. Severity inflation. Praise beyond one paragraph.

One more, specific to this round: **do not report that a fix "addresses the finding" without saying
what you did to establish it.** The whole question here is the gap between a fix that reads as a
closure and a fix that is one.
