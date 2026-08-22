# External Review 5 (Codex) — the round-4 fixes and the restructure

Reviewer identity: OpenAI GPT-5.6 (Sol), Codex; reasoning effort: not exposed to the model; served model alias: `gpt-5.6-sol`

**Independence contamination.** I did not open `EXTERNAL-REVIEW-5-PROMPT-GROK.md` or `EXTERNAL-REVIEW-5-GROK.md`. A concurrent Grok session nevertheless overwrote this authorized output path twice: first with an identity stub, then—after I restored and appended my own findings—with its complete report. I necessarily saw portions while diagnosing failed appends. The core findings below were identified and written before the full-report overwrite; later checks use my own commands and source reads. The collision means this report is not cleanly blind to the other reviewer, and that limitation should be retained when the two reports are compared.

## Coverage

18 of 18 claims engaged. Read both `SKILL.md` files in full, all eight linked reference files, `README.md` and `HOW-IT-WORKS.md` in full, the skills/design-doc diff, the pre-restructure skill versions, and the relevant round-4 ledger rulings. Ran pinned `git diff`/`show`, whole-scope `rg`, `wc`, reference/link and prefix checks, `python3 scripts/validate.py` (all 10 checks pass, three pre-existing closed-ledger warnings), five read-only Claude Code token-prefix probes under `/tmp`, and current Anthropic documentation lookups. The live branch had advanced to `2565c08`, so substantive inspection used `d411d1e` snapshots; assigned paths were unchanged above it. I did not substantively audit validator logic, the calibration corpus, or backlog/ledger content outside the rulings needed for prior-ground context. I did not open either forbidden Grok file, but the concurrent output-path overwrite disclosed above contaminated reviewer independence.

## Findings, ranked

Strict order by cost of leaving unfixed; no ties.

### 1. Required reference procedures are linked only below the compaction cut

- **Impact** — high
- **Location** — `skills/adversarial-review-prompt/SKILL.md:206-214,247-253`; `skills/review-adjudication/SKILL.md:241,310-311,345-346,395`; `skills/review-adjudication/references/second-opinion.md`; `references/verification-standard.md`.
- **Mechanism** — Supporting files are useful after compaction only if the retained prefix tells Claude what exists and when to load it. The prompt template's only path is at `:249`, below the measured cut. The adjudication links to `verification-standard.md` and `second-opinion.md` are all below its cut. The retained invariant requires a second opinion but records only exposure; it omits the required restricted-agent setup and the sanitized-copy procedure, and a spawned agent does not inherit the skill. The restructure moved the procedure out but left its navigation on the discarded side.
- **Trigger** — The skill is invoked, the long read/verification work causes one auto-compaction before prompt emission or before a high-impact self-refutation, and the reference was not proactively opened earlier.
- **Consequence** — Prompt generation can improvise the four-branch/no-filesystem/deliverable template, while adjudication can spawn an unrestricted verifier that never received the write boundary. Contract items 2, 3, and 5 fail.
- **Status — CONFIRMED** for link placement and retained content; **THEORETICAL** for the model's post-cut choice. Anthropic says references must be named from `SKILL.md` so Claude knows when to load them and that compaction keeps only the first 5,000 tokens ([skills documentation](https://code.claude.com/docs/en/slash-commands)).
- **Pass** — directed, claims 3 and 15; also found while tracing the extracted files end to end.
- **Why it ranks here** — it affects both skills' late deliverables on the ordinary long-session path and can silently remove the only safe procedure for a write-capable verifier.

### 2. The extracted second-opinion procedure says a `Bash`-capable verifier cannot modify the target

