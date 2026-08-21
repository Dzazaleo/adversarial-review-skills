# Reviewer calibration

**The problem this fixes:** when a review comes back clean, nothing in the pipeline can tell you
whether the work is sound or the reviewer was asleep. Both look identical from here — a report
with no findings — and the second one is worth less than no review at all, because it gets
recorded as an all-clear and the next brief skips the ground it "covered".

Every other rule in these two skills demotes an assertion to a claim and asks for evidence. The
reviewer itself was the one thing still being taken on trust. This corpus tests it the same way
it tests everything else: hand it work with known defects planted in it, and see whether it comes
back with them.

Six cases: four traps with one planted defect each, two clean cases with none. About twenty
minutes and six reviewer runs, once per reviewer model.

## The isolation rule

**Copy one case directory into an empty scratch folder, and root the reviewer there.** Never
point it at `calibration/` itself, and never copy `ANSWER-KEY.md` alongside a case.

A reviewer rooted anywhere above these files can read the answers, and a calibration a reviewer
can read is a calibration it passes. This is the same failure the adjudication skill guards
against between reviewers — reports landing one `ls` away from each other and agreement getting
banked as independence — arriving one level up, in the thing that measures the reviewer.

```bash
CASE=trap-unfalsifiable-test
WORK=$(mktemp -d)
cp -R calibration/cases/$CASE/. "$WORK"/
cp calibration/CALIBRATION-PROMPT.md "$WORK"/BRIEF.md
echo "$WORK"        # root the reviewer here, then: "read BRIEF.md and do what it says"
```

Run each of the six cases this way, in a **fresh session** each time. A reviewer that carries the
last case into the next one has been primed to look for planted defects, which is exactly the
condition real use will not give it.

## Scoring

Score each run against [ANSWER-KEY.md](ANSWER-KEY.md) — do not open the key before the run.

- **Trap** — hit if the report **asserts** the primary defect. Wording is free, but a mention is
  not a hit: every identifier in the key already appears in the case, so a reviewer that summarises
  the work will use all the right words while finding nothing. The key says what each report has to
  claim, and where to look for it. A report that names the defect but rates it `low` still counts as a hit, and the
  rating goes in the record: a reviewer that finds a service-role key in a client bundle and
  calls it `low` is calibrated for detection and miscalibrated for severity, and you want that
  written down before you trust its ranking.
- **Clean** — passes if it raises no `critical` or `high` finding. Count the mediums.

**Pass:** all four traps hit, and at least one clean case with nothing above `medium`. The
reasoning behind both halves, and behind "at least one" rather than both, is in the key.

## The record

Write the result to `.adversarial-review/calibration/<reviewer-id>.md` in the project you intend
to review, using [record-template.md](record-template.md). Both skills read it from there.

`<reviewer-id>` is the model's **own** identity, slugged — `gpt-5.6-codex`, `gemini-3-pro`,
`claude-fable-5` — never the product name. A record filed under `cursor` or `copilot` says
nothing, because those are thin layers over a base model that changes underneath them, and the
whole return on cross-model review is the architecture difference. Ask the reviewer what it is
and record the answer verbatim; where it will not say, record that, and the record is
`UNKNOWN MODEL` — which does not pass.

The record lives in the project, not in your home directory, because the result is
project-shaped: a reviewer that reads Python plans well may be poor on your Rust service, and a
pass earned somewhere else is not evidence about here.

## Expiry

A record is stale when any of these is true, and stale is treated exactly as missing:

- **30 days have passed.** Not because reviewers decay on a schedule, but because providers ship
  changes behind an unchanged model name, so the identity string cannot be relied on to tell you
  the model changed.
- **The reviewer's reported model identity differs from the record's.**
- **This corpus changed.** The record names the corpus commit; a different one is a different
  measurement.

Do not re-date a stale record. Re-run it.

## What a missing, stale or failed record does — and what it does not

**Calibration governs the reviewer's silence, never its speech.**

A finding is a claim to be re-verified on its own evidence, and that is true whoever raised it. An
uncalibrated reviewer's findings are adjudicated normally, at the standard the ledger already
demands. A real defect does not become less real because the reviewer that spotted it was never
tested.

What an uncalibrated reviewer cannot do is *close* anything:

- Its **claims-examined-and-upheld** list is not coverage. Every load-bearing claim on it is a
  `COULD NOT VERIFY` entry unless the adjudicator re-established the claim itself.
- A **report with no findings** is inconclusive, not an all-clear. It gets no ledger of its own,
  the same as a report that turned out not to be a review.
- The next brief's **"ground already walked"** section does not inherit anything from it.

This is deliberately the same treatment a **partial report** already gets: findings stand,
silence covers nothing. A reviewer that was never shown to be able to find anything is, for the
purpose of what its silence proves, a reviewer that stopped before it started.

Both skills say this in their own hand-offs. Neither will refuse to run over it — the user decides
whether an uncalibrated review is worth having, which it very often is. What neither will do is
let an untested reviewer's quiet be written down as approval.
