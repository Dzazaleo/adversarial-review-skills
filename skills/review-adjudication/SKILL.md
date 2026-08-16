---
name: review-adjudication
description: "Adjudicate an external or cross-model review that has come back — decide which findings are real, re-verify them, and record a durable disposition for every one. Use when a Codex/Gemini/GPT/Cursor review report has landed — NN-EXTERNAL-REVIEW.md, NN-EXTERNAL-CODE-REVIEW.md, or any *EXTERNAL* report family — and the user asks what to act on, what is worth fixing, whether the reviewer is right, to triage or sort or work through the findings, or to close out a review. Also use when a review's findings need re-checking before a phase closes. Produces a NN-REVIEW-ADJUDICATION.md ledger with one row per finding — never a ship/no-ship verdict, and never a fix applied on its own initiative."
argument-hint: "<review file | phase N> [--round N]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

<objective>
A review has come back. Your job is to rule on every finding in it and write those rulings to a
durable ledger — `<phase-dir>/NN-REVIEW-ADJUDICATION.md` — so that each finding leaves with a
recorded verdict, a recorded disposition, and evidence behind both.

You are **not** fixing anything in this skill. The deliverable is the ledger plus a hand-off that
names what the owner must decide and what is queued for execution. Fixes are a separate, explicit
act afterwards, and the ledger is what they are executed against.

You are also **not** deciding whether the work ships. That is the owner's call. The sibling skill
`adversarial-review-prompt` refuses to let the reviewer issue a verdict for exactly this reason;
the refusal does not lapse because the reader is now Claude.
</objective>

<why_this_is_hard>
The naive framing of this task — "decide what's worth implementing" — is the failure mode, not the
goal. Three forces push toward wrongly disposing of real findings, and every rule below exists to
resist one of them.

1. **You are usually mid-phase and want the phase closed.** Dismissal is the cheapest path to that,
   and it wears good clothes: "pre-existing", "out of scope", "scaffold only", "will handle later."
   A finding you just found and immediately deferred is the tell. Deferral is a legitimate outcome
   *only* when it costs something — a durable backlog artifact that exists on disk before the
   ledger is written.

2. **Rejection is held to a lower evidence standard than accusation.** The review brief made the
   reviewer produce Location · Mechanism · Trigger · Consequence · Status for every finding. A
   refutation typically arrives as a paragraph of reading. That asymmetry is where false REFUTEDs
   come from. **The refutation carries the same burden as the finding.** For any claim about
   runtime behaviour, a static read plus a reassuring code comment is not evidence — the comment is
   the party under review talking. Reconstruct and run the actual path.

3. **Self-review re-enters through the back door.** If you wrote the code, your refutation of a
   finding about that code is self-review again, and it carries the same blind spots that produced
   the defect. High-impact refutations of your own work need execution evidence or an independent
   check — never confident prose.

There is a fourth, quieter force running the other way: a reviewer with no access to your settled
decisions will reopen arguments you finished months ago, and implementing those is real damage —
churn, complexity, sometimes a reversal of a deliberate choice. Screening for that is legitimate and
is step 3. But it is a channel that dismissal will try to use, so it is gated: a "settled already"
ruling requires the citation, and a finding that brings **new evidence** the settled decision never
considered is not settled — it is reopened, and it goes to the owner.
</why_this_is_hard>

<process>

## 1. Fix the inputs

From `$ARGUMENTS`, resolve:

- **The report** — the reviewer's own file. Never resolve by a single naming pattern: glob the
  target directory for `*EXTERNAL*` report families (excluding `*PROMPT*`, `*COVER-NOTE*`,
  `*ADJUDICATION*`, `*RESPONSE*`) — real corpora hold several (`NN-EXTERNAL-REVIEW.md`,
  `NN-EXTERNAL-CODE-REVIEW.md`, `NN-EXTERNAL-AUDIT-<reviewer>.md`). The ledger header must name
  every report file found and say which are and are not adjudicated in this ledger. If the user
  has only a chat transcript, write it to disk first; an adjudication of something not on disk
  cannot be re-read later.
