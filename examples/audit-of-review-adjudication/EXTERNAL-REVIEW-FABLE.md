# Independent Audit — the `review-adjudication` skill
**Reviewer:** Claude Fable 5 (claude-fable-5)   **Date:** 2026-08-10
**Coverage:** 22 of 22 §6 load-bearing claims engaged (claims 5 and 20 lightly). Read in full:
both in-scope files (`SKILL.md` 230 lines, `references/ledger-template.md` 157 lines), the sibling
`adversarial-review-prompt/SKILL.md` (315) and its `references/prompt-template.md` (335), and all
three corpus ledgers (103.46, 106.1, 107). Listed every `*EXTERNAL*`/`*ADJUDICATION*` artifact in
`.planning/phases/`; grepped all review prompts for ledger references; measured the description
field. Did **not** read the underlying `NN-EXTERNAL-REVIEW.md` report bodies (relied on the brief's
spot-checked row counts and the ledgers' own prose), the cover-note template, or the sibling's
Codex-audit artifacts.

---

## Defects in the audit brief itself (reported first, per §8)

1. **The §3 "verified facts" figures do not reproduce.** The brief says "all 16 verdict cells in
   the three existing ledgers" with distribution "14 bare ACCEPTED, 1 partially, 1
   resolved-differently." The three ledgers actually hold **32** verdict-bearing rows (103.46: 10 +
   6 across two rounds; 106.1: 7; 107: 9). My tally: 21 bare `ACCEPTED` (7 + 6 in 103.46's rounds,
   8 in 107), 1 `ACCEPTED (partially)`, 1 `ACCEPTED, resolved differently than suggested`, 1
   glossed `ACCEPTED (defect is real…)`, 1 compound `CONFIRMED — OWNER RULING REQUIRED`, and 7
   `FIX — blocking/cheap/trivial` in 106.1. An obedient reviewer executing §6.A1 on "all 16 cells"
   under-samples the retrodiction by half, and the omitted 106.1 `FIX`-family cells are the
   strongest retrodiction evidence in the corpus (they show verdict and disposition already
   conflated in practice). The brief's substantive claims — bare ACCEPTED dominates, no two table
   headers agree — hold.
2. Trivial: the description field measures ~633 characters, not 629 (counting-method difference);
   the ordering-guard quote cited as `SKILL.md:84-86` sits at 85–87. Neither affected the audit.

---

## Findings, ranked

### 1. The two-axis vocabulary is not total: a CONFIRMED finding awaiting an owner disposition has no legal row
- **Class** — irreversible design constraint / false record in the ledger
- **Impact** — high
- **Location** — `SKILL.md:165-184` (the two tables); `:182` (`ACCEPTED AS-IS` "Requires the
  owner's words, quoted. You may propose it; you may not issue it"); `:184` (`PENDING OWNER`
  "Paired with `OWNER RULING REQUIRED`"); `:174`.
- **Mechanism** — a finding whose *truth* is machine-settled but whose *disposition* is the
  owner's call (an `ACCEPTED AS-IS` proposal; a fix-worth-the-cost question) has no legal cell:
  `ACCEPTED AS-IS` cannot be written without owner words that don't exist mid-run; `FIX LATER`
  requires manufacturing a backlog artifact the owner may decline; `PENDING OWNER` is reserved to
  verdict `OWNER RULING REQUIRED`, which per `:174` means "Not yours to rule on" — false here,
  because the truth *was* ruled on. The skill itself creates this state (`:182` invites proposing
  ACCEPTED AS-IS) and then provides no row for it.
- **Trigger** — real and already on disk: `103.46-REVIEW-ADJUDICATION.md` row 2 reads
  `**CONFIRMED — OWNER RULING REQUIRED**` — a compound verdict invented on the spot because no
  single label fit exactly this case (mechanism confirmed real; resolution re-scoped a locked
  decision and went to the owner). §6.21's "hard middle" (defect undisputed, fix-worth-cost open)
  is the same hole and is arguably the most common serious case.
