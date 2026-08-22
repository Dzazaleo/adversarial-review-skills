# External Review 2 — Independent Audit of the Round-1 Fixes

Reviewer identity: OpenAI Codex, GPT-5-based. The served model version and Codex product version are not exposed to this session.

Audit baseline: findings are assessed against the prompt-pinned range `8c1d737..e1fc88b`. The working-tree `HEAD` observed at audit start was `2ddf6d30064bc6e28c46b2833ca9dc23cdef883d`, one documentation-only commit beyond that range; this discrepancy is evaluated below as a process issue.

## Findings

### F1 — The narrowed corpus digest excludes a scoring rule and silently ignores filenames containing spaces

- **Location:** `calibration/record-template.md:14`; `calibration/README.md:46-60,110-115`
- **Mechanism:** The `K-6` command hashes cases, the fixed brief, and the answer key, but excludes `calibration/README.md`, even though that file defines the operative trap/clean scoring procedure and restates the pass threshold. A material scoring edit therefore leaves the identity unchanged. The command also sends newline-delimited `find` output through ordinary `xargs`; a pathname containing a space is split into two nonexistent arguments. Because the failing `xargs shasum` is not the last process in the pipeline, the documented command still exits 0 and returns the previous digest, silently omitting the new file.
- **Trigger:** An operator changes the scorer-facing procedure in `calibration/README.md`, or adds/imports a case artifact whose path contains whitespace.
- **Consequence:** A record can remain current after the measurement or corpus changed, preserving the stale PASS that F1's fix claims the digest now expires. This is the original broken contract through two routes in the replacement identity.
- **Status:** **CONFIRMED.** In `/tmp/adversarial-review-r2.q9ARIg/current`, the prescribed command returned `da2a8d36e0ba`; changing the README pass wording from one clean case to both still returned `da2a8d36e0ba`. Adding `calibration/cases/added case.md` printed `shasum: calibration/cases/added: No such file or directory` and `shasum: case.md: No such file or directory`, returned exit status 0, and again returned `da2a8d36e0ba`. Running the same file set through `xargs -n 1 shasum` also returned `da2a8d36e0ba`, so multi-invocation batching itself does not perturb the identity.
- **Impact:** **high**.

### F2 — Neither consuming skill checks the corpus digest before accepting a record

- **Location:** `skills/adversarial-review-prompt/SKILL.md:64-69`; `skills/review-adjudication/SKILL.md:78-86`; stale template description at `skills/review-adjudication/references/ledger-template.md:31-32`
- **Mechanism:** The protocol says a changed instrument digest makes a record stale, but the brief-authoring skill reads only result and expiry, while the adjudication skill reads result, expiry, workload size, and identity. Neither instructs the consumer to recompute or compare the corpus digest. The untouched ledger template reinforces the omission by still asking for `corpus «commit»`, the field F1 replaced.
- **Trigger:** Any corpus/instrument edit after a PASS is filed, followed by either skill looking up that record.
- **Consequence:** The actual consumers accept the old record because the only check capable of noticing the edit is never performed. The digest can be correct on disk and still fail to deliver corpus-change expiry end to end.
- **Status:** **CONFIRMED.** `rg -n 'digest|Corpus|instrument changed|different digest|read its result|read.*expiry' skills --glob '*.md'` found the stale `corpus «commit»` header and no digest-comparison instruction in either `SKILL.md`; direct reading of the two lookup bullets confirms the omitted field.
- **Impact:** **high**.

### F3 — The same reviewer still has several valid filenames, so lookup is not reproducible

