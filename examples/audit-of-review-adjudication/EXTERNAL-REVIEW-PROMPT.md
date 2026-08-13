# Adversarial Independent Audit — the `review-adjudication` skill

> **Prompt for an external reviewer (Claude Fable 5).** Hand this file to a model that did **not**
> write the skill under review. Everything below is written to be read by that reviewer, not by
> the author.

---

## 1. Why you are here

The work you are auditing is a Claude Code *skill* — a set of instructions that a future model
loads and follows. It was written by Claude Opus 5 in a single session, in response to a user who
asked for it, reviewed by that same model, and declared complete by that same model. No one else
has read it. It has never been run.

A caution about your own independence, stated plainly because overclaiming it would be its own
defect: you are a Claude model too. You do not have a different architecture and a different
training corpus from the author in the way a Codex or Gemini reviewer would, and you share priors
with it about what good instructions look like. **That makes agreement cheaper here, not more
meaningful.** What you genuinely do have is the two things that matter most: you did not write
this, and you do not have the conversation that produced it — the arguments the author made, the
framing it committed to early, the design it talked itself into. Those commitments are invisible
to the author and visible to you only as text that has to stand on its own.

So the bar is higher than usual:

- **Confirmation is near-worthless output.** If you spend your effort re-deriving what the
  document already claims and agreeing that it is well-reasoned, this audit has failed. A
  same-family reviewer producing a warm summary is the single most likely bad outcome here.
- **Your job is to find what is wrong, missing, or unjustified**, and to prove it from the text.
- **A manufactured finding is worse than no finding.** If a rigorous search comes back nearly
  empty, say so and show the search. Few or zero findings is an admissible result, and the
  claims-examined-and-upheld section is where it earns its credibility.
- **A finding that survives your own attempt to refute it is worth more than ten observations.**
  Try to break your own findings before writing them down.

Assume competence, not correctness. The skill is carefully built and its author had good reasons
for most of it. Where it is wrong, it is wrong in ways its author cannot see.

One structural note about the target that is unusual and important: **this skill's failure mode is
silent.** A defective build script fails loudly. A defective set of instructions produces a
plausible-looking document that omits something, and nobody notices, because the artifact it
produces is the only record of what it was supposed to produce. Weight your attention accordingly.

## 2. The single most important instruction

**This document argues for its own correctness, at length and persuasively. Treat every one of
its assertions as a claim by the party under review, never as evidence.**

The skill is written in a confident, aphoristic register that is very good at making a rule sound
like it has already been validated. Real examples, quoted verbatim:

> "A `FIX LATER` with no artifact is a drop wearing a deferral label, and is not permitted."
> — `SKILL.md:181`

> "**Count in = count out.** The ledger's row count must equal the report's finding count."
> — `SKILL.md:96`

> "**The refutation carries the same burden as the finding.**" — `SKILL.md:42`

> "This ordering is the guard against the most common real-world drift: the easy findings get
> fixed, the hard ones get forgotten, and the ledger records only what was convenient."
> — `SKILL.md:84-86`

> "The split is the discipline." — `SKILL.md:132`

> "Never write a bare 'ACCEPTED.'" — `SKILL.md:186`

For each of these, the question is not whether it sounds right. It is: **what actually stops a
model from doing the forbidden thing?** These are instructions to a future instance of the same
kind of model that wrote them, operating under exactly the pressure the skill says it is guarding
against — mid-phase, wanting the phase closed. An instruction that a motivated model can satisfy
in letter while defeating in spirit is not a guard; it is a sentence.

Where a rule's enforcement is only that the rule was stated, that is a finding — and it is a
severe one, because the entire value proposition of this skill over just-asking-Claude is that it
*binds*.

The same treatment applies to the causal claims. "This ordering is the guard against…" asserts a
mechanism. Ask whether the mechanism actually connects: does writing a skeleton to disk first, in
fact, prevent the hard findings from being forgotten — or does it only ensure that their titles
survive while their verdicts stay empty?

