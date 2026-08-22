# Step-1 inputs — identity, calibration, and what a record's silence is worth

Background for `SKILL.md` §1. The obligations are in the skill; this is the reasoning behind them,
kept out of the main file so the obligations sit above the compaction cut.

## calibration record

- **The reviewer's calibration record** — `.adversarial-review/calibration/<reviewer-id>.md` under
  the project root. The record is keyed on what the reviewer actually is — model family, product
  *and version*, reasoning effort, and its own self-report where it gave one. The filename is
  always `<identity>-<effort>.md`, and `<identity>` is the first of these the session gave you:
  the served model alias (`gpt-5.6-sol`), else family plus product and version
  (`openai-codex-cli-0.147.0`), else the family alone (`openai-codex`). **`<identity>` never
  carries the effort** — the effort is appended once, by the `-<effort>` half, so a
  `gpt-5.6-sol` reviewer at high effort is filed at `gpt-5.6-sol-high.md` and never at
  `gpt-5.6-sol-high-high.md`. The examples used to be written as finished filenames here, which
  taught exactly that doubled lookup; `calibration/README.md` has always had it right. **List the directory before
  concluding a record is absent** — the same product does not always describe itself the same way
  from one session to the next, so a near-miss on the family is a record worth opening and checking
  the four identity fields against. Read its
  result, its expiry, **its corpus digest**, **and the size of work it was earned on**; a record
  past its expiry date, or filed against a different identity — different family, product version,
  or reasoning effort — is stale and counts as missing.

  **The digest is the only check that notices the instrument moving.** Recompute it from the corpus
  the record names — the command is in `calibration/record-template.md` — and compare. A different
  digest is a different measurement, so the record is stale and counts as missing however recent it
  is. Where you do not have the corpus at all, which is the normal case for an installed skill,
  say that staleness was **unknowable** rather than passing the record: an unchecked digest is not
  a matching one. Record what you found in the ledger header beside the
  isolation line — it is the same kind of fact, and it is read for the same purpose.

  The record's own caveat is part of what you read, not boilerplate under it: a pass is evidence
  about work of roughly the corpus's size and kind. **State both sizes in numbers and let the
  reader judge** — the record's `Workload` row says what the pass was earned on, and you say what
  this review covered, in the header and again at hand-off. Do not characterise the gap as "far
  larger" or "comparable": there is no measured threshold at which that fires, so a word in place
  of the two numbers is a sentence an adjudicator can write regardless of the facts. The gap does
  not make the record worthless and it is not a reason to discount a single finding; it bounds
  what the reviewer's *silence* is entitled to close, which is the only thing calibration was ever
  buying.

## uncalibrated reviewer

- **Was this reviewer ever shown to be able to find anything?** With no passing calibration record
  (missing, stale, or `FAIL`), you know it produced a report; you do not know it can detect a
  defect it was not handed. So it gets a partial report's treatment, for a partial report's
  reason — **its findings stand, its silence covers nothing.** Adjudicate every finding normally
  and at the usual standard: a defect does not become less real because the model that spotted it
  was never tested, and downgrading real findings for the reviewer's paperwork would be this
  skill's own dismissal reflex wearing a rigorous costume. What lapses is only what its quiet is
  allowed to close — every load-bearing claim on its upheld list is a CNV entry rather than
  coverage, and a report with no findings at all is inconclusive, ruled the same as a report that
  turned out not to be a review. Say it in the header and in the hand-off, and point once at
  the calibration corpus — https://github.com/Dzazaleo/adversarial-review-skills/tree/main/calibration
  — 20 minutes, six cases, and the next review's silence starts meaning something. It is not
  installed alongside the skill, so give the URL rather than a bare path. Do not raise it twice.


## Establishing the reviewer's identity — the long version

- **Who the reviewer was** — model family, product and version, and reasoning effort. **Establish
  this; never infer it**, and resolve it before the calibration record below, which is keyed on
  it and cannot be looked up without it. Take it from `$ARGUMENTS`, or from the brief the report
  answers, or from a prior round's ledger header where one exists. Failing all three, **ask**.

  Do not read it off the report itself. Prose style, formatting habits, the phrase "As an AI
  language model", a tool name in a citation and a section layout that resembles some other
  reviewer's are not identification — they are the reviewer's output, which is the thing under
  adjudication, and several products are thin layers over a shared base model besides. Guessing
  here fails the same way it fails in the prompt skill and one step later: a wrong identity
  loads a different model's calibration record, and a `PASS` read for the wrong reviewer is
  written into the ledger header as this reviewer's, where nothing downstream can tell it from
  a correct one. An identity you could not establish is recorded as unknown, and unknown is
  treated exactly as no record — one honest sentence, and no false credit.

## is it a review — the long version

- **Is it actually a review?** A description of what the code does, a re-narration of the diff, a
  question asking for more input, or a plan for a review that was never run — none of these is a
  review, and adjudicating one as "no findings" writes down an all-clear nobody gave. The cadre
  project has measured how easily this passes unnoticed: three of its stored artifacts were counted
  as finished reviews without being reviews, and everything they failed to mention was read as
  approved. So no findings **and** no coverage line is an inconclusive run — say so in the hand-off
  and ask for a re-run. Do not write a zero-row ledger against it.

## the round — the long version

- **The round.** If a ledger already exists at the target path, check whether its last round is
  *closed*. Closed is defined over obligations, not cell presence: every numbered row AND every
  auxiliary entry (process, CNV, prior-review disagreement, re-opened upheld claim) carries both a
  verdict and a disposition, no `PENDING OWNER` remains unresolved, no blocking `VERIFY` remains
  open, and every
  executed `FIX NOW` row has been backfilled with its execution reference. A closed round is
  history: append `# Round N`, never edit it — a superseded ruling gets a new row that says so. A
  round not yet closed — an interrupted skeleton, an unexecuted queue, an unanswered owner
  question — is the current round: fill it in place, and state/evidence backfill (owner answers,
  execution references) is not only legal but required until closure.