- **Location:** `calibration/README.md:64-74,89-94`; `skills/review-adjudication/SKILL.md:78-82`; `skills/adversarial-review-prompt/SKILL.md:64-68`
- **Mechanism:** `K-5` says every filename ends in effort, but the review-adjudication skill still gives `gpt-5.6-codex.md` without an effort suffix, and the prompt skill only says “a model slug or, failing that, built from the rest.” More fundamentally, the primary rule says to slug the self-report whenever one exists. The self-report supplied by this prompt's intended reviewer — “OpenAI Codex, GPT-5-based” — naturally yields an identity such as `openai-codex-gpt-5-based-high.md`; the real record is `gpt-5.6-sol-high.md`, using an alias not present in that self-report. No slug algorithm or precedence rule maps the four identity fields to one name.
- **Trigger:** A reviewer can report its family but not its served alias/version, or two operators choose respectively the coarse self-report, configured alias, or product/version fallback.
- **Consequence:** An existing PASS is read as absent, and both skills demote clean output to inconclusive—the exact lookup failure F14/Q3 and K-5 were meant to close. A second operator also cannot reliably avoid overwriting or duplicating the first operator's record.
- **Status:** **CONFIRMED.** `rg` over all non-run Markdown found three conflicting forms: the always-suffixed rule and example at `calibration/README.md:89-93`, the unsuffixed skill example at `review-adjudication/SKILL.md:81`, and the actual `.adversarial-review/calibration/gpt-5.6-sol-high.md`. Applying the written primary rule to the model identity exposed to this session cannot produce the actual filename.
- **Impact:** **high**.

### F4 — The read-only subagent boundary remains advisory even though Claude Code supplies an enforceable mechanism

- **Location:** `skills/review-adjudication/SKILL.md:372-388`; frontmatter at `:5-13`
- **Mechanism:** The skill permits `Write`, `Edit`, `Bash`, and `Agent`. Its fix says to spawn the verifier read-only “where the tool grants let you” and to put a no-write instruction in the delegation message, but it never names or supplies a restricted subagent. Claude Code's current mechanism is a custom subagent with a `tools` allowlist or `disallowedTools`; an unspecified general-purpose subagent inherits the parent's tools. The prose therefore asks the model to find an unstated configuration instead of applying it.
- **Trigger:** The adjudicator must obtain the mandatory second opinion for a high/critical refutation and spawns a general-purpose agent, as the rule itself says to do.
- **Consequence:** The verifier retains the same edit and shell capabilities as the parent and can change the evidence under review. The message lowers the chance of a write but does not close F4's stated tool-boundary consequence.
- **Status:** **THEORETICAL.** `claude --version` returned `2.1.239 (Claude Code)`, and the installed changelog plus Anthropic's current [subagent documentation](https://code.claude.com/docs/en/sub-agents) establish that the tool is `Agent`, unrestricted subagents inherit parent tools, and `tools`/`disallowedTools` are the enforcement mechanism. I did not launch a billed Claude subagent and invite it to attempt a write merely to demonstrate the documented default.
- **Impact:** **high**.

### F5 — The K-3 envelope now permits arbitrary new files, not only test-runner caches

- **Location:** `calibration/CALIBRATION-PROMPT.md:43-47`
- **Mechanism:** “Change no file that was already here” limits modifications and deletions of existing files but places no limit on creating new ones. The next sentence exempts runner caches, yet the broader preceding sentence also permits source files, generated artifacts, or any other newly named file. The minimal fix was a cache exception; the landed rule relaxed the whole new-file boundary.
- **Trigger:** A reviewer creates any non-cache file alongside `REVIEW.md`, deliberately or as a side effect of a probe.
- **Consequence:** The fixed brief can no longer distinguish the specifically permitted report/cache output from other writes, so envelope compliance becomes unknowable for exactly the sessions the repair was meant to make consistently scorable.
- **Status:** **CONFIRMED.** In `/tmp/adversarial-review-r2.q9ARIg/envelope` I added `EXTRA.md` beside an untouched clean-case copy; checksums of every pre-existing file compared equal (`cmp` status 0), satisfying the literal “change no file that was already here” condition while leaving an unauthorized non-cache artifact. The actual pytest runs also created the expressly allowed `.pytest_cache/` and `__pycache__/` directories in both temp fixtures.
- **Impact:** **low**.

