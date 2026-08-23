# External Review 7 (Grok) — the skills, the ledger, and the self-certified round
Reviewer identity: xAI family, Grok Build / Grok 4.6, reasoning effort high, served alias verbatim: "Grok 4.6"

## Coverage
20 of 20 claims engaged. Read the two `SKILL.md` files, `ledger-template.md`, `cover-note-template.md`, `prompt-template.md`, both `why-this-is-hard.md` files, `second-opinion.md`, `BACKLOG.md`, `calibration/README.md`, `calibration/record-template.md`, round 6 of `REVIEW-ADJUDICATION.md` (`§R6.*` from `:4155`), the round-3 rows at `:2383`/`:2384`, this round's Grok brief and both cover notes, and the envelope table of the Codex brief (claim 18 asked for both pairs; I did not read its claims list). Ran `git diff --stat 2565c08..d610112`, `git show` line counts, prefix `cmp` of the ledger against `2565c08`, `python3 scripts/validate.py` and `--list`, the digest command on a `/tmp` copy (clean / tracked edit / untracked add), and planted mutations under `/tmp/probe-r7` and `/tmp/probe-r7b`. Did not read `ROUND-6-HANDOFF.md`. Did not re-run the author's 29-probe suite (spot-checked the two probes this half needed). Did not hunt `scripts/validate.py` beyond what the prose claims about it.

Pinned range `2565c08..d610112` is `d610112` at HEAD. The 15 files / `+491/−171` figure reproduces if and only if `REVIEW-ADJUDICATION.md` and `ROUND-6-*` are excluded; the file table still lists the 5,234-line ledger as a target. Not ranked: the ledger is given its own line count.

Session note, not a finding: this Grok worktree was at `0d65b51` (round 4) and did not contain the brief. The work under review is `/Users/leo/Documents/WORK/CODING/adversarial-review-skills` at `d610112`. This report is written there.

## Findings, ranked

### 1. `TRUE, NOT A DEFECT` — the license survived compaction; the gate did not
- **Impact** — high
- **Location** — `skills/review-adjudication/SKILL.md:41-43` (invariant 2, above the `~195` cut) vs `:412` (gate and boundary, well below it); `references/ledger-template.md:107` (gate in the example row, no boundary); `scripts/validate.py:127-129` (`VERDICTS` / `NO_ACTION_OK`)
- **Mechanism** — Round 6 added a dismissal term and put its *permission* in the surviving prefix (`NO ACTION` is legal under "the gated `TRUE, NOT A DEFECT`") while leaving the *gate* (quote the Consequence; name what would make it a defect) and the *boundary* (if the claim says anything here is wrong, never this verdict) in §6. A compacted session therefore knows it may issue the pairing and does not have the text that was supposed to make that expensive. The validator matches the same split: it legalises the pairing and does not read the cell. In a `/tmp` copy, this auxiliary row:

  `| A99 | Ungated true-not-a-defect | hygiene | **TRUE, NOT A DEFECT** | **NO ACTION** — because I say so |`

  produced `12 of 12 checks pass (2 warning(s))`, exit 0. The same pairing under `**CONFIRMED**` errors. The hatch works; the lock does not. This is g6-11's shape, introduced in the same pass that claimed to have closed g6-11: a name above the cut, the qualifier that makes it safe below it.
- **Trigger** — any later adjudication that wants a cheap `NO ACTION` on a real defect, especially after compaction, or any row that uses the term with empty gate text. The author's own worked example already walks through the hole: `§R6.15` says `R3-P4` (citations in a report that lives in this repository) **qualifies** for the new term, against a boundary that says "if the claim asserts that anything in this repository is wrong, the verdict is never this one." "Here" is doing unspecified work, which is how a motivated reading gets in.
- **Consequence** — contract items 4 and 5. The term was sold as resisting the dismissal reflex at the same weight as `FIX LATER`'s backlog artifact (`§R6.15:4869`). What shipped is the cheaper half of that deal. Step 3 still says a real out-of-scope defect is `CONFIRMED` + `FIX LATER`, never `NO ACTION` (`SKILL.md:261-263`); the new term is the way around that, and nothing mechanical, and nothing above the cut, stops it.
- **Status** — CONFIRMED (planted row; line numbers of the two halves; `§R6.15:4891-4892` on `R3-P4`)
- **Why it ranks here** — every future round can use this term; the last round's whole point was that a check which cannot fail is how a wrong result looks right.
- **Pass** — directed (claims 1–3), with the cut-placement half reached by reading the invariants against claim 9's cut, not by the claim 1 sub-question naming it.

