# Independent Audit — the `review-adjudication` skill, Round 2 (post-amendment)
**Reviewer:** OpenAI Codex (GPT-5)   **Date:** 2026-08-10
**Coverage:** 22 of 22 load-bearing claims engaged. Read in full both in-scope files (`SKILL.md`, 261 lines; `references/ledger-template.md`, 160), both sibling contract files (316/336), the round-1 brief/report/ledger (468/416/294), the sibling's two prior audit artifacts (151/29), all four real ledgers, and the untouched 103.5 report plus its 577-line brief. Census-run every report family; read the 105 response in full and the finding/coverage sections needed from the remaining reports. Ran only read-only `find`, `rg`, `wc`, `awk`, `sed`, `stat`, and `git status` checks. Did not re-adjudicate application findings, execute product tests, mutate any target, test unprompted skill selection empirically, or substantively read every unrelated report body.

## Findings, ranked

### 1. “Complete” freezes provisional rows before the required backfill
- **Class** — false record in the ledger / internal contradiction
- **Impact** — high
- **Location** — `review-adjudication/SKILL.md:77-81,205,231,247-251`; `references/ledger-template.md:112-127`; `review-adjudication/REVIEW-ADJUDICATION.md:122-137,233-263`.
- **Mechanism** — A round becomes complete as soon as every table row has any verdict and any disposition. `PENDING OWNER` and `FIX NOW` are valid nonempty dispositions, so unresolved proposals and an unexecuted queue qualify as immutable history. Later rules nevertheless require the owner's answer to be added and whoever lands a fix to “update that row” / “Backfill each row.” Editing violates the completed-round rule; adding prose or a new row does not perform the required row backfill. The lifecycle has no consistent final-state transition.
- **Trigger** — The first-run ledger is the exact case. Row 7 remains `PENDING OWNER — proposed: adopt the recorded-acceptance bridge` at `REVIEW-ADJUDICATION.md:130`; §5 says the proposal was adopted and that a note supersedes the pending state at `:233-239`. Rows 1–6 and 8–14 still say `FIX NOW` at `:124-137`; §5/§6 say all 13 were executed at `:241-263`. No row carries the dated execution reference.
- **Consequence** — The authoritative table says work is pending/queued while later prose says it is resolved/executed. A downstream reader following the sibling's statement that ledger “rows are the dispositions” reads false current state. This violates C-3 and the skill's own `:249-251` definition of a false record.
- **Status** — **CONFIRMED.** The stale table and contradictory later state are present in the only ledger this skill produced. The absence of git history prevents commit hashes, not a dated row-status update—the ledger already has that evidence in prose.
- **Amendment it bears on** — F6, F1's proposal form, and the bridge/backfill amendment jointly opened the lifecycle conflict.
- **Why it ranks here** — It makes false row state the normal successful outcome of executing a queue, and it has already happened.
- **Suggested fix** — Define closure over obligations, not cell presence: all auxiliary entries ruled, no unresolved `PENDING OWNER` or blocking `VERIFY`, and all executed items backfilled. Permit state/evidence backfill until closure; after closure, require a new superseding row for a changed ruling.

### 2. `VERIFY` does not reach the could-not-verify population it was added to protect
- **Class** — lost finding / broken contract
- **Impact** — high
- **Location** — `review-adjudication/SKILL.md:97-108,181-205,235-238`; `references/ledger-template.md:55-95`; sibling `adversarial-review-prompt/SKILL.md:108-114`.
- **Mechanism** — Step 2 declares could-not-verify (CNV) entries to be findings but routes them to an auxiliary block and excludes them from numbered rows. The amended `COULD NOT DETERMINE` + `VERIFY` pairing exists only in the two-axis row schema. The CNV template instead asks whether each gap “blocks anything, is now covered elsewhere, or is still open”; it requires neither a verdict nor a disposition. The no-empty-cell gate covers numbered rows, while downstream the sibling says ledger *rows* are the dispositions.
- **Trigger** — `103.5-EXTERNAL-REVIEW.md:116-122` has five entries: two “could not determine,” two “partially verified only,” and one eleven-item future-UAT gap. Under the stated routing, all five land in prose, not as `COULD NOT DETERMINE`/`CONFIRMED (partial)` rows with `VERIFY`. The first-run ledger demonstrates the shape: `REVIEW-ADJUDICATION.md:174-190` leaves CNV-1 “still open” outside its adjudication table.
- **Consequence** — The ledger passes count and no-empty-cell checks while unresolved verification obligations have no legal two-axis record. A later brief following the row-only reading rule can omit the gap, turning an honest CNV into a downstream pass. This violates C-3 and C-7.
- **Status** — **CONFIRMED.** The untouched 103.5 report supplies the five-entry trigger; the real first-run ledger supplies an open-CNV-outside-the-table instance; the current sibling names rows, not auxiliary entries. This round-2 brief did recover CNV-1 manually, showing diligent full-file reading can mitigate the defect, not that the stated row contract covers it.
- **Amendment it bears on** — F2 incomplete; F4's carve-out and F5's row-only reader preserve the hole.
- **Why it ranks here** — It leaves the most epistemically fragile population outside the fix designed for it.
- **Suggested fix** — Give every CNV a stable ID and Verdict/Disposition fields (including `VERIFY`) in its block; include those fields in closure checks; make the sibling read ruled auxiliary entries as well as the main table.