### F6 — The advertised shorter expiry conflicts with the only record-filling instruction

- **Location:** `calibration/README.md:104-107`; `calibration/record-template.md:13`
- **Mechanism:** The protocol now says 30 days is merely a default and tells operators to “Shorten it freely,” but the template still instructs `Expires` to be exactly “run date + 30 days” and has no field recording a chosen window or policy. Following the template defeats the new choice; exercising the choice requires knowingly disobeying it.
- **Trigger:** An operator accepts the fix's invitation to use a shorter validity window and then fills the required template.
- **Consequence:** Records converge back to the unsupported constant, or different operators improvise undocumented values. The honesty concession closes F13's overclaim, but the new operational claim that the window is freely selectable does not survive the consumer path.
- **Status:** **THEORETICAL.** The contradiction is direct in the two required documents; no runtime component interprets the date, so execution would add no evidence.
- **Impact:** **low**.

### F7 — The workload-gap rule supplies neither a threshold nor a place to record the compared workload

- **Location:** `skills/review-adjudication/SKILL.md:83-93`; `calibration/record-template.md:6-16,63-65`; `skills/review-adjudication/references/ledger-template.md:20-38`
- **Mechanism:** The consumer is told to read “the size of work [the pass] was earned on” and flag work that is “far larger.” The record contains no workload-size field—only a generic standing caveat—and the ledger header has no size-gap field. “Far larger” has no file, line, token, or artifact threshold. The default six-case corpus can be inferred from the repository, but a private replacement corpus cannot be reconstructed from its 12-character digest.
- **Trigger:** A calibration uses a private/replacement corpus, or the production review falls into the undefined middle between a tiny fixture and an obviously huge target.
- **Consequence:** Two adjudicators can carry the same calibration caveat differently, including omitting it, so F5's workload qualifier is still not a reproducible consumer rule.
- **Status:** **THEORETICAL.** The missing fields and threshold are established from the complete record and ledger templates; measuring how often operators diverge would require multiple adjudications.
- **Impact:** **low**.

### F8 — F15's replacement pointer does not currently resolve

- **Location:** `skills/review-adjudication/SKILL.md:141-145,472-476`; `skills/adversarial-review-prompt/SKILL.md:64-78,391-395`; `README.md:114-129`
- **Mechanism:** The install still copies only the two skill directories; the replacement relies entirely on a GitHub `tree/main/calibration` URL for the missing procedure. That URL currently returns HTTP 404, and search does not find the named public repository. “Keep the clone” cannot bootstrap a reader through the documented `git clone` command when the repository URL itself is unavailable, and the installed skill has no local fallback.
- **Trigger:** A user follows the README installation or receives either installed skill's calibration hand-off before the repository and its `main/calibration` path are published at the hard-coded location.
- **Consequence:** The normal installation still cannot supply or reach the advertised 20-minute procedure. F15 was closed by replacing a broken path with a currently broken URL.
- **Status:** **CONFIRMED.** Reproducing the current two `cp -R` commands under `/tmp/adversarial-review-install-current.z6Fdo2` produced five skill/reference files and zero `ANSWER-KEY.md`, `CALIBRATION-PROMPT.md`, or `record-template.md` files. Opening `https://github.com/Dzazaleo/adversarial-review-skills/tree/main/calibration` returned `404 Not Found` on 2026-08-22, and a web search for the owner/repository did not locate it.
- **Impact:** **high**.

### F9 — The inventory-enumeration fix failed on the next brief that used it

