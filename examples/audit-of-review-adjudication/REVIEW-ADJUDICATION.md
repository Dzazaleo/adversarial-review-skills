# `review-adjudication` skill — External Review Adjudication (Round 1)

**Review:** `EXTERNAL-REVIEW-FABLE.md` (Claude Fable 5, 2026-08-10, envelope honoured — the report file was its only write; one self-finding retracted in-file with the refuting commands shown)
**Brief:** `EXTERNAL-REVIEW-PROMPT.md`
**Target:** this skill directory (`SKILL.md`, `references/ledger-template.md`); sibling contract surface read but not adjudicated as a target
**Adjudicated:** 2026-08-10, by a Claude Fable 5 session deliberately blind to the authoring conversation (the author's design arguments were not in context; owner's instruction)
**Findings in: 14 · Rows out: 14** · +2 brief defects ruled in the process block · +5 could-not-verify items ruled in their block

> **Count convention (deviation, recorded):** the invariant population is the report's *ranked*
> findings (14 = 14). Brief defects and CNV items are counted separately in this header rather
> than folded into one number. This deviates from a literal reading of `SKILL.md:96-98` and
> `:210-211` and is live evidence for finding 4 — see P-3.

> **Independence discount (owner-supplied, not visible in the report):** the brief's §6 claims
> behind findings **1, 5, 6, 14** were the author's own residual doubts leaked into the brief
> (the known `residual-doubts-leak-into-the-brief` failure). For those four rows, reviewer
> agreement is treated as an echo of the author, and the verdict below rests ONLY on this
> adjudication's direct checks of primary sources (skill text, sibling text, corpus). All four
> verdicts survived that discount on primary evidence alone.

## 1. Situation in one paragraph

The `review-adjudication` skill (written and self-reviewed by Claude Opus 5 in one session on
2026-08-10, never run) was audited by an external Claude Fable 5 instance against a brief that
demanded retrodiction against the three real adjudication ledgers in the the corpus project
corpus (103.46, 106.1, 107). The reviewer engaged 22/22 load-bearing claims and returned 14 ranked
findings (3 high, 4 medium, 7 low), 2 defects in the brief itself, and a 5-item could-not-verify
list including one honestly retracted self-finding. Its headline results: the two-axis
verdict/disposition vocabulary is not total (a corpus row already had to invent a compound label);
`COULD NOT DETERMINE` has no legal disposition; report discovery misses two of three real filename
families; the count invariant is self-contradictory; and the no-fix boundary contradicts all three
existing ledgers' actual practice. This adjudication — the skill's first real run, applied to
itself — re-verified every machine-checkable claim from primary sources and additionally observed
two findings (1 and 4) fire live against this very ledger.

## 2. Re-verification performed before accepting anything

Commands run in `~/projects/corpus-project` (corpus checks) and on the
skill files, with real output. Full files read line-numbered: `SKILL.md` (all 230), `ledger-template.md`
(all 157), the three corpus ledgers (all lines), sibling `SKILL.md:100-129` and `:215-229`,
sibling `prompt-template.md:125-149`, `:195-209`, `:252-265`.

**Verdict-cell recount (bears on BD-1, and on findings 1, 7):** manual tally from full reads —

| Ledger | Rows | Bare ACCEPTED | Other labels |
|---|---|---|---|
| 103.46 R1 | 10 | 7 (rows 1,3,4,7,8,9,10) | row 2 `CONFIRMED — OWNER RULING REQUIRED`; row 5 glossed `ACCEPTED (defect is real…)`; row 6 `ACCEPTED (partially)` |
| 103.46 R2 | 6 | 6 (R2-1…R2-6) | — |
| 106.1 | 7 | 0 | 7 × `FIX — blocking/cheap/one line/trivial` (verdict column holds dispositions) |
| 107 | 9 | 8 (rows 2–9) | row 1 `ACCEPTED, resolved differently than suggested` |
| **Total** | **32** | **21** | |

Reviewer claimed 32 rows / 21 bare (7+6+8): **reproduces exactly.** Brief claimed "all 16 cells,
14 bare": **does not reproduce.**

**Filename families (finding 3):**
```
$ find .planning/phases -maxdepth 2 -name "*EXTERNAL*" | sort
```
26 files. Three families verified present exactly as the reviewer stated: 103.46 and 107 each hold
BOTH `NN-EXTERNAL-REVIEW.md` and `NN-EXTERNAL-CODE-REVIEW.md`; 105 holds only
`105-EXTERNAL-CODE-REVIEW.md` (+`-RESPONSE.md`, a fourth artifact shape) and no
`NN-EXTERNAL-REVIEW.md`; 103.45 holds `103.45-EXTERNAL-AUDIT-codex.md`.

**Reading-side ledger reference (finding 5):**
```
$ grep -l "ADJUDICATION" .planning/phases/*/*PROMPT*.md
.planning/phases/103.46-loose-re-import-alpha-convention-inserted/103.46-EXTERNAL-REVIEW-2-PROMPT.md
```
Exactly one prompt, as the reviewer found. Direct read of sibling `SKILL.md:108-124` (§4) and
`prompt-template.md:127-147` (§7): dispositions demanded, **no file named** — confirmed
independently of the seeded doubt.