- **Consequence** — every such row is either *illegal* (CONFIRMED + PENDING OWNER, breaking the
  stated pairing) or *false on the verdict axis* (OWNER RULING REQUIRED, recording an established
  truth as un-ruled). Either way the one-way-door vocabulary (§4.1 of the brief) is broken by real
  rows from day one, and downstream briefs machine-reading verdicts misread them. Breaks C-3/C-8.
- **Status** — **CONFIRMED** (corpus row quoted above; tables quoted from the skill).
- **Why it ranks here** — the brief's own words: vocabulary non-totality is the highest-value
  return, and this hole sits on the most common serious case with a corpus instance already.
- **Suggested fix** — drop the exclusivity clause in `:184`: verdict records truth, disposition
  records state, and `PENDING OWNER` may pair with any verdict. Add one legal form for the
  proposal state: `PENDING OWNER — proposed: ACCEPTED AS-IS` (owner's answer recorded in §5 of the
  ledger, row superseded by a new row per the round rule).

### 2. `COULD NOT DETERMINE` has no disposition — the template writes a non-disposition into the cell
- **Class** — lost finding
- **Impact** — high
- **Location** — `SKILL.md:172` (verdict exists), `:180-184` (no compatible disposition;
  `NO ACTION` explicitly closed to it at `:183`); `references/ledger-template.md:66` (row 7's
  Disposition cell holds "«what would settle it, concretely»").
