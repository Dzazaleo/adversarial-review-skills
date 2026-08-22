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

## echo audit — the history of leaked doubts

- **Discount non-independent agreement.** Where a brief claim was the author's own suspicion — a
  residual doubt leaked into the brief — the reviewer agreeing with it is an echo, not
  confirmation. Verify those findings from primary sources as if the reviewer had said nothing.
  **Whether a doubt was kept out of the brief is your ruling to make, not the hand-off's.** An
  author cannot certify absence in a document they wrote, and here they never have: 2026-08-10,
  five doubts of five were in the brief; 2026-08-15, four of four, reported as "deliberately
  excluded"; 2026-08-17, two of three, reported after the authoring skill had made a search
  mandatory and the author had run it with queries that missed their own doubt. Claims of
  *presence* have been reliable throughout — it is only absence that fails. So for each doubt,
  search the whole brief **and the cover note**, not just the claims list (in the 2026-08-17 case
  half the leak sat in the one-way doors), using the doubt's own citations and identifiers as the
  queries rather than a paraphrase. Record per doubt what you found — in the brief at ‹id›:‹line›,
  or no line found — with the query beside it, and score only a doubt *you* ruled absent as
  independent corroboration. A hand-off that says "held back", "withheld" or "excluded from the
  brief" is asserting what its author was not positioned to know: unverified until you check.

  **The residual doubts are the small channel. The brief's load-bearing claims list is the large
  one, and it is the one that will actually be carrying the author's suspicions.** Every claim
  there with a pointed sub-question — "is 30 derived from anything, or chosen because it sounds
  like a period?", "does the loud error crowd out the quiet gap?" — states the suspected defect
  outright and directs the reviewer at it. A reviewer that comes back agreeing has not
  independently found anything; it has answered a question, which is what it was asked to do and
  is not its failure. So run the same probe over **every finding**, not just the doubts: query the
  brief and cover note with that finding's own identifiers, and record for each whether the brief
  had already said it. Then rule the echoes from primary sources, scoring the reviewer's agreement
  as nothing. Put the tally in the ledger — how many findings were echoes, how many partial, how
  many were free to surprise. That last number is what the report's evidentiary weight actually
  rests on, and a report whose independent findings are all confirmed has earned more than its
  count of findings suggests.

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
