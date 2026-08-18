# How it works

This is for people who want to know *why* each rule is in there.

Almost every rule in these two skills was written in response to something that actually went
wrong — usually something that had already happened at least once. Where a rule was only added
because a later review caught it missing, it says so.

---

## 1. The shape of it

Two skills, four files, one loop.

```
                  ┌─────────────────────────────┐
   your work ────►│  adversarial-review-prompt  │
                  └──────────────┬──────────────┘
                                 │ writes
                    ┌────────────┴────────────┐
                    ▼                         ▼
       NN-EXTERNAL-REVIEW-PROMPT.md   NN-EXTERNAL-REVIEW-COVER-NOTE.md
              (the brief)                (what you paste)
                    │                         │
                    └────────────┬────────────┘
                                 ▼
                       a DIFFERENT model
                    (Codex / Gemini / Cursor /
                     an unrelated Claude session)
                                 │ writes
                                 ▼
                     NN-EXTERNAL-REVIEW.md
                          (the report)
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │     review-adjudication     │
                  └──────────────┬──────────────┘
                                 │ writes
                                 ▼
                  NN-REVIEW-ADJUDICATION.md
                         (the ledger)
                                 │
                                 └──► feeds the *next* brief's
                                      "already covered" section
```

Everything is a file on disk, sitting next to the work. Nothing that matters lives in a chat
window. That is a deliberate constraint rather than a preference — §4 explains why.

`NN` copies whatever numbering the surrounding work already uses: a phase number, a PR number.
If there is no such numbering — a standalone skill, a bare repo — the files drop the prefix and
just sit next to the report. Sitting next to the report is the rule; the prefix is not.

*(That last part was added after round 2 of the self-audit. The other skill was only looking for
the prefixed filename, so the un-prefixed ledger it actually produced was invisible to the next
brief.)*

---

## 2. Why "just ask another model" is not enough

The obvious version of this is to paste your code into a second model and ask it to review. That
fails in a predictable way. The reviewer works through the author's reasoning, decides it makes
sense, and hands back a summary of the author's own beliefs with an independent-looking wrapper
on it. You come away more confident and no better informed.

The brief-writing skill uses three tactics against that. (Inside the skill file itself they are
called levers 1, 2 and 3 — same three things.)

### Tactic 1 — describe the situation, not the mistakes

You cannot tell the reviewer where the blind spots are. If you could see them they would not be
blind, and finding them is the reviewer's whole job.

What you *can* tell it is a fact about how the work was made, rather than about the work itself:

> Every line of this was written by one model, reviewed by that same model, and verified by that
> same model against tests it also wrote. It currently reads as complete and passing. That is
> exactly the problem. You have a different architecture and different training. You will notice
> different things, and those things are the entire value of this exercise.
>
> Confirmation is near-worthless output. A manufactured finding is worse than no finding. A
> finding that survives your own attempt to refute it is worth more than ten observations.

Two safeguards sit inside that framing.

**The sentence about provenance is a factual claim, so it gets checked before the brief goes
out.** If the work contains inherited code, human edits, or third-party code, then "every line
was written by one model" is false. A reviewer that catches the brief in a falsehood starts
doubting everything else in it.

**"I found nothing" has to stay an acceptable answer.** An early draft leaned so hard on *find
what is wrong* that coming back empty read as failing to follow instructions — which is a machine
for inventing findings. *(Codex, finding 1.)* The brief now says plainly that few or zero findings
is a legitimate result, and gives an empty audit somewhere to show its work: a section listing the
claims it examined and found sound.

### Tactic 2 — treat the author's confident statements as claims, not facts

This is the single most productive instruction in the brief:

> This codebase's comments argue for their own correctness. Treat every one of them as a claim by
> the party under review, never as evidence.

It is followed by four to six **real comments quoted out of the actual source**. That makes the
instruction concrete, and it also proves whoever wrote the brief really read the code. Then:

> For any that is load-bearing: open the test, read what it actually asserts, and check whether
> it would fail if the claim were false. A test whose name matches a guarantee is not a test of
> that guarantee.

For a plan or design document, the equivalent target is confident prose — "proven", "industry
standard", "this obviously scales", cited benchmarks.

There is a matching rule pointing the other way, added later: **the reviewer cannot sign a claim
off by quoting a comment either.** A comment, a test name, or a docstring is the code vouching for
itself. Quoting one tells you where the claim lives; it does not check it. That is a "could not
determine", not a confirmation.

