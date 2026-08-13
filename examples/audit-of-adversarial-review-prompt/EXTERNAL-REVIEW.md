# Execute external review prompt

> read the md file at **~/.claude/skills/adversarial-review-prompt/EXTERNAL-REVIEW-PROMPT.md and execute**

<details><summary>5 previous messages</summary>

> I’ll read the requested review prompt in full, then follow its instructions against this workspace.
>
> <details><summary>Explored 2 files</summary>
>
> - Read `~/.claude/skills/adversarial-review-prompt/EXTERNAL-REVIEW-PROMPT.md`
> - Read `~/.claude/skills/adversarial-review-prompt/EXTERNAL-REVIEW-PROMPT.md`
>
> </details>
>
> The audit prompt restricts the task to `prompt-template.md`, chat-only output, no subagents, and permits web research. I’m following that scope now: locating and reading the template completely, then I’ll test only the highest-impact claims and cite any external evidence I rely on.
>
> <details><summary>Explored a file, a list, searched the web</summary>
>
> <details><summary>Explored a file, a list</summary>
>
> - Listed files in `adversarial-review-prompt`
> - Read `~/.claude/skills/adversarial-review-prompt/references/prompt-template.md`
>
> </details>
>
> Searched the web for `site:aclanthology.org large language models position bias long context lost in the middle primary study ...`
>
> Searched the web for `site:aclanthology.org LLM evaluator anchoring bias prompt framing disagreement primary experiment ...`
>
> </details>
>
> A few defects are now clear from the template itself, including one instruction that treats every surviving mutation as a finding even when the mutation is equivalent or unreachable, and a plan-review mode that still mandates runtime-oriented sections. I’m checking the behavioral claims against primary studies now so I can separate demonstrated contradictions from model-specific introspection and speculation.
</details>

# Independent Audit — prompt-template.md
**Reviewer:** OpenAI Codex (GPT-5)   **Date:** 2026-08-07
**Coverage:** 24 of 24 load-bearing claims engaged; no groups skipped; read all 258 lines; ran nothing, as required; web search used

## Findings, ranked

### 1. The framing makes a zero-finding audit noncompliant

