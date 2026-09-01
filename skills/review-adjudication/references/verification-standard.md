# The verification standard — why the card, the pre-registration, and the symmetric burden

Background for `SKILL.md` §5. Every obligation this explains is stated in the skill; this file is
the reasoning, kept out of the main file so the obligations sit above the compaction cut.

## What the claim card buys, and what it does not

You have already read that argument once, in step 1. The point of the card is not that you are
blind to it — you are not — but that the check is aimed at the claim instead of at the case made
for it, and that your expected result is on paper before the evidence arrives. It is the same rule
the ledger template already applies to every re-verification, for the same reason: an expectation
recorded before the run surfaces a surprise mechanically, whereas an expectation recalled
afterwards reshapes itself to fit whatever came back.

Be exact about what pre-registration is worth, because it is easy to claim more. It works on *you*,
in the moment, and only if you actually write the expectation first: the surprise has to land
somewhere it cannot be quietly re-remembered. What it is not is proof to a later reader. The
finished ledger records an expectation and an output but nothing that establishes their order — no
timestamp, no append-only event, and the current round is deliberately editable so it can be
backfilled. A reader six months from now cannot distinguish a pre-registration from a well-written
reconstruction, and should not be told otherwise. Write it first because it changes what you
notice, not because the document will vouch for you.

What that guards against is real and runs in two directions. A well-argued false finding earns a
`CONFIRMED` it did not deserve; a finding stated flatly, in poor English, or by a reviewer whose
earlier numbers failed to reproduce, earns a `REFUTED` on exactly the same non-evidence. Both are
rulings on the reviewer's prose, which is a fact about the reviewer and not about the code.

Re-reading the argument afterwards is required, not a formality — it is often where the
reproduction steps are, and a card whose `Trigger` field says `not stated` may only be reproducible
from the prose around it. What the ordering decides is which of the two ends up as the finding of
record.

One thing this deliberately does **not** borrow from the refutation pipelines it resembles: those
tell the refuter to *default to refuted when uncertain*, and that is right for them, because they
are filtering findings before a human ever sees them and a false positive spends the reader's
attention. This ledger is the opposite position. The finding is already in front of you, the
ruling is durable, and `COULD NOT DETERMINE` — with the check that would settle it named beside
it — is an honest outcome that costs one line. Dropping a finding for being unclear is the
dismissal reflex of `<why_this_is_hard>` wearing a methodology's clothes.

## The evidence standard, restated

A refutation carries the finding's own burden. For any claim about runtime behaviour, a static
read plus a reassuring code comment is not evidence — the comment is the party under review
talking. Reconstruct and run the actual path.

## the throwaway copy — one that can actually run

§5 requires deliberate breakage in a throwaway copy, and §7 forbids writing to the working tree.
Both obvious ways to satisfy the first violate the second or produce nothing: mutating the real
`src/` is the write boundary, and a bare copy of the sources cannot run a suite whose dependencies
were never copied. A git worktree has the same defect, and it is the shape that has actually caused
trouble — an *external reviewer* handed one found it had no `node_modules` and silently ran in the
shared tree instead.

What works, and costs a minute:

