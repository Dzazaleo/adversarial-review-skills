# External Review 3 — Unscoped Product and Implementation Audit

**Reviewer identity:** OpenAI Codex (exact served model and effort not stated by the user at capture time — see the identity line below before adjudicating).

**Delivery:** returned in the reviewer's chat, not written to a file. This document is the operator's verbatim transcription of that chat output, captured on 2026-08-22. The only material omitted is the reviewer's collapsed tool-call trace (`Explored N files`, `Ran ...` blocks); every word of the prose report is preserved. Because the reviewer did not write this file itself, the report is a **transcription**, and the ledger must treat transcription fidelity as an open question rather than an established fact.

**Brief:** none. The operator's instruction was: *"i've been creating claude skills to deal with external reviews. I'm not pointing you at anything particular, but i'd want you to take a look at it and tell me your impressions about it. Anything worth improving/fixing is worth telling in the report."* There is no audit brief, no pinned range, no load-bearing claim list, and no declared scope. This is an unscoped review.

**Self-declared method:** *"I'll review the repository as a product and implementation audit: skill design, instruction quality, workflow safety, scripts/tests, portability, and maintainability. I'll keep it read-only and return prioritized findings with concrete file references. I'm not invoking the Codex skill-creator skill because these are Claude-oriented skills and you asked for an assessment, not a Codex skill change."*

---

## Report

Overall: this is genuinely strong work—far more rigorous and self-critical than most prompt-based review systems. The separation between "is the finding true?" and "what do we do about it?" is especially good.

I would use it, but I would not yet trust its permission boundaries or claims of blind verification without the fixes below.

## Highest-priority findings

1. **The `allowed-tools` frontmatter is dangerously misunderstood**

Both skills pre-approve broad capabilities, including unrestricted `Bash`; adjudication also pre-approves `Write`, `Edit`, and `Agent`:

- [adversarial-review-prompt/SKILL.md](./skills/adversarial-review-prompt/SKILL.md:5)
- [review-adjudication/SKILL.md](./skills/review-adjudication/SKILL.md:5)