- **Impact** — high
- **Location** — `skills/review-adjudication/references/second-opinion.md:27-40` versus `:46-53`; correct warning at `skills/review-adjudication/SKILL.md:385-394`.
- **Mechanism** — The reference correctly says `Bash` is write-capable and a verifier retaining it is trusted rather than confined, then nine lines later says “Excluding `Write` and `Edit` stops the verifier modifying the target.” The prescribed `Read, Bash, Glob, Grep` verifier can still write through an arbitrary subprocess. The stale sentence was extracted unchanged and placed after the round-4 correction without reconciliation.
- **Trigger** — A high/critical self-authored finding reaches second opinion, the verifier retains `Bash`, and the adjudicator relies on the later confinement claim.
- **Consequence** — A write-capable verifier can be represented as confined and can mutate the evidence while forming its opinion. Contract items 1, 2, 4, and 5 fail.
- **Status — CONFIRMED.** Anthropic states that `Edit`/`Read` rules do not constrain arbitrary subprocesses that open files ([permissions](https://code.claude.com/docs/en/permissions#read-and-edit)).
- **Pass** — directed, claims 1 and 15; independently found by reading the extracted procedure.
- **Why it ranks here** — it can let the mandatory verifier alter the evidence while the ledger records a stronger confinement than existed.

### 3. The real compaction cut drops reopened upheld claims because the invariant forgot them

- **Impact** — high
- **Location** — `skills/review-adjudication/SKILL.md:26-30,40-42,189-202`; prompt comparison at `skills/adversarial-review-prompt/SKILL.md:22-26,203-214`.
- **Mechanism** — Current Claude tokenization places adjudication's 5,000-token boundary in line 197, not around line 214. The cut drops the step-2 upheld-claims bullet at `:200-202`; invariant 3 rescues process/CNV/prior-disagreement entries but omits reopened upheld claims (`U-N`). That obligation disappears after compaction. The prompt boundary is in line 209 rather than around 221, truncating the mandatory unseeded-pass explanation mid-rule.
- **Trigger** — Adjudication auto-compacts before/during step 2 and the report upheld a claim using only a comment or test name.
- **Consequence** — A false upheld claim can enter the next brief as covered ground while every retained invariant appears satisfied. Contract item 3 fails.
- **Status — CONFIRMED.** Claude Code 2.1.239 / Claude Sonnet 5 prefix probes, calibrated against the same baseline: adjudication through line 196 added ~4,990 cached input tokens and through 205 ~5,241; prompt through line 200 added ~4,786 and through 209 ~5,004. Anthropic documents the 5,000-token behavior and model-dependent tokenization ([skill lifecycle](https://code.claude.com/docs/en/slash-commands#skill-content-lifecycle), [token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)). All Claude probes ran read-only under `/tmp`; including the exploratory full-skill and baseline calls, they cost approximately $0.67 total.
- **Pass** — directed, claims 3 and 4.
- **Why it ranks here** — the trigger is common in long adjudications and a missed reopening becomes false covered ground for every later brief.

### 4. The hoisted append invariant forbids the skill's skeleton-first workflow

- **Impact** — medium
- **Location** — `skills/review-adjudication/SKILL.md:32-36`, contradicted by `:133-138`, `:182-187`, and narrowed at `:450-456`.
- **Mechanism** — Invariant 1 unconditionally requires additions-only at the ledger's end. The procedure requires writing a blank current-round skeleton and later filling it in place, which replaces text and produces deletions. Section 7 limits immutability to completed rounds; the compaction-surviving invariant expands it to every write.
- **Trigger** — A session creates the mandatory skeleton and fills its first verdict, especially after compaction removes the narrower §7 rule.
- **Consequence** — It must violate the invariant, append duplicate rows, or leave the skeleton empty. Contract items 3 and 5 fail.
- **Status — CONFIRMED.** Simultaneous textual requirements at `d411d1e`.
- **Pass** — directed, claim 3.
- **Why it ranks here** — every new/current round reaches skeleton filling, so the retained rule collides with the mandatory workflow before any verdict can be completed.

### 5. The repaired `FIX LATER` ordering remains in three live documents in its impossible form

- **Impact** — medium
- **Location** — `skills/review-adjudication/references/why-this-is-hard.md:13-15`; `HOW-IT-WORKS.md:408-415`; `README.md:83-87`; corrected rule at `skills/review-adjudication/SKILL.md:43-45,419-420`.
- **Mechanism** — Round 4 replaced “before the ledger is written” with “before the row receives its `FIX LATER` disposition” because step 2 writes the skeleton before dispositions exist. The new extracted rationale and both public docs still publish the superseded wording.
- **Trigger** — A reader follows any of those sites during a run that assigns `FIX LATER`.
- **Consequence** — The required order is already impossible when the disposition is chosen, reopening the round-4 failure. Contract items 1, 2, and 5 fail.
- **Status — CONFIRMED.** `rg -nF 'before the ledger is written'`; the reference phrase was moved unchanged.
- **Pass** — directed, claims 1, 8, and 16.
- **Why it ranks here** — it reopens a proven loss-of-deferral path at three reader-facing sites, but only when a finding is deferred.

### 6. The extracted rationale weakens the high-impact refutation burden from `AND` to `OR`

- **Impact** — medium
- **Location** — `skills/review-adjudication/SKILL.md:46-50,374-383`; `skills/review-adjudication/references/why-this-is-hard.md:24-27`.
- **Mechanism** — The operative invariant requires execution evidence **AND** a second opinion. The extracted rationale says high-impact self-refutations need execution evidence **OR** an independent check. It is unchanged pre-restructure text and directly lowers a conjunctive gate to either branch alone.
- **Trigger** — Claude authored the code, the reviewer rated a finding high/critical, and the adjudicator reads the linked rationale while deciding whether the expensive gate is necessary.
- **Consequence** — A self-refutation can be recorded without one mandatory check. Contract items 2 and 5 fail.
- **Status — CONFIRMED.** The `AND` and `OR` versions coexist; the `OR` sentence was moved unchanged.
- **Pass** — directed, claims 1, 3, and 16.
- **Why it ranks here** — it weakens the evidence gate at the exact high-impact self-refutation where dismissal is costliest, though that branch is less frequent than ordinary ledger writes.

### 7. Public workflow docs still certify doubt absence and call prompted echoes independent confirmation

- **Impact** — medium
- **Location** — `README.md:47-49,181-193`; `HOW-IT-WORKS.md:159-177,186-191,792-794`; corrected rules at both skills.
- **Mechanism** — The skills say doubt/claim overlap is normal, forbid the author to certify absence, require “no line found — unverified,” and reserve independence scoring for adjudication. README says doubts are “deliberately kept out,” rediscovery is “real confirmation,” and the hand-off identifies which “really were kept out.” HOW says hunches stay out “entirely” and “never enter the brief,” despite explaining overlap between those sentences.
- **Trigger** — A normal run returns a finding overlapping a sharp claim sub-question.
- **Consequence** — An echo is banked as independent corroboration before the required search, recreating the leakage failure. Contract items 1, 4, and 5 fail.
- **Status — CONFIRMED.** Current-doc comparison at `d411d1e`.
- **Pass** — directed, claims 9 and 16.
- **Why it ranks here** — it systematically inflates seeded findings, but adjudication can still undo the damage if the user retained the hand-off.

### 8. The no-filesystem route still requires the cover note it forbids

- **Impact** — medium
- **Location** — `skills/adversarial-review-prompt/SKILL.md:28-40,132-142,389-396,445-465`; `references/prompt-template.md:379-406`.
- **Mechanism** — The invariant and route correctly say a browser reviewer gets the brief alone, no cover note, and returns the report in chat. The final mandatory checklist still requires “The two file paths,” the cover note verbatim, and checking that the report file exists at run end, without an exception.
- **Trigger** — The reviewer is browser-only and the skill reaches §10.
- **Consequence** — Claude must fabricate forbidden artifacts or violate the checklist and can promise a file the reviewer cannot create. Contract items 1, 3, and 5 fail.
- **Status — CONFIRMED.** End-to-end route trace.
- **Pass** — directed, claim 14.
- **Why it ranks here** — it makes one supported delivery route internally impossible, but only browser-only reviewers take that route.

### 9. The README enforcement snippet denies the artifacts it claims to allow

- **Impact** — medium
- **Location** — `README.md:147-164`.
- **Mechanism** — The snippet denies `Edit(**)` and narrowly allows review/backlog paths. Claude Code evaluates deny before allow regardless of specificity; `Edit(path)` governs built-in `Edit` and `Write`. The broad deny therefore blocks the brief, cover note, report, ledger, and backlog too.
- **Trigger** — A user copies the recommended `.claude/settings.json` and either skill attempts its first write.
- **Consequence** — Neither skill can produce its deliverable under the advertised enforcement. Contract item 4 fails.
- **Status — CONFIRMED.** Anthropic documents deny-first precedence and says broad deny cannot carry narrow allow exceptions ([permissions](https://code.claude.com/docs/en/permissions#manage-permissions)); it also confirms `Edit(path)` governs `Write` ([Read and Edit](https://code.claude.com/docs/en/permissions#read-and-edit)).
- **Pass** — directed, claim 17.
- **Why it ranks here** — copying it blocks every deliverable, but the trigger is limited to users who opt into the recommended hard boundary.

### 10. The extracted prompt rationale still teaches the pre-branch framing

- **Impact** — medium
- **Location** — `skills/adversarial-review-prompt/references/why-this-is-hard.md:13-22`; contradicted by `SKILL.md:31-52,117-125` and `references/prompt-template.md:42-88`.
- **Mechanism** — The new reference says the author can state as process fact that one model wrote/reviewed/tested the work, a different-architecture reviewer notices different things, and agreement is therefore failed. The repaired skill supports human/mixed/unknown provenance, same-family reviewers, and rigorous zero-finding audits. The reference's “Nothing here is an instruction” header does not neutralize imperative text (“What you can state,” “Never imply”), and its link survives compaction while the four-branch template link does not.
- **Trigger** — Human/mixed or same-family work reaches framing after compaction and Claude opens the surviving rationale link.
- **Consequence** — Claude can emit false provenance/independence or pressure a reviewer to manufacture disagreement, violating contract items 2, 4, and 5.
- **Status — CONFIRMED.** The stale block was moved unchanged from the pre-restructure skill.
- **Pass** — directed, claims 1, 6, 11, and 15.
- **Why it ranks here** — it can bias or falsify framing after compaction, but the current emit template itself is correct when it remains available.

### 11. The “downgraded caution” still asserts an unmeasured likelihood

- **Impact** — low
- **Location** — `skills/adversarial-review-prompt/references/prompt-template.md:69-73,84-88`; `HOW-IT-WORKS.md:742-744`.
- **Mechanism** — The emitted branch says a shared blind spot is “least likely to catch” and instructs weighting agreement, while adjacent prose concedes no measurement. This is the prior “most likely to survive” claim restated inversely, not downgraded out of assertion; HOW generalizes it to “the more different … the better.”
- **Trigger** — Same-family reviewer branch.
- **Consequence** — Evidence is weighted by an admitted unmeasured proposition. Contract item 4 fails.
- **Status — CONFIRMED** as an unsupported emitted assertion; the empirical proposition itself remains unmeasured.
- **Pass** — directed, claim 12.
- **Why it ranks here** — it changes evidence weighting without support, but does not by itself create or erase a concrete finding.

### 12. The design doc still denies the chat-only dependency README now discloses

- **Impact** — low
- **Location** — `HOW-IT-WORKS.md:48-49`; contradicted by `:159-177`, `README.md:188-193`, and adjudication `SKILL.md:123-132`.
- **Mechanism** — HOW says everything matters is on disk and nothing matters in chat. The required residual-doubts hand-off is chat-only and irrecoverable unless the user saves it. README's stale copy was fixed; HOW's was not.
- **Trigger** — User closes the authoring chat before adjudication.
- **Consequence** — The leakage check is unavailable and independent-corroboration credit cannot be awarded. Contract items 1 and 5 fail.
- **Status — CONFIRMED.** Current-doc comparison.
- **Pass** — directed, claims 9 and 16.
- **Why it ranks here** — it can lose one independence check, but the README and adjudication skill now give the correct operator instruction.

### 13. Removing write tools does not guarantee the user sees each write

- **Impact** — low
- **Location** — `README.md:141-145`; both skill frontmatters `:5-8`.
- **Mechanism** — Omission from `allowed-tools` leaves tools callable under ordinary permissions; it does not force a prompt. `acceptEdits`, auto/bypass modes, or a matching allow rule can approve writes silently relative to the promised “you see it before it happens.”
- **Trigger** — Either skill runs under an auto-accepting edit configuration.
- **Consequence** — Public safety explanation overstates the frontmatter boundary. Contract item 4 fails; end-to-end function remains intact.
- **Status — CONFIRMED.** Anthropic says `allowed-tools` is prompt-free pre-approval, not restriction, and unlisted tools remain governed by settings ([skills permissions](https://code.claude.com/docs/en/slash-commands#pre-approve-tools-for-a-skill)).
- **Pass** — directed, claims 13 and 17.
- **Why it ranks here** — it is a false safety explanation whose actual behavior still follows the user's pre-existing permission configuration.

## The unseeded pass

I set the claims list aside and reread the pinned skills/design-doc diff and every current reference as a document, then traced each workflow from input to hand-off. It produced no additional repository defect wholly outside the 18 directed claims. It did independently reach finding 2 (the adjacent `Bash` contradiction), finding 4 (the append invariant versus current-round filling), and finding 10 (the extracted pre-branch framing), but claim 1 or 3 can reasonably be read broadly enough to seed each; I therefore do not credit them as free findings. The only genuinely unseeded process result was the concurrent overwrite of this report, disclosed at the top, and that is an execution-environment collision rather than a repository defect.

Considered and not raised: both files really are below the documented 500-line guidance; all relative reference links resolve in the un-compacted file; the residual-doubts `unavailable` value is an honest, visibly discounted fallback rather than a defect; and the remaining uses of “blind” are ordinary English or explicitly distinguish prompt isolation from read isolation. The independent pass was already underway before the full-report overwrite, but its evidentiary independence is still qualified by that later contamination.

## Claims examined and upheld

1. **REFUTED** — five files were created and much rationale moved, but findings 2, 5, 6, and 10 show meaning/obligations were not preserved; the exact “~9,300 characters moved” is not reconstructable because fixes and extraction share commit `9893aaa` (net skill reduction from the pinned base is 7,403 bytes, not a measure of movement).
2. **CONFIRMED** — `wc -l` at `d411d1e` gives 484 and 498, and Anthropic says “Keep `SKILL.md` under 500 lines”; two lines under is under ([skills](https://code.claude.com/docs/en/slash-commands#add-supporting-files)).
3. **REFUTED** — verifier exposure and append wording are above the cut, but the append summary contradicts current-round filling (finding 4) and the verifier's required safe procedure is linked only below the cut (finding 1).
4. **REFUTED** — labels are honestly estimates, but current Sonnet 5 probes place 5,000 tokens in prompt line 209 and adjudication line 197, not around 221/214; adjudication loses an obligation absent from its invariant (finding 3).
5. **CONFIRMED** — targeted search found no current “never saw/seen the report”; operative sites say “not handed” and explicitly record whether the verifier could have read it.
6. **CONFIRMED** for emit paths — the prompt template's four branches and `HOW-IT-WORKS.md` placeholder removed the unconditional emitted sentence; finding 10 is a stale rationale that can steer emission after the real template link is lost, not a third literal emit branch.
7. **CONFIRMED** — invariant 6 and §6 cover brief, cover note, and named report, bind suffixes, and can check them with pre-approved `Glob`; the ledger is separately read in step 1 and governed by append/backfill rules (whose overbroad invariant is finding 4).
8. **REFUTED** as a repository-wide close — invariant 4 and §6 are satisfiable, but the old impossible rule remains in the extracted rationale, README, and design doc (finding 5).
9. **CONFIRMED** — README discloses the hand-off dependency and the required template field makes “unavailable” visibly mean no independence check/no corroboration credit; nothing should prevent the honest fallback once the user cannot supply the hand-off.
10. **CONFIRMED** — author provenance is collected at prompt `SKILL.md:117-125` before template branch selection and is explicitly one of the two inputs choosing the branch.
11. **CONFIRMED** — different-family, same-family, human/mixed/several, and unknown-on-either-side branches are reachable from collected inputs and each carries its own payoff; claim 12 is about an assertion inside one branch, not missing case coverage.
12. **REFUTED** — “least likely to catch” is the same unmeasured relative-likelihood assertion in inverse wording, and the emitted reviewer sees the assertion rather than the author-facing “caution” label (finding 11).
13. **CONFIRMED with a documentation correction** — neither frontmatter pre-approves write, but omission does not remove write tools; default interactive runs stop for ordinary permission handling at the prompt skill's first brief save (`:325`) or adjudication's skeleton write (`:183`) and work if approved. Visibility is not guaranteed under auto-accepting settings (finding 13).
14. **REFUTED** — the invariants carry the exception and continuation, but final hand-off still mandates a nonexistent cover note/two paths/report-file check (finding 8).
15. **REFUTED** — all files and relative links resolve before compaction, but `prompt-template.md`, `verification-standard.md`, and `second-opinion.md` are not navigable from the retained prefix when their procedures are needed (finding 1).
16. **REFUTED** — stale `FIX LATER`, residual-doubt, and chat-dependency claims remain in `HOW-IT-WORKS.md` (findings 5, 7, and 12); the refutation-burden contradiction is in the extracted reference (finding 6).
17. **REFUTED** — README is right that `Edit(path)` governs built-in writes and `Write(path)` is ignored, but deny-first evaluation makes its broad-deny/narrow-allow snippet block the allowed artifacts; its guaranteed-prompt sentence is also too strong (findings 9 and 13).
18. **REFUTED** — “extracted text does not get re-read on the way out” describes one manifestation, not the controlling failure. Findings 5–7 and 12 include non-extracted public copies: the general defect is no claim inventory/single authority or repository-wide verification when a rule changes.

## Could not verify

- The exact historical quantity behind “~9,300 characters moved.” Commit history exposes the before/after committed trees, but the post-fix/pre-extraction intermediate state was never committed; net reduction is not movement.
- The cut line for every Claude model/version. The reported lines are measured for installed Claude Code 2.1.239 using Claude Sonnet 5; Anthropic documents that Claude 4.7+ uses a newer tokenizer and instructs recounting for the actual model. The invariant defect holds on the current served model, not universally at exactly the same line.
- Whether a real auto-compacted session would improvise a `Glob` search and recover references whose links disappeared. Source reachability is confirmed; the ultimate model choice remains theoretical.
- Whether same-family reviewers empirically share enough blind spots to justify the emitted weighting. No matched blinded population exists in this repository, which is why finding 11 is about asserting it, not about proving it false.
- A live end-to-end run under every permission mode. Anthropic's rules settle the mechanisms; I did not create skill deliverables with Claude Code or run a `dontAsk` headless workflow.

## Disagreements with the prior rounds

- **R4-Q2 / §R4.12 understates the restructure trade.** The extracted material is not only motivating history: it contains operative imperatives, stale versions of repaired rules, and the only detailed second-opinion procedure. Two required references are navigated exclusively below the cut they were meant to mitigate.
- **Round 4's `FIX LATER` “✔ executed” close reached only the two named operative sites.** The exact rejected phrase survives in a new reference, README, and HOW (finding 5), so the finding is not closed repository-wide.
- **Round 4's verifier-write fix is internally undone by its extracted procedure.** The new “trusted rather than confined” paragraph and the old “stops modifying” sentence coexist nine lines apart (finding 2).
- **Round 4's no-filesystem close is partial.** Qualifying invariants and adding `continue` did not remove §10's unconditional cover-note/two-path/file-exists obligations (finding 8).
- **Round 4's same-family downgrade changed the wording, not the epistemic status.** The emitted text still makes the conceded-unmeasured likelihood claim (finding 11).
- **R4-Q1's accepted settings remedy has the correct tool name and an invalid rule composition.** `Edit(path)` is correct, but `deny Edit(**)` cannot be narrowed by later allow rules (finding 9).
- **§R4.14 draws the lesson one level too low.** Re-reading extraction output would catch some cases; repository-wide claim enumeration or a single authoritative rule would address the repeated one-site fixes whether text moved or not.
