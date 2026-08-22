# Round 6 hand-off — read this before adjudicating `EXTERNAL-REVIEW-6-GROK.md`

> **STATUS: the report has landed.** `EXTERNAL-REVIEW-6-GROK.md` is in the repository root,
> complete — coverage line, closing rank, `## Mutation results` table, CNV section. 20 of 20 claims
> engaged, **51 mutation probes**, 15 findings (4 high · 8 medium · 3 low), 2 of them unseeded and
> 1 process. **Nothing in it has been adjudicated.** §3's doubt outcomes below are the reviewer's
> claims, recorded as leads — not rulings.

Written 2026-08-22 by the session that adjudicated round 5, executed its fixes, and commissioned
round 6. **Not a review, not a ledger.** It exists because the next session cannot reconstruct any
of it, and round 5 was damaged by exactly this kind of thing living only in a chat window.

> **Leak warning for whoever writes the next brief.** §3 below is a residual-doubts list. It is on
> disk because the round-6 reviewer was already running when it was written and reads from
> `/private/tmp/r6/audit`, not from this repository — so it cannot reach that reviewer. **Any
> future brief must exclude this file from the reviewer's read scope, or treat these doubts as
> spent and score nothing against them.**

## 1. What is in flight

A Grok 4.6 audit of the previously-unaudited half — validator, ledger, calibration corpus.

| | |
|---|---|
| Brief | `EXTERNAL-REVIEW-6-PROMPT-GROK.md` (in this repo, and copied into the audit tree) |
| Cover note | `EXTERNAL-REVIEW-6-COVER-NOTE-GROK.md` |
| Reviewer | xAI Grok 4.6, `--reasoning-effort high`, headless `grok --prompt-file`, `--permission-mode acceptEdits` |
| Runs in | `/private/tmp/r6/audit` — a **disposable copy**, not this working tree |
| Report lands at | `/private/tmp/r6/audit/EXTERNAL-REVIEW-6-GROK.md` |
| Run log | `/private/tmp/r6/grok-run.log` and the task output under the session's `tasks/` dir |
| Repo backup | `/private/tmp/r6/repo-backup-before-grok.tgz`, taken before the run |

**To bring the report back:**

```bash
cp /private/tmp/r6/audit/EXTERNAL-REVIEW-6-GROK.md \
   /Users/leo/Documents/WORK/CODING/adversarial-review-skills/
```

**Check it finished** before adjudicating: a coverage line, a closing rank, and a `## Mutation
results` table. If it stops mid-sentence the findings still stand and its silence covers nothing.

**Why the audit tree has a commit this repo does not.** The round-5 fixes are **still uncommitted
here**. To give the reviewer an immutable, pinnable range, they were committed *in the copy only*
as `c62ca24`. The brief pins `2565c08..c62ca24` and says so plainly. Nothing was committed in this
repository. If the fixes get committed here later, the hash will differ — that is expected and the
brief already discloses it.

## 2. The independence problem with round 6, stated plainly

**This brief was written by the adjudicator, not by `adversarial-review-prompt`.** That is worse
than round 5's problem, not better, and the round-6 ledger header must say so:

- All 20 load-bearing claims were chosen by the session that had just written the code under audit.
- **Three of them are defects that session found in its own work** — claim 2 (the two new validator
  checks were never break-tested), claim 7 (the registry says 13, the run says 12), and claim 19
  (the append rule was rewritten by the session that then edited rows under the rewrite).
- So the echo discount is near-total. **Almost nothing Grok returns against those 20 claims is
  independent.** The unseeded pass (§4b of the brief) is where round 6's real evidence lives, and
  it should be weighted accordingly.
- The brief's §0 and the cover note both disclose this to the reviewer in as many words. That does
  not remove the problem; it just means the reviewer was told.

## 3. Residual doubts — the adjudicator's own, pre-registered

These are what that session was privately unsure about after executing nineteen fixes. Ranked by
how much damage each would do if true. **A finding that lands on one of these is an echo, not
corroboration.** One doubt was checked before writing and is recorded as resolved, so the next
session does not re-spend the effort.

1. **Claim 19 is the sharpest exposure, and it is a real one.** Invariant 1 was rewritten from
   unconditional append-only to "current round filled in place, completed rounds append-only" — and
   then rows *inside* round 5 were edited under the widened rule. The defence is that §7 already
   said "Completed rounds append only" before anything was touched, so the invariant was corrected
   toward §7 rather than widened past it. **That defence has not been checked by anyone else.**
   Read `git show 2565c08:skills/review-adjudication/SKILL.md` §7 and decide independently.

2. **`check_retired_wordings` probably buys much less than §R5.15 claims.** It matches literal
   retired phrasings with whitespace normalized. **The actual recurring failure in this repository
   is a rule restated in different words at another site** — which that check cannot touch. §R5.15
   presents its one catch as evidence the validator earns its place; the honest reading may be that
   it caught a verbatim copy-paste, which is the easy case. Brief claim 4 points at this.

