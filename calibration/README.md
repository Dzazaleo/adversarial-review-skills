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

Write the result to `.adversarial-review/calibration/<reviewer-id>.md` in the project you intend
to review, using [record-template.md](record-template.md). Both skills read it from there.

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

So the lookup rule has a second half. **Before concluding a record is absent, list the directory.**
`.adversarial-review/calibration/` holds few enough files to read at a glance; a near-miss on the
family is a record worth opening and checking the four identity fields against, and treating a
present record as missing is the exact failure this scheme was built to escape. Both skills look
the record up by filename, and both are told to look at the directory before saying there is
nothing there.

The record lives in the project, not in your home directory, because the result is
project-shaped: a reviewer that reads Python plans well may be poor on your Rust service, and a
pass earned somewhere else is not evidence about here.

## Expiry

A record is stale when any of these is true, and stale is treated exactly as missing:

- **30 days have passed.** Providers ship changes behind an unchanged model name, so the identity
  string cannot be relied on to tell you the model changed, and a record has to age out on
  something. **The 30 is a chosen default, not a derived one** — nothing here measured it, and
  nothing here can. Shorten it freely; the cost of a shorter window is one twenty-minute rerun.
- **The reviewer's identity differs from the record's** — a different family, a different product
  version, a different reasoning effort, or a different self-reported string.
- **The instrument changed.** The record names a digest rather than a commit, so an uncommitted
  edit to a case or a private replacement corpus expires the record too. A different digest is a
  different measurement. The digest covers what actually decides a result — `cases/`, the fixed
  brief, and the answer key — and deliberately **not** this file or the record template, which are
  operator documentation the reviewer never sees. Fixing a typo in the protocol should not throw
  away every record you hold.

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
