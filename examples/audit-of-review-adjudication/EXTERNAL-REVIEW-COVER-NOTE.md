```text
Context: this is a pre-use correctness review of my own work — a Claude Code "skill",
which is just a markdown instruction file that my AI coding assistant loads and follows
when a task matches it. Nothing runs on a server, there's no network service and no
users but me; it's two prose files sitting in my home directory that shape how an
assistant writes a document. I own all of it, it was written today and has never been
used once, and I'm reviewing it before I start relying on it. The defects I care about
are the ones that would let a real review finding get quietly lost, wrongly dismissed,
or recorded as something it isn't.

Please read and execute the audit brief at:

  ~/.claude/skills/review-adjudication/EXTERNAL-REVIEW-PROMPT.md

Two things about how to deliver it, which the brief also states:

1. WRITE YOUR REPORT TO A FILE as you go:
   ~/.claude/skills/review-adjudication/EXTERNAL-REVIEW-FABLE.md
   Create it early, append each finding as you confirm it, and finish with a pass that
   sets the final ranking and the coverage line. Do not hold the report only in memory —
   a previous review of the sibling skill was told to return its report in chat, the
   message never reached me, and because nothing was on disk the whole audit was lost.
   Writing that one file is authorized. Everything else stays read-only: do not modify
   either skill file, and do not touch anything in the corpus project.
   Commit nothing.

2. In your reply here, give me only a short summary: your coverage line, the ranked
   finding titles with impact levels, and the file path. Keep all detail in the file.

Two host notes so neither reads as a finding. The brief sends you into
~/projects/corpus-project/.planning/ to check the skill
against real documents there — that project has an uncommitted working tree and another
review is actively running inside it, so read it but run no git command that changes
state. And the brief is long; open it from disk rather than asking me to paste it.
```
