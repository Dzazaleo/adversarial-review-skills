I maintain a small open-source repository of two Claude Code "skills" — structured markdown
instruction files that a coding agent loads and follows. One writes adversarial review prompts to
hand to a different AI model; the other adjudicates the reviews that come back. It is published
CC0 on GitHub, it is unreleased in any product sense, and I own it entirely. Nothing here is a
production system and there is no user data anywhere near it.

You reviewed this repository yesterday, unscoped, and returned eleven findings. I adjudicated all
eleven and applied ten fixes. **This round is a patch verification: I want you to attack the
fixes, not re-find the findings.** Several of them are the kind where adding a sentence that says
the problem is handled can look identical to handling it, and I would rather know now than
believe it.

**One thing before you start.** A different model is auditing the same range in parallel. Its
brief, cover note and report sit in the repository root as `EXTERNAL-REVIEW-4-PROMPT-GROK.md`,
`EXTERNAL-REVIEW-4-COVER-NOTE-GROK.md` and `EXTERNAL-REVIEW-4-GROK.md`. **Please don't open
those three.** Two reports agreeing only means something if the second couldn't read the first,
and nothing technically stops you — I'm asking rather than enforcing. If you do end up seeing
one, just say so in your report; that's still useful, whereas quietly reading it isn't.

The full brief is on disk. Please read it first — it pins the audit range, lists 22 load-bearing
claims to adjudicate, and states exactly what you may and may not touch:

**`EXTERNAL-REVIEW-4-PROMPT.md`** (repository root)

Two things about how to deliver it:

1. **Write your report to `EXTERNAL-REVIEW-4.md` in the repository root, creating it early and
   appending as you go** — not held in memory until the end, and not returned as a chat message.
   If the run gets cut short I would rather have half a report on disk than none.
2. **Return only a short summary in this chat** — your coverage line, the ranked finding titles
   with impact levels, and the file path. All the detail belongs in the file.

You may read anything in the repository, run its two-fixture pytest suite, and do whatever you
like under `/tmp`. Please modify nothing else in the repository. Web search is allowed and
genuinely useful here — several claims turn on what Claude Code's `allowed-tools`,
`disallowed-tools` and auto-compaction actually do, and I would rather you check the current docs
than take my word for it. Cite the URL where you do.

Please don't give me a ship/no-ship verdict — rank the findings by what it would cost to leave
each one unfixed instead. And if any two instructions in the brief contradict each other, report
that as a process finding; previous rounds have found good ones.
