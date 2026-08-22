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

**Status, 2026-08-22 — `scripts/validate.py` exists and covers ten of these.** Written after round
4, which found several defects a script would have caught in milliseconds. It checks: frontmatter
parses and declares the required keys; no write-capable tool is pre-approved; `SKILL.md` stays
under the documented 500 lines; no unresolved `«»` ships in a `SKILL.md`; every relative
`references/` link resolves; no unescaped `|` sits inside a ledger table cell; every verdict in the
current round carries a disposition; `NO ACTION` appears only under `REFUTED` or `SETTLED ALREADY`
and no bare `ACCEPTED` appears at all; the current round's findings-in equals its rows-out; and
every filed calibration record's digest matches the instrument. Closed rounds are append-only, so
defects there are reported as warnings rather than errors.

**Each of the ten was break-tested** — mutated in a throwaway copy to confirm it fails when its
invariant is broken, because a check that cannot fail is the defect this repository keeps finding.
9/9 mutations were caught; the tenth check (installed copies match the repository) is a warning by
design.

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
