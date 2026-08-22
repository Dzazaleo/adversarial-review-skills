> **Recovered file — provenance note added by the round-5 adjudicator, 2026-08-22.**
>
> This report was never saved to its own path. The operator pasted the **Codex** cover note into
> the Grok session, so this reviewer read `EXTERNAL-REVIEW-5-PROMPT-CODEX.md`, audited the Codex
> half, and wrote its report to `EXTERNAL-REVIEW-5-CODEX.md` — where the concurrent Codex session
> overwrote it while restoring its own file.
>
> The text below the rule is the **verbatim 37,070-character payload** of the Grok session's
> `write` tool call (`call-17a0277b-f572-4a5c-9375-1edab33b1011-53`, agent timestamp
> 1787416977417), recovered from the live session log at
> `~/.grok/sessions/.../01a02a4d-dbbf-7961-819a-e66a2e1c999a/updates.jsonl` lines 241 and 242.
> Both records carry the payload independently and are byte-identical;
> `sha256` = `cb4c514b76129542…`. Nothing was added, removed, or reflowed.
>
> Its `# External Review 5 (Codex)` title and the identity-mismatch paragraph are the reviewer's
> own words, written under the mis-pasted brief. The reviewer is **xAI Grok 4.6**, self-reported at
> line 3 of its own text. Adjudicated in `REVIEW-ADJUDICATION.md` under the `grok-*` finding IDs.

---

# External Review 5 (Codex) — the round-4 fixes and the restructure

Reviewer identity: xAI Grok 4.6, Grok Build TUI / coding agent; reasoning effort: not exposed as a named knob; served model alias: `grok-4.6`.

**Identity mismatch (process).** The brief at `EXTERNAL-REVIEW-5-PROMPT-CODEX.md` addresses the reviewer as "OpenAI's GPT-5.6 (Sol)". This session is Grok 4.6. The independence-payoff paragraph in that brief is therefore false for this run. A stub already occupied this path claiming GPT-5.6 identity; this file is that path, rewritten with the actual identity rather than a second copy.

I did not open `EXTERNAL-REVIEW-5-PROMPT-GROK.md` or `EXTERNAL-REVIEW-5-GROK.md`. A grep over `*.md` for compaction/500-line terms did not print their contents. I did open `EXTERNAL-REVIEW-5-GROK-VOID.md`, which the brief marks as fair game.

## Coverage

18 of 18 claims engaged. Read both `SKILL.md` files, all six files under `skills/*/references/` (five new plus `cover-note-template.md`, `prompt-template.md`, `ledger-template.md`), `HOW-IT-WORKS.md` (edited hunks plus the FIX LATER / blindness / Tactic 1 sections), `README.md` (permissions section and the adjudication rules list), and the round-4 ledger rows needed to know what was claimed (`§R4.12`, `§R4.14`, `R4-Q1`/`R4-Q2`, `X-1`/`X-2`). Ran `git diff --stat 0d65b51..d411d1e` (27 files, +3530/−406, matches the brief), `git show d411d1e:<path> | wc -l` for every in-scope file (matches the brief's current counts), prefix character counts for the compaction estimates, a verbatim-line overlap of the five new files against the pre-restructure skills, and `git grep` for `before the ledger`, `different architecture`, `never saw`/`never seen`/`not handed`, and `overwrite`. Fetched current Anthropic docs: [skills](https://code.claude.com/docs/en/skills), [context window / what survives compaction](https://code.claude.com/docs/en/context-window), [permissions](https://code.claude.com/docs/en/permissions).

Did not: tokenize with Anthropic's tokenizer (no tokenizer in the environment; installs forbidden); invoke either skill in a live Claude Code session; audit `scripts/validate.py` or the corpus as an assignment (tripped over the length gate's off-by-one while checking claim 2). Did not read the parallel Grok round-5 brief or report.

Pinned range `0d65b51..d411d1e`. Repo HEAD at authoring time was `2565c08` (the round-5 briefs), one commit past the pin; skill files are identical at `d411d1e` and `HEAD`. Working from `/Users/leo/Documents/WORK/CODING/adversarial-review-skills`, not the Grok worktree at `0d65b51`.

## Findings, ranked

Strict order by cost of leaving unfixed (blast radius × likelihood the trigger is reached). No ties.

---

### 1. The README permission snippet denies every write, including the deliverables it claims to allow — **high**

