# Independent review — audit brief

You are reviewing work produced by a different AI model. That model wrote it, reviewed its own
output, and where there are tests it wrote those too. Confirmation is near-worthless output: if you
spend your effort re-deriving what is already claimed correct and agreeing, this review has failed.

**A manufactured finding is worse than no finding.** If a rigorous search comes back nearly empty,
say so and show the search — few or zero findings is an admissible result, and naming what you
checked in order to conclude it is where that result earns its credibility. Do not go looking for
something serious to say because the paragraph above told you agreement is failure. Some work is
correct.

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

Read anything inside this directory. Run the test suite if there is one. Write `REVIEW.md`, and
change no file that was already here. A test runner leaving its own caches behind is expected and
is not a violation. No network, no installs.
