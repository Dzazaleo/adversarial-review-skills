I maintain a small open-source repository of two Claude Code "skills" — structured markdown
instruction files that a coding agent loads and follows. One writes adversarial review prompts to
hand to a different AI model; the other adjudicates the reviews that come back. It is published
CC0 on GitHub, it is unreleased in any product sense, and I own it entirely. Nothing here is a
production system and there is no user data anywhere near it.

You reviewed this repository once before and returned 13 findings; 12 were confirmed and one was
refuted from Anthropic's docs. You then passed the calibration corpus 4/4 on traps and 2/2 on clean
cases. **The reason you are getting this particular half is that you mutation-tested on both a trap
and a clean case** — you broke a suite to convict, and broke one to acquit. That is exactly the
capability this half needs.

Since your last review I applied 24 fixes, added an executable validator that claims to turn ten
prose invariants into checks that fail, and changed the calibration digest so a record stops
expiring whenever anyone runs the fixtures. **Those are mechanical claims and I want them tested
rather than argued about.** The ledger asserts the validator was break-tested 9/9. That is me
testing my own harness; please redo it and tell me what stays silent.

**Two things before you start.**

A different model is auditing a **different half** of the same range in parallel. Its brief and
report are `EXTERNAL-REVIEW-5-PROMPT-CODEX.md` and `EXTERNAL-REVIEW-5-CODEX.md`. **Please don't
open those two** — note they are the ones *with* `-CODEX` in the name; your own brief and report
are yours to use freely. It has the two skills' prose; you have the validator, the ledger and the
calibration corpus. Two reports agreeing only means something if the second couldn't read the
first. You disclosed exactly this situation last round unprompted, which was the right call — if
it happens again, just say so.

**You are being asked to audit your own calibration record.** `.adversarial-review/calibration/grok-4.6-high.md`
records how your six runs scored. That is not a conflict I want you to tiptoe around — it is a file
with claims in it, and if it overstates what your run established, or gets its caveat wrong in
either direction, that is a finding I want.

The full brief is on disk. Please read it first — it pins the audit range, lists 17 load-bearing
claims, and states exactly what you may and may not touch:

**`EXTERNAL-REVIEW-5-PROMPT-GROK.md`** (repository root)

How to deliver it:

1. **Write your report to `EXTERNAL-REVIEW-5-GROK.md` in the repository root, creating it early
   and appending as you go** — not held in memory until the end, and not returned as a chat
   message. If the run gets cut short I would rather have half a report on disk than none.
2. **Return only a short summary in this chat** — your coverage line, the ranked finding titles
   with impact levels, and the file path. All the detail belongs in the file.

You may read anything in the repository except those two files, run read-only commands in the repo,
and **do anything you like under `/tmp` — including copying the whole repository there and mutating
it freely**, which is how I would like the validator tested. Please modify nothing else in the
repository itself. One gotcha: the two-fixture pytest suite writes `__pycache__` into the corpus if
run in-tree, so copy it to `/tmp` first.

Please don't give me a ship/no-ship verdict — rank the findings by what it would cost to leave each
one unfixed instead. And if any two instructions in the brief contradict each other, report that as
a process finding; you found one last round.