3. **The `<why_this_is_hard>` compression was not diffed clause by clause.** ~8 lines were removed
   from `review-adjudication/SKILL.md` to buy gate headroom, on the stated grounds that the full
   text survives in `references/why-this-is-hard.md`. The reference was confirmed to exist and to
   cover the four forces. **It was not compared sentence by sentence against what was deleted.**
   Something may have been lost that was not duplicated. Brief claim 20 asks for this.

**Outcomes — what the round-6 reviewer said about doubts 1–3. Verify before relying on any of it.**

- **Doubt 1 (claim 19) — the reviewer cleared it, unprompted, in its unseeded pass.** It compared
  the rewritten invariant against §7 and step 2 as they already stood and concluded: *"That is a
  genuine correction of an over-broad summary, not a rule widened in order to violate it."* It also
  verified the ledger prefix is an exact byte prefix of HEAD. **This is the single most important
  thing for the round-6 adjudicator to re-check independently**, because it exonerates the session
  that commissioned the audit, on the question that session flagged as its own sharpest exposure.
  A clearing verdict on a directed claim is exactly where an echo does the most damage.
- **Doubt 2 — CONFIRMED as finding 7.** `check_retired_wordings` is *"silent on emphasis, inline
  code, and restatement — the failure it was built for."* The mutation table shows 5 silent probes
  against 4 caught. The doubt was right and §R5.15 overstates what that check buys.
- **Doubt 3 — cleared.** *"No unique operational rule was found only in the deleted lines"*; the
  compressed clauses survive in `references/why-this-is-hard.md`.
- **Not a doubt, but it belongs here: finding 11 is a defect this session introduced.** The
  references index added by fix item 1 names `example-audit-prompt.md`, which **does not exist** in
  `skills/adversarial-review-prompt/references/` — confirmed by `ls`. The pre-existing text at
  `SKILL.md:256` names it as *"may be present … deliberately not linked"*; the new index names it
  flatly. `check_links` misses it because the index uses backticks, not markdown link syntax. The
  reviewer scored it **unseeded**. It looks correct; it has not been ruled.

4. **RESOLVED before hand-off — do not re-spend effort here.** The worry was that adding a
   reference index above the compaction cut pushed previously-surviving content past it. Checked:
   `</invariants>` moved 53 → 57 (+4), but `<process>` moved 75 → 73 (−2), because the compression
   freed more than the index consumed. **Net two lines more survive the cut than before.** No
   content was pushed past it.

5. **Round 5's free findings — now 2, and the remaining doubt still stands.** Codex reported that its own unseeded pass
   produced no repository defect outside the 18 claims, and that self-report was accepted at face
   value — scoring Review A at 0 free. That is the party under review reporting on its own
   independence, which the ledger rejects everywhere else. The true free count could be higher (if
   Codex was being modest) or the directed count higher still. Nobody checked.

6. **`A-1` may make the whole cut-line exercise moot, and that was not thought through.** If a
   skill can be dropped *entirely* after compaction when several were invoked — which Anthropic's
   docs state — then tuning whether the cut lands at line 195 or 214 is rearranging deck chairs.
   The number was corrected and the whole-drop case was documented, but **the invariants-block
   design was not re-examined in light of it.** That is a design question for a later round.

## 4. What is still open from round 5

Round 5 is **OPEN**. Its status section is `§R5.17`.

- **`CNV-R5-1` — CLOSED.** The owner supplied the hand-off; it is ruled at `§R5.18`. Two results
  the round-6 adjudicator must carry:
  - **Doubts D3 and D5 are unspent and are now live in the round-6 brief** as claims 14 and 13.
    They lived only in `EXTERNAL-REVIEW-5-PROMPT-GROK.md`, which no reviewer ever read. **A
    round-6 finding landing on the digest's blindness to uncommitted edits (D3) or on "the checks
    are the ones that were hand-run, not the right ones" (D5) is a directed echo, not a
    discovery.**
  - Round 5's free count dropped from 3 to 2, with `grok-7` downgraded to partial. The prediction
    that the doubts could only reduce it held.
- **`P-1` / `grok-8` / `CNV-R5-7`** — the unaudited half. **Round 6 is the execution of this.** When
  its report is adjudicated, these close.
- **`Q-4`** — `~/.claude/skills/` is behind this repository. **The skills actually executed at
  runtime contain none of the nineteen fixes.** Not synced; outside the round-5 authorization.
- **`CNV-R5-2, -4, -5, -6`** — open `VERIFY` items, all non-blocking, each naming its check.

## 5. Uncommitted state

Nothing in this repository is committed since `2565c08`. Modified: `HOW-IT-WORKS.md`, `README.md`,
`REVIEW-ADJUDICATION.md`, `scripts/validate.py`, and seven files under `skills/`. Untracked:
`EXTERNAL-REVIEW-5-CODEX.md`, `EXTERNAL-REVIEW-5-GROK.md`, the two round-6 brief files, and this
hand-off. The owner has not been asked for a commit.