## 3. Governing sources and how to check things

There is no test suite here. The skill is prose. But this is **not** a paper-only audit — there is
a real corpus to check it against, and findings grounded in it are worth far more than findings
grounded in reasoning about the text.

| | |
|---|---|
| **The skill under review** | `~/.claude/skills/review-adjudication/` |
| **Its sibling, which it is designed to pair with** | `~/.claude/skills/adversarial-review-prompt/` |
| **The real corpus it was derived from** | `~/projects/corpus-project/.planning/` |
| **Skill mechanics reference** | `~/.claude/skills/<name>/SKILL.md`; the YAML `description:` field is the *only* text a model sees when deciding whether to load the skill; `allowed-tools:` is an optional whitelist active while it runs |

**The decisive check available to you** is retrodiction: the skill claims to codify a practice the
user was already performing by hand. Three real ledgers exist. Read them, and ask whether the
skill as written would have produced them — and, more sharply, whether its vocabulary can even
*express* what those ledgers needed to say.

```
.planning/phases/103.46-loose-re-import-alpha-convention-inserted/103.46-REVIEW-ADJUDICATION.md   (97 lines, 10 rows, 2 rounds)
.planning/phases/106.1-accounting-recount-advisory-correction-v2-1-inserted/106.1-REVIEW-ADJUDICATION.md  (152 lines, 7 rows)
.planning/phases/107-slot-render-pose-correctness-v2-1/107-REVIEW-ADJUDICATION.md   (43 lines, 9 rows)
```

Their source reports sit beside them as `NN-EXTERNAL-REVIEW.md`. Verified facts about that corpus,
which you may rely on but should spot-check:

- Across all existing ledgers, the verdict label distribution is: **14 bare `**ACCEPTED**`**, 1
  `**ACCEPTED (partially)**`, 1 `**ACCEPTED, resolved differently than suggested**`. The skill at
  `SKILL.md:186` forbids the bare form outright.
- 103.46 and 107 both have ledger row counts exactly equal to their report's finding counts (10/10
  and 9/9). 106.1 uses a different finding-ID scheme (`F-1`…`F-7`) and a different table header
  (`# | Finding | Verdict | Reason` — no Class, no Disposition column).
- The three ledgers use three *different* table headers. No two agree.
- Review reports in this project exist under **two** naming families: `NN-EXTERNAL-REVIEW.md` and
  `NN-EXTERNAL-CODE-REVIEW.md`. The latter appears in phases 105, 107 and 103.46 and comes from a
  different tool. Phase 105 ran five review-prompt rounds (`-PROMPT`, `-R2` … `-R5`) and has no
  `NN-EXTERNAL-REVIEW.md` at all.
- Of the distinct review targets that produced a report on disk, roughly half have a ledger.

Project-specific context the skill leans on, which you should verify rather than assume:
`corpus-project/CLAUDE.md` contains a "Critical non-obvious facts (do not relitigate)"
block that `SKILL.md:104` cites by name as a screening input.

## 4. Scope

**In scope** — the whole of the new skill, 387 lines:

| File | Lines | What it is |
|---|---|---|
| `~/.claude/skills/review-adjudication/SKILL.md` | 230 | frontmatter, `<objective>`, `<why_this_is_hard>`, an 8-step `<process>` |
| `~/.claude/skills/review-adjudication/references/ledger-template.md` | 157 | the output document's skeleton, loaded only when the body links to it |

**Also in scope, as the contract this must fit:** the sibling skill
`~/.claude/skills/adversarial-review-prompt/SKILL.md` (315 lines) and its
`references/prompt-template.md` (335 lines). You are not auditing the sibling. You *are* auditing
whether the new skill's claims about interoperating with it are true.

**Out of scope:** the the corpus project application itself, its source, its phases, and the
correctness of any past adjudication decision recorded in the corpus. Do not review absent work
and do not propose features. Read the corpus as evidence about the skill, not as a target.