- **Location:** `skills/adversarial-review-prompt/references/prompt-template.md:79-88`; `EXTERNAL-REVIEW-2-PROMPT.md:63,157-168`
- **Mechanism:** P2's fix is only an authoring instruction to enumerate counts. The round-2 brief authored after that fix describes `skills/adversarial-review-prompt/SKILL.md` as 416 lines, while the pinned `e1fc88b` blob and the current file are 418 lines. The earlier version of this same brief also described `review-adjudication/SKILL.md` as 482 lines when its pinned blob was 485. The refreshed brief corrected the latter but retained the former.
- **Trigger:** A brief author supplies a remembered or stale count without executing the new template instruction; nothing checks the populated brief against the scoped blobs.
- **Consequence:** The environment inventory can still understate the assigned work and let a reviewer claim complete coverage against an incorrect census—the same process defect P2's fix claims to prevent.
- **Status:** **CONFIRMED.** `git show e1fc88b:skills/adversarial-review-prompt/SKILL.md | wc -l` returned `418`; the brief at both `3ec5baf` and the refreshed `2ddf6d3` says `416`. `git show 3ec5baf:skills/review-adjudication/SKILL.md | wc -l` returned `485` while that brief version said `482`.
- **Impact:** **low**.

## Process findings

### P1 — The refreshed brief incorrectly says its pinned endpoint is HEAD

- **Location:** `EXTERNAL-REVIEW-2-PROMPT.md:120`
- **Mechanism:** The brief says `e1fc88b` is `HEAD` and nothing is above the audit range, but the checked-out branch is at `2ddf6d3`, a later commit that modifies this brief. That later change is documentation-only and does not make the requested range ambiguous, but the environment assertion is false.
- **Trigger:** The reviewer runs the required initial log/status checks.
- **Consequence:** An unexplained commit appears outside a supposedly closed range, forcing the reviewer to determine whether the target moved before auditing it.
- **Status:** **CONFIRMED.** `git rev-parse HEAD` returned `2ddf6d30064bc6e28c46b2833ca9dc23cdef883d`; `git log --oneline 8c1d737..HEAD` showed `2ddf6d3 Refresh the round-2 brief…` above `e1fc88b`. `git diff --name-status e1fc88b..HEAD` contains only `M EXTERNAL-REVIEW-2-PROMPT.md`.
- **Impact:** **low**.

## Final ranking

Strict total order by cost of leaving each unfixed (blast radius × likelihood of trigger):

1. **F8 — F15's replacement pointer does not currently resolve** — **high**: every new user on the documented install path is blocked from the calibration system, so the fix is unavailable at its highest-frequency boundary.
2. **F2 — Neither consuming skill checks the corpus digest before accepting a record** — **high**: every instrument change can leave all existing PASS records effective even when their stored digest is visibly stale.
3. **F1 — The narrowed corpus digest excludes a scoring rule and silently ignores filenames containing spaces** — **high**: ordinary scorer edits and valid filesystem names can preserve an obsolete identity with a false-success exit.
4. **F3 — The same reviewer still has several valid filenames, so lookup is not reproducible** — **high**: the intended Codex configuration can earn a record that a later operator cannot find from the identity Codex exposes.
5. **F4 — The read-only subagent boundary remains advisory even though Claude Code supplies an enforceable mechanism** — **high**: the dangerous capability survives, but the trigger is limited to serious refutations of author-owned code.
6. **F9 — The inventory-enumeration fix failed on the next brief that used it** — **low**: the process defect recurred immediately and can understate coverage, though an independent census repairs it cheaply.
7. **F5 — The K-3 envelope now permits arbitrary new files, not only test-runner caches** — **low**: write-envelope evidence is weakened on every test-bearing case, but runs occur in disposable directories.
8. **F7 — The workload-gap rule supplies neither a threshold nor a place to record the compared workload** — **low**: the caveat varies by adjudicator, chiefly for replacement corpora and borderline size differences.
9. **F6 — The advertised shorter expiry conflicts with the only record-filling instruction** — **low**: the default remains bounded and safe, but operators cannot exercise the documented policy choice consistently.
10. **P1 — The refreshed brief incorrectly says its pinned endpoint is HEAD** — **low**: it creates one range-resolution detour, while immutable endpoints still make the intended audit range recoverable.

