# Reviewer calibration

**The problem this fixes:** when a review comes back clean, nothing in the pipeline can tell you
whether the work is sound or the reviewer was asleep. Both look identical from here — a report
with no findings — and the second one is worth less than no review at all, because it gets
recorded as an all-clear and the next brief skips the ground it "covered".

Every other rule in these two skills demotes an assertion to a claim and asks for evidence. The
reviewer itself was the one thing still being taken on trust. This corpus tests it the same way
it tests everything else: hand it work with known defects planted in it, and see whether it comes
back with them.

Six cases: four traps with a planted defect, two clean cases with none. About twenty
minutes and six reviewer runs, once per reviewer model.

## The isolation rule

**Copy one case directory into an empty scratch folder, and root the reviewer there.** Never
point it at `calibration/` itself, and never copy `ANSWER-KEY.md` alongside a case.

A reviewer rooted anywhere above these files can read the answers, and a calibration a reviewer
can read is a calibration it passes. This is the same failure the adjudication skill guards
against between reviewers — reports landing one `ls` away from each other and agreement getting
banked as independence — arriving one level up, in the thing that measures the reviewer.

**Be exact about what this buys.** Rooting the reviewer in a scratch folder removes *adjacent*
discovery — there is nothing to stumble into by listing the directory or its parent. It is not
confinement. A process rooted there keeps ordinary filesystem reach and can still read this
directory by absolute path if it goes looking, and it can still have the public repository in its
training data. The envelope is an instruction, not a sandbox; enforce the rest with the receiving
tool's own permission system, and treat a run you could not confine as a run whose result is weaker
than one you could.

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

**Every rule that decides a result lives in the key, and only in the key.** What each trap's report
must assert, that a mention is not a hit, that severity does not gate a trap, what a clean case may
raise, and the pass rule itself: read them there and score from there. This file does not restate
them, deliberately. The key is inside the corpus digest and this file is not, so a rule restated
here could be edited without expiring a single record — the measurement would change and every
stored `PASS` would go on looking current. If you want to change how cases are scored, change the
key.

The procedure, then, is only: run the six cases as above, open
[ANSWER-KEY.md](ANSWER-KEY.md), score each report against it, and record the result and the counts
the key asks for in [record-template.md](record-template.md).

## The record

Write the result to `~/.adversarial-review/calibration/<reviewer-id>.md`, using
[record-template.md](record-template.md). Both skills read it from there.

`<reviewer-id>` is the model's **own** identity, slugged, followed by the reasoning effort —
`gpt-5.6-codex-high`, `gemini-3-pro-high`, `claude-fable-5-default`. The exact rule for building it
is below, and it is one rule: there is no shorter form. Ask the reviewer what it is and record the
answer verbatim. A record filed under
`cursor` or `copilot` alone says nothing, because those are thin layers over a base model that
changes underneath them, and the whole return on cross-model review is the architecture difference.

**Many models cannot name their own served version, and that is normal rather than a failure.** Ask
anyway, record verbatim whatever comes back, and let the rest of the identity carry the key: model
family, product *and version*, and the reasoning effort the run used.

**Capture all four from the first session, before you close it** — not after the sixth. Reasoning
effort in particular is a session setting and is nowhere in the reports, so an operator who runs
all six and then opens this template is reconstructing it from memory. Ask the reviewer directly in
that first session, once it has written its report. Do **not** put the question in
`CALIBRATION-PROMPT.md`: a review brief that asks a reviewer what model it is announces that the
session is an evaluation, which is the one thing this corpus cannot afford to disclose. Those four together are the
identity — not the self-reported string alone. Only a reviewer that will not name even its family
is `UNKNOWN MODEL`, which does not pass.

Effort earns its place in that list. The same model at high and at low reasoning effort is not the
same reviewer, and a pass earned by the strong configuration is not evidence about the weak one
running under the same name.

For the **filename**, always end with the reasoning effort, because a run at a different effort is
a different reviewer and must file its own record rather than overwrite one: `<identity>-<effort>.md`.

`<identity>` is built by taking **the first of these the session actually gave you**, and no other:

1. **The served model alias**, where the reviewer named one — `gpt-5.6-sol`, `gemini-3-pro`. This
   is the alias itself, not the sentence around it: a reviewer that says "OpenAI Codex, an agent
   based on GPT-5; the active model alias is `gpt-5.6-sol`" has given you `gpt-5.6-sol`.
2. **Family plus product and version**, where it named no alias — `openai-codex-cli-0.147.0`.
3. **Family alone**, where it named only that — `openai-codex`. A reviewer that will not name even
   its family is `UNKNOWN MODEL`, which does not pass.

The order is fixed so that two people filing the same session reach the same name. What it cannot
fix is that **the same product does not always say the same thing about itself**: on 2026-08-22 one
Codex session named the alias `gpt-5.6-sol` and another, hours later, could give only "OpenAI
Codex, GPT-5-based". Those two sessions produce two filenames for one reviewer, and no naming rule
closes that.