The expensive version of this is a reviewer that gets as far as a real bug, reads the comment
above it, decides the author must have meant it, and drops the finding. Rank that below simply
missing the bug. A miss leaves you the bug. This leaves you the bug plus a written case for
keeping it, and whoever reads the report next inherits both. The brief's instruction is: report
it, and say why you think it was deliberate. *(This one came from cadre, which scores that outcome
in its own right — see §10.)*

### Tactic 3 — hand over a target list, not a codebase

"Audit this" spreads a reviewer thin across a whole tree. So instead the brief lists 15–25
**load-bearing claims** — the specific things the work's "it is correct" status is resting on —
each with a `file:line` reference and a follow-up question aimed at the weak point:

> `below * 100 <= maxPct * total` (integer form, `classifier.ts:44`) is exact and immune to float
> drift at the boundary, versus Python's `100.0 * below / total <= 0.5`.
> *The CLI accepts arbitrary decimal `--borderline-max-pct` values — does the guarantee survive
> that?*

These get mined by searching the source for self-assertion (`measured|verified|guaranteed|immune|
cannot|never|by construction`), plus comments that cite a test as proof, frozen contract
declarations, thresholds and comparison operators flagged as deliberate, and any claim that
something behaves identically across machines.

Each one comes back CONFIRMED, REFUTED, or COULD NOT DETERMINE. That is evidence about a single
claim, not a verdict on the work as a whole (§5). And "engaging" a claim means doing the work
needed to settle it — a claim the reviewer only *read* belongs in its could-not-verify list, not
in its coverage count.

### Keeping your own suspicions out of it

The author's own hunches about what is wrong are **kept out of the brief entirely**, and out of
the cover note as well — the cover note gets read first, so planting a suspicion there is worse,
not better. They go to you instead, in the hand-off, as three to five questions with a mechanism
attached to each.

The reason is that the two cases are worth very different amounts. A suspicion you plant gets
echoed back at you. A suspicion the reviewer arrives at on its own is independent corroboration,
which is the strongest evidence this exercise can produce. And disclaimers do not help — "I
suspect X, but do not let that bias you" does not survive contact with a model reading it.

What the author is *not* allowed to do is certify that a hunch stayed out. Hunches and
load-bearing claims come out of the same reading of the same work, so a hunch is usually about a
claim you just wrote, and the follow-up question aimed at that weak point *is* the hunch. The
claim stays sharp — that sharpness is most of the brief's value — and the overlap gets declared
instead. The hand-off lists, for each hunch, which parts of the brief a search actually landed on,
along with the raw search output. Where the search finds nothing, the required wording is "no line
found — unverified", never "held back".

That split exists because the softer version failed three times running. The third failure came
*after* a mandatory search had been added, and performed: the author picks the search terms, and
picks them from the half of the hunch that is not in the brief. Across all three occasions, every
wrong label was a claim that something was *absent*, and not one claim that something was
*present* was ever wrong. Claiming absence in a document you wrote yourself is not a judgement you
are in a position to make.

So the ruling happens on the other side. The adjudicator searches the brief itself, records what
it found for each hunch, and only then can a rediscovered hunch count as corroboration. Where a
hunch did leak into the brief, the reviewer's agreement with it is treated as an echo and the
finding gets re-established from scratch. That rule exists because it happened: four of the
fourteen findings in the self-audit were seeded this way, and all four had to be proved again on
primary evidence alone.

---

## 3. What the reviewer is allowed to do

The brief spells this out in its own block, and fills in every line even when the answer is "no" —
because an omission reads as permission to one model and as prohibition to another.

| Area | What gets stated |
|---|---|
| **Read** | What is in scope, and whether reading outside it is allowed (usually yes, for context) |
| **Write** | Its own report file, always. Everything else read-only by default; if more, exactly which paths, and the obligation to restore them |
| **Execute** | The precise commands, with the slow or destructive ones called out |
| **Network / installs** | Almost always no — and if the project forbids network access at runtime, that prohibition is itself a claim worth auditing |
| **Its own tools** | Web search, MCP servers, subagents. Web search is usually allowed, with a requirement to cite the URL |
| **Effort** | Depth over breadth, and roughly how much |

Three of the rules here are not obvious.

**The permission to write the report and the read-only rule go in the same sentence.** Split across
two paragraphs they read as contradictory, and a model resolving a contradiction plays it safe by
not writing the file — which loses the only output that matters.

