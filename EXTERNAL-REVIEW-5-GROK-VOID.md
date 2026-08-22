# Grok run at 0d65b51 — VOID as calibration, retained for two live findings

**What this is.** An unscoped review of the repository at `0d65b51`, produced by xAI Grok 4.6
(high effort) on 2026-08-22. It is filed here because it found two real defects, and for no other
reason.

**Why it is void as a calibration run.** The session was rooted at the full repository rather than
an isolated case directory, and it read `calibration/ANSWER-KEY.md` — which names every planted
defect in all six cases and where to look for each. It disclosed this in detail, unprompted, when
asked what it had opened. Nothing here measures detection; it measures reading. No partial credit
is available and the run is not scored. `calibration/README.md`'s isolation rule is explicit:
*"Never point it at `calibration/` itself, and never copy `ANSWER-KEY.md` alongside a case."*

**Why it is not a scoped review either.** It answered `CALIBRATION-PROMPT.md`, which is the fixed
calibration instrument, not a brief about this repository. There was no pinned range, no claims
list, no envelope written for this target, and no cover note. It also read every prior report
including both round-4 reports and the adjudication ledger, so nothing in it is independent of
work already on record.

**What became of its eight findings.** Six restate defects round 4 had already confirmed and that
were fixed in `9893aaa` before this run was read: the corpus digest, the leftover payoff sentence,
the overwrite guard's scope, uncollected author family, the `FIX LATER` ordering contradiction,
and the no-filesystem route's missing continuation step. Two were new, neither reviewer in round 4
having found them, and both were live at `bf092c9`:

- **Finding 7** — the calibration filename examples wrote `<identity>` as a finished, effort-
  suffixed filename (`gpt-5.6-sol-high.md`), teaching a lookup of `gpt-5.6-sol-high-high.md`. The
  round-4 restructure had *moved* this text into `references/inputs-and-calibration.md` unchanged
  rather than fixing it — a defect relocated, not repaired.
- **Finding 8** — `HOW-IT-WORKS.md` still printed the unconditional *"You have a different
  architecture and different training"* as Tactic 1, the second copy of the exact claim `grok-2`
  had removed from the template.

Both fixed 2026-08-22. A record of the reviewer's own report follows verbatim.

**Consequence for any future Grok calibration:** this model has now read the answer key in a
session that discussed the planted defects by name. A fresh session does not carry that, and the
corpus tests capability rather than recall, so a later calibration is weakened rather than
worthless — but it is weakened, and `B-1`'s private replacement corpus is the honest remedy.

---

# Independent review

- **Reviewer:** Grok 4.6 (xAI)
- **Target:** this directory (adversarial-review-skills, branch `calibration-corpus-and-claim-cards`, HEAD `0d65b51`)
- **Date:** 2026-08-22
- **Envelope honoured:** read the tree; ran the two fixture suites; wrote only this file; no network; no installs. Pytest left `__pycache__` / `.pytest_cache` as the brief permits.

**Coverage:** Read both skills and all four reference/template files, `README.md`, `HOW-IT-WORKS.md`, `BACKLOG.md`, the calibration README / answer key / record template / fixed brief, all six calibration cases, `examples/README.md`, `.gitignore`, the stored calibration record, and the untracked round-4 reports after candidates were formed (they did not originate the checks below). Ran `python3 -m pytest` on both fixture cases (8 passed). Recomputed the prescribed corpus digest and the `git ls-files` digest. Mutated `verify_checksum` to `return True` in a `/tmp` copy. Did not fetch Claude Code documentation (network forbidden) and did not spawn a Claude Code subagent.

Planted defects inside `calibration/cases/trap-*` match `calibration/ANSWER-KEY.md` and are not findings against the repository.

---

## Findings, ranked

Most important first. Rank is cost of leaving the defect unfixed (blast radius × how readily the trigger is reached). Evidence status is not rank.

### 1. The prescribed corpus digest is not the instrument identity the record pins — running the suite, or merely having already run it, makes every PASS look stale