### The one-way doors — spend disproportionate attention here

Two things in this design become expensive to change later, and a flaw found now is worth more
than any wording bug:

1. **The verdict/disposition vocabulary** (`SKILL.md:165-184`). Once ledgers are written with these
   labels, they are cited by later phases, read by future review briefs, and — per the design —
   used to decide what does not need re-reviewing. Changing the vocabulary later means either
   rewriting history or holding two incompatible vocabularies at once. **If this vocabulary is not
   total — if there is a real disposition a finding can have that no legal row can express — say
   so plainly.** That is the highest-value thing you can return.

2. **The ledger filename and location contract** (`SKILL.md:201-202`,
   `<phase-dir>/NN-REVIEW-ADJUDICATION.md`). The claimed payoff of the whole skill is that the next
   review brief reads this file so findings are not re-found. If the path convention does not match
   what actually exists, or if nothing on the reading side ever looks for it, the payoff is
   fictional and the skill is pure overhead.

## 5. The contract the work must satisfy

The skill exists to answer a specific problem the user named: *"not everything Codex says is worth
implementing — the model reading the review must decide what's worth tackling."* The author argued
back that framing it as "decide what's worth tackling" is the failure mode, and redirected the
skill toward *adjudicate and record*. Judge the delivered skill against both readings: it should
solve the user's actual problem, and if the redirect was wrong, the redirect is itself the finding.

Design commitments the skill makes explicitly — these are what "correct" means here:

| ID | Commitment | Where |
|---|---|---|
| C-1 | It never issues a ship/no-ship verdict | `SKILL.md:23-25`, `:228` |
| C-2 | It never applies fixes; fixing is a separate act afterwards | `SKILL.md:19-21`, `:228` |
| C-3 | Every finding leaves with a recorded verdict **and** a recorded disposition | `SKILL.md:15-17` |
| C-4 | Rejecting a finding costs the same evidence as making one | `SKILL.md:39-45`, `:137-139` |
| C-5 | Owner-judgement items are handed up unresolved, never ruled | `SKILL.md:126-129`, `:218-220` |
| C-6 | Deferral requires a durable artifact that exists before the ledger is written | `SKILL.md:181` |
| C-7 | The ledger closes the loop into the next review brief's prior-findings section | `SKILL.md:224-226` |
| C-8 | The two-axis vocabulary removes the ambiguity of a bare "ACCEPTED" | `SKILL.md:186-190` |

## 6. Load-bearing claims — attack these

These are the assertions the skill's "complete" status rests on. Each is a target. For each one you
engage, state whether you **confirmed** it, **refuted** it, or **could not determine** it, and show
your work. Engaging a claim means doing the work its adjudication needs — reading its entry here is
not engagement, and a claim you only read belongs in your could-not-verify list, not your coverage
count. If effort runs short, spend it on independent defect search first, then the highest-risk
claims here.

### A. Vocabulary and contract — the one-way door