### 3. The sibling cannot discover the standalone ledger this skill writes
- **Class** — broken contract / lost finding
- **Impact** — high
- **Location** — `review-adjudication/SKILL.md:222-225`; `adversarial-review-prompt/SKILL.md:108-114`; `adversarial-review-prompt/references/prompt-template.md:127-135`.
- **Mechanism** — The writer publishes two shapes: `<phase-dir>/NN-REVIEW-ADJUDICATION.md` and bare `REVIEW-ADJUDICATION.md` beside a non-phase report. The reading amendment checks only `<phase-dir>/*-REVIEW-ADJUDICATION.md`. That glob requires a hyphen before `REVIEW` and cannot match a filename beginning `REVIEW-ADJUDICATION.md`.
- **Trigger** — The only ledger this skill has produced is `~/.claude/skills/review-adjudication/REVIEW-ADJUDICATION.md`, exactly the unmatched form. Command: `find ~/.claude/skills/review-adjudication -maxdepth 1 -type f -name '*-REVIEW-ADJUDICATION.md' -print`; output: empty.
- **Consequence** — For standalone targets, previously ruled findings can be omitted from “ground already walked” and reappear as new; undispositioned items can be mistaken for silence. This round-2 brief contains the history, so some manual/general discovery recovered it, but the claimed canonical reading loop did not do so. C-7 is closed for only one of the two published shapes.
- **Status** — **CONFIRMED.** The current strings, real output filename, and empty read-side-pattern result establish the mismatch.
- **Amendment it bears on** — F5 plus the P-5 non-phase path generalization; individually plausible fixes compose into a broken loop.
- **Why it ranks here** — The loop fails on the skill's own target shape, but broad directory reading can recover the artifact.
- **Suggested fix** — In both sibling files, require looking beside each report for either the phase-prefixed form or bare `REVIEW-ADJUDICATION.md`, and show both literal patterns.

### 4. The worked template can still hide an entire discovered report
- **Class** — lost finding / false record in the ledger
- **Impact** — high
- **Location** — `review-adjudication/SKILL.md:65-70,97-110,235-238`; `references/ledger-template.md:14-24,77-95,145-152`.
- **Mechanism** — F3/F4 amended the body to require a report census, per-report coverage status, and auxiliary counts. Neither template header carries those fields: both show one singular `Review:` and only `Findings in · Rows out`. The body names three auxiliary categories, but its literal count grammar names only process and CNV; the template has no block for disagreements with a prior internal review, only one for disagreements between several external reviewers. Because step 7 says to follow the template, it supplies a complete-looking pre-amendment shape without the amendment's loss detectors.
- **Trigger** — Phase 107 has both `107-EXTERNAL-REVIEW.md` and `107-EXTERNAL-CODE-REVIEW.md`; its ledger names only the former at `107-REVIEW-ADJUDICATION.md:3`. The code-review report has three ranked findings at `:301-337`; exact-title searches find each only in that report. Untouched 103.5 independently requires `+1 process, +5 CNV, +4 prior-review disagreements`, which neither header can fully express.
- **Consequence** — An artifact can look count-complete while a whole discovered report or auxiliary population is absent, defeating C-9 and weakening C-3's only mechanical guard.
- **Status** — **CONFIRMED** for the incomplete cross-file amendment and live corpus trigger. The current template contains neither required addition; the second 107 report's finding population has no matching row in the phase ledger or exact-title trace elsewhere in planning. I did not rule out a differently worded disposition in another artifact. Whether a future model obeys the body over the template conflict is **THEORETICAL**; my self-report is that I would add the body-required fields, but only after noticing the conflict.
- **Amendment it bears on** — F3 and F4 incomplete in the template; F4 is also incomplete in the body's own header grammar.
- **Why it ranks here** — The potential loss is a whole report, but the body states the correct rule clearly enough for a diligent model to override the template.
- **Suggested fix** — Add a required `Reports found:` list with `adjudicated here / already adjudicated in round N / not adjudicated` status to both template headers; add `+K process, +M CNV, +D prior-review disagreements` counts and the missing disagreement block.