**"Read-only" and "does not change anything" are not the same thing.** Commands you explicitly
authorised can still write: test runners that update snapshots, builds that write caches, `git`
subcommands that change state. The envelope says so, and tells the reviewer to hold such a command
back and report what it held back. *(Codex, finding 10.)*

**Mutation testing is the one thing that genuinely earns write access.** The real question about a
test suite is not "do the tests pass" but "would they fail if the code were wrong", and nothing
else answers it. When it is authorised it is bounded: throwaway edits in an obviously temporary
place, commit nothing, put the tree back, report it clean at the end. And a mutation the tests
failed to catch is only a finding if the reviewer can show the change affected behaviour that is
required, reachable and observable — otherwise it proves nothing. An earlier draft said every
uncaught mutation was a finding, which is a false-positive generator. *(Codex, finding 3.)*

**And you get told.** The hand-off to you has to contain one explicit line naming every path the
reviewer may write to and every capability it was granted. Not buried in the brief — in the
message. Nobody's objection is "an external model touched files." The objection is "an external
model touched files and I found out afterwards."

One caveat worth keeping in mind: the envelope is an instruction, not a sandbox. Where a boundary
actually matters, enforce it with the receiving tool's own permission settings too.

---

## 4. Why the report is a file, written as it goes

The brief tells the reviewer to create its report file *before its first finding* — just a title
and its own identity — and then append each finding as it confirms it. At the end it does a closing
pass that sets the final ranking and fills in the coverage line, since what got covered is only
knowable once you are done.

The closing pass is expected and fine. What is forbidden is a report that exists only in the
model's head until the last moment.

The reason is boring and expensive. A report that lives only in chat is one dropped message, one
truncated reply, or one closed tab away from being lost completely. A half-written file can be
picked up; an interrupted composition cannot. So the chat reply is deliberately cut down to a
summary — the coverage line, the ranked finding titles with their impact levels, and the path to
the file. There is a standing instruction not to paste the report twice, because a duplicate that
drifts from the file is worse than no duplicate.

The **cover note** exists for the same reason in reverse. A 400-line markdown brief pasted into a
chat box arrives with its code fences mangled and its opening instruction buried somewhere in the
middle. So the note is about 25 lines of plain prose pointing at the brief on disk, and it carries
exactly four things:

1. **Context and permission, in your own voice** — what the software is, who it runs for, what its
   real exposure is, and that you own it. This is load-bearing, not politeness. A brief that opens
   with *attack this, prove it is wrong* and no explanation of where it came from reads like a
   request to break into someone else's system, and an unsure reviewer spends its output hedging.
2. **The pointer** — the brief's path, written the way the reviewer's session will see it.
3. **Delivery** — write the report to a file as you go, summarise in chat.
4. **Host gotchas** — only the ones that would otherwise get reported as findings. The recurring
   example: on Windows PowerShell, use `npm.cmd` rather than `npm`, because the execution policy
   blocks the `npm.ps1` shim and it fails *before* npm even starts, which looks exactly like a
   failing test suite.

If the reviewer is a browser-only chat with no access to your filesystem, no cover note gets
written at all. A path it cannot open and a file it cannot write are instructions it has no way to
follow. You get told to attach the brief instead and save the returned report yourself.

The brief and the cover note get checked against each other before hand-off: the brief path, the
report path and every permission have to match exactly. The brief tells the reviewer to report
contradictory instructions as a finding, so a cover note saying "read-only" against a brief
authorising mutation burns the whole run on that instead of on your code.

---

## 5. No verdict — a forced ranking instead

The brief never asks "should this ship?" Two reasons:

- It is the owner's call, not a reviewer's.
- A model that commits to yes or no early will bend every finding underneath it to stay consistent
  with itself.

But a review that commits to nothing is just a pile of observations. What the verdict was really
buying is *commitment* — and a strict ranking buys it better. So the reviewer has to order every
finding by the cost of leaving it unfixed (how much damage it does × how likely anything actually
triggers it), with no ties, and one clause of justification for each position. "These are all
equally important" is a refusal to do the one piece of judgement being asked for.

Two distinctions the brief enforces:

- **Impact is a label on a finding, never a section heading.** Grouping findings into severity
  buckets is how a reviewer avoids saying which of its six "criticals" it would fix first.
