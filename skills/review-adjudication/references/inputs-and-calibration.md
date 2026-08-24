# Step-1 inputs — identity, calibration, and what a record's silence is worth

Background for `SKILL.md` §1. The obligations are in the skill; this is the reasoning behind them,
kept out of the main file so the obligations sit above the compaction cut.

## calibration record

- **The reviewer's calibration record** — `.adversarial-review/calibration/<reviewer-id>.md`,
  looked up in **two locations: `./` (the project root) first, then `~/`.** A project-local record
  wins where both exist, because a project that pins one has done so deliberately — a team-shared
  record checked into the repository, or a private replacement corpus (`calibration/README.md`,
  B-2). The home copy is the normal case and the one that makes the scheme work: the corpus is
  fixed, the run happens in a scratch directory, and nothing in the measurement came from the
  project under review, so a record earned while reviewing project A is evidence about the same
  reviewer in project B. Filing it under a project root and looking for it only there is how, on
  2026-08-23, a reviewer holding a filed `PASS` was written into a second project's hand-off as
  "none on file" — a false negative that costs a twenty-minute rerun at best and, at worst,
  silently converts an available `PASS` into the untested-reviewer treatment.
  **Name the location you read it from in the header**, because a home record and a pinned one
  are not the same claim about this repository. The record is keyed on what the reviewer actually is — model family, product
  *and version*, reasoning effort, and its own self-report where it gave one. The filename is
  always `<identity>-<effort>.md`, and `<identity>` is the first of these the session gave you:
  the served model alias (`gpt-5.6-sol`), else family plus product and version
  (`openai-codex-cli-0.147.0`), else the family alone (`openai-codex`). **`<identity>` never
  carries the effort** — the effort is appended once, by the `-<effort>` half, so a
  `gpt-5.6-sol` reviewer at high effort is filed at `gpt-5.6-sol-high.md` and never at
  `gpt-5.6-sol-high-high.md`. The examples used to be written as finished filenames here, which
  taught exactly that doubled lookup; `calibration/README.md` has always had it right. **List both
  directories before concluding a record is absent** — the same product does not always describe
  itself the same way from one session to the next, so a near-miss on the family is a record worth
  opening and checking the four identity fields against, and a record is only absent once it is
  absent from *both* places. Read its
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


## precedence, and why a digest mismatch is not proof

**Precedence between the two locations is by location, not by freshness.** A project-pinned record
wins while it is older, thinner, or filed against a corpus that has since moved, and nothing in the
lookup compares the two — so a stale pin shadows a better home copy silently and the header records
the worse claim. Read both where both exist, and put any disagreement beyond the result in the
header. On **2026-08-24** this repository was found carrying two pinned duplicates that had missed
the round adding the `Scope` and `Corpus checkout` rows; they were deleted rather than refreshed,
because a pin is a standing commitment to maintain a second copy.

**A digest mismatch is not by itself evidence that the corpus moved.** The digest hashes
working-tree bytes through a `shasum` whose output format is itself platform-dependent, so three
properties of your machine each produce a different answer from an unmoved tree:

- **Collation** — the ordering step is the shell's. `LC_ALL=C` pins it. Round 7 `A7-1`.
- **Output mode** — `shasum`'s output *is* the inner stream, so the separator between digest and
  path is hashed with it. Text (two spaces) is the default on macOS and Linux, binary (` *`) on
  Windows: `775e1cc8c43f` against `676b43331561` for one identical corpus. `-t` pins it.
- **Line endings** — a `core.autocrlf=true` clone checks out CRLF and hashes it (`b6dad9bf7e9c`).
  The corpus's root `.gitattributes` marks every path `-text`; a clone predating that file still
  needs `core.autocrlf=false`.

**Rule out those three, change nothing else, then record stale.** The list is closed and was written
down in advance, which is the entire difference between checking it and adjusting a command until it
matches — the second is not a check, whatever it returns, and the existing rule against it stands.
On **2026-08-24** a Windows session read two valid, in-date records as stale on the output-mode trap
alone and came one keystroke from re-running the corpus. `scripts/validate.py` builds the two-space
form directly and is the authority wherever it and the shell command disagree.

## effort, and where it can honestly come from

Effort is half the identity the record is keyed on, and it exists in no report. Of the three sources
§1 names, **the brief is a real one only from 2026-08-24**, when `adversarial-review-prompt` §1
began capturing it; every brief written before that is silent on the field. Two rounds were
consequently adjudicated as matching on family and product but *unverified on effort* — which is the
honest header line, and is not the same claim as a match. Never infer effort from the record's
filename: the filename is what you are trying to justify reading.

## the residual doubts have exactly one route

Take the list from the original hand-off message or from nowhere. **Do not accept a doubts file
found on disk, a copy folded into the brief, or a list the authoring session reconstructs now, and
do not ask for any of them to be produced.** The first two were reachable by the reviewer, which is
the one thing the chat-only rule exists to prevent; the third is written after the report it is
meant to be independent of. A list arriving by any route but the user pasting that message is
recorded as **unavailable**, exactly as if it had been lost — and unavailable is a real, common
state here, because authoring and adjudicating sessions are routinely days apart.