1. **The two-axis system is claimed to strictly improve on the corpus's bare "ACCEPTED"**
   (`SKILL.md:161-190`, C-8). *Take all 16 verdict cells in the three existing ledgers and re-encode
   them in the new vocabulary. Does every one survive? 103.46's row 5 reads `**ACCEPTED** (defect
   is real, pre-existing, cheap to fix in a site this phase already owns)` — which cell pair is
   that, and is anything lost?*

2. **`NO ACTION` is available only under `REFUTED` or `SETTLED ALREADY`** (`SKILL.md:183`).
   *Construct a finding that is CONFIRMED, real, trivially unimportant, and that the owner does not
   want tracked. Which legal row expresses it? `ACCEPTED AS-IS` requires the owner's quoted words
   (`:182`), `FIX LATER` requires a backlog artifact (`:181`). Is the vocabulary total, or does it
   force a false entry?*

3. **`COULD NOT DETERMINE` has no disposition partner.** The verdict table lists it (`:172`); the
   disposition table (`:180-184`) contains no matching row, and `NO ACTION` is explicitly closed to
   it. *What does the adjudicator write in that cell? Is this a hole in a table that claims to be a
   contract?*

4. **`CONFIRMED (partial)` is claimed to carry "mechanism real, prevalence unestablished"**
   (`:170`). *Compare against the real instance in 103.46 — `ACCEPTED (partially) — mechanism
   source-settled, prevalence unmeasured`. Does the label plus its one-line gloss preserve enough,
   or does the information now live only in prose that the label implies is unnecessary?*

5. **No pairing rule is stated beyond `NO ACTION`'s.** *Enumerate the illegal or nonsensical
   verdict/disposition pairs the tables permit — e.g. `REFUTED` + `FIX NOW`, `SETTLED ALREADY` +
   `FIX LATER`, `OWNER RULING REQUIRED` + `FIX NOW`. Is the absence of a full pairing matrix a
   defect, or is it correctly leaving room for real cases?*

### B. Do the anti-dismissal rules actually bind?

6. **"The refutation carries the same burden as the finding"** (`SKILL.md:42`, C-4). *The brief
   demands five named parts for a finding — Location, Mechanism, Trigger, Consequence, Status. What
   does the skill actually demand for a refutation? Trace it through to the ledger template's
   REFUTED row, which asks for "the evidence, with the command; not the reasoning". Is that the
   same burden, or a weaker one wearing the same name?*

7. **Self-authored high-impact refutations require execution evidence, else the verdict drops to
   `COULD NOT DETERMINE`** (`SKILL.md:155-157`). *Impact is assigned by the reviewer. Nothing in the
   skill forbids the adjudicator from disagreeing with the assigned impact. Can a model escape this
   rule by re-rating a finding from high to medium, and is there any guard? If there is not, is
   this rule load-bearing or decorative?*

8. **`FIX LATER` requires a durable backlog artifact created before the ledger is written, path
   quoted** (`SKILL.md:181`, C-6). *Nothing specifies the artifact's content. Does creating an empty
   or one-line file satisfy the rule as written? Is the rule checkable by anyone reading the ledger
   afterwards, or does it only look checkable?*

9. **"Count in = count out", with merging permitted by an explanatory note** (`SKILL.md:96-99`,
   C-3). *Is the merge clause an unbounded escape hatch? What, in the text, stops seven findings
   from becoming two rows with a sentence of justification — and would the resulting ledger still
   satisfy the stated invariant?*

10. **Enumerate-first is claimed to guard against fix-easy-forget-hard** (`SKILL.md:79-96`). *The
    skeleton is written to disk before judging. The only stated end-check is a count
    (`SKILL.md:209-211`). A row can exist with an empty verdict. Does the guard actually catch a
    run that stalls, runs out of context, or is interrupted halfway — the exact scenarios the
    sibling skill's append-as-you-go design exists to survive?*

11. **`SETTLED ALREADY` is gated by a citation requirement, and "new evidence reopens it"**
    (`SKILL.md:100-118`). *Who judges whether the evidence is new? The same actor, with the same
    incentive to close the phase. Is this gate self-adjudicated, and if so does the citation
    requirement do any real work beyond adding a step?*

12. **The three forces in `<why_this_is_hard>` (`SKILL.md:28-57`) are asserted as the operative
    ones.** *Is any major dismissal pathway unnamed? Consider in particular: a finding the
    adjudicator does not understand, and the "the reviewer misread the code" ruling — which is the
    most natural way to dispose of something confusing and is not addressed anywhere in the skill.*

### C. Does it actually interoperate?

13. **Report discovery assumes `NN-EXTERNAL-REVIEW.md`** (`SKILL.md:65`). *The real corpus contains
    a second family, `NN-EXTERNAL-CODE-REVIEW.md`, in at least three phases, produced by a
    different tool. Does the skill find those? If a phase has both, what happens — one ledger, two,
    or one that silently covers half the findings?*

14. **C-7, the loop-closing claim** (`SKILL.md:224-226`): the ledger feeds the next brief's
    prior-findings section. *Read the sibling's §4 (`adversarial-review-prompt/SKILL.md`, "Inventory
    the ground already walked") and its template's §7. Do they name `NN-REVIEW-ADJUDICATION.md`, or
    any file? If nothing on the reading side looks for this artifact, is the loop closed by design
    or by hope — and what would actually close it?*

15. **Multiple reviewers adjudicate into one ledger** (`SKILL.md:73-76`). *The sibling deliberately
    gives each reviewer its own report path so runs cannot overwrite each other. Two reports both
    number their findings 1..N. What is the row `#` for the second reviewer's finding 3? The skill
    says to keep the reviewer's numbering (`ledger-template.md`, §3 note). Do these two instructions
    collide?*