- **How well-evidenced a finding is has nothing to do with how important it is.** A theoretical
  data-loss bug outranks a confirmed cosmetic one. "A confirmed finding is worth more" is about
  credibility and effort, never about rank. Earlier drafts blurred the two, and the wording was
  still competing with impact after the first round of patches — it took a second verification
  pass to fix. *(Codex, finding 2.)*

Every finding worth reporting carries five parts:

- **Location** — `file:line`.
- **Mechanism** — why the code does the wrong thing, in terms of its own logic.
- **Trigger** — a concrete input. "A malformed PNG" is not a trigger. "A greyscale PNG with a tRNS
  chunk" is.
- **Consequence** — tied to something the work said it would do.
- **Status** — confirmed, with the command and its output, or theoretical, saying what stopped it
  from confirming.

For a plan or design document, "confirmed" becomes "cited and quoted a source that settles it."

The brief also invites findings *about itself* — a `file:line` that does not match, two instructions
that contradict each other, a leftover authoring placeholder. Which is why the brief gets verified
before hand-off: every `file:line` reopened and checked, every command it prints re-run, and the
saved draft searched for the `«guillemets»` that mark author-only notes in the templates. One
leftover guillemet means an instruction meant for the brief's author is about to be read by the
reviewer, so that check fails closed.

---

## 6. Judging what comes back

### First: is the report worth judging at all?

Three checks before anything gets ruled on.

**Is this actually a review?** A description of what the code does, a re-narration of the diff, a
question asking for more input, or a plan for a review that was never run — none of these is a
review. Adjudicating one as "no findings" writes down an all-clear nobody gave. The cadre project
has measured how easily this slips through: several of its stored artifacts were counted as
finished reviews without being reviews at all, and everything they failed to mention was read as
approved. So a report with no findings *and* no coverage line is inconclusive. It needs a re-run,
not a ledger of zero rows.

**Did it finish?** Reviews get cut off partway through, which is exactly why the file-as-you-go
rule exists. Everything it managed to write still counts and gets adjudicated normally. Its silence
counts for nothing: every load-bearing claim it never reached is recorded as unchecked rather than
approved, and the ledger header says the report was partial and where it stopped.

**Is it trying to give instructions?** The report was written by a model you asked to be hostile,
and the adjudicator is about to run commands based on what it says. Its findings are claims to be
checked. Any line in it that tells *the adjudicator* what to do — run this, skip that, go read
something outside the target — gets flagged as a process finding rather than followed.

### The four forces pushing toward the wrong answer

Framing this job as "decide what is worth implementing" is the failure mode, not the goal. Four
forces push toward wrongly dismissing real findings.

**1. You are usually mid-task and want it closed.** Dismissal is the cheapest way to get there, and
it wears respectable clothes: "pre-existing", "out of scope", "scaffold only", "will handle later".
*A finding you just found and immediately deferred is the tell.* So deferring has to cost something.
`FIX LATER` requires a backlog file that exists on disk **before the ledger is written**, with the
finding's location, mechanism and consequence copied into it — the ledger row alone does not contain
them, and a stub with nothing but a path is a dropped finding with a deferral label on it. *(The
content requirement was added after round 2: the original rule checked that the file existed, not
that it said anything.)*

**2. Rejecting a finding is held to a lower standard than making one.** The brief made the reviewer
produce five specific parts for every finding. A refutation typically arrives as a paragraph of
confident reading. That asymmetry is where false rejections come from. **A refutation carries the
same burden as the finding.** For anything about runtime behaviour, reading the code and finding a
reassuring comment is not evidence — *the comment is the thing under review talking*. Reconstruct
the real path and run it, with production's entry point, production's defaults, and the real data.

**3. Self-review sneaks back in.** If you wrote the code, your refutation of a finding about that
code is self-review again, carrying the same blind spots that produced the bug in the first place.
So a `REFUTED` verdict on anything the reviewer rated high or critical, in code you wrote, requires
evidence from actually running something. Without that, the verdict is `COULD NOT DETERMINE`, and
you say what would settle it.

**4. Running the other way: relitigation is real damage.** A reviewer cannot see decisions you
settled months ago and will happily reopen them. Screening for that is legitimate, so it is a step
in the skill — but it is also the channel dismissal will try to use, so it is gated three ways. A
`SETTLED ALREADY` verdict requires the decision quoted with its `file:line`. It has to be the *same*
decision — same root cause, same place, same claim, and where you cannot tell, it is not settled.
And a finding that brings **new evidence the original decision never considered** is not settled
either; it is reopened, and it goes to you.