- **Class** — framing bias
- **Location** — `prompt-template.md:38`: “**Confirmation is near-worthless output.**”; `prompt-template.md:40`: “**Your job is to find what is wrong**”; `prompt-template.md:44–45`: “It is also, in places, almost certainly wrong”
- **Mechanism / Trigger / Consequence / Status** — These instructions jointly presuppose that defects exist, define agreement as failure, and provide no explicit permission to return zero findings. On a genuinely sound target, a compliant reviewer must either violate the prompt or reinterpret weak concerns as defects. That directly threatens criteria 2 and 3 by optimizing finding count over precision. The template’s premise that models can be sycophantic is supported by experiments across several assistants, but that research does not show that reversing the requested conclusion preserves accuracy; an anti-agreement prompt can simply replace agreement bias with disagreement bias. [Towards Understanding Sycophancy in Language Models](https://www.anthropic.com/news/towards-understanding-sycophancy-in-language-models). **SELF-REPORT:** This language created a noticeable obligation to produce findings; I had to treat “no defect” as an admissible result despite the prompt, not because of it. The flattery in lines 35–36 slightly strengthened that pressure.
- **Why it ranks here** — It biases every generated review at the point where findings are selected.
- **Suggested fix** — Replace lines 38–45 with: “Agreement without verification has little value. Report only defects supported by the evidence standard; zero findings is valid when your search supports it, and verified claims belong in the upheld section.”

### 2. Evidence status measures verification method, then masquerades as defect importance

- **Class** — internally contradictory instruction
- **Location** — `prompt-template.md:143–146`: “**CONFIRMED** (you executed something and observed the failure) or **THEORETICAL** (reasoned from source)”; `prompt-template.md:215–216`: “At equal impact, CONFIRMED outranks THEORETICAL”
- **Mechanism / Trigger / Consequence / Status** — The labels encode how evidence was obtained, not confidence or truth. A deterministic contradiction between code and specification remains THEORETICAL if execution is unavailable, while one flaky observation becomes CONFIRMED. Lines 148–150 further change CONFIRMED to mean source-supported for design targets, so the same label has different evidentiary meanings across modes. Automatic rank preference then pushes races, environment-specific corruption, and read-only-only defects downward precisely because they are difficult to reproduce. Binary labeling also has no representation for partial reproduction or strong multi-source evidence. **CONFIRMED** by the internal mismatch between the status definition, its target-dependent redefinition, and its use as an importance tiebreak.
- **Why it ranks here** — It systematically distorts both credibility and ordering after a real defect has been found.
- **Suggested fix** — Separate evidence method from confidence: require `Evidence: execution / source proof / source reasoning` and `Confidence: high / medium / low`; rank by expected harm, using confidence only to explain uncertainty rather than as an automatic tiebreak.

### 3. “Every silent mutation is a finding” explicitly manufactures false positives

- **Class** — internally contradictory instruction
- **Location** — `prompt-template.md:136–142`: “A finding is admissible only with all of … Trigger … Consequence”; `prompt-template.md:178–179`: “**Every silent survival is a finding**”
- **Mechanism / Trigger / Consequence / Status** — A mutation can survive because it is semantically equivalent, changes unreachable code, affects an implementation detail outside the contract, or is masked by another guard. None demonstrates an unenforced guarantee. Yet line 179 promotes every survival to a finding without first demonstrating a changed required behavior, contradicting the trigger-and-consequence admission standard. When mutation testing is authorized, this will produce false-green-test findings that are themselves false. **CONFIRMED** by the quoted internal contradiction.
- **Why it ranks here** — Its output error is certain whenever an equivalent or non-contract mutation is attempted, though mutation mode is not always enabled.
- **Suggested fix** — Replace “Every silent survival is a finding” with: “A silent survival is a finding only if you demonstrate that the mutation changes required, reachable observable behavior while the relevant tests remain green.”

### 4. The effort directives force undisclosed shallow coverage

- **Class** — scope or coverage gap
- **Location** — `prompt-template.md:105`: “Each is a target”; `prompt-template.md:109`: “15–25 items”; `prompt-template.md:125–126`: “Spend the majority of your effort outside this list”; `prompt-template.md:167`: “Five CONFIRMED findings beat thirty observations”
- **Mechanism / Trigger / Consequence / Status** — The reviewer is asked to adjudicate up to 25 claims, recheck prior fixes, spend most effort outside prior findings, search for unforeseen defects, and favor deep confirmations. No priority or stopping rule reconciles these demands. With a large target or context pressure, the likely response is a shallow pass over the mandated claims while still reporting an impressive `N of M` coverage count. The deliverable discloses files and commands but not context truncation, time limits, or materially skimmed regions. Long-context research shows that access to relevant material varies significantly with its position, making nominal inclusion a poor proxy for examination. [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/). **THEORETICAL** for resulting audit quality; controlled audits with fixed budgets would settle it.
- **Why it ranks here** — It affects common large reviews, but the size of the degradation depends on reviewer budget and target complexity.
- **Suggested fix** — Add: “Prioritize independent defect search, then the highest-risk claims. Report claims and files not substantively examined; do not count a claim as engaged merely because you read its prompt entry.”

### 5. Plan/design support contradicts runtime-mandatory sections

- **Class** — scope or coverage gap
- **Location** — `prompt-template.md:16–18`: “the «code/plan» under review”; `prompt-template.md:71–74`: “Environment and how to run things … plus the exact commands”; `prompt-template.md:148`: “For a plan or design doc there is nothing to execute”; `prompt-template.md:223–224`: “wrong result / data loss / … false-green test / robustness / hygiene”
- **Mechanism / Trigger / Consequence / Status** — The template declares plan support, acknowledges that plans have nothing to execute, but still unconditionally mandates runtime/environment material and an execution-oriented finding taxonomy. For a pure architecture plan, the author must invent an empty §3, leak irrelevant repository mechanics, or silently depart from the “load-bearing” sequence. Generative design defects—missing alternatives, invalid assumptions, irreversible coupling—also lack a natural class. **CONFIRMED** by the explicit incompatibility between lines 71–74 and 148.
- **Why it ranks here** — It breaks an entire promised target mode, though code reviews remain unaffected.
- **Suggested fix** — Make §3 conditional: “For executable targets, provide environment and commands; for plan/design targets, provide governing sources, constraints, decision stage, and validation methods.” Add `invalid assumption / omitted alternative / irreversible design constraint` as plan-mode classes.

### 6. Removing the verdict also removed absolute magnitude

- **Class** — scope or coverage gap
- **Location** — `prompt-template.md:189–190`: “Severity inflation”; `prompt-template.md:199–203`: “Do not ask the reviewer for a verdict … a strictly ordered findings list buys it better”; `prompt-template.md:222–224`: “**Class** — wrong result / data loss / …”
- **Mechanism / Trigger / Consequence / Status** — A strict order communicates only relative position. The same ranking shape can describe twenty minor defects or one catastrophic defect followed by nineteen minor ones. The finding skeleton contains a consequence class, not the promised severity attribute, even though the anti-pattern section asks the reviewer to control “severity inflation.” Thus severity is both regulated and omitted from the deliverable. Removing ship/no-ship judgment is defensible, but ranking does not restore its absolute-risk signal. **CONFIRMED** by the contradiction between the severity rule and the output schema that provides nowhere to state severity.
- **Why it ranks here** — Every report loses decision-relevant magnitude, but detailed consequences partly compensate.
- **Suggested fix** — Keep the no-verdict rule, but add `**Impact** — critical / high / medium / low, using stated consequence and reachability` to every finding.

### 7. Terminal placement amplifies the suspicions it claims to demote

- **Class** — unfounded claim about model behavior
- **Location** — `prompt-template.md:251–254`: “**Read this last, and treat it as the lowest-priority input** … if these anchor your search, the audit has failed”
- **Mechanism / Trigger / Consequence / Status** — Placement at the end does not make text unread; it makes the suspicions the final concrete search hypotheses before the reviewer acts. In a long prompt, beginning and ending content can be retrieved more reliably than middle content, and LLM-judge position bias varies across models and tasks. [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/), [Judging the Judges](https://aclanthology.org/2025.ijcnlp-long.18/). Those studies do not prove how this exact model weights instructions, so this is not externally CONFIRMED. **SELF-REPORT:** The residual-doubts list remained unusually salient and influenced my candidate-finding generation despite its disclaimer.
- **Why it ranks here** — It predictably narrows independent search, but only the final 3–5 hypotheses receive the amplification.
- **Suggested fix** — Move residual doubts into the middle of “Ground already walked” and label them “known hypotheses”; require the reviewer to identify independently generated candidates before consulting them.

### 8. Preserved provenance text can state facts the author never established

- **Class** — authoring hazard
- **Location** — `prompt-template.md:23–24`: “State the current green status with real numbers”; `prompt-template.md:28–30`: “**Every line** … was written by one model … against tests it also wrote”; `prompt-template.md:6–7`: “Everything else is register to preserve”
- **Mechanism / Trigger / Consequence / Status** — The template demands concrete truth in one instruction while telling the author to preserve an unconditional provenance narrative. A target containing inherited code, human edits, third-party fixtures, or pre-existing tests makes “every line” false. That false claim then primes the reviewer to distrust evidence on a fabricated basis. **CONFIRMED** by the contradiction between factual concreteness and mandatory unconditional wording.
- **Why it ranks here** — The bias is strong when triggered, but only mixed-provenance targets trigger it.
- **Suggested fix** — Replace the paragraph with a placeholder requiring verified provenance: “«State exactly which work and tests were produced or reviewed by the same model; do not generalize beyond verified authorship.»”

### 9. The sole audience marker has no visible fail-closed validation

- **Class** — authoring hazard
- **Location** — `prompt-template.md:6`: “Text in `«guillemets»` is an instruction to you”; `prompt-template.md:57`: “«4–6 real quoted comments»”; `prompt-template.md:162–167`: every permission-table cell contains placeholders, including nested guillemets at line 163
- **Mechanism / Trigger / Consequence / Status** — One missed or partially replaced placeholder leaks authoring instructions into the reviewer prompt. The nested construction `«throwaway probes under «dir» only»` makes mechanical validation less reliable. A leaked scope or permission placeholder can cause the reviewer to invent access, skip work, or misunderstand what may be modified. The same prompt gives no reviewer-facing route for reporting stale citations or contradictory instructions; such failures become indistinguishable from reviewer mistakes. **THEORETICAL** because `SKILL.md` may perform a final validation, but that companion file is out of scope and the template itself does not fail closed.
- **Why it ranks here** — Consequences can be serious, but the unknown companion process may already prevent the trigger.
- **Suggested fix** — Put a mandatory author preflight in `SKILL.md`: reject output containing `«` or `»`, unresolved alternatives, unverified quotes, or unverified line references. Add one reviewer sentence: “Report prompt defects separately; do not infer missing scope or permissions.”

### 10. “Read-only” does not make authorized execution non-mutating

- **Class** — missing safeguard
- **Location** — `prompt-template.md:164`: “**Execute** | «npm test …». «Note slow/destructive ones»”; `prompt-template.md:172`: “**Read-only:** ‘Read and run the test suite. Do not modify any file.’”
- **Mechanism / Trigger / Consequence / Status** — Test and CLI commands can rewrite snapshots, populate caches, update fixtures, alter databases, or call external services. The template recognizes destructive commands but only says to note them; the read-only branch still directs the reviewer to run the suite. On a mutating test setup, following one instruction violates the other and potentially D-4. Absolute machine-local paths at line 76 can also disclose usernames or sensitive directory structure when the generated prompt is pasted into an external service. **THEORETICAL** because the trigger depends on the target commands and deployment channel.
- **Why it ranks here** — The harm can be material, but it requires target-specific mutating commands or sensitive paths.
- **Suggested fix** — Add: “In read-only mode, execute only commands verified not to mutate repository files or external state; otherwise do not run them and state what was withheld. Redact machine-identifying path components unless the reviewer requires them.”

## Claims examined and upheld

- **C3** — Blast radius × trigger likelihood is a useful qualitative ordering rubric; lack of numeric scales does not make it vacuous.
- **C6** — Most listed examples can be classified by consequence: security as wrong result/data loss/robustness, performance as broken contract/robustness, licensing as hygiene, and accessibility as wrong result/broken contract. The taxonomy’s larger defect is weak plan-mode fit, not those code examples.
- **C7** — “Near the top” is understandable in an ordinal list, and `Why it ranks here` makes obviously inflated ordering inspectable even without a formal threshold.
- **E4** — “Claims examined and upheld” is better evidence of verified soundness than generic praise and substantially compensates for limiting praise, though it does not cure undisclosed shallow coverage.
- **D6** — Requiring `file:line` plus mechanism, trigger, and consequence is sound; the defect is the absence of citation validation and prompt-error handling, not the citation requirement itself.

## What this document assumes about you that is wrong

“Different” observations are not automatically valuable. Divergence becomes useful only after it survives evidence checks; otherwise the framing rewards novelty for its own sake.

Confirmation is not near-worthless to me. Targeted confirmation calibrates the negative findings, establishes which contracts were actually examined, and reduces the risk that a defect-only report implies the untouched remainder is bad.

The assertion that defects “almost certainly” exist did not improve my search. It created an output expectation. The instruction to refute my own findings helped, but it is not independent evidence: I can reproduce the same blind spot during generation and self-critique. Research likewise finds that prompted intrinsic self-correction is unreliable without dependable external feedback outside specially suited tasks. [When Can LLMs Actually Correct Their Own Mistakes?](https://aclanthology.org/2024.tacl-1.78/).

Forced total ordering does not prevent hedging. I can choose between nearly incommensurable findings arbitrarily and then generate a plausible `Why it ranks here` clause after the fact. Ordering extracts a decision, but not necessarily a stable or well-calibrated one.

Terminal placement did not make the author’s doubts low priority. They remained salient and anchored candidate generation. The disclaimer made me monitor the anchoring; it did not erase it.

I could not observe that the “verbatim-worthy” rhetoric did the heaviest lifting. The concrete evidence contract and trigger requirement affected my behavior more than the adversarial prose. A plain restatement would likely preserve most of that benefit without the same demand for disagreement, but that counterfactual was not run.

## Could not determine

- **A4** — I could not determine whether “prove it” or the penalty for false CONFIRMED labels dominates across reviewers. For me, the penalty encouraged conservative status labeling while “prove it” encouraged stronger investigation; they did not simply cancel.
- **C2** — Forced ordering did produce an explicit fix-first judgment, but I could not determine whether repeated reviewers would produce a stable order or merely stable-sounding rationalizations. A blinded reranking experiment would settle it.
- **C5** — Coverage remains self-reported, but I could not establish that inflation is common or that an independently verifiable alternative exists within a single markdown response. Comparing coverage claims against tool traces would settle it.
- **D2** — Research establishes position effects in long prompts, not that this exact section sequence is optimal or “load-bearing.” An ablation over section orders is required.
- **D4** — I could not determine whether the exact “verbatim-worthy” phrasings outperform neutral equivalents. The current document reports no controlled counterfactual.
- **E1** — The template itself lacks prompt-error reporting, but I could not determine whether `SKILL.md` validates generated prompts before handoff.