**CNV-2 check the reviewer could not run (bears on finding 3's consequence):**
```
$ grep -rln "EXTERNAL-CODE-REVIEW" .planning --include="*.md" | grep -v "EXTERNAL-CODE-REVIEW"
.planning/STATE.md
.planning/seeds/SEED-124-attachment-paths-escape-the-detector-population.md
.planning/todos/pending/2026-08-09-107-residuals-451-symmetry-and-stale-citation.md
.planning/todos/resolved/2026-08-09-103-46-wr05-detector-memo-self-invalidation.md
.planning/phases/103.46-.../103.46-VERIFICATION.md  (+ REVIEW.md, SECURITY.md, UAT.md)
```
The `-CODE-REVIEW` family's findings were NOT silently lost in practice — they were handled through
other artifacts (gsd-code-review flow, seeds, todos). **Against my expectation** (I expected no
trace). Softens finding 3's "uncovered" consequence; the adjudication-record discovery gap stands.

**Measurements (BD-2, line counts):**
```
$ wc -l SKILL.md ledger-template.md ../adversarial-review-prompt/SKILL.md .../prompt-template.md
230 / 157 / 315 / 335        (all four exactly as brief and reviewer stated)
$ awk '/^description:/{print length($0)}' SKILL.md
648                          (minus "description: " prefix (13) and quotes (2) = 633 — reviewer's 633 reproduces; brief's 629 does not)
```
**Against my expectation:** the ordering-guard quote actually spans `SKILL.md:84-85` (verified in
the line-numbered read). The brief's citation `:84-86` is off by one at the tail — and the
reviewer's correction ("sits at 85–87") is off by one at both ends. The reviewer's sole
non-reproducing figure.

**Line citations:** every `SKILL.md` and `ledger-template.md` line cited in findings 1–14 was
checked against the line-numbered read; all anchor correctly (±1 line where ranges were rounded).
Corpus quotes verified verbatim: `103.46-REVIEW-ADJUDICATION.md:16` row 2 compound verdict;
`106.1-REVIEW-ADJUDICATION.md:6` "All 7 findings are FIX. Plans amended in the same session.";
`107-REVIEW-ADJUDICATION.md:20` disposition column headed "Where fixed"; 103.46 R1 = 10 numbered
findings + 2 prompt defects (lines 26-28) + 4 CNV items (lines 30-33), finding 4's exact trigger.

**Live instantiations observed during this run (not from the report):**
- Row 7 below requires verdict `CONFIRMED (partial)` + disposition `PENDING OWNER` — the pairing
  `SKILL.md:184` forbids. Finding 1 fired on the skill's first real use.
- This ledger's header could not satisfy the literal count invariant (14 findings + 2 brief
  defects + 5 CNV items). Finding 4 fired on first use.
- Filling this skeleton in place after writing it collides with a literal reading of the
  never-edit rule at `SKILL.md:71-72` — finding 6's mechanism, observed as friction (resolved by
  reading "prior rounds" as completed rounds, which is exactly the fix the reviewer proposes).

## 3. Adjudication

Class abbreviations are the reviewer's. Reviewer-assigned impact frozen at enumeration; none
re-rated. No `SETTLED ALREADY` verdict was available for any row: the author's design arguments
exist only in an unavailable conversation, and no durable locked-decision artifact exists for this
skill (see P-6).