In current Claude Code, `allowed-tools` is a permission grant, not an allowlist restricting available tools. Thus the prose saying "only write the report/ledger" is advisory while the skill has already authorized much more. The grant also expires after the invoking turn, making it simultaneously overbroad and unreliable across clarification turns. [Claude Code's documentation is explicit about both points](https://code.claude.com/docs/en/slash-commands).

Recommended fix:

- Pre-approve only `Read`, `Grep`, and `Glob`.
- Let writes and arbitrary shell commands go through normal permission handling.
- If the boundary must be enforced, distribute these as a plugin with a path-aware `PreToolUse` hook rather than relying on prose.
- Reopen the earlier "unbounded Write/Edit" finding: the recorded prose-only fix did not close the actual permission issue.

2. **Compaction can remove the most important half of each skill**

The prompt skill is about 5,583 words; adjudication is about 6,472 words and 523 lines. Claude Code recommends keeping `SKILL.md` under 500 lines and, after compaction, reattaches only the first 5,000 tokens of each invoked skill. [The lifecycle and limit are documented here](https://code.claude.com/docs/en/slash-commands).

The likely truncation point is around line 300. That risks dropping:

- Prompt skill: operating envelope, cover note, doubt checking, hand-off.
- Adjudication skill: echo analysis, subagent escalation, verdict matrix, write boundary, ledger and hand-off rules.

Those are precisely the rules most expensive to lose.

Recommended fix: reduce each `SKILL.md` to a compact operational checklist, move history and rationale into direct reference files, and put all safety/write/closure invariants near the beginning. Deterministic checks should become scripts.

3. **Residual doubts do not survive the documented fresh-session workflow**

The README says nothing later depends on keeping the authoring session open and that adjudication can happen days later on another machine:

- [README.md](./README.md:149)

But residual doubts are kept only in the session scratchpad and chat hand-off:

- [prompt skill](./skills/adversarial-review-prompt/SKILL.md:425)

The fresh adjudicator is then expected to search and rule on those doubts:

- [adjudication skill](./skills/review-adjudication/SKILL.md:336)

It has no durable source from which to obtain them.

Recommended fix: make the prior hand-off an explicit adjudication input. Either instruct the user to paste it verbatim into the fresh session, or save a private author-notes artifact outside the reviewer's readable root. A commitment/hash plus later disclosure would give stronger proof that the doubts predated the review without anchoring the reviewer.

4. **The "blind" subagent is write-restricted, but not read-isolated**

The adjudication skill says the second opinion "never saw the report," yet the report is beside the code and the verifier retains `Read`. The skill itself correctly observes that artifacts in the same directory are one `ls` away:

- [review-adjudication/SKILL.md](./skills/review-adjudication/SKILL.md:365)
- [blind escalation](./skills/review-adjudication/SKILL.md:400)

A tool allowlist prevents edits; it does not prevent the verifier from opening the report. This is an inference from Claude Code's documented subagent working-directory and tool behavior. [Subagent documentation](https://code.claude.com/docs/en/sub-agents).

Recommended fix: run the verifier against a sanitized temporary copy containing only the claim card and relevant source files, under an enforced filesystem boundary. If read isolation cannot be established, it should not count as the mandatory blind second opinion for a high-impact `REFUTED`.

5. **Same-family reviews receive a knowingly false framing sentence**

The skill supports another fresh Claude session and tells the user when the reviewer belongs to the same family. Nevertheless, the template unconditionally tells every reviewer:

> "You have a different architecture and different training."

See [prompt-template.md](./skills/adversarial-review-prompt/references/prompt-template.md:31).

That is false for the explicitly supported same-family route and may also be unknowable for products wrapping undisclosed models.

Recommended fix: make the framing conditional:

- Different known family: state the two identified families.
- Same family: state that context is fresh but architectural independence is absent.
- Unknown lineage: say it is unknown; do not infer architecture or training.

## Other worthwhile improvements

- **Add executable invariant checks.** The repository currently has tests for two calibration fixtures, but no validator for the skills themselves. Add checks for YAML, unresolved guillemets, valid verdict/disposition combinations, finding-count equality, permission agreement, artifact collisions, report/brief pairing, and no-filesystem variants. This would also address the known corpus-validation backlog more systematically.

- **Define artifact naming and collision rules.** Instructions describe `NN-EXTERNAL-REVIEW...`, while the repository also uses `EXTERNAL-REVIEW-2...`. Phase number and review round are not mapped by one algorithm, and prompt generation does not explicitly forbid overwriting an existing brief or cover note.

- **Standardize `COULD NOT DETERMINE`.** [calibration/README.md](./calibration/README.md:150) uses `COULD NOT VERIFY`, while the ledger vocabulary uses `COULD NOT DETERMINE`.

- **Repair the browser-chat delivery wording.** The template asks for one continuous message but also says to end and resume if length forces a break. Most chat models cannot initiate that continuation without another user turn.

- **Remove or replace the optional broken link** to `references/example-audit-prompt.md` in [SKILL.md](./skills/adversarial-review-prompt/SKILL.md:220).

- **Keep the public-corpus limitation prominent.** You have already captured this well in `BACKLOG.md`: a public answer key may eventually measure recall rather than review ability. That remains the largest validity limitation of calibration, even though it is honestly documented.

## What is especially good

- Verdict and disposition are correctly separated.
- "Calibration governs silence, never speech" is an excellent rule.
- Partial and non-review reports are handled without laundering silence into approval.
- The report-as-an-early-file design improves interruption recovery.
- Prompt/report instructions are treated as untrusted data during adjudication.
- Count-in/count-out and durable deferral obligations prevent findings from disappearing.
- The repository openly preserves past mistakes and corrective reasoning rather than presenting a cleaned-up mythology.

I parsed both skill frontmatters successfully, ran the available fixture suites—`8 passed`—and left the working tree unchanged. My main recommendation is architectural: preserve the methodology, but move deterministic enforcement out of prose and shorten the operational skill bodies substantially.
