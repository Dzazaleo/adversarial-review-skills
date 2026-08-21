Context: this is a pre-publication correctness review of my own work. The repo is a small
public-domain project of mine — two Claude Code skills that help get an AI's work audited by a
rival model and then sort the resulting complaints into real and not-real. I've just added a
"calibration" corpus: six small cases with defects planted in four of them, used to check
whether a reviewer model can actually find anything before I trust it saying a review came back
clean. I own the repo, none of this is committed or published yet, and I'm checking it before it
goes out. The defects I care about are the ones that would make that corpus measure the wrong
thing — a planted defect nobody could reasonably find, or a case I've labelled "clean" that
isn't — because that kind of mistake fails silently and would make every reviewer I test look
bad forever.

Please read and execute the audit brief at:

  EXTERNAL-REVIEW-PROMPT.md

Two things about how to deliver it, which the brief also states:

1. WRITE YOUR REPORT TO A FILE as you go:
   EXTERNAL-REVIEW.md
   Create it early, append each finding as you confirm it, and finish with a pass that sets the
   final ranking and the coverage line. Do not hold the report only in memory — an earlier round
   on this same repo was cut off partway, and everything that had already been written to disk
   still counted while everything held in the reply was lost. Writing that one file in the repo
   root is authorized.

   You may also copy the calibration cases into a temp directory and mutate them freely there —
   that is how you confirm the central claim about the checksum case rather than just reasoning
   about it. Everything inside the repository itself stays read-only: no edits to any file under
   calibration/, skills/, or examples/, not even edits you intend to revert, and commit nothing.
   Please finish by running `git status --short` and pasting the output so I can see the tree is
   as I left it.

2. In your reply here, give me only a short summary: your coverage line, the ranked finding
   titles with impact levels, and the file path. Keep all detail in the file.

Two host notes so they don't read as findings: Python is `python3` (3.14) and pytest is
available, but there is no test runner, linter or CI for the repository itself — that absence is
real and is in scope, not something you're failing to find. And the TypeScript case has no
package.json and no install; it's there to be read, not built.