So the lookup rule has a second half. **Before concluding a record is absent, list both
directories.** Each holds few enough files to read at a glance; a near-miss on the family is a
record worth opening and checking the four identity fields against, and treating a present record
as missing is the exact failure this scheme was built to escape. Both skills look the record up by
filename, and both are told to look at the directories before saying there is nothing there.

## Where the record lives, and why it is not the project

**Home, not the project root.** The run is made on *this* corpus, in a scratch directory, against
work the project under review never supplied — the isolation rule above requires exactly that.
Nothing in the measurement touches the project, so nothing in the result is project-shaped, while a
record filed under one project root is invisible to the next one. That is not hypothetical: on
2026-08-23 a reviewer with a filed `PASS` was reported to a second project as "none on file",
because the lookup only ever looked where it stood. One reviewer, one record, on the machine that
runs it.

**A project may still pin its own, and it wins.** Both skills read
`./.adversarial-review/calibration/` first and `~/.adversarial-review/calibration/` second; a
project-local record takes precedence where both exist. Use that when a team wants one record
checked into the repository, or when you have replaced the corpus with private traps (B-2) and the
pass there means something the machine-wide record does not.

**What a home record does not buy** — the true half of the rule it replaces. The pass is earned on
this corpus: six small Python, HTML and plan-document cases. A reviewer that finds the planted
defects here has not thereby been shown to read your Rust service well. But that is a statement
about what the reviewer's *silence* closes, which is what the `Workload` row and the consumers'
workload-gap line already carry in numbers — and both consumers state it whatever the record's
location. It was never a reason to hide a real result from the next project.

**Both consumers say which of the two they read it from**, because "PASS, from `~`" and "PASS, from
this repo" are not the same claim, and a later reader cannot tell them apart otherwise.

## Expiry

A record is stale when any of these is true, and stale is treated exactly as missing:

- **30 days have passed.** Providers ship changes behind an unchanged model name, so the identity
  string cannot be relied on to tell you the model changed, and a record has to age out on
  something. **The 30 is a chosen default, not a derived one** — nothing here measured it, and
  nothing here can. Shorten it freely; the cost of a shorter window is one twenty-minute rerun.
- **The reviewer's identity differs from the record's** — a different family, a different product
  version, a different reasoning effort, or a different self-reported string.
- **The instrument changed.** A different digest is a different measurement. The digest covers
  what actually decides a result — `cases/`, the fixed brief, and the answer key — and
  deliberately **not** this file or the record template, which are operator documentation the
  reviewer never sees. Fixing a typo in the protocol should not throw away every record you hold.
  It enumerates **tracked** files (`git ls-files`) but hashes working-tree bytes, so running the
  fixtures cannot expire a record — while an uncommitted edit to a tracked case **does** move the
  digest, and only a never-added file is invisible: commit corpus changes before filing or
  trusting a record. **Run the command with `LC_ALL=C`** — the ordering step is the shell's
  collation, and a UTF-8 locale orders this corpus differently, producing a digest the validator's
  byte-sort will never reproduce and a record that reads as permanently stale (round 7 `A7-1`).
  **`-t` is not optional either, and neither is an LF checkout** — `shasum` defaults to binary mode
  on Windows and hashes a different separator into the stream, and a `core.autocrlf=true` clone
  hashes CRLF bytes. Each produces a different digest from identical cases, and a record carries no
  record of the platform that computed it. `record-template.md` carries the command, all three
  traps, and the reasoning.

Do not re-date a stale record. Re-run it. **But establish that it is stale first** — a digest
mismatch is the expected reading when the command or the checkout differs from the one that filed
the record, and on 2026-08-24 that cost two valid records a near-miss with forty minutes of
re-running. The three traps in `record-template.md` are the first thing to rule out, and they are
cheaper to rule out than a single case is to re-run.

## What a missing, stale or failed record does — and what it does not

**Calibration governs the reviewer's silence, never its speech.**

A finding is a claim to be re-verified on its own evidence, and that is true whoever raised it. An
uncalibrated reviewer's findings are adjudicated normally, at the standard the ledger already
demands. A real defect does not become less real because the reviewer that spotted it was never
tested.

What an uncalibrated reviewer cannot do is *close* anything:

- Its **claims-examined-and-upheld** list is not coverage. Every load-bearing claim on it is a
  `COULD NOT DETERMINE` entry unless the adjudicator re-established the claim itself.
- A **report with no findings** is inconclusive, not an all-clear. It gets no ledger of its own,
  the same as a report that turned out not to be a review.
- The next brief's **"ground already walked"** section does not inherit anything from it.

This is deliberately the same treatment a **partial report** already gets: findings stand,
silence covers nothing. A reviewer that was never shown to be able to find anything is, for the
purpose of what its silence proves, a reviewer that stopped before it started.

Both skills say this in their own hand-offs. Neither will refuse to run over it — the user decides
whether an uncalibrated review is worth having, which it very often is. What neither will do is
let an untested reviewer's quiet be written down as approval.
