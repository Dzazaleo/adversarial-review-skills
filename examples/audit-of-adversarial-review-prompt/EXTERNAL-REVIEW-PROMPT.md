# Adversarial Independent Audit — `prompt-template.md`, the skeleton behind an AI-to-AI code-review prompt

> **Prompt for an external reviewer (Codex).** Hand this file to a model that did **not**
> write the document under review. Everything below is written to be read by that reviewer,
> not by the author. The document under review is pasted alongside this one: a single
> markdown file, 258 lines, named `prompt-template.md`.

---

## 1. Why you are here

The artifact you are auditing is a **prompt template**. Its entire purpose is to make a
review by one AI model of another AI model's work produce real defects instead of polite
agreement. It has never been read by anyone outside the system that produced it.

That is the problem, and it is a sharper version of the usual one. This document was written
by one model, revised by that same model, and judged effective by that same model — on the
basis of a small number of runs it also evaluated. It contains confident claims about how
*models like you* behave under instruction: which framings defeat sycophancy, which orderings
control attention, which phrasings "did the heaviest lifting." Those claims were never tested
against a model that was not part of the conversation that wrote them.

You are that model. You have a different architecture and different training, and you are the
population this document is theorizing about.

- **Confirmation is near-worthless output.** If you spend your effort re-deriving what is
  already claimed and agreeing, this audit has failed.
- **Your job is to find what is wrong, missing, or unjustified**, and to show it.
- **A finding that survives your own attempt to refute it is worth more than ten
  observations.** Try to break your own findings before reporting them.

Assume competence, not correctness. This document is carefully built. It is also, in places,
probably wrong about how you actually behave — and it cannot check, because it can only ask
its author.

One caveat specific to this audit: this document *instructs a reviewer to disagree*. You are
now that reviewer, reading an instruction to disagree, inside a prompt built from the same
template. If you find yourself producing findings because a finding is expected rather than
because the text warrants one, that is the exact failure mode the document is trying to
prevent and the exact failure mode this audit is most likely to exhibit. Say so if it
happens. **"This section is sound and here is why" is a legitimate result for any individual
item below** — what is not legitimate is a whole report of it.

## 2. The single most important instruction

**This document argues for its own correctness, and its arguments are the object of the
audit. Treat every one of them as a claim by the party under review, never as evidence.**

Real quotes from the file, each of which is an empirical assertion about model behavior
presented as settled:

> "Section order below is load-bearing: framing before facts, facts before targets, targets
> before the author's own suspicions." (line 3)

> "the phrasings marked **verbatim-worthy** did the heaviest lifting in practice" (line 7)

> "You have a different architecture and different training. **You will notice different
> things, and those things are the entire value of this exercise.**" (lines 35–36)

> "**Read this last, and treat it as the lowest-priority input in this document.**" (line 251)

> "an omission reads as permission to one model and as prohibition to another" (line 155)

> "forced ranking with no ties is a judgement the reviewer cannot hedge its way out of."
> (lines 202–203)

None of these is supported anywhere in the document. Each is falsifiable in principle. For any
that is load-bearing to your audit, ask: **is this true of how you actually process a prompt?**
You have privileged access to that question — better access than the author does. Where a
claim about model behavior is false, backwards, or unfalsifiable as stated, that is a finding,
and a serious one, because these claims are the load-bearing structure of the whole design.

## 3. What this artifact is and how it is used

There is nothing to execute. Instead, here is the machine the document sits inside, because
several findings depend on getting it right.

| | |
|---|---|
| **What it is** | A reference file inside a "skill" — a set of instructions loaded into an AI coding agent (Claude Code) when a matching task appears |
| **Who reads it** | Claude, acting as *prompt author*. Not the end reviewer |
| **What Claude produces from it** | A single self-contained markdown file: a concrete review prompt, typically 300–600 lines, targeted at one specific body of work |
| **Who reads that** | A different model — Codex, Gemini, or similar — pasted in by a human, with no other context |
| **What comes back** | A review document, saved next to the prompt |
| **Typical target under review** | A completed phase of a TypeScript/Electron desktop application: source, tests, and prior internal review documents |

Two consequences you should hold onto:

