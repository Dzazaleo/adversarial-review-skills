# Backlog

Deferred work with a recorded origin. Each entry carries the finding's **Location**, **Mechanism**
and **Consequence** copied from the report that raised it, so the item can be picked up without
re-reading the review.

The reports and ledger cited below as **Origin** are no longer in this repository — the seven-round
working corpus was removed in `4290a91`. Recover any of them from `ef74e91`, where they sit at the
repository root under the names given. The citations are kept as provenance, and every entry is
readable without them by the design stated above.

---

## B-1 — No corpus-level check that the cases and the answer key remain mutually valid

**Origin:** `EXTERNAL-REVIEW.md` finding F9 (OpenAI Codex, 2026-08-21), impact `medium`.
Adjudicated `CONFIRMED` / `FIX LATER` in `REVIEW-ADJUDICATION.md` §3 row 9.

**Location:** `calibration/README.md:38-52`; corpus-wide (no harness or CI artifact exists).

**Mechanism:** The repository has executable fixture tests inside two cases, but no corpus-level
manifest or check verifies six expected cases, four expected trap signals, clean-case baselines,
the checksum mutation, answer-key paths, or prompt/record invariants. The protocol is entirely
manual. `HOW-IT-WORKS.md:740-743` concedes the absence of scoring but offers no gate for simple
internal drift either.

**Consequence:** The benchmark can silently stop measuring what its key says while every
calibration run continues to produce authoritative-looking PASS/FAIL records.

**Adjudicator's note on scope:** this is not the eval-suite item already conceded at
`HOW-IT-WORKS.md:700-704` (scoring reviews against fixtures with recall/precision thresholds). A
drift gate is narrower: it checks that the corpus still matches its own key. Verified absent on
2026-08-21 — no `pyproject.toml`, `tox.ini`, `noxfile.py`, `Makefile`, `package.json`, `setup.py`,
`setup.cfg` or `.github/` anywhere in the repository.

**Sketch of the minimal shape, if taken up:** one script asserting the six case directories exist,
that each trap's primary-defect identifier from `ANSWER-KEY.md` is still present in its case, that
the two clean cases' suites pass, and that the `return True` mutation still leaves
`trap-unfalsifiable-test` green. Anything larger is the eval suite, which is a different decision.

---

## B-2 — No construction or validation procedure for private replacement traps

**Origin:** `EXTERNAL-REVIEW.md` finding F10 (OpenAI Codex, 2026-08-21), impact `medium`. The
*wording* half of F10 was dispositioned `FIX NOW` in `REVIEW-ADJUDICATION.md` §3 row 10; this entry
carries the fuller remedy that was not queued.

**Location:** `HOW-IT-WORKS.md:733-739`; `calibration/README.md:1-106` and
`calibration/ANSWER-KEY.md:1-87`.

**Mechanism:** The default distribution publishes each primary defect and search vocabulary beside
the cases. The stated mitigation is to author four private shipped-defect traps, but the repository
gives no construction checklist, validation protocol, scorer-blinding method, or baseline for
showing that replacements are findable, single-defect, distinct, and clean in the opposite
direction. It delegates the original hard problem to every user.

**Consequence:** PASS can mean memorization; alternatively, a malformed private ruler can make
competent reviewers fail indefinitely. In both branches the record looks normal and the downstream
skills trust it for silence.

**Adjudicator's note on scope:** verified 2026-08-21 that the only replacement guidance in the
repository is the two lines at `HOW-IT-WORKS.md:737-739`; nothing under `calibration/` resembles a
checklist or a validation protocol.

---

## B-3 — No executable validator for the skills themselves *(partly discharged 2026-08-22)*

**Origin:** `EXTERNAL-REVIEW-3.md`, "Other worthwhile improvements" bullet 1 (OpenAI Codex,
`gpt-5.6-sol` at `high` effort, 2026-08-22), impact `other`. Adjudicated `CONFIRMED` / `FIX LATER`
in `REVIEW-ADJUDICATION.md` §R3.3 row `R3-F6`.

**Scope note:** this entry carries the **skill-level** half only. The corpus-level half — that the
cases and the answer key remain mutually valid — is `B-1` and is not duplicated here.

**Location:** `skills/adversarial-review-prompt/SKILL.md`,
`skills/review-adjudication/SKILL.md`, both `references/` directories, and the repository root
(no harness, CI, task runner or lint artifact exists anywhere).