### 5. Pasted reviews require a report write that the amended envelope forbids
- **Class** — internal contradiction / lost finding
- **Impact** — medium
- **Location** — `review-adjudication/SKILL.md:65-76,233-234`.
- **Mechanism** — Step 1 supports a chat transcript and requires writing it to disk before adjudication. F14's absolute envelope says the *only* created or edited files are the ledger and `FIX LATER` artifacts—never the review. A report materialized from chat is neither. The model must violate C-10 or stop before enumeration.
- **Trigger** — A user pastes a Codex/Gemini review and asks “is this right?”—a brief-less input the description and F8 explicitly support. The corpus's `105-EXTERNAL-CODE-REVIEW.md` confirms transcript-shaped reviews are real, although that one was already saved.
- **Consequence** — The whole finding population can receive no ruling because its prerequisite report cannot be created within the write set; alternatively the ledger falsely implies C-10 was honored after a third artifact was written.
- **Status** — **THEORETICAL** for behavioral resolution. The current instructions directly contradict and the corpus confirms the input shape, but no run beginning from an unsaved transcript exists.
- **Amendment it bears on** — F14 opened the contradiction; F8 reinforces the now-unexecutable branch.
- **Why it ranks here** — It can lose every finding, but only on the chat-only branch and a model can surface the conflict instead of proceeding.
- **Suggested fix** — Add “a report file materialized from a chat-only input” to the envelope with a fixed destination, or require the user to save it before invoking the skill.

### 6. The interrupted-skeleton exception is contradicted by the template's absolute no-edit rule
- **Class** — lost finding / internal contradiction
- **Impact** — medium
- **Location** — `review-adjudication/SKILL.md:77-81`; `references/ledger-template.md:141-158`.
- **Mechanism** — F6 says an incomplete on-disk skeleton is the current round and must be filled in place. The template still says without qualification: “A follow-up or delta review appends to the same file; it never edits what is already there.” A resumed session receives opposite instructions. Obeying the template preserves the original empty cells and appends elsewhere.
- **Trigger** — Any interruption after step 2 writes the skeleton and before every ruling is filled—the precise partial-file state the write-early design expects.
- **Consequence** — Titles survive but their original verdict/disposition cells remain blank; a later round can be complete while original findings have no ruling. The F6 loss path remains open.
- **Status** — **THEORETICAL.** The contradiction is exact, but no interrupted adjudication skeleton exists. A controlled interrupted run would settle which instruction dominates.
- **Amendment it bears on** — F6 incomplete in `references/ledger-template.md`.
- **Why it ranks here** — It loses findings only after an interruption and template-first conflict resolution.
- **Suggested fix** — Give the template the identical exception: fill incomplete current-round skeletons in place; only completed rounds are immutable.

