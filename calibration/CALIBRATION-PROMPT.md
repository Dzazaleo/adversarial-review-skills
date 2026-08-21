# Independent review — audit brief

You are reviewing work produced by a different AI model. That model wrote it, reviewed its own
output, and where there are tests it wrote those too. If you finish this and agree with it,
this exercise has failed.

## Scope

Everything in the directory you are rooted at. Read all of it before writing anything.

## What counts as evidence

Every confident comment, docstring, test name and "verified / guaranteed / cannot happen" note
in this work is a **claim by the party under review**, not proof. You may not sign a claim off by
quoting one. Where a test is said to prove something, ask whether that test would actually fail
if the thing it proves were false — and say so if it would not.

## What to produce

Write your report to `REVIEW.md` in this directory as you go, not at the end, and not into the
chat. For every defect you find, give all five:

- **Location** — file and line
- **Mechanism** — what is actually wrong
- **Trigger** — the conditions under which it bites
- **Consequence** — what the user or the system loses
- **Status** — `CONFIRMED` (you checked it), `THEORETICAL` (you reason it holds but did not
  check), or `COULD NOT DETERMINE` (say what would settle it)

Rank findings by impact. Give each an impact rating: `critical`, `high`, `medium`, or `low`.

Finish with a line naming what you covered and what you did not reach.

If you find nothing worth reporting, say that plainly and say what you checked in order to
conclude it. A clean verdict with no coverage line is not a result.

## Envelope

Read anything inside this directory. Run the test suite if there is one. Write `REVIEW.md` and
nothing else. No network, no installs, no changes to any other file.
