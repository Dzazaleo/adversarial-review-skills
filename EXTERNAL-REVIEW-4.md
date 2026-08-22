# External Review 4 — audit of the round-3 fixes

Reviewer identity: OpenAI GPT-5 family, Codex; version/served model alias and reasoning-effort label are not exposed to this session.

Audit baseline: findings assessed against `fe9bbac..540c60a`; `HEAD` observed at `818214bda0154c9ccb0f08a67fdce0c94d88e7c3`.

## Coverage

Read the complete pinned diff and all seven in-scope files at the reviewed/current forms needed by the brief, including the full two skills and changed prompt template, all of `EXTERNAL-REVIEW-3.md`, `BACKLOG.md`, `calibration/README.md`, and round 3 plus its two post-closure corrections. Read both unchanged reference templates, README, the relevant HOW-IT-WORKS design sections, and the round-1/2 finding tables and closure/history entries needed to test ancestry. Verified the exact `7 files changed, 951 insertions(+), 19 deletions(-)` range; parsed both frontmatters; ran collision, blindness, vocabulary, provenance, and placeholder searches; ran the two-fixture suite in a clean `/tmp` archive (`8 passed in 0.01s`); reproduced the dirty-tree digests and a clean before/after digest; and measured rendered skill prefixes with Claude Code 2.1.239's native token accounting. Checked current official Claude Code documentation for skill permissions, compaction, tools, and subagents. I did not execute either skill end to end or run model-population experiments; those gaps are itemized below. Repository state at close: only this report plus the two pre-existing untracked `__pycache__/` directories.

## Findings, ranked

Strict final order by cost of leaving each unfixed (blast radius × likelihood of trigger):

1. **`Write` remains an unbounded, prompt-free grant** — **high**; a normal invocation of either publicly installed skill can write any path without the boundary's promised stop.
2. **The supposedly enforced read-only verifier can still write through `Bash`** — **high**; the rare trigger sits exactly on serious self-authored refutations, where target mutation can manufacture a false rejection.
3. **Round 3's findings were not independent “by construction”** — **high**; it already fired and materially overstates the central evidentiary value assigned to this entire patch set.
4. **The blindness fix changed one site and left the governing rule false** — **medium**; every qualifying high-impact refutation encounters contradictory evidence requirements and a disclosure the template does not preserve.
5. **`FIX LATER`'s ordering rule is impossible under the mandatory sequence** — **medium**; every future deferral must violate one of two invariants, making a routine disposition structurally nonconforming.
6. **The collision guard still leaves the report artifact available to overwrite** — **medium**; a routine second round can destroy the primary evidence that all later adjudication depends on.
7. **The residual-doubt fix still contradicts the advertised fresh-machine workflow** — **medium**; the recommended hand-off path commonly loses the only copy of an input used to score independence.
8. **The no-filesystem route is contradicted by the surviving invariants and omits continuation** — **medium**; a supported browser reviewer can yield a truncated or mechanically impossible delivery.
9. **The hoisted residual-doubt invariant contradicts the full method** — **medium**; compaction can make the surviving rule suppress precisely the sharp claims the review needs.
10. **The digest defect is broader and less reproducible than `R3-F12` records** — **medium**; valid calibration state already changes across clean machines and will recur under each new artifact family.
11. **The compaction verification used the wrong tokenizer and wrong cut bands** — **medium**; the safety blocks survive, but every maintainer is given a materially false map of what else survives and a false verification record.
12. **The three independence branches have no human or mixed-authorship case** — **medium**; ordinary supported targets force a false sentence or an invented fourth branch.
13. **Appending `R3-F12` made the round's CLOSED status false** — **medium**; the durable ledger gives mutually exclusive answers about whether obligations remain.
14. **The ledger inflates ten defect claims into eleven findings** — **low**; metrics and count integrity drift, but no real defect was dropped.

### Finding detail — `Write` remains an unbounded, prompt-free grant