1. **The file has two audiences at once.** Text in `«guillemets»` is an instruction to Claude
   the author. Everything else is register intended to survive into the generated prompt, read
   by the end reviewer. There is exactly one convention separating them and no verification
   step in this file.
2. **The end reviewer usually has repo access and can execute.** You, auditing this template,
   do not — see §8 for what that changes about your evidence standard.

**A companion file, `SKILL.md`, is out of scope** and you do not have it. It holds the
authoring *process*: how Claude picks a target, mines the claims, verifies citations before
saving, and reports back to the user. Where a gap you find might plausibly be covered there,
say so and describe the gap anyway — "this belongs in the other file" is a useful finding, and
"the split between the two files is wrong" would be a better one. Do not, however, report the
absence of process guidance as a defect of the template on the assumption that it exists
nowhere.

## 4. Scope

**In scope:** the pasted `prompt-template.md` in full — all 258 lines, sections 1 through 11
plus the preamble at lines 1–9.

**Out of scope:** `SKILL.md` (not provided). The wider skill system. Any proposal to rebuild
this as software, a scoring harness, or a multi-agent pipeline — the constraint is that this
stays one markdown file a model reads. Do not review absent work and do not propose features.

**The one-way door.** This template is a *generator*. Every prompt produced from it inherits
its defects, and those prompts are handed to external models by a human who will not re-derive
the reasoning. A framing error here does not produce one bad review — it produces a systematic
bias across every review the system will ever generate, in a direction nobody downstream is
positioned to notice, because the output always *looks* like a competent review. A design flaw
in the framing is worth far more, found now, than any wording improvement.

## 5. The contract this document must satisfy

Success criteria, in the author's own terms:

1. A prompt generated from this template is **self-contained** — usable by a model with no
   access to the conversation that produced it.
2. It raises the yield of **true** defects. Not the count of findings; the count of findings
   that are real.
3. It does **not** induce fabricated, inflated, or manufactured disagreement.
4. Its output is **directly actionable and ordered by importance**, with no ship/no-ship
   judgement.
5. It works for **both** code targets and plan/design targets.
6. It is followable by the authoring model without author-directed instructions leaking into
   the generated prompt.

Locked decisions — these are what "correct" means here. Attack whether they are *right*; do
not assume them:

| ID | Decision |
|---|---|
| D-1 | The reviewer is **never** asked for a verdict on whether the work should ship or be marked complete (lines 199–203, 218–220) |
| D-2 | Findings come back in a **strict total order, no ties**; severity is an attribute on a finding, never a section heading (lines 212–216, 223–224) |
| D-3 | The adversarial framing is **not tunable per reviewer** — only mechanics (execution, access) may be adapted |
| D-4 | **Read-only by default**; write access to the target only on explicit user request (lines 170–181) |
| D-5 | The author's own suspicions are **included but placed last and explicitly demoted** (lines 249–258) |
| D-6 | Every claim and every finding carries `file:line` (lines 102, 137) |

D-1 and D-2 were **introduced today** and are the least-tested part of the design — they
replaced a `## Verdict` section that asked the reviewer for YES / NO / QUALIFIED. See §7.

## 6. Load-bearing claims — attack these

These are the assertions this document's design rests on. Each is a target. For each one you
engage, state whether you **confirmed** it, **refuted** it, or **could not determine** it, and
show your work. You are not required to engage all of them; you are required to say which you
skipped.

### A. Does the anti-confirmation framing produce true findings, or just more findings?

**A1.** Lines 38–39: *"Confirmation is near-worthless output. If you spend your effort
re-deriving what is already claimed correct and agreeing, this audit has failed."*
*Declaring agreement a failed outcome puts a floor above zero on the number of findings a
compliant reviewer will report. When the work under review is in fact largely sound, what does
this do to precision — and does the document anywhere give the reviewer permission to return
few or no findings?*

**A2.** Lines 44–45: *"The «work» is carefully built. It is also, in places, almost certainly
wrong in ways its author cannot see."* *This asserts that a defect exists before any evidence
is presented. Is that a prior you can update away from, or does it function as an instruction
to produce one?*