### 7. F12's “copy the row” shortcut still permits content-free deferral
- **Class** — unenforceable rule / lost finding
- **Impact** — medium
- **Location** — `review-adjudication/SKILL.md:90-91,201`; `references/ledger-template.md:55-68`.
- **Mechanism** — F12 requires a `FIX LATER` artifact to carry Location, Mechanism, and Consequence, then says copying the row is enough. The row schema contains only ID, title, class, verdict, and disposition; step 2 initially seeds only ID, title, and impact. Template row 5 contains a title and artifact path, not the three required fields. Literal compliance with the shortcut fails its own content test.
- **Trigger** — Any confirmed out-of-scope defect under `SKILL.md:128-130`: copy template row 5 into a seed/todo and quote its path.
- **Consequence** — The ledger records a valid durable deferral while the backlog artifact lacks enough information to reproduce or understand the finding—the same laundering path F12 was meant to close.
- **Status** — **THEORETICAL.** The schema proves the shortcut insufficient, but no post-amendment `FIX LATER` pair exists. The real `SEED-124` is content-rich by independent project convention and does not trigger it.
- **Amendment it bears on** — F12 incomplete; the amendment's shortcut contradicts its content requirement.
- **Why it ranks here** — The original drop remains possible, but only when a future finding is deferred.
- **Suggested fix** — Remove the shortcut; require three explicitly labeled fields in the artifact (or a link to a detailed durable finding record) and verify them before accepting `FIX LATER`.

### 8. F10 requires a clean-tree report where no tree exists
- **Class** — unenforceable rule / invalid assumption
- **Impact** — low
- **Location** — `review-adjudication/SKILL.md:167-170,222-225`; `references/ledger-template.md:126-127`.
- **Mechanism** — The standalone path supports non-repository targets, but F10 unconditionally requires reporting “the tree” clean. No fallback defines cleanliness outside version control. The same shape makes the template's commit-only backfill unavailable.
- **Trigger** — This skill's own target. Command: `git -C ~/.claude status`; output: `fatal: not a git repository (or any of the parent directories): .git`.
- **Consequence** — A model must state cleanliness falsely, omit a mandatory result, or refuse otherwise available re-verification; after fixes it must invent a commit or improvise an undocumented substitute. This weakens record truthfulness but does not itself erase a ruling.
- **Status** — **CONFIRMED.** The read-only command produced the quoted failure in the exact environment of the first run.
- **Amendment it bears on** — F10 did not generalize to P-5's standalone target; bridge backfill inherits the premise.
- **Why it ranks here** — Certainly unsatisfiable on a supported target, but likely to produce a disclosed caveat rather than silent loss.
- **Suggested fix** — Define VCS and non-VCS branches: VCS uses status/commit; non-VCS records pre/post hashes or mtimes for the declared set and a dated changed-path plus verification reference.

## Claims examined and upheld

