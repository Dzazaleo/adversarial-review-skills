# Adversarial Independent Audit — the `review-adjudication` skill, Round 2 (post-amendment)

> **Prompt for an external reviewer.** Hand this file to a model that did **not** write the skill
> under review and did **not** perform its first audit. Everything below is written to be read by
> that reviewer, not by the author.

---

## 1. Why you are here

The target is a Claude Code *skill* — a prose instruction document that another model loads and
follows. It was written and self-reviewed by one model in a single session on 2026-08-10. It was
then audited once, by a second model, which returned 14 ranked findings. All 13 accepted fixes were
applied **the same day, by a model in the same family as the one that wrote the skill, in the same
session that adjudicated the audit.** The skill now reads as complete: every finding closed, a
ledger on disk recording it, an owner sign-off quoted.

That is exactly the problem, and it is worse here than in the ordinary case.

The first audit found real holes. The fixes were then authored by the same side of the table — and
a fix written by the party under review is a *claim that the hole is closed*, not evidence that it
is. Amendments are the highest-risk text in any document: they are written under time pressure,
against a specific finding rather than against the whole, and they are the least re-read. The
recurring failure mode is a fix that lands in one of two coupled files, or that closes its own hole
while opening a new path to the same failure.

You have a different architecture and different training. **You will notice different things, and
those things are the entire value of this exercise.**

- **Confirmation is near-worthless output.** If you spend your effort re-deriving that the 13 fixes
  do what their ledger rows say they do, and agreeing, this audit has failed.
- **Your job is to find what is wrong, missing, or unjustified**, and to prove it.
- **A manufactured finding is worse than no finding.** If a rigorous search comes back nearly
  empty, say so and show the search — few or zero findings is an admissible result, and the
  claims-examined-and-upheld section is where it earns its credibility.
- **A finding that survives your own attempt to refute it is worth more than ten observations.**
  Try to break your own findings before reporting them.

Assume competence, not correctness. This document is carefully built and well argued. Where it is
wrong, it is wrong in ways its author cannot see — those places are what you are here for.

## 2. The single most important instruction

**This document argues for its own correctness in prose. Treat every confident sentence in it as a
claim by the party under review, never as evidence.** There is no compiler here and no test suite;
the assertions are all there is, and they are unusually assertive:

> `SKILL.md:110` — "A finding with no row is the defect this whole skill exists to prevent."
>
> `SKILL.md:106` — "**Count in = count out — over the report's *numbered* findings.**"
>
> `SKILL.md:144` — "The split is the discipline."
>
> `SKILL.md:192` — "`COULD NOT DETERMINE` | Say precisely what would settle it. This is an honest,
> available outcome."
>
> `SKILL.md:233` — "The only files this skill creates or edits are the ledger and `FIX LATER`
> backlog artifacts — never the code, the plans, or the review, whatever the tool grants allow."
>
> `SKILL.md:249-251` — "Whoever lands a `FIX NOW` change updates that row — a ledger still saying
> 'queued' after the work landed is a false record."

For any of these that is load-bearing to your audit: **do not check whether the rule is stated —
check whether a model following the whole document end to end can comply with it, and what it
writes when it cannot.** A rule that is stated in one file and contradicted by the worked example
in the other is not a rule. A rule whose only enforcement is a later sentence asking the model to
have complied is not a guard.

The same treatment applies with extra force to the 13 amendments (§7). Each was written to answer
one finding. Ask of each: does it close the hole *for the case that produced it*, or *for every
case the document reaches* — and did closing it open a new path to the same failure?

## 3. Governing sources and how to check things

There is no test suite. The skill is prose. But this is **not** a paper-only audit — there is a
real corpus to check it against, and findings grounded in it are worth far more than findings
grounded in reasoning about the text.

| | |
|---|---|
| **The skill under review** | `~/.claude/skills/review-adjudication/` |
| **Its sibling, which it pairs with** | `~/.claude/skills/adversarial-review-prompt/` |
| **The real corpus it was derived from** | `~/projects/corpus-project/.planning/` |
| **Skill mechanics** | `~/.claude/skills/<name>/SKILL.md`; the YAML `description:` field is the *only* text a model sees when deciding whether to load the skill; `allowed-tools:` is an optional whitelist active while it runs |

**The two decisive checks available to you** are:

1. **Prediction.** One report on disk has **no ledger and has never been adjudicated**:
   `.planning/phases/103.5-guided-handoff-path-inserted/103.5-EXTERNAL-REVIEW.md` (129 lines).
   The amended skill has never seen it. Walk the skill against it end to end and produce, on paper,
   the ledger header it demands and the shape of the ledger it would yield. Anything that cannot be
   written is a defect, and it is the strongest kind available here.

2. **Retrodiction against the amendment itself.** The skill's own first run is on disk as
   `REVIEW-ADJUDICATION.md` (294 lines) — the only worked example that exists. It was written under
   the *pre-amendment* text. Read it as evidence: which of its improvisations did the amendments
   actually legalize, and which are still improvisations under the amended text?