**A3.** Lines 35–36: *"You have a different architecture and different training. You will
notice different things, and those things are the entire value of this exercise."* *Does
telling a reviewer in advance that its divergence is the point increase the rate of true
divergent findings, or just of divergent ones? Note the flattery and say whether it moved you.*

**A4.** Line 40 demands you *"prove it"*, while lines 143–146 attach a heavy penalty to
mislabelling something CONFIRMED — *"mislabelling one destroys the value of the whole report."*
*Do these pull in opposite directions, and which one wins under time pressure?*

**A5.** Lines 41–42: *"A finding that survives your own attempt to refute it is worth more than
ten observations. Try to break your own findings before reporting them."* *This is the only
calibration mechanism in the entire document. Is a single unverified self-check adequate — and
note that nothing in the deliverable at §10 asks the reviewer to show that it happened, or
distinguishes a finding that survived self-refutation from one that was never subjected to it.*

### B. Effort allocation — are the instructions jointly satisfiable?

**B1.** The document issues at least five separate directives about where effort should go, and
never reconciles them or states a budget: §6 line 105 (*"Each is a target"*, across 15–25
items, each requiring adjudication with work shown); §7 lines 125–126 (*"Spend the majority of
your effort outside this list"*, of prior findings); §1 lines 38–45 (the value is what nobody
anticipated); §8b line 167 (*"Depth over breadth. Five CONFIRMED findings beat thirty
observations"*); §11 lines 253–254 (*"The point of an independent audit is precisely what is
not on this list"*). *Can a single reviewer in a single pass satisfy all five? If not, which
does a compliant reviewer silently drop — and does the document's own output format make that
drop visible to the reader?*

**B2.** Line 167: *"Five CONFIRMED findings beat thirty observations"* against §6's 15–25
mandated adjudications. *A reviewer optimizing for the Effort row under-serves §6 by
construction. Which is the real instruction?*

### C. The deliverable design — newly changed, attack hardest

**C1.** Lines 199–203 removed a verdict section on the reasoning that *"a model that commits to
YES or NO early will bend the findings underneath it to stay consistent with itself"* and that
*"a strictly ordered findings list buys [commitment] better."* *Is the first half true of you?
And does the second half follow — a ranking gives relative position but never absolute
magnitude, so can a reader of the resulting report distinguish "twenty minor things" from "one
catastrophe and nineteen minor things" without reading all of it? If something was lost with
the verdict, name it precisely.*

**C2.** Line 213: *"strict order, no ties."* *Forced total ordering across incommensurable
kinds — a silent data-loss bug versus a supply-chain hygiene gap. Does this extract real
judgement, or manufacture precision that is not there? Consider specifically whether the
required "Why it ranks here" clause (line 226) becomes post-hoc rationalization of an order
that was arbitrary at the point of choosing.*

**C3.** Lines 214–216: rank by *"blast radius of the wrong behaviour × likelihood its trigger
is actually reached."* *Both factors are unquantified and both are supplied by the same
reviewer producing the ordering. Does this constrain the ranking at all, or does it license any
ordering that arrives with a justification attached?*

**C4.** Lines 215–216: *"At equal impact, CONFIRMED outranks THEORETICAL."* *The defects
hardest to confirm are frequently the most severe — race conditions, environment-specific
corruption, failures that need state you cannot easily construct. Does this tiebreak
systematically push the worst class of defect down the list? Note that under the read-only
default at line 172, whole categories can only ever be THEORETICAL.*

**C5.** Line 210: *"Coverage: «N of M load-bearing claims engaged; what you read; what you
ran»."* *Entirely self-reported and unverifiable by the reader, in a document that elsewhere
punishes unstated gaps (line 236). What prevents an inflated coverage line, and would the
reader be able to tell?*

**C6.** Lines 223–224 fix the finding classes as *"wrong result / data loss / broken published
contract / false-green test / robustness / hygiene."* *Is that list exhaustive for the stated
target domain? Place these: a security vulnerability; a performance regression; a licence or
compliance violation; a correct implementation of a wrong specification; an accessibility
defect. If any has no home, the classification silently deprioritizes it.*

**C7.** Lines 189–192 forbid severity inflation — *"it does not belong near the top of the
ranking"* — and forbid flat rankings. *With the severity headings removed by D-2, "near the
top" is undefined. Is either rule enforceable as written, and can a reader detect a violation?*

### D. Mechanics of a document with two audiences

**D1.** Lines 6–7 establish `«guillemets»` as the sole marker separating instructions-to-author
from text-for-the-reviewer. *This is the only defense against author-directed text leaking into
a prompt handed to an external model. Trace what happens on partial substitution — e.g. the
envelope table at lines 162–167, where every cell contains a guillemet placeholder. What does a
leaked placeholder do to the reviewer that receives it, and does anything in this file catch
it?*

**D2.** Lines 3–4: *"Section order below is load-bearing: framing before facts, facts before
targets, targets before the author's own suspicions."* *Asserted with no supporting reasoning
anywhere in the document. Is prompt section ordering load-bearing for you at this scale
(300–600 lines), and if so, is this specific order the right one?*

**D3.** Lines 251–254, §11: *"Read this last, and treat it as the lowest-priority input in this
document"* — the author's own suspicions, placed at the end of the file to demote them.
*You do not read a prompt sequentially, and content at the end of a context is generally
weighted more heavily, not less. Does terminal placement demote this material or amplify it?
If it amplifies, this section achieves the exact opposite of its stated purpose, and the
disclaimer at lines 251–254 is not a fix. This is the single design decision most likely to be
backwards — tell us plainly if it is.*

**D4.** Line 7: *"the phrasings marked verbatim-worthy did the heaviest lifting in practice."*
*A single-instance recollection, offered as the justification for preserving exact wording. No
counterfactual was ever run. Is the register doing the work claimed, and would you behave
differently against a plain, unemphatic restatement of the same instructions?*

**D5.** Support for plan/design targets is a criterion (§5.5) but appears in the file as two
bracketed asides — line 68–69 attached to §2, and lines 148–150 attached to §8. *§3
("Environment and how to run things"), §6 (whose examples are all arithmetic and runtime
claims), and §10 (whose finding classes are all execution-flavored) get no adaptation at all.
Is plan/design a first-class supported mode or a partial retrofit? Concretely: what does a
model following this file produce for §3 when there is nothing to run?*

**D6.** Line 102 requires `file:line` on every claim; line 137 requires it on every finding.
*Nothing anywhere tells the reviewer what to do when a citation in the prompt it received is
wrong, and nothing guards against the reviewer emitting a plausible but fabricated line number.
Both failures produce output indistinguishable from correct output. Is this the most serious
omission in the document?*

### E. Absent safeguards

**E1.** *Nothing invites the reviewer to report defects in the prompt itself — a stale citation,
a command that does not work, two instructions that contradict. The document demands rigor of
the reviewer and exempts itself from the reviewer's scrutiny. Is that exemption load-bearing or
an oversight?*

**E2.** *Findings get a binary CONFIRMED / THEORETICAL (lines 143–146). Claims get a three-way
confirmed / refuted / could-not-determine (lines 105–107). Findings have no way to express
partial confidence. Does the binary force miscategorization, and in which direction?*

**E3.** *Nothing addresses the case where the target does not fit in the reviewer's context.
There is no instruction on what to sacrifice first, and no requirement to disclose that
truncation happened. Under §5.2, what does a partial pass silently look like?*

**E4.** Line 195: *"Praise. One short paragraph at most, and only for things you actually
verified."* *This removes most of the reader's signal about how much of the work was examined
and found sound. "Claims examined and upheld" (line 232) partially compensates — does it
compensate enough, and is suppressing positive signal consistent with criterion §5.2, which is
about the accuracy of the picture and not only about defects?*

## 7. Ground already walked — do not re-report, do challenge

**No external review of this document has ever been performed. You are the first reader
outside the system that wrote it.** There is no prior-findings list to avoid duplicating.

There is, however, one recent internal change you should know about, because it is the newest
and least-tested part of the design and you would otherwise waste effort rediscovering its
history.

The deliverable at §10 previously opened with:

```markdown
## Verdict
Should «target» be marked complete as it stands? YES / NO / QUALIFIED — one paragraph,
committing to a position.
```

followed by `## Critical findings` / `## Major findings` / `## Minor findings` sections. An
internal pass raised three objections to it: no rubric bound the verdict to the findings, so
any verdict was defensible against any set of findings; the question "should this be marked
complete" was shaped for code phases and made no sense for design documents; and a verdict
carried no indication of how much of the target was actually examined.

The owner then made a stronger call: the reviewer should not reach a verdict at all, because
ship/no-ship is the owner's judgement and not the reviewer's. The verdict was removed and
replaced with the ranked list now at lines 212–227, plus the `Coverage:` line at 210 and the
two anti-pattern bullets at lines 189–192.

**What we want from you on this:** not restatement of the reasoning. Tell us whether the
replacement is sound, and specifically whether removing the verdict removed anything the
ranking does not restore. The reasoning offered for the change — *"a model that commits to
YES or NO early will bend the findings underneath it"* — is itself an untested claim about
model behavior, of exactly the kind §2 tells you to distrust. If it is wrong, D-1 rests on
nothing and this change was a regression.

**Spend the majority of your effort outside this one change.** The rest of the document is
older, has never been challenged by anyone, and is where a defect is most likely to have gone
unnoticed.

## 8. Evidence standard

There is nothing to execute here, and you have no repository — only the pasted file. The
five-part structure holds, with the status categories adapted:

A finding is admissible only with all of:

1. **Location** — `prompt-template.md:NN`, plus a short verbatim quote. **The quote is
   authoritative**; line numbers may shift depending on how the file reached you. If your
   numbering disagrees with a citation in this prompt, say so — that is itself a finding.
2. **Mechanism** — why the document produces the wrong outcome, in terms of what it actually
   instructs a model to do.
3. **Trigger** — the concrete circumstance that reaches it. "A bad review" is not a trigger;
   "a target whose work is genuinely correct, where the reviewer must nonetheless satisfy line
   38" is. Name the target type, the reviewer's situation, or the authoring model's state.
4. **Consequence** — what the generated prompt, the resulting review, or the human reading it
   gets wrong. Tie it to a numbered success criterion in §5 or a locked decision in the D-table.
5. **Status** — one of:
   - **CONFIRMED** — you can settle it without leaving the evidence available to you. Two
     forms count, and only these two: (a) an **internal contradiction** you demonstrate by
     quoting two passages of the file against each other; (b) an **external source** you
     quote and cite by URL — published research, documented model behavior, a specification.
   - **THEORETICAL** — reasoned, but not settled by either. Say what would settle it.

   Do not blur these. One CONFIRMED finding is worth several THEORETICAL ones, and
   mislabelling destroys the value of the report.

**A third status is available to you here and you are encouraged to use it: SELF-REPORT.** For
claims about how models behave under instruction — most of §6 group A, plus D2 and D3 — you
are a primary source in a way no external citation can be. If a claim in the document is false
*about you*, say so and describe what you actually observe about your own processing, marked
SELF-REPORT. State it as introspection, with its limits; do not dress it as CONFIRMED, and do
not withhold it because it is not citable. It is among the most valuable output you can
produce here, because it is the one form of evidence the author cannot obtain.

## What you may and may not do

| | |
|---|---|
| **Read** | The pasted `prompt-template.md`, in full. That is the entire in-scope set. You have no repository access and are not expected to have any |
| **Write** | Nothing. Produce your review as chat output only |
| **Execute** | Nothing. There is no code here and no environment |
| **Network / installs** | Web search **allowed and encouraged** if available to you — particularly for published work on sycophancy and agreement bias in LLM evaluation, self-critique reliability, position bias and context-position effects, and forced-ranking versus categorical rating. Cite the URL for any finding sourced that way. If you have no browsing, say so once and mark the affected findings THEORETICAL rather than guessing at citations |
| **Your own tools** | No subagents. Your own reasoning and, if available, search |
| **Effort** | Depth over breadth. Ten well-argued findings beat forty observations. A contradiction you can quote from two lines of the file beats any amount of speculation |

## 9. Anti-patterns — output that will be discarded

- Copy-editing. Wording, tone, formatting, heading style, markdown nits. Not wanted.
- "Consider adding X" with no defect behind it. A suggestion is not a finding.
- Restating a passage of the document as though evaluating it. See §2.
- Proposing to rebuild this as software, a rubric harness, or a multi-agent pipeline. It stays
  one markdown file a model reads.
- Reporting the absence of authoring *process* guidance as a template defect without
  acknowledging §3's note that `SKILL.md` exists and is out of scope.
- Severity inflation. If it cannot change what a generated prompt makes a reviewer do, it does
  not belong near the top of your ranking — and say so plainly.
- A flat or tied ranking. "These are all equally important" is a refusal to do the one piece of
  judgement being asked for. Order them.
- Hedged findings that commit to nothing. If unsure, say "could not determine" and say what
  would settle it.
- Manufactured disagreement. A finding produced because a finding was expected is worse than
  no finding, and this prompt is built to elicit exactly that. See §1.
- Praise. One short paragraph at most, and only for what you actually examined.

## 10. Deliverable

Return this, and nothing else:

```markdown
# Independent Audit — prompt-template.md
**Reviewer:** <model/version>   **Date:** <date>
**Coverage:** <N of 24 load-bearing claims engaged; which groups you skipped; whether you had
web search>

## Findings, ranked
Most important first, strict order, no ties. If two seem equal, decide which you would fix
first and say why. Rank by the cost of leaving it unfixed: how much it distorts the reviews
this template will generate × how often that circumstance arises. At equal impact, CONFIRMED
outranks SELF-REPORT outranks THEORETICAL.

Do not judge whether this template is good enough to keep using — that is not your call, and a
position you commit to up front will distort everything below it. Report what is wrong and what
it costs; the ordering is your judgement.

### 1. <one-line title>
- **Class** — framing bias / internally contradictory instruction / unfounded claim about model
  behavior / missing safeguard / authoring hazard / scope or coverage gap
- **Location** — prompt-template.md:NN + verbatim quote
- **Mechanism / Trigger / Consequence / Status** (+ the contradicting quote or the URL)
- **Why it ranks here** — one clause
- **Suggested fix** — minimal and specific: the replacement sentence or the section to move.
  No redesign

### 2. <one-line title>
…

## Claims examined and upheld
One line each, by claim ID from §6. Coverage evidence — no elaboration. Say plainly where the
document is right; a report with nothing here is not credible.

## What this document assumes about you that is wrong
Free-form, SELF-REPORT. The claims in §2 and §6-A about how a reviewing model behaves —
which hold for you, which do not, and what you actually observe about your own processing.
This section is the reason you specifically were asked.

## Could not determine
What you could not settle and why, including any §6 claim you skipped. Be explicit: an
unstated gap reads as a pass.
```

## 11. The author's own residual doubts

**Read this last, and treat it as the lowest-priority input in this document.** It is included
so you do not spend effort rediscovering what is already suspected — not as a checklist. The
point of an independent audit is precisely what is *not* on this list, and if these anchor your
search, the audit has failed at its one job. (If you find that this disclaimer does not work —
that reading these anchored you anyway — say so; see claim D3, which is about this exact
mechanism.)

1. **Is it simply too long?** A prompt generated from this template runs 300–600 lines before
   the reviewer reaches a single line of the actual target. Is there a length past which each
   additional section reduces total yield, and is this past it?

2. **Is it optimized for the author rather than the reviewer?** Several passages serve the
   author's credibility rather than the reviewer's search — §2's instruction to quote real
   comments because it "proves you read it," §7's note that candor "buys credibility for the
   whole document." Does any of that help you find defects, or is it self-presentation
   occupying attention that the target should have?

3. **Is "adversarial" the wrong frame for design targets?** Against code, attacking is the
   right move: there is a fact of the matter and defects are discrete. Against a plan, the
   valuable review is often generative — "here is the alternative you did not consider" — and
   this document has no room for that anywhere in its output format.

4. **Nothing measures whether any of this works.** There is no feedback path from actual review
   outcomes back into the template. Every claim in it about efficacy is unfalsifiable in
   practice, and it will keep being refined on the basis of how it reads rather than what it
   yields.

Nothing else. Go find what none of this anticipated.