- **Impact:** high
- **Class:** broken published contract / false-green (false-stale) measurement
- **Location:** `calibration/record-template.md:14`; `calibration/README.md:132-135`; `.adversarial-review/calibration/gpt-5.6-sol-high.md:11`; `.gitignore:1-2`
- **Mechanism:** The record template's digest command is:

  ```
  find calibration/cases calibration/CALIBRATION-PROMPT.md calibration/ANSWER-KEY.md
    -type f ! -name .DS_Store -print0 | sort -z | xargs -0 shasum | shasum | cut -c1-12
  ```

  The only name it prunes is `.DS_Store`. Two of six cases ship pytest suites. Pytest writes `__pycache__/*.pyc` into those case directories; those files are ordinary `-type f` results, so they enter the digest. `.gitignore` ignores neither `__pycache__` nor `*.pyc` nor `.pytest_cache`, so the bytecode stays in the working tree. The stored PASS record pins `775e1cc8c43f`. `git ls-files` over the same three paths yields `775e1cc8c43f`. The prescribed `find` on this tree, with the `__pycache__` directories that were already untracked at session start, yields `9fb019996546`. Those are different instruments under the skill's own rule: a differing digest is stale and counts as missing.
- **Trigger:** (a) A consumer recomputes the digest as both skills now require, on a tree where anyone has ever run `python3 -m pytest` from a fixture directory. (b) A scorer follows `calibration/README.md` and runs the suites. (c) This session's pytest run, which the envelope explicitly allows.
- **Consequence:** Calibration is what lets a reviewer's *silence* mean anything. A PASS record that the documented command cannot reproduce is treated as missing: upheld claims become CNV, a clean report is inconclusive, and the next brief inherits no "ground already walked." The one currently filed reviewer (`gpt-5.6-sol` @ high) is in that state on this working tree right now. Pruning `__pycache__` by name would repeat the `.DS_Store` shape: the next cache directory (`.pytest_cache` already exists at repo root; a `*.pyc` outside `__pycache__`; a type-checker cache) reopens it. `git ls-files` of the same paths already equals the pinned digest.
- **Status:** CONFIRMED. Commands and outputs:

  ```
  $ python3 -m pytest calibration/cases/clean-wordcount calibration/cases/trap-unfalsifiable-test -q
  ........                                                                 [100%]
  8 passed in 0.01s

  $ find calibration/cases calibration/CALIBRATION-PROMPT.md calibration/ANSWER-KEY.md \
      -type f ! -name .DS_Store -print0 | sort -z | xargs -0 shasum | shasum | cut -c1-12
  9fb019996546

  $ git ls-files -- calibration/cases calibration/CALIBRATION-PROMPT.md calibration/ANSWER-KEY.md \
      | sort | xargs shasum | shasum | cut -c1-12
  775e1cc8c43f
  ```

  Listed digest inputs included `calibration/cases/clean-wordcount/__pycache__/*.pyc` and `calibration/cases/trap-unfalsifiable-test/__pycache__/*.pyc`. The same `find` with those paths excluded returns `775e1cc8c43f`.

  Why it ranks here: this is the measurement the rest of the pipeline trusts for silence, and the trigger is the documented procedure itself, already satisfied on this tree.

---

### 2. The three-branch independence fix still emits "You will notice different things" on every brief, including same-family

- **Impact:** high
- **Class:** invalid assumption / process
- **Location:** `skills/adversarial-review-prompt/references/prompt-template.md:39-40` (payoff line); `:63-66` (same-family branch); `skills/adversarial-review-prompt/SKILL.md:43-44` (invariant 7); `:57-59` (unconditional architecture claim in the surviving `<why_this_is_hard>` block)
- **Mechanism:** Round 3 replaced the unconditional *"You have a different architecture and different training"* with a placeholder resolved by three branches. The next sentence of the same verbatim-worthy quote is not a placeholder:

  > «independence sentence — one of the three branches below». **You will notice different things, and those things are the entire value of this exercise.**

  Same-family text the author is told to splice in is: *"you do not bring a different architecture, so the blind spots you share with its author are the ones most likely to survive this review."* The emitted pair is then "you do not bring a different architecture" immediately followed by "You will notice different things, and those things are the entire value of this exercise." Unknown-lineage splices "no claim is made about whether your architecture differs" into the same payoff. The leftover sentence is marked verbatim-worthy, so it is not an authoring note that the guillemet grep would catch. The skill's own surviving why-block still states as fact "that a reviewer with a different architecture notices different things" (`SKILL.md:57-59`), which is the sentence invariant 7 exists to stop emitting.