### Three rules about sequencing the work

- **Enumerate before judging.** Every finding goes into the ledger skeleton — ID, title copied word
  for word, the reviewer's own impact rating — and that skeleton gets written to disk *before any
  verdict is formed*. This guards against the most common real-world drift: the easy findings get
  fixed, the hard ones get forgotten, and the ledger ends up recording only what was convenient.
- **Count in = count out.** One row per numbered finding, with the other categories counted
  separately in the header. A finding with no row is the exact failure this whole skill exists to
  prevent.
- **Split by class.** Machine-checkable (you can settle it by running something) · owner judgement
  (it turns on what the product should do or what risk is acceptable — hand it up as one decidable
  question with options and costs) · process (it is about the brief or the method, so its fix lands
  there rather than in the code). *Resolving a machine-checkable finding by reasoning is an unforced
  error. Resolving an owner-judgement finding yourself is taking a call that is not yours.*

### Weighing what the reviewer said

- **When a finding says a test proves nothing, do not check whether the suite passes — check
  whether it would fail if the thing were wrong.** Break it deliberately, in a throwaway copy
  outside the working tree, and see what happens.
- **Separate what a finding says about your work from what it says about the codebase.** Some
  findings would read the same against any file in the project — "this has no test", in a project
  that tests nothing — and the reviewer could have written them without opening the work at all.
  They can still be real and worth fixing, so they get a row like anything else. They are just not
  evidence that the reviewer read anything.
- **Claims the reviewer says it checked get spot-checked, not copied.** That list is the coverage
  evidence the next brief will trust, which is exactly why it cannot be transcribed on faith.
  Anything signed off by quoting a comment, a test name, or a docstring was not checked, and goes
  back on the pile.
- **Two reviewers agreeing only counts if the second could not read the first.** Everything here
  lands in one directory, so by default it could — the brief, the earlier report and the ledger all
  sit one `ls` away from a reviewer working in that folder. For a follow-up review that visibility
  is deliberate. For a genuine second opinion it is contamination wearing the costume of
  independent agreement. So the ledger records what each reviewer was able to see, and where it
  could see the earlier report, the shared finding gets re-established as though only one reviewer
  had raised it.

---

## 7. Why every finding gets two answers

Every row carries a **verdict** and a **disposition**, because they answer different questions.

| Verdict — is the claim true? | |
|---|---|
| `CONFIRMED` | The defect is real. Evidence in the ledger. |
| `CONFIRMED (partial)` | The mechanism is real; some part — usually how widespread it is, or how much damage it does — is unestablished. Say which. |
| `REFUTED` | False, with evidence at the same standard the finding was held to. |
| `COULD NOT DETERMINE` | An honest and available outcome. Say precisely what would settle it. |
| `SETTLED ALREADY` | It reopens a decision that is already locked. Citation required. |
| `OWNER RULING REQUIRED` | Not the adjudicator's call to make. |

| Disposition — what happens now? | |
|---|---|
| `FIX NOW` | Queued for this round. Name the smallest fix that closes it. |
| `FIX LATER` | Requires the backlog file: path quoted, contents verified. |
| `ACCEPTED AS-IS` | Real, and shipping anyway. **Requires your words, quoted.** Can be proposed, never issued. |
| `NO ACTION` | Only available under `REFUTED` or `SETTLED ALREADY`. |
| `VERIFY` | Pairs with `COULD NOT DETERMINE`: the specific check, and whether it blocks. |
| `PENDING OWNER` | Pairs with **any** verdict — whether something is true and what happens about it are independent. |

**Never a bare "ACCEPTED."** It means both "we accept that the finding is real" and "we accept the
risk and are shipping" — opposite dispositions from one word. That word is what the pre-existing
ledgers in the project this skill was derived from actually used, 21 times.

The vocabulary is not decorative, and it was not complete on the first try. The first real run of
this skill — auditing itself — produced two rows that had *no legal form*: a confirmed finding
waiting on an owner's decision, and a could-not-determine with nothing to pair with. Both gaps fired
live, inside the ledger that was diagnosing them. `PENDING OWNER` with any verdict, and `VERIFY`,
were added in response. *(Fable, findings 1 and 2.)*

Two more rules about the accepted pile:

