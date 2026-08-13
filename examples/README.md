# Worked examples — the skills used on themselves

Everything in this folder is real output. Nothing is illustrative, reconstructed, or written to
look good. Two different AI models were sent to attack these skills, both found genuine defects,
and the defects were adjudicated and fixed using the very skill under review.

**Only two things were changed:** absolute file paths (`/Users/<name>/…` → `~/…`) and the name of
one private project the reviewers used as a test corpus (→ `corpus-project`). Findings, evidence,
commands, outputs, rulings and owner decisions are untouched.

---

## `audit-of-adversarial-review-prompt/` — Codex attacks the brief-writer

Target: the prompt template that tells an external reviewer how to behave. Reviewer: OpenAI Codex
(GPT-5), read-only, web search allowed.

| Read in this order | What it is |
|---|---|
| `EXTERNAL-REVIEW-PROMPT.md` | The brief. 484 lines aimed at a model that didn't write the template. |
| `EXTERNAL-REVIEW.md` | Codex's report. 24/24 load-bearing claims engaged, 10 findings ranked with no ties, plus a section titled *"What this document assumes about you that is wrong."* |
| `PATCH-VERIFICATION-PROMPT.md` | A second, narrower brief: *the fixes are claimed — check them.* |
| `PATCH-VERIFICATION-REVIEW.md` | The verdict: 8 of 10 amendments implemented, **2 diverged**. Both were then actually fixed. |

The thing to notice is the last step. "I applied the fixes" is a claim by the party under review
like any other, and re-verifying it caught two that hadn't landed.

**Findings worth reading:** #1 (the framing made a zero-finding audit noncompliant — i.e. it was
pressuring the reviewer to invent findings), #3 (treating every surviving mutation as a finding
manufactures false positives), #10 (an "authorized" command can still mutate the repo).

---

## `audit-of-review-adjudication/` — two rounds against the judge

Target: the skill that rules on returned reviews. Round 1 reviewer: Claude Fable 5. Round 2
reviewer: OpenAI Codex (GPT-5).

| Read in this order | What it is |
|---|---|
| `EXTERNAL-REVIEW-PROMPT.md` | Round 1 brief. Demands *retrodiction*: apply the skill's rules to three real ledgers and check whether they produce what actually happened. |
| `EXTERNAL-REVIEW-COVER-NOTE.md` | The short message that was pasted into the reviewer's chat box. This is what a cover note looks like. |
| `EXTERNAL-REVIEW-FABLE.md` | Fable's report. 14 findings, 2 defects **in the brief itself**, 5 could-not-verify items — and one self-finding it retracted mid-report, publishing the commands that refuted it. |
| `REVIEW-ADJUDICATION.md` | **The centrepiece.** The skill's first real run, applied to itself. 14 in, 14 out, both rounds. |
| `EXTERNAL-REVIEW-2-PROMPT.md` / `-COVER-NOTE.md` / `EXTERNAL-REVIEW-2.md` | Round 2: a different model audits the round-1 amendments. 8 more findings, two of them amendments that contradicted rules elsewhere in the skill. |

### Why the ledger is the interesting document

Open `REVIEW-ADJUDICATION.md` and look for these:

- **Two findings that fired live, inside the ledger diagnosing them.** Finding 1 said the
  verdict/disposition vocabulary was incomplete; row 7 of that same ledger then needed a
  compound label the vocabulary didn't have. Finding 4 said the count invariant was
  self-contradictory; the header had to record a deviation from it. Both are logged as `P-3` and
  `P-4`.
- **An independence discount, applied against the ledger's own interest.** Four of the fourteen
  findings matched suspicions the author had leaked into the brief. Reviewer agreement with a
  planted suspicion is an echo, not corroboration — so those four were re-established from
  primary sources alone, as if the reviewer had said nothing. All four survived.
- **Two questions the adjudicator refused to answer** (§4), each with options, costs and a
  recommendation that is explicitly *not* a ruling. One asked whether to change a declared
  one-way door; the other whether a rule that contradicted three-for-three real practice should
  bend or hold.
- **Pre-registered expectations** in §2 — the expected outcome written *beside each command
  before running it*, so a surprise surfaces mechanically instead of by recall.
- **Round 2 appended, never editing round 1.** Superseded rulings get new rows that cite the rows
  they supersede. The record of having been wrong stays in the file.

---

## What these examples are not

They are not a template to copy. The skills generate briefs and ledgers sized to the target;
these particular ones are long because the targets were dense prose documents where every
sentence is load-bearing. A brief for a 400-line module is considerably shorter.

They are also not a claim that the skills are now correct. Round 2 found eight things wrong with
round 1's fixes. That is the expected behaviour of the process, not a failure of it.