- **Trigger:** Any brief handed to another Claude session, or to any product that is a thin layer over the author's family — both cases the skill explicitly supports (`prompt-template.md:57-59`; `SKILL.md:107-109`).
- **Consequence:** The round-3 finding this was meant to close was that a false independence claim "tells the reviewer that its disagreement is evidence of an architectural difference which may not exist, inflating exactly the findings this exercise is least able to check" (`prompt-template.md:71-73`). The false claim moved one sentence later. Same-family reviews, which the skill says buy much less, are told that noticing different things *is the entire value*.
- **Status:** CONFIRMED — read the quote, the three branch strings, and invariant 7 in the current files. No execution required; the emitted text is the defect.

  Why it ranks here: every same-family run (a supported, likely path) reintroduces the exact inflation the last round paid to remove, and the leftover line is in the surviving prefix plus the template authors are told to copy.

---

### 3. The overwrite guard names the brief and the cover note, and leaves the report (and the ledger) as the default collision

- **Impact:** medium
- **Class:** data loss / process
- **Location:** `skills/adversarial-review-prompt/SKILL.md:41-42`, `:324-330`; `skills/adversarial-review-prompt/references/cover-note-template.md:86-91`; `skills/adversarial-review-prompt/references/prompt-template.md:337-358`; `skills/review-adjudication/SKILL.md:155-164`, `:527-530`
- **Mechanism:** The new guard, including the copy that survives compaction, is "Never overwrite an existing brief or cover note." The reviewer is still told, in the skill (`:349`), the cover-note template (`:51`), and the default deliverable, to write `NN-EXTERNAL-REVIEW.md`. The cover-note template already records what happens if that is left to chance: *"A reviewer left to guess will overwrite"* (`cover-note-template.md:90-91`). That warning was not lifted into the guard. Several reviewers on one brief get distinct report paths; a later *round* over the same target gets `-2` on the brief and cover note only. The ledger's append-only rule is a prose sentence (`review-adjudication/SKILL.md:527-530`) with no existence check before `Write`.
- **Trigger:** A second review of the same target using the default report path; a follow-up round that suffixes the brief but not the report; an adjudication session that `Write`s the whole ledger file rather than appending.
- **Consequence:** The report is the evidence the ledger's echo audit is scored against and the next brief's "ground already walked" is read out of. Destroying it is the failure the brief-guard exists to prevent, applied to the wrong file. This repository's actual workflow is sequential rounds in one directory (`EXTERNAL-REVIEW.md`, `EXTERNAL-REVIEW-2.md`, `EXTERNAL-REVIEW-3.md`).
- **Status:** CONFIRMED — the guard text names two files; the default report path is still the unsuffixed name; the cover-note template already states the overwrite for delta reviews.

  Why it ranks here: blast radius is an entire prior audit; likelihood is the default path, not an exotic one. Below 1 and 2 because a careful author following the several-reviewers variant (as round 4's briefs did) can dodge it, whereas 1 fires from the documented command and 2 fires from the verbatim template.

---

### 4. Author family is never collected; the three independence branches cannot express human, mixed, or undetermined authorship

- **Impact:** medium
- **Class:** invalid assumption
- **Location:** `skills/adversarial-review-prompt/SKILL.md:76-109` (§1 inputs); `skills/adversarial-review-prompt/references/prompt-template.md:26-29` (provenance gate), `:32-34` (default "every line… written by one model"), `:61-69` (three branches, all of which name «author family» or «family»)
- **Mechanism:** §1 makes reviewer identity a required input and never asks who wrote the work. The template's independence branches all require an author family: different / same / unknown *reviewer* lineage. There is no branch for human-written work, mixed human/AI, several model families, or undetermined author. The default provenance sentence remains "Every line of the code you are about to audit was written by one model…" The gate paragraph tells the author to "state the actual provenance instead" when they already know it is mixed, but nothing in §1 collects that fact, and invariant 7 says the three branches are the whole resolution. The skill description itself includes "a red-team of their own code."
- **Trigger:** A user asks for an independent review of work they wrote, or of a tree with inherited/third-party/human commits — the case `HOW-IT-WORKS.md:88-91` already flags as making "every line was written by one model" false.
- **Consequence:** The brief either emits a false provenance sentence (the reviewer is primed to distrust everything else, which is the failure `HOW-IT-WORKS.md:91` names) or the author invents a fourth branch the invariant says does not exist. Same-family vs different-family cannot be evaluated without the author half, so invariant 7 cannot be obeyed on these targets.
- **Status:** CONFIRMED that §1 never asks for author family and that the three branches are the only options written. THEORETICAL that human-authored targets are a common use — the skill's own description names that use; I did not measure frequency.

  Why it ranks here: false provenance is the brief-trust failure the design doc already ranks high, but it only fires when authorship is not "one model," which is not every run.

---

### 5. `FIX LATER` "before the ledger is written" cannot be obeyed together with "write the skeleton before judging"

- **Impact:** medium
- **Class:** internal contradiction
- **Location:** `skills/review-adjudication/SKILL.md:42-44` (invariant 4, surviving prefix); `:209-212` (step 2: skeleton to disk before any adjudication); `:498-499` (§6: backlog created before the ledger is written)
- **Mechanism:** Step 2 requires the ledger skeleton on disk before any finding is judged. Invariant 4 and §6 require the `FIX LATER` backlog artifact to exist **before the ledger is written**. Dispositions do not exist until after the skeleton exists. Both instructions cannot be true of the same run. The copy that survives compaction is the unsatisfiable half (invariant 4).
- **Trigger:** Any report with a finding that is (correctly) dispositioned `FIX LATER` after enumeration — the skill's own deferral path, not an edge.
- **Consequence:** Every conforming adjudicator must violate one invariant. Future ledgers can record a structurally forced sequence as operator error (as round 3 did for `B-3`). The rule does not actually guard against dropped deferrals, which is the only thing it is for.
- **Status:** CONFIRMED as a documentary contradiction. The round-3 ledger plus `BACKLOG.md` B-3 is a worked instance of writing the artifact after the ledger row. I did not re-run the skill.

  Why it ranks here: it fires on every deferral, but a conscientious operator can still produce a complete backlog file; the lost thing is the guard, not always the finding.

---

### 6. The no-filesystem route is forbidden by the surviving invariant, and the operator "continue" instruction is missing from the skill's hand-off and from the cover-note variant that skill §1 actually cites

- **Impact:** medium
- **Class:** process / broken contract
- **Location:** `skills/adversarial-review-prompt/SKILL.md:36-37` (invariant 4); `:137-147` (§1 delivery route, points at `cover-note-template.md`); `:462-495` (§10 hand-off checklist); `skills/adversarial-review-prompt/references/cover-note-template.md:79-84`; `skills/adversarial-review-prompt/references/prompt-template.md:360-376`
- **Mechanism:** Three artifacts disagree.

  1. Invariant 4, the copy that survives compaction: the report is a file the reviewer creates — **"never a review handed back in chat for you to file."**
  2. Skill §1 and the cover-note template: a browser chat is a supported reviewer; do not emit a cover note; the report comes back in chat and the user saves it.
  3. The prompt template's no-filesystem variant (only) tells the *reviewer* to stop at a section boundary and wait for one word to continue, and says to put that in the hand-off because the operator, not the reviewer, has to send it.

  Skill §10's hand-off checklist has no continue bullet. The cover-note-template variant that §1 points at for this case also has no continue bullet. After compaction, the surviving instruction is (1), which makes (2) a violation.
- **Trigger:** The user names a browser chat (ChatGPT, Gemini, Claude.ai, …) as the reviewer — the case skill §1 says "a great many are."
- **Consequence:** A brief authored from the surviving invariant tells a filesystem-less reviewer to write a file it cannot write, which is the instruction the template says teaches the reviewer that this brief is approximate. A brief authored from the template variant produces a chat report; if output truncates at a section boundary, nothing in the skill's hand-off tells the user to send "continue," and a partial report is filed as complete — the failure the template's continue paragraph exists to prevent.
- **Status:** CONFIRMED — the three texts are as quoted. I did not drive a browser-chat reviewer.

  Why it ranks here: truncation-as-complete is expensive, but only on the no-filesystem delivery route, not on Codex/Cursor/Claude Code.

---

### 7. Adjudication's calibration filename examples bake effort into `<identity>`, which would look up a file that does not exist

- **Impact:** medium
- **Class:** false lookup / process
- **Location:** `skills/review-adjudication/SKILL.md:117-120`; contrast `calibration/README.md:94-101`; `skills/adversarial-review-prompt/SKILL.md:113-115`
- **Mechanism:** The adjudication skill says the filename is always `<identity>-<effort>.md`, then defines `<identity>` as "the served model alias (`gpt-5.6-sol-high.md`)" or "family plus product and version (`openai-codex-cli-0.147.0-high.md`)." Both parentheticals are finished filenames that already include `-<effort>.md`, attached grammatically to the identity half. The calibration README's actual rule uses `gpt-5.6-sol` as the alias and appends effort once. The file on disk is `.adversarial-review/calibration/gpt-5.6-sol-high.md`. An adjudicator who takes the parenthetical literally looks up `gpt-5.6-sol-high-high.md`, or treats `gpt-5.6-sol-high` as the alias. The skill says a wrong identity loading a different record is "an error no later step can see," and a present record read as absent is "the exact failure this scheme was built to escape." The mandatory "list the directory" sentence immediately below is the mitigation; it is not a reason the examples are correct.
- **Trigger:** An adjudication of a `gpt-5.6-sol` @ high (or similarly named) reviewer, following the adjudication skill's examples rather than the README.
- **Consequence:** A real PASS is treated as missing: that reviewer's silence covers nothing, and the next brief does not inherit its upheld claims. The opposite error — concatenating effort twice and then matching a near-miss — is less likely because the directory listing is required, but the examples still teach the wrong key.
- **Status:** CONFIRMED that the examples are effort-suffixed filenames labelled as identity, and that the only on-disk record is `gpt-5.6-sol-high.md`. I did not watch a live adjudicator miss it.

  Why it ranks here: the cost is a false uncalibrated ruling on a reviewer that was tested, but the directory-listing rule, if followed, makes the trigger rarer than findings 1–2.

---

### 8. `HOW-IT-WORKS.md` still presents the unconditional architecture sentence as the current tactic

- **Impact:** low
- **Class:** documentation drift
- **Location:** `HOW-IT-WORKS.md:77-81`
- **Mechanism:** The design doc's "Tactic 1" quote, offered as what you *can* tell the reviewer, still contains "You have a different architecture and different training. You will notice different things…" The template now forbids emitting the first sentence unconditionally (`prompt-template.md:56-59`). An author who learns the skill from the design doc — which `README.md:213-214` points the technically curious at — is handed the sentence the last round removed.
- **Trigger:** Someone writes a brief from `HOW-IT-WORKS.md` rather than from `prompt-template.md`.
- **Consequence:** Same inflation as finding 2, on a less likely path: the skill itself tells the author to follow the template.
- **Status:** CONFIRMED — the quote is in the current file.

  Why it ranks last: the authoritative emit path is the template; this is a second copy that was not updated.

---

## Claims examined and upheld

What upheld each item is a command or a primary file read, not a comment.

- **Answer key vs traps.** `trap-ghost-dependency`: `src/` contains only `api.py` and `store.py`; `PLAN.md:12` names `src/limits.py` / `RateLimiter` as already existing. `trap-undelivered-goal`: Goal 2 is the audit log (`PLAN.md:16-17`); steps 1–3 never call `audit.record`; nothing imports `src/audit.py`. `trap-unfalsifiable-test`: `checksum.py:20` is `actual[:8] == expected[:8]`; `test_checksum.py` never supplies a mismatching digest. `trap-key-to-client`: `config.ts:12` reads `NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY`; `page.tsx:1` is `"use client"` and sends that key as `apikey` (`:12-14`). All four match `ANSWER-KEY.md:32-36`.
- **The unfalsifiable suite stays green under `return True`.** `/tmp` copy, replaced `return actual[:8] == expected[:8]` with `return True`, `python3 -m pytest -q` → `3 passed in 0.01s`, exit 0. The test name `test_returns_a_boolean` would not fail if the function never returned False. This is the planted defect, not a repo bug.
- **Clean-wordcount tests are falsifiable for the whitespace-run claim.** `test_runs_of_whitespace_do_not_inflate_the_count` asserts `count_words("  a\t\tb\n\nc  ") == 3`. `str.split(' ')` on that input is not three tokens. Suite: 5 passed.
- **Clean-copy-link is a plan to add a button, not a claim that `viewer.html` already contains one.** `PLAN.md:10-13` is "Add a `<button…>`"; `viewer.html` has the page chrome and no button. That is not the `trap-ghost-dependency` shape (`already implements`).
- **No `COULD NOT VERIFY` remains in `skills/`.** Round-3 vocabulary fix is present in `calibration/README.md` (`COULD NOT DETERMINE` at the upheld-claims bullet).
- **Guillemet placeholders** are confined to templates / `record-template.md` (authoring instructions), not leaked into `SKILL.md` process prose as live `«»` except inside the templates those skills point at.
- **Workload numbers on the stored record.** `git ls-files calibration/cases | xargs wc -l` → 17 files, 315 lines, matching `.adversarial-review/calibration/gpt-5.6-sol-high.md:12`.
- **`trap-unfalsifiable-test` line citation.** `[:8]` comparison is `checksum.py:20` as the key says.

## Could not verify

- **Whether Claude Code `allowed-tools` is a grant or an allowlist, and whether `disallowed-tools` / path-scoped `Edit` would enforce the write envelope.** Both frontmatters are `Read, Write, Grep, Glob` (YAML as written). Current product behaviour needs the live docs; this envelope forbade network. Prior ledgers quote those docs; that is the work talking, not a check I ran.
- **Whether a spawned verifier with `tools: Read, Bash, Glob, Grep` can mutate the target through `Bash`.** The capability is in the tool set; I did not spend a subagent run.
- **The exact 5,000-token cut line under Claude Code's tokenizer.** Character heuristic at 3.1 c/t puts the prompt skill near line 222 and adjudication near line 204, vs the skills' "roughly line 280 / 270." Without the native tokenizer (and without installs) that remains a bound, not a pin. The invariant blocks still sit above either estimate.
- **Whether description-field triggering works on natural phrasing.** Conceded at `HOW-IT-WORKS.md:724-727`; not re-tested.
- **Cross-host digest identity** (`shasum` vs `sha1sum`, `find` sort order). Not claimed portable; not checked off macOS.

## Unseeded pass

Setting the round-4 briefs' claim lists aside: the adjudication filename examples (finding 7) are the defect this pass reached that those lists did not name. Findings 1–6 were also independently re-derived from the current files and from commands run in this session; they overlap defects already sitting in untracked `EXTERNAL-REVIEW-4.md` / `EXTERNAL-REVIEW-4-GROK.md` and in open ledger row `R3-F12`. I am not treating that overlap as corroboration.

Considered and not raised: compaction line-number estimates being slightly off (direction depends on tokenizer; I could not pin it); `why_this_is_hard` still mentioning architecture difference (author-facing, subsumed by finding 2); `allowed-tools` remaining `Write` (needs docs I was forbidden to fetch); absence of a corpus validator (`BACKLOG.md` B-1 / B-3 — conceded absences, not false claims).

## Mutation results

Mutation testing was not authorized on the skills (prose). For the calibration fixture, in `/tmp` only:

| Break | Suite |
|---|---|
| `verify_checksum` → `return True` | 3 passed, exit 0 |

That is the planted unfalsifiable-test result, not a finding against the repo.

---

**Covered:** both skills, four templates, calibration corpus and key, stored PASS record, README / HOW-IT-WORKS / BACKLOG, fixture tests + one mutation, digest command vs `git ls-files`, planted-trap/answer-key correspondence, clean-case honesty. **Not reached:** live Claude Code permission/compaction behaviour, a no-filesystem reviewer run, a live adjudication of this report, Linux digest portability, skill-description triggering.
