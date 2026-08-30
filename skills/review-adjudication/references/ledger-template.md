# Ledger skeleton

The adjudication ledger is a durable record, not a working note. It is read by three later
audiences: the person executing the fixes, the next review brief's "ground already walked" section,
and whoever asks in six months why a known defect was left alone. Write for those three.

Section order below is load-bearing: identity, then the evidence gathered *before* any ruling, then
the rulings, then what is owed. Adapt headings to the work; keep the sequence.

Text in `«guillemets»` is an instruction to you and must not survive into the output.

---

## Header — identity and the count

```markdown
# Phase «NN» — External Review Adjudication

**Reports found:** «every `*EXTERNAL*` report file the step-1 census discovered, each marked
`adjudicated in this ledger` / `adjudicated in round N` / `not adjudicated — <why, and where its
findings go instead>`»
**Review:** `«NN-EXTERNAL-REVIEW.md»` («reviewer model family, product and version, and reasoning
effort», «date», «envelope honoured? say so or say what it wrote beyond its report»)
**Reviewer identity established from:** «the user told me / the brief at `«path»` / round N's ledger
header» / «could not establish — recorded as unknown». Never inferred from the report's own prose;
an unknown identity is treated exactly as no calibration record below
**Brief:** `«NN-EXTERNAL-REVIEW-PROMPT.md»`
**Adjudicated:** «date», by «this planning/execution session»
**Report state:** «complete / partial — no coverage line, stops at «where» / inconclusive — not a
review, «what it actually is»»
**Reviewer isolation:** «which earlier artifacts this reviewer could read — the prior report, this
ledger, another reviewer's findings — and where. Same directory means yes. "First reviewer, nothing
to see" where that is the case»
**Reviewer calibration:** «PASS, run «date», expires «date», corpus digest «12-char» — recomputed
and «matches» / «differs, so stale» / «not checkable, no corpus here» — from
`«./» / «~/».adversarial-review/calibration/«reviewer-id».md`; **name which of the two**, since a
machine-wide record and one pinned to this repository are different claims» / «none on file —
**both** `./` and `~/.adversarial-review/calibration/` listed and empty of a matching identity» /
«stale — run «date», expired
«date»» / «FAIL» / «not looked up — reviewer identity unknown, so no record could be keyed; treated
as none on file». «Where it is anything but PASS, add: findings adjudicated normally; upheld claims
recorded as CNV, not coverage»
**Workload gap:** «`[deep]` only — the size the pass was earned on, from the record's Workload
row, beside the size of the work this review covered, both in numbers. State them; do not
characterise the gap»
**Tier:** «light / deep», «and the tier the brief was written at, where they differ»
**Independence:** «agreement with the brief is non-independent by default; no author's doubts list
exists — that protocol is retired» «`[deep]`: echo tally — «E» echo, «P» partial, «F» free»
**Upheld claims:** «`[deep]`: «S» sampled of «T» listed · «K» re-opened as `U-N`» / «light: list
scanned for claims cleared on a comment, a test name or a docstring; «K» found and given rows»
**Findings in: «N» · Rows out: «N»** «the two must match; if merged, say which IDs». «`[deep]`
breaks the auxiliary rows out per namespace: +«K» process, +«M» CNV, +«D» prior-review
disagreements ruled, +«U» re-opened upheld claims, +«A» adjudicator findings, +«C» corrections to
earlier rounds — each stated even when it is zero»
```

The envelope line matters. The brief's permissions are an instruction, not a sandbox — if the
reviewer wrote outside its report file, that is worth knowing before its findings are weighed.

The three lines above it matter for the opposite reason — they say how much the report is entitled
to settle. A partial report has not upheld the claims it never reached; a reviewer that could read
the previous one is not a second opinion on anything they agree about; and a reviewer never shown
to be able to find a planted defect has not cleared anything by staying quiet. None of the three
touches what its findings are worth — only what its silence is worth.

## 1. Situation in one paragraph

What was reviewed, what state it was in, what the reviewer was asked to do, and what came back at
the top level. No rulings here. A reader who stops after this paragraph should know what happened
and nothing they would have to unlearn.