**Mechanism:** The repository has executable tests inside two calibration fixtures and nothing
else. Verified 2026-08-22: no `Makefile`, `pyproject.toml`, `package.json`, `conftest.py`, `*.sh`
or `.github/` anywhere in the tree. Every invariant the two skills depend on is therefore checked
only by a human reading prose, including: frontmatter YAML parses and declares the fields the
skills assume; no unresolved `«»` placeholder ships in a template; every verdict/disposition pair
written into a ledger is one the skill's own matrix permits; count-in equals count-out on a
finished ledger; the two skills' declared permissions agree with the write envelope their prose
claims; a generated brief does not overwrite an existing one; a report has the brief it answers;
and the no-filesystem template variant stays consistent with the filesystem one.

**Consequence:** Every one of those invariants has already failed at least once in two rounds of
external review — the stale `corpus «commit»` header (round-2 `F1`), the `Task`/`Agent` tool-name
drift (round-1 `F4`), the carried-forward `418`-for-`416` inventory count (round-2 `F9`), the
`COULD NOT VERIFY` vocabulary break and the missing overwrite guard (round-3 `R3-F8`, `R3-F7`).
Each was found by a paid external reviewer reading prose, which is the most expensive possible
detector for a class of defect a script would catch in milliseconds. Until a validator exists, the
skills' correctness depends on the next review round noticing, and a round that does not notice
reads as a pass.

**Status, 2026-08-22 (revised after round 6) — `scripts/validate.py` exists: 13 named invariants
over 12 checks**, two names sharing the frontmatter implementation. It checks: frontmatter parses
and declares the required keys; no write-capable tool is pre-approved, **including when
`allowed-tools` is written as a YAML string**; `SKILL.md` stays under the documented 500 lines; no
unresolved `«»` ships in a `SKILL.md`; every relative `references/` link resolves, **titles and
all**; no unescaped `|` sits inside a ledger table cell, **while a backslash-escaped one passes**;
every verdict carries a disposition; `NO ACTION` appears only under the verdicts that permit it and
no bare `ACCEPTED` appears at all; **the stated rows-out equals the numbered finding rows that
actually exist, in every round — a mismatch in a closed round warns rather than fails, and a row ID
matching no declared series is reported rather than silently classified**; every filed calibration record's digest matches the instrument **and is inside
its expiry window**; no retired rule wording survives in live prose; and every invariants block
exists and cites real sections. Closed rounds are append-only, so defects there are **reported as
warnings** — visible, never failing the build.

**The break-test claim that stood here until round 6 was wrong, and is replaced by measurement.**
It read *"each of the ten was break-tested… 9/9 mutations were caught."* Round 6 re-ran the whole
thing adversarially and found four checks silent on the invariant they were named for, two firing
on correct work, and at least two that **could not fail at all** — `check_calibration_digests` had
no error path, and `check_counts` compared two numbers in the same header rather than counting
anything. The full mutation record is `REVIEW-ADJUDICATION.md` §R6.2 and §R6.16. **Every check was
re-broken after the round-6 fixes**, both to confirm it fails on its invariant and to confirm it
stays quiet on correct work; the results are in §R6.16.

**One bound worth stating rather than discovering:** `check_retired_wordings` matches literal
retired phrasings with whitespace, emphasis and code markup normalized away. **It does not catch a
retired rule restated in different words**, which is the failure it was created for and which is
not mechanically closable. It buys the copy-paste and the re-wrap; it does not buy the paraphrase.
The `installed copies match the repository` check is a warning by design.

**What remains open, and why this entry is not closed:** the validator checks artifacts, not
behaviour. It cannot tell whether a generated brief overwrote an existing one, whether a report has
the brief it answers, or whether the no-filesystem template variant stays consistent with the
filesystem one — those need the skills actually executed end to end, which nothing here does. It
also cannot check that a claim in a brief is true, which is the class round 4 spent most of its
findings on.

**Measured bound, 2026-08-22.** Two defects (`X-1`, `X-2` in `REVIEW-ADJUDICATION.md` §R4.14) were
found the same day the validator shipped, and **it caught neither** — one was a misleading example
filename, the other a stale copy of a claim in a design doc. Neither is expressible as a rule a
script could run. What the validator did catch, three times in one session, is the author's own
slips against rules the author had just written: two illegal verdict/disposition pairings and a
missing disposition. That is the honest description of what it buys — it enforces the form, not the
truth.