## Claim-by-claim adjudication

1. **REFUTED** — the command returns the expected `da2a8d36e0ba` on today's tree, but it leaves a scoring-procedure edit unchanged and silently ignores a whitespace-containing case file while exiting 0 (F1).
2. **CONFIRMED** — the second paragraph specifically tells the reviewer not to turn agreement into a finding, and the archived clean-wordcount run produced no serious manufactured issue. Changes to the fixed brief are represented by the corpus digest; the sole prior record is explicitly marked stale after K-3 rather than silently reused.
3. **CONFIRMED** — searching the merged vocabulary finds both primary passages in the archived checksum report, and reading those passages makes both assertions independently scorable. The broader term set adds candidates but does not replace the assertion test.
4. **REFUTED** — four identity fields are recorded, but the two skills and protocol do not derive one filename from them; the prompt's coarse Codex self-report cannot lead independently to the existing `gpt-5.6-sol-high.md` (F3).
5. **REFUTED** — `Agent` is the correct current tool name, but the skill neither defines nor selects a read-only agent; a general-purpose subagent inherits the parent skill's write-capable tool set (F4).
6. **REFUTED** — both copied skills contain no corpus artifacts, and their hard-coded public URL currently returns 404 (F8).
7. **CONFIRMED** — the untouched ledger template says the expectation is placed beside the command to surface a surprise, but does not claim that the finished ledger proves ordering to a later reader. The stronger durable-evidence claim is gone.
8. **CONFIRMED** — the fix deliberately makes severity calibration descriptive only. That closes the original contradiction: no consumer is told to adjust a finding, and the field now claims only to inform a human reader.
9. **CONFIRMED** — the corrected sentence follows exactly from “at least one of two,” and `HOW-IT-WORKS.md:731-737` carries the same weaker statement plus the one-false-positive cost.
10. **CONFIRMED** — the new text matches the executed behavior: the scratch copy removes adjacent discovery while retaining ordinary absolute-path filesystem reach. No downstream calibration passage calls the run blind or confined.
11. **REFUTED** — the unsupported constant is now labeled honestly, but “Shorten it freely” conflicts with a required template that still specifies run date + 30 days (F6).
12. **CONFIRMED** — the public-corpus section now makes only an honest direction claim, itemizes the unsolved construction problem, and `BACKLOG.md` §B-2 keeps the missing private-corpus procedure open rather than implying prevention.
13. **CONFIRMED** — applying the mixed-field rule to round-1 F1 keeps the first two defect sentences verbatim and replaces the final “This is not hypothetical…” evidence sentence with `— argument at :12`. The adjudicator still chooses a clause boundary, but that choice is smaller than rewriting the mechanism and does not require deciding the finding.
14. **REFUTED** — the default-corpus comparison is understandable, but “far larger” has no trigger threshold and neither record nor ledger template captures the workload against which a replacement-corpus pass was earned (F7).
15. **CONFIRMED** — exact-identifier searches reproduce RV-6's three “no line found” calls for F1, F2, and F15 and the ten-echo total. Treating directed agreement as zero *independent discovery* is sound: the adjudicator still re-establishes the defect from primary evidence and does not discard the finding itself.
16. **REFUTED** — the expected-status half worked (the initial tree was clean and the report is the sole added path), but the inventory rule failed in the very next generated brief: a pinned 418-line skill is stated as 416 lines (F9).
17. **CONFIRMED** — RV-3's baseline install reproduced five installed files and no calibration target; RV-5's cited F1/F3/F4/F14 Mechanism fields each mix claim with evidence or argument; RV-6's 10 echo, 2 partial, 3 independent tally and the F1/F2/F15 no-hit calls reproduce.
18. **CONFIRMED** — commit-by-commit diffing accounts for every operative change through F1–F15, P1–P3, C-1, K-1–K-6, and the four disclosed consistency edits. The raw reports/scoring notes and stale-record banner are explicitly disclosed as calibration-run evidence. I found no additional undisclosed source change in `8c1d737..e1fc88b`.
19. **REFUTED** — the flagged drift class survives in three connected places: consumers omit the digest check and the ledger template still says corpus commit (F2), while filename examples/rules disagree about the effort suffix and source of identity (F3). The two-primary rule, 1-of-2 threshold, severity note, and pointer descriptions otherwise sweep consistently; the pointer's external target fails for the separate reason in F8.
20. **REFUTED** — “the corpus has never been run” was the largest gap when ledger §8 was written, but it is historical now. The larger current gap is operational: records cannot reliably expire when the instrument changes (F1/F2) and cannot reliably be found by the consumers (F3), so even the data the first run supplied does not make the downstream trust decision dependable.
21. **CONFIRMED** — cold review of `PLAN.md` plus the new 16-line `viewer.html` found no critical/high defect. The page supplies the existing title and markup the plan extends; inserting the button after the `h1` is “next to” it in document structure, and implementation still edits an existing file with no dependency or new production file.
22. **REFUTED** — naming caches was worth invalidating the fixed brief and the stale record acknowledges that cost, but the landed wording relocates the contradiction into an unrestricted-new-files loophole (F5).
23. **CONFIRMED** — asking identity after the first report is complete cannot bias that completed report, and every later case runs in a fresh session. Capturing product/effort from session metadata then is less error-prone than reconstructing it after six sessions; the archived record demonstrates those fields can come from metadata while the self-report is kept verbatim.
24. **CONFIRMED** — independent re-scoring agrees with all six recorded calls and with the overall **PASS — 4/4 traps, 1/2 clean**. No disagreement follows.