## 2. Re-verification performed before accepting anything

The section that gives every ruling below its weight. For each thing you checked:

- The outcome you expected, stated **beside the command before running it** — pre-registration is
  what makes a surprise surface mechanically instead of by recall
- The command, verbatim, and its real output — not a paraphrase and not a summary
- Which finding it bears on
- Whether the reviewer's own figures reproduced, where it gave any, exactly
- **The ruling you reached checking the claim card**, before re-reading the reviewer's argument for
  that finding — then, on its own line, whether re-reading it moved the ruling and which way. Most
  rows read "unchanged", and that is the point: the exceptions are where the report did the
  persuading rather than the evidence, and they are worth being able to find later

Mark every check whose result contradicted its pre-stated expectation. A re-verification section
containing only confirmations of what you already believed is self-review with extra steps.

Where a claim is about runtime behaviour, say how you reconstructed the production path — the real
entry point, production defaults, the deduped real population. A fixture that made the check
convenient is a different check.

> «Where nothing could be executed — a plan or design target — say so in one line and state the
> evidence standard used instead: the source cited and quoted that settles each claim.»

## 3. Adjudication

One row per finding. Both axes, always.

```markdown
| # | Finding | Class | Verdict | Disposition |
|---|---------|-------|---------|-------------|
| 1 | «title, verbatim from the report» | «false-green gate / wrong result / broken contract / invalid assumption / omitted alternative / internal contradiction / robustness / hygiene» | **CONFIRMED** | **FIX NOW** — «the minimal fix, named, with the file or plan task it lands in» |
| 2 | «title» | «class» | **OWNER RULING REQUIRED** | **PENDING OWNER** — see §4. «Blocks / does not block» execution |
| 3 | «title» | «class» | **REFUTED** | **NO ACTION** — «the evidence, with the command; not the reasoning». «Where a second opinion was required: **Verifier exposure —** it ran «with `Write`/`Edit` excluded / unbounded», and «read only a sanitized copy at «path» / could have read the report, which sat in the directory it was spawned into»» |
| 4 | «title» | «class» | **SETTLED ALREADY** | **NO ACTION** — «decision cited: file:line, quoted» |
| 5 | «title» | «class» | **CONFIRMED** | **FIX LATER** — «backlog artifact path, which must already exist» |
| 6 | «title» | «class» | **CONFIRMED (partial)** | «what is established vs unestablished, then the disposition» |
| 7 | «title» | «class» | **COULD NOT DETERMINE** | **VERIFY** — «the concrete check that would settle it»; «blocks / does not block» execution; listed in the hand-off |
| 8 | «title» | «class» | **TRUE, NOT A DEFECT** | **NO ACTION** — «the claim's Consequence quoted verbatim from the report, or `no consequence stated`»; «one clause: what would have to be true for this to be a defect here, and that it is not» |
```

Keep the reviewer's numbering. Where you merged two findings, keep both IDs in the `#` cell and say
why in the row.

**Light tier writes one table.** Every auxiliary item — a could-not-verify entry, a process or
prompt defect, a disagreement with a prior review, an upheld claim cleared on a comment — is a row
in it, tagged in the `Class` cell (`process`, `CNV`, `prior-review`, `upheld`) and carrying both
axes like any other. The separate blocks and ID namespaces below are `[deep]`; the obligation they
serve — a row for everything that came in — is the same either way, and one table meets it with
less bookkeeping.

**When the vocabulary changes, earlier rounds do not become wrong.** A verdict or disposition term
added in round N does not reach back: rows written before it were correct under the rules then in
force, and they are history under invariant 1 — **not defects to repair.** Where a widened
mechanical check begins reporting on the closed prefix, the round that widened it records the
expected output, row by row, so a later session reads those lines as known history rather than as
new work. When more than one report feeds a round, prefix each ID with the reviewer tag
(`codex-3`, `fable-3`) so a row number names exactly one finding.

No bare "ACCEPTED" — it means both "the finding is real" and "we are shipping with it."