- **1 — REFUTED:** `VERIFY` closes numbered CND rows, not the real CNV auxiliary population (finding 2).
- **2 — CONFIRMED:** a de-minimis real finding has `ACCEPTED AS-IS` when the owner's “do not track” words are available, or a `PENDING OWNER — proposed: ACCEPTED AS-IS` state until they are; no new vocabulary hole was established.
- **3 — REFUTED:** universal `PENDING OWNER` combines with the cell-only completion test to freeze unresolved state (finding 1).
- **4 — REFUTED:** the proposal can resolve in §5 while the row remains pending; the real ledger does exactly that (finding 1).
- **5 — CONFIRMED:** the five real `CONFIRMED (partial)` rows state the established/unestablished part in the Verdict cell; the distinction does not depend on the Disposition axis.
- **6 — CONFIRMED:** the current include/exclude rule selects all ten report files across the seven censused phase directories and all three filename families; 105's `-RESPONSE` is correctly excluded because full read shows it is an adjudication/disposition record, not another review.
- **7 — REFUTED:** the body duty is absent from the template, and “not adjudicated” has no downstream completion obligation (finding 4).
- **8 — REFUTED:** the declared header grammar omits the third auxiliary category, reached by four real 103.5 entries (finding 4).
- **9 — REFUTED:** F2/F3/F4/F5/F6/F10/F12/F14 did not land everywhere or opened a new path; see findings 1–8.
- **10 — REFUTED:** cell completeness is decidable but semantically wrong; it classifies pending/queued rows as complete (finding 1). `--round N` remains undocumented in the process, but no independent wrong result was established beyond that mechanics gap.
- **11 — REFUTED:** non-VCS targets cannot report a git tree clean (finding 8).
- **12 — REFUTED:** the row-copy shortcut does not carry the required content (finding 7).
- **13 — REFUTED in part:** the core write-envelope sentence binds code/plan edits and the bridge can begin a separate act, but it contradicts the chat-materialization write (finding 5). The scratchpad's implementation is unspecified, so I did not separately find on it.
- **14 — CONFIRMED in part:** 103.5 supplies per-finding high/medium labels, 103.45 uses High/Medium/Low in headers, and 106.1 groups findings as Critical/Major/Minor. The gate fires directly for High/Critical; it provides no stated `Major → high` mapping. I did not elevate that taxonomy seam because the general step-5 execution requirement still applies to every machine-checkable finding.
- **15 — CONFIRMED:** read as an act boundary, owner acceptance ends adjudication and starts an explicitly requested fixing act in the same session; `:19-21`/`:259` govern the skill act, while `:247-251` governs the accepted follow-on. No evidence showed the offer wording coerced acceptance.
- **16 — REFUTED:** an actor is named, but the lifecycle forbids or fails its required row update; the first application left every executed row unbackfilled (finding 1).
- **17 — REFUTED:** the sibling pattern covers only phase-prefixed ledgers (finding 3).
- **18 — REFUTED overall:** 103.5 yields eight main rows, but its auxiliary population cannot be represented and counted coherently (findings 2 and 4). The plan/design evidence escape itself holds: the brief and template both authorize cited-source evidence instead of a nonexistent production path.
- **19 — REFUTED:** prior-internal-review disagreements are enumerated in the body but absent from the class list, template block set, and header grammar (finding 4).
- **20 — COULD NOT DETERMINE empirically:** textual collision check mostly holds—the widened description distinguishes adjudicating a landed review from `gsd-code-review` (perform review), the sibling (write a review prompt), and phase-audit/verify skills. Actual unprompted selection has still never been observed.
- **21 — CONFIRMED as a cost, not a correctness defect:** amendments increased fixed ceremony and no proportionality valve exists, but no corpus evidence showed a two-finding run lose or falsify a ruling because of that cost.
- **22 — REFUTED in part:** discovery, fallback evidence, reviewer-tag IDs, and hygiene improve ordinary code-phase runs, but non-VCS cleanliness/backfill and several self-ledger lifecycle rules overfit the first standalone run (findings 1 and 8).

## Round-1 amendments assessed

- **F1 — incomplete / opened a new path:** proposal state is expressible, but resolution is not reconciled with the row or completion rule (`SKILL.md:77-81,205`; finding 1).
- **F2 — incomplete:** `VERIFY` exists for numbered rows but not routed CNV findings (`SKILL.md:97-108,204`; finding 2).
- **F3 — incomplete:** discovery body and description hold; template header remains singular (`ledger-template.md:14-24,145-152`; finding 4).
- **F4 — incomplete:** main numbered invariant is coherent; template headers and the disagreement count/block are not (`SKILL.md:97-110`; finding 4).
- **F5 — incomplete:** phase-prefixed readback holds; bare standalone readback does not (sibling `SKILL.md:111`; finding 3).
- **F6 — incomplete / opened a new path:** body supports incomplete skeletons, template forbids editing them; “complete” now freezes provisional states (`SKILL.md:77-81`; findings 1 and 6).
- **F8 — holds:** a brief-less report gets the same five-part evidence standard in both directions (`SKILL.md:72-76`).
- **F9 — holds in part:** the reviewer governs and High/Critical labels bind; the real Major label is unmapped, though the general execution rule still supplies the evidence duty (`SKILL.md:174-177`).
- **F10 — incomplete:** bounded scratch/command hygiene holds for repositories; unconditional clean-tree reporting fails standalone (`SKILL.md:167-170`; finding 8).
- **F11 — holds:** reviewer-tag prefixes resolve simultaneous-report ID collision (`ledger-template.md:71-73`).
- **F12 — incomplete:** content fields are named, but the permitted row-copy does not contain them (`SKILL.md:201`; finding 7).
- **F13 — holds as instruction, SELF-REPORT:** “before running” made me form expectations before checks; the finished markdown cannot prove timing, but I found no resulting lost or false ruling (`ledger-template.md:39-46`).
- **F14 — opened a new path:** the envelope binds target edits but forbids its own chat-report prerequisite (`SKILL.md:70,233`; finding 5).
- **P-5 non-phase path — incomplete in composition:** the writer, sibling reader, cleanliness check, and commit backfill do not share the same standalone branch (findings 3 and 8).
- **P-7 independence discount — holds:** it directs primary-source re-verification rather than merely relabeling an echo (`SKILL.md:160-162`).
- **Bridge — separation holds; backfill incomplete:** acceptance is an explicit follow-on act, but completed-row immutability and non-VCS evidence make the promised current-state update unreliable (finding 1).

