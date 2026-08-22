I maintain a small open-source repository of two Claude Code "skills" — structured markdown
instruction files that a coding agent loads and follows. One writes adversarial review prompts to
hand to a different AI model; the other adjudicates the reviews that come back. It is published
CC0 on GitHub, it is unreleased in any product sense, and I own it entirely. Nothing here is a
production system and there is no user data anywhere near it.

You reviewed this repository two days running and returned 14 findings last time. I adjudicated
all 27 findings from that round across two reviewers, applied 24 fixes, and then restructured both
skills — moving about 9,000 characters of prose into new reference files to get them under a
documented length limit. **This round is a patch verification, and I want you to attack the
restructure hardest.**

Here is why, and it is the most useful thing I can tell you. After those 24 fixes were applied, a
separate run found two defects that had survived all of them. One was text the restructure had
*moved into a reference file unchanged* — a defect relocated rather than repaired, by the same
session that was doing the repairing. Then, while writing this brief, I found a third of the same
shape. **Fixes that reach one site of something living at several are this project's recurring
failure**, and the restructure was a large opportunity to make more of them.

**Two things before you start.**

A different model is auditing a **different half** of the same range in parallel. Its brief and
report are `EXTERNAL-REVIEW-5-PROMPT-GROK.md` and `EXTERNAL-REVIEW-5-GROK.md`. **Please don't
open those two.** It has the validator, the ledger and the calibration corpus; you have the two
skills and their references. Two reports agreeing only means something if the second couldn't read
the first, and nothing technically stops you — I'm asking rather than enforcing. If you do end up
seeing one, just say so in your report; that's still useful, whereas quietly reading it isn't.

Several claims turn on what Claude Code specifically does — how `allowed-tools` behaves, whether
`Edit(path)` rules govern the `Write` tool, how much of a skill survives auto-compaction. Please
answer those from Anthropic's published docs with the URL cited, or say you couldn't determine it.

The full brief is on disk. Please read it first — it pins the audit range, lists 18 load-bearing
claims, and states exactly what you may and may not touch:

**`EXTERNAL-REVIEW-5-PROMPT-CODEX.md`** (repository root)

Two things about how to deliver it:

1. **Write your report to `EXTERNAL-REVIEW-5-CODEX.md` in the repository root, creating it early
   and appending as you go** — not held in memory until the end, and not returned as a chat
   message. If the run gets cut short I would rather have half a report on disk than none.
2. **Return only a short summary in this chat** — your coverage line, the ranked finding titles
   with impact levels, and the file path. All the detail belongs in the file.

You may read anything in the repository except those two files, run read-only commands, and do
whatever you like under `/tmp`. Please modify nothing else in the repository. One gotcha: the
two-fixture pytest suite writes `__pycache__` into the corpus if you run it in-tree — copy the
fixtures to `/tmp` if you want them. Web search is allowed and genuinely useful here.

Please don't give me a ship/no-ship verdict — rank the findings by what it would cost to leave each
one unfixed instead. And if any two instructions in the brief contradict each other, report that as
a process finding; every previous round has found good ones.