### 2. Round 7's own envelopes fail the check this range added
- **Impact** — high
- **Location** — `skills/adversarial-review-prompt/references/cover-note-template.md:72-76` (the fix); `EXTERNAL-REVIEW-7-COVER-NOTE-GROK.md:44-49` and `EXTERNAL-REVIEW-7-COVER-NOTE-CODEX.md:43-46` (the live test); `EXTERNAL-REVIEW-7-PROMPT-GROK.md:267-271` and `EXTERNAL-REVIEW-7-PROMPT-CODEX.md:279-284` (what the briefs grant); `REVIEW-ADJUDICATION.md:5227-5230` (R6.19's three requirements for this round)
- **Mechanism** — Queue item 18 added a network line and a "walk the brief's permission table row by row" paragraph, because round 6 shipped a brief granting web search beside a cover note silent on network. This round's two cover notes both state network. Neither states **Your own tools** (both briefs: "Subagents and MCP servers as you see fit") nor **Effort budget**. Omission of a granted axis is the defect the new paragraph names. Separately, R6.19 required `ROUND-6-HANDOFF.md` excluded from round 7's read scope as one of three load-bearing conditions. The Grok brief and cover note exclude it. The Codex brief's Read row is "Everything in this repository, `.git` history included" with no exception, and the Codex cover note says "You may read anything in the repository." The contamination control landed on one of two reviewers.
- **Trigger** — already triggered: these two cover notes, this round. A Codex session that opens the hand-off gets the author's residual doubts about the validator it is supposed to be independently auditing.
- **Consequence** — contract items 1 and 4. The remedy closed the last spelling (network) and not the class (any omitted axis). R6.19's own "what cannot be fixed" list is incomplete on an item it called a requirement.
- **Status** — CONFIRMED (the four files, side by side)
- **Why it ranks here** — it is this range's own fix, failing its own live test, on the round that exists to be independent of the session that wrote the fixes.
- **Pass** — directed (claims 18 and 20)

### 3. `B-4` still describes a closed defect as parked and unfixed
- **Impact** — medium
- **Location** — `BACKLOG.md:139-159` vs `scripts/validate.py:438-441` vs `REVIEW-ADJUDICATION.md:5149-5165`
- **Mechanism** — `§R6.18` opened `B-4` as `FIX LATER` because a footnote-broken retired phrase stayed silent after queue item 10. `§R6.19` then closed it: the check now strips `[^…]` markers, and a `/tmp` probe of `before the ledger[^fn] is written` in `README.md` now errors (`ERROR retired: README.md still carries a retired wording`, exit 1). `B-4` was not updated. It still says "Why it is here rather than fixed: the round-6 owner authorization covered 25 named items and this is a twenty-sixth … belongs with the next authorized pass."
- **Trigger** — the next brief's "ground already walked" / backlog read, which will treat a closed item as open work. Same inheritance path as `g6-9` / old `B-3`'s `9/9`.
- **Consequence** — contract items 2 and 3. A discharge record that still reads as a live defect is a false floor. `B-3` was rewritten in this range for exactly that reason and carries a "partly discharged" marker; `B-4` did not get the same pass.
- **Status** — CONFIRMED (code, ledger, backlog, and a `/tmp` mutation)
- **Why it ranks here** — a later reader acting on `B-4` will "fix" a check that already strips footnotes, or skip the class because a backlog item exists for it. Either way the record is wrong.
- **Pass** — directed (claim 15)

### 4. The `A-N` slot was added in four places and missed a fifth; `C-N` still has no slot
- **Impact** — medium
- **Location** — invariant 3 at `SKILL.md:44-46` (has `U-N` and `A-N`); §7 at `:461-463` (has `U-N` and `A-N`, **omits prior-review disagreements**); §2 at `:202-205` (still `"Findings in: N · Rows out: N · +K process, +M CNV, +D prior-review disagreements ruled"` — **no `U`, no `A`**); `ledger-template.md:49-51` and `:227-228` (both have `U` and `A`, neither has `C`); round 6 header at `REVIEW-ADJUDICATION.md:4224` (`+5 corrections to earlier rounds`, a field the grammar still does not contain) and `:4229-4231` (the note that the `A-N` field "had to be invented" left standing after the slot was added)
- **Mechanism** — `A6-7` was that the header grammar had no slot for adjudicator-raised findings, so real ruled rows get left out of the count. Queue 19+25 added `A-N` to invariant 3, §7, and both template formulas. §2's worked example of the same formula was not touched — the named X-2/C-6/U-4 shape, a rule restated in one more place than was edited. The same header that motivated `A-N` also had to invent `+5 corrections`. `C6-1`…`C6-5` exist, the template's round-append section tells you to write them, and no header slot names them. `A6-7`'s fix was the instance, not the class.
- **Trigger** — the next round that raises corrections, or any session that copies the §2 example rather than the template.
- **Consequence** — contract item 1. Round 6's own header still does not match the grammar it just wrote: it carries a `C-N` field the grammar lacks, and a note describing a missing `A-N` slot that now exists.
- **Status** — CONFIRMED (five sites read; IDs counted: 15 g6, 7 A6, 6 U6, 5 C6, 6 CNV-R6, 5 D6)
- **Why it ranks here** — the next census is where a missing slot becomes a dropped row; that is the defect this skill exists to prevent.
- **Pass** — directed (claim 4) for `A-N` sites; unseeded for `C-N`

### 5. The compaction-cut figure dropped "this is an estimate" while the numbers moved
- **Impact** — medium
- **Location** — `skills/adversarial-review-prompt/SKILL.md:22-25` (`~205`); `skills/review-adjudication/SKILL.md:26-28` (`~195`). At `2565c08` both said *"Estimated cut: around line 221/214, from a measured ~3.1 characters per token … an estimate, not a tokenizer run, and biased late if anything."*
- **Mechanism** — the range rewrote both cuts and deleted the only sentence that said the number was back-computed. At ~3.1 characters/token, 5,000 tokens is ~15,500 characters, which is line **220** of the prompt skill and line **209** of the adjudication skill — later than the new figures, earlier than the old ones. The invariants blocks still end at lines 59 and 57, so they fit. The honesty about the figure does not. `R3-CNV-2` / `CNV-R5-2` exist because nobody has a tokenizer run; deleting the caveat is how an estimate becomes a spec.
- **Trigger** — a compacted session treating `~205` as a hard line, or a later edit that adds operational rules between ~195 and ~220 believing they survive.
- **Consequence** — contract items 2 and 5. Finding 1 is what this costs when it happens: the operational half of a new rule was placed at `:412`.
- **Status** — CONFIRMED (`git diff` of the two files; character counts through the claimed lines)
- **Why it ranks here** — the cut is the reason invariants exist; a quiet number-change plus a dropped caveat is how the next operational rule lands in the wrong half.
- **Pass** — directed (claim 9)

### 6. `B-3` and `--list` still disagree with the checks they describe
- **Impact** — medium
- **Location** — `BACKLOG.md:102` (*"the stated rows-out equals the numbered finding rows that actually exist"*); `scripts/validate.py:343-348` (row counting is skipped on closed rounds); `:478-480` (registry still labels two whole-file checks as `"current round"`)
- **Mechanism** — `g6-1` was that `check_counts` compared two header numbers and never counted rows. The fix counts numbered finding rows **in the current round only**; closed rounds still compare header-to-header (`:343-344`: `if not current: continue`). `B-3`'s rewrite dropped the "current round" qualifier that `--list` still prints for counts, and that the pre-round-6 `B-3` had. Separately, `g6-6` widened two-axes and disposition checks to the whole file (closed rounds warn). `--list` still names both `"current round: …"`. `B-3` correctly says closed-round defects warn; `--list` does not.
- **Trigger** — reading `B-3` or `--list` as the description of what the validator does, which is how the last `9/9` sentence got into a brief.
- **Consequence** — contract item 2. The discharge record for the validator overstates the one check this round most carefully bounded, which is the failure `g6-9` was supposed to close.
- **Status** — CONFIRMED (`--list` output; `check_counts` source; `B-3` text)
- **Why it ranks here** — same inheritance path as finding 3, smaller blast radius (operator-facing description, not a live backlog item to execute).
- **Pass** — directed (claim 14) for `B-3`; unseeded for the `--list` names

### 7. `CNV-R6-1` is still an open row after the gap it named was closed
- **Impact** — low
- **Location** — `REVIEW-ADJUDICATION.md:4668-4669` (`CNV-R6-1`: `COULD NOT DETERMINE` / `VERIFY`) vs `:5092-5108` (settled as `CONFIRMED` open gap, `FIX LATER`) vs `:5149-5165` (then closed)
- **Mechanism** — invariant 1 allows filling the current round in place. Round 6 is not marked closed (`§R6.17` says OPEN; there is no later CLOSED section). The `CNV-R6-1` row was not backfilled after `§R6.18` or `§R6.19`. A reader of the table, rather than of the narrative 400 lines later, still sees an open verify item. The footnote probe in finding 3 shows the check now catches the case.
- **Trigger** — a later census of open `VERIFY` rows, or a brief that copies `§R6.9` as outstanding work.
- **Consequence** — contract item 3. The ledger's machine-readable half disagrees with its prose half on a settled item.
- **Status** — CONFIRMED
- **Why it ranks here** — it is one row, already explained in prose; the cost is a false open item, not a false close.
- **Pass** — directed (claims 11, 13, 15)

### 8. This brief tells the reviewer not to read the Codex brief, then requires a check of both
- **Impact** — low
- **Location** — `EXTERNAL-REVIEW-7-PROMPT-GROK.md:105-108` (*"You are not reading that brief and it is not reading yours"*) vs `:203-205` (claim 18: *"check this round's own two cover notes against this round's own two briefs on every permission axis"*); cover note `:56-57` repeats the first instruction
- **Mechanism** — both instructions cannot be obeyed. The cover note also asks that contradictory instructions be reported as a process finding. I read only the Codex envelope table and its cover note, not its claims. That is a resolution I had to invent.
- **Trigger** — this run.
- **Consequence** — the reviewer spends effort on the contradiction (I did) or skips claim 18's live test of the cover-note fix (finding 2 would have been weaker).
- **Status** — CONFIRMED
- **Why it ranks here** — it burned time on this run and does not survive into the skills; it is the brief asking to be audited as a brief.
- **Pass** — process, invited by the brief's own last paragraph

### 9. Queue item 24 asked to record the history rule in the skill; it landed in the template
- **Impact** — low
- **Location** — `REVIEW-ADJUDICATION.md:4919` (item 24: *"Record in the skill that the term arrived in round 6 … and that the two round-3 rows are history … with the expected warning output from item 3 named"*); `skills/review-adjudication/SKILL.md` (no match for `vocabulary`, `2383`, or "arrived in round 6"); `references/ledger-template.md:113-118` (generic "when the vocabulary changes, earlier rounds do not become wrong"); `§R6.15:4894-4904` (the instance-specific expected warnings)
- **Mechanism** — `§R6.16` claims "All 25 queued items landed." Item 24 specified the skill. The generic rule is in the template, which is the file you open before writing a ledger, and the expected output is in the ledger. A session that reads only `SKILL.md` — the copy that survives compaction — does not have it. The grouping note at `:4922-4923` said items 24 and 25 "touch the same two files"; only one of those files received item 24.
- **Trigger** — a later session that sees the two `WARN disposition` lines and "repairs" history, which is the event item 24 existed to prevent. The template's generic rule is some defence; the named line numbers are not in the skill.
- **Consequence** — contract items 2 and 4, small. The expected-output documentation is in the ledger, which is what `§R6.15` said a later session should read. The miss is the skill-level copy.
- **Status** — CONFIRMED
- **Why it ranks here** — the generic rule did land somewhere a ledger-writer looks; the cost is a missing compactable copy, not a missing rule.
- **Pass** — directed (claim 12)

### 10. Three dismissal examples survived the why-block compression; the fourth did not
- **Impact** — low
- **Location** — `SKILL.md:62` (`"pre-existing", "out of scope", "will handle later"`) vs `references/why-this-is-hard.md:13` (the same list plus `"scaffold only"`)
- **Mechanism** — `§R6.18` counted exactly three dropped clauses and called all three motivation, permitted below the cut by `A-2`. Redo of the `2565c08` diff agrees the three unique lost sentences are `"scaffold only"`, *"a refutation typically arrives as a paragraph of reading"*, and *"and implementing those is real damage"*, and all three are in the reference at `:13`, `:20`, `:31`. The second and third are motivation for rules that survived in the compressed block. `"scaffold only"` is not: it is the same kind of named dismissal costume as the three examples that were kept. A compacted session has a three-item list of tells and will not see the fourth.
- **Trigger** — a finding dismissed as "scaffold only" after compaction.
- **Consequence** — contract item 5, narrow. `A-2` does not justify dropping one of four examples of the same operational tell.
- **Status** — CONFIRMED (`git diff` of the why-block; reference file read)
- **Why it ranks here** — one missing example, remaining three still in the surviving prefix.
- **Pass** — directed (claims 6–7)

### 11. `CNV-R6-2` is parked as unfixable; the portable implementation is already in the tree
- **Impact** — low
- **Location** — `REVIEW-ADJUDICATION.md:5203` (*"One operating system available here. Needs a Linux checkout"*); `calibration/record-template.md:14` (the named command uses `shasum`); `scripts/validate.py:357-367` (`corpus_digest()` already hashes with `hashlib.sha1` and matched the shell command on every `/tmp` tree I ran)
- **Mechanism** — `§R6.19` lists nine items as unfixable. Equivalence of `sha1sum` vs `shasum` on Linux is genuinely unverified here. Making the *record command* portable is not: Python is what the validator already uses, and a template that named that implementation would close the gap for future records. Parking the whole item as "needs a Linux checkout" is cheaper than changing the one line operators copy.
- **Trigger** — the next calibration record filed on Linux against a template command that may or may not exist there.
- **Consequence** — contract item 2, on `§R6.19`'s completeness. An item parked as impossible is the cheapest disposition; this one had a cheaper fix than a second OS.
- **Status** — CONFIRMED (the two implementations agreed on clean `775e1cc8c43f`, a tracked-edit digest, restore, and an untracked add that moved nothing; I did not have a Linux checkout)
- **Why it ranks here** — it does not make a current record stale; it leaves the next one to rediscover the portability hole.
- **Pass** — directed (claims 19–20)

## The unseeded pass

The directed list is where findings 1 (gate/enforcement half), 2, 3, 5, 7, 8, 9, 10, 11 came from. Setting it aside and reading the diff, the header, and `--list` on their own produced:

- **Finding 1's cut-placement half** — not asked by claim 1's sub-question (which pointed at the validator). Visible once the new invariant 2 is read against the cut the documents themselves state.
- **Finding 4's `C-N` half** — the round-6 header invents `+5 corrections` the same way it had to invent `+7 adjudicator findings`; only the second got a slot.
- **Finding 6's `--list` names** — registry strings still say `"current round"` for checks `g6-6` widened.

Nothing else in `HOW-IT-WORKS.md`, `README.md`, `prompt-template.md`, or `second-opinion.md` in this range produced a defect that is not already on the ledger (`FIX LATER` wording updated; residual-doubts "list vs claim" qualifier; permission-example rewrite; `Bash` writes). A considered nothing on those four files.

## Claims examined and upheld

1. **`TRUE, NOT A DEFECT` is gated** — **REFUTED.** No mechanism enforces the gate. Planted `A99` with cell text "because I say so": `12 of 12 checks pass`. The permission is above the cut; the gate is not. See finding 1.
2. **Boundary cannot be used as an out-of-scope dodge** — **REFUTED** as a wording that stops it. Step 3 and the boundary agree *if* the adjudicator classifies honestly. `§R6.15` itself files `R3-P4` (bad citations in a report in this repository) as qualifying. The borderline case is a real defect the author would rather not fix, recharacterised as "a fact about the reviewer." The wording does not stop that; the author's example is that recharacterisation.
3. **Term stated identically in all six sites** — **REFUTED.** Invariant 2: name + "gated". Verdict table: full gate + boundary. Disposition table: name as a `NO ACTION` parent. Template row: gate, no boundary. `VERDICTS` / `NO_ACTION_OK`: name only.
4. **`A-N` header slot identical everywhere; round 6's header matches** — **REFUTED.** §2 still has the pre-fix formula. §7 omits `D`. Round 6's header adds `+5 corrections` the grammar lacks, and still says the `A-N` field had to be invented. See finding 4.
5. **Bare-ACCEPTED paragraph lost nothing (six clauses)** — **CONFIRMED.** Diff against `git show 2565c08:skills/review-adjudication/SKILL.md`: never write it; reads as "the finding is real"; also as "we accept the risk and are shipping it"; opposite dispositions from one word; past ledgers use the first sense; new rows use both axes. Six is a fair parse of that paragraph, not a count drawn only around survivors — the wrapping change is the only loss, and it is not a clause.
6. **`§R6.18`'s three-clause diff is right** — **CONFIRMED.** Redo of the `2565c08` why-block: the three unique dropped sentences are `"scaffold only"`, *"a refutation typically arrives as a paragraph of reading"*, *"and implementing those is real damage"*. All three are in `references/why-this-is-hard.md` at `:13`, `:20`, `:31`.
7. **Those three being below the cut is acceptable under `A-2`** — **REFUTED in part.** Clauses 2 and 3 are motivation for rules that survived. `"scaffold only"` is the same operational tell as the three examples kept in `SKILL.md:62`. See finding 10.
8. **Invariants-index qualifier is above the cut; index otherwise accurate** — **CONFIRMED.** Qualifier is at `SKILL.md:30-32`, inside `<invariants>` (block ends `:59`; cut `~205`). `prompt-template.md` exists and is the four-branch authority (`prompt-template.md:54-84`). `cover-note-template.md` and `why-this-is-hard.md` exist. `example-audit-prompt.md` is absent (`ls` on the path: no such file).
9. **`~205` still describes reality; documents say it is an estimate** — **REFUTED** on the second half; **CONFIRMED** that invariants still fit. Cuts are now `~205` and `~195` with the estimate caveat deleted. At 3.1 chars/token the 5,000-token line is ~220 / ~209. See finding 5. No tokenizer was run (`CNV-R5-2`).
10. **Round 6 header arithmetic is exact** — **CONFIRMED.** Counted IDs in `§R6.4`–`§R6.10`: 15 g6, 7 A6, 6 U6, 5 C6, 6 CNV-R6, 5 D6. Process is `g6-15` classified, not added. `CNV-R6-5` is also `A6-5` (reviewer's gap and adjudicator finding of the same fact); both classes require a row.
11. **Append discipline held; in-place round-6 edits match the rewritten rule** — **CONFIRMED.** `git diff --numstat 2565c08..d610112 -- REVIEW-ADJUDICATION.md` is `1611 0`. First 299,772 bytes of the current file are byte-identical to `git show 2565c08:REVIEW-ADJUDICATION.md`. Filling round 6 in place (executed markers, owner ruling) is what round 5's invariant-1 rewrite permits; completed rounds were not rewritten.
12. **`§R6.16`'s execution account is accurate and complete** — **CONFIRMED (partial).** The listed file-level changes are in the diff. The line gate was not raised (`MAX_SKILL_LINES` is still 500; files are 497 and 494 `split("\n")`). `497 → 497` / `493 → 494` are not the `2565c08..HEAD` deltas (those are 499→497 and 485→494 split-lines); they are unverifiable intra-session numbers because round-5 and round-6 skill edits share `3724016`. Item 24 landed in the template, not the skill. See finding 9.
13. **`§R6.16`'s two-bug disclosure is complete** — **REFUTED** as complete. Both named bugs are in the code (`row_cells` splits on unescaped pipes; `check_counts` skips closed rounds). Not named as defects in that disclosure: `B-4` left stale after close, §2's stale header formula, the gate sitting below the cut, `--list` still saying `"current round"` for whole-file checks. A disclosure of two parsing bugs is not a disclosure of the rest.
14. **`B-3` now describes the validator accurately** — **CONFIRMED (partial).** `--list` prints `13 named invariants over 12 checks`. Frontmatter-as-string, titles on links, escaped pipes, digest-as-error, restatement bound: all match. It overstates the counts check (no "current round") and is more accurate than `--list` on whole-file vs current-round scope. See finding 6. "Every check was re-broken" is the author's 29-probe; I did not re-run all 29.
15. **`B-4` is accurate and does not trip the check; defect still open** — **REFUTED** on open/accurate. The check now strips footnotes and catches the planted phrase. `B-4` still says it is here rather than fixed. It does not reproduce retired phrasings, so it does not trip the check. See finding 3.
16. **Round-3 rows at `:2383`/`:2384` correctly left as history** — **CONFIRMED.** Invariant 1 forbids editing a completed round. Round 5 withdrew `P-3` in an *open* round rather than write the pairing; that is a different tense of the same rule, not a contradiction. `R3-P3` would still be an illegal pairing under the *new* matrix (`§R6.15` says it does not qualify); leaving it is a true record, and `C6-5` plus the template's vocabulary-does-not-reach-back paragraph are the append-only correction. The two `WARN` lines are the documented expected output. Not a finding; engaged here as instructed.
17. **`§R6.3` echo audit is honest** — **CONFIRMED.** Re-probed `EXTERNAL-REVIEW-6-PROMPT-GROK.md` and its cover note with each finding's identifiers. 10 echoes, 3 partial, 2 free. `g6-11` (`example-audit-prompt` / `Supporting files`) and `g6-14` (`CNV-R5-3` / `jsonc`): no line in either document. `g6-2` as partial: claim 14 pointed at what the digest "silently miss[es]"; the reviewer returned that the operator docs, not the code, were wrong. That is an inversion of the brief's premise, not a free finding and not an echo. The scoring is not self-serving; scoring it free would have been.
18. **Cover-note network rule prevents the defect it was written for** — **CONFIRMED** that the *template text*, if followed, would have caught a silent network axis. **REFUTED** that this round's cover notes agree with their briefs on every permission axis. See finding 2.
19. **Calibration docs now describe the digest correctly** — **CONFIRMED.** `/tmp/adv-r7`: clean `775e1cc8c43f` (Python and `shasum` pipeline agree); tracked edit of `calibration/ANSWER-KEY.md` moved both to `70f6f9fdf9f3`; restore returned `775e1cc8c43f`; untracked `calibration/cases/untracked-probe.txt` moved nothing. Matches `record-template.md:38-41` and `calibration/README.md:134-137`.
20. **`§R6.19`'s unfixable list is honest and complete** — **REFUTED** as complete. `A-3`, restatement, compaction, intra-session order, tokenizer, headless `Write` drop, `529/587`, and "this session cannot independently review itself" are honestly unfixable *by that session*. Incomplete: `ROUND-6-HANDOFF.md` exclusion was listed as a requirement for this round and landed on one brief (finding 2); `CNV-R6-2` has a portable command already in `corpus_digest()` (finding 11); the new verdict's unenforced gate is not on the list (finding 1).

## Could not verify
- Intra-session `497 → 497` / `493 → 494` line counts in `§R6.16` (round-5 and round-6 skill edits are one commit).
- Where 5,000 Anthropic tokens actually fall (`CNV-R5-2`; no tokenizer run; estimate only).
- Linux `sha1sum` vs macOS `shasum` on the template command (`CNV-R6-2`).
- The author's full 29-probe table (spot-checked footnote catch and ungated-verdict pass; the other reviewer has the validator).
- Whether the Codex session in fact opened `ROUND-6-HANDOFF.md` (the envelope permits it; I did not read that file).
- Whether a real auto-compaction drops an older skill entirely vs truncating at ~5,000 tokens (the new sentence asserts both; only the second is what `~205` describes).

## Disagreements with the prior rounds
- **My own g6-11 remedy was applied to the example-file index and not to the new verdict term added in the same pass.** The pattern (name above the cut, safety below it) is now in invariant 2. That is the most valuable result this round can return about its own previous findings, and it is finding 1.
- **`A6-7`'s fix was the instance (`A-N`) not the class.** Round 6's header still invents a `C-N` field. Finding 4.
- **`g6-15`'s fix closed the network spelling.** This round's cover notes omit two other granted axes, and only one of two briefs excludes the hand-off R6.19 named as required. Finding 2.
- **`g6-9`'s rewrite of `B-3` was not applied to `B-4` after `B-4` was closed.** Finding 3.
- **`§R6.16`'s two-bug disclosure is real and not complete.** Finding 1, 3, 4, 6 are the rest.
- Round 5's why-block compression claim holds on the three-clause count (`U6-6` / `§R6.18`); I disagree only that all three are motivation (finding 10).
- Round 3's `:2383`/`:2384` as history: I agree with the ruling, including that `R3-P3` is still the wrong pairing under the new matrix and must not be "repaired."