| # | Finding (title, verbatim) | Impact | Class | Verdict | Disposition |
|---|---------------------------|--------|-------|---------|-------------|
| 1 | The two-axis vocabulary is not total: a CONFIRMED finding awaiting an owner disposition has no legal row | high | irreversible design constraint | **CONFIRMED** — `:184` pairing rule + `:174` "Not yours to rule on" + `:182` owner-words requirement quoted; corpus instance `103.46:16` verified; re-instantiated live by row 7 of THIS ledger. (Seeded finding; confirmed on primary evidence alone.) | **FIX NOW** — in `SKILL.md:184`: verdict records truth, disposition records state; `PENDING OWNER` may pair with any verdict; add the legal proposal form `PENDING OWNER — proposed: <disposition>` with the owner's answer recorded in ledger §5 |
| 2 | `COULD NOT DETERMINE` has no disposition — the template writes a non-disposition into the cell | high | lost finding | **CONFIRMED** — `:172` vs `:180-184` (no compatible row; `NO ACTION` closed at `:183`); `ledger-template.md:66` row 7's Disposition cell verified to hold an epistemic note, violating C-3 in the skill's own worked example | **FIX NOW** — add disposition `VERIFY — <what would settle it>; blocks / does not block execution; listed in the hand-off`; correct template row 7 |
| 3 | Report discovery names one of at least three real filename families — a both-family phase gets a half-covered ledger | high | lost finding | **CONFIRMED (partial)** — mechanism fully established (three families on disk, census above; `:65` and the `description:` at `:3` name one). Consequence "silent wholesale loss" overstated: CNV-2 check shows the CODE-REVIEW findings were dispositioned via other artifacts. The adjudication-record gap is real; the practical loss was lower | **FIX NOW** — step 1 resolves by glob (`<dir>/*EXTERNAL*` minus `*PROMPT*`, `*COVER-NOTE*`, `*ADJUDICATION*`, `*RESPONSE*`); ledger header MUST enumerate every report file found and state which are and are not covered by this ledger; widen the description's example naming |
| 4 | The count invariant contradicts itself three ways, and the "fix it" instruction sanctions dropping rows | medium | unenforceable rule / lost finding | **CONFIRMED** — `:88-94` vs `:96-98` vs `:210-211` vs template's separate blocks (`:74-87`) all quoted and mutually incompatible; trigger verified (103.46 R1: 10+2+4); fired live against this ledger's own header | **FIX NOW** — invariant defined over the report's *numbered* findings; auxiliary blocks counted separately in the header (the format this ledger uses); merge carve-out added to `:210-211` |
| 5 | C-7's loop is closed by hope: nothing on the reading side names the ledger | medium | broken contract with the sibling skill | **CONFIRMED** — sibling §4 and template §7 read directly: no file named; corpus grep: exactly 1 of 10+ prompts ever cited a ledger, ad hoc. (Seeded finding; confirmed on primary evidence alone.) | **FIX NOW** (lands in the SIBLING, cross-file, flagged for owner visibility) — one line in sibling §4 + template §7: "check `<phase-dir>/*-REVIEW-ADJUDICATION.md` first — its rows are the dispositions" |
| 6 | An interrupted skeleton is trapped by the round-append rule — titles survive, verdicts stay empty, by rule | medium | lost finding | **CONFIRMED (partial)** — the rule conflict is textually real (`:71-72` vs `:81-86` quoted; end-check `:210-211` counts rows, not filled cells); the loss event itself remains unobserved (reviewer honestly marked THEORETICAL; observed here only as benign friction). (Seeded finding; confirmed on primary evidence alone.) | **FIX NOW** — scope never-edit to *completed* rounds (every row carries both verdict and disposition); extend the end-check to "no empty verdict or disposition cells" |
| 7 | The no-fix boundary contradicts 3-for-3 corpus practice, and the backfill obligation binds nobody | medium | invalid assumption | **CONFIRMED (partial)** — practice mismatch established 3-for-3 (quotes in §2); the unowned-backfill *consequence* (rulings never marked executed) is textually real (`ledger-template.md:123-124` assigns no actor) but unobserved | **PENDING OWNER — proposed: adopt the recorded-acceptance bridge** (see §4 Q1). Does not block the rest of the FIX NOW queue. *This row uses the compound form finding 1 legalizes — under `SKILL.md` as written it is illegal, which is itself evidence for row 1* |
| 8 | With no brief on disk, step 1 has no branch and the symmetric-burden rule loses its referent | low | unenforceable rule | **CONFIRMED** — `:68-70` unconditional; `:137-138` defines the refutation bar by "the brief"; the `description:` explicitly invites brief-less reports. Textual gap; behavioral damage theoretical | **FIX NOW** — one sentence: "If no brief exists, the standard is this skill's own: Location · Mechanism · Trigger · Consequence · Status — both directions" |
| 9 | The high-impact-refutation gate keys on an impact rating the adjudicator may quietly re-rate | low | unenforceable rule | **CONFIRMED (partial)** — the textual ambiguity is real (`:155` names no rating owner; `:82` freezes the reviewer's); the escape behavior is SELF-REPORT only, per the brief's own admissible-evidence rules | **FIX NOW** — three words at `:155`: "a finding **the reviewer rated** high or critical" |
| 10 | Re-verification runs unbounded in a live tree; "break it deliberately" has hygiene rules only by inheritance | low | unenforceable rule (envelope) | **CONFIRMED** — asymmetry verified by direct read: sibling `prompt-template.md:199-205` names snapshot-updating runners and cache-writing builds; `SKILL.md:135-152` names none; `:150` has "throwaway copy" but no location or cleanup duty | **FIX NOW** — import the sibling's sentence; name the session scratchpad as the throwaway location; end step 5 with "report the tree clean" |
| 11 | Two simultaneous reviewers produce colliding row IDs in one table | low | false record in the ledger | **CONFIRMED** — `:73-76` (one ledger) + `ledger-template.md:69` ("Keep the reviewer's numbering") + sibling `:258-260` (per-reviewer report paths are the sibling's own design) — collision follows with no disambiguation rule | **FIX NOW** — one line in template §3: multiple reports in one round ⇒ prefix IDs with the reviewer tag (`codex-3`, `fable-3`) |
| 12 | `FIX LATER`'s artifact requirement checks existence, not content | low | unenforceable rule | **CONFIRMED (partial)** — `:181` verified to require existence + path only; the laundering path is theoretical and partially mitigated by this project's seed/todo conventions (e.g. SEED-124's content-rich form) | **FIX NOW** (cheap, in a site already being amended — `:196-197` makes it non-deferrable) — require the artifact to contain the finding's Location, Mechanism, Consequence: "copy the row into it" |
| 13 | "Include the checks that came out against your expectation" is unfalsifiable as written | low | unenforceable rule | **CONFIRMED** — unfalsifiable by construction (`ledger-template.md:43-44`): an absent list is indistinguishable from no wrong expectations. (This ledger's §2 pre-registered two expectations; both surprises surfaced mechanically) | **FIX NOW** — pre-registration line in template §2: state the expected outcome beside each command before running it |
| 14 | `Edit`/`Write` granted unbounded while the body's write set is two artifacts — the envelope is never stated as a sentence | low | unenforceable rule | **CONFIRMED** — textual gap verified: `:5-11` grants unbounded tools; no single envelope sentence exists; the sibling requires exactly that of every brief it writes (`:221-226`, read directly). Bindingness of the existing prose is SELF-REPORT. (Seeded finding; confirmed on primary evidence alone.) | **FIX NOW** — one line in §7: "The only files this skill creates or edits are the ledger and `FIX LATER` backlog artifacts" |

### Process and prompt defects (the reviewer's preamble + this run's own)

- **BD-1 — the brief's §3 "verified facts" figures do not reproduce.** REAL, independently
  recounted (table in §2): 32 verdict cells / 21 bare ACCEPTED, not 16 / 14. The brief's
  substantive claims (bare-ACCEPTED dominance, three disagreeing headers) survive; the figures do
  not, and an obedient §6.A1 execution would have under-sampled retrodiction by half — the omitted
  106.1 FIX-family cells are the strongest conflation evidence in the corpus. What changed: the
  recount stands here as the corrected record; the next brief's authoring must recount, not quote.
  This is the second brief-authoring failure in this pair (with the §6 leak the owner reported) —
  both now on record for the sibling skill's next revision.
- **BD-2 — trivial measurement drift.** REAL both directions: description is 633 chars (brief said
  629, reviewer's 633 reproduces); but the ordering-guard quote sits at `:84-85` — the brief was
  off by one, and **the reviewer's own correction (85–87) is also wrong**. The reviewer's only
  non-reproducing figure. Harmless; noted for weight calibration only.
- **P-3 — count invariant fired on this run** (header deviation documented above). Live
  confirmation of finding 4 by the skill's first real use.
- **P-4 — compound row required on this run** (row 7). Live confirmation of finding 1.
- **P-5 — the skill assumes a phase directory and NN prefix.** This target is a skill directory
  with no phase number; ledger path and name were improvised as `REVIEW-ADJUDICATION.md` beside
  the report. Cheap generalization available when the FIX NOW queue executes: "save beside the
  report, mirroring its prefix" — the phase form remains the common case.
- **P-6 — step 3 had no ground to screen against.** The author's argued-for design choices
  (the adjudicate-and-record redirect, the C-2 boundary, the pairing rule) live only in the
  authoring conversation; no durable decision record exists for this skill. Consequence: deliberate
  choices and oversights are indistinguishable to a blind adjudicator — which the owner chose
  deliberately here, but which also means findings 1 and 7 attack choices whose rationale could not
  be weighed. If the owner wants argued-for choices defensible in future rounds, they need a
  decisions block somewhere durable (owner's call; queued as a question, not a fix).
- **P-7 — the skill has no slot for non-independent confirmations.** The owner's seeding
  disclosure (findings 1, 5, 6, 14) had to be handled by an improvised header note and per-row
  discount. The existing memory (`residual-doubts-leak-into-the-brief`) prevents the leak at
  authoring time; nothing handles it at adjudication time when it has already happened. Optional
  one-line fix rolled into the queue (step 5: "where a brief claim was the author's own suspicion,
  reviewer agreement is not independent confirmation — verify from primary sources").

### Reviewer's could-not-verify items

- **CNV-1 — skill firing behavior (claim 17):** still open; only live invocation-by-description
  settles it. This run invoked the skill by explicit name, so it contributes no evidence. Does not
  block. The reviewer's "close out 107" weak-phrasing observation stands as a residual risk.
- **CNV-2 — whether `-CODE-REVIEW` findings were dispositioned elsewhere:** **now resolved** (§2):
  yes, through non-adjudication artifacts (8 files). Finding 3's verdict adjusted to
  CONFIRMED (partial) accordingly. Closed.
- **CNV-3 — underlying report bodies unread:** the one load-bearing dependence (103.46's 10+2+4
  composition, finding 4's trigger) was verified from the ledger's own prose in this session's full
  read. Remaining dependence is nil; acceptable, still open as stated.
- **CNV-4 — sibling's Codex-audit artifacts unread:** still open. Bears only on
  inherited-convention re-validation, which findings 6 and 10 engaged directly anyway. Acceptable.
- **CNV-5 — retracted self-finding (stray `</output>` tag):** retraction verified in kind — the
  reviewer published its own refuting commands (`grep -n '</output>' SKILL.md` → no match;
  `wc -l` → 230, which this session's `wc -l` reproduces). An honest self-retraction with evidence;
  raises the report's credibility. Closed.

## 4. Owner decisions required

### Q1 — Does the no-fix boundary (C-2) get a bridge, stay strict, or get relaxed? (finding 7)

**What turns on it:** whether the skill's rule matches how you actually work. All three real
ledgers were written by sessions that fixed in-session; under the skill as written every one of
them violated C-2, and future runs will either bend the rule (false "queued" records) or double
the ceremony.
**Options:**
- **A — recorded-acceptance bridge (reviewer's proposal, my recommendation):** the hand-off's
  offer, once you accept it, *is* the "separate, explicit act"; acceptance is recorded in the
  ledger, the same session executes and backfills, and whoever lands a `FIX NOW` commit updates
  the row. Costs one recorded sentence per run; keeps the separation-of-acts principle; assigns
  the backfill an actor (closes the second half of finding 7).
- **B — strict boundary as written:** adjudication always stops; a later session executes. Maximal
  drift protection; contradicts 3-for-3 corpus practice and doubles ceremony on plan-stage runs.
- **C — accept as-is:** rule stays, practice keeps violating it, ledgers keep recording "queued"
  for work done seconds later. A standing false record; not recommended.
**Recommendation:** A — it is the only option under which the three existing ledgers would have
been compliant, and it gives the backfill obligation an owner.
**Blocks:** nothing in this round's queue (queue execution awaits your go-ahead regardless), but it
should be answered before the skill's next run.

### Q2 — May the vocabulary fixes (findings 1 and 2) change the one-way door?

**What turns on it:** the verdict/disposition vocabulary is the brief's declared one-way door.
Findings 1 and 2 are proven holes, and the fixes are additive (a legalized pairing + a `VERIFY`
disposition), retroactively legalizing 103.46's row 2 rather than invalidating anything. I ruled
them FIX NOW on that basis — but changing a one-way door on the author's argued-for design without
the author present is the kind of call you said you wanted surfaced.
**Options:**
- **A — execute as ruled** (recommended): the corpus already needed both forms; only 4 ledgers
  exist; the door gets cheaper to change never.
- **B — hold the vocabulary, fix everything else:** preserves the author's exclusivity argument
  (which is not in evidence anywhere durable — see P-6) at the cost of the next real run hitting
  the same wall this one did (rows 7 and P-4).
**Recommendation:** A, with one clause: the holes fired on the skill's very first run.
**Blocks:** findings 1 and 2 in the queue; nothing else.

## 5. Locked owner decisions from this adjudication

**D-R1-1 (answers Q2, and Q1 by enactment) — owner, 2026-08-10:** *"If you think this skill
is usefuld do the recommended changes to it"* — given after the hand-off's usefulness assessment.
Sanctions executing the full FIX NOW queue as ruled, including the one-way-door vocabulary changes
(findings 1, 2). The instruction to execute in-session is Q1's option A enacted: this acceptance,
recorded here, is the "separate, explicit act," and the bridge rule is now codified in
`SKILL.md` step 8. Row 7's disposition resolves accordingly — the proposed bridge was adopted
(this note supersedes the pending state; the original row stays as written).

**Executed same session, 2026-08-10:** all 13 queue items + P-5 + P-7 applied across
`SKILL.md`, `references/ledger-template.md`, and (F5, cross-file) the sibling's `SKILL.md` §4 and
`prompt-template.md` §7.

## 6. Amendments required (the FIX NOW queue — 13 items, **all executed 2026-08-10** per D-R1-1)

Each landed in this skill's files unless marked; IDs reference §3. Items 1–2 were gated on Q2,
answered by D-R1-1. No git history exists for `~/.claude/skills/`, so the backfill reference is
this dated note rather than commits.

1. **F1** — `SKILL.md:184`: unpair `PENDING OWNER`; add `PENDING OWNER — proposed: <disposition>` form. *(gated on Q2)*
2. **F2** — `SKILL.md` disposition table + `ledger-template.md:66`: add `VERIFY — …` disposition. *(gated on Q2)*
3. **F3** — `SKILL.md:65` + `:3`: glob-based report discovery; header enumerates all reports found, covered and not.
4. **F4** — `SKILL.md:96-98`, `:210-211`: invariant over numbered findings; auxiliary counts separate; merge carve-out.
5. **F5** — *sibling* `SKILL.md` §4 + `prompt-template.md` §7: one line naming `*-REVIEW-ADJUDICATION.md` as the disposition source. *(cross-file)*
6. **F6** — `SKILL.md:71-72` + `:210-211`: never-edit scoped to completed rounds; end-check adds "no empty cells".
7. **F8** — `SKILL.md` step 1/5: fallback evidence standard when no brief exists.
8. **F9** — `SKILL.md:155`: "the reviewer rated".
9. **F10** — `SKILL.md` step 5: sibling's mutation-hygiene sentence; scratchpad as throwaway location; "report the tree clean".
10. **F11** — `ledger-template.md` §3: reviewer-tag ID prefix rule for multi-report rounds.
11. **F12** — `SKILL.md:181`: backlog artifact must contain Location/Mechanism/Consequence ("copy the row into it").
12. **F13** — `ledger-template.md` §2: pre-register expected outcomes beside commands.
13. **F14** — `SKILL.md` §7: the single write-envelope sentence. *(+ optional P-5 path generalization and P-7 independence-discount line, rolled in if owner approves)*

## 7. Claims examined and upheld

The reviewer's coverage: 22/22 §6 claims engaged, 4 upheld outright — claim 4 (`CONFIRMED
(partial)` preserves the corpus's partially-row losslessly), claim 6 (refutation burden genuinely
symmetric where a brief exists), claim 11 (the SETTLED ALREADY citation gate does real work), claim
17 (description fires on the user's actual phrasings, "close out NN" weakest). Claim 20 ruled a
cost, not a defect (no de-minimis path is deliberate). Spot-checked here: the upheld-4 mapping was
re-run against 103.46 row 6 and holds; the retrodiction bottom line (31/32 cells encode; all three
ledgers procedurally non-compliant via finding 7) is consistent with this session's own reads. The
reviewer's figure-reproduction record after independent recount: every figure reproduced except one
off-by-one line citation (BD-2) — a record that earns its SELF-REPORT and THEORETICAL claims
above-default weight.

## 8. What this review could not settle, and why that is acceptable

- **Whether the skill fires unprompted from its description** (CNV-1) — only real future
  invocations settle it; the first data point will arrive free the next time a review lands.
- **Whether the interrupted-skeleton trap (F6) and FIX LATER laundering (F12) occur in practice** —
  both ruled on textual mechanism; their fixes are one-liners, cheaper than waiting for an
  occurrence.
- **The author's design rationale for the attacked choices** (P-6) — deliberately excluded by the
  owner. The cost is bounded: both attacked designs (pairing exclusivity, strict C-2) go to the
  owner as Q1/Q2 rather than being silently overridden.
- **Model-behavioral claims** (F9, F14 bindingness) — SELF-REPORT is the ceiling the brief itself
  set for these; the fixes are cheap enough that settling the behavioral question first would cost
  more than the fix.

This ledger feeds the next review brief's "ground already walked" section: findings 1–14 and their
dispositions here are covered ground; Q1/Q2 outcomes and the executed-fix commits should be
appended as Round 2 when they land.

---

# Round 2 — post-amendment audit (Codex GPT-5)

**Reports found (census):** `EXTERNAL-REVIEW-FABLE.md` (round 1 — adjudicated in Round 1 above; history) ·
`EXTERNAL-REVIEW-2.md` (adjudicated in this round). No other `*EXTERNAL*` report files exist in the
target directory after the standard exclusions.
**Review:** `EXTERNAL-REVIEW-2.md` (OpenAI Codex GPT-5, 2026-08-10, envelope honoured — the report
file was its only write; its coverage line declares read-only commands only, and the directory
holds no other new artifact)
**Brief:** `EXTERNAL-REVIEW-2-PROMPT.md` (author's residual doubts withheld this round per its §7 —
no independence discount required; every §6 claim treated as independent)
**Adjudicated:** 2026-08-10, by a Claude Fable 5 session — the skill's second real run and its
first *post-amendment* run; this run's own live observations are recorded as P-R2-* below
**Findings in: 8 · Rows out: 8** · +0 process/prompt defects reported · +7 CNV items ruled ·
+7 round-1 disagreement items ruled (Corrections block)

> **Grammar note — live evidence for finding 4 (P-R2-1):** the header grammar at `SKILL.md:108`
> has no slot for the third auxiliary category; the `+7 round-1 disagreement items` form above is
> invented, exactly as the reviewer's 103.5 prediction said it would have to be.

## 1. Situation in one paragraph

The 13 round-1 amendments (plus P-5, P-7, and the owner-ruled bridge) were audited by OpenAI Codex
GPT-5 against a brief demanding it treat every amendment as a claim by the party under review. It
engaged 22/22 load-bearing claims and returned 8 ranked findings (4 high, 3 medium, 1 low), zero
brief defects, 7 could-not-verify items, and 7 disagreements with the round-1 review/adjudication.
Its headline: the amendments individually landed but fail in composition — round "completeness"
freezes rows before the backfill the bridge requires (and the round-1 ledger already exhibits the
false state); the `VERIFY` fix never reaches the CNV population that motivated it; the sibling's
new reading glob cannot match the standalone ledger filename this skill writes; and the worked
template still teaches the pre-amendment header. All eight findings were re-verified here from
primary sources; every reviewer figure re-run reproduced exactly. Three round-1 fixes (F1/F6
composed with the bridge, F5 composed with P-5, F14) opened new paths to the failures they closed.

## 2. Re-verification performed before accepting anything

Expectations pre-registered per check; all commands read-only. One check surprised (marked ⚠).

1. **Sibling reading-side text (findings 2, 3).** Expected: both amended lines name only
   `<phase-dir>/*-REVIEW-ADJUDICATION.md`, rows-as-dispositions, no bare form.
   `sed -n '105,118p' adversarial-review-prompt/SKILL.md` → "Check
   `<phase-dir>/*-REVIEW-ADJUDICATION.md` first — its rows *are* the dispositions";
   `sed -n '124,138p' …/references/prompt-template.md` → "sourced from
   `<phase-dir>/*-REVIEW-ADJUDICATION.md` where one exists; its rows are the dispositions."
   As expected. No mention of ruled auxiliary entries or the bare filename.
2. **The reviewer's discovery command (finding 3).** Expected: empty.
   `find ~/.claude/skills/review-adjudication -maxdepth 1 -type f -name
   '*-REVIEW-ADJUDICATION.md' -print` → empty (exit 0). Reviewer's output reproduces exactly; the
   glob's literal hyphen cannot match `REVIEW-ADJUDICATION.md`, the only ledger this skill has
   produced.
3. **Line counts (reviewer figure check).** Expected 261/160/316/336/468/416/294. `wc -l` on
   `SKILL.md`, `ledger-template.md`, sibling `SKILL.md`, sibling `prompt-template.md`, round-1
   brief/report/ledger → 261/160/316/336/468/416/294. All seven reproduce exactly; 103.5 report =
   129 and its brief = 577, both as the reviewer stated.
4. **Non-VCS target (finding 8).** Expected: fatal. `git -C ~/.claude status` →
   `fatal: not a git repository (or any of the parent directories): .git`. Reproduces verbatim.
5. **103.5 auxiliary populations (findings 2, 4).** Expected: 5 CNV entries incl. two "partially
   verified only", 4 disagreement bullets. `sed -n '110,129p' 103.5-EXTERNAL-REVIEW.md` → CNV: A2,
   A4 ("could not determine"), C16, C17 ("partially verified only"), plus the eleven-item future-
   UAT entry; "Disagreements with the internal review": exactly 4 bullets. As stated.
6. **107 two-report trigger (finding 4).** Expected: ledger names one report; code-review report
   holds 3 ranked findings. `sed -n '1,6p' 107-REVIEW-ADJUDICATION.md` → header names
   `107-EXTERNAL-REVIEW.md` only; `sed -n '298,340p' 107-EXTERNAL-CODE-REVIEW.md | grep '###'` →
   3 ranked findings. Both as stated.
7. **CNV-R2-6 spot-check (finding 4's consequence).** Expected (reviewer left open): titles might
   be dispositioned elsewhere. `grep -rl` for each of the three 107 code-review finding titles
   across `.planning` → each appears **only** in `107-EXTERNAL-CODE-REVIEW.md`. No adjudication
   record exists for that report anywhere; a differently-worded disposition remains formally
   unexcluded but nothing was found.
8. **Round-1 row state (finding 1).** Direct full read of this ledger: rows 1–6, 8–14 read
   `FIX NOW` (`:124-137`); row 7 reads `PENDING OWNER — proposed:` (`:130`); §5 records adoption
   and same-day execution of all 13 (`:233-243`); §6 is headed "all executed" (`:245`). The
   reviewer's trigger reproduces against the authoritative table.

⚠ **Against expectation — skill-firing data (bears on CNV-R2-1):** this session was **not** invoked
by skill name. The user announced "external review … has landed" with a path; the skill was
selected from its `description:` alone — the first observed description-driven firing, and it
selected correctly with no collision among 73 skills. Both prior runs were explicit invocations.

**Hygiene (SKILL.md:167-170, applied as writable):** the only file this session writes is this
ledger. `~/.claude` has no tree to report clean — finding 8 fired live (P-R2-3); file-level check
substituted: directory listing shows no other new/modified file. The corpus repo was touched
read-only: `git status --porcelain` matches the session-start snapshot (four pre-existing untracked
`.planning` paths, none modified).

## 3. Adjudication

Reviewer-assigned impacts frozen at enumeration. No verdict is REFUTED, so the high-impact
execution-evidence escalation gate was not triggered. No `SETTLED ALREADY` was available: the
round-1 ledger is the only durable decision record, and none of its rulings locks the composition
behaviors these findings attack (see Corrections — the reviewer's disagreements with round 1 were
themselves adjudicated, not presumed).

| # | Finding (title, verbatim) | Impact | Class | Verdict | Disposition |
|---|---------------------------|--------|-------|---------|-------------|
| 1 | "Complete" freezes provisional rows before the required backfill | high | false record in the ledger / internal contradiction | **CONFIRMED** — `SKILL.md:77-81` (complete = any nonempty cells; complete = never edit) vs `:249-251` (whoever lands a fix "updates that row") vs `ledger-template.md:126-127` ("Backfill each row"); the round-1 table exhibits the exact false state (§2 check 8), and this Round 2 append cannot legally repair those rows (P-R2-2) | **FIX NOW** — define round closure over obligations, not cell presence: all auxiliary entries ruled, no unresolved `PENDING OWNER`, no blocking `VERIFY`, every executed `FIX NOW` backfilled into its row; state/evidence backfill legal until closure; after closure, superseding rows only. **✔ executed 2026-08-10, `ebd7947`** |
| 2 | `VERIFY` does not reach the could-not-verify population it was added to protect | high | lost finding / broken contract | **CONFIRMED** — `SKILL.md:97-108` routes CNV to a block; the two-axis schema and no-empty-cell gate (`:235-238`) cover numbered rows only; template CNV block (`ledger-template.md:87-90`) asks three prose questions, no verdict/disposition; sibling reads "rows"; trigger real (103.5's five entries, §2 check 5); round 1's own CNV-1 sits "still open" outside any table | **FIX NOW** — CNV entries get stable IDs + Verdict/Disposition cells (incl. `VERIFY`) in their block; closure check covers them; sibling line widened to ruled auxiliary entries (cross-file). **✔ executed 2026-08-10, `ebd7947`** |
| 3 | The sibling cannot discover the standalone ledger this skill writes | high | broken contract / lost finding | **CONFIRMED** — writer publishes two shapes (`SKILL.md:222-225`); both sibling lines glob `*-REVIEW-ADJUDICATION.md` (§2 check 1); the literal hyphen cannot match this very file, and the reviewer's find reproduces empty (§2 check 2) | **FIX NOW** (cross-file, sibling, flagged for owner visibility like round 1's F5) — both sibling lines show both literal patterns: `NN-REVIEW-ADJUDICATION.md` and bare `REVIEW-ADJUDICATION.md` beside each report. **✔ executed 2026-08-10, `ebd7947`** |
| 4 | The worked template can still hide an entire discovered report | high | lost finding / false record in the ledger | **CONFIRMED (partial)** — template headers (`ledger-template.md:14-24`, `:145-152`) verified pre-amendment: singular `Review:`, counts without census or `+D` slot, no prior-internal-review block; corpus trigger verified (107: two reports, ledger names one, 3 code-review findings rowless anywhere — §2 checks 6, 7); fired live on this round's header (P-R2-1). Unestablished part: whether a model follows body over template — one data point now exists (this run followed the body, P-R2-1), not generality | **FIX NOW** — `Reports found:` census line with per-report adjudication status in both template headers; count grammar (body `:108` + template) gains `+D prior-review disagreements`; template gains the prior-internal-review disagreement block. **✔ executed 2026-08-10, `ebd7947`** |
| 5 | Pasted reviews require a report write that the amended envelope forbids | medium | internal contradiction / lost finding | **CONFIRMED (partial)** — contradiction textually exact: `SKILL.md:69-71` ("write it to disk first") vs `:233` ("only files … are the ledger and `FIX LATER` backlog artifacts — never … the review"); corpus confirms the input shape (105's transcript-shaped review). Unestablished: how a model resolves it — no chat-only run exists | **FIX NOW** — envelope admits the one write: "a report file materialized from a chat-only input, saved beside the ledger before adjudication begins". **✔ executed 2026-08-10, `ebd7947`** |
| 6 | The interrupted-skeleton exception is contradicted by the template's absolute no-edit rule | medium | lost finding / internal contradiction | **CONFIRMED (partial)** — conflict exact: `SKILL.md:77-81` (fill incomplete round in place) vs `ledger-template.md:143` ("never edits what is already there", unqualified). Unestablished: the loss event — no interrupted skeleton exists | **FIX NOW** — mirror the completed-rounds scope into the template's round-append rule. **✔ executed 2026-08-10, `ebd7947`** |
| 7 | F12's "copy the row" shortcut still permits content-free deferral | medium | unenforceable rule / lost finding | **CONFIRMED (partial)** — schema proof verified: `SKILL.md:201` requires Location/Mechanism/Consequence then blesses row-copy; the row schema (`ledger-template.md:60-68`) and template row 5 carry none of the three fields. Unestablished: no post-amendment `FIX LATER` pair exists to exhibit the drop | **FIX NOW** — delete "copying the row into it is enough"; require the three explicitly labeled fields present in the artifact before `FIX LATER` is accepted. **✔ executed 2026-08-10, `ebd7947`** |
| 8 | F10 requires a clean-tree report where no tree exists | low | unenforceable rule / invalid assumption | **CONFIRMED** — `git -C ~/.claude status` → fatal, reproduced verbatim (§2 check 4); `SKILL.md:170` and the template's commit backfill (`:126-127`) have no non-VCS branch; fired live this run (P-R2-3, hygiene reported at file level instead) | **FIX NOW** — VCS branch (status/commit) and non-VCS branch (dated changed-path note + file-level listing) for both the cleanliness report and the backfill reference. **✔ executed 2026-08-10, `ebd7947`** |

### Process and prompt defects

The reviewer reported none (+0), and none surfaced here against the brief. This run's own live
observations, recorded per round-1 convention:

- **P-R2-1 — finding 4 fired live:** this round's header required an invented `+7 round-1
  disagreement items` slot; the body was followed over the template at the conflict.
- **P-R2-2 — finding 1 fired live:** rows 1–14 of Round 1 could not legally be backfilled by this
  session (completed rounds are append-only); execution status lives in Round 1 §5/§6 prose and the
  Corrections block below — the false table state the finding describes persists *by rule* until
  the R2-F1 amendment lands. *(It landed as `ebd7947`; the obligation is discharged by the
  "Round 1 execution backfill" block below.)*
- **P-R2-3 — finding 8 fired live:** no tree exists to report clean; file-level substitute used.
- **P-R2-4 — first description-driven firing observed** (⚠ in §2): bears on CNV-R2-1.
- **P-R2-5 — ordering deviation, recorded:** enumeration (8 + 7 + 7, IDs and titles) preceded all
  rulings in-session, but the skeleton was never written to disk as a separate act — this append
  landed complete. A deviation from step 2's write-early letter, not from its no-dropped-rows
  purpose (count gate enforced below); noted rather than laundered.

### Reviewer's could-not-verify items

- **CNV-R2-1 — unprompted firing untested:** partially settled *by this run* — one correct
  description-driven selection (P-R2-4). The over-firing half remains open. Does not block.
- **CNV-R2-2 — no post-amendment run existed:** this run is the first; it supplied one
  body-over-template data point (P-R2-1) and two more live confirmations (P-R2-2, P-R2-3). The
  general behavioral question stays open. Does not block.
- **CNV-R2-3 — no interrupted-skeleton or post-amendment FIX LATER pair exists:** still open;
  round 1's reasoning holds — the fixes are one-liners, cheaper than waiting for an occurrence.
  Does not block.
- **CNV-R2-4 — no git history under `~/.claude`:** permanent for the past amendments; the
  forward-looking remedy is owner question Q3. Does not block.
- **CNV-R2-5 — application findings not re-adjudicated; not every report body read:** acceptable —
  outside the brief's scope; the load-bearing triggers were independently re-verified here (§2).
- **CNV-R2-6 — a re-worded 107 disposition not excluded:** spot-checked here (§2 check 7): the
  three titles appear only in their own report and no adjudication artifact for it exists. Residual
  uncertainty acceptable; it bears on finding 4's consequence weight, not its mechanism. Does not
  block.
- **CNV-R2-7 — no product tests or mutations run:** acceptable — the brief authorized read-only
  inspection, and no ruling above needed more than read-only reproduction.

### Corrections to earlier rounds (the reviewer's 7 disagreements, each ruled)

Round-1 *verdicts* all stand. What Round 2 corrects is the round-1 session's fix-verification and
§6's "all executed" gloss — which must now be read as "executed; seven incompletely or with a new
path opened." Original rows stay as written; these entries supersede the statements they name.

- **D-1** (supersedes R1 row 2's fix-adequacy): **CONFIRMED** — F2 closed the numbered-row hole
  only; the CNV population named by the finding never enters the table. Carried by finding 2.
- **D-2** (supersedes R1 rows 3, 4, 6 "landed" status): **CONFIRMED** — fixes landed in `SKILL.md`
  but not the template; verification stopped one file early. Carried by findings 4 and 6.
- **D-3** (supersedes R1 row 5's closure claim): **CONFIRMED** — F5 and P-5 were never checked in
  composition; the sibling glob cannot match P-5's filename. Carried by finding 3.
- **D-4** (supersedes R1 §5's supersede-by-note method): **CONFIRMED** — "the original row stays as
  written" and "whoever executes updates the row" are incompatible as written. Carried by finding 1.
- **D-5** (supersedes R1 row 12's fix-adequacy): **CONFIRMED** — the F12 amendment asserted the row
  carries fields the schema provably lacks. Carried by finding 7.
- **D-6** (supersedes R1 row 10's fix-adequacy): **CONFIRMED** — F10 was verified as repository
  hygiene only, while the run verifying it was itself on a non-VCS target. Carried by finding 8.
- **D-7** (supersedes R1 row 14's fix-adequacy): **CONFIRMED** — the F14 ruling missed the
  pre-existing chat-materialization instruction; the amendment made the contradiction absolute.
  Carried by finding 5.

**Did any round-1 fix open a new path to the failure it closed?** Yes, three: F1 + F6 + the bridge
compose into the closure/backfill contradiction (finding 1); F14 turned an existing instruction
into a forbidden write (finding 5); F5 + P-5 compose into a reader/writer mismatch (finding 3).
Holding cleanly: F8, F9 (Major-label seam noted, not elevated), F11, F13, P-7, and the bridge's
act-separation itself (reviewer claim 15 upheld).

### Round 1 execution backfill (legal under R2-F1 as of `ebd7947`; supersedes the stale row state, original rows stay as written)

- **R1 rows 1–6, 8–14** (`FIX NOW`): executed 2026-08-10, same session, per D-R1-1 — before the
  repository existed, so no commits; the dated record is Round 1 §5–§6. Round 2 findings 1–8
  establish that seven of those thirteen fixes were incomplete or opened a new path; the
  completing amendments are commit `ebd7947`.
- **R1 row 7** (`PENDING OWNER — proposed: adopt the recorded-acceptance bridge`): resolved
  2026-08-10 by D-R1-1 — proposal adopted, bridge codified in `SKILL.md` step 8.

## 4. Owner decisions required

### Q3 — Put the skills directory under version control?

**What turns on it:** whether future amendment rounds have commit-level history — fix commits as
backfill references, diffable amendments, a reconstructable sequence. Two CNV categories and half
of finding 8 exist only because `~/.claude` has no repository. The R2-F8 fix adds a non-VCS branch
regardless; this decides whether that branch is the permanent normal or a rarely-used fallback.
**Options:**
- **A — a plain local git repo at `~/.claude/skills` (recommended):** no remote, linear commits
  only. One-time setup; every future ledger backfill gets a real reference; retires CNV-R2-4's
  class permanently.
- **B — stay without version control:** zero setup; dated ledger notes remain the only record, and
  every future audit repeats the "cannot reconstruct pre/post bytes" gap.
**Recommendation:** A — cheap, local-only, and it converts finding 8's fallback branch into the
exception it should be.
**Blocks:** nothing in this round's queue.

## 5. Locked owner decisions from this round

**D-R2-1 — owner, 2026-08-10:** *"ok go"* — given in response to the hand-off that presented
(a) the 8-item queue with third-touch flags on R2-F1/R2-F2 and (b) Q3 with recommendation A. Read
as accepting both, and that interpretation is recorded rather than assumed: the queue execution is
sanctioned (this acceptance is the bridge's separate, explicit act), and Q3 option A is enacted —
a **local-only** git repository initialized at `~/.claude/skills` (no remote, reversible by
deleting `.git/`). Baseline commit `0e1f808` captures the pre-amendment state; the amendments are
commit `ebd7947`.

## 6. Amendments required (the Round 2 FIX NOW queue — 8 items, **all executed 2026-08-10,
commit `ebd7947`**, per D-R2-1)

Executed under the bridge after the owner's recorded acceptance (D-R2-1). Items R2-F1 and R2-F2
modified rules the round-1 amendments already moved once — flagged as third-touch territory in
the hand-off, and the acceptance covered them.

1. **R2-F1** (finding 1) — `SKILL.md:77-81`, `:247-251`; `ledger-template.md:112-127`, `:154-158`:
   closure defined over obligations (all auxiliary entries ruled, no unresolved `PENDING OWNER`,
   no blocking `VERIFY`, executed items backfilled); backfill legal until closure; superseding rows
   after. *(third-touch)*
2. **R2-F2** (finding 2) — `SKILL.md:97-108` + template CNV block + sibling line (cross-file):
   CNV entries get IDs and two-axis cells incl. `VERIFY`; closure covers them; sibling reads ruled
   auxiliary entries. *(third-touch)*
3. **R2-F3** (finding 3) — *sibling* `SKILL.md:111` + `prompt-template.md:130` (cross-file): both
   literal ledger filename patterns shown.
4. **R2-F4** (finding 4) — `ledger-template.md:14-24`, `:145-152` + `SKILL.md:108`: `Reports
   found:` census with per-report status in both headers; `+D prior-review disagreements` count
   slot; prior-internal-review disagreement block added to the template.
5. **R2-F5** (finding 5) — `SKILL.md:233`: envelope exception for a report file materialized from
   chat-only input, fixed destination beside the ledger.
6. **R2-F6** (finding 6) — `ledger-template.md:143`: never-edit scoped to completed rounds,
   mirroring `SKILL.md:77-81`.
7. **R2-F7** (finding 7) — `SKILL.md:201`: remove the row-copy shortcut; require the three labeled
   fields verified present.
8. **R2-F8** (finding 8) — `SKILL.md:167-170` + `ledger-template.md:126-127`: VCS and non-VCS
   branches for cleanliness reporting and backfill references.

## 7. Claims examined and upheld

Coverage: 22/22 §6 claims engaged. Upheld outright: claim 2 (de-minimis case expressible via
`ACCEPTED AS-IS` / `PENDING OWNER — proposed`), claim 5 (`CONFIRMED (partial)` carries its
distinction in the verdict cell), claim 6 (discovery selects all ten corpus reports; `-RESPONSE`
correctly excluded — verified by the reviewer via full read of the 105 response), claim 15 (the
bridge preserves the act boundary; no coercive-offer evidence). Upheld with noted seams: claim 9
(Major/Minor labels unmapped to the high/critical gate — not elevated, general step-5 duty
applies), claim 13 (envelope binds except the finding-5 contradiction), claim 21 (ceremony growth
is a cost, not a correctness defect — no proportionality valve added, consistent with round 1's
ruling). Figure-reproduction record after independent re-run: **every figure reproduced exactly**
(seven wc counts + two more, the empty find, the git fatal verbatim, the 103.5 composition
8 findings/1 bookkeeping defect/5 CNV/4 disagreements, the 107 composition). A perfect record —
the report's THEORETICAL and SELF-REPORT claims earn above-default weight, the same standard
round 1 applied to Fable's near-perfect record.

## 8. What this round could not settle, and why that is acceptable

- **Template-vs-body obedience in general** — one data point now exists (this run, body). The
  R2-F4/R2-F6 fixes remove the conflicts rather than betting on obedience; cheaper than testing.
- **Interrupted-skeleton behavior and FIX LATER laundering in practice** — still unobserved;
  fixes are one-liners (same ruling as round 1).
- **Over-firing of the description** — one correct firing observed (P-R2-4); the collision half
  waits for organic future invocations, free to collect.
- **The round-1 rows' stale state** — persists by rule until R2-F1 lands and redefines closure;
  recorded in P-R2-2 and the Corrections block rather than repaired in place. Whoever executes
  this round's queue must backfill *this* round's rows — and, once R2-F1 makes it legal, add the
  execution-status rows for Round 1.

This Round 2 feeds the next brief's "ground already walked": findings R2-1…8 and their
dispositions are covered ground — and whether the next brief can *find* this file at all is
exactly R2-F3.