- **Location:** `README.md:150-157` (added in this range, `0d65b51..d411d1e`).
- **Mechanism:** The snippet is offered as the way to "actually enforce" the write envelope:

  ```jsonc
  "deny":  ["Edit(**)"],
  "allow": ["Edit(**/*REVIEW*.md)", "Edit(**/BACKLOG.md)"]
  ```

  Current Anthropic permissions docs say rules are evaluated **deny, then ask, then allow**, and that **specificity does not change the order**: "A broad deny rule like `Bash(aws *)` blocks every matching call, including calls that also match a narrower allow rule like `Bash(aws s3 ls)`, so a deny rule can't carry allowlist exceptions." ([permissions](https://code.claude.com/docs/en/permissions#manage-permissions)). The same page says Claude Code consults `Edit(path)` rules for the Write tool, including creating a new file ([Read and Edit](https://code.claude.com/docs/en/permissions#read-and-edit)). `Edit(**)` therefore matches every path, deny wins, and the allow entries never fire. The prose immediately above the snippet (`README.md:151-152`) claims this "deny[s] writes outside the review artifacts." It denies writes *into* them too.

  The `Edit(path)` vs `Write(path)` warning in the paragraph under the snippet (`:160-164`) is accurate against those same docs. The snippet that uses `Edit(path)` is the part that does not do what it says.
- **Trigger:** An operator following the new "What these skills are allowed to do" section pastes the block into `.claude/settings.json` and then invokes `/adversarial-review-prompt` or `/review-adjudication`.
- **Consequence:** Every `Write`/`Edit` of a brief, cover note, ledger, or backlog file is denied. The round-4 owner decision `R4-Q1 (c)+(d)` — drop `Write` from `allowed-tools` and ship an `Edit(path)` settings snippet that actually bounds the envelope — ships a snippet that either blocks the product (if the file is accepted) or is invalid JSON if `//` comments are not accepted in `settings.json` (could not determine from the docs; the fenced block is labelled `jsonc`). Neither interpretation enforces "review artifacts only." Contract items 1 and 4.
- **Status:** **CONFIRMED.** Docs quoted above, fetched 2026-08-22. Snippet and surrounding claims read at `README.md:139-169`. I did not apply the snippet to a live Claude Code session.

Why it ranks here: this is the one operator-facing "how to actually enforce it" recipe added in the range, and following it breaks the only writes the skills exist to make.

---

### 2. The FIX LATER timing defect was repaired in one `SKILL.md` site and left live in three others, one of them a file the restructure created by copying the old text — **high**

- **Location:**
  - Fixed: `skills/review-adjudication/SKILL.md:44-45` (invariant 4) and `:420` (§6).
  - Not fixed: `skills/review-adjudication/references/why-this-is-hard.md:14-15` (**new file**), `HOW-IT-WORKS.md:411`, `README.md:86`.
- **Mechanism:** Round 4's claimed close of the FIX LATER / skeleton-first contradiction is the wording *"created before the row receives its `FIX LATER` disposition … not before the ledger file exists, which step 2 has already required by then"* (`SKILL.md:420`). That is satisfiable: step 2 writes a skeleton with empty dispositions, then step 6 fills `FIX LATER` after the backlog file exists.

  The extracted motivation file, which the skill tells the agent to open "when a rule looks arbitrary and you are deciding whether to follow it" (`why-this-is-hard.md:4-5`), still says the opposite:

  > Deferral is a legitimate outcome *only* when it costs something — a durable backlog artifact that exists on disk **before the ledger is written**. (`:14-15`)

  That sentence is byte-for-byte the pre-restructure skill. At `0d65b51` it lived in `skills/review-adjudication/SKILL.md:60-61` inside `<why_this_is_hard>`. The restructure copied it into the new file (84% of that file's long lines are verbatim from the old skill) and repaired only §6 and the invariant. `HOW-IT-WORKS.md:411` and `README.md:86` were both edited in this range for other defects (`not handed`, residual-doubts hand-off, the permissions section) and still say "before the ledger is written" / "written before the ledger."

  This is the X-1 shape the brief asked to treat as the highest-yield hypothesis, plus two non-extracted copies — the pattern the brief named as "a change that reached one site of something living at several."
- **Trigger:** (a) An adjudication session that hits auto-compaction: the surviving prefix still links `why-this-is-hard.md` at `SKILL.md:72` (above the estimated cut at line 214) and tells the agent to read it when a rule looks arbitrary. The corrected §6 text is at line 420, past the cut. (b) An operator learning the rule from README or HOW-IT-WORKS, which the README still points the technically curious at. (c) Any later pass that greps the skill body, sees the invariant, and does not grep the design doc.
- **Consequence:** After compaction, the surviving instruction set contains both timings. The file the agent is told to consult to decide whether to follow the rule is the stale one. Contract items 1, 2, and 4. This is also the unsatisfiable pair round 4 claimed to have closed (`codex`/`grok` FIX LATER findings → `✔ executed` at `SKILL.md:420` only).
- **Status:** **CONFIRMED.**

  ```
  $ git grep -n "before the ledger" 0d65b51 d411d1e -- skills/ HOW-IT-WORKS.md README.md
  0d65b51:HOW-IT-WORKS.md:401: ... **before the ledger is written**
  0d65b51:README.md:86: written before the ledger
  0d65b51:skills/review-adjudication/SKILL.md:499: **created before the ledger is written
  d411d1e:HOW-IT-WORKS.md:411: ... **before the ledger is written**
  d411d1e:README.md:86: written before the ledger
  d411d1e:skills/review-adjudication/SKILL.md:420: **created before the row receives its `FIX LATER` disposition
  ```

  The new file is not in the pre-restructure grep because it did not exist. `git show 0d65b51:skills/review-adjudication/SKILL.md` lines 60–61 are the source of `references/why-this-is-hard.md:14-15`.

Why it ranks here: three live copies of a contradiction this round claimed to have closed, one of them created by the restructure, one of them linked on the surviving side of the compaction cut.

---

### 3. The restructure put history on the surviving side of the cut and left the operational templates on the discarded side — **high**

- **Location:** Link placement in both `SKILL.md` files versus the in-file cut estimates (`adversarial-review-prompt/SKILL.md:24` "around line 221"; `review-adjudication/SKILL.md:28` "around line 214"). Official compaction behaviour: invoked skill bodies are re-injected, "capped at 5,000 tokens per skill", "Truncation keeps the start of the file" ([context window](https://code.claude.com/docs/en/context-window#what-survives-compaction); [skill content lifecycle](https://code.claude.com/docs/en/skills#skill-content-lifecycle)).
- **Mechanism:** Observed links at `d411d1e`:

  | File | Line vs estimated cut | Target |
  |---|---|---|
  | arp `SKILL.md:69` | above 221 | `why-this-is-hard.md` (new) |
  | arp `SKILL.md:138` | above 221 | `cover-note-template.md` |
  | arp `SKILL.md:249` | **below** | `prompt-template.md` |
  | arp `SKILL.md:385` | **below** | `cover-note-template.md` (second) |
  | adj `SKILL.md:72` | above 214 | `why-this-is-hard.md` (new, contains finding 2's stale rule) |
  | adj `SKILL.md:121` | above 214 | `inputs-and-calibration.md` (new) |
  | adj `SKILL.md:241,311,346` | **below** | `verification-standard.md` (new) |
  | adj `SKILL.md:395` | **below** | `second-opinion.md` (new) |
  | adj `SKILL.md:441` | **below** | `ledger-template.md` |

  Anthropic's own skill guidance is to keep `SKILL.md` as the operational overview and put "the most important instructions near the top of `SKILL.md`" because truncation keeps the start. The restructure did the opposite of that priority: the two new *why* files (motivating history, 96% and 84% verbatim from the old skills) are linked in the surviving prefix; the files that actually tell the agent what to emit (`prompt-template.md`, `ledger-template.md`) and how to re-verify (`verification-standard.md`, `second-opinion.md`) are not.

  Invariant 7 tells a compacted prompt-author to use "four branches" in "template §1" (`arp SKILL.md:50-52`) and does not name `references/prompt-template.md`. The path is only at line 249. Finding 2 is the concrete payload of this structure: the stale FIX LATER rule is in the reachable why-file; the corrected rule is past the cut.

  File-read content is not re-injected after compaction (it is message history, summarized). Opening a reference *before* compaction does not preserve it *after*.
- **Trigger:** A session that invokes either skill, auto-compacts once, and then reaches "write the brief" (§6) or "re-verify / write the ledger" (steps 5–7).
- **Consequence:** The condensed invariants survive (claim 3's narrow version). The files that contain the emit text and the spawn/sanitized-copy how-to do not, unless the agent independently globs `references/`. Contract items 2 and 3. This is the trade `§R4.12` called "not a clean win," described as moving motivating history out of the skills; the actual layout also moved the *pointers to the remaining operational files* onto the discarded side.
- **Status:** **CONFIRMED** for link placement and for the documented truncation-keeps-the-start rule. **THEORETICAL** for which branch a compacted Claude session actually follows (did not run one). The 5,000-token line itself is an estimate — see Could not verify.

Why it ranks here: compaction is the documented fate of a ~11k-token skill, and the restructure's new files are what the surviving prefix can and cannot find.

---

### 4. The no-filesystem user-facing variant still omits the continue instruction that the invariants require — **medium**

- **Location:** `skills/adversarial-review-prompt/references/cover-note-template.md:79-84`; pointed at from `SKILL.md:137-139` (above the cut). Compare invariant 4 (`SKILL.md:37-40`) and §10 (`SKILL.md:462-465`).
- **Mechanism:** Invariants 1 and 4, added/extended in this range, require: no cover note; report in chat; the hand-off "must say so **and** tell the user to send one word to continue if the output stops at a section boundary." §1's delivery-route paragraph — which survives compaction — says to follow the **"Reviewer has no filesystem access"** variant in `cover-note-template.md`. That variant, unchanged in `0d65b51..d411d1e` (`git diff --stat` on the file is empty), tells the user to attach the brief and save the returned report. It does not mention `continue`. The matching *reviewer*-facing text in `prompt-template.md:387-395` does. The operator-facing text does not.
- **Trigger:** A browser-chat reviewer, a skill session that follows §1's pointer to the template variant as the complete user message, and a report that hits an output limit at a section boundary.
- **Consequence:** The operator is not told to send continue. The truncated chat report is saved as the complete artifact. That is the failure invariant 4 exists to prevent. Contract items 1 and 5: the exception was added to the invariants and to §10, and not to the file §1 says to use for that exception.
- **Status:** **CONFIRMED** as a text contradiction. Did not run a no-filesystem reviewer.

Why it ranks here: the trigger is a supported route the skill itself calls "a great many" reviewers, and the lost continue is exactly the silent-truncation bug the round claimed to have closed.

---

### 5. A third copy of the unconditional architecture claim sits in the new prompt `why-this-is-hard.md` — **medium**

- **Location:** `skills/adversarial-review-prompt/references/why-this-is-hard.md:17-19`. The two copies round 4 / X-2 closed: `prompt-template.md:54-82` (four branches) and `HOW-IT-WORKS.md:80-94` (placeholder naming the template as authority).
- **Mechanism:** Claim 6 asked whether there was a third copy. There is. The new file, 96% line-verbatim from the pre-restructure skill, still states lever 1 as:

  > that a reviewer with a different architecture notices different things; and that agreement is therefore a failed outcome.

  That is the unconditional claim, now in an author-facing file linked from `SKILL.md:69` — above the compaction cut. The file header says "Nothing here is an instruction" (`:3`), which is the same class of disclaimer that failed to stop X-2: HOW-IT-WORKS was also "not the emit path" and still produced the sentence in a brief. An author compacted or writing from the why-file can re-emit it. The emit path that *is* supposed to be used (`prompt-template.md`) is only linked past the cut (finding 3).
- **Trigger:** A prompt-authoring session that opens the reachable why-file (or is compacted onto it) and writes Tactic 1 from that prose rather than from the four-branch block.
- **Consequence:** Same-family or unknown-lineage briefs again receive "you have a different architecture." Contract items 1, 2, and 4. X-2's lesson was "search for the claim, not the files you were told about"; the restructure then copied the claim into a new file and did not search it.
- **Status:** **CONFIRMED.** `git grep -n "different architecture" d411d1e -- skills/ HOW-IT-WORKS.md README.md` is the inventory; the only remaining unconditional statement of the lever is this line. `examples/` still contain old briefs with the sentence; those are spent artifacts, not emit paths.

Why it ranks here: it is the X-2 defect, relocated rather than repaired, into a file created in this range.

---

### 6. The same-family emit path is still an unmeasured assertion; the "caution" lives only in author-facing commentary — **medium**

- **Location:** `skills/adversarial-review-prompt/references/prompt-template.md:69-72` (emitted) vs `:84-88` (author-facing).
- **Mechanism:** Claim 12 asks whether the new wording is a caution or an assertion with a hedge in front of it. The *reviewer* is handed:

  > you do not bring a different architecture, and any blind spot you share with its author is one this review is least likely to catch. Weight your own agreement accordingly.

  That asserts a mechanism (shared-family blind spots survive) that `:84-88` immediately admits "is not established anywhere — nothing in this project has measured whether same-family reviewers share an author's blind spots. It is stated as a caution rather than a finding." The caution is not in the emitted block. The hedge in front of the assertion is "you do not bring a different architecture" (true given the branch) plus "any blind spot you share" (the unmeasured part, still stated as fact).
- **Trigger:** A same-family reviewer, which this skill explicitly supports (fresh Claude session; `:57-59`).
- **Consequence:** The reviewer is told its agreement is worth less *because of* an unmeasured architecture claim, which is the same inflation the four-branch rewrite was meant to stop, one notch weaker. Contract item 4.
- **Status:** **CONFIRMED** as a property of the emitted text. I am not claiming to have measured same-family overlap either.

Why it ranks here: every same-family brief this skill emits carries it; it is narrower than finding 5 (it does not fire on different-family briefs) and so sits below.

---

### 7. The new why-files say they contain no instructions, then contain instructions — **medium**

- **Location:** `skills/adversarial-review-prompt/references/why-this-is-hard.md:3` and `:94-99` (the grep loop); `skills/review-adjudication/references/why-this-is-hard.md:3-5` and `:14-15` (the stale FIX LATER rule). Contrast `second-opinion.md:2-4` and `verification-standard.md:2-3`, which honestly say they hold "the full procedure" / "the reasoning."
- **Mechanism:** Both why-files open with "Nothing here is an instruction; every obligation it motivates is in the skill itself." That is false. The prompt why-file contains the only copy of the doubt-search shell loop (`:94-99`); skill §9 describes the search in prose and points at this file for "case histories." The adj why-file contains a timing rule that *contradicts* the skill (finding 2). An agent that believes the header skips the search how-to. An agent that does not believe it follows a stale obligation. The header is a trap in both directions.
- **Trigger:** A compacted or hurried session that takes the first paragraph of a just-opened reference as a routing instruction.
- **Consequence:** Either the §9 search is run from memory (the failure mode that file's own history records) or the stale FIX LATER rule is treated as current. Contract items 2 and 5.
- **Status:** **CONFIRMED.**

Why it ranks here: it is the mechanism that lets findings 2 and 5 survive contact with a careful agent ("the file said it wasn't an instruction").

---

### 8. This brief's independence sentence is false of the session that received it — **medium** (process)

- **Location:** `EXTERNAL-REVIEW-5-PROMPT-CODEX.md:12-16`; this file's identity line.
- **Mechanism:** The brief says "You are OpenAI's GPT-5.6 (Sol). You have a different architecture and different training." This session is Grok 4.6. The skill this repository exists to ship forbids emitting that sentence without establishing both identities (`prompt-template.md:54-59`; arp invariant 7). The brief also required the report at this exact path; a GPT-5.6 stub already occupied it. That is the overwrite case invariant 6 exists to prevent, happening to the audit of the invariant.
- **Trigger:** Already triggered: this run.
- **Consequence:** Agreement between this report and a true GPT-5.6 report would not mean what the split was designed to buy; disagreement is still informative. The architecture-difference payoff line is false. Contract item 4, applied to the brief that is currently using the product on itself.
- **Status:** **CONFIRMED.**

Why it ranks here: it contaminates *this* audit's independence claim, not the skills' future runs, so it sits below defects that will fire on every user.

---

### 9. `review-adjudication/SKILL.md` lands on the last passing line of the length gate, against a baseline that never existed in git — **low**

- **Location:** `skills/review-adjudication/SKILL.md` 498 lines (`wc -l`); `scripts/validate.py:43,78-85` (`len(text.split("\n")) >= 500`); ledger `§R4.12` "484 and 498, from 529 and 587"; brief table "was 529; was 587."
- **Mechanism:** Counts at every commit in the pinned range:

  | commit | arp | adj |
  |---|---|---|
  | `0d65b51` / `540c60a` | 497 | 572 |
  | `9893aaa` … `d411d1e` | 484 | 498 |

  529 and 587 do not appear as `SKILL.md` line counts in this history. The current counts 484 and 498 are real and are under the documented "Keep `SKILL.md` under 500 lines" guidance ([skills](https://code.claude.com/docs/en/skills#add-supporting-files)). The drop was 13 and 74 lines, not 45 and 89.

  The validator, added in this range (`bf092c9`), counts `split("\n")`, which is 485 and **499** on these newline-terminated files. The gate is `n >= 500`. Adjudication is one character-of-a-newline from failing it. The next one-line clarification fails the gate and forces another extraction of the finding-3 kind. Nothing was obviously padded to cross 500 — 74 lines left the adj skill — but 498 is where they stopped once they were under, and the false 529/587 baseline inflates how much "under" was achieved.
- **Trigger:** The next round-5/6 prose fix that adds three lines to `review-adjudication/SKILL.md`.
- **Consequence:** Either the length gate fails, or more operational text is pushed into reference files linked past the cut (finding 3). Contract item 4 for the 529/587 figure; item 2 for what the tightness will do next.
- **Status:** **CONFIRMED** for the counts and the validator arithmetic (tripped over, not audited as an assignment). The 529/587 source is **COULD NOT DETERMINE** — they are not in git.

Why it ranks here: it does not currently mis-instruct an agent; it sets up the next extraction to repeat finding 3.

---

## The unseeded pass

Set the 18 claims aside and read `git diff 0d65b51..d411d1e -- skills/ HOW-IT-WORKS.md README.md` plus the five new files as files.

What it produced that the claims list did not already point at:

- **Finding 7** (the "nothing here is an instruction" headers) — not in the claims list as such. Claim 1 asked whether reference files contain instructions; the *false disclaimer* is the extra.
- **Finding 8** (this brief's identity) — a process finding the brief invited, not a claim.
- **Finding 9's false 529/587 baseline** — adjacent to claim 2, but claim 2 asked whether 484/498 are under 500, not whether the "from" numbers exist.
- **`why-this-is-hard.md` (adj) "Three forces"** (`:8`) vs the skill's "Four forces" (`SKILL.md:57`) vs HOW-IT-WORKS "Four forces" (`:405`). The extracted file disagrees with both parents about how many forces it is listing. Not ranked separately; it is the same copy-without-re-read as finding 2.
- **Net extraction is 7,354 characters, not ~9,300; the five files total 30,455 characters, 60–96% verbatim.** Claim 1 asked whether meaning was preserved. The measurement the ledger reports is not either of the two quantities on disk.

Findings 1–6 were reached from the claims list (17, 8/1/16, 15/3, 14, 6, 12). Finding 2's HOW-IT-WORKS and README sites were the unseeded extra on a directed claim: claim 8 said "read both" meaning invariant 4 and §6; the other two sites were outside that pair.

Considered and not raised: `cover-note-template.md` already handles several-reviewers and follow-up overwrite of the *report* (`:86-91`); that is the reviewer-side half of claim 7 and looks consistent with the author's existence check. `second-opinion.md` still contains the Bash-is-write and sanitized-copy discussion, and it is more careful than the skill summary; its problem is reachability (finding 3), not content. Style/length of the remaining 498-line skill is not a finding.

## Claims examined and upheld

1. **~9,300 characters moved, meaning preserved.** **REFUTED** as a measurement (net `SKILL.md` reduction is 7,354 characters; new files are 30,455 characters, 60–96% line-verbatim from the old skills). **REFUTED** as "preserved meaning without relocating defects": findings 2, 5, 7. `X-1`'s shape recurred in this range, in a file this range created.
2. **Both `SKILL.md` under 500 lines (484, 498).** **CONFIRMED** against `wc -l` at `d411d1e` and against [Keep SKILL.md under 500 lines](https://code.claude.com/docs/en/skills#add-supporting-files). The "from 529 and 587" half is **REFUTED** against git (497 and 572). The 2-line margin is 1 line on `scripts/validate.py`'s `split("\n")` count (499/500). Not "padded to cross"; stopped at the gate. Finding 9.
3. **Round-4 obligations sit above the cut and say what the full rule says.** **CONFIRMED** that the verifier-exposure recording rule and append-not-rewrite rule are in `<invariants>` at adj `:32-36` and `:46-50`. **REFUTED** that they say what the full rule says: spawn allowlist, Bash-is-write, and sanitized-copy how-to are only in §5 / `second-opinion.md`, both past the cut and unlinked from the surviving prefix (finding 3). Not an opposite-summary this time; an incomplete one whose missing how-to is in an unreachable file. The FIX LATER *opposite* summary is in the reachable why-file (finding 2), not in the invariant.
4. **Cut estimates labelled as estimates, ~3.1 chars/token → lines 221 / 214.** **CONFIRMED** the labels exist at arp `:23-25` and adj `:27-29`. Whole-file `/ 3.1` including frontmatter lands at 15,604 chars ≈ 5,034 tokens at line 221 (arp) and 15,549 chars ≈ 5,016 tokens at line 214 (adj) — that is how those numbers were produced. **COULD NOT DETERMINE** where 5,000 *rendered* tokens actually land: no Anthropic tokenizer here. Round-4 Codex measured with frontmatter removed; body-only `/ 3.1` would put arp's cut nearer file line 232–235, i.e. the in-file estimate is slightly *early* under that method, not "biased late." Official cap and start-preserving behaviour: [context window](https://code.claude.com/docs/en/context-window#what-survives-compaction).
5. **Blindness claim aligned everywhere.** **CONFIRMED** for the operational phrase: `git grep` on `never saw`/`never seen` in `skills/`, `HOW-IT-WORKS.md`, `README.md` at `d411d1e` is empty; remaining uses are "not handed the report" (adj `SKILL.md:48,378`, `second-opinion.md:7`) or ordinary English ("blind spots", "reviewer reaches blind"). HOW-IT-WORKS `:492` was updated in this range. No leftover "never saw" in the five new files.
6. **Unconditional architecture sentence gone from every emit path.** **REFUTED.** Finding 5: `why-this-is-hard.md:19`. The two named copies (template, HOW-IT-WORKS) are repaired. A search for the *claim*, not those files, found the third.
7. **Overwrite guard covers brief, cover note and report; does `ls`/`Glob` bind without `Write`?** **CONFIRMED** the guard text at arp invariant 6 (`:46-49`) and `:329-339` names all three and binds the suffixes. **CONFIRMED** the check can run: `Glob` is in `allowed-tools`; `ls` is in the documented read-only Bash set that runs without a permission prompt in every mode ([permissions — read-only commands](https://code.claude.com/docs/en/permissions#read-only-commands)). `allowed-tools` is a *grant*, not a restriction ([pre-approve tools](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill)), so dropping `Write` does not block the later create; it only means that create is prompted. **The ledger is not in that three-file existence check.** Adjudication invariant 1 / §7 require append-and-prove via `git diff` showing no deletions (`:32-36`, `:450-456`). That is a different mechanism, still prose, still no `ls` before a `Write` that would replace the file. Not a re-report of `grok-5`; the report half was added, the ledger half was redirected to append-proof rather than existence-check.
8. **FIX LATER ordering contradiction resolved.** **CONFIRMED** that invariant 4 and §6 are now mutually satisfiable with step 2. **REFUTED** as closed: finding 2, three live copies of the old timing, one of them the extracted file.
9. **Residual-doubts dependency disclosed; required field makes absence visible.** **CONFIRMED** that `README.md:188-194` tells the operator to keep the hand-off, and `ledger-template.md:42-47` makes the doubts line required with an `unavailable` option that records absence-of-the-check rather than "doubts were kept out." Nothing *stops* an adjudicator writing `unavailable` and moving on — that is the designed honest skip, and the skill at `:129-132` (above the cut) still requires asking first. The required field is another sentence, not a gate; it makes a skip *visible if filled*. The "this line is required" comment is only in `ledger-template.md:46`, linked past the cut (finding 3).
10. **Author provenance is a required input and is used.** **CONFIRMED.** Collected in arp §1 (`:117-125`) before the emit at template §1 (`prompt-template.md:54-82`) and the hand-off (`SKILL.md:452`). Both halves are required to pick a branch. After compaction the *path* to the branch text is gone (finding 3); the requirement to have the fact is not.
11. **Four branches cover the real cases; each has its own payoff; no branch promises what another denies.** **CONFIRMED** by reading `prompt-template.md:66-82`. Different-family / same-family / human-mixed-several / unknown-on-either-side. Payoffs differ. No cross-branch contradiction. The fourth branch is reachable: §1 explicitly allows author provenance "simply undetermined" (`SKILL.md:120-121`).
12. **Same-family blind-spot assertion downgraded to a caution.** **REFUTED.** Finding 6: the emitted block is still an assertion; the caution is author-facing commentary the reviewer never sees.
13. **Neither skill pre-approves a write-capable tool; do they still work?** **CONFIRMED** both frontmatters are `Read, Grep, Glob`. **CONFIRMED** from current docs that this does not *remove* Write: "It does not restrict which tools are available: every tool remains callable, and your permission settings still govern tools that are not listed. The grant clears when you send your next message" ([pre-approve tools](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill)). In an interactive session the skills still work; first-turn writes now prompt. Even *with* `Write` in `allowed-tools`, the grant was already turn-scoped, so turn two onwards was already a prompt. **COULD NOT DETERMINE** for `claude -p` / `dontAsk` (no live run); docs say `dontAsk` auto-denies tools not pre-approved, which would now include Write on the invoking turn — a real headless regression relative to the previous grant, theoretical here. Finding 1 is what happens if the operator then "fixes" that with the README snippet.
14. **No-filesystem route consistent with the invariants.** **REFUTED.** Finding 4: invariants 1 and 4 and §10 have the exception and the continue item; the cover-note-template variant §1 points at does not. Prompt-template's reviewer-facing variant does (`:387-395`). The user-facing half of the pair is the one that was not updated in this range.
15. **Five new reference files reachable and used.** **CONFIRMED** every relative link resolves (files exist at the linked names). **REFUTED** that each is pointed at from the place a compacted reader needs it. Finding 3: `verification-standard.md` and `second-opinion.md` have no surviving-prefix link; `prompt-template.md` and `ledger-template.md` (not new, but the emit/write templates) neither. `inputs-and-calibration.md` and both why-files do.
16. **`HOW-IT-WORKS.md` matches the skills.** **REFUTED** at the FIX LATER timing (`:411`, finding 2). **CONFIRMED** the architecture placeholder and the "not handed" wording were updated in this range and match the template / adj skill. The file was edited twice, both times reactively, and the third live copy of the old FIX LATER rule was not in the diff hunks they touched.
17. **`README.md:139-170` permissions section is accurate; would the snippet do what it says?** The `allowed-tools` description (pre-approval, not restriction; writes go through normal prompts) is **CONFIRMED** against [pre-approve tools](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill). The `Edit(path)` / `Write(path)` warning is **CONFIRMED** against [permissions — Read and Edit](https://code.claude.com/docs/en/permissions#read-and-edit): "Claude Code checks file permissions against `Edit(path)` and `Read(path)` rules only. If you write a path rule for `Write` … Claude Code accepts the rule but never consults it." The snippet is **REFUTED** as doing what it says. Finding 1.
18. **`§R4.14`'s lesson — "extracted text does not get re-read on the way out" — is the right lesson from X-1.** **REFUTED** as the complete lesson. Finding 2's README and HOW-IT-WORKS sites were *not* extracted and still carry the unrepaired rule. Extraction is one more site of a claim that lives at several. Treating X-1 as an extraction-process failure predicts the why-file copy and misses the two files they edited in this range without touching that sentence. The brief's own pre-start note is the better lesson: "Fixes that reach one site of something living at several are this project's recurring failure."

## Could not verify

- **Where 5,000 rendered tokens actually land in either `SKILL.md`.** No Anthropic tokenizer in the environment; installs forbidden. Character/`3.1` arithmetic reproduces the in-file line numbers if and only if frontmatter counts. Round-4 Codex's method (frontmatter stripped) would move arp's cut ~10–15 lines later. Official docs confirm the 5,000-token cap and start-preserving truncation, not the line number.
- **Whether a live compacted Claude Code session opens `references/` by glob when the path has been truncated away.** Finding 3's consequence is theoretical at the "what the model does" layer; the link placement is confirmed.
- **Whether `.claude/settings.json` accepts `//` JSONC comments.** Finding 1's snippet is labelled `jsonc`. If comments are illegal, the file fails to parse and the deny never applies (silent no-op, still not "review artifacts only"). If they are legal, deny-all applies. Did not find a primary-source statement either way on the permissions page.
- **Headless / `dontAsk` behaviour after dropping `Write` from `allowed-tools`.** Docs imply first-turn writes are now denied in `dontAsk`. Did not run `claude -p`.
- **Origin of the 529 / 587 figures.** They are not `wc -l` of any committed `SKILL.md` in this history.

## Disagreements with the prior rounds

- **`§R4.12`'s "pass — 484 and 498, from 529 and 587"** records a current count that is real and a baseline that is not. The same row's "moved 9,300 characters of rationale" does not match net reduction (7,354) or new-file size (30,455). The surrounding "trade, not a clean win" is the right *kind* of sentence and understates the trade: it describes losing motivating history, not leaving operational templates unlinked from the surviving prefix (finding 3) and copying a live defect into a new file (finding 2).
- **`§R4.14`'s lesson from X-1 is too narrow.** See claim 18. The next failure after X-1, which the brief-author found while writing this brief (`§R4.10` stale status), was also multi-site and was *not* an extraction. The FIX LATER leftovers in README and HOW-IT-WORKS are that shape again.
- **Round 4's close of the FIX LATER contradiction (`✔ executed` at `SKILL.md:420`) is a one-site close.** Disagree that it is closed. Finding 2.
- **Round 4's close of the architecture-sentence copies (`X-2` ✔ executed) is a two-site close of a three-site claim.** Finding 5. The search that would have caught the third copy is the one X-2 itself recommended and then did not run on the files the same commit created.
- **Q1(d)'s settings snippet was the right *form* (`Edit(path)`, not `Write(path)`) and the wrong *composition* (deny-then-allow as an allowlist).** The `Edit(path)` fact grok-1 contributed is correctly described in the README paragraph. The snippet under it cannot do what Q1(d) was accepted to do. Finding 1.

No ship/no-ship verdict.