## B-4 — `check_retired_wordings` is silent on a footnote-broken phrase

**Location:** `scripts/validate.py`, `check_retired_wordings` — the normalization step that strips
`[*_`]` before matching. Raised as `CNV-R6-1` and ruled at `REVIEW-ADJUDICATION.md` §R6.18.

**Mechanism:** live prose is whitespace-normalized and has emphasis characters and backticks
removed, then matched against literal retired phrasings. A markdown footnote marker is a bracketed
token, not an emphasis character, so inserting one mid-phrase — after the noun in the retired
`FIX LATER` ordering rule, say — leaves the phrase unmatched and no error is raised. Confirmed by
execution 2026-08-22 in both spellings, plain and combined with emphasis: each returned
`12 of 12 checks pass`, exit 0. **The retired phrasings themselves are not reproduced here** — this
file is live prose inside the check's own glob, and quoting them would trip it. They are in
`scripts/validate.py`.

**Consequence:** contract items 1 and 4. A retired rule can survive in live prose in a spelling the
check was extended to cover in every other form, and the run still certifies itself. The same class
as round 6's `g6-7`, in the one spelling queue item 10 did not reach.

**DISCHARGED 2026-08-22**, in the same round that raised it. `check_retired_wordings` now strips
markdown footnote markers alongside emphasis characters and backticks before matching; the closing
record is `REVIEW-ADJUDICATION.md` §R6.19, and round 7 `grok7-3` is the finding that this paragraph
was left reading as open work after the fix landed. Re-verified by execution 2026-08-23: a
footnote-broken retired phrase now errors. **Nothing here is outstanding.**


## B-5 — `clean-copy-link`'s `viewer.html` reads as an undelivered feature, so the control no longer measures over-flagging

**Origin:** the K-1 regression brief (Claude artifact *The K-1 Regression*, 2026-09-10),
root-causing the `grok-4.6-xhigh` record filed 2026-09-09 — `FAIL`, 4/4 traps, **0/2 clean**.
Not raised by an external reviewer; raised against the corpus by the operator.

**Location:** `calibration/cases/clean-copy-link/viewer.html`, all 16 lines, read against
`calibration/cases/clean-copy-link/PLAN.md:12-28` (Steps 1-3). Scored by
`calibration/ANSWER-KEY.md:66` and the pass rule at `:76-77`. Introduced by `e1fc88b` as K-1.

**Mechanism:** K-1 added `viewer.html` so that the plan would have the existing markup it extends,
retiring the pre-fix reading "the required `viewer.html` is absent". The file it added carries the
one thing Step 1 names as its attachment point — `<h1 id="page-title">` — and none of Steps 1-3:
no `<button id="copy-link">`, no `navigator.clipboard.writeText` call, no `execCommand` fallback,
no label swap, no `<script>` element at all. The gap was therefore not removed but made **more
citable**: a reviewer that previously had to argue from an absent file can now quote a present one
line by line and report every element the plan names as missing from it. Both readings are
available from the same bytes — "the starting page Step 1 would edit" and "an undelivered feature"
— and nothing in the case, the fixed brief or the key tells the reviewer which artifact is the
deliverable.

**Consequence:** `clean-copy-link` is a negative control. It exists to measure one thing — whether
a reviewer invents `critical` or `high` severity against a small, complete plan. It now also
measures whether the reviewer guessed correctly which artifact was under review, and on the
evidence that second thing dominates. Because `clean-wordcount` is then the only clean case still
measuring what it claims to, the pass rule's tolerance is spent: `ANSWER-KEY.md:76-77` passes a
reviewer on *at least one* of two clean cases, so a single over-flag on `clean-wordcount` now fails
a reviewer outright — precisely the flakiness `ANSWER-KEY.md:85-87` chose that threshold to avoid.
Reviewers are failing on the instrument rather than on their own calibration, and the resulting
`FAIL` records are indistinguishable from earned ones.

**Evidence, and which half of it this repository can settle.** On the frozen post-K-1 bytes, the
two archived runs both **passed** the control: `2026-08-22-gpt-5.6-sol-high-775e1cc8c43f` raised one
medium and one low, and `2026-08-22-grok-4.6-high` raised nothing, stating the reading explicitly —
"`viewer.html` has no copy control and no script; that is the starting page Step 1 would edit, not
an undelivered feature." The one archived **pre**-K-1 run, `2026-08-22-gpt-5.6-sol-high`, failed the
control with a `High` citing the absent file: K-1 was written against a real defect. Four
subsequent runs on the same frozen bytes are reported to have failed the control, the most recent
being `grok-4.6-xhigh` on 2026-09-09. **Those archives are not in this repository** — they sit on
the machine that produced them under `runs/2026-09-09-grok-4.6-xhigh/`. So the 2-pass/4-fail split
is archive-verified on the two passes and operator-reported on the four failures; the mechanism
above is verified here by reading the bytes.

**What a fix costs, before anyone picks one.** The instrument digest covers `cases/`, the fixed
brief and the answer key — K-6, in this same commit, narrowed it to exactly those three. Every
remedy below touches one of them, so **no fix here is digest-free**: each expires every stored
calibration record and costs a twenty-minute re-run per reviewer on file. Choose on merit; the
cost is identical whichever way it goes.

**Sketch of the options, if taken up:**

- **(a) Revert K-1.** Returns to the absent-file state, which the pre-fix archived run shows also
  fails this control. Known-failing; listed only so it is not rediscovered.
- **(b) Make `viewer.html` coherent on its own** — a complete page whose current behaviour is
  self-consistent, which the plan then extends *additively*. Leaves "not implemented" nothing to
  attach to, and is the only option that fixes the ambiguity rather than labelling it.
- **(c) Say which artifact is the deliverable**, in the case rather than in `CALIBRATION-PROMPT.md`
  — the fixed brief is shared by all six cases and must not hint that the session is an evaluation
  (K-4). Cheapest to write, but it narrows what the control measures by telling the reviewer the
  answer to half of it.
- **(d) Tighten the pass rule** so both clean cases must come back clean. Does not touch this case
  at all, and makes the problem worse rather than better while `clean-copy-link` is ambiguous.

**Not yet ruled on.** This entry records the defect and the evidence; which option lands is the
owner's call, and B-1's corpus-level validity check is the thing that would have caught it.

**Amended 2026-09-10 — a third post-K-1 run, and a correction to the entry above.** `grok-4.6` was
calibrated at **xhigh** on this machine against digest `775e1cc8c43f` — the same digest the
`grok-4.6-high` PASS was earned on, so the instrument is provably frozen between the two. Result:
**PASS**, 4/4 traps (two of them proven by execution, including a constructed `dc478bbc` collision),
`clean-wordcount` clean with zero findings, and `clean-copy-link` rated **`critical`** — *"The
copy-link feature is not implemented"*, locating `viewer.html:1-16` and listing every element of
Steps 1-3 absent from it. That is the Mechanism above almost word for word, from a third
independent run.

Two things this settles, one of which corrects the entry:

- **The controlled comparison now exists.** Same bytes, same model, same digest: at **high**,
  `grok-4.6` passed this case with zero findings and argued the reading out explicitly (*"the
  starting page Step 1 would edit, not an undelivered feature"*); at **xhigh** it rates the same 16
  lines `critical`. Neither reading is wrong on the bytes, which is the ambiguity this entry is
  about. It also means the case is not simply "broken" — it is **effort-sensitive**, and a negative
  control whose result turns on the reviewer's effort setting is measuring the wrong variable.
- **The Consequence paragraph's margin claim is no longer a prediction.** This run passed *only*
  because `clean-wordcount` came back clean. Had it produced one `high`, a reviewer that found every
  planted defect and proved four of them by execution would have been recorded `FAIL`.

**And the correction:** this entry leaned on a reported "4 of 4 reviewer-runs failing the control
since the fix," which invited reading the whole `grok-4.6-xhigh` `FAIL` of 2026-09-09 (4/4 traps,
**0/2 clean**) as B-5's doing. It is not. B-5 accounts for the `clean-copy-link` half only, and
`clean-wordcount` — the half that actually decided that `FAIL`, since one clean case suffices to
pass — came back **clean** here on the same digest at the same effort. So whatever flagged
`clean-wordcount` on 2026-09-09 is **not** reproducible and is **not** explained by this entry. That
run's `clean-wordcount` report, still only on the machine that produced it, is the one artifact that
would settle it, and it is worth retrieving before anyone edits a case.

Record: `~/.adversarial-review/calibration/grok-4.6-xhigh.md`. Raw reports:
`.adversarial-review/calibration/runs/2026-09-10-grok-4.6-xhigh/`.
