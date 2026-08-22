I maintain a small open-source repository of two Claude Code "skills" — structured markdown
instruction files that a coding agent loads and follows. One writes adversarial review prompts to
hand to a different AI model; the other adjudicates the reviews that come back. It is published
CC0 on GitHub, it is unreleased in any product sense, and I own it entirely. Nothing here is a
production system and there is no user data anywhere near it.

The repository has been through three review rounds and has just had ten fixes applied. **I want
you to attack those fixes.** Most of them are the kind where adding a sentence saying the problem
is handled looks identical to handling it, and I would rather find out now than believe it.

Two things you should know before you start, both of which are in the brief but matter enough to
say twice:

**A different model is auditing the same range in parallel.** Its three files sit in the
repository root: `EXTERNAL-REVIEW-4-PROMPT.md`, `EXTERNAL-REVIEW-4-COVER-NOTE.md` and
`EXTERNAL-REVIEW-4.md`. **Please don't open those three** — note they are the ones *without*
`-GROK` in the name; your own brief and report are yours to use freely. Two reports agreeing only means something if the second one couldn't read the
first, and nothing technically stops you — I'm asking rather than enforcing. If you do end up
seeing one, just say so in your report; that's still useful, whereas quietly reading it isn't.

**Several claims turn on what Claude Code specifically does** — how its `allowed-tools`
frontmatter behaves, whether `disallowed-tools` exists, how much of a skill survives
auto-compaction. Coding agents have converged on similar-looking skill formats and yours may
implement something that resembles it. Please answer those from Anthropic's published docs with
the URL cited, or say you couldn't determine it. A confident answer that turns out to describe
your own tooling rather than Claude Code is the one kind of wrong finding I'd have real trouble
catching.

The full brief is on disk. Please read it first — it pins the audit range, lists 24 load-bearing
claims to adjudicate, and states exactly what you may and may not touch:

**`EXTERNAL-REVIEW-4-PROMPT-GROK.md`** (repository root)

How to deliver it:

1. **Write your report to `EXTERNAL-REVIEW-4-GROK.md` in the repository root, creating it early
   and appending as you go** — not held in memory until the end, and not returned as a chat
   message. If the run gets cut short I would rather have half a report on disk than none.
2. **Return only a short summary in this chat** — your coverage line, the ranked finding titles
   with impact levels, and the file path. All the detail belongs in the file.

You may read anything in the repository apart from those three files, run its two-fixture pytest
suite, and do whatever you like under `/tmp`. Please modify nothing else in the repository. Web
search is allowed and genuinely useful here.

Please don't give me a ship/no-ship verdict — rank the findings by what it would cost to leave
each one unfixed instead. And if any two instructions in the brief contradict each other, report
that as a process finding; previous rounds have found good ones.
