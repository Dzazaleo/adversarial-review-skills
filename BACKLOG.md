# Backlog

Deferred work with a recorded origin. Each entry carries the finding's **Location**, **Mechanism**
and **Consequence** copied from the report that raised it, so the item can be picked up without
re-reading the review.

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
