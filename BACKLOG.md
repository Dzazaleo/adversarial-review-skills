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