- **The fix has to be the smallest one that closes the finding.** Where a real finding's suggested
  fix would harden throwaway scaffolding or add complexity out of proportion, the disposition stays
  `FIX NOW` with a *simpler* fix named, or becomes `ACCEPTED AS-IS` with your sign-off. It never
  quietly becomes `NO ACTION` — "the fix is too heavy" is a statement about the fix, not about the
  bug.
- **A cheap fix in a place the work already touches is not deferrable**, even if the bug predates
  the work. Split findings by what they cost to fix, not by where they came from.

---

## 8. Rounds, closure, and the append-only rule

A ledger accumulates rounds. Completed rounds are immutable: a ruling that gets superseded gets a
**new row citing the row it supersedes**, and the original stays exactly as written. The record of
having been wrong is part of what the ledger is for.

But "completed" needs a definition, and the obvious one is wrong. Closure is defined over
**obligations, not filled-in cells**: every numbered row and every auxiliary entry carries both
answers, no `PENDING OWNER` is left unresolved, no blocking `VERIFY` is left open, and every
executed `FIX NOW` row has been updated with what actually landed. A round that is not closed — an
interrupted skeleton, an unexecuted queue, an unanswered question — is still the *current* round,
and filling it in place is required rather than a violation.

Without that definition, the append-only rule traps an interrupted run forever. The skeleton gets
written first by design, so a run killed halfway leaves titles with empty verdicts that the
immutability rule then forbids anyone from filling in. *(Fable, finding 6; refined again in round 2,
when "complete" turned out to freeze provisional rows before their required updates.)*

Findings that do not fit the numbered list get the same two answers, each with its own stable ID:

- `P-n` — defects in the process or the brief. The brief invites these, and their fix lands in the
  brief or the skill rather than in the code, so they get their own block.
- `CNV-n` — the reviewer's could-not-verify list. That list is the reviewer being honest about a gap
  it could not close. Dropping it re-hides the gap, and downstream it reads as a pass.
- `D-n` — places where this reviewer disagrees with an earlier internal review.
- `U-n` — claims the reviewer said it upheld, that the spot-check reopened.

Where two reviewers contradict each other about the same code, neither is presumed right — not by
seniority, not by which arrived first — and the item gets re-verified before either is ruled on. And
where a reviewer's stated numbers fail to reproduce, that gets recorded: a reviewer whose figures
reproduce exactly has earned some weight on the claims you cannot check, and one whose figures drift
has not.

---

## 9. What the adjudicator will not do

- **It does not fix anything.** The deliverable is the ledger. Fixing is a separate, deliberate act
  afterwards, done *against* the ledger.

  There is one sanctioned shortcut, added because the strict rule contradicted what actually
  happened in three real runs out of three: the hand-off's offer to execute the fix queue becomes
  the separate act **the moment you accept it**. Your acceptance gets written into the ledger word
  for word, and then the same session may execute and update the rows. Whoever lands a `FIX NOW`
  change updates that row — a ledger still saying "queued" after the work shipped is a false record.
  *(Fable, finding 7.)*
- **It does not decide whether the work ships.** The other skill refuses to let the reviewer issue a
  verdict, and that refusal does not lapse just because the reader is now Claude.
- **It writes almost nothing.** The only files it creates or edits are the ledger, the `FIX LATER`
  backlog files, and — when the review arrived only as a chat transcript — the report file saved out
  of that transcript before adjudication starts. Never the code, never the plans, never an existing
  review, whatever the tool permissions technically allow.
- **Its re-verification stays clean.** Only commands confirmed not to rewrite repository files or
  external state; the throwaway copy for deliberate breakage lives in a scratch directory, never in
  the working tree; and the step ends by reporting the tree clean. On a target with no repository at
  all, that becomes naming the only files the session wrote and showing the directory otherwise
  unchanged. *(That second branch was added in round 2, after a run against a directory with no git
  in it was still required to report `git status` clean.)*

---

## 10. Where this came from

Neither skill was designed in the abstract. `adversarial-review-prompt` was distilled from a real
audit brief that worked. `review-adjudication` was derived from three real ledgers in a working
project, and then tested backwards against them: apply the rule to what actually happened, and see
whether it produces what the ledger actually says.

Then both were pointed at themselves.

