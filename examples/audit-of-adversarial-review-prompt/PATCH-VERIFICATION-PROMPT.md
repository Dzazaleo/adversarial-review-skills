# Patch Verification — the ten amendments to `prompt-template.md` and `SKILL.md`

> **Prompt for an external reviewer (Codex).** You audited `prompt-template.md` on
> 2026-08-07 and reported ten findings. Nine were accepted (some with altered fixes) plus
> one addition, and the amendments have been applied. This is a **patch verification, not a
> second audit**. The design decisions are settled and are not the question. The question
> is: does each amendment implement its stated intent, and did the new text introduce
> defects the old text did not have?

## Ground rules

- **Do not re-audit unchanged text.** The remainder of both files was covered by your first
  pass. Re-reporting anything from it, or re-litigating an accepted design decision (no
  verdict, ranked findings, doubts held back), is discarded output.
- **Zero findings is an admissible result.** If the patch is clean, say so and show what
  you checked. A manufactured finding is worse than none.
- If this prompt is itself defective — a citation that does not match the file, an intent
  that misdescribes a finding you made — report that at the top of your reply.
- A note on quoting: text wrapped in `«guillemets»` inside the template is, by that file's
  own convention, an instruction to the prompt author, not to the end reviewer. Several
  amendments below are deliberately guillemeted. That is correct usage, not leakage.

## Files

| | |
|---|---|
| Template | `~/.claude/skills/adversarial-review-prompt/references/prompt-template.md` (296 lines; was 258 at your first pass) |
| Skill | `~/.claude/skills/adversarial-review-prompt/SKILL.md` (239 lines) |
| Your first review | `~/.claude/skills/adversarial-review-prompt/EXTERNAL-REVIEW.md` — optional context; the checklist below states each intent compactly |

## The checklist — verify implementation against intent

For each item: **IMPLEMENTED** (matches intent, no new defect), **DIVERGES** (quote the gap
between intent and text), or **DEFECTIVE** (the new text creates a new problem — quote it).

**V-1 — Zero-findings escape valve** (your F-1). New bullet at `prompt-template.md:44` ("A
manufactured finding is worse than no finding") and softened closing at line 51 ("those
places are what you are here for" replacing "almost certainly wrong"). *Intent: make an
empty or near-empty report admissible without dissolving the adversarial pressure.* Check
both directions: does pressure to fabricate remain, and has the block now tipped so far the
adversarial framing is blunted?

**V-2 — Provenance gated on fact** (your F-8). Intro at `prompt-template.md:26` makes the
"every line" sentence conditional on verified authorship. *Intent: no false provenance on
mixed-authorship targets.* Check: does the instruction actually stop an author from keeping
the verbatim sentence unverified, or is it advisory decoration?

**V-3 — Plan/design mode** (your F-5). §3 replacement at `prompt-template.md:91-93`;
plan-mode finding classes at line 256. *Intent: plan targets get a coherent §3 and a class
taxonomy that fits.* Check the seams: §4 (scope), §5 (contract), and §8b (envelope) were
NOT given plan-mode variants — does the patched document still force runtime material into
a plan prompt anywhere?

**V-4 — Engagement definition + coverage disclosure** (your F-4). `prompt-template.md:119-122`
("Engaging a claim means doing the work its adjudication needs…") and the Coverage line at
240-241 ("what you did not substantively examine"). *Intent: an inflated N-of-M count
becomes a lie rather than an ambiguity.* Check specifically against line 140 ("Spend the
majority of your effort outside this list") — are the two effort rules now consistent or in
tension?

**V-5 — Impact attribute + tiebreak removal** (your F-2 and F-6 merged). Ranking rubric at
`prompt-template.md:246-248` ("Evidence status is not impact…"); per-finding **Impact**
field at line 258; anti-pattern reworded at line 219 ("Impact inflation"); matching SKILL.md
text at lines 165-168. *Intent: severity exists as an attribute, evidence-acquisition method
no longer distorts rank.* Check: does any surviving text still imply CONFIRMED should rank
higher, and do the two files state the same rule?

**V-6 — Mutation survival narrowed** (your F-3). `prompt-template.md:206-209`. *Intent:
equivalent mutants, unreachable code, and out-of-contract behaviour no longer count as
findings.* Check the wording carries the full three-part condition: required, reachable,
observable.

**V-7 — Read-only means non-mutating + path redaction** (your F-10). `prompt-template.md:198-202`
and the redaction note at 82-84. *Intent: snapshot-updating suites are not "read-only";
machine paths do not leak to external services.* Check: the same read-only prose still says
"Read and run the test suite" — is the sentence now internally coherent?

**V-8 — Guillemet preflight + prompt-defect channel** (your F-9). SKILL.md:178-180
(fail-closed grep) and the reviewer-facing instruction at `prompt-template.md:172-175`.
*Intent: placeholders cannot leak; a reviewer that receives a defective prompt reports it
instead of guessing.* Check the interaction that already bit once: is there any remaining
**verbatim-worthy, reviewer-facing** text in the template that contains literal guillemets
and would therefore be rejected by the preflight it must pass? (Guillemets in
author-instruction text and in fill-in placeholders are correct; the defect is only text
meant to survive into the generated prompt as-is.)

**V-9 — Residual doubts held back** (your F-7, altered fix — removal, not relocation).
Template §11 at `prompt-template.md:284-296`; SKILL.md:170-174 and the hand-off bullet at
226-228. *Intent: the reviewer never sees the author's suspicions; the user compares them
against the returned review afterward.* Check for orphans: does any remaining text in either
file still assume the doubts appear in the prompt?

**V-10 — SELF-REPORT conditional status** (new, from your review's most useful output
channel). `prompt-template.md:167-169`. *Intent: available only when the target makes claims
about model behaviour; never a standing status for code targets.* Check: is the condition
stated tightly enough that a reviewer of ordinary code cannot invoke it?

## Sweep the new text — one pass, new text only

Beyond the checklist: read only the amended passages listed above as a set and ask whether
any two of them contradict each other or the sentence beside them. The one defect class a
patch author cannot see is the interaction between two of their own simultaneous edits —
that is what this sweep is for. SELF-REPORT status is admissible where an amended passage
makes a claim about how models behave.

## What you may and may not do

| | |
|---|---|
| **Read** | The two files above, plus your first review for context |
| **Write** | Nothing |
| **Execute** | Read-only shell only (`cat`, `grep`, `sed -n`) — nothing that writes |
| **Network / installs** | Not needed; skip |
| **Effort** | Small. This is a patch check, not an audit. Expect 0–5 findings; a clean report with the checklist filled is a complete deliverable |

## Deliverable

```markdown
# Patch Verification — adversarial-review-prompt amendments
**Reviewer:** <model/version>   **Date:** <date>
**Coverage:** <N of 10 checklist items verified; which you did not substantively examine>

## Checklist verdicts
V-1 … V-10, one line each: IMPLEMENTED / DIVERGES / DEFECTIVE, with the quote when not
IMPLEMENTED.

## Findings, ranked
Only if any exist. Most important first, strict order, no ties. Each with:
- **Class** — new contradiction / intent not implemented / new false claim / regression
- **Impact** — critical / high / medium / low
- **Location** — file:line + verbatim quote
- **Mechanism / Consequence / Status** (CONFIRMED = quoted contradiction or quoted
  intent-vs-text gap; THEORETICAL = reasoned; SELF-REPORT = introspective, stated as such)
- **Suggested fix** — the replacement sentence, no redesign

## Clean
What you checked and found sound, one line per area. If everything: say so plainly.
```

Go.