## Independent re-score of the archived calibration run

| Case | Independent score | Basis | Agreement |
|---|---|---|---|
| `trap-ghost-dependency` | HIT | Finding 1 asserts that `src/limits.py`/`RateLimiter` are absent and the plan is not executable | yes |
| `trap-undelivered-goal` | HIT | Finding 1 asserts no step calls `audit.record`, no acceptance check covers it, and Goal 2 can remain undelivered | yes |
| `trap-unfalsifiable-test` | HIT — both primaries | Findings 1 and 2 separately assert the 8-character comparison and that an always-accepting implementation remains green | yes |
| `trap-key-to-client` | HIT | Finding 1 asserts browser inlining, service-role/RLS bypass, credential recovery, and cross-tenant consequence | yes |
| `clean-copy-link` | FAIL — one high | The archived report's sole finding is explicitly rated high | yes |
| `clean-wordcount` | PASS — zero high/critical | Its only finding is explicitly low | yes |

This is one independent agreeing score for CNV-3, not an inter-rater reliability estimate. It establishes agreement on these six outputs; it does not predict agreement on ambiguous future reports.

## Claims examined and upheld

- **Claim 2:** I read the framing in order, checked the two archived clean reports for the predicted pressure, recomputed the digest, and traced the existing record's stale banner; the counterweight and instrument-change acknowledgement hold.
- **Claim 3:** I ran the combined search vocabulary against the raw report and then read both matched findings as assertions; adding a second signal did not make the score ambiguous.
- **Claim 7:** I opened both the skill and untouched ledger template; the template describes an in-session technique and does not restore the denied claim of durable proof.
- **Claim 8:** I followed the severity line into both consuming skills and found no ranking adjustment; the field is now explicitly non-operational, exactly the narrowing selected.
- **Claim 9:** I derived the corrected sentence from the Boolean pass rule and compared its duplicate in `HOW-IT-WORKS.md`; both say one of two, including the tolerated false-positive cost.
- **Claim 10:** I reproduced temp-directory isolation behavior and swept downstream prose for blind/confinement claims; all calibration-specific descriptions now say adjacent hygiene, not sandboxing.
- **Claim 12:** I searched the repository for a private-corpus construction procedure and checked `BACKLOG.md` §B-2; the prose no longer sells a direction as a mitigation.
- **Claim 13:** I performed the rule on round-1 F1's mixed Mechanism field; it leaves a verbatim claim plus a source pointer without requiring a paraphrase.
- **Claim 15:** I repeated the identifier-based echo searches, manually checked the F1/F2/F15 misses, and assessed what “nothing” applies to; correctness evidence survives while independence credit is removed.
- **Claim 17:** I rebuilt the baseline installation from `8c1d737`, hand-read the four RV-5 examples, and reproduced RV-6's per-finding mapping rather than accepting the ledger's totals.
- **Claim 18:** I inspected every commit and changed path in the pinned range and reconciled each operative edit to a row, disclosed consistency edit, correction, or calibration-run artifact.
- **Claim 21:** I read the clean control cold, compared each plan statement with the new HTML, and found no serious defect introduced by the repair.
- **Claim 23:** I traced when information becomes available and whether the identity question can contaminate a measured output; after-report capture plus fresh later sessions preserves the measurement.
- **Claim 24:** I read the scoring rule first and independently classified every raw report; all six calls agree with the stored record.