- **The brief it answers** — `NN-EXTERNAL-REVIEW-PROMPT.md`. You need its scope, its declared
  envelope, and its load-bearing claims list, because coverage against that list is part of what
  you are ruling on. If no brief exists — a pasted chat review, a report from another tool — the
  evidence standard is this skill's own, in both directions: Location · Mechanism · Trigger ·
  Consequence · Status.
- **The round.** If a ledger already exists at the target path, check whether its last round is
  *closed*. Closed is defined over obligations, not cell presence: every numbered row AND every
  auxiliary entry (process, CNV, prior-review disagreement) carries both a verdict and a
  disposition, no `PENDING OWNER` remains unresolved, no blocking `VERIFY` remains open, and every
  executed `FIX NOW` row has been backfilled with its execution reference. A closed round is
  history: append `# Round N`, never edit it — a superseded ruling gets a new row that says so. A
  round not yet closed — an interrupted skeleton, an unexecuted queue, an unanswered owner
  question — is the current round: fill it in place, and state/evidence backfill (owner answers,
  execution references) is not only legal but required until closure.
- **Multiple reviewers.** Adjudicate them into one ledger. Where two reviewers disagree about the
  same code, that disagreement is signal: neither is presumed right, and the item is re-verified
  before either is ruled on.

Read the report in full before anything else. Do not start ruling from its summary.

## 2. Enumerate first, judge nothing yet

Extract every finding into the ledger skeleton **before adjudicating any of them**, each with its
ID, its title verbatim, and its reviewer-assigned impact. Then write the skeleton to disk.

This ordering is the guard against the most common real-world drift: the easy findings get fixed,
the hard ones get forgotten, and the ledger records only what was convenient. Rows exist first;
verdicts fill in.

Enumerate these too — they are findings, and each gets a ruled entry in its own ledger block
(they are counted separately from the numbered-finding rows; see below). Every auxiliary entry
gets a stable ID (`P-1`, `CNV-1`, `D-1`, …) and the same two axes as a table row — a verdict and
a disposition (`VERIFY` is the usual pairing for an open CNV gap). The no-empty-cells closure
check covers these entries, not just the table:

- The reviewer's **could-not-verify** list. That list is the reviewer being honest about a gap.
  Dropping it re-hides the gap and it reads downstream as a pass.
- Any **process or prompt defect** the reviewer reported (the brief invites these). These get ruled
  on in their own block, because their fix lands in the brief or the skill, not the code.
- Any **disagreement with a prior internal review** the reviewer raised.