16. **C-2, the no-fixing boundary** (`SKILL.md:19-21`). *The FIX NOW queue is executed later by a
    session operating under none of these constraints. Did the separation remove the failure mode
    or relocate it? Is there anything that makes the second session honor the ledger — and what
    happens to a ledger row whose fix is never executed and never marked?*

### D. Skill mechanics — will it even fire, and can it be trusted with its tools?

17. **The `description:` field** (`SKILL.md:3`, 629 characters) is the only text a model sees when
    deciding to load this skill. *Test it against the phrasings the user actually uses — "what
    should I fix from this", "is Codex right about this", "triage this review", "close out 107". Does
    it fire? Does it collide with the sibling skill's description, or with a `gsd-code-review` skill
    that exists in the same directory and reviews code changes directly?*

18. **`allowed-tools` grants `Write` and `Edit`** (`SKILL.md:5-11`) while the body states the only
    writes are the ledger and backlog artifacts (`SKILL.md:19-21`, `:206-211`). *The skill itself
    treats "a permission stated two ways" as a reportable defect when it appears in a review brief.
    Does it commit that defect in its own frontmatter? What stops a model with `Edit` from fixing
    the code it just confirmed is broken?*

19. **`Bash` is granted for re-verification, unbounded** (`SKILL.md:5-11`, `:135-152`). *The sibling
    brief explicitly names snapshot-updating test runners and cache-writing builds as writes that a
    read-only reviewer must withhold. This skill's re-verification section names no such
    restriction, while instructing the model to "reconstruct the real path" and "break it
    deliberately" (`:148-151`). Where does the deliberate breaking happen, and what restores it?*

### E. Premise

20. **The premise that a per-finding recorded disposition is the missing artifact.** *Roughly half
    the review targets in the corpus have a ledger. The skill reads that as a gap. Is it? Consider
    the alternative: adjudication was correctly skipped where the review was small or its findings
    self-evident. What does this skill cost on a report with two findings, and does it have any
    proportionality valve?*

21. **The machine-checkable / owner-judgement split is asserted to be decidable** (`SKILL.md:120-133`,
    C-5). *Work the hard middle: a finding whose defect is undisputed and whose only open question
    is whether the fix is worth its cost. Is that machine-checkable, owner-judgement, or both? If
    the split mis-sorts the most common real case, "the split is the discipline" (`:132`) is
    load-bearing on something that does not hold.*

22. **The ledger template asks for checks "that came out against your expectation"**
    (`references/ledger-template.md:35-51`, §2). *This is unfalsifiable — an absent list is indistinguishable from
    having had no wrong expectations. Is there a version of this instruction with teeth, and is its
    current form actively harmful in that it lets a section look rigorous while containing nothing?*

## 7. Ground already walked

**No prior review of this skill has been performed. You are the first reviewer.** It was written,
self-reviewed, and handed over within a single session on 2026-08-10.