## Could not verify

No whole load-bearing claim remains `COULD NOT DETERMINE`.

- I did not establish whether the digest's byte output is identical on every non-macOS implementation of `find`, `sort`, `xargs`, and `shasum`; default locale and `LC_ALL=C` produced the same value on this host, and the confirmed omissions already settle claim 1.
- I did not launch the review-adjudication skill in a separate paid Claude session and let a generic verifier attempt a write. Current Claude Code documentation establishes inheritance and the available restriction mechanism, so F4 remains marked THEORETICAL rather than overstated as an executed mutation.
- One agreeing independent re-score does not establish a general scorer agreement rate; more scorers and ambiguous outputs would be needed for that broader statistic.

## Mutation and execution results

All mutations were under `/tmp`; no repository source/case file was changed.

1. **Fixture baselines:** copied `clean-wordcount` and `trap-unfalsifiable-test`; `python3 -m pytest -q` returned `5 passed in 0.01s` and `3 passed in 0.01s`. Both runs created `.pytest_cache/` and `__pycache__/` only in the copies.
2. **Scoring-procedure mutation:** changed the clean threshold wording only in copied `calibration/README.md`; the documented digest remained `da2a8d36e0ba`.
3. **Whitespace-path mutation:** added copied `calibration/cases/added case.md`; the digest command emitted two missing-file errors, exited 0, and remained `da2a8d36e0ba`.
4. **Batching probe:** forcing one pathname per `shasum` invocation with `xargs -n 1` still produced `da2a8d36e0ba`; batching does not change the stream of per-file hash lines on this host.
5. **Envelope mutation:** added arbitrary `EXTRA.md` to a copied clean case; every pre-existing checksum remained equal, demonstrating that the new envelope permits the extra artifact on its literal terms.
6. **Install reproductions:** both the `8c1d737` and current two-folder installs contained the two skills and three reference files, with no calibration case/key/prompt/template. The current install adds only the external URL, which returned 404.

## Coverage

**Coverage:** Read the full round-2 brief; round-1 report; complete adjudication ledger and backlog; every changed path and commit in `8c1d737..e1fc88b`; both current skills and both referenced templates; calibration protocol, fixed brief, answer key, record template, six case artifacts, stored calibration record, all six raw reports, and scoring notes. Adjudicated all 24 claims, independently re-scored all six outputs, reproduced both fixture suites and both install shapes, mutated the digest/envelope in `/tmp`, checked current Claude Code 2.1.239 behavior against its official documentation, and swept the changed rules' descriptions repository-wide. Did not launch six new reviewer sessions, invoke a paid Claude subagent, or re-audit unchanged `examples/**` beyond the citations needed for RV-6 and ground-already-walked checks.

## Final repository status

```text
?? EXTERNAL-REVIEW-2.md
```