- **Copy the code the mutation touches, not the repository.** `src/`, `tests/`, `scripts/` and the
  config files the runner reads (`package.json`, the tsconfig, the runner's own config) into the
  session scratchpad.
- **Link the dependency directory rather than copying it.** A symlink on POSIX, a directory
  junction on Windows (`mklink /J`). Copying it is slow enough that people skip the copy entirely,
  which is how mutating the real tree starts looking reasonable.
- **Remove the link with a link-aware command.** On Windows this is the one that matters:
  `cmd /c rmdir <link>` unlinks it, while a recursive delete from Git Bash or MSYS *traverses the
  junction* and empties the real dependency tree behind it. A POSIX symlink is not followed by a
  recursive delete, so the hazard is Windows-specific and total when it lands.
- **A test the copy cannot satisfy has failed as an artifact of the copy, not as a defect.** Specs
  that read repository files outside the copied set are the usual case, and they fail identically
  whether or not the finding is real. Take whole-suite baselines in the real tree instead, with a
  runner invoked so that it writes nothing (`vitest run`, `pytest -p no:cacheprovider`), and use
  the copy only for the mutation and the one target spec.

The same copy serves the check after the fix. Re-running the original mutation against the fixed
gate is what separates a repaired guarantee from a decorative one: in one round of seven fixes,
three were only provably real because of that re-run, and one newly written test passed cleanly
under the very mutation it had been written to catch.

## echo audit — what agreement with the brief is worth

**Agreement with the brief is non-independent by default.** The brief's load-bearing claims list
states suspected defects outright and points the reviewer at them, so a reviewer that comes back
agreeing has answered a question rather than found anything — which is what it was asked to do and
is not its failure. Verify those findings from primary sources as if the reviewer had said nothing.

**`[deep]` runs the probe and puts the tally in the ledger.** For every finding, query the brief
**and the cover note** with that finding's own identifiers — never a paraphrase — and flatten
whitespace before concluding nothing is there, since the brief's prose wraps and a line-oriented
grep has reported "no line found" for a phrase that was present. Record for each whether the brief
had already said it, then tally: how many findings were echoes, how many partial, how many were
free to surprise. That last number is what the report's evidentiary weight actually rests on, and a
report whose independent findings are all confirmed has earned more than its count of findings
suggests. Measured twice on this repository: 10 of 15 findings were echoes of the brief's own
sub-questions, then 6 of 9, with roughly one in nine arriving unprompted.

**The author's residual doubts are retired and no list reaches you.** The sibling skill used to
form one after saving the brief, bucket each doubt `SEEDED` or `UNSEEDED`, and hand both lists over
in chat for this skill to re-rule. It leaked into the brief every time it was measured — 2026-08-10
five of five, 2026-08-15 four of four (reported as "deliberately excluded"), 2026-08-17 two of
three (the author chose queries that missed their own doubt), 2026-08-23 five of five **with the
search run correctly**. Doubts mined from one reading of one body of work are structurally almost
certain to be claims already in the brief, and no search subtracts a leak the collection order
guarantees. Do not ask for the list, and do not accept one from disk or reconstructed now.

One rule from that history is not doubts-specific and keeps its force: **nobody can certify absence
in a document they wrote.** Across all four runs every wrong label was a claim of absence, and not
one claim of presence was wrong. If a report or a hand-off tells you something was "held back",
"withheld" or "excluded from the brief", that is a claim its author was not positioned to make —
unverified until you check.

## What the claim card buys — the long version

Be exact about what this buys, because overstating it is how a technique becomes a ritual. You read
the report in full in step 1 and you cannot unread it; the card does not make you blind to the
argument and nothing in this skill can. What it does is give step 5 a target that contains only the
claim, so the check is aimed at the mechanism rather than at the case made for it. Genuine
blindness exists in exactly one place in this skill — the subagent in step 5's escalation, which
is never *handed* the report — and that is the only place the word is used for it. **Read that
as narrowly as it is written.** Not being handed the report is not the same as being unable to
read it: the subagent is spawned into the working directory where the report sits beside the
code, it keeps `Read`, `Glob` and `Bash`, and the report is one `ls` away — the identical
exposure this skill names for *reviewers* in step 5. What the escalation buys is a verifier
whose **prompt** contains only the claim. Buying more than that takes a sanitized copy, and the
escalation says how.

## generic findings — the long version

- **Separate what a finding says about the work from what it says about the codebase.** Some
  findings would read the same against any file in the project — "this has no test", in a project
  that tests nothing — and the reviewer could have written them without opening the work at all.
  They can be real and worth fixing, so they get a row like any other. They are simply not evidence
  that the reviewer read anything, and they earn the report no credit on the claims you cannot
  check yourself.

## between-reviewer discount — the long version

- **The same discount applies between reviewers.** Two reports agreeing is corroboration only if
  the second could not read the first. Ours all land in one directory, so by default it could: the
  brief, the earlier report and this ledger sit one `ls` away from a reviewer rooted there. For a
  delta review that visibility is deliberate; for a second opinion it is contamination that looks
  exactly like independent agreement — the failure the cadre harness refuses structurally, by
  keeping each reviewer's output out of the tree the next one reads. Record in the header what each
  reviewer could see, and where it could see the earlier report, re-establish the shared finding
  from primary sources as if only one reviewer had raised it.

## upheld claims — the long version

- **A claim the reviewer upheld is a ruling you inherit, not a line you copy.** Its
  claims-examined-and-upheld list is the coverage evidence the next brief will trust, so sample it
  rather than transcribing it, and re-open anything upheld on the strength of a comment, a test
  name, or a docstring. That is the party under review talking — the exact thing the brief exists
  to demote — arriving through the reviewer instead of the author. The expensive shape is a
  reviewer that got as far as the defect, decided the work must have meant it, and said so, usually
  on the authority of a nearby comment or of a test built around the behaviour as it currently
  stands. Rank that below a plain miss. A miss leaves you the bug; this leaves you the bug plus a
  written case for keeping it, and whoever reads the report next inherits both. Any such passage is
  an open finding, not coverage.


## the refutation burden reads a label, not the stakes

The escalation rule in §5 keys the execution-evidence requirement on **the impact the reviewer
assigned**. That is deliberate — it is the reviewer's own claim about seriousness, and grading it
yourself before you have checked anything is how dismissal gets in. But it has a consequence nobody
chose: **a reviewer that systematically mis-rates a class of defect moves the burden with it.** A
finding filed `low` by a model that under-rates its kind escapes the requirement altogether, and
nothing in the ledger notices, because the rule read the label and the label was wrong.

Two shapes were reported on **2026-08-24** from a run of these skills, and they run in opposite
directions:

- One reviewer filed an unbuildable plan dependency at `low`, ranked third, **having filed the same
  defect at `high` in its own earlier record.** Its plan-integrity ratings do not track its code
  ratings.
- Another put two `high`s on a clean plan. On code its `high` means high; on a plan it can mean
  "this design cannot meet its own acceptance criteria" — real, but a different claim.

So where the reviewer's calibration record carries a **Severity calibration** note about some class
(`calibration/record-template.md` asks for one), or where the report ranks a defect far below where
its own stated Consequence puts it, **apply the burden the consequence earns, and say in the row
that you did and why.**

**This is the one place a severity note may change what you do, and it moves exactly one thing:
the evidence bar for *refusing* a finding.** Never the finding's rank, never its verdict, and never
in the direction of accepting one more cheaply. Calibration governs the reviewer's silence and not
its speech, and that holds here too — the note is being used to stop a cheap refutation, which is
the direction this skill's dismissal reflex never pushes on its own.