**`[deep]`: every `REFUTED` that required a second opinion carries a verifier-exposure clause**, in
the row itself, saying two things: whether the verifier's tools were restricted, and whether it could have
read the report. Neither is decoration. A reader who is not told assumes the stronger version of
both, and "blind" is never the word for a check that was merely uninformed — the `Reviewer
isolation` line in the header is about the *external reviewer* and does not cover this.

### Process and prompt defects

Their own short block. The brief invites the reviewer to report contradictory instructions, stale
citations, and leaked placeholders, and those findings are wanted — but their fix lands in the brief
or the skill, not the code, so they do not belong in the table above.

State for each: what it was, whether it is real, and what changed as a result. A stale citation that
turned out to be the review-prompt commit's own SHA is real but harmless; a permission stated two
ways is real and cost the reviewer output.

### Reviewer's could-not-verify items

One entry per item, each with a stable ID (`CNV-1`, `CNV-2`, …) and **both axes**, same as a table
row — the usual pairing is `COULD NOT DETERMINE` + `VERIFY — «the concrete check»; «blocks / does
not block»`, but an item you settled here gets its real verdict (`CONFIRMED`, `REFUTED`, …) and
disposition. The no-empty-cells closure check covers these entries. The reviewer flagged a gap
honestly; an unruled gap reads downstream as a pass.

### Disagreements with a prior internal review   «when the report raises any»

One entry per disagreement, stable IDs (`D-1`, …), both axes. Where the reviewer says a prior
round's ruling or fix-verification was wrong and this adjudication confirms it, the entry names
the superseded row or statement explicitly — it is a correction record, and the original stays as
written.

### Disagreements between reviewers   «only when several reviewed»

Where two reviewers contradict each other on the same code, say which was re-verified and how it
came out. Neither is presumed right by seniority or by order of arrival.

## 4. Owner decisions required

The reason this ledger stops rather than finishing. One block per question:

```markdown
### «Q1 — one-line question»

**What turns on it:** «the trade-off in the user's terms, not the code's»
**Options:**
- «A» — «what it costs, what it buys, what it forecloses»
- «B» — «same»
**Recommendation:** «yours, with one clause of why — a recommendation is not a ruling»
**Blocks:** «which plan/task cannot start before this is answered, or "nothing"»
```

Once answered, the answer is recorded here verbatim and dated. An owner ruling that lives only in
chat is the same failure as a review that lives only in chat.

## 5. Locked owner decisions from this adjudication   «add as they arrive»

The answers, quoted, dated, each naming the question it settles. This block is what later phases
cite; it is the durable half of §4.

## 6. Amendments required

The `FIX NOW` queue as an executable list — file or plan task per item, and the ID it answers. This
is what the fixing session works from, so it must be specific enough to execute without re-reading
the review.

Backfill each row as the work lands — with its commit where the target is version-controlled, or
a dated change note naming the files touched where it is not. A ledger whose Disposition column
still says "queued" three phases later is telling you something true.

## 7. Claims examined and upheld — and the ones re-opened

The reviewer's coverage list, and anything it checked and found sound. One line each, no
elaboration. This is what stops the next brief re-targeting ground already walked — which is exactly
why it is sampled rather than transcribed. Say how many you sampled and how you chose them.

Then the re-openings, as `U-N` entries with a verdict and a disposition like any other. A claim
upheld by quoting a comment, a test name, or a docstring was not checked — it is upheld in the
report and open here. So is any claim the reviewer reached and then argued was intentional on the
strength of the work's own words.

Where the report is partial, the claims it never reached are listed in §8, never here.

## 8. What this review could not settle, and why that is acceptable

Explicit. An unstated gap reads as a pass — the same rule the brief imposes on the reviewer applies
to the adjudicator.

---

## Round appends

A follow-up or delta review appends to the same file. Closed rounds are immutable — never edit
them. A round not yet closed — empty cells, an unresolved `PENDING OWNER`, an unexecuted or
unbackfilled queue — is still the current round and is filled and backfilled in place (`SKILL.md`
step 1 defines closure).