**Count in = count out — over the report's *numbered* findings.** One table row per numbered
finding; the auxiliary categories are ruled in their own blocks and counted separately in the
header ("Findings in: N · Rows out: N · +K process, +M CNV, +D prior-review disagreements
ruled"). Two findings may be merged only with a row that says which IDs merged and why — then the
header says so too. A finding with no row is the defect this whole skill exists to prevent.

## 3. Screen against settled ground — cheap, and gated

Before spending execution effort, check each finding against what the project has already decided:

- `CLAUDE.md` "do not relitigate" facts and any equivalent locked-facts block
- Locked decisions (`D-NN`) in the phase's PLAN/CONTEXT, and the ROADMAP's constraints
- Prior review ledgers and prior dispositions — the ground the brief's §7 already covered
- Explicit non-goals, deferred-by-decision items, and archived debates

An external reviewer cannot see any of this, so relitigation is expected and is not the reviewer's
error. Three rules keep the check honest:

1. A **SETTLED ALREADY** verdict requires the citation — file and line of the decision, quoted.
   Without it the verdict is unavailable to you.
2. If the finding presents **evidence the settled decision did not consider**, it is not settled. It
   is a reopened decision, its verdict is `OWNER RULING REQUIRED`, and it goes in the hand-off.
3. "Out of scope" is a statement about *this phase's* work, never about whether the defect is real.
   A real defect outside scope is `CONFIRMED` with disposition `FIX LATER`, which means step 6's
   backlog obligation applies. It is not `NO ACTION`.

## 4. Split by class

Sort every remaining finding into exactly one:

- **Machine-checkable** — its truth can be settled by running something: a test, a script, a
  reconstructed call, a mutation, a diff. → step 5, then rule.
- **Owner judgement** — it turns on what the product should do, what risk is acceptable, what to
  spend effort on, or a trade-off between two defensible designs. → do not rule. Reframe it as a
  single decidable question with the options and their consequences, and hand it up. Verdict
  `OWNER RULING REQUIRED`.
- **Process/prompt** — about the brief, the envelope, the review method itself. → its own block.

The split is the discipline. A machine-checkable finding you resolve by reasoning is an unforced
error; an owner-judgement finding you resolve yourself is you taking a call that is not yours.

## 5. Re-verify — symmetric standard, running pipeline

For every machine-checkable finding, produce evidence at the same standard the brief demanded of
the reviewer, whichever way it comes out:

- **Reconstruct the real path.** Call it the way production calls it, with production's defaults and
  the deduped real population — not a hand-built fixture that happens to be convenient. Measuring
  the internal metric instead of the user-visible one has repeatedly produced a wrong ruling here.
- **Run it, and record the command and its output.** Both in the ledger. A verdict whose evidence
  cannot be re-run by a later reader is not evidence.
- **Check the reviewer's numbers where it gave any.** Say whether they reproduced. A reviewer whose
  figures reproduce exactly has earned weight on its unverifiable claims; one whose figures drift
  has not.
- **Discount non-independent agreement.** Where a brief claim was the author's own suspicion — a
  residual doubt leaked into the brief — the reviewer agreeing with it is an echo, not
  confirmation. Verify those findings from primary sources as if the reviewer had said nothing.
  **Do not take the hand-off's word for it that a doubt was kept out of the brief.** Before you
  count the reviewer agreeing as corroboration, open the brief and search it yourself for the
  words naming that doubt's mechanism. On 2026-08-15 a hand-off said four doubts had been
  "deliberately excluded from the brief" while the brief asked all four almost word for word
  (B3, C1, C6, C4) — the author was going by what they meant to leave out, not by what the file
  said. Write down what you found for each doubt (held back / prompted by claim ‹id›), and treat
  any "held back" that arrives without that check as unverified.
- **Confirm the gate would actually fail.** When a finding is about a test or gate proving nothing,
  the check is not "does the suite pass" but "would it fail if the thing were wrong." Break it
  deliberately, in a throwaway copy, and see. A gate that passes before its implementation exists
  is the recurring shape.
- **Re-verification hygiene.** Run only commands verified not to rewrite repository files or
  external state — snapshot-updating test runners and cache-writing builds count as writes. The
  throwaway copy for deliberate breakage lives in the session scratchpad, never the working tree.
  End this step by reporting the working state clean: on a version-controlled target, the tree
  (`git status`); on a target with no repository, a file-level substitute — name the only files
  this session wrote and show the target directory otherwise unchanged.

Then two escalation rules:

- A **REFUTED** verdict on a finding **the reviewer rated** high or critical impact, in code you
  authored, requires
  execution evidence. If you cannot execute it, the verdict is `COULD NOT DETERMINE` — not
  `REFUTED` — and you say what would settle it.
- Where your refutation rests on a hypothesis you formed before reading the evidence, get an
  independent check that is blind to that hypothesis rather than arguing for it.

## 6. Rule — two axes, never one word

Every row carries **both**, and they are different questions:

**Verdict — is the reviewer's claim true?**

| | |
|---|---|
| `CONFIRMED` | The defect is real. Evidence in the ledger. |
| `CONFIRMED (partial)` | The mechanism is real; some part — usually prevalence or blast radius — is unestablished. Say which part. |
| `REFUTED` | The claim is false, with evidence at the finding's own standard. |
| `COULD NOT DETERMINE` | Say precisely what would settle it. This is an honest, available outcome. |
| `SETTLED ALREADY` | Relitigates a locked decision. Citation required (step 3). |
| `OWNER RULING REQUIRED` | Not yours to rule on. Reframed as a question in the hand-off. |

**Disposition — what happens now?**

| | |
|---|---|
| `FIX NOW` | Queued for execution in this phase. Name the minimal fix. |
| `FIX LATER` | Requires a durable backlog artifact — seed/todo file, and a requirements row where the project uses them — **created before the ledger is written, with its path quoted in the row.** The artifact must carry three explicitly labeled fields copied from the report — the finding's Location, Mechanism, and Consequence (the ledger row alone does not contain them) — and you verify all three are present before accepting this disposition. A bare-path stub is still a drop wearing a deferral label, and is not permitted. |
| `ACCEPTED AS-IS` | The defect is real and will not be fixed. Requires the owner's words, quoted. You may propose it; you may not issue it. |
| `NO ACTION` | Available only under verdict `REFUTED` or `SETTLED ALREADY`. |
| `VERIFY` | Paired with `COULD NOT DETERMINE`: name the concrete check that would settle it, say whether it blocks execution, and list it in the hand-off. |
| `PENDING OWNER` | May pair with **any** verdict — verdict records truth, disposition records state. With `OWNER RULING REQUIRED` it marks a question about truth; with a settled verdict, write `PENDING OWNER — proposed: <disposition>` and record the owner's answer in ledger §5. Always say whether it blocks execution. |

**Never write a bare "ACCEPTED."** It reads as both "we accept the finding is real" and "we accept
the risk and are shipping it" — opposite dispositions from the same word. Past ledgers in this
project use it in the first sense; new rows use the two-axis form.

Two more rules on the accepted pile:

- **The fix must be the minimal one that closes the finding.** Where a real finding's suggested fix
  would harden throwaway scaffolding or ratchet complexity, the disposition stays `FIX NOW` with a
  *simpler* fix named, or becomes `ACCEPTED AS-IS` with the owner's sign-off. It never quietly
  becomes `NO ACTION` — "the fix is too heavy" is a statement about the fix, not about the defect.
- **A cheap fix in a site this phase already touches is not deferrable**, even when the defect
  predates the phase. Split findings by cost, not by origin.

## 7. Write the ledger

Follow [references/ledger-template.md](references/ledger-template.md). Save to
`<phase-dir>/NN-REVIEW-ADJUDICATION.md`, beside the report and the brief — mirror the report's
prefix. When the target has no phase directory or NN (a skill, a standalone repo), save
`REVIEW-ADJUDICATION.md` beside the report; beside-the-report is the invariant, the prefix is not.

Non-negotiables:

- Every command you ran, with its real output, in the re-verification section. Not paraphrased.
- Nothing in the ledger claims the work is complete, correct, or ready to ship.
- Completed rounds append only. A superseded ruling gets a new row citing the row it supersedes;
  the original row stays as written.
- The only files this skill creates or edits are the ledger, `FIX LATER` backlog artifacts, and —
  when the input review exists only as a chat transcript — the report file materialized from it,
  saved beside the ledger before adjudication begins. Never the code, the plans, or an existing
  review, whatever the tool grants allow.
- Before saving, verify one row per numbered finding and **no empty verdict or disposition cells**,
  and state the counts in the header (numbered findings, plus process and CNV items separately). A
  mismatch is a defect in your own work — a merge row or a header note explains it; dropping a row
  never does.

## 8. Hand off

Report to the user, briefly:

- The ledger path, and the count: N findings in, N rows out.
- **The owner questions**, in full — each as one decidable question with its options and what each
  costs. These are the reason the skill stops here. Say which of them block execution.
- The `FIX NOW` queue, one line each, and an offer to execute it as a separate act. The owner's
  acceptance of that offer **is** the separate, explicit act: record the acceptance verbatim in
  the ledger, and the same session may then execute and backfill. Whoever lands a `FIX NOW`
  change updates that row — a ledger still saying "queued" after the work landed is a false
  record.
- The `FIX LATER` items with their backlog artifact paths, so the user can see they exist.
- Anything you ruled `COULD NOT DETERMINE`, and what would settle it.
- Where a reviewer's figures failed to reproduce, or two reviewers disagreed — that bears on how
  much weight the rest of that report earns.
- One line on what this ledger feeds: the next review brief's "ground already walked" section reads
  it, so those findings are not re-found. That is why undispositioned findings are expensive.

Do not apply fixes in this skill, and do not offer a ship/no-ship judgement.

</process>
