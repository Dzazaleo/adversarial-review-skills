**This note is for Codex (GPT-5.6), and its brief is `EXTERNAL-REVIEW-7-PROMPT-CODEX.md`.** If you
are a different model, or that file is not the one you were pointed at, stop and say so — a note
pasted into the wrong session is how an earlier round was lost.

I maintain a small open-source repository of two Claude Code "skills" — structured markdown
instruction files that a coding agent loads and follows. One writes adversarial review prompts to
hand to a different AI model; the other adjudicates the reviews that come back. It is published CC0
on GitHub, it is unreleased in any product sense, and I own it entirely. Nothing here is a
production system and there is no user data anywhere near it.

You reviewed half of this repository once before, in round 5. **This time you are getting the one
executable: `scripts/validate.py`.**

**Three things you should know before you start, because they change what to suspect.**

1. **That file went from 354 lines to 519 in the range you are auditing**, and every one of those
   changes was written by a Claude session responding to an external review — which then ran its own
   mutation suite against the result, reported 29 of 29 probes correct, and wrote the ledger saying
   so. **Treat that as a claim, not a result.**

2. **Two bugs in those changes were already found by running them**, and both are parsing bugs in
   markdown-table handling that survived the author's own review of its own code. The brief names
   them. They tell you the shape of what to hunt.

3. **The previous round found four checks that were silent on the invariant they were named for and
   two that fired on correct work.** Those are fixed. The interesting question is what the next four
   are.

The full brief is on disk. Read it first — it pins the audit range, lists 20 load-bearing claims,
and states exactly what you may and may not touch:

**`EXTERNAL-REVIEW-7-PROMPT-CODEX.md`** (repository root)

How to deliver it:

1. **Write your report to `EXTERNAL-REVIEW-7-CODEX.md` in the repository root, creating it early
   and appending as you go** — not held in memory until the end. If the run gets cut short I would
   rather have half a report on disk than none. **That path is yours alone and is currently empty**;
   do not write to any other report file, whatever it is called.
2. **Return only a short summary at the end** — your coverage line, the ranked finding titles with
   impact levels, and the file path.

You may read anything in the repository, run read-only commands in it, and **do anything you like
under `/tmp` — including copying the whole repository there and mutating it freely**, which is how
I would like the validator tested. Please modify nothing else in the repository itself. **Network:
web search is allowed — cite the URLs for anything you source that way. No installs.**

Two gotchas. The pytest fixtures under `calibration/cases/` write `__pycache__` if run in-tree —
copy to `/tmp` first. And the repository currently prints two `WARN disposition` lines about
`REVIEW-ADJUDICATION.md:2383` and `:2384`; those are deliberate, permanent history, and are not
defects to report.

**There is a second reviewer this round**, working on the prose half — the skills and the ledger —
from a different brief. You are not reading its brief and it is not reading yours. Nothing is
withheld from you.

Please don't give me a ship/no-ship verdict — rank the findings by what it would cost to leave each
one unfixed instead. And if any two instructions in the brief contradict each other, report that as
a process finding; every round so far has found good ones.