```markdown
---

# Round «N» — «delta review of the amendment commits / second reviewer / re-review after fixes»

**Reports found:** «the full census again, with per-report status — earlier rounds' reports are
`adjudicated in round N`»
**Review:** `«NN-EXTERNAL-REVIEW-«N».md»` («reviewer», «date»)
**Findings in: «N» · Rows out: «N» · +«K» process, +«M» CNV, +«D» prior-review disagreements
ruled, +«U» re-opened upheld claims, +«A» adjudicator findings, +«C» corrections to earlier rounds**
```

Then the same sections. Two additions specific to later rounds:

- **Corrections to earlier rounds.** Where round N shows a round-1 ruling was wrong, write a new row
  citing the row it supersedes and say what changed — new evidence, or a ruling made without it.
  Never edit the original row. The record of having been wrong is part of what the ledger is for.
- **Did any round-1 fix open a new path to the failure it closed?** Ask it explicitly. It is the
  question the next reviewer will be asked in the brief's §7, and it is cheaper to answer now.


---

## The ID namespace — declared, not guessed

`scripts/validate.py` classifies every ruling row by its ID, and it now **errors on an ID that
matches no declared series** rather than guessing. Round 7 `codex7-10`: the old rule reserved seven
single uppercase letters silently, so numbering two reviewers `C7-N` and `G7-N` dropped all thirteen
`C7-` rows from the census — the very check bought to stop findings vanishing.

| Series | Spelling | What it is |
|---|---|---|
| Numbered findings | a lowercase reviewer tag — `codex7-1`, `grok7-3`, `g6-1` | one row per numbered finding in the report |
| | `F«n»` or a bare integer | historical; rounds 1–3 and the worked example use these |
| Auxiliary | `P-«n»` process · `CNV-«n»` could-not-verify · `D-«n»` prior-review disagreements | ruled in their own blocks, counted separately |
| | `U-«n»` re-opened upheld claims · `A-«n»` your own findings · `C-«n»` corrections to earlier rounds | |
| | `X-«n»` · `Q-«n»` owner questions | |

**Pick numbered IDs that are lowercase.** An uppercase tag collides with the auxiliary namespace,
and the validator will tell you so rather than quietly miscounting.

**Where history records a census the rule cannot derive**, the exception belongs in the validator's
`COUNT_EXCEPTIONS` — dated, reasoned, naming the round and the ID. Closed rounds cannot be edited to
declare themselves, so the exception lives in the checker. Do not relax the rule until history
passes; that is how a check stops being one.

## Assembling a round — and the append proof

**Assemble the current round outside the ledger and concatenate it once.** Round 7 `A7-6`: an
in-place edit with an unanchored string replace matched an *earlier round's* identical phrase first
and silently rewrote a completed round. Nothing mechanical catches that — closed-round edits are
warnings by design.

**Re-run the append proof after every write, not only at the end:**

```
head -n «last line of the prior round» «ledger» | diff - «a copy taken before this session»
```

Silent, or you have edited history. Keep the pre-session copy in the session scratchpad from the
first write, because after the fact there is nothing to compare against.

## Verdict and disposition pairings that are easy to get wrong

| Situation | Verdict | Disposition |
|---|---|---|
| A re-opened `U-N` claim that checks out — true, and alleges no defect | `TRUE, NOT A DEFECT` with its gate filled | `NO ACTION` |
| A re-opened `U-N` claim that does not | `CONFIRMED` / `CONFIRMED (partial)` | `FIX NOW` or `FIX LATER` |
| A real defect you will not fix this phase | `CONFIRMED` | `FIX LATER` **plus its backlog artifact** — never `NO ACTION` |
| A correction to an earlier round, where the erroneous text is not a repository file | `CONFIRMED` | `FIX NOW` naming what *is* fixable, or the queue item that carries it |

**When the vocabulary changes, earlier rounds do not become wrong** — and the validator now says so
at the point of use. Rows written under a superseded rule surface as warnings labelled *"expected
permanent history"*; anything else in a closed round is labelled *"NOT one of the expected history
warnings"*. Pin the expected ones by row **identity** in `EXPECTED_HISTORY`, never by line number:
appending above them shifts every line below and re-flags them as new.