| Round | Target | Reviewer | Result |
|---|---|---|---|
| 1 | `prompt-template.md` | OpenAI Codex (GPT-5) | 24/24 claims engaged, **10 findings** — including that the framing made a zero-finding audit read as non-compliant, that "every surviving mutation is a finding" manufactures false positives, and that evidence status was masquerading as importance |
| 1b | the patches | Codex again | 8 of 10 amendments verified as implemented; **2 found to have diverged** and were fixed |
| 2 | `review-adjudication` | Claude Fable 5 | 22/22 claims engaged, **14 findings**, 2 defects in the brief itself, 5 could-not-verify items. Two findings fired *live against the ledger diagnosing them* |
| 3 | `review-adjudication`, after the fixes | OpenAI Codex (GPT-5) | 22/22 claims engaged, **8 findings** on the round-2 fixes — including two amendments that contradicted rules elsewhere in the skill |

The round-2 adjudication was deliberately run by a session kept blind to the authoring
conversation, so the author's design arguments could not be used to wave findings away. Two of them
survived anyway and became questions for the owner.

Every file from those rounds is in [examples/](examples/), unedited apart from local paths and one
private project name. The round-2 ledger is worth reading in full: it contains a recorded deviation
from its own counting rule, an independence discount applied to four of its own rows, and two owner
questions the adjudicator explicitly refused to answer itself.

### Borrowed from code review cadre

Four rules here came from reading
[VibeCodyH/code-review-cadre](https://github.com/VibeCodyH/code-review-cadre) (MIT). It tackles a
different problem — *which set of reviewers should I use*, graded against answer keys mined from
real fix commits — but it had already measured failures these skills were not guarding against:

- **Spotting a defect and then arguing it away does more damage than never spotting it.** Cadre
  scores that outcome in its own right and disqualifies a reviewer for it. Here it became two rules:
  the brief forbids signing off a claim on the authority of a nearby comment, and the ledger
  spot-checks the upheld-claims list rather than copying it over.
- **A report that is not a review must not be adjudicated as a clean one.** Cadre has stored
  artifacts that were counted as finished reviews while being nothing of the kind, with every file
  they never mentioned read as approved. Adjudication now classifies before it enumerates.
- **A reviewer that stopped early has approved nothing.** Directly relevant because the
  file-as-you-go rule *produces* partial reports on purpose; nothing downstream was reading them as
  partial.
- **Agreement between reviewers who can read each other is not agreement.** Cadre prevents it
  structurally, by keeping one reviewer's output out of any tree the next one can reach. This pair
  puts everything in one directory deliberately, so it is recorded and discounted instead.

Smaller things taken from the same source: the settled-decision check now breaks toward *not
settled*; findings true of the whole codebase are separated from findings about the work; the
reviewer's model family gets named at hand-off; and a public target's own issue tracker is treated
as a way for it to leak its own answers.

The ideas are cadre's; the wording here is ours. Nothing was copied out of that repository — no
code, and no prose.

---

## 11. What this does not fix

- **One path is untested.** Whether the skill descriptions reliably trigger on natural phrasing
  ("close out the review") rather than an explicit `/name` invocation has never been checked live —
  every recorded run was invoked by name. It is in the ledger as an open could-not-verify item
  rather than quietly assumed to work.
- **This reduces self-confirmation; it does not eliminate it.** A second model with similar training
  can still miss what the first one missed. The value comes from the difference between them, so the
  more different the reviewer, the better the return.
- **The envelope is an instruction, not a sandbox.** Enforce the boundaries that matter with the
  receiving tool's own permission system.
- **It costs something.** A serious brief runs 400–600 lines, and reading the work properly enough
  to write one is not cheap. This is for work where being wrong is expensive.
- **The ledger is only as good as its re-verification.** The rules push hard toward actually running
  things, but a lazy run can still produce a plausible-looking ledger full of prose. The
  countermeasure is in the template: every command and its real output, verbatim, and the expected
  result written down *beside the command before it runs* — so a surprise surfaces mechanically
  rather than by memory.

---

## 12. Changing them

Both skills are prose. Edit them.

Worth changing for your own setup: the filenames and where they land; the search patterns used to
mine load-bearing claims (they are tuned for TypeScript comments); the "settled decisions" sources
in adjudication step 3, which currently look for a `CLAUDE.md` do-not-relitigate block, locked
decision IDs, and prior ledgers; and the backlog file requirement in `FIX LATER`, which assumes your
project has somewhere durable to put one.

Worth keeping, because it is where the value is: the reviewer never issues a verdict; your own
hunches never enter the brief, and you never certify that they did not; the report is a file written
as it goes; refuting a finding is as much work as making one; enumerate before judging; and every
finding leaves with both a verdict and a disposition.