## The 103.5 prediction

Discovery finds one surviving report after exclusions: `103.5-EXTERNAL-REVIEW.md`; the brief is `103.5-EXTERNAL-REVIEW-PROMPT.md`; no ledger exists, so this is round 1.

The amended body's required identity/count material is:

```markdown
**Reports found:** `103.5-EXTERNAL-REVIEW.md` — adjudicated in this ledger
**Findings in: 8 · Rows out: 8 · +1 process, +5 CNV ruled**
```

That line is incomplete: the report also has four `Disagreements with the internal review`, and the specified grammar has no `+D` slot. The truthful extension would be `· +4 prior-review disagreements ruled`, but that is an invented form absent from both files. The template itself would emit only `**Findings in: 8 · Rows out: 8**` and one singular `Review:` line.

The ledger shape required by the whole body is:

1. Header/situation/re-verification sections.
2. Eight numbered table rows, preserving five high and three medium reviewer impacts.
3. One process/prompt-defect entry for the 4,677-versus-4,515 bookkeeping error.
4. Five CNV entries: A2, A4, C16, C17, and the eleven future UAT observations.
5. Four prior-internal-review disagreement entries.
6. Owner questions, locked answers, amendment queue, upheld claims, and unsettled items as applicable.

Step 5 is writable for this plan target: the 103.5 brief explicitly defines source citation/quotation as confirmation, and `ledger-template.md:52-54` supplies the non-executable-target branch. No production call needs to be fabricated.

What cannot be written without improvisation is (a) a template-conformant header that counts all three auxiliary categories, (b) two-axis verdict/disposition records for the five CNV findings, and (c) a template-defined block for the four prior-internal-review disagreements. A ledger containing only the eight main rows nevertheless passes the stated `8 = 8` and no-empty-cell gate.

## Could not verify

- Actual unprompted firing from `description:` remains untested; both known runs were explicit invocations.
- No post-amendment run of the skill exists. Where a finding turns on whether a model follows the body or the conflicting template, I separated the confirmed text/corpus trigger from the theoretical behavioral outcome.
- No interrupted-skeleton or post-amendment `FIX LATER` artifact pair exists; findings 6 and 7 therefore remain THEORETICAL.
- There is no git history under `~/.claude/`, so the amendment sequence and exact pre/post bytes cannot be independently reconstructed. Current text and the dated first ledger are the available record.
- I did not re-adjudicate any corpus-project application finding or substantively inspect every unrelated report body; targeted reads established filename families, impact shapes, auxiliary populations, and otherwise-unrecorded titles only.
- Exact-title searches showed the three 107 code-review titles only in their report and no matching ledger rows; they do not exclude a differently worded disposition in some other artifact.
- I did not run product tests or mutation experiments: the brief authorized read-only inspection only, and none was needed to establish these prose-contract defects.

## Disagreements with the round-1 review and its adjudication

- Round 1 correctly found F2, but its fix was judged against the main table only. The real CNV route never enters that table, so the amendment did not close the population most closely named by the finding.
- F3/F4/F6 were adjudicated as landed after changes to `SKILL.md`, but the worked template retained the singular header, main-only count, and absolute no-edit form. The fix verification stopped one file too early.
- F5 and P-5 were each locally reasonable but were not checked in composition: the sibling glob cannot match P-5's bare filename.
- The adjudication says row 7's pending state is superseded while “the original row stays as written” (`REVIEW-ADJUDICATION.md:233-239`), then codifies a rule that whoever executes must update the row. Those positions are incompatible, and the real ledger demonstrates the resulting false table state.
- F12's amendment copied the finding's requested field names but added an unjustified assertion that the row already carries them. The template proves it does not.
- F10 was verified only as repository hygiene, despite the skill's first target and new P-5 branch being outside version control.
- The round-1 ruling that F14's one-line envelope closes the write boundary missed the pre-existing chat-materialization instruction; the amendment made that contradiction absolute.