- **Impact:** high.
- **Location:** `skills/adversarial-review-prompt/SKILL.md:5-9`; `skills/review-adjudication/SKILL.md:5-9`; `skills/review-adjudication/SKILL.md:32-35`; `REVIEW-ADJUDICATION.md:2261-2273`, especially Q1(b)/(c).
- **Mechanism:** Both skills still put bare `Write` in `allowed-tools`. Current Claude Code documentation says this pre-approves that tool for the invoking turn, does not restrict it to named paths, and applies even to a project skill in an untrusted workspace. The prose boundaries therefore remain advisory over a grant capable of creating or overwriting any writable path. The ledger's option (c) would deny `Edit`/`NotebookEdit`, but bare `Write` would remain, so its statement that option (c) makes the brief-and-cover-only envelope “enforced” is false. Denying `Write` as well would also deny the intended deliverable; path-aware enforcement needs a hook or external permission policy.
- **Trigger:** A skill is invoked with all required arguments in a repository containing adversarial instructions in a report/source file, or the model simply chooses a wrong output path during the invoking turn. `Write` does not prompt before that path is written.
- **Consequence:** The `R3-F1` change closes the unrestricted-`Bash` edge but not the finding's broader prose-over-permission mechanism. A publicly installed skill can still overwrite code, plans, an existing report, or files outside the stated envelope without a permission stop, contrary to contract items 1 and 4.
- **Status:** **CONFIRMED.** YAML parsing and direct inspection returned `Read, Write, Grep, Glob` for both files. The current primary source says `allowed-tools` grants prompt-free use for the turn and “does not restrict which tools are available”; it separately says `disallowed-tools` removes whole tools, not paths: [Claude Code skills documentation](https://code.claude.com/docs/en/slash-commands#pre-approve-tools-for-a-skill). The current permissions documentation identifies `PreToolUse` hooks as the path/argument-aware mechanism: [Claude Code permissions documentation](https://code.claude.com/docs/en/permissions#hooks-and-permissions).

### Finding detail — The supposedly enforced read-only verifier can still write through `Bash`

- **Impact:** high.
- **Location:** `skills/review-adjudication/SKILL.md:449-465`; round-2 row `F4` at `REVIEW-ADJUDICATION.md:1468`.
- **Mechanism:** The round-2 fix calls `tools: Read, Bash, Glob, Grep` an allowlist that enforces non-modification because it omits `Write`, `Edit`, and `NotebookEdit`. `Bash` can itself create, replace, or delete files. A subagent `tools` list restricts which tools exist; it is not a command-level Bash sandbox, and the subagent's calls still run under the session's permission rules. The adjacent prose instruction not to run writing commands is therefore the same advisory boundary the earlier finding rejected.
- **Trigger:** The mandatory second opinion for a high/critical refutation uses the prescribed agent type in a parent session where a Bash write is already allowed, approved, classified as permissible in auto mode, or permissions are bypassed. The verifier uses redirection, `sed -i`, a formatter/test runner with writes, or any other mutating shell command.
- **Consequence:** The verifier can alter the target while establishing the evidence used to refute a serious finding. The resulting ledger can record a false `REFUTED` against post-mutation evidence, reopening the exact target-modification failure round 2 `F4` was marked as having closed.
- **Status:** **THEORETICAL.** I did not spend a model/subagent run to make it mutate a fixture. The mechanism is explicit in the tool set and current primary documentation: `Bash` executes shell commands, and subagent tool calls remain subject to inherited permission rules rather than acquiring filesystem confinement from the `tools` list ([tools reference](https://code.claude.com/docs/en/tools-reference), [subagent permissions](https://code.claude.com/docs/en/sub-agents#permission-modes)). A harmless `/tmp` subagent mutation would settle the behavioral half; the capability defect does not depend on the model choosing it in this run.

### Finding detail — `FIX LATER`'s ordering rule is impossible under the skill's own mandatory sequence

- **Impact:** medium.
- **Location:** `skills/review-adjudication/SKILL.md:42-44`, `:209-216`, `:239-263`, `:498-500`; `REVIEW-ADJUDICATION.md:2194`.
- **Mechanism:** Step 2 mandates writing the ledger skeleton before adjudicating any finding. The `FIX LATER` rule later mandates creating the backlog artifact before the ledger is written. At skeleton time no disposition has been chosen; once adjudication selects `FIX LATER`, the ledger already exists. The two orders cannot both hold. The recorded `R3-F6` “slip” was therefore not merely a missed practical rule; it was the inevitable execution of the earlier mandatory step.
- **Trigger:** Any report contains a real finding that is classified `FIX LATER` only after its row and claim card have been enumerated as required.
- **Consequence:** Every conforming adjudicator must violate one invariant or the other, so future ledgers can repeatedly label a structurally forced sequence as operator error. The rule provides no reliable guard against dropped deferrals and makes closure depend on an impossible history, violating contract items 3 and 5.
- **Status:** **THEORETICAL.** The contradiction is documentary and the round-3 ledger is a worked instance; no executable skill harness exists (known `B-3`). The deterministic repair is to require the artifact before the row receives a `FIX LATER` disposition or before the completed ledger is handed off—not before the ledger file/skeleton exists.

### Finding detail — The hoisted residual-doubt invariant contradicts the full method

- **Impact:** medium.
- **Location:** `skills/adversarial-review-prompt/SKILL.md:38-40`, `:300-310`, `:420-457`, `:479-486`.
- **Mechanism:** Invariant 5 says residual doubts “stay out of the brief” without qualification. The full rule says the normal case is that a doubt is also a load-bearing claim's pointed sub-question, orders the author to keep that claim sharp, and says the harm is not presence in the brief but later mis-scoring the prompted answer as independent corroboration. The invariant therefore summarizes the opposite policy at the exact location intended to survive when the nuanced rule disappears.
- **Trigger:** Auto-compaction leaves only the first 5,000 tokens while the author is mining claims and notices that one of its private doubts is also the strongest claim sub-question.
- **Consequence:** Following the surviving invariant removes or blunts the load-bearing claim, reducing the directed review's defect-finding power; following the full rule violates the surviving absolute. This is contract item 3's forbidden invariant drift and a direct regression introduced by the compaction fix.
- **Status:** **THEORETICAL.** The text is irreconcilable as written; an observed post-compaction authoring run would measure which branch Claude follows, not remove the contradiction.

### Finding detail — The compaction verification used the wrong tokenizer and materially wrong cut bands

- **Impact:** medium.
- **Location:** `skills/adversarial-review-prompt/SKILL.md:23-26`; `skills/review-adjudication/SKILL.md:27-30`; `REVIEW-ADJUDICATION.md:2459`, `:2464-2471`.
- **Mechanism:** The ledger declares cut bands of lines 288–322 and 265–302 from a word-count heuristic. Product-native Claude token accounting places 5,000 rendered skill tokens inside prompt-skill line 227 and adjudication line 205 (last complete lines below the cap: 226 and 204). The invariant blocks still survive, so the narrow hoist succeeds, but the ledger's verification and both skills' “roughly line 280/270” warnings are false by 54–97 lines. The files also grew from 11,030 to 11,843 rendered tokens and 12,707 to 14,129: the fraction discarded after a 5,000-token cap rose from 54.7% to 57.8% and from 60.7% to 64.6%, respectively.
- **Trigger:** Either skill is invoked and the conversation auto-compacts without a later re-invocation.
- **Consequence:** Operators and future maintainers are told substantially more of each full rule remains than actually does, and the execution ledger records a tokenizer-free estimate as a recomputed pass. In adjudication, everything from the claim-card enumeration onward is in the truncated tail; in prompt authoring, the cut arrives during the prior-review inventory rather than near the reported operating-envelope boundary. This violates contract item 5 even though the invariant blocks themselves remain above the cap.
- **Status:** **CONFIRMED.** I used Claude Code 2.1.239 with tools disabled and a system instruction that returns a fixed 13-token output, streaming progressively longer rendered prefixes (frontmatter removed, base-directory prefix present, `$ARGUMENTS` expanded empty). Prompt lines 224/225/226/227 measured 4,985/4,996/4,996/5,023 tokens; adjudication lines 204/205 measured 4,960/5,002. Full rendered counts before/current were 11,030/11,843 and 12,707/14,129. The documented cap and start-preserving behavior are current primary-source facts ([skills lifecycle](https://code.claude.com/docs/en/slash-commands#skill-content-lifecycle), [context-window documentation](https://code.claude.com/docs/en/context-window#what-survives-compaction)).

### Finding detail — The blindness fix changed one site and left the governing rule false

- **Impact:** medium.
- **Location:** `skills/review-adjudication/SKILL.md:269-276`, `:439-475`; `skills/review-adjudication/references/ledger-template.md:31-33`; `HOW-IT-WORKS.md:479-485`.
- **Mechanism:** The qualification at lines 269–276 says the verifier is merely not handed the report and can read it. The mandatory escalation still says the second opinion “never saw the report”; the public design explanation says it “has never seen the report at all.” The same skill then says never to call such a check blind. The ledger template's `Reviewer isolation` field concerns the external reviewer and earlier artifacts, not the escalation verifier, and no verifier-exposure field appears beside the verdict row. Finally, a “sanitized copy” is named as real blindness without instructions that confine `Read`/`Bash` to it; changing a working directory removes adjacent discovery but is not an access boundary.
- **Trigger:** An adjudicator is about to refute a reviewer-rated high/critical finding in its own work and follows the escalation bullet or public explanation rather than the earlier qualification; it spawns in the project or in an unconstrained scratch copy.
- **Consequence:** It can either misrecord an exposed verifier as blind or treat the owner's permitted unisolated check as nonconforming and fall back to `COULD NOT DETERMINE`. Because the template does not solicit the exposure fact, even a correctly performed weaker check can lose its qualification in the durable ledger. Contract items 1, 3, and 5 remain open.
- **Status:** **THEORETICAL.** Repository-wide `rg -ni 'blind|never saw|not handed|sanitized'` produced the contradictory sites above. Current Claude Code docs confirm a subagent starts in the parent working directory and that a tool list controls tools, not which readable paths those tools can address ([subagents documentation](https://code.claude.com/docs/en/sub-agents#write-subagent-files)). An empirical read attempt is already deferred as `R3-CNV-1`; it would measure behavior, while the textual contradiction and missing template field exist regardless.

### Finding detail — The residual-doubt fix still contradicts the advertised fresh-machine workflow

- **Impact:** medium.
- **Location:** `skills/review-adjudication/SKILL.md:145-154`; `README.md:149-155`, `:162-172`; `skills/review-adjudication/references/ledger-template.md:14-46`.
- **Mechanism:** The new input does not make the doubts durable; it asks the operator to retain and paste a chat hand-off. The README still promises that “everything it writes stands on its own,” “nothing later depends on keeping this session open,” and adjudication can resume days later on another machine from “the report and the files on disk.” Those statements are now demonstrably false. If the operator lacks the chat, the fallback conservatively withholds corroboration credit, but the template has no header field requiring the absence to be recorded, so even that disclosure is easy to omit from the durable artifact.
- **Trigger:** The authoring session is closed and its chat is unavailable when a fresh adjudication begins later or on another machine—the exact workflow README step 5 recommends.
- **Consequence:** The entire per-doubt leak audit is skipped, and findings that actually echo the author's doubts cannot be distinguished from independently reached ones. The fallback avoids false corroboration only if followed and durably recorded; it does not close the durable-source finding the ledger marks executed.
- **Status:** **THEORETICAL.** The dependency and contradiction are direct text. This round itself cannot execute loss of a historical chat without manufacturing external state; a real hand-off-loss run would confirm prevalence, not the missing durable source.

### Finding detail — The no-filesystem route is contradicted by the new surviving invariants and omits the operator continuation step

- **Impact:** medium.
- **Location:** `skills/adversarial-review-prompt/SKILL.md:17-19`, `:36-37`, `:134-147`, `:369-418`, `:462-493`; `skills/adversarial-review-prompt/references/prompt-template.md:360-387`.
- **Mechanism:** The objective and new invariant 4 say the deliverable is two files and the reviewer always creates the report file. The supported browser-chat route later says no cover note is emitted and the reviewer returns the report in chat for the operator to save. After compaction, the absolute file invariant survives while the exception does not. Separately, the template now says the hand-off must warn the operator to send one word to continue, but §10's exhaustive hand-off checklist omits that item; the no-filesystem branch in §1 mentions attachment and saving, not continuation.
- **Trigger:** The named reviewer is a browser-only chat, and the authoring session compacts before or while it prepares the hand-off, or it follows §10 as the authoritative checklist.
- **Consequence:** The skill can emit mutually incompatible delivery mechanics or omit the user action needed to resume a length-limited report. A truncated chat report can then be saved as complete—the exact `R3-F9` consequence—so the fix is not carried through the route it was intended to repair.
- **Status:** **THEORETICAL.** The conflict is documentary. A browser review forced across its output limit would settle behavioral incidence; no such external run was necessary to establish the missing checklist item.

### Finding detail — The collision guard still leaves the report artifact available to overwrite

- **Impact:** medium.
- **Location:** `skills/adversarial-review-prompt/SKILL.md:276-289`, `:320-330`, `:407-417`; `skills/adversarial-review-prompt/references/cover-note-template.md:86-91`.
- **Mechanism:** The new mandatory check and next-free-name algorithm cover only the brief and cover note. The report path is a separately generated path, and nothing says to check whether it already exists or forces a `-2` brief to name a `-2` report. The cover-note reference has helpful variants for several reviewers and delta reviews, but the latter merely says to choose append versus new; it neither checks collision nor binds the report suffix to the guarded brief suffix.
- **Trigger:** A later round over the same target finds the original brief and creates `...PROMPT-2.md`, but emits the default unsuffixed `NN-EXTERNAL-REVIEW.md` report destination; the external reviewer obeys and writes it.
- **Consequence:** The new review destroys the prior report while preserving the brief that was meant to protect its evidentiary history. The adjudication ledger's append-only rule cannot reconstruct the lost source, so `R3-F7` closes two artifacts while leaving the third artifact in the same evidence chain exposed.
- **Status:** **THEORETICAL.** The generated-path algorithm is prose and there is no validator (`B-3`); an end-to-end second-round generation would establish how often Claude notices the reference variant on its own.

### Finding detail — The three independence branches have no human or mixed-authorship case

- **Impact:** medium.
- **Location:** `skills/adversarial-review-prompt/SKILL.md:75-109`; `skills/adversarial-review-prompt/references/prompt-template.md:26-30`, `:54-73`.
- **Mechanism:** The template correctly tells the author to state human/inherited/third-party provenance, then requires one of three branches whose inputs all presume an `author family`: known-different model family, same model family, or unknown reviewer lineage relative to a model author. No step collects the work's author family, and there is no independence wording for human-authored or mixed human/multi-model work. The prompt skill is advertised for arbitrary code/plans, not only work authored by one known model.
- **Trigger:** A human-written repository, a mixed human/AI target, or a target written by multiple model families is handed to a known reviewer.
- **Consequence:** The author must either emit a false single-family sentence, misuse “unknown lineage” (the reviewer may be known; the author side is what is mixed), or invent a fourth branch despite an invariant requiring one of three. `R3-F5`'s unconditional architecture claim survives in a new form for supported provenance states the fix did not model.
- **Status:** **THEORETICAL.** A repository-wide provenance search found human edits only in the template warning and `author family` only in the known-different branch; no collection or mixed-provenance branch exists.

### Finding detail — Round 3's findings were not independent “by construction”

- **Impact:** high.
- **Location:** `REVIEW-ADJUDICATION.md:1818-1824`, `:2201-2216`; `EXTERNAL-REVIEW-3.md:7`, `:28-35`, `:107`.
- **Mechanism:** The absence of a bespoke brief rules out brief echoes; it does not establish that “no document primed” the reviewer. The reviewer was handed the repository, whose accumulated reports, backlog, and adjudication ledger were readable. The report proves it used that history: finding 1 explicitly says “Reopen the earlier ‘unbounded Write/Edit’ finding,” and its corpus-limitation bullet says the limitation was “already captured ... in `BACKLOG.md`.” At least those items were reached through prior artifacts, not independently. The round-3 header also omits the template's required reviewer-isolation line despite claiming a whole-repository review.
- **Trigger:** An unscoped reviewer reads the repository history while forming findings, as this reviewer demonstrably did.
- **Consequence:** Agreement with prior work is credited as independent corroboration and §R3.4 calls all eleven findings the round's “strongest evidentiary fact.” Downstream readers therefore overweight the report and the method records a claim directly disproved by its source report, violating contract item 5.
- **Status:** **CONFIRMED.** `rg -n 'Reopen the earlier|BACKLOG.md|independent by construction|Reports found' EXTERNAL-REVIEW-3.md REVIEW-ADJUDICATION.md` located both explicit history-derived report items and the universal independence claim. The operator's generic subject description did not name the individual defects; the readable repository history did.

### Finding detail — The ledger inflates ten defect claims into eleven “findings”

- **Impact:** low.
- **Location:** `EXTERNAL-REVIEW-3.md:95-107`; `REVIEW-ADJUDICATION.md:1867-1875`, `:2199`.
- **Mechanism:** Five numbered findings plus the first five “Other worthwhile improvements” bullets are ten defect/improvement claims. The sixth bullet says the public-corpus limitation is already captured well and should remain prominent; it identifies no missing behavior and asks for no change. The ledger itself rules `R3-F11` “not a defect” and `NO ACTION`, yet counts it among “Findings in: 11” after asserting all six bullets state defects. That assertion contradicts both the report and its own row.
- **Trigger:** Any later audit or metric uses the round header's findings-in count, or §R3.4's eleven-independent-findings claim, as evidence of reviewer yield.
- **Consequence:** Reviewer productivity and independence are overstated by one, and count-in/count-out is made to look exact by redefining an endorsement as a finding. No actual defect was dropped, so the direct operational cost is low, but the ledger is not an accurate record under contract item 5.
- **Status:** **CONFIRMED.** The source report contains five numbered items and six bullets; direct inspection shows the last bullet is an endorsement, and the adjudication row calls it “not a defect.”

### Finding detail — Appending `R3-F12` made the round's CLOSED status false

- **Impact:** medium.
- **Location:** `skills/review-adjudication/SKILL.md:155-164`; `REVIEW-ADJUDICATION.md:2386-2410`, `:2540-2597`.
- **Mechanism:** The skill defines closure to require no unresolved `PENDING OWNER`. After §R3.12 marked round 3 closed, §R3.16 appended a new numbered round-3 finding with disposition `PENDING OWNER`. Appending rather than editing preserves the old text, but the ledger now simultaneously says the round is closed and contains an unresolved closure-blocking obligation. A correction may supersede a ruling; it cannot leave the superseded status presented as the current round status without a new status record.
- **Trigger:** The next brief or adjudication reads the explicit “Round 3 status: CLOSED” heading to decide whether to append a new round and what obligations remain.
- **Consequence:** `R3-F12` can be skipped as though it belonged to immutable history, or a later session can append round 4 while the previous round violates its own entry condition. The append-only discipline survives mechanically, but the closure definition and durable record do not, violating contract item 5.
- **Status:** **CONFIRMED.** Direct line inspection shows the closed marker precedes the new `PENDING OWNER` row; the skill's closure predicate is explicit and needs no behavioral assumption.

### Finding detail — The digest defect is broader and less reproducible than `R3-F12` records

- **Impact:** medium.
- **Location:** `calibration/record-template.md:14`, `:24-29`; `REVIEW-ADJUDICATION.md:2540-2597`; `.gitignore:1-2`.
- **Mechanism:** Hashing every file under the case directories makes any runtime artifact part of the instrument. `__pycache__` is one instance; the proposed name-by-name prune leaves `.pytest_cache`, coverage files, editor state, OS metadata other than `.DS_Store`, and future language/build caches as recurring instances. The exact post-test digest is also environment/checkout dependent: default `.pyc` files encode source timestamp and size, while pytest writes rewritten bytecode caches. Therefore the ledger's observed `775e1cc8c43f → 9fb019996546` is not a portable reproduction of the trigger.
- **Trigger:** Run the prescribed two suites in a fresh checkout whose source mtimes differ, under a different Python/pytest version, or run another permitted tool that writes an unpruned artifact under a case.
- **Consequence:** Valid calibration records expire differently across machines despite identical instrument source. Pruning one cache directory fixes today's tree and guarantees another false expiry when a new artifact name appears; the digest remains a machine-state hash rather than an instrument manifest.
- **Status:** **CONFIRMED.** In a clean `git archive 540c60a` under `/tmp`, the prescribed digest was `775e1cc8c43f`; the suite returned `8 passed in 0.01s`; the same digest command then returned `ce0a9e5f3046`, not the ledger's `9fb019996546`. Excluding cache directories restored `775e1cc8c43f`. The current dirty repository does reproduce `9fb019996546`, proving that number belongs to its existing cache bytes. `git ls-files` over the published instrument returns stable `775e1cc8c43f` at negligible runtime cost, but would omit intentionally untracked private replacement cases; the general fix is an explicit instrument manifest (one maintained path list, usable for tracked or private corpora), not another filename predicate. Python's primary documentation confirms timestamp-mode `.pyc` embeds source timestamp and size ([`py_compile`](https://docs.python.org/3/library/py_compile.html)); pytest documents that assertion rewriting writes `.pyc` caches ([assertion rewriting](https://docs.pytest.org/en/stable/how-to/assert.html#assertion-introspection-details)).

## The unseeded pass

I cannot literally unread the 23-claim list, so I did the defensible substitute: after the directed pass I reopened the two skill diffs and their full operational text without walking the claim numbers, traced each surviving invariant into its later rule, and searched every claimed tool boundary for alternate capabilities. That pass independently produced three issues not stated by a seeded sub-question:

1. The “read-only” subagent still has `Bash`, so the round-2 write-boundary fix does not enforce non-modification.
2. The new prompt invariant says doubts stay out of the brief while the full method says their overlap with pointed claim questions is normal and must remain sharp.
3. The new prompt invariant says the reviewer always creates a report file, contradicting the supported browser-only route before the later continuation omission is even reached.

It also re-reached the `FIX LATER` sequencing contradiction, but claim 8 had pointed directly at the adjacent self-violation, so I do not count that as unseeded discovery.

## Claims examined and upheld

1. **REFUTED** — both grants are exactly `Read, Write, Grep, Glob`, but bare `Write` preserves the original prose-over-broad-grant mechanism; the fix closes unrestricted `Bash`, not the whole finding.
2. **REFUTED** — `disallowed-tools` is real and was deliberately declined, but there is still no mechanism behind the absolute path boundary; denying only Edit/NotebookEdit leaves arbitrary `Write`, while denying `Write` also removes the deliverable.
3. **CONFIRMED** — `Agent` was removed beyond the literal owner choice and the ledger flags it. The feared permission prompt does not follow on current Claude Code: `Agent` is listed as not requiring permission and launching a subagent does not itself prompt ([tools reference](https://code.claude.com/docs/en/tools-reference)).
4. **COULD NOT DETERMINE** — removal does not remove Bash capability, and current manual mode auto-runs a built-in subset of read-only shell commands while auto mode classifies others; whether added friction causes fewer checks needs matched adjudication runs, not static inference.
5. **REFUTED** — the invariant blocks are above the cap, but the asserted/recomputed locations are not: native counts cross at prompt line 227 and adjudication line 205, not the recorded 288–322/265–302 bands.
6. **CONFIRMED** — line and native-token counts both grew; the discarded token fractions rose 54.7%→57.8% and 60.7%→64.6%. The narrow invariant survival improves, while the tail exposure measurably regresses.
7. **REFUTED** — prompt invariant 5 contradicts the full doubt-overlap rule; adjudication invariant 4 conflicts with skeleton-first ordering; adjudication invariant 5 says “not handed” while the governing escalation says “never saw.”
8. **CONFIRMED** — the round-3 ledger did violate invariant 4, and the complete artifact bounded this instance's harm. The deeper cause is not impractical operator discipline but mutually impossible ordering instructions.
9. **REFUTED** — the named input exists, but it relocates the dependency to retained chat and leaves README's “nothing later depends”/fresh-machine promise false.
10. **REFUTED** — the fallback is epistemically conservative but cheap and not template-gated; the ledger skeleton has no required field proving the doubts were requested or unavailable.
11. **REFUTED** — `never saw the report` remains in the mandatory escalation and “never seen ... at all” remains in `HOW-IT-WORKS.md`; the fix reached only one site.
12. **REFUTED** — the template's `Reviewer isolation` line describes the external reviewer, not the escalation verifier, and the verdict-row skeleton has no verifier-exposure prompt.
13. **REFUTED** — a sanitized copy is enough to remove adjacent discovery, not to enforce read blindness; no construction or filesystem-confinement procedure is given.
14. **CONFIRMED** — the placeholder contains guillemets, and the mandatory post-save `«|»` grep catches it if it survives substitution. Direct `rg -nF` found it at template line 39.
15. **REFUTED** — the branches omit human, mixed human/AI, and multiple-model authorship, and no step establishes an author-family input.
16. **COULD NOT DETERMINE** — the same-family sentence's “most likely” behavioral claim has no measurement or primary source here; comparative blinded review runs would settle it.
17. **REFUTED** — brief and cover collisions are guarded, but the report path is not obligatorily checked or suffix-bound; the ledger remains append-only by instruction rather than enforcement.
18. **CONFIRMED** — “check the path before writing” plus `Glob` is deterministic and actionable in a single-agent workflow. It is still prose, but unlike a security boundary its purpose is to direct an operation the skill itself controls.
19. **REFUTED** — the template tells the author to warn the operator about one-word continuation, but the skill's exhaustive §10 hand-off list omits it and the surviving file-delivery invariant contradicts the browser route.
20. **CONFIRMED** — the active verdict vocabulary uses `COULD NOT DETERMINE`; remaining “could not verify” text is a section heading or historical mention, not a competing verdict. `BACKLOG.md` B-3 has explicit Location, Mechanism, and Consequence fields and cleanly assigns corpus drift to B-1 and skill validation to B-3.
21. **REFUTED** — no original numbered verdict or disposition depended on uncalibrated status, so that narrow assertion holds; however §R3.16 then added an unresolved `PENDING OWNER` finding to a round still headed CLOSED, contradicting the closure definition.
22. **REFUTED** — ten defect claims plus one endorsement do not make eleven findings, and at least two items explicitly drew on readable prior artifacts, so universal independence “by construction” is false.
23. **REFUTED** — the dirty tree reproduces both recorded digests, but a clean before/after run produces `775e1cc8c43f → ce0a9e5f3046`; this is the same artifact-inclusion root cause round-2 F1's `.DS_Store` instance exposed, and another name prune is not a general fix.

## Could not verify

- I did not run an empirical before/after population of adjudications to measure whether removing bare `Bash` reduces verification depth (claim 4).
- I did not spawn a Claude subagent and observe report reading (`R3-CNV-1`) or target mutation through retained `Bash`; those behavioral demonstrations would not change the documented capabilities or textual contradictions.
- Native token measurements used Claude Code 2.1.239 served by `claude-opus-5[1m]`. The current product documents a 5,000-token cap but does not promise identical token boundaries across every present/future Claude model; the recorded boundaries are exact for the measured current configuration.
- I did not run comparative same-family/different-family reviewer populations, so claim 16 remains unsupported rather than disproved.
- I did not execute either skill end to end against synthetic multi-round/browser/mixed-authorship scenarios. The known absence of a skill validator is `B-3` and is not re-reported; the concrete contradictions and missing paths above are the patch defects it would need to catch.

## Disagreements with the prior rounds

- **Round 2 `F4` (`REVIEW-ADJUDICATION.md:1468`):** the finding was correctly confirmed, but its executed fix was incomplete. A subagent allowlist retaining `Bash` is not an enforced no-write boundary.
- **Round 2 `F1` (`REVIEW-ADJUDICATION.md:1465`):** `R3-F12` is a new artifact name but not a new root cause. Round 2 explicitly identified inclusion of unauthored runtime files as “the same failure in the other direction”; pruning only `.DS_Store` should have been recorded as a narrow/incomplete repair.
- **Round 3 `R3-F1`:** dropping unrestricted `Bash` is a real reduction, but the row's executed/closed framing overstates closure while bare `Write` remains unrestricted and option (c) was incorrectly described as path enforcement.
- **Round 3 `R3-F3`:** asking for retained chat is a fallback, not closure of the durable-source finding; README still promises the opposite workflow.
- **Round 3 `R3-F4`:** the qualification is correct at one site, but the unqualified mandatory rule, public explanation, template omission, and unconstrained “sanitized copy” remain.
- **Round 3 `R3-F7`:** the guard is complete for brief and cover note only; the report—the source artifact the ledger adjudicates—remains collision-prone.
- **Round 3 `R3-F9`:** the reviewer-facing half is repaired, but the operator-facing hand-off checklist omits the newly required continuation action.
- **Round 3 `R3-P3`:** “all eleven findings independent by construction” is directly refuted by report text that reopens an earlier finding and credits `BACKLOG.md`.
