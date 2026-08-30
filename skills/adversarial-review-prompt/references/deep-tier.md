# The deep tier — what `--deep` adds

**Loaded only on a deep run.** `SKILL.md` carries the light protocol whole and stubs this in place,
so a light brief never pays for this file. The `D` number is the stub label; the `§` in the heading
is the `SKILL.md` section the piece belongs to.

The tier is decided in `SKILL.md` §1: a one-way door, a disputed high-severity finding, or a
reviewer/author disagreement worth arbitrating. Deep adds one thing to this skill and it is below.
Everything else in `SKILL.md` is the light path and runs either way.

---

## D1 · §1 — calibration: digest, precedence, workload

Light reads two fields, result and expiry, and reports one line. Deep adds three checks, and each
must be run exactly as written — the whole reason they sit in a file of their own rather than as a
sentence in the skill.

**Recompute the corpus digest** with the command the record names, unmodified, and compare. It is
the only check that notices the instrument moving, and one adjusted until it matches is not a
check. Without the corpus, staleness is **unknowable**, not passed.

**A mismatch is not by itself proof the corpus moved.** Rule out three properties of the *machine*
first — collation (`LC_ALL=C`), `shasum`'s output mode (`-t`; it defaults to binary on Windows and
hashes a different separator), and a CRLF checkout — and nothing else, then record stale. That list
is closed, and having it written down in advance is the whole difference between checking and
adjusting until it matches. The three digests each trap produces, and the 2026-08-24 session that
read two valid in-date records as stale on the output-mode trap alone, are in
[why-this-is-hard.md](why-this-is-hard.md).

**Arbitrate the two locations.** Precedence is by location, not freshness: a project-local record
wins while it is older, thinner, or filed against a corpus that has since moved, and nothing
compares the two — so a stale pin shadows a better home copy silently. Open both where both exist,
and flag at hand-off any disagreement beyond the result.

**State the workload gap in numbers**, never adjectives: the record's `Workload` row beside the
size of the work this brief covers. It bounds what the reviewer's *silence* closes, nothing more.
