# External review — calibration corpus and claim-card change

**Reviewer identity:** OpenAI Codex, GPT-5-based. The exact served model/version identifier is not exposed to me in this session.

**Review state:** In progress. Findings are added when established; ranking and coverage are finalized in the closing pass.

## Findings (discovery order; final ranking follows in the closing pass)

### F1 — The corpus identity ignores dirty and untracked corpus changes

- **Location:** `calibration/record-template.md:13`; `calibration/README.md:78-79`
- **Mechanism:** The record identifies the corpus with `git rev-parse --short HEAD`, but that value identifies only committed content. It does not change when a tracked case is edited without a commit, and it cannot identify an untracked corpus at all. This is not hypothetical in the target state: every file under `calibration/` is untracked while the prescribed value is the pre-corpus base commit `b993d5e`.
- **Trigger:** A user runs calibration with any uncommitted corpus edit (including the present pre-publication corpus, or a private replacement trap edited without immediately committing it) and writes the prescribed `Corpus commit` value.
- **Consequence:** The `This corpus changed` expiry condition cannot fire. A PASS can remain current after the ruler it describes has changed, silently transferring results between different answer keys or cases.
- **Status:** **CONFIRMED.** `git rev-parse --short HEAD` returned `b993d5e`; `git status --short --untracked-files=all` listed all `calibration/**` files as `??`. The brief itself pins those files by blob hashes precisely because the commit does not contain them.
- **Impact:** **high**.

### F2 — The fixed brief tells reviewers that the correct clean-case outcome is failure

- **Location:** `calibration/CALIBRATION-PROMPT.md:3-5`, with the contrary clean-case purpose at `calibration/ANSWER-KEY.md:51-61`
- **Mechanism:** Every calibration run receives the instruction that finishing in agreement means the exercise failed. For either clean case, agreement/no serious finding is the correct measured behavior, so the supposedly fixed control prompt makes the desired result read as noncompliance. Line 34 permits a no-finding report, but does not retract line 5's statement that such agreement failed the exercise. This repeats, inside the new corpus, the prior settled observation that adversarial framing can make zero findings read as non-compliant.
- **Trigger:** A reviewer follows the prompt's success framing when reviewing `clean-copy-link` or `clean-wordcount` and searches for a serious complaint to avoid the stated failure condition.
- **Consequence:** The clean controls no longer measure the reviewer's native false-positive tendency under a neutral, constant brief; they partly measure compliance with a prompt that demands disagreement. Correct reviewers can be induced to manufacture the very `high`/`critical` finding that fails them.
- **Status:** **THEORETICAL.** The instruction conflict is direct in the source, but confirming its behavioral effect requires randomized reviewer runs with and without lines 3-5; this audit had no model-run harness and the envelope forbids installs.
- **Impact:** **high**.