Two pieces of history that are context, not prior findings, and that you should not treat as
already-covered ground:

- The **sibling** skill (`adversarial-review-prompt`) was itself audited by Codex in August 2026 —
  ten findings, nine accepted amendments plus one addition, then a verification pass. That audit's
  artifacts sit in `adversarial-review-prompt/EXTERNAL-REVIEW.md` and
  `PATCH-VERIFICATION-REVIEW.md`. The new skill inherits several conventions from the amended
  sibling without those conventions having been re-validated in the new context. *Whether an
  inherited convention still holds on this side of the loop is fair game and is not covered
  ground.*
- The author recorded, in conversation, that the user's original framing ("a skill that decides
  what's worth tackling") was rejected in favor of "adjudicate and record". That argument has not
  been reviewed by anyone.

## 8. Evidence standard

A finding is admissible only with all of:

1. **Location** — `path/to/file:line`.
2. **Mechanism** — why the instruction produces the wrong outcome, in terms of the document's own
   logic. Not "this is vague" — *what specifically does a model do differently because of it.*
3. **Trigger** — a concrete scenario that reaches it. "A confusing review" is not a trigger; "a
   report with findings under both `NN-EXTERNAL-REVIEW.md` and `NN-EXTERNAL-CODE-REVIEW.md` in
   phase 107" is. Where you can, name the real corpus file.
4. **Consequence** — what the resulting ledger gets wrong, or what a finding's fate becomes. Tie it
   to a commitment in §5 or a one-way door in §4.
5. **Status** — one of:
   - **CONFIRMED** — you checked it against something outside the document: a real ledger, a real
     report, the sibling skill's actual text, the corpus. Quote what you found and give the path.
     For this target, *cited-and-quoted-a-contradicting-source* is the equivalent of executing.
   - **THEORETICAL** — reasoned from the text alone. Say what stopped you from confirming it.

Do not blur these. A CONFIRMED finding is worth several THEORETICAL ones — worth meaning
credibility, and the effort you should spend confirming, never rank, which impact alone decides —
and mislabelling one destroys the value of the whole report.

A third status is admissible here and only here, because part of what this skill claims is a claim
about **how models behave under instruction**: **SELF-REPORT** — your introspective account of what
you would actually do when given a particular rule. Several claims in §6.B can only be assessed
this way. State it as introspection with its limits, and never dress it up as CONFIRMED. It is
weaker than CONFIRMED and stronger than nothing, and for this target it is genuinely relevant
evidence: you are a member of the population the skill is trying to constrain.

If this prompt is itself defective — a citation that does not match the file, two instructions that
contradict each other, a leaked authoring placeholder — report that at the top of your reply and do
not guess at the intended scope or permissions. A defect in the prompt is a finding about the
process, and it is wanted.

## What you may and may not do

| | |
|---|---|
| **Read** | The two in-scope files; the sibling skill at `~/.claude/skills/adversarial-review-prompt/`; and anything under `~/projects/corpus-project/.planning/` — the ledgers, the review reports, the prompts, `CLAUDE.md`. You may also list `~/.claude/skills/` to check for description collisions |
| **Write** | Your report at `~/.claude/skills/review-adjudication/EXTERNAL-REVIEW-FABLE.md` — create and append to it as you work. Nothing else: do not modify either in-scope file, the sibling skill, or anything in the corpus project |
| **Execute** | Read-only shell only — `ls`, `wc -l`, `grep`, `find`, `git log`, `git status`, `stat`. Nothing that writes, installs, or mutates a repository. The corpus project has an uncommitted working tree and a Codex review actively running in it; do not run `git` commands that alter state |
| **Network / installs** | No. Nothing here requires it |
| **Your own tools** | Web search allowed if you need Claude Code skill-mechanics documentation — cite the URL for any finding sourced that way. No subagents |
| **Effort** | Depth over breadth. Five CONFIRMED findings grounded in the real corpus beat thirty observations about the prose. The retrodiction check in §3 is the highest-yield single activity available to you |