- **Mechanism** — every disposition row presumes either a real defect (`FIX NOW`, `FIX LATER`,
  `ACCEPTED AS-IS`), a dead claim (`NO ACTION`), or an owner question (`PENDING OWNER`). A CND row
  fits none, so the skill's own template fills the Disposition column with an epistemic note —
  which is not a disposition. C-3 ("every finding leaves with a recorded verdict **and** a
  recorded disposition", `SKILL.md:15-17`) is violated by the skill's own worked example.
- **Trigger** — any finding the adjudicator cannot settle: the corpus's standing example is the
  owner-only licensed-editor run (103.46 R2, "remains owner-only by design"); the sibling brief's
  could-not-verify items land here too, and step 2 (`:88-91`) forces them into rows.
- **Consequence** — precisely the at-risk findings leave with no recorded next action. Combined
  with the never-edit-prior-rounds rule (`:71-72`), an undispositioned CND row is frozen: a drop
  with a paper trail. CND becomes the safe parking spot for hard findings (the brief §6.12's
  "confusing finding" pathway) — honest-looking, terminal.
- **Status** — **CONFIRMED** (internal: the two tables plus the template's own row 7).
- **Why it ranks here** — same door as finding 1 but the failure is loss rather than mis-typing;
  no corpus instance yet (all 32 real rows reached decisive verdicts), which is why it ranks second.
- **Suggested fix** — add one disposition row: `VERIFY — <the concrete thing that would settle
  it>; blocks / does not block execution; listed in the hand-off`. The hand-off already requires
  the list (`:222`); the table just cannot express it.

### 3. Report discovery names one of at least three real filename families — a both-family phase gets a half-covered ledger
- **Class** — lost finding
- **Impact** — high
- **Location** — `SKILL.md:65` ("the reviewer's own file (`NN-EXTERNAL-REVIEW.md`, or
  `-<reviewer>.md` when several ran)"); the `description:` at `:3` also names only
  `NN-EXTERNAL-REVIEW.md`.
- **Mechanism** — step 1 resolves "the report" by one naming pattern. A literal resolution in a
  phase holding a second-family report adjudicates half the phase's external findings and reports
  success; in a phase holding *only* another family it resolves nothing.
- **Trigger** — confirmed on disk (`ls` of `.planning/phases/`): **107** and **103.46** each hold
  both `NN-EXTERNAL-REVIEW.md` and `NN-EXTERNAL-CODE-REVIEW.md`; **105** holds only
  `105-EXTERNAL-CODE-REVIEW.md` (+ `-RESPONSE.md`) and no `NN-EXTERNAL-REVIEW.md` at all;
  **103.45** holds a third family the brief itself did not list: `103.45-EXTERNAL-AUDIT-codex.md`.
  The two existing ledgers for 107 and 103.46 name only the `-EXTERNAL-REVIEW` family — whether
  the CODE-REVIEW findings were dispositioned anywhere is not discoverable from any
  `*ADJUDICATION*` file.
- **Consequence** — silent wholesale loss of a report's findings — the exact failure class the
  skill exists to prevent, triggered by the most likely invocation ("adjudicate phase 107").
- **Status** — **CONFIRMED** (directory listing quoted in this audit's working notes; three
  families verified present).
- **Why it ranks here** — highest per-event loss (an entire report), but partially mitigated in
  practice because the user usually points at a specific file; findings 1–2 corrupt the
  vocabulary contract itself.
- **Suggested fix** — step 1 resolves by glob (`<phase-dir>/*EXTERNAL*` minus `*PROMPT*`,
  `*COVER-NOTE*`, `*ADJUDICATION*`), and the ledger header must name every report file found and
  explicitly say which are and are not adjudicated in this ledger.

### 4. The count invariant contradicts itself three ways, and the "fix it" instruction sanctions dropping rows
- **Class** — unenforceable rule / lost finding
- **Impact** — medium
- **Location** — `SKILL.md:88-95` (could-not-verify items, process defects, and prior-review
  disagreements "are findings and they get rows") vs `:96-98` ("The ledger's row count must equal
  the report's finding count", merge allowed with a row saying why) vs `:209-211` ("If they
  differ, that is a defect in your own work — fix it before writing", no carve-out) vs
  `ledger-template.md:74-87` (process defects and CNV items go in their own non-table blocks).
- **Mechanism** — (a) if CNV/process items get table rows per `:88-95`, rows > numbered findings
  and the `:96` equality fails; (b) if they go in the template's separate blocks, step 2's "they
  get rows" is violated; (c) a legitimate merge makes the counts differ, and `:209-211` calls any
  difference a defect to be fixed before writing — the merge allowance and the end-check never
  meet. The denominator ("the report's finding count") is undefined for a report with numbered
  findings plus a CNV list plus prompt-defect preamble.
- **Trigger** — 103.46 round 1: 10 numbered findings + 2 prompt defects + 4 could-not-verify
  items. Rows out = 10, 12, or 16 depending on which instruction is obeyed. Every honest ledger
  with a CNV list hits this.
- **Consequence** — the skill's *only* mechanical end-check is unsatisfiable as specified, and the
  instruction "fix it before writing" hands a compliant model a sanctioned path to making the
  numbers match by dropping exactly the rows (CNV, process) most prone to dropping anyway.
- **Status** — **CONFIRMED** (internal contradiction; corpus trigger real).
- **Why it ranks here** — the guard most likely to be *followed* is the one that's incoherent;
  ranked below 3 because a diligent model documents the discrepancy rather than deleting.
- **Suggested fix** — define the invariant over the report's *numbered* findings only; count the
  auxiliary blocks separately in the header ("Findings in: 10 · Rows out: 10 · +2 process, +4 CNV
  ruled"); add the merge carve-out to `:209-211`.

### 5. C-7's loop is closed by hope: nothing on the reading side names the ledger
- **Class** — broken contract with the sibling skill
- **Impact** — medium
- **Location** — claim: `SKILL.md:225-226` ("the next review brief's 'ground already walked'
  section reads it"). Reading side: `adversarial-review-prompt/SKILL.md:108-124` (§4) and
  `prompt-template.md:127-147` (§7) — "List every prior finding — internal review, code review,
  CI, earlier audits — with its severity label and its **disposition**". No file is named; nothing
  instructs the prompting model to look for `NN-REVIEW-ADJUDICATION.md`.
- **Mechanism** — the payoff claim assumes the sibling discovers the ledger; the sibling's
  contract asks for dispositions but not their canonical source, so discovery depends on the
  prompting model's memory of a convention it was never told.
- **Trigger** — every next-phase brief. Grep across all `*PROMPT*.md` in the corpus: exactly one
  references an adjudication ledger (`103.46-EXTERNAL-REVIEW-2-PROMPT.md`) — written same-day,
  same-author, ad hoc, not by contract. Today's 103.5 prompt cites internal rounds only (no ledger
  existed to cite — consistent with, not proof of, the gap).
- **Consequence** — dispositions get re-derived from reports and memory; findings re-found,
  re-adjudicated, possibly differently; the whole-skill payoff (brief §4.2: otherwise "the skill
  is pure overhead") rests on convention.
- **Status** — **CONFIRMED** (sibling text quoted; corpus grep run).
- **Why it ranks here** — cost is churn and re-work, not loss; the artifact still exists and a
  diligent prompt-writer chasing "dispositions" will usually find it.
- **Suggested fix** — one line in the sibling's §4 and its template §7: "check
  `<phase-dir>/*-REVIEW-ADJUDICATION.md` first — its rows *are* the dispositions." (One-line
  cross-file amendment; the sibling is out of audit scope but in contract scope per brief §4.)

### 6. An interrupted skeleton is trapped by the round-append rule — titles survive, verdicts stay empty, by rule
- **Class** — lost finding
- **Impact** — medium
- **Location** — `SKILL.md:70-72` ("If a ledger already exists at the target path, you are
  appending `# Round N`, not overwriting. Prior rounds are never edited") vs `:81-87` (write the
  skeleton to disk before judging; "Rows exist first; verdicts fill in").
- **Mechanism** — step 2 deliberately puts a half-empty ledger on disk. A session resumed after
  interruption (context death, kill) finds "a ledger already exists at the target path" and is
  instructed to append a new round rather than fill the current one; nothing distinguishes a
  completed round from an abandoned skeleton. The end-check (`:209-211`) counts rows, not filled
  cells, so a row with an empty verdict passes the only mechanical gate.
- **Trigger** — interruption between steps 2 and 7 — the exact scenario the append-as-you-go
  design (inherited from the sibling) exists to survive, and the brief's §6.10 asks about.
- **Consequence** — the brief §2's predicted failure realized by rule rather than drift: "their
  titles survive while their verdicts stay empty," frozen by the no-edit rule.
- **Status** — **THEORETICAL** (no interrupted run exists yet; produced from the rule text alone).
- **Why it ranks here** — real loss pathway, but requires an interruption plus a literal-minded
  resume to fire.
- **Suggested fix** — scope the no-edit rule to *completed* rounds ("a round every one of whose
  rows carries both a verdict and a disposition"); an unfilled skeleton is the current round and
  is filled in place. Extend the end-check to "no empty verdict or disposition cells," which also
  closes §6.10's gap.

### 7. The no-fix boundary contradicts 3-for-3 corpus practice, and the backfill obligation binds nobody
- **Class** — invalid assumption
- **Impact** — medium
- **Location** — `SKILL.md:19-21`, `:180` (`FIX NOW` = "Queued for execution"), `:228`;
  `ledger-template.md:117-124` (§6: "Backfill each row with its commit as the work lands").
- **Mechanism / Trigger** — all three real ledgers record fixes applied by the adjudicating
  session itself: 106.1 "All 7 findings are FIX. **Plans amended in the same session**"; 107's
  disposition column is literally headed "**Where fixed**" (past tense); 103.46's dispositions
  describe amendments already made ("re-floored", "rebuilt", "now three conjuncts"). Under the
  skill as written those sessions must stop, hand off, and execute as a separate act. Meanwhile
  the template's backfill duty has no assigned actor — the fixing session never loads this skill,
  and the skill's last word on stale queues (`:124` "is telling you something true") observes the
  failure without giving anyone the job of noticing it.
- **Consequence** — either the rule bends in practice (rows say "queued" seconds before the same
  session fixes them — a false record in the ledger) or every plan-stage adjudication doubles in
  ceremony; and no mechanism ever marks a `FIX NOW` row done, so C-2's separation relocates the
  drop from "finding never ruled" to "ruling never executed" with nobody watching the second half.
- **Status** — **CONFIRMED** for the practice mismatch (three ledgers quoted); THEORETICAL for the
  unowned-backfill consequence.
- **Why it ranks here** — goes to whether the skill will be *followed*, not just whether it is
  consistent; below 6 because the failure is friction/false-freshness rather than silent loss.
- **Suggested fix** — keep the boundary, add the bridge: the hand-off's offer (`:220`), when
  accepted, *is* the "separate, explicit act" — record the acceptance in the ledger, let the same
  session execute and backfill; and state that whoever lands a `FIX NOW` commit updates the row.

### 8. With no brief on disk, step 1 has no branch and the symmetric-burden rule loses its referent
- **Class** — unenforceable rule
- **Impact** — low
- **Location** — `SKILL.md:68-70` (resolving "the brief it answers" is unconditional);
  `:137-138` ("evidence at the same standard **the brief demanded** of the reviewer").
- **Mechanism** — C-4's burden symmetry is defined by reference to the brief's standard. The
  description invites brief-less inputs ("a Codex/Gemini/GPT/Cursor review report … has landed";
  chat transcripts per `:66-67` — the *report* gets written to disk, but no brief exists to
  reconstruct). No fallback standard is stated, so the refutation bar reverts to the adjudicator's
  own judgement — the asymmetry the rule exists to kill, active exactly when the input is least
  structured.
- **Trigger** — a pasted chat review; corpus-adjacent: 105's `-RESPONSE.md`-shaped exchange shows
  real review artifacts that do not fit the report+brief pair.
- **Status** — **CONFIRMED** for the missing branch (text); THEORETICAL for behavior.
- **Why it ranks here** — narrow trigger; a reasonable model improvises a standard, it just isn't
  bound to one.
- **Suggested fix** — one sentence: "If no brief exists, the standard is this skill's own:
  Location · Mechanism · Trigger · Consequence · Status — both directions."

### 9. The high-impact-refutation gate keys on an impact rating the adjudicator may quietly re-rate
- **Class** — unenforceable rule
- **Impact** — low
- **Location** — `SKILL.md:155-157`; partial guard at `:82-83` (skeleton records
  "reviewer-assigned impact" before judging).
- **Mechanism** — the execution-evidence requirement triggers on "a finding of high or critical
  impact" without saying whose rating governs. The skeleton freezes the *reviewer's* rating first,
  so a down-rate is at least visible as a discrepancy — but nothing forbids it or names it.
- **Status** — **SELF-REPORT**, as the brief invites for §6.B: introspecting honestly, with the
  reviewer's rating frozen in the row I would treat it as operative; absent that line I would
  consider my own assessment controlling. The rule is one word from unambiguous, and a motivated
  reading has room today.
- **Why it ranks here** — the guard is decorative only if the frozen rating is ignored, and
  ignoring it leaves visible evidence; low, not medium, for that reason.
- **Suggested fix** — `:155`: "a REFUTED verdict on a finding **the reviewer rated** high or
  critical…".

### 10. Re-verification runs unbounded in a live tree; "break it deliberately" has hygiene rules only by inheritance
- **Class** — unenforceable rule (envelope)
- **Impact** — low
- **Location** — `SKILL.md:135-152` (`:150` "Break it deliberately, in a throwaway copy");
  contrast `adversarial-review-prompt/references/prompt-template.md:199-205`, which explicitly
  forbids "snapshot-updating test runners and cache-writing builds" for a read-only reviewer.
- **Mechanism** — the sibling names the write-shaped hazards of "just running the tests"; this
  skill instructs reconstructing and running production paths with no such caveat, names no
  location for the throwaway copy and no cleanup/tree-clean obligation — while the adjudicating
  session typically sits mid-phase in a live repo with an uncommitted tree (this project, today,
  literally).
- **Status** — **CONFIRMED** for the asymmetry against the sibling's own text; THEORETICAL for
  damage.
- **Suggested fix** — import the sibling's sentence; name scratch as the copy location; end step 5
  with "report the tree clean."

### 11. Two simultaneous reviewers produce colliding row IDs in one table
- **Class** — false record in the ledger (ambiguous identity)
- **Impact** — low
- **Location** — `SKILL.md:73-76` (one ledger for multiple reviewers) vs
  `ledger-template.md:69` ("Keep the reviewer's numbering"); rounds (`:145`) cover *sequential*
  reviewers, but step 1 frames simultaneous adjudication (disagreements re-verified "before either
  is ruled on") — one pass, one table.
- **Mechanism** — two reports each number findings 1..N; keep-the-numbering with no prefix rule
  yields duplicate `#` cells; "row 3" stops naming one finding, and downstream briefs citing rows
  misresolve.
- **Trigger** — the sibling's own multi-reviewer mode (distinct `NN-EXTERNAL-REVIEW-<reviewer>.md`
  paths, `prompt-template.md:258-260`).
- **Status** — **CONFIRMED** (the two instructions quoted; no disambiguation rule exists).
- **Suggested fix** — one line: when more than one report feeds a round, prefix the ID with the
  reviewer tag (`codex-3`, `gemini-3`).

### 12. `FIX LATER`'s artifact requirement checks existence, not content
- **Class** — unenforceable rule
- **Impact** — low
- **Location** — `SKILL.md:181`.
- **Mechanism** — "durable backlog artifact … created before the ledger is written, with its path
  quoted" is satisfied by a one-line stub; a later reader can verify the path exists, not that the
  artifact carries the finding. A drop wearing a deferral label with a valid-looking path is the
  targeted laundering, one level down.
- **Status** — **THEORETICAL**; partially mitigated in this project, whose seed/todo conventions
  (and the requirements-row clause the skill already includes) impose content by habit.
- **Suggested fix** — require the artifact to contain the finding's Location, Mechanism, and
  Consequence — "copy the row into it" is enough.

### 13. "Include the checks that came out against your expectation" is unfalsifiable as written
- **Class** — unenforceable rule
- **Impact** — low
- **Location** — `references/ledger-template.md:43-44`.
- **Mechanism** — an absent list is indistinguishable from having had no wrong expectations, so
  the section can look rigorous while selecting only confirmations — the precise thing it warns
  against ("self-review with extra steps").
- **Status** — **CONFIRMED** as unfalsifiable by construction (logic, not corpus).
- **Suggested fix** — pre-registration: "state the expected outcome beside each command *before*
  running it." Surprises then surface mechanically instead of by recall.

### 14. `Edit`/`Write` granted unbounded while the body's write set is two artifacts — the envelope is never stated as a sentence
- **Class** — unenforceable rule (C-2's enforcement is only that the rule was stated)
- **Impact** — low
- **Location** — `SKILL.md:5-11` vs `:19-21`, `:206`.
- **Mechanism** — `allowed-tools` cannot scope paths, so the real boundary is prose; the prose
  says "You are not fixing anything in this skill" but never states the write envelope in one
  place the way the sibling *requires of the briefs it writes* ("read, write your report to X,
  modify nothing else" — `adversarial-review-prompt/SKILL.md:221-226`). A model that just
  CONFIRMED a one-line defect holds the tool that fixes it, with only register-level prose in the
  way. This is the skill committing (mildly) the "permission stated two ways" defect it treats as
  reportable elsewhere.
- **Status** — **SELF-REPORT** + CONFIRMED for the textual gap: honestly, the objective's no-fix
  language reads binding to me; the missing piece is the single envelope sentence, which costs one
  line.
- **Suggested fix** — add to §7: "The only files this skill creates or edits are the ledger and
  `FIX LATER` backlog artifacts."

---

## Claims examined and upheld

Keyed to §6 of the brief. Engaged = worked, not merely read.

- **1** — engaged: 31 of 32 real verdict cells re-encode; the failure is 103.46 row 2 (→ finding
  1); 106.1's blocking/cheap/trivial urgency survives only in prose (lossy, tolerable).
- **2** — engaged → finding 1 (the constructed case is real and corpus-instantiated).
- **3** — engaged → finding 2.
- **4** — **upheld**: `CONFIRMED (partial)` + mandatory "say which part" (`:170`) preserves
  103.46 row 6's "mechanism source-settled, prevalence unmeasured" fully.
- **5** — engaged lightly: nonsensical pairs (`REFUTED`+`FIX NOW`, `SETTLED ALREADY`+`FIX LATER`)
  are permitted but no real case forces one; the absent matrix is acceptable — the one pairing
  rule that *does* exist (`PENDING OWNER`) is the harmful one (finding 1).
- **6** — **upheld where a brief exists**: template's REFUTED row demands command-backed evidence
  and §2 demands verbatim output — genuinely symmetric; the dangling referent when no brief
  exists is finding 8.
- **7** — engaged → finding 9 (partial guard found: skeleton freezes reviewer impact first).
- **8** — engaged → finding 12.
- **9** — engaged → finding 4 (the merge clause is bounded less by its own text than by the
  end-check that contradicts it).
- **10** — engaged → finding 6 (the guard preserves titles, not verdicts; end-check counts rows
  only).
- **11** — engaged, SELF-REPORT: the citation requirement does real work — it forces opening the
  decision file, and a quoted `file:line` is checkable by the owner in the hand-off. Novelty of
  evidence remains self-judged; residual risk noted, no stronger mechanism exists short of the
  owner reading every SETTLED row, which the hand-off enables. Not a finding.
- **12** — engaged: the "confusing finding" pathway lands in CND (honest, available) and
  "reviewer misread the code" must clear the refutation burden; the real hazard is CND being
  terminal, which is finding 2. No further unnamed pathway found.
- **13** — engaged → finding 3 (three families, not two).
- **14** — engaged → finding 5.
- **15** — engaged → finding 11.
- **16** — engaged → finding 7.
- **17** — **mostly upheld**: the description fires on "what should I fix from this" ("what to act
  on / worth fixing"), "is Codex right about this" ("whether the reviewer is right"), "triage this
  review" (verbatim). "Close out 107" is the weak phrasing — it matches `gsd-verify-work` at
  least as well and carries no review token; context would have to carry it. No collision with the
  sibling (opposite direction: generate vs adjudicate) or `gsd-code-review` (performs a review).
  Assessed by reading; firing cannot be tested empirically here.
- **18** — engaged → finding 14.
- **19** — engaged → finding 10 (the brief's "what restores it?" has a partial answer — `:150`
  does say "in a throwaway copy" — the gap is location, cleanup, and the snapshot-runner class).
- **20** — engaged lightly, **no defect proven**: the ledger-less half of the corpus is consistent
  with adjudication-skipped-when-trivial, and the skill only fires when invoked; it has no
  de-minimis path, but that follows the deliberate adjudicate-and-record redirect. Recorded as a
  cost, not a finding.
- **21** — engaged: the hard middle case is real, is exactly finding 1's trigger, and the split
  survives *if* verdict and disposition are allowed to split ownership (finding 1's fix). "The
  split is the discipline" holds for the verdict axis only.
- **22** — engaged → finding 13.

One paragraph of checked praise: the ledger template retrodicts the corpus's *practice*
remarkably well — 106.1's blind-verifier §2, 103.46's owner-question block with a dated verbatim
ruling, 107's upheld-claims section all have exact template counterparts, and the two-axis reform
genuinely fixes the bare-ACCEPTED ambiguity for 31 of 32 real cells. The retrodiction failures
above are at the edges the corpus had already hit, not in the core design.

## Could not verify

- **Skill firing behavior** (claim 17) — no way to empirically test description-based skill
  selection in this session; assessed from text only.
- **Whether the `-CODE-REVIEW` family's findings were dispositioned elsewhere** — I searched only
  `*ADJUDICATION*` files and the ledgers' own references; a disposition in some other artifact
  (e.g. a gsd-code-review REVIEW.md flow) would soften finding 3's "uncovered" claim but not the
  discovery gap.
- **The underlying report bodies** — I did not open `NN-EXTERNAL-REVIEW.md` files; row counts and
  CNV counts come from the brief's spot-checked facts and the ledgers' own prose (103.46's ledger
  itself lists 2 prompt defects and 4 CNV items, which is what finding 4 needs).
- **Sibling's Codex-audit artifacts** (`EXTERNAL-REVIEW.md`, `PATCH-VERIFICATION-REVIEW.md`) —
  unread; inherited-convention re-validation was assessed only where the brief pointed (§6.10,
  §6.19).
- **Retracted self-finding, kept for the record**: my first logged finding claimed a stray
  `</output>` tag at `SKILL.md:231`. It was an artifact of my own file-reading harness (the tag
  was the tool's result wrapper, not file content); refuted by `grep -n '</output>' SKILL.md`
  (no match) and `wc -l` (exactly 230). Retracted before ranking. It is also incidental
  confirmation that the brief's line counts (230/157/315/335) are all exact.

## Retrodiction results

| Ledger | Would the skill as written have produced it? | Does the new vocabulary encode every row? |
|---|---|---|
| **103.46** (10+6 rows, 2 rounds) | **Structurally, largely yes** — the template's class list, prompt-defect block, CNV block, owner-question block with dated verbatim ruling, and round-append shape all have exact counterparts here (the template is visibly this ledger's descendant). **Procedurally, no** — every disposition records an amendment already applied in-session (C-2 forbids), the header carries no counts, and CNV/prompt-defect items sit in prose blocks that step 2 says must be rows (finding 4). | **15/16.** Row 2 (`CONFIRMED — OWNER RULING REQUIRED`) has no legal cell — the compound verdict exists *because* the vocabulary hole is real (finding 1). Row 5's gloss ("real, pre-existing, cheap, site already owned") maps to `CONFIRMED`+`FIX NOW` via `:196-197` cleanly; row 6 maps to `CONFIRMED (partial)` losslessly. |
| **106.1** (7 rows) | **No** — different header (`# | Finding | Verdict | Reason`), and its Verdict column holds dispositions (`FIX — blocking/cheap/trivial`): the exact conflation the skill exists to fix. The skill would have restructured it, an improvement. Its §2 (blind second verifier, negative/positive controls, exact figure reproduction) is precisely what the template's §2 demands — the *practice* retrodicts perfectly. Fixes again applied in-session. | **7/7** as `CONFIRMED`+`FIX NOW`, but the blocking/cheap/trivial urgency gradation has no slot in either axis and survives only in prose. |
| **107** (9 rows) | **Mostly** — near-template structure (re-verification first, upheld-claims section, one owner-facing conditional). But the disposition column is "Where fixed", past tense (C-2 again), there is no class column, and the phase's *second* report (`107-EXTERNAL-CODE-REVIEW.md`) is covered by no ledger — finding 3 instantiated in the real corpus. | **9/9.** Row 1 (`ACCEPTED, resolved differently than suggested`) maps to `CONFIRMED`+`FIX NOW` with a different minimal fix named — explicitly supported at `SKILL.md:191-195`. |

**Bottom line:** the vocabulary encodes 31 of 32 real cells and fails on exactly the row type the
corpus had to invent a compound label for (finding 1). The *process* as written would have
produced none of the three ledgers verbatim — chiefly because all three adjudicating sessions
applied fixes in-session (finding 7), and secondarily because the count invariant cannot survive
contact with a real report's CNV and prompt-defect items (finding 4).