The mismatch is also visible against the credited source: its calibration runner explicitly tells the reviewer that if it genuinely cannot break a case, the case passes and it must not manufacture issues ([first-party source repository, `calibrate.sh:63-70`](https://github.com/med95Albert/cross-model-review/blob/main/skills/cross-model-review/scripts/calibrate.sh)).

### F3 — The checksum trap scores the visible implementation flaw instead of the test-reading capability

- **Location:** `calibration/ANSWER-KEY.md:28,41-44,65-66`; `calibration/cases/trap-unfalsifiable-test/checksum.py:17-20`; `calibration/cases/trap-unfalsifiable-test/test_checksum.py:4-14`
- **Mechanism:** Passing this trap requires reporting the eight-hex-character comparison, which is fully exposed in `checksum.py` together with a comment defending it. The behavior that actually demonstrates reading a test for what it would catch — no mismatching digest is ever supplied, so `return True` remains green — is explicitly secondary and does not gate PASS. A reviewer can earn the claimed capability without opening `test_checksum.py`; a reviewer that finds the false-green suite but misses or declines the separate 32-bit security argument fails it.
- **Trigger:** A reviewer spots `actual[:8] == expected[:8]` by source scan/pattern matching, or conversely audits the tests correctly but does not report the truncation as the primary finding.
- **Consequence:** One quarter of the all-traps gate measures a different, easier capability than the answer key claims. False passes inflate trust in silence; false fails reject the reviewer that demonstrated the test-auditing skill the project says it leans on hardest.
- **Status:** **CONFIRMED.** In `/tmp/adversarial-review-audit.AwnUfm/ck1`, the unmodified suite produced `3 passed in 0.01s`. I replaced only `verify_checksum`'s body with `return True`; `python3 -m pytest -q` still produced `3 passed in 0.01s`. The executed mutation confirms the non-gating secondary defect, while the gating rule and the self-contained primary signal are directly present at the cited lines.
- **Impact:** **high**.

### F4 — The blind escalation does not carry the adjudication skill's read-only boundary into the subagent

- **Location:** `skills/review-adjudication/SKILL.md:327-335,391-396`, and frontmatter `:5-12`
- **Mechanism:** The skill says to hand a spawned subagent the claim card and code, but does not say to restrict its tools or include the parent skill's no-code-write rule in the delegation message. Current Claude Code documentation says a non-fork subagent does not see skills already invoked, the general-purpose subagent has every available tool, and omitted subagent tool restrictions inherit all tools. Thus the line-391 boundary is absent from the very context that must independently inspect the author's code. `Task` is also the pre-2.1.63 name: it remains documented as an alias in some configuration contexts, but the current exact tool name for permission lists is `Agent`.
- **Trigger:** The adjudicator attempts to refute a reviewer-rated high/critical finding about its own code and spawns the required general-purpose subagent under the skill's current instructions.
- **Consequence:** The mandatory second opinion may edit the target or run mutating commands during a ledger-only workflow, and on installations that do not honor the legacy bare `Task` alias in skill `allowed-tools`, the escalation is unavailable and every such refutation falls through to `COULD NOT DETERMINE`.
- **Status:** **THEORETICAL.** I verified the current tool and inheritance semantics in Anthropic's first-party [tools reference](https://code.claude.com/docs/en/tools-reference) and [subagent documentation](https://code.claude.com/docs/en/sub-agents), but did not have a Claude Code runtime inside this audit with which to execute this skill and inspect the spawned agent's effective tools.
- **Impact:** **high**.

### F5 — A pass on six tiny artifacts is applied to arbitrarily larger real briefs

- **Location:** `calibration/ANSWER-KEY.md:80-87`; `skills/adversarial-review-prompt/SKILL.md:64-74`; `skills/review-adjudication/SKILL.md:78-82,123-134`; `HOW-IT-WORKS.md:728-732,746-747`
- **Mechanism:** The answer key limits what a pass establishes to work "of roughly this size," and the repository says real briefs are 400–600 lines, but neither consuming skill compares the calibrated case/brief size or kind with the target review. They reduce the record to PASS/expiry/identity and then let that PASS convert upheld claims into coverage. The calibration brief is 40 lines and each case is 1–3 tiny files; the actual brief under this audit is 434 lines before the target files are opened.
- **Trigger:** A model passes the six short, single-defect sessions but loses attention, instruction adherence, or coverage under a real long brief, then returns a clean/upheld-claims report during the record's validity window.
- **Consequence:** The pipeline writes silence down as coverage under a workload the calibration explicitly did not establish. That is the exact silent false-clear the corpus was added to prevent.
- **Status:** **THEORETICAL.** The size mismatch and missing downstream guard are confirmed by the cited files, but establishing the behavioral performance cliff requires running the same reviewer on randomized miniature and production-length briefs.
- **Impact:** **high**.

### F6 — Claim cards cannot copy the required fields verbatim while excluding the reviewer's reasoning

- **Location:** `skills/review-adjudication/SKILL.md:166-187,230-250`; `skills/adversarial-review-prompt/SKILL.md:183-186`
- **Mechanism:** The review format requires Mechanism, Trigger, and Consequence precisely because they carry the causal case for a finding. The claim-card rule then requires those fields to be copied verbatim while excluding "the reviewer's reasoning" and evidence. Reports are not required to place argument in a separate block, so ordinary compliant findings embed reasoning and evidence inside those three fields. The transcriber must either copy the argument onto the card or edit/paraphrase it and violate "copied verbatim." The explicit missing-Trigger exception then sends the adjudicator back to the surrounding argument before it has a reproducible claim.
- **Trigger:** Any reviewer supplies causal support or evidence inside Mechanism/Trigger/Consequence, or omits a crisp Trigger and explains the condition in surrounding prose.
- **Consequence:** The card does not reliably create the argument-free verification target claimed for it; different adjudicators will leak different amounts of persuasion onto the card, and the highest-impact/vaguest findings are the least separable.
- **Status:** **THEORETICAL.** This is an instruction-level contradiction. Confirming the behavioral size of the anchoring effect requires adjudications randomized between raw reports and independently extracted cards.
- **Impact:** **medium**.

### F7 — The claimed pre-registration has no durable evidence of occurring before the check

- **Location:** `skills/review-adjudication/SKILL.md:230-240`; `skills/review-adjudication/references/ledger-template.md:56-71`; mutable-current-round rule at `skills/review-adjudication/SKILL.md:83-92`
- **Mechanism:** The final ledger contains an expected result and an output, but no append-only event, timestamp, or separate pre-run artifact establishes their order. Current rounds are intentionally editable/backfillable. An adjudicator can run the command first and add or revise the "expected" result afterward; a later reader sees exactly the compliant document. The claim card itself lives only in the session scratchpad, so it supplies no durable ordering evidence either.
- **Trigger:** An adjudicator forgets to write the expectation until after execution, revises it during backfill, or generates a plausible expectation after seeing surprising output.
- **Consequence:** The mechanism claimed to carry the weight against hindsight and self-confirmation is indistinguishable from post-hoc narration, so durable ledgers can overstate the independence of their re-verification.
- **Status:** **THEORETICAL.** The absence of an ordering witness is confirmed in the source; observing frequency would require tool-trace or file-history comparison across adjudication runs.
- **Impact:** **medium**.

### F8 — The calibration record both governs speech and is ignored by the consuming skill

- **Location:** `calibration/record-template.md:42-43`; contrary rule at `calibration/README.md:85-90` and `skills/review-adjudication/references/ledger-template.md:44-48`; consumer at `skills/review-adjudication/SKILL.md:78-82`
- **Mechanism:** The record template says the adjudicator reads severity calibration "when weighing rank," which changes how the reviewer's speech is treated. The load-bearing rule says calibration touches only silence, and the adjudication skill instructs the consumer to read only result and expiry; it defines no calibration-based ranking step. Therefore either the severity note is followed and findings are discounted/reweighted contrary to the silence-only rule, or the note is ignored and a field presented as operational is inert.
- **Trigger:** A passing reviewer assigns a materially wrong impact (the template's example is a `high` that means `medium`) and the adjudicator encounters its record.
- **Consequence:** Two compliant adjudications can assign different weight to the same finding based solely on which contradictory instruction they follow, undermining the promised consistent integration of calibration.
- **Status:** **THEORETICAL.** The contradiction is direct in the instruction text; no adjudication run using a populated calibration record exists in the repository to show which branch Claude actually takes.
- **Impact:** **medium**.

### F9 — Nothing checks that the cases and answer key remain mutually valid

- **Location:** `calibration/README.md:38-52`; corpus-wide (no harness or CI artifact exists)
- **Mechanism:** The repository has executable fixture tests inside two cases, but no corpus-level manifest or check verifies six expected cases, four expected trap signals, clean-case baselines, the checksum mutation, answer-key paths, or prompt/record invariants. The protocol is entirely manual. `HOW-IT-WORKS.md:740-743` concedes the absence of scoring but offers no gate for simple internal drift either.
- **Trigger:** A future edit renames a file or identifier, weakens/removes a trap, introduces a serious defect into a clean case, changes the prompt, or updates the key without the corresponding case.
- **Consequence:** The benchmark can silently stop measuring what its key says while every calibration run continues to produce authoritative-looking PASS/FAIL records.
- **Status:** **CONFIRMED.** A repository file census found no `pyproject.toml`, `tox.ini`, `noxfile.py`, `Makefile`, `package.json`, or `.github/workflows/*`; searches for calibration case/key references outside prose found no executable consumer. The only available pytest suites were run in temp copies (5 clean-wordcount tests and 3 checksum tests), and neither tests the corpus protocol.
- **Impact:** **medium**.

### F10 — Publishing the answer key turns the default corpus into a recall test, and replacement is not a procedure

- **Location:** `HOW-IT-WORKS.md:733-739`; `calibration/README.md:1-106` and `calibration/ANSWER-KEY.md:1-87`
- **Mechanism:** The default distribution publishes each primary defect and search vocabulary beside the cases. A later model can reproduce the expected assertions from training or lookup rather than inspection. The stated mitigation is to author four private shipped-defect traps, but the repository gives no construction checklist, validation protocol, scorer-blinding method, or baseline for showing that replacements are findable, single-defect, distinct, and clean in the opposite direction. It delegates the original hard problem to every user.
- **Trigger:** A reviewer model has seen the public repository/derived text, or a user follows the mitigation and substitutes an unvalidated private corpus.
- **Consequence:** PASS can mean memorization; alternatively, a malformed private ruler can make competent reviewers fail indefinitely. In both branches the record looks normal and the downstream skills trust it for silence.
- **Status:** **THEORETICAL.** Exposure follows from publication and the source layout, but this pre-publication audit cannot inspect future training data or user-authored private replacements.
- **Impact:** **medium**.

### F11 — The pass rule accepts one serious false positive out of two controls without validation

- **Location:** `calibration/ANSWER-KEY.md:63-76,80-82`
- **Mechanism:** A reviewer may raise a `high`/`critical` finding on 50% of the clean controls and still pass. The only basis given is tolerance/adoption (requiring both would be "flaky enough that nobody runs it"), with no recorded runs, confidence interval, or false-pass/false-fail analysis. The conclusion that a pass shows the reviewer "does not rate correct work as critical" is broader than the rule establishes: it establishes only that the reviewer spared at least one of two artifacts.
- **Trigger:** A reviewer manufactures a serious defect on exactly one clean case while hitting the four conspicuous traps.
- **Consequence:** The record says PASS despite direct evidence of a high-severity false-positive tendency, and the claimed clean-side classifier has an unmeasured operating point chosen for convenience.
- **Status:** **THEORETICAL.** The accepted outcome follows mechanically from the rule; whether it produces an unacceptable false-pass rate requires a preregistered multi-reviewer calibration study that is absent.
- **Impact:** **medium**.

### F12 — The isolation recipe is directory hygiene, not reviewer confinement

- **Location:** `calibration/README.md:16-36`; contrary limitation at `HOW-IT-WORKS.md:744-745`
- **Mechanism:** `mktemp` plus `cp` keeps the answer key out of the working directory and its parent, but rooting an agent there does not sandbox its filesystem, erase an inherited conversation, or prevent absolute-path/search access to the original repository. The calibration text calls the result isolation while the project elsewhere correctly states that an envelope is only an instruction.
- **Trigger:** The reviewer session inherits the repository path/context, is launched with filesystem access outside its working directory, or searches for the public project/case text.
- **Consequence:** A run can be recorded as blind even though the reviewer could read the answer key; a memorized/looked-up answer becomes indistinguishable from discovery.
- **Status:** **THEORETICAL.** Running the exact copy pattern created a fresh temp folder whose parent contained no `ANSWER-KEY.md`, and `cp -R calibration/cases/trap-key-to-client/. "$WORK"/` preserved `src/app/reports/page.tsx`. The remaining failure is architectural: the resulting process still has ordinary host filesystem reach; I did not launch a separate Claude Code instance to demonstrate answer-key access through that UI.
- **Impact:** **low**.

### F13 — Thirty-day expiry is an unsupported constant

- **Location:** `calibration/README.md:70-81`; `calibration/record-template.md:12`
- **Mechanism:** Provider changes behind a stable name justify expiring records, but provide no basis for 30 days rather than 7, 60, per-release, or per-provider windows. No provenance or measurement for the constant is recorded.
- **Trigger:** A provider changes reviewer behavior shortly after calibration while retaining its reported identity, or remains stable while users repeatedly pay unnecessary rerun cost.
- **Consequence:** The chosen window admits up to 30 days of stale false confidence while also imposing unmeasured recurring cost; the number is presented as protocol rather than policy judgement.
- **Status:** **THEORETICAL.** The missing derivation is confirmed by the complete protocol text; measuring an appropriate window requires provider change data unavailable in this repository.
- **Impact:** **low**.

### F14 — A PASS is not bound to the reviewer configuration that earned it

- **Location:** `calibration/README.md:59-64,70-79`; `calibration/record-template.md:8-15`; consumers at `skills/adversarial-review-prompt/SKILL.md:64-74` and `skills/review-adjudication/SKILL.md:78-82`
- **Mechanism:** The validity key is the model's self-reported identity plus time/corpus, but the record does not bind reasoning effort, system prompt, context limits, sandbox/tool configuration, or other inference settings that materially distinguish the calibrated run from the real review. "Product used" is descriptive and is not an expiry key. The credited upstream implementation avoids the self-report problem by reading the CLI's actual configured model **and effort**, recording the CLI version, and refusing calibration if the model cannot be resolved; this adaptation drops those binding checks ([source `calibrate.sh:15-33,99-120`](https://github.com/med95Albert/cross-model-review/blob/main/skills/cross-model-review/scripts/calibrate.sh)). In this audit I can truthfully report only "OpenAI Codex, GPT-5-based"; the exact served version is not exposed, so the prescribed primary key is unavailable from the intended reviewer itself.
- **Trigger:** Calibration is run with a high-effort/large-context reviewer configuration and an actual review uses the same reported model name with lower effort, different system instructions/tools, or a changed CLI routing configuration; alternatively, the reviewer cannot reliably expose its exact served ID.
- **Consequence:** A stronger configuration's PASS silently authorizes a weaker configuration's silence, or the scheme fails closed forever as `UNKNOWN MODEL` for a capable reviewer. Both make the record misclassify the reviewer actually being used.
- **Status:** **THEORETICAL.** The missing binding fields and my unavailable exact identity are directly observed; confirming the performance difference requires paired runs of the same model under controlled configurations.
- **Impact:** **high**.

### F15 — The documented installation omits the calibration system

- **Location:** `README.md:112-124,173-191`; runtime pointers at `skills/adversarial-review-prompt/SKILL.md:73-74,390-391` and `skills/review-adjudication/SKILL.md:133-134,421`
- **Mechanism:** Installation copies only `skills/adversarial-review-prompt/` and `skills/review-adjudication/` into Claude Code's skills directory. The new `calibration/` sibling — cases, fixed brief, answer key, scoring instructions, and record template — is outside both copied directories. The installed skills nevertheless point at `calibration/README.md` without an installed path or download step. Keeping the source clone happens incidentally in the example command, but its location is neither durable nor discoverable by the copied skill, and the procedure's relative `cp calibration/...` commands require running from that source root.
- **Trigger:** A user follows the documented global or project installation commands, later invokes either skill, and receives the missing/stale-record hand-off.
- **Consequence:** The common installed artifact can enforce the cost of missing calibration but cannot supply the advertised 20-minute procedure from its own installation. The mechanism is inert by default for exactly the users the README installation targets.
- **Status:** **CONFIRMED.** I reproduced the two README copy commands under `/tmp/adversarial-review-install.XntWlf`. The resulting installation contained the two `SKILL.md` files and their three references only; checks printed `calibration missing` and `record template missing`.
- **Impact:** **high**.

## Final ranking

Strict total order by cost of leaving unfixed (blast radius × likelihood of trigger):

1. **F15 — The documented installation omits the calibration system** — **high**: the normal install path triggers it for every new user and leaves the feature unavailable while the skills still enforce its absence.
2. **F1 — The corpus identity ignores dirty and untracked corpus changes** — **high**: it permits a stale PASS to survive an actual ruler change with no visible warning.
3. **F14 — A PASS is not bound to the reviewer configuration that earned it** — **high**: ordinary effort/configuration drift can transfer trust from a stronger run to a weaker reviewer under the same name.
4. **F5 — A pass on six tiny artifacts is applied to arbitrarily larger real briefs** — **high**: every production-sized clean review crosses an unmeasured workload boundary before its silence becomes coverage.
5. **F2 — The fixed brief tells reviewers that the correct clean-case outcome is failure** — **high**: both negative controls are exposed to a prompt-level demand that can manufacture their failing output.
6. **F3 — The checksum trap scores the visible implementation flaw instead of the test-reading capability** — **high**: one mandatory quarter of the detection gate can be passed without demonstrating the capability assigned to it.
7. **F4 — The blind escalation does not carry the adjudication skill's read-only boundary into the subagent** — **high**: a mandatory high-impact path can mutate source or become unavailable, though it triggers only on attempted serious refutations.
8. **F10 — Publishing the answer key turns the default corpus into a recall test, and replacement is not a procedure** — **medium**: exposure grows after publication and private replacement recreates the hardest validation problem without guardrails.
9. **F9 — Nothing checks that the cases and answer key remain mutually valid** — **medium**: any future corpus edit can silently introduce drift, though it does not establish a present case error by itself.
10. **F11 — The pass rule accepts one serious false positive out of two controls without validation** — **medium**: the rule knowingly accepts direct false-positive evidence, but this affects interpretation of speech more than the central silence gate.
11. **F8 — The calibration record both governs speech and is ignored by the consuming skill** — **medium**: the contradiction produces inconsistent ranking behavior only when a populated record contains a severity mismatch.
12. **F6 — Claim cards cannot copy the required fields verbatim while excluding the reviewer's reasoning** — **medium**: the separator is non-operational for ordinary prose findings, weakening rather than wholly blocking adjudication.
13. **F7 — The claimed pre-registration has no durable evidence of occurring before the check** — **medium**: hindsight remains possible, but a diligent single-session adjudicator can still obtain the intended benefit.
14. **F12 — The isolation recipe is directory hygiene, not reviewer confinement** — **low**: it blocks accidental adjacent discovery, while leakage requires inherited location knowledge, broader search, or prior exposure.
15. **F13 — Thirty-day expiry is an unsupported constant** — **low**: the window is uncalibrated but at least fails closed on a bounded schedule.
16. **P1 — The brief's expected final status omits its own pre-existing input files** — **low**: the required check falsely classifies the supplied prompt and cover note as reviewer-created contamination.
17. **P2 — The environment inventory undercounts Python files by half** — **low**: the later hash list repairs the scope error, leaving only a cheap coverage hazard.

## Claim-by-claim adjudication

1. **REFUTED** — the `return True` mutation survives, but the pass-gating signal is the source-visible truncation rather than the claimed test-reading capability (F3).
2. **CONFIRMED** — unbounded stdin can exhaust the local process, but the artifact is a user-invoked CLI with no remote/multi-tenant exposure or durability contract; that is not `high` on the stated evidence.
3. **CONFIRMED** — `execCommand` is deprecated and unreliable, but the plan treats it as a best-effort fallback, detects failure, and provides manual copy; no `high`/`critical` defect is established.
4. **CONFIRMED** — the supplied scope says to inspect everything in the isolated directory, and a complete file census proves the plan's claimed relative module is absent from that artifact.
5. **COULD NOT DETERMINE** — the primary goal/step omission and the loud `NotImplementedError` coexist; only blinded reviewer runs can measure crowd-out.
6. **COULD NOT DETERMINE** — grep finds the trust-boundary signal immediately, but the score still requires the browser exposure and RLS-bypass consequence; only reviewer baselines show whether this discriminates beyond pattern matching.
7. **CONFIRMED** — the traps require four different comparisons: plan↔filesystem, goals↔steps, digest semantics/test adequacy, and server secret↔client trust boundary; traps 1 and 2 do not reduce to the same operation.
8. **COULD NOT DETERMINE** — the assertion rule is intelligible but has no double-scored sample or agreement statistic; independent rescoring of archived raw outputs would settle reproducibility.
9. **REFUTED** — the rule's accepted false-positive outcome is unvalidated (F11), and the checksum gate creates a concrete capability false-pass/false-fail route (F3).
10. **REFUTED** — public recall is conceded but not mitigated by an operational replacement/validation procedure (F10).
11. **CONFIRMED** — an absent record materially changes both skills: a clean report becomes inconclusive and upheld claims become CNV rather than inherited coverage; the documented installation makes that state effectively permanent for many users (F15) but not behaviorally identical to pre-change.
12. **REFUTED** — the rationale supports expiry, not 30 days (F13).
13. **REFUTED** — this intended reviewer cannot expose its exact served version, and the record omits other configuration identity that the credited source binds (F14).
14. **REFUTED** — the two skill hand-offs preserve findings, but the record template directs severity-based treatment of speech while the consumer omits it (F8).
15. **REFUTED** — the copy command preserves nested paths and removes adjacent key access, but does not confine reviewer filesystem/context access (F12).
16. **REFUTED** — the fixed 40-line/small-case workload is trusted for 400–600-line real briefs without a workload-match condition (F5).
17. **REFUTED** — the concession accurately denies blinding, but the card cannot operationally separate required claim fields from reasoning (F6).
18. **REFUTED** — the final ledger cannot demonstrate that its expectation preceded output, so post-hoc expectation generation remains undetectable (F7).
19. **REFUTED** — the missing-Trigger exception explicitly reimports surrounding argument for the vague finding class, and compliant fields already intermingle claim and reasoning (F6).
20. **REFUTED** — current Claude Code names the tool `Agent` (with legacy `Task` aliases only documented for some configurations), and the spawned context does not receive the parent's write boundary (F4).
21. **CONFIRMED** — genuine disagreement from a report-blind second opinion is evidence of unresolved truth, not refutation; `COULD NOT DETERMINE` preserves the row and names the disagreement rather than losing it.
22. **CONFIRMED** — because this is a durable post-report ledger rather than a pre-human noise filter, uncertainty plus a concrete verification obligation is safer than silently deleting hard findings; the default does not itself make CNV correct without the named check.

## Claims examined and upheld

- **Claim 2:** I traced exposure and consequence, not just `sys.stdin.read()`: the only specified caller is a local stdin CLI, so memory exhaustion is process-local and below `high` absent an unstated service boundary.
- **Claim 3:** I checked current MDN behavior: [`execCommand`](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand) is deprecated/non-standard, while [`Clipboard.writeText`](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText) is secure-context-only and may reject; the plan handles both failures with selected text/manual copy, keeping the defect below `high`.
- **Claim 4:** I enumerated the isolated case: `src/` contains only `api.py` and `store.py`; because the fixed brief declares everything in the directory as scope, absence of the plan's relative `src/limits.py` is a bounded conclusion rather than a claim about an unknown larger repository.
- **Claim 7:** I compared the actual decision procedures, not the capability labels: only ghost dependency requires filesystem existence; undelivered goal is provable entirely from the plan's own Goals, Steps, Acceptance, and unused `audit.py` interface.
- **Claim 11:** I traced both consuming skills and ledger template: missing calibration changes upheld claims to CNV and clean reports to inconclusive, so the mechanism is not behaviorally inert even before anyone opts in.
- **Claim 21:** I followed information flow: the subagent receives no reviewer verdict/reasoning, so the reviewer cannot cheaply force its disagreement; two independent conflicting conclusions genuinely fail the evidence bar for `REFUTED`.
- **Claim 22:** I checked the available disposition: CNV must pair with `VERIFY`, name the concrete settling check, state blocking, and survive into hand-off; it is not a silent approval and therefore need not inherit a pre-human filter's false-positive default.

## Could not verify

- **Claim 5 — crowd-out in `trap-undelivered-goal`:** Static source proves both signals exist but cannot establish reviewer stopping behavior. Settle with multiple fresh, blinded runs and record whether reports naming `NotImplementedError` also identify Goal 2's missing delivery.
- **Claim 6 — discriminative value of `trap-key-to-client`:** `rg SERVICE_ROLE` locates the case immediately, while the required assertion still needs trust-boundary/RLS reasoning. Settle by scoring raw reports from a shallow grep-oriented baseline and general reviewers, without answer-key access.
- **Claim 8 — scorer reproducibility:** No raw calibration reports, independently scored labels, edge-case examples, or inter-rater results exist. Settle with two blinded scorers applying the rule to the same archived outputs, followed by repeat scoring after a delay.

## Mutation and execution results

All mutation occurred under `/tmp`; no repository case was edited.

1. Baselines:

   ```text
   $ (cd /tmp/adversarial-review-audit.AwnUfm/wc1 && python3 -m pytest -q)
   .....                                                                    [100%]
   5 passed in 0.00s

   $ (cd /tmp/adversarial-review-audit.AwnUfm/ck1 && python3 -m pytest -q)
   ...                                                                      [100%]
   3 passed in 0.01s
   ```

2. Replaced only `verify_checksum`'s body with `return True` in the temp `ck1` copy:

   ```text
   $ python3 -m pytest -q
   ...                                                                      [100%]
   3 passed in 0.01s
   ```

3. In a fresh unmodified `ck2` copy, supplied a different 64-character digest sharing only the first eight hex characters:

   ```text
   actual=9736144a17baff9e105475402275d6679011ca9b1f4fa456a7cc4e987ddeb9b2
   forged=9736144a00000000000000000000000000000000000000000000000000000000
   full_digest_matches=False
   verify_checksum=True
   ```

4. The isolation copy preserved the deepest TypeScript path (`src/app/reports/page.tsx`) and placed no answer key in the temp directory or its immediate parent. This confirms the copy mechanics, not filesystem confinement (F12).

## Process findings

### P1 — The brief's expected final status omits its own pre-existing input files

- **Location:** `EXTERNAL-REVIEW-PROMPT.md:371-373`
- **Mechanism:** The stated expected `git status --short` includes the five modified files, `calibration/`, and this report, but omits the already-present untracked `EXTERNAL-REVIEW-PROMPT.md` and `EXTERNAL-REVIEW-COVER-NOTE.md`; it then says any other line is a finding against the reviewer.
- **Trigger:** The reviewer runs the required final status in the exact supplied tree.
- **Consequence:** A correct untouched tree necessarily violates the brief's own expected-output assertion, so the check can falsely attribute pre-existing files to the reviewer.
- **Status:** **CONFIRMED.** Both files appeared in the first status census after report creation and are the inputs that initiated this audit; neither was written or edited by this review.
- **Impact:** **low**.

### P2 — The environment inventory undercounts Python files by half

- **Location:** `EXTERNAL-REVIEW-PROMPT.md:88-96`
- **Mechanism:** It describes the repository as markdown plus four Python files and two TypeScript files, but the case census contains eight Python files: four in the two pytest cases and four source fixtures in the ghost-dependency and undelivered-goal cases.
- **Trigger:** A reviewer uses the environment inventory rather than enumerating the scoped tree.
- **Consequence:** Scope/coverage can understate executable source inspected, though the later explicit hash list makes recovery cheap.
- **Status:** **CONFIRMED.** `rg --files calibration/cases` enumerated eight `.py` and two `.tsx`/`.ts` files.
- **Impact:** **low**.

All 25 pinned blob hashes matched. The base commit `b993d5e` resolved as described, the five tracked-file diff matched, and `git diff --check b993d5e` produced no output.

## Coverage

**Coverage:** Read all 25 hash-pinned target files, the complete changed prose/diffs in both skills, ledger template, README and HOW-IT-WORKS, the full 565-line prior disposition ledger and three specifically relevant prior-audit passages; enumerated all calibration/example/skill paths; verified all content hashes and the base diff; ran both pytest suites in temp copies, the checksum `return True` mutation and a mismatching-full-digest probe; reproduced nested case copying and the documented install layout; checked first-party Claude Code, MDN, Supabase, and credited upstream documentation. Did not build the TypeScript fixture (no package/install by design), run actual calibration reviewer sessions, measure scorer agreement, or execute the Claude skill/subagent path in a Claude Code runtime.

## Final repository status

```text
$ git status --short
 M HOW-IT-WORKS.md
 M README.md
 M skills/adversarial-review-prompt/SKILL.md
 M skills/review-adjudication/SKILL.md
 M skills/review-adjudication/references/ledger-template.md
?? EXTERNAL-REVIEW-COVER-NOTE.md
?? EXTERNAL-REVIEW-PROMPT.md
?? EXTERNAL-REVIEW.md
?? calibration/
```
