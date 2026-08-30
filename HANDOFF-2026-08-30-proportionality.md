# Handoff: add proportionality to the adversarial-review skill pair

**Date:** 2026-08-30 · **Requested by:** Leo · **Origin:** the Spine_Texture_Manager
retrospective session of 2026-08-30 (the "why did the project stall" analysis). This file is
self-contained; you do not need that session's transcript.

**Deliverable:** edits to `skills/adversarial-review-prompt/SKILL.md` and
`skills/review-adjudication/SKILL.md` (and their references where named) implementing §3 below.
The installed live copy is a SEPARATE git repo at `~/.claude/skills/` (it flattens the `skills/`
prefix — the dirs sit at its root) — after editing here, sync the installed copy too, and note it
currently carries uncommitted drift (modified `adversarial-review-prompt/SKILL.md`, several
deleted review artifacts) that should be reconciled before syncing over it.

---

## 1. Why change — the measured evidence

The owner paused the Spine_Texture_Manager project on 2026-08-30 because phases had stopped
closing. The retrospective measured (all figures re-derivable from that repo's git history):

- **The skills were NOT the engine of the stall.** Phase 103.695 ran its whole
  verify→gap-plan→execute loop three rounds with **zero** external reviews. The loop's engine was
  project-side: prose-accuracy gates written into plan must_haves. That is fixed project-side
  (CLAUDE.md closure policy, 2026-08-30: Success Criteria close phases; prose is never a blocker;
  two verification rounds max; external reviews once per phase, at the end, blockers only).
- **But the skills were a large cost multiplier.** Phase 103.69 absorbed ~10 external review
  reports (3 models × 2 rounds on one question, plus plan/close reviews), 49 adjudicated findings,
  and generated **31 distinct owner-ruling IDs / 65 owner-question mentions** — most manufactured
  by the adjudication skill's "hand every owner-judgement finding up as a decidable question"
  rule. The owner could not follow them ("guide me, plain terms" opened 8 sessions in 8 days).
  One adjudication ≈ one full session of work under the current protocol.
- **The skills' own text records the echo problem.** prompt §3: of the reviewer findings, 10 of 15
  in one round and 6 of 9 in another were echoes of the brief's seeded sub-questions; roughly one
  in nine findings arrived unprompted. The directed-claims list works, but most of what comes back
  is the brief talking to itself — which the adjudicator then re-verifies at full cost.
- **The residual-doubts ritual has failed every time it was measured.** prompt §9's own history:
  doubts leaked into the brief 5/5, 4/4, 2/3, then 5/5 again on 2026-08-23 *with the search
  correctly run*. The protocol (SEEDED/UNSEEDED buckets, chat-only channel, "keep the message
  until the adjudicator asks, if the window is lost the list is lost") protects a small
  corroboration credit at ~80 lines of protocol plus a fragile human channel. Cost ≫ value for a
  solo project.
- **The claims-mining framing helped set a damaging culture.** §3 greps comments for
  `measured|verified|guaranteed|never…` and directs the reviewer at them. Combined with a
  project-side rule ("a false clause shipped in a fix commit is a blocker", 103.69 round 2), code
  comments became a first-class attack surface: 103.69 verification rounds 3–5 and 103.695 round 3
  were **100% documentation-class findings** — wrong line pointers, docblock phrasing — while all
  ROADMAP Success Criteria passed. Prose-fix commits then minted new false clauses at a measured
  2-of-3 rate, feeding the loop.
- **No stop rule exists anywhere in the pair.** 103.6 and 103.68 each ran 4 review rounds; the
  only cap ever applied ("R5 is FINAL", phase 105) was the owner improvising one mid-flight.
- **Scale of the cost:** August ran 2–3M output tokens/day on this project; review+adjudication
  cadence (plan-review + code-review + close-review × models × rounds through 103.65–103.69) was a
  major component. Meanwhile src-touching commits fell 3–6× vs July.

The conclusion the owner accepted: **keep the pair, demote the ceremony to an opt-in deep tier.**
The craft in these skills is failure-bought and real (see §2) — the problem is that the maximal
protocol is the only protocol.

## 2. What must NOT be lost (the failure-bought core)

Preserve these behaviours in every tier — each encodes a real, dated failure:

- Read the actual work; never write a brief from memory; re-derive every count in-session
  (stale citations shipped in three briefs).
- Pin the audit range to immutable commit IDs, never a branch relation (the empty
  `main..HEAD` range of 2026-08-16).
- The evidence standard: Location · Mechanism · Trigger · Consequence · Status, with
  CONFIRMED-by-execution vs THEORETICAL kept distinct; forbid upholding a claim on the author's
  own comment/test-name/docstring.
- Declared operating envelope (read-only + the report file), report written as a file as the
  reviewer works, no ship/no-ship verdict, forced ranking by cost-of-leaving-unfixed.
- "Ground already walked" — prior findings with dispositions, so nothing is paid for twice.
- Adjudication: count-in = count-out (one row per finding; a dropped finding is the failure the
  skill exists to prevent); never dismiss a finding you just found ("pre-existing"/"out of scope"
  as dismissal wears good clothes); FIX LATER requires a durable backlog artifact.
- No-overwrite of briefs/reports/ledgers.

## 3. The changes

### 3a. Both skills: depth tiers

Add a `--deep` flag (or equivalent input). **Default = light.** The current full protocol becomes
the deep tier, recommended only for: a one-way door, a disputed high-severity finding, or a
reviewer/author disagreement worth arbitrating. State the tier choice in the hand-off so the
adjudicator knows what it received.

### 3b. Both skills: stop rule

After **two rounds** on the same target, the skill instructs: stop; unresolved residuals go to the
durable backlog; the owner closes. No third round without an explicit owner request in their own
words. (Mirrors the project-side policy; encode it here so it travels to other projects.)

### 3c. adversarial-review-prompt

1. **Retire §9–§10 residual doubts** to one sentence in the hand-off: "Author doubts are never
   corroboration; the adjudicator treats reviewer agreement with the brief as non-independent by
   default." Delete the SEEDED/UNSEEDED protocol, the chat-only channel, and the §10 doubts block.
   (Its own 4-round failure history is the warrant.)
2. **Re-aim §3 at behaviour.** Keep mining load-bearing claims — it is where confirmed defects
   came from — but add, verbatim or close: *"A claim whose falsity has no behavioural consequence
   (a comment, a docblock, a citation) is a NOTE for the report's appendix, never a ranked
   finding. Rank only findings whose consequence is a wrong number, a wrong file, a crash, or a
   gate that cannot fail."*
3. **Slim calibration in the light tier** to: result + expiry ("calibrated PASS until X" / "no
   record — findings count, silence covers nothing"). Digest recomputation, two-location
   precedence arbitration, and workload-gap arithmetic move to `--deep`.
4. Optional but recommended: trim the compaction-defensive restatement so the default path reads
   ≤ ~200 lines. The invariants block can point into sections instead of duplicating them.

### 3d. review-adjudication

1. **Light mode default:** for each finding — verify it (run something real; the §5 evidence
   standard holds), then one line: verdict + disposition. Fix blockers, backlog the rest, done.
   Keep count-in = count-out and the CNV list. Everything else moves to `--deep`: claim cards,
   pre-registered expectations, blind second-opinion subagents, the P/D/U/A/C auxiliary
   namespaces, per-write head-diff round proofs, echo-audit tallies.
2. **Owner questions are batched and bounded.** One hand-off block, plain terms (the owner has
   ruled on this twice), each question genuinely two-defensible-options; anything that has a
   sensible default takes the default with a one-line note instead of a question. The 31-ruling
   load of 103.69 is the anti-pattern.
3. **Refutation burden, light tier:** `COULD NOT DETERMINE` + the named settling check replaces
   the mandatory blind-subagent machinery. The full second-opinion protocol is `--deep`.

### 3e. What not to do while editing

Do not prove these edits with gate ceremonies — no falsification matrices, no collision censuses,
no token-stream proofs. That style is the disease this handoff treats. Edit, read the whole file
once, commit with a plain message. The done-check below is the whole acceptance.

## 4. Done when

- [ ] Both SKILL.md files have a light default and a `--deep` tier, stated in their invariants.
- [ ] Two-round stop rule present in both.
- [ ] prompt §9/§10 residual-doubts protocol replaced by the one-line rule.
- [ ] prompt §3 carries the behavioural-consequence sentence.
- [ ] Adjudication light mode ≈ verify + one-line rows + count-in=count-out + CNV; owner
      questions batched/bounded.
- [ ] Committed here; installed copy at `~/.claude/skills/` reconciled (mind its existing
      uncommitted drift) and synced.
- [ ] Calibration corpus (`calibration/` in this repo) and filed records
      (`.adversarial-review/calibration/` per project-root convention) untouched;
      https://github.com/Dzazaleo/adversarial-review-skills/tree/main/calibration stays the pointer.
