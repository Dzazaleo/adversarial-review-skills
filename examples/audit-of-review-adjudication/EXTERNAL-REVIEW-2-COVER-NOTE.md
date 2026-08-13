Context: this is a second-round correctness review of a document I own and wrote — a "skill" file
for my own AI coding assistant, running locally on my machine. It is not software, not published,
not networked, and has no users but me: it is a page of prose instructions that another model reads
and follows when a code review comes back, telling it how to rule on each finding and write the
results into a record file. It was audited once already, and every fix from that audit was written
by the same model family that wrote the original — so what I actually need checked is whether those
fixes work, not whether they exist. The defects I care about are the ones where a real problem in a
review ends up with no ruling and quietly disappears, or where the record file ends up saying
something that is not true.

Please read and execute the audit brief at:

  ~/.claude/skills/review-adjudication/EXTERNAL-REVIEW-2-PROMPT.md

Two things about how to deliver it, which the brief also states:

1. WRITE YOUR REPORT TO A FILE as you go:
   ~/.claude/skills/review-adjudication/EXTERNAL-REVIEW-2.md
   Create it early, append each finding as you confirm it, and finish with a pass that sets the
   final ranking and the coverage line. Do not hold the report only in memory — if the session is
   cut short, anything not on disk is gone, and this is a long brief. Start a new file; do not
   append to EXTERNAL-REVIEW-FABLE.md, which is the first round's report and is history. Writing
   that one file is authorized. Everything else — both files under review, the sibling skill at
   ~/.claude/skills/adversarial-review-prompt/, and everything under
   ~/projects/corpus-project/ — stays read-only, and commit nothing.

2. In your reply here, give me only a short summary: your coverage line, the ranked finding titles
   with impact levels, and the file path. Keep all detail in the file.

Two things about this machine that would otherwise look like findings. First, ~/.claude/
is not a git repository, so `git status` there fails — that is expected and is itself one of the
things the brief asks about, not a broken setup. Second, the corpus project has an
uncommitted working tree with untracked files in it; read it freely but do not run any git command
that changes state there.
