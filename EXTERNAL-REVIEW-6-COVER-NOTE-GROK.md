**This note is for Grok 4.6, and its brief is `EXTERNAL-REVIEW-6-PROMPT-GROK.md`.** If you are a
different model, or that file is not the one you were pointed at, stop and say so — a note pasted
into the wrong session is how the previous round was lost.

I maintain a small open-source repository of two Claude Code "skills" — structured markdown
instruction files that a coding agent loads and follows. One writes adversarial review prompts to
hand to a different AI model; the other adjudicates the reviews that come back. It is published
CC0 on GitHub, it is unreleased in any product sense, and I own it entirely. Nothing here is a
production system and there is no user data anywhere near it.

You have reviewed this repository once before and returned 13 findings, 12 confirmed. You then
passed the calibration corpus 4/4 on traps and 2/2 on clean cases. **The reason you are getting
this particular half is that you mutation-tested on both a trap and a clean case** — you broke a
suite to convict, and broke one to acquit. That is exactly the capability this half needs.

**Three things you should know before you start, because they change what to suspect.**

1. **This half has never been audited by anyone.** Five rounds have run here and every one was
   pointed at the skills' prose. A brief for this half was written last round and never delivered —
   the wrong cover note was pasted into the reviewing session, so it read the wrong brief and
   audited the wrong half. That is my error, not the reviewer's, and it is why the first line of
   this note now says which brief it belongs to.

2. **The most recent commit was written by the session that adjudicated the last round.** It ruled
   on 22 findings, authorized itself against its own fix queue, applied nineteen fixes, extended
   the validator you are auditing, and then used that validator to certify its own work. It
   reported the validator catching one of its own regressions and offered that as evidence the
   validator earns its place. **Treat that as a claim, not a result.**

3. **The ledger asserts the validator was break-tested 9/9.** That is me testing my own harness,
   and it covered ten checks — there are now twelve, and the two new ones were never
   break-tested at all. **Please redo the whole thing and tell me what stays silent.**

The full brief is on disk. Read it first — it pins the audit range, lists 20 load-bearing claims,
and states exactly what you may and may not touch:

**`EXTERNAL-REVIEW-6-PROMPT-GROK.md`** (repository root)

How to deliver it:

1. **Write your report to `EXTERNAL-REVIEW-6-GROK.md` in the repository root, creating it early
   and appending as you go** — not held in memory until the end. If the run gets cut short I would
   rather have half a report on disk than none. **That path is yours alone and is currently
   empty**; do not write to any other report file, whatever it is called.
2. **Return only a short summary at the end** — your coverage line, the ranked finding titles with
   impact levels, and the file path.

You may read anything in the repository, run read-only commands in it, and **do anything you like
under `/tmp` — including copying the whole repository there and mutating it freely**, which is how
I would like the validator tested. Please modify nothing else in the repository itself. One
gotcha: the two-fixture pytest suite writes `__pycache__` into the corpus if run in-tree, which is
itself the subject of one of the claims — copy it to `/tmp` first.

There is no parallel reviewer this time and nothing is withheld from you.

Please don't give me a ship/no-ship verdict — rank the findings by what it would cost to leave each
one unfixed instead. And if any two instructions in the brief contradict each other, report that as
a process finding; you found one last time.
