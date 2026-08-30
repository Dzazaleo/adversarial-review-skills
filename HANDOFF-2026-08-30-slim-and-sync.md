# Handoff: slim the deep tier out of the SKILL.md files, and commit the installed copy

**Date:** 2026-08-30 · **Requested by:** Leo · **Follows:** `HANDOFF-2026-08-30-proportionality.md`,
implemented in commit `3b448b9`. That implementation was verified aligned; these are the two gaps
it deliberately left open. Self-contained — no prior transcript needed.

---

## Gap A — the tier split saves execution, not context. Move `[deep]` into references.

**Why.** `3b448b9` implemented the light/deep tiers by annotating passages `[deep]` inside the
SKILL.md files. That fixes the *work* (light runs skip the machinery) but not the *load*: a skill's
SKILL.md is injected whole into the session on every invocation, and the files barely shrank
(prompt 519→504 lines, adjudication 513→508). References, by contrast, load only when opened —
and a light-tier run never opens the deep material. Moving `[deep]` bodies into a reference file
makes the default invocation pay only for the default protocol.

**What to do.**

1. Per skill, create `references/deep-tier.md`. Enumerate the `[deep]` sites first
   (`grep -n '\[deep\]' skills/*/SKILL.md skills/*/references/*.md`). As of `3b448b9`:
   adjudication SKILL.md has **13** (the heavy bodies: claim cards in §2, pre-registration and the
   echo probe and upheld-list sampling in §5, the blind second opinion in §5, the aux ID
   namespaces in §2, the append-proof in §7, per-namespace header counts in §7); the prompt
   SKILL.md has **3** (calibration digest/arbitration/workload in §1 — small).
2. **Move, never rewrite.** Each multi-sentence `[deep]` body relocates verbatim to
   `deep-tier.md`; the SKILL.md keeps a one-line stub in place:
   `**[deep]** <topic> — references/deep-tier.md §N.` The invariants blocks keep their tier
   statement as-is (it is the contract; only the bodies move).
3. Keep section numbers stable — cross-references are load-bearing across the pair (prompt §3 ↔
   template §6b; adjudication §5 ↔ verification-standard; the two skills cite each other's §
   numbers). Move content out of sections, do not remove sections.
4. Update the compaction preambles after the move: both files open with "treat everything past
   line ~205/~195 as gone" — recompute those estimates for the new lengths, since that is the one
   number in each file that depends on the file's own size.
5. Realistic targets, not quotas: adjudication SKILL.md ≤ ~350 lines (it holds nearly all the
   deep bodies); the prompt SKILL.md will land ~480 and that is fine — its remaining length is
   light-path craft, and cutting craft to hit a number is exactly what
   `HANDOFF-2026-08-30-proportionality.md` §3e forbids.
6. `scripts/validate.py` — check what it validates before and after; if it parses SKILL.md
   structure, run it once at the end.

**Done when:** every `[deep]` marker in a SKILL.md is a one-line stub pointing into
`deep-tier.md`; a diff shows the moved bodies arriving there verbatim (allowing pronoun/joining
edits only); light-tier behaviour is unchanged on a single full read of each file; compaction
line-estimates updated; then Gap B step 3 (re-sync + commit) runs again for this change.

## Gap B — the installed copy is synced but uncommitted, on top of two unrelated drifts

**Why.** `~/.claude/skills/` is its own **local-only** git repo (standing rule: commit skill
edits there; **never add a remote to it**). Right now `git status` in it shows three unrelated
change families sitting uncommitted together, which is exactly how an accidental
sweep-commit or a botched sync loses history:

1. **The pair sync from `3b448b9`** — modified `adversarial-review-prompt/SKILL.md` + 2 templates,
   `review-adjudication/SKILL.md` + `ledger-template.md`, plus **5 untracked new references**
   (`why-this-is-hard.md` ×2, `inputs-and-calibration.md`, `second-opinion.md`,
   `verification-standard.md`). All verified byte-identical to this repo at `3b448b9`.
2. **11 deleted review artifacts** (EXTERNAL-REVIEW*/PATCH-VERIFICATION*/REVIEW-ADJUDICATION.md
   under both skill dirs). **All 11 verified present in this repo** — at its root or under
   `examples/audit-of-*/` — so the deletions are duplicate-cleanup after the artifacts were
   relocated here. Safe to commit; nothing is lost.
3. **~60 modified `gsd-*/SKILL.md` files** — the gsd-core 1.11.0 in-place update of 2026-08-26,
   nothing to do with this pair.

**What to do, in `~/.claude/skills/` (local commits only — no remote, ever):**

1. Commit family 3 alone: `git add gsd-*/ && git commit` — message names the gsd-core 1.11.0
   update of 2026-08-26 as the source.
2. Commit families 1+2 together: add the two skill dirs (modifications, the 5 new references,
   and the 11 deletions) and commit with a message citing authoring commit `3b448b9`
   ("mirror of adversarial-review-skills 3b448b9; deleted artifacts relocated to that repo").
3. After Gap A lands here: re-copy `skills/adversarial-review-prompt` and
   `skills/review-adjudication` over the installed dirs (the installed repo flattens the
   `skills/` prefix), verify with `diff -rq`, and commit again citing the Gap A commit.
4. There is no sync script and none is wanted (`scripts/` holds only `validate.py`); instead add
   a three-line "Installing / syncing" note to this repo's README naming the copy direction
   (this repo → `~/.claude/skills/`, prefix flattened) and the diff -rq check.

**Done when:** `git status` in `~/.claude/skills/` is clean; its log shows the three concerns as
separate commits; README here carries the sync note.

## What not to do (unchanged from the previous handoff)

No gate ceremonies to prove these edits — no falsification matrices, no censuses. Edit, read each
touched file once whole, commit with a plain message. Don't touch `calibration/`. Pushing this
repo to its GitHub origin is the owner's call, never done as part of this work.