Read, run read-only inspection commands, and write your report to
`~/.claude/skills/review-adjudication/EXTERNAL-REVIEW-FABLE.md`. Modify nothing else —
that one file is the only write you are authorized to make, and it is authorized. Where a finding
would need a mutation to confirm, mark it THEORETICAL and say exactly what would settle it. Commit
nothing.

## 9. Anti-patterns — output that will be discarded

- Style, tone, naming, or length opinions about the prose. Not wanted. "This section could be
  shorter" is not a finding.
- "Consider adding X" with no defect behind it. A suggestion is not a finding.
- Restating one of the skill's own rules as though verifying it. See §2.
- Proposing a different skill, a different architecture, or features outside the stated scope.
- Impact inflation. If it cannot cause a real finding to be lost, mis-recorded, wrongly dismissed,
  or a false claim to be entered in a ledger, it is not critical — mark it low and rank it there.
- A flat or tied ranking. "These are all equally important" is a refusal to do the one piece of
  judgement being asked for. Order them.
- Hedged findings that commit to nothing. If unsure, say "could not determine" and say what would
  settle it.
- Praise. One short paragraph at most, and only for things you actually checked.
- **Agreeing that the design is sound because it is well-argued.** The document is well-argued. That
  is the hazard, not the evidence.

## 10. Deliverable

**Write your report to `~/.claude/skills/review-adjudication/EXTERNAL-REVIEW-FABLE.md` as
you go.** Create the file early — before your first finding — with the title and your identity, and
append each finding as you confirm it. Findings arrive in discovery order, so finish with a closing
pass that re-orders them into the strict rank the skeleton below demands and fills in the coverage
line — only then do you know what you covered. That closing pass is expected, and it is not
composing at the end: what is forbidden is holding the report only in memory. A partial file is
recoverable; an interrupted composition is not. Writing that one file is authorized — see the
permissions block above.

**In your chat reply, give a short summary only:** your coverage line, the ranked finding titles
with their impact levels, and the path to the file. Keep every detail — mechanisms, triggers,
quotes, suggested fixes — in the file. Do not paste the report into the reply as well; a duplicate
that drifts from the file is worse than no duplicate.

**Do not judge whether this skill is ready to use.** That is the owner's call, and a position you
commit to up front will distort everything under it. Report what is wrong and what it costs; the
ordering is your judgement.

```markdown
# Independent Audit — the `review-adjudication` skill
**Reviewer:** <model/version>   **Date:** <date>
**Coverage:** <N of 22 load-bearing claims engaged; which files you read; which corpus ledgers you
checked; what you did not substantively examine>

## Findings, ranked
Most important first, strict order, no ties. If two seem equal, decide which you would fix first
and say why. Rank by the cost of leaving it unfixed: how badly a real finding gets lost or
misrecorded × how often the trigger is actually reached. Evidence status is not impact — a
THEORETICAL vocabulary hole that loses findings outranks a CONFIRMED typo.

### 1. <one-line title>
- **Class** — lost finding / wrongly dismissed finding / false record in the ledger / broken
  contract with the sibling skill / unenforceable rule / invalid assumption / omitted alternative /
  irreversible design constraint
- **Impact** — critical / high / medium / low
- **Location / Mechanism / Trigger / Consequence / Status** (+ the quote and path if CONFIRMED)
- **Why it ranks here** — one clause
- **Suggested fix** — minimal, specific, no redesign

### 2. <one-line title>
…

## Claims examined and upheld
Short list, one line each, keyed to the §6 numbering. Coverage evidence — no elaboration.

## Could not verify
What you could not check and why. Be explicit: an unstated gap reads as a pass.

## Retrodiction results
The §3 check, as a table: for each of the three real ledgers, would the skill as written have
produced it, and does the new vocabulary encode every row it contains?
```

Go find what none of this anticipated.