### Verified facts about the corpus — you may rely on these, but spot-check them

Report files on disk (`*EXTERNAL*` minus `*PROMPT*`, `*COVER-NOTE*`, `*ADJUDICATION*`,
`*RESPONSE*` — the skill's own discovery rule at `SKILL.md:65-71`), per phase directory:

```
103.45-…  103.45-EXTERNAL-AUDIT-codex.md                      (398 lines)   no ledger
103.46-…  103.46-EXTERNAL-CODE-REVIEW.md                                    ledger exists (2 rounds)
          103.46-EXTERNAL-REVIEW-2.md                          (342 lines)
          103.46-EXTERNAL-REVIEW.md
103.5-…   103.5-EXTERNAL-REVIEW.md                             (129 lines)  NO LEDGER — never adjudicated
105-…     105-EXTERNAL-CODE-REVIEW.md                          (258 lines)  no ledger
          (+ 105-EXTERNAL-CODE-REVIEW-RESPONSE.md, excluded by the rule)
106-…     106-EXTERNAL-REVIEW.md                               (413 lines)  no ledger
106.1-…   106.1-EXTERNAL-REVIEW.md                                          ledger exists
107-…     107-EXTERNAL-CODE-REVIEW.md                          (400 lines)   ledger exists
          107-EXTERNAL-REVIEW.md
```

Exactly three ledgers exist in the corpus, all written by hand before this skill was authored:

```
.planning/phases/103.46-…/103.46-REVIEW-ADJUDICATION.md    (10 rows, 2 rounds)
.planning/phases/106.1-…/106.1-REVIEW-ADJUDICATION.md      (7 rows, header: # | Finding | Verdict | Reason)
.planning/phases/107-…/107-REVIEW-ADJUDICATION.md          (9 rows, disposition column headed "Where fixed")
```

Plus the skill's own, written by the skill's first run:
`~/.claude/skills/review-adjudication/REVIEW-ADJUDICATION.md` (14 rows).

Other verified measurements — recount rather than quoting these if a finding turns on one:

- `SKILL.md` is 261 lines (was 230 before the amendments). `references/ledger-template.md` is 160
  (was 157).
- The `description:` field at `SKILL.md:3` is 699 characters of description text (the raw line is
  714 including the `description: ` prefix and the surrounding quotes).
- `~/.claude/skills/` contains 73 skill directories. It is **not** a git repository —
  `git -C ~/.claude status` returns `fatal: not a git repository`. There is no version history for
  any change made to this skill or to its sibling.
- `103.5-EXTERNAL-REVIEW.md` contains: 8 ranked numbered findings, a "**Prompt bookkeeping
  defect:**" paragraph in its preamble, a "Claims examined and upheld" list, a "Could not verify"
  list of 5 entries, and a "Disagreements with the internal review" section of 4 entries.

Project context the skill leans on and you should verify rather than assume:
`corpus-project/CLAUDE.md` contains a "Critical non-obvious facts (do not relitigate)" block
that `SKILL.md:116` cites by name as a screening input.

## 4. Scope

**In scope — 421 lines, the amended skill:**

| File | Lines | What it is |
|---|---|---|
| `~/.claude/skills/review-adjudication/SKILL.md` | 261 | frontmatter, `<objective>`, `<why_this_is_hard>`, an 8-step `<process>` |
| `~/.claude/skills/review-adjudication/references/ledger-template.md` | 160 | the output document's skeleton, loaded only when the body links to it |

**Also in scope, as the contract this must fit:** the sibling skill
`~/.claude/skills/adversarial-review-prompt/SKILL.md` (316 lines) and its
`references/prompt-template.md` (336 lines). You are not auditing the sibling — except at
`adversarial-review-prompt/SKILL.md:111` and `references/prompt-template.md:130`, two lines that
were **added by this skill's round-1 amendment** and are therefore in scope as amendments.

**History, not targets:** `EXTERNAL-REVIEW-PROMPT.md` (468 lines, the round-1 brief),
`EXTERNAL-REVIEW-FABLE.md` (416 lines, the round-1 report), `REVIEW-ADJUDICATION.md` (294 lines,
the round-1 ledger). Read them — §7 depends on it — but do not audit the round-1 brief's prose or
re-litigate a round-1 disposition unless the amendment it produced is defective.

**Out of scope:** the the corpus project application, its source, its phases, and the
correctness of any adjudication decision recorded in the corpus. Do not review absent work and do
not propose features. Read the corpus as evidence about the skill, not as a target.

### The one-way doors — spend disproportionate attention here

1. **The verdict/disposition vocabulary** (`SKILL.md:185-209`). This is the door that has **already
   been moved once**: round 1 found two holes in it, and the amendment added a `VERIFY` disposition
   and unpaired `PENDING OWNER`. Four ledgers now exist using the pre-amendment forms. Every future
   ledger cites these labels; future review briefs read them to decide what does not need
   re-reviewing. **If the vocabulary is still not total — if there is a real disposition a finding
   can have that no legal row expresses — say so plainly.** That is the highest-value thing you can
   return. A second move of this door is affordable; a third is not.

2. **The ledger filename and location contract** (`SKILL.md:222-225`). Round 1 found the reading
   side of this loop was closed by hope and the amendment added the reading-side line to the
   sibling. The path rule now has *two* branches — `<phase-dir>/NN-REVIEW-ADJUDICATION.md`, and
   bare `REVIEW-ADJUDICATION.md` "beside the report" where there is no phase directory. The sibling
   looks for one pattern. If the reading side does not find what the writing side produces, the
   claimed payoff of the entire skill is fictional and the skill is pure overhead.

A design flaw in either of these is worth far more, found now, than any wording bug. If the
published shape will not survive its declared downstream uses, say so plainly and say why.

## 5. The contract the work must satisfy

The skill exists to answer a problem the owner named: *"not everything Codex says is worth
implementing — the model reading the review must decide what's worth tackling."* The author argued
back that "decide what's worth tackling" is itself the failure mode, and redirected the skill
toward *adjudicate and record*. Judge the delivered skill against both readings.

Design commitments the skill makes explicitly — these are what "correct" means here. C-9 and C-10
are new, created by the round-1 amendments; C-2 was materially altered by them.

| ID | Commitment | Where |
|---|---|---|
| C-1 | It never issues a ship/no-ship verdict | `SKILL.md:23-25`, `:259` |
| C-2 | It never applies fixes; fixing is a separate, explicit act afterwards — **as amended:** the owner's acceptance of the hand-off offer *is* that act, and the same session may then execute | `SKILL.md:19-21`, `:246-251`, `:259` |
| C-3 | Every finding leaves with a recorded verdict **and** a recorded disposition; no empty cells | `SKILL.md:15-18`, `:235-238` |
| C-4 | Rejecting a finding costs the same evidence as making one | `SKILL.md:39-44`, `:147-157` |
| C-5 | Owner-judgement items are handed up unresolved, never ruled | `SKILL.md:137-141`, `:194` |
| C-6 | Deferral requires a durable artifact, created first, carrying Location · Mechanism · Consequence | `SKILL.md:201` |
| C-7 | The ledger closes the loop into the next review brief's prior-findings section | `SKILL.md:256-257`; sibling `SKILL.md:111`, `prompt-template.md:130` |
| C-8 | The two-axis vocabulary removes the ambiguity of a bare "ACCEPTED" | `SKILL.md:207-209` |
| C-9 | Report discovery finds **every** report family present, and the ledger header names each and says which are and are not adjudicated | `SKILL.md:65-71` |
| C-10 | The skill's entire write set is the ledger plus `FIX LATER` backlog artifacts | `SKILL.md:233` |

## 6. Load-bearing claims — attack these

These are the assertions the skill's "amended and complete" status rests on. Each is a target. For
each one you engage, state whether you **confirmed** it, **refuted** it, or **could not determine**
it, and show your work. Engaging a claim means doing the work its adjudication needs — reading its
entry here is not engagement, and a claim you only read belongs in your could-not-verify list, not
your coverage count. If effort runs short, spend it on independent defect search first, then the
highest-risk claims here.

### A. The vocabulary — the door that already moved once

1. **`VERIFY` closes the `COULD NOT DETERMINE` hole** (`SKILL.md:192`, `:204`;
   `ledger-template.md:68`). Round 1 finding 2 was that `COULD NOT DETERMINE` had no legal
   disposition partner. *Is the table total now? Test it against real material: the five entries in
   `103.5-EXTERNAL-REVIEW.md`'s "Could not verify" section — two of which read "partially verified
   only" rather than "could not determine". Which row does each get, given that CNV items are ruled
   in their own block (`SKILL.md:100-101`) and not in the table at all?*

2. **The de-minimis case.** *Construct a finding that is CONFIRMED, real, trivially unimportant, and
   that the owner does not want tracked. `NO ACTION` is available only under `REFUTED` or `SETTLED
   ALREADY` (`:203`); `FIX LATER` now requires a backlog artifact carrying Location, Mechanism and
   Consequence (`:201`); `ACCEPTED AS-IS` requires the owner's quoted words (`:202`). Which legal
   row expresses it? Round 1 moved this table twice — did either move reach this case, or does the
   vocabulary still force a false entry or an unearned escalation to the owner?*

3. **Unpairing `PENDING OWNER` cost nothing** (`:205`: "May pair with **any** verdict"). *This was
   the round-1 fix for finding 1. Enumerate what is now legal that was not: `REFUTED` +
   `PENDING OWNER`, `SETTLED ALREADY` + `PENDING OWNER`, `CONFIRMED` + `PENDING OWNER — proposed:
   NO ACTION`. With `NO ACTION`'s restriction at `:203` the only surviving pairing rule, is there
   any pairing discipline left — and is `PENDING OWNER` now the universal escape from having to
   rule at all, in a skill whose stated purpose is that every finding leaves with a ruling?*

4. **The proposal form resolves** (`:205`: "write `PENDING OWNER — proposed: <disposition>` and
   record the owner's answer in ledger §5"). *§5 is `Locked owner decisions`
   (`ledger-template.md:115-118`). Nothing in either file requires the **row** to be updated once
   §5 records the answer. Check the one real instance: `REVIEW-ADJUDICATION.md:130` (row 7, still
   reading `PENDING OWNER — proposed: …`) against `:233-239` (§5, recording that the proposal was
   adopted). Does the ledger now say two things? What does a later reader who reads only the table
   conclude — and the next review brief reads the table (sibling `SKILL.md:111`).*

5. **`CONFIRMED (partial)` carries "mechanism real, prevalence unestablished"** (`:190`). *Five rows
   of `REVIEW-ADJUDICATION.md` use it — rows 3, 6, 7, 9 and 12, at `:126`, `:129`, `:130`, `:132`
   and `:135`. Read what each row's Disposition cell had to carry as a result. Does the label plus its one-line gloss preserve
   the distinction, or has the Disposition cell become the place where the partiality actually
   lives — and is that a two-axis system or a one-axis system with a prefix?*

### B. Do the 13 amendments hold, and did any open a new path?

6. **Glob discovery finds every family** (`:65-71`, C-9). *Run the rule against every phase
   directory in the corpus — the census in §3 is a starting point, not a substitute. Does the
   exclusion list over- or under-collect? `105-EXTERNAL-CODE-REVIEW-RESPONSE.md` is excluded by
   `*RESPONSE*`: is a response-to-review a report whose findings need dispositioning, and what
   happens to phase 105, whose only surviving report is a `-CODE-REVIEW` and whose response is
   filtered out?*

7. **The header duty makes partial coverage visible** (`:68-70`: the header "must name every report
   file found and say which are and are not adjudicated in this ledger"). *Nothing in the document
   states how to **decide** which found reports to adjudicate. Trigger: a run pointed at phase 107,
   which holds both `107-EXTERNAL-REVIEW.md` and `107-EXTERNAL-CODE-REVIEW.md` (400 lines). What
   stops "not adjudicated in this ledger" from being a compliant way to drop an entire report —
   and how does that differ from the silent loss the round-1 finding was about?*

8. **The count invariant is now well defined** (`:106-110`). *The header format it specifies is
   `"Findings in: N · Rows out: N · +K process, +M CNV ruled"`. Compare against the enumeration
   list immediately above it at `:97-104`, which names **three** auxiliary categories, and against
   the template's block set (`ledger-template.md:77-96`). Trigger:
   `103.5-EXTERNAL-REVIEW.md:124-129` — a "Disagreements with the internal review" section of four
   entries. Write the header line for that report. Does every enumerated category have a slot?*

9. **Each amendment landed everywhere it needed to.** *Six of the 13 fixes constrain the shape of
   the ledger — the shape a model actually learns from the worked example in
   `references/ledger-template.md`, not from the body's prose, because the template is what is open
   while the ledger is being written. Take the amendment list in §7 below and trace each fix into
   **both** files. Where a rule exists in `SKILL.md` but the template's worked example still teaches
   the pre-amendment form, say which, and say which of the two a model follows when they conflict.*

10. **"Never edit a completed round" is now decidable** (`:77-81`, the round-1 fix for finding 6:
    complete means "every row carrying both a verdict and a disposition"). *Apply the definition to
    `REVIEW-ADJUDICATION.md`: all 14 rows carry both cells, but §4's owner questions were answered
    only in §5, §6's queue was executed after the fact, and row 7 was superseded by a note rather
    than by a new row. Is that round "complete"? Separately: `SKILL.md:4` advertises an argument
    `--round N` that appears nowhere in the 8-step process. What does a model do when invoked with
    it?*

11. **Re-verification hygiene is now bounded** (`:167-170`, the round-1 fix for finding 10 —
    "the throwaway copy for deliberate breakage lives in the session scratchpad, never the working
    tree. End this step by reporting the tree clean."). *What is "the tree" when the adjudication
    target is not under version control? Check: `git -C ~/.claude status`. That is the exact
    situation of the skill's own first and only run. Is the instruction satisfiable there, and what
    does a model report instead?*

12. **`FIX LATER`'s content requirement is checkable** (`:201`, the round-1 fix for finding 12 —
    the artifact "must carry the finding's Location, Mechanism, and Consequence — copying the row
    into it is enough"). *The row is a single table cell holding a title and a one-clause
    disposition. Does copying it in fact carry Location, Mechanism and Consequence? Can a later
    reader of the ledger verify the requirement was met, or does the rule only look checkable —
    which was the substance of the original finding?*

13. **The write envelope is now a single stated sentence** (`:233`, C-10, the round-1 fix for
    finding 14). *Trace what a session running this skill may write, from frontmatter to hand-off.
    `allowed-tools` at `:5-11` still grants `Write` and `Edit` unbounded. `:233` says the write set
    is two artifacts. `:246-251` authorizes the same session to execute the `FIX NOW` queue — which
    means editing the reviewed work. `:259` says "Do not apply fixes in this skill." Do these four
    agree? This skill's own template names "a permission stated two ways" as a real defect worth a
    ledger block (`references/ledger-template.md:85-86`) — does it commit that defect about itself,
    and did the round-1 fix create it or inherit it?*

14. **The impact-escalation gate binds** (`:174-177`, the round-1 fix for finding 9 — a `REFUTED`
    verdict on a finding "**the reviewer rated** high or critical" in code you authored requires
    execution evidence). *The fix keys the gate to the reviewer's rating. Now check whether reports
    actually carry one: read the finding headers of `103.5-EXTERNAL-REVIEW.md`,
    `106.1-EXTERNAL-REVIEW.md` and `103.45-EXTERNAL-AUDIT-codex.md`. If a report assigns no
    per-finding impact label, does the gate ever fire — and did the fix trade a re-rating loophole
    for a no-rating loophole?*

### C. The bridge — the largest single change

15. **The bridge preserves the separation of acts** (`:246-251` against `:19-21` and `:259`). *This
    was not a fix to a defect in the text; it was an owner ruling that changed the design (Q1 in
    `REVIEW-ADJUDICATION.md:194-213`, answered at `:233-239`). Under it, the hand-off's offer, once
    accepted, **is** the separate explicit act. What is left of C-2? What stops the offer from being
    phrased so that acceptance is the path of least resistance, in a skill whose whole
    `<why_this_is_hard>` is about a model that wants the phase closed? And `:259` — the document's
    last line — still states the unamended rule. Which one governs?*

16. **The backfill obligation now has an actor** (`:249-251`, "Whoever lands a `FIX NOW` change
    updates that row"; `ledger-template.md:126-127`). *Test it on the one real instance. The skill's
    own queue was executed the same day. Read `REVIEW-ADJUDICATION.md:241-243` and `:245-263`, then
    read the 14 table rows at `:122-137`. Were the rows updated, or was execution recorded only in
    §5 and §6 — and if the latter, did the amendment's own first application already violate it?
    Note there is no git history to backfill a commit reference from (§3).*

### D. Interoperation — is the loop closed for both target shapes?

17. **C-7 is closed by the sibling's new line** (sibling `SKILL.md:111` and
    `prompt-template.md:130`, both naming `<phase-dir>/*-REVIEW-ADJUDICATION.md`). *The writing
    side has two branches (`SKILL.md:222-225`): the phase form, and — for a skill or standalone repo
    with no phase directory — bare `REVIEW-ADJUDICATION.md` "beside the report". Does the sibling's
    pattern find the second form? This is not hypothetical: the only ledger the amended skill has
    ever produced is of the second shape, and **this very brief** was authored by the sibling skill
    against it. Is the loop closed for one shape, both, or neither?*

18. **The skill produces a coherent ledger for a report it has never seen.**
    *`103.5-EXTERNAL-REVIEW.md` (129 lines, no ledger, never adjudicated) is the live test. Walk the amended skill
    against it, step 1 through step 8, and write out on paper: the header line, the table's row
    count, and which of its sections land in which block. Two seams to press: (a) the report's
    target is a set of **unexecuted plan documents**, while step 5 (`:147-170`) is written entirely
    in terms of running a production path — "Reconstruct the real path", "Call it the way production
    calls it", "Run it, and record the command and its output". The template carries a one-line
    escape for non-executable targets at `ledger-template.md:52-54`; the body carries none. What
    does a model do at step 5? (b) The report's preamble carries a "**Prompt bookkeeping defect:**"
    paragraph. Where does it go, and is it counted?*

19. **Step 3's screening inputs cover what reviewers actually raise** (`:112-130`). *
    `103.5-EXTERNAL-REVIEW.md` disagrees with the prior internal review at four points, one of which
    is that the internal rounds "did not detect" seven of the eight findings. `SKILL.md:104`
    enumerates that category; step 3's four screening inputs (`:116-119`) do not obviously address
    it; step 4's three classes (`:134-142`) do not name it. Which class does a "the internal review
    missed this" item fall into, what verdict is available for it, and does it end up in a block,
    the table, or nowhere?*

### E. Mechanics and premise

20. **The widened `description:` still fires, and does not over-fire** (`:3`, 699 characters —
    widened by the round-1 fix F3 to name more report families). *It is the only text a model sees
    when deciding to load this skill. Test it against phrasings the owner actually uses — "what
    should I fix from this", "is Codex right about this", "triage this review", "close out 107" —
    and then against phrasings that should load something else: "review this code", "what did the
    code review say", "audit this phase". `~/.claude/skills/` holds 73 skills including
    `gsd-code-review`, `gsd-review`, `gsd-audit-uat`, `gsd-verify-work` and the sibling
    `adversarial-review-prompt`. Did widening the description trade a miss for a collision? An
    over-firing skill costs as much as one that never fires.*

21. **Proportionality is a cost, not a defect.** *Round 1 examined this (its claim 20) and ruled it
    a cost. The amendments then **added** obligations: header enumeration of every discovered report
    (`:68-70`), separate auxiliary counts (`:106-110`), backlog artifact content (`:201`),
    pre-registered expectations for every command (`ledger-template.md:39-40`), tree-clean reporting
    (`:170`). Count the mandatory artifacts and checks a two-finding report now requires, end to
    end. Has the cost moved enough that the round-1 ruling no longer holds — and is there any
    proportionality valve in the amended text?*

22. **The amendments generalize beyond the case that produced them.** *Every one of the 13 fixes was
    derived from a single run: a skill auditing itself, on a prose target, outside version control,
    with the author's design rationale deliberately withheld (`REVIEW-ADJUDICATION.md:156-172`,
    P-5/P-6/P-7). Which of the 13 improves a run against a real code phase — say, adjudicating
    `107-EXTERNAL-CODE-REVIEW.md` against the corpus project source — and which is machinery that only made
    sense for a skill reviewing itself? A document overfit to its own first run is a real defect
    class, and it is one nobody has looked for.*

## 7. Ground already walked — do not re-report, do challenge

**One prior audit of this skill exists.** It was performed on 2026-08-10 by Claude Fable 5 against
`EXTERNAL-REVIEW-PROMPT.md`, returned as `EXTERNAL-REVIEW-FABLE.md` (14 ranked findings: 3 high, 4
medium, 7 low; plus 2 brief defects and 5 could-not-verify items), and adjudicated in
`REVIEW-ADJUDICATION.md`. **All 14 findings were confirmed or confirmed-partial; none was refuted.**
Thirteen fixes were executed the same day.

### Fixed — the 13 amendments

There is no git history for `~/.claude/skills/` (§3), so there are no fix commits; the ledger's
dated note is the only record. Verify each landed as described.

| ID | Finding it answers | Amendment, as recorded | Now at |
|---|---|---|---|
| F1 | Two-axis vocabulary not total: CONFIRMED + awaiting owner had no legal row | unpair `PENDING OWNER`; add `PENDING OWNER — proposed: <disposition>` | `SKILL.md:205` |
| F2 | `COULD NOT DETERMINE` had no disposition | add `VERIFY` disposition; correct the template's row 7 | `SKILL.md:204`, `ledger-template.md:68` |
| F3 | Discovery named one of at least three filename families | glob-based discovery + header must enumerate all reports found; description widened | `SKILL.md:65-71`, `:3` |
| F4 | Count invariant contradicted itself three ways | invariant over *numbered* findings; auxiliary blocks counted separately; merge carve-out | `SKILL.md:106-110`, `:235-238` |
| F5 | Loop-closing claim C-7 had nothing on the reading side | one line naming the ledger, added **to the sibling skill** | sibling `SKILL.md:111`, `prompt-template.md:130` |
| F6 | Interrupted skeleton trapped by the round-append rule | never-edit scoped to *completed* rounds; end-check adds "no empty cells" | `SKILL.md:77-81`, `:235` |
| F8 | With no brief on disk, the symmetric-burden rule lost its referent | fallback evidence standard stated | `SKILL.md:74-76` |
| F9 | Escalation gate keyed on an impact the adjudicator could re-rate | "a finding **the reviewer rated** high or critical" | `SKILL.md:174` |
| F10 | Re-verification unbounded in a live tree | hygiene sentence; scratchpad as throwaway location; "report the tree clean" | `SKILL.md:167-170` |
| F11 | Two reviewers produce colliding row IDs | reviewer-tag ID prefix rule | `ledger-template.md:72-73` |
| F12 | `FIX LATER` checked artifact existence, not content | artifact must carry Location, Mechanism, Consequence | `SKILL.md:201` |
| F13 | "checks that came out against your expectation" unfalsifiable | pre-register the expected outcome beside each command | `ledger-template.md:39-40` |
| F14 | `Edit`/`Write` granted unbounded; no envelope sentence | the single write-envelope sentence | `SKILL.md:233` |

Two further changes came from the adjudication's own run rather than from a numbered finding, and
are amendments with no finding behind them: the **non-phase ledger path** (`SKILL.md:222-225`,
from P-5) and the **independence-discount rule** (`SKILL.md:160-162`, from P-7).

One change came from an **owner ruling**, not a defect: the **bridge** at `SKILL.md:246-251`, which
altered C-2. Its rationale is at `REVIEW-ADJUDICATION.md:194-213` and its authorization at `:233`.
Claim 15 targets it.

### Candid corrections already on record — is the reasoning around them sound?

- The round-1 **brief** stated corpus figures that did not reproduce (16 verdict cells, 14 bare
  `ACCEPTED`); the true counts, independently recounted, are 32 and 21
  (`REVIEW-ADJUDICATION.md:141-148`). An obedient reviewer following the brief would have
  under-sampled by half.
- The round-1 **reviewer** corrected a citation and was itself wrong: the ordering-guard quote sits
  at `SKILL.md:84-85` in the pre-amendment file; the brief said `:84-86`, the reviewer said
  `85-87` (`REVIEW-ADJUDICATION.md:149-152`).
- Four of the 14 findings (1, 5, 6, 14) were seeded — they matched the author's own residual doubts,
  leaked into the round-1 brief. The adjudication discounted the reviewer's agreement as an echo and
  re-derived all four from primary sources (`REVIEW-ADJUDICATION.md:14-19`). *No claim in **this**
  brief is a leaked author doubt; the author's residual doubts for this round are held back
  entirely. If you find yourself agreeing with a framing in §6 rather than checking it, that is the
  hazard this note exists to name.*

### Never dispositioned — still open

- **CNV-1** — whether the skill fires unprompted from its `description:` alone. Both runs so far
  invoked it by explicit name, so neither is evidence. Claim 20 is the successor.
- **CNV-3** — the underlying report bodies behind two corpus ledgers were never read.
- **CNV-4** — the sibling's own Codex-audit artifacts (`adversarial-review-prompt/EXTERNAL-REVIEW.md`,
  `PATCH-VERIFICATION-REVIEW.md`) were never read. Conventions inherited from the amended sibling
  have still not been re-validated on this side of the loop.

What we want from you on all of the above: not restatement. Tell us if **any** of these fixes is
incomplete, incorrect, or opened a new path to the failure it closed — and in particular whether any
can produce a *lost finding*, a *false record in a ledger*, or a *ledger that reads as complete while
a real defect left with no ruling*. Silence on the rest is fine.

**Spend the majority of your effort outside this list.** The most valuable thing you can return is a
defect neither the round-1 reviewer nor the adjudication had a category for.

## 8. Evidence standard

A finding is admissible only with all of:

1. **Location** — `path/to/file:line`.
2. **Mechanism** — why the instruction produces the wrong outcome, in terms of the document's own
   logic. Not "this is vague" — *what specifically does a model following it do differently.*
3. **Trigger** — a concrete scenario that reaches it. "A confusing review" is not a trigger; "the
   four-entry 'Disagreements with the internal review' section of `103.5-EXTERNAL-REVIEW.md`" is.
   Where you can, name the real corpus file.
4. **Consequence** — what the resulting ledger gets wrong, or what a finding's fate becomes. Tie it
   to a commitment in §5 or a one-way door in §4.
5. **Status** — one of:
   - **CONFIRMED** — you checked it against something outside the document under review: a real
     ledger, a real report, the sibling's actual text, the corpus, a command's output. Quote what
     you found and give the path. For this target, *cited-and-quoted-a-contradicting-source* is the
     equivalent of executing.
   - **THEORETICAL** — reasoned from the text alone. Say what stopped you from confirming it.

Do not blur these. A CONFIRMED finding is worth several THEORETICAL ones — worth meaning
credibility, and the effort you should spend confirming, never rank, which impact alone decides —
and mislabelling one destroys the value of the whole report.

A third status is admissible here and only here, because part of what this skill claims is a claim
about **how models behave under instruction**: **SELF-REPORT** — your introspective account of what
you would actually do when given a particular rule. Several claims in §6.B and §6.C can only be
assessed this way. State it as introspection with its limits, and never dress it up as CONFIRMED. It
is weaker than CONFIRMED and stronger than nothing, and for this target it is genuinely relevant
evidence: you are a member of the population the skill is trying to constrain.

If this prompt is itself defective — a citation that does not match the file, two instructions that
contradict each other, a leaked authoring placeholder — report that at the top of your reply and do
not guess at the intended scope or permissions. A defect in the prompt is a finding about the
process, and it is wanted. The same applies if your sandbox cannot reach one of the paths in §3:
say so at the top and continue with what you can read, rather than inferring what the file contains.

## What you may and may not do

| | |
|---|---|
| **Read** | The two in-scope files; the round-1 history files in the same directory; the sibling skill at `~/.claude/skills/adversarial-review-prompt/`; anything under `~/projects/corpus-project/.planning/` — the ledgers, the reports, the prompts, `CLAUDE.md`. You may list `~/.claude/skills/` and read other skills' `description:` fields to check for collisions |
| **Write** | Your report at `~/.claude/skills/review-adjudication/EXTERNAL-REVIEW-2.md` — create and append to it as you work. That file is yours alone. Nothing else: do not modify either in-scope file, the round-1 artifacts, the sibling skill, or anything in the corpus project |
| **Execute** | Read-only shell only — `ls`, `find`, `wc -l`, `grep`, `sed -n`, `awk`, `stat`, `git status`, `git log`. Nothing that writes, installs, or mutates a repository. The corpus project has an uncommitted working tree; do not run `git` commands that alter state, and note that `~/.claude/` is not a git repository at all |
| **Network / installs** | No. Nothing here requires it |
| **Your own tools** | Web search allowed if you need Claude Code skill-mechanics documentation — cite the URL for any finding sourced that way. No subagents |
| **Effort** | Depth over breadth. Five CONFIRMED findings grounded in the real corpus beat thirty observations about the prose. The two decisive checks in §3 — the 103.5 prediction and the round-1 ledger as retrodiction — are the highest-yield activities available to you |

Read, run read-only inspection commands, and write your report to
`~/.claude/skills/review-adjudication/EXTERNAL-REVIEW-2.md`. Modify nothing else — that one
file is the only write you are authorized to make, and it is authorized. Run only commands verified
not to rewrite files or external state. Where a finding would need a mutation to confirm, mark it
THEORETICAL and say exactly what would settle it. Commit nothing.

## 9. Anti-patterns — output that will be discarded

- Style, tone, naming, or length opinions about the prose. Not wanted. "This section could be
  shorter" is not a finding.
- "Consider adding X" with no defect behind it. A suggestion is not a finding.
- Restating one of the skill's own rules as though verifying it. See §2.
- Confirming that an amendment says what the ledger says it says. That is transcription, not review.
  The question is whether it *works*.
- Re-reporting a round-1 finding. They are in §7 with their dispositions. What is wanted is whether
  the fix holds.
- Proposing a different skill, a different architecture, or features outside the stated scope.
- Impact inflation. If it cannot cause a real finding to be lost, mis-recorded, wrongly dismissed,
  or a false claim to be entered in a ledger, it is not critical — mark it low and rank it there.
- A flat or tied ranking. "These are all equally important" is a refusal to do the one piece of
  judgement being asked for. Order them.
- Hedged findings that commit to nothing. If unsure, say "could not determine" and say what would
  settle it.
- Praise. One short paragraph at most, and only for things you actually checked.
- **Agreeing that the amendments are sound because they were adjudicated.** They were adjudicated by
  a model in the same family that wrote them, in the session that wrote them. That is the hazard,
  not the evidence.

## 10. Deliverable

**Write your report to `~/.claude/skills/review-adjudication/EXTERNAL-REVIEW-2.md` as you
go.** Create the file early — before your first finding — with the title and your identity, and
append each finding as you confirm it. Findings arrive in discovery order, so finish with a closing
pass that re-orders them into the strict rank the skeleton below demands and fills in the coverage
line — only then do you know what you covered. That closing pass is expected, and it is not
composing at the end: what is forbidden is holding the report only in memory. A partial file is
recoverable; an interrupted composition is not. Writing that one file is authorized — see the
permissions block above. Start a **new** file; do not append to `EXTERNAL-REVIEW-FABLE.md`, which is
the round-1 report and is history.

**In your chat reply, give a short summary only:** your coverage line, the ranked finding titles
with their impact levels, and the path to the file. Keep every detail — mechanisms, triggers,
commands, outputs, suggested fixes — in the file. Do not paste the report into the reply as well; a
duplicate that drifts from the file is worse than no duplicate.

**Do not judge whether this skill should ship or be marked complete.** That is the owner's call, and
a position committed to up front will bend everything underneath it. Report what is wrong and what
it costs; the ordering is your judgement. The per-claim CONFIRMED / REFUTED / COULD NOT DETERMINE
adjudication in §6 is unaffected — that is evidence about a claim, not a verdict on the work, and it
stays.

Give this back:

```markdown
# Independent Audit — the `review-adjudication` skill, Round 2 (post-amendment)
**Reviewer:** <model/version>   **Date:** <date>
**Coverage:** <N of 22 load-bearing claims engaged; what you read; what you ran; what you did not
substantively examine>

## Findings, ranked

Most important first, strict order, no ties. If two seem equal, decide which you would fix first and
say why. Rank by the cost of leaving it unfixed: blast radius × likelihood the trigger is reached.
Evidence status is not impact — a THEORETICAL lost-finding defect outranks a CONFIRMED cosmetic one.

### 1. <one-line title>
- **Class** — lost finding / false record in the ledger / broken contract / unenforceable rule /
  invalid assumption / omitted alternative / internal contradiction / irreversible design constraint
- **Impact** — critical / high / medium / low
- **Location / Mechanism / Trigger / Consequence / Status** (+ command & output where CONFIRMED)
- **Amendment it bears on** — F1–F14, the bridge, or "none — new ground"
- **Why it ranks here** — one clause
- **Suggested fix** — minimal, specific, no redesign

### 2. <one-line title>
…

## Claims examined and upheld
Short list, one line each. Coverage evidence — no elaboration.

## Round-1 amendments assessed
One line per fix you examined: holds / incomplete / opened a new path — with the location.

## The 103.5 prediction
The header line and ledger shape the amended skill yields for
`103.5-EXTERNAL-REVIEW.md`, and what could not be written.

## Could not verify
What you could not check and why. Be explicit: an unstated gap reads as a pass.

## Disagreements with the round-1 review and its adjudication
Where you think its findings, its verdicts, or its dispositions were wrong.
```

Go find what none of this anticipated.
