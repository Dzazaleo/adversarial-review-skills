# External Review Adjudication — calibration corpus and claim-card change

**Reports found:** `EXTERNAL-REVIEW.md` — *adjudicated in this ledger*. The step-1 census globbed
the repository root for `*EXTERNAL*` report families excluding `*PROMPT*`, `*COVER-NOTE*`,
`*ADJUDICATION*` and `*RESPONSE*`; it returned exactly one file. `examples/**` holds four prior-round
reports (`audit-of-adversarial-review-prompt/EXTERNAL-REVIEW.md`,
`audit-of-review-adjudication/EXTERNAL-REVIEW.md`, `-2.md`, `-FABLE.md`) — *not adjudicated here:
they are rounds 1–3, already dispositioned in
`examples/audit-of-review-adjudication/REVIEW-ADJUDICATION.md`, and are read in this round only as
settled ground (§3 screening).*

**Review:** `EXTERNAL-REVIEW.md` (OpenAI Codex, GPT-5-based — the reviewer reported that its exact
served model/version identifier was not exposed to it; 2026-08-21). **Envelope honoured.** Verified:
all 25 hash-pinned target files still return their pinned blob hashes, the working tree is byte-for-byte
what the brief describes, and the only file the reviewer added inside the repository is its own
report. No `__pycache__` or `.pytest_cache` droppings; all mutation was done under `/tmp`.

**Brief:** `EXTERNAL-REVIEW-PROMPT.md` (434 lines, 22 load-bearing claims, 6 in-scope paths).

**Reviewer calibration:** **none on file.** `.adversarial-review/` does not exist in this project.
Per `calibration/README.md:85-102` — the rule this very change introduces — this reviewer's findings
are adjudicated normally and at the usual standard, and its *silence* closes nothing: its seven
claims-examined-and-upheld entries are recorded in §7 as unverified rather than as coverage.

**Report completeness:** **complete.** It carries a closing ranked order (17 positions, no ties), a
coverage line, a mutation-results section, a could-not-verify section and a final repository status.
No truncation.

**Adjudicated:** 2026-08-21, by a fresh session that did not write the work under review.

**Findings in: 15 · Rows out: 15 · +3 process, +3 CNV, +0 prior-review disagreements ruled**

No findings merged. The 15 numbered rows are F1–F15. The process block holds P1 and P2 (raised by
the reviewer) plus P-3 (raised by this adjudication). The CNV block holds the reviewer's three
declared could-not-verify items. The reviewer raised no disagreement with a prior internal review —
checked against the three prior findings the brief's §6 named at
`examples/audit-of-adversarial-review-prompt/EXTERNAL-REVIEW.md:134,138,140`; the report agrees with
all three and re-contests none, so the count is zero rather than omitted.

---

## 1. Situation in one paragraph

An uncommitted change to this repository adds a reviewer-calibration corpus (`calibration/` — six
cases, four with planted defects, plus a fixed brief, an answer key, a scoring protocol and a record
template) and amends both skills to read the resulting record, plus a claim-card step and a blind-
subagent escalation in `review-adjudication`. It was written entirely by one model in one session,
which chose the defects, wrote the key declaring what they are, wrote the two "clean" cases and the
rule declaring them clean. OpenAI Codex was handed a 434-line adversarial brief with 22 load-bearing
claims and asked to attack it. It returned 15 numbered findings (5 `high`, 6 `medium`, 2 `low` by its
own ranking, plus 2 `high` it ranked into positions 4–6), 2 process findings, 3 declared could-not-
verify gaps, 7 claims examined and upheld, and a mutation section. Three of its findings were
established by execution, twelve by reading the source. Nothing in this ledger says whether the work
should ship.

## 2. Re-verification performed before accepting anything

Every command below was run read-only against the repository or inside the session scratchpad at
`/private/tmp/claude-501/.../scratchpad`. Nothing in the repository was written, edited or reverted.
Expectations are stated **before** each command, as the ledger template requires.

**A note on the evidence standard for this target.** Twelve of the fifteen findings are about
instruction text — a document contradicting another document. For those, the standard used here is
the one the brief imposed on the reviewer in the other direction: the source cited, opened, and
quoted, with the contradicting passage quoted beside it. Where a finding *could* be executed, it was.

---

### RV-1 · Corpus identity ignores dirty and untracked corpus changes — bears on **F1**

**Expected before running:** `git rev-parse --short HEAD` returns `b993d5e`; `calibration/` is
entirely untracked, so the value the record template prescribes identifies a commit that does not
contain the corpus at all.

```
$ git rev-parse --short HEAD
b993d5e

$ git status --short --untracked-files=all | grep -c '^?? calibration/'
20

$ git ls-tree -r --name-only HEAD | grep -c '^calibration/'
0
```

**Result: as expected.** All 20 corpus files are untracked; zero are in `HEAD`. The reviewer's
figures reproduced exactly.

**Second check — would the prescribed value detect a corpus edit at all?** Expected: no; a content
digest over the corpus tree would. Run against a *copy* in the scratchpad, never the repo:

```
$ cp -R calibration "$SP/corpus"
$ (cd "$SP" && find corpus -type f | sort | xargs shasum | shasum | cut -c1-12)
997e432c3c2b
$ printf '\n<!-- edited -->\n' >> "$SP/corpus/ANSWER-KEY.md"
$ (cd "$SP" && find corpus -type f | sort | xargs shasum | shasum | cut -c1-12)
52d0d65374f9
```

**Result: as expected.** A one-line uncommitted edit moves the digest and leaves
`git rev-parse --short HEAD` untouched. This also establishes that a working fix exists and is one
line.

---

### RV-2 · The checksum trap's mutation and its gating signal — bears on **F3**, and on brief claim 1

**Expected before running:** both suites green at baseline (5 and 3); after replacing
`verify_checksum`'s body with `return True`, still 3 passed; a forged 64-char digest sharing only the
first 8 hex characters verifies `True` while the full digests differ.

```
$ (cd "$SP/ck1" && python3 -m pytest -q)
...                                                                      [100%]
3 passed in 0.01s

$ (cd "$SP/wc1" && python3 -m pytest -q)
.....                                                                    [100%]
5 passed in 0.00s
```

Body of `verify_checksum` replaced with `return True` in the scratchpad copy:

```
$ (cd "$SP/ck1" && python3 -m pytest -q)
...                                                                      [100%]
3 passed in 0.00s
```

Forged-digest probe in a fresh unmodified copy:

```
$ (cd "$SP/ck2" && python3 -c '...')
actual= d8c8b90e2a6d06f066986209ab092fa9aefa1f3e42a75a77f10dcfe41a2238aa
forged= d8c8b90e00000000000000000000000000000000000000000000000000000000
full_digest_matches= False
verify_checksum= True
```

**Result: as expected. The reviewer's figures reproduced exactly** (3 passed / 5 passed / 3 passed
after mutation). The digests differ from the reviewer's only because a different payload string was
used; the mechanism is identical.

**What this settles for F3, which the mutation alone does not.** The mutation confirms the *secondary*
signal. The finding is about which signal *gates*. Read directly:

- `calibration/ANSWER-KEY.md:28` names the capability measured as *"Reads a test for what it would
  catch, not whether it passes"*, and names the primary defect the report must assert as the
  *"only the first 8 hex characters"* comparison.
- That comparison is at `checksum.py:20`, immediately under a comment defending it at `:18-19`
  (*"Comparing all 64 hex characters is wasteful on the hot path, and the first 8 are more than
  enough to catch corruption in practice."*) — fully visible without opening the test file.
- The test-reading signal is at `ANSWER-KEY.md:41-44`, under the heading **"Secondary signals —
  record, do not gate"** (`:31`), and `:34` states *"a reviewer can miss all of them and still pass."*

The gate and the capability label do not name the same behaviour. Confirmed by source, not by the
reviewer's argument.

---

### RV-3 · The documented installation omits the calibration system — bears on **F15**

**Expected before running:** the two `cp -r` commands at `README.md:120-121` produce a skills
directory holding two `SKILL.md` files and their references, and no `calibration/` anything — while
four lines inside those installed files point at a bare relative `calibration/README.md`.

```
$ cp -r <repo>/skills/adversarial-review-prompt  $SP/install/skills/
$ cp -r <repo>/skills/review-adjudication        $SP/install/skills/
$ find $SP/install -type f
<skills-root>/skills/adversarial-review-prompt/SKILL.md
<skills-root>/skills/adversarial-review-prompt/references/cover-note-template.md
<skills-root>/skills/adversarial-review-prompt/references/prompt-template.md
<skills-root>/skills/review-adjudication/SKILL.md
<skills-root>/skills/review-adjudication/references/ledger-template.md

$ find $SP/install -name 'record-template.md' -o -name 'ANSWER-KEY.md' -o -name 'CALIBRATION-PROMPT.md'
no corpus/protocol/record files anywhere in the install

$ grep -rn "calibration/README.md" $SP/install
<skills-root>/skills/review-adjudication/SKILL.md:133
<skills-root>/skills/review-adjudication/SKILL.md:421
<skills-root>/skills/adversarial-review-prompt/SKILL.md:74
<skills-root>/skills/adversarial-review-prompt/SKILL.md:390
```

**Result: as expected, and the live install corroborates it.** This machine's real installation —
which is where this session's own skill was loaded from — has no calibration directory:

```
$ ls -d ~/.claude/skills/calibration
ls: /Users/leo/.claude/skills/calibration: No such file or directory
```

Four installed pointers, zero installed targets. The reviewer's reproduction was accurate.

---

### RV-4 · The isolation recipe — bears on **F12**, and on brief claim 15

**Expected before running:** the snippet at `calibration/README.md:26-32` copies the nested
`src/app/reports/page.tsx` correctly and puts no answer key in the work directory or its parent —
*and* a process rooted there still reads the answer key by absolute path, because nothing sandboxes it.

```
$ CASE=trap-key-to-client; WORK=$(mktemp -d)
$ cp -R calibration/cases/$CASE/. "$WORK"/ && cp calibration/CALIBRATION-PROMPT.md "$WORK"/BRIEF.md
$ find "$WORK"
$WORK/BRIEF.md
$WORK/README.md
$WORK/src/app/reports/page.tsx
$WORK/src/config.ts

$ ls "$WORK"/ANSWER-KEY.md; ls "$(dirname "$WORK")"/ANSWER-KEY.md
ls: .../tmp.VtoBtE5Fd9/ANSWER-KEY.md: No such file or directory
ls: .../T/ANSWER-KEY.md: No such file or directory

$ (cd "$WORK" && head -3 /Users/leo/.../calibration/ANSWER-KEY.md)
# Answer key

**Never copy this file, or the `calibration/` directory as a whole, into the directory you root
```

**Result: as expected, both halves.** The copy mechanics are correct and adjacent discovery is
removed. Confinement is not: the first three lines of the answer key came back to a process rooted
at `$WORK`, from `$WORK`, with no obstruction.

---

### RV-5 · Claim cards cannot copy the required fields verbatim while excluding reasoning — bears on **F6**

The reviewer rated this THEORETICAL, saying only randomized adjudications would settle it. That is
true of the *anchoring effect size*, but not of the contradiction, which this adjudication had to
resolve in practice at step 2 — a real report was on the desk and the cards had to be cut from it.

**Expected before running:** if the rule is operable, the three verbatim-copy fields
(Mechanism · Trigger · Consequence) of a compliant report will contain claim only. Expected instead:
a substantial minority carry evidence, citations or the severity argument inside those fields.

A regex sweep flagged 9 of 17 blocks; the regex is a pointer, not evidence, so four were hand-read in
full. Verbatim from this report's **Mechanism** fields:

- `EXTERNAL-REVIEW.md:12` (F1) — *"…This is not hypothetical in the target state: every file under
  `calibration/` is untracked while the prescribed value is the pre-corpus base commit `b993d5e`."*
  That sentence is **evidence**, inside Mechanism.
- `:41` (F4) — *"Current Claude Code documentation says a non-fork subagent does not see skills
  already invoked…"* — an **evidence appeal**, inside Mechanism.
- `:32` (F3) — *"A reviewer can earn the claimed capability without opening `test_checksum.py`; a
  reviewer that finds the false-green suite but misses… fails it."* — the **severity argument**,
  inside Mechanism.
- `:131` (F14) — a **URL citation** to `calibrate.sh` plus *"The credited upstream implementation
  avoids the self-report problem by…"* — citation and argument, inside Mechanism.

**Result: as expected.** At least 4 of 15 numbered findings put reasoning, evidence or a citation
inside a field `skills/review-adjudication/SKILL.md:168-174` requires to be *"copied verbatim and
nothing else"* while *"what stays out of the card"* is *"the reviewer's reasoning, its evidence, the
argument for its severity."* Both instructions cannot be obeyed on the same field. **This upgrades
the reviewer's THEORETICAL to CONFIRMED on the contradiction** — the first-hand demonstration is this
ledger's own step 2.

---

### RV-6 · Reviewer-echo audit — bears on the weight the whole report earns

`skills/review-adjudication/SKILL.md:277-278` requires discounting agreement that is not independent.
There is no residual-doubts hand-off on disk for this brief, so the doubts themselves cannot be
scored one by one. The larger and checkable channel is the brief's own §5: 22 load-bearing claims,
most carrying an italicised sub-question that *states the suspected defect*. Each finding was probed
against the full brief **and** the cover note using its own identifiers, not a paraphrase:

| Finding | Result | Where the brief already said it |
|---|---|---|
| **F1** | **no line found** | — |
| **F2** | **no line found** | the only hit is `EXTERNAL-REVIEW-PROMPT.md:30`, the production brief's *own* counterweight — not a pointer at `CALIBRATION-PROMPT.md` |
| **F15** | **no line found** | hits on `install` are `:91` ("no install step") and the case-copy commands at `:143-144` — unrelated |
| F14 | partial | `:263-264` raised self-reported identity (claim 13). The *configuration-binding* half — effort, system prompt, context, CLI version — is new |
| F9 | partial | `:92`, `:96` and cover-note `:37` state the absence of CI/test-runner as a **known fact**. The corpus-drift angle is new |
| F3 | echo | `:194-195` — *"or would a reviewer hit the primary defect (the 8-char comparison) purely from reading `checksum.py`, never opening the test at all?"* |
| F4 | echo | `:306-309` — names `Task`, asks if it is the correct tool name, and cites `:391-396` |
| F5 | echo | `:281-282` — *"It is 40 lines; the real briefs this project produces are 400–600."* |
| F6 | echo | `:300-302` — *"Does that exception swallow the rule…"* |
| F7 | echo | `:293-298` — *"can an adjudicator write the 'expected result' after seeing the output, and who would ever know?"* |
| F8 | echo | `:272` — *"Is there anywhere the rule is asserted in prose but the surrounding instruction would in fact cause a finding to be discounted?"* |
| F10 | echo | `:242-244` — *"Is that a real mitigation or a disclaimer?"* |
| F11 | echo | `:236-238` — *"is adoption a legitimate input into a correctness threshold?"* |
| F12 | echo | `:274-275` — *"Does it isolate? Consider what a reviewer rooted at that temp directory can still reach"* |
| F13 | echo | `:257` — *"Is 30 derived from anything, or chosen because it sounds like a period?"* |

**Result: 10 of 15 findings are echoes of a question the brief itself posed, 2 are partial, 3 are
independent.** This is not the reviewer's fault — §5 *required* it to adjudicate all 22 items. What
follows is a rule about weight, applied throughout §3 below: **for the ten echoes, the ruling rests
on this session's own reading of the primary sources, and the reviewer's agreement is scored as
nothing.** Every one of the ten was re-derived that way. The report's independent evidentiary value
concentrates in **F1, F2, F15, P1, P2** and the new half of **F14** — and all five of those are
CONFIRMED, which is a strong result on the part of the report that was actually free to surprise.

---

### RV-7 · The reviewer's primary-source citations — bears on **F2** and **F14**

The report cites an upstream project twice. First, that the upstream is genuinely credited here:

```
$ grep -rn "cross-model-review" --include='*.md' .
README.md:225:The calibration corpus follows [cross-model-review](https://github.com/med95Albert/cross-model-review),
HOW-IT-WORKS.md:684:  [med95Albert/cross-model-review](https://github.com/med95Albert/cross-model-review) makes the
```

Then the upstream `calibrate.sh` itself, fetched and read:

- **F2's comparison holds.** The upstream runner tells the reviewer: *"If you genuinely cannot break
  the document from primary sources, it passes — do not manufacture issues."*
- **F14's comparison holds.** The upstream extracts the configured judge model **and effort**,
  captures `codex --version`, and aborts with *"calibration records lacking model identification are
  treated as invalid"* when the model cannot be resolved.

**One drift, recorded:** the reviewer cited `calibrate.sh:63-70` and `:15-33,99-120`; the fetched
source puts these at roughly `:53-54` and `:18,23-36`. **The substance reproduced exactly; the line
numbers did not.** Both readings are of a remote file that may have moved, and the fetch was
summarised by a tool rather than read line-by-line, so this is recorded as a caution rather than
charged against the report.

---

### RV-8 · Process findings against the brief — bears on **P1** and **P2**

**P1, expected before running:** `EXTERNAL-REVIEW-PROMPT.md:371-373` lists the expected final
`git status` as the five modified files, `calibration/`, and the report — and the tree also holds two
pre-existing untracked inputs, so a correct untouched tree violates the brief's own assertion.

```
$ awk 'NR>=371 && NR<=373' EXTERNAL-REVIEW-PROMPT.md
At the end, report the repository tree clean: run `git status --short` and paste the output. The
expected result is the five modified files, `calibration/`, and your `EXTERNAL-REVIEW.md`. Any
other line is a finding against you.

$ ls -lT EXTERNAL-REVIEW-COVER-NOTE.md EXTERNAL-REVIEW-PROMPT.md EXTERNAL-REVIEW.md
Aug 21 17:39:25 2026 EXTERNAL-REVIEW-COVER-NOTE.md
Aug 21 17:40:20 2026 EXTERNAL-REVIEW-PROMPT.md
Aug 21 18:02:57 2026 EXTERNAL-REVIEW.md
```

**Result: as expected.** The two files predate the report by 22 minutes; neither was written by the
reviewer, and both necessarily appear in the required status output.

**P2, expected before running:** `:91` says "four small Python files"; the actual count is eight.

```
$ find calibration/cases -name '*.py' | wc -l
8
$ awk 'NR==91' EXTERNAL-REVIEW-PROMPT.md
| Install step | none — this repository is markdown plus four small Python files and two TypeScript files |
```

**Result: as expected.** Eight, not four. The TypeScript count (two) is right.

---

### RV-9 · Subagent tool naming — bears on **F4**

**Expected before running:** current Claude Code names the subagent tool `Agent`; the repository
skill's frontmatter at `:12` still says `Task`.

```
$ claude --version
2.1.238 (Claude Code)

$ grep -h -A15 '^allowed-tools' ~/.claude/skills/*/SKILL.md | grep -oE '^\s*-\s*(Task|Agent)\b' | sort | uniq -c
  30   - Agent

$ grep -rln '^\s*-\s*Task\s*$' ~/.claude/skills/*/SKILL.md
(no output)
```

**Result: as expected.** Thirty installed skills on this machine declare `Agent`; none declare
`Task`. This session's own tool surface exposes `Agent` and no `Task`. **What is not established:**
whether a bare `Task` in `allowed-tools` still resolves through a legacy alias — settling that needs
the repository skill actually invoked and its escalation exercised, which this session did not do.

**The other half of F4 is settled by reading.** `skills/review-adjudication/SKILL.md:327-335` says to
*"Spawn a subagent, hand it the claim card and the code the claim concerns"* and says nothing about
restricting its tools or restating the write boundary. The boundary it would need is 60 lines away at
`:391-396` — in the parent skill's text, which the spawned context does not receive.

---

### RV-10 · Working state clean at the end of re-verification

```
$ git status --short --untracked-files=all
 M HOW-IT-WORKS.md
 M README.md
 M skills/adversarial-review-prompt/SKILL.md
 M skills/review-adjudication/SKILL.md
 M skills/review-adjudication/references/ledger-template.md
?? EXTERNAL-REVIEW-COVER-NOTE.md
?? EXTERNAL-REVIEW-PROMPT.md
?? EXTERNAL-REVIEW.md
?? calibration/… (20 files)

$ <recompute all 25 pinned blob hashes>
ALL 25 STILL MATCH — nothing in the repo was written

$ find . -name '__pycache__' -o -name '.pytest_cache' | grep -v '^./.git'
(none)
```

The only files this session created in the repository are `BACKLOG.md` and this ledger — both
permitted by step 7, both listed here rather than left to be discovered. Claim cards were cut into
the session scratchpad and are not beside the ledger.

---

## 3. Adjudication

One row per numbered finding. Both axes on every row. Impact shown is the **reviewer's**, not a
re-rating.

| # | Finding | Class | Verdict | Disposition |
|---|---------|-------|---------|-------------|
| F1 | The corpus identity ignores dirty and untracked corpus changes *(high)* | broken contract | **CONFIRMED** — RV-1. `HEAD=b993d5e`, 20/20 corpus files untracked, 0 in `HEAD`. The `This corpus changed` expiry trigger at `calibration/README.md:78-79` cannot fire for the corpus as it exists today. **Independent finding** (RV-6) | **FIX NOW** — `calibration/record-template.md:13`: replace `git rev-parse --short HEAD` with a digest over the corpus tree, and match the wording at `calibration/README.md:78-79`. **✔ executed 2026-08-21** — `Corpus commit` → `Corpus digest` running `find calibration -type f \| sort \| xargs shasum \| shasum \| cut -c1-12` (returns `45be0d8ac190` on the committed corpus); expiry bullet rewritten to name the digest and to say an uncommitted or never-committed corpus expires the record |
| F2 | The fixed brief tells reviewers that the correct clean-case outcome is failure | internal contradiction | **CONFIRMED (partial)** — *established:* `CALIBRATION-PROMPT.md:4-5` states agreement means the exercise failed, `:34-35` permits a no-finding report without retracting it, and two of six cases have "no serious finding" as the correct answer (`ANSWER-KEY.md:51-56`). The project's own production template pairs the same sentence with its counterweight at `references/prompt-template.md:44-45`; the calibration brief drops it. *Unestablished:* the behavioural effect size — whether reviewers actually manufacture findings under it. **Independent finding** | **FIX NOW** — port the counterweight from `prompt-template.md:44-45`. **✔ executed 2026-08-21** — `CALIBRATION-PROMPT.md:3-11`: the agreement-is-failure sentence now sits with "A manufactured finding is worse than no finding… few or zero findings is an admissible result", plus one line telling the reviewer not to hunt for something serious because the paragraph above said agreement is failure |
| F3 | The checksum trap scores the visible implementation flaw instead of the test-reading capability *(high)* | invalid assumption | **CONFIRMED** — RV-2. `ANSWER-KEY.md:28` labels the capability "reads a test for what it would catch"; the gating primary defect is `checksum.py:20`, visible with its defending comment at `:18-19` without opening the test; the test-reading signal sits under "Secondary signals — **record, do not gate**" (`:31`, `:34`). Echo of brief claim 1 — re-derived from source | **FIX NOW** — Q1 settled as option A (§5). **✔ executed 2026-08-21** — `ANSWER-KEY.md:29` now carries two primary defects, either of which scores the case, with both search vocabularies; the negative-path bullet moved out of "Secondary signals"; a new paragraph explains why the case has two; `:7-9`, `:62` and `record-template.md:26-31` follow, the record now asking **which** signal hit |
| F4 | The blind escalation does not carry the adjudication skill's read-only boundary into the subagent *(high)* | internal contradiction | **CONFIRMED (partial)** — RV-9. *Established:* `SKILL.md:327-335` names no tool restriction and does not restate the `:391-396` write boundary, which the spawned context never receives; and `Agent`, not `Task`, is the current tool name (30 installed skills declare `Agent`, none `Task`, on Claude Code 2.1.238). *Unestablished:* whether a bare `Task` in `allowed-tools` still resolves via a legacy alias — i.e. whether the escalation breaks or is merely mis-named. Echo of brief claim 20 — re-derived | **FIX NOW** — rename the tool and carry the boundary. **✔ executed 2026-08-21** — `SKILL.md:12` `Task` → `Agent` (frontmatter re-parsed clean; no `Task` reference remains anywhere in `skills/`); the third escalation rule gains a paragraph requiring the subagent be spawned read-only and the delegation message state the boundary itself, since the subagent never sees the parent skill |
| F5 | A pass on six tiny artifacts is applied to arbitrarily larger real briefs *(high)* | broken contract | **CONFIRMED** — the qualifier exists and is not carried. `ANSWER-KEY.md:80` limits a pass to work "of roughly this size"; `record-template.md:45-47` repeats it; `SKILL.md:78-82` tells the consumer to read result and expiry only. A grep of both skills and the ledger template for any size/workload comparison returns one unrelated hit (`adversarial-review-prompt/SKILL.md:292`, about pasting). Echo of brief claim 16 — re-derived | **FIX NOW** — make the consumer read the caveat the record already carries. **✔ executed 2026-08-21** — `review-adjudication/SKILL.md:78-90` now reads result, expiry **and the size of work the pass was earned on**, and states the gap in the header and at hand-off where the reviewed work is far larger; the same bullet in `adversarial-review-prompt/SKILL.md` follows. No size-match gate added — that would ratchet |
| F6 | Claim cards cannot copy the required fields verbatim while excluding the reviewer's reasoning *(medium)* | internal contradiction | **CONFIRMED** — RV-5, upgraded from the reviewer's THEORETICAL by first-hand execution against a real report: at least 4 of 15 findings (F1, F3, F4, F14) carry evidence, a citation or the severity argument inside Mechanism, a field `SKILL.md:168-174` requires "copied verbatim and nothing else" while excluding exactly those. Echo of brief claim 19 — re-derived | **FIX NOW** — give the mixed field a rule. **✔ executed 2026-08-21** — the claim-card section gains a paragraph: expect argument inside Mechanism on the highest-impact findings, copy the claim clause verbatim and replace the argument with a pointer to its report line (`— argument at :131`), and never paraphrase, because a paraphrase silently edits the thing about to be verified |
| F7 | The claimed pre-registration has no durable evidence of occurring before the check *(medium)* | invalid assumption | **CONFIRMED** — true by construction, verified by reading: `ledger-template.md:60-61` requires the expectation beside the command, `SKILL.md:83-92` makes the current round editable and backfillable *by design*, and the finished artifact carries no timestamp, append-only event, or separate pre-run file. The claim at `SKILL.md:237-238` — "the pre-registration is what carries the weight here" — is the overclaim. What is *not* refuted: it remains a real discipline in-session. Echo of brief claim 18 — re-derived | **FIX NOW** — correct the overclaim. **✔ executed 2026-08-21** — "The pre-registration is what carries the weight here" is gone; the passage now says it works on the adjudicator in the moment and is **not** proof to a later reader — no timestamp, no append-only event, and the current round is deliberately editable — so "write it first because it changes what you notice, not because the document will vouch for you" |
| F8 | The calibration record both governs speech and is ignored by the consuming skill *(medium)* | internal contradiction | **CONFIRMED** — direct contradiction, three sources open side by side: `record-template.md:42-43` says the severity note is what "the adjudicator reads when weighing rank"; `calibration/README.md:85` says calibration governs silence **never speech**; and a grep of `review-adjudication/SKILL.md` for any calibration-based ranking step returns nothing — the consumer at `:78-82` reads result and expiry only. This is exactly the amendment-contradicts-a-rule-elsewhere class the brief's §6 warned was most likely. Echo of brief claim 14 — re-derived | **FIX NOW** — stop the record instructing what the consumer never does. **✔ executed 2026-08-21** — "The adjudicator reads this when weighing rank" deleted from `record-template.md`; the severity line is now explicitly a note for whoever reads the record, and the template states it never adjusts a finding's verdict or rank, quoting the silence-never-speech rule |
| F9 | Nothing checks that the cases and answer key remain mutually valid *(medium)* | false-green gate | **CONFIRMED** — census reproduced: no `pyproject.toml`, `tox.ini`, `noxfile.py`, `Makefile`, `package.json`, `setup.py`, `setup.cfg` or `.github/` anywhere; no executable consumer of the case or key paths. **Not settled by** `HOW-IT-WORKS.md:700-704` — that decision defers an *eval suite* (recall/precision scoring of reviews); a corpus-drift gate is a different thing, and step 3 forbids filing a finding under a ruling about a different defect. Partial echo (the absence was stated in the brief and cover note; the drift angle is new) | **FIX LATER** — backlog artifact created before this ledger: **`BACKLOG.md` §B-1**, carrying the finding's Location, Mechanism and Consequence verbatim plus a minimal-shape sketch |
| F10 | Publishing the answer key turns the default corpus into a recall test, and replacement is not a procedure *(medium)* | invalid assumption | **CONFIRMED (partial)** — *established:* the replacement mitigation is two lines (`HOW-IT-WORKS.md:737-739`) and nothing else in the repository helps a user execute it — a grep of `calibration/` for any construction checklist, validation protocol or findability criterion returns nothing. *Unestablished:* that a PASS *does* mean memorisation — that needs training-data inspection nobody here can do, and the reviewer said so. Echo of brief claim 10 — re-derived | **FIX NOW** — narrow the claim. **✔ executed 2026-08-21** — `HOW-IT-WORKS.md` §11 no longer calls replacement a mitigation: it is "only a direction", it now spells out that replacing means solving the original problem again, and states plainly that **nothing in this repository helps you do any of it** — no checklist, no findability check, no baseline to tell a bent ruler from a bad reviewer. The procedure remains on record at **`BACKLOG.md` §B-2** |
| F11 | The pass rule accepts one serious false positive out of two controls without validation *(medium)* | invalid assumption | **CONFIRMED (partial)** — *established:* the justification at `ANSWER-KEY.md:74-76` is explicitly adoption/tolerance ("flaky enough that nobody runs it"), with no recorded runs or error analysis; and the conclusion at `:80-82` — the reviewer "does not rate correct work as critical" — is strictly broader than the rule, which establishes only that it spared **one of two** artifacts. *Unestablished:* whether the resulting false-pass rate is unacceptable — that needs a multi-reviewer study. Echo of brief claim 9 — re-derived | **FIX NOW** — Q2 settled as option A (§5): threshold stands, overclaim corrected. **✔ executed 2026-08-21** — `ANSWER-KEY.md` now says a pass establishes the reviewer "spared at least one of two correct artifacts — not that it does not rate correct work as critical, which is more than two controls scored this way can show", and a new paragraph states outright that a reviewer may raise a serious finding on **half the negative controls** and pass, that nothing here establishes this rate is acceptable, and how to tighten it. `HOW-IT-WORKS.md:731` follows |
| F12 | The isolation recipe is directory hygiene, not reviewer confinement *(low)* | invalid assumption | **CONFIRMED** — RV-4, executed. The copy mechanics are correct and adjacent discovery is removed; a process rooted at the work directory still read the answer key by absolute path, unobstructed. `calibration/README.md:16-36` calls the result isolation; `HOW-IT-WORKS.md:744-745` states the opposite correctly elsewhere. Echo of brief claim 15 — re-derived by execution | **FIX NOW** — say what the recipe actually buys. **✔ executed 2026-08-21** — `calibration/README.md` §"The isolation rule" gains **"Be exact about what this buys"**: it removes *adjacent* discovery, it is not confinement, a rooted process keeps ordinary filesystem reach and may have the public repo in training data — enforce the rest with the receiving tool's permission system, and treat an unconfined run as a weaker result |
| F13 | Thirty-day expiry is an unsupported constant *(low)* | invalid assumption | **CONFIRMED** — `calibration/README.md:74-76` gives a reason to time-bound records ("providers ship changes behind an unchanged model name") and no derivation for 30 over 7, 60 or per-release; nothing elsewhere in the protocol supplies one. Echo of brief claim 12 — re-derived | **FIX NOW** — honesty about the number, not a different number. **✔ executed 2026-08-21** — the expiry bullet now reads **"The 30 is a chosen default, not a derived one — nothing here measured it, and nothing here can. Shorten it freely; the cost of a shorter window is one twenty-minute rerun."** No constant substituted |
| F14 | A PASS is not bound to the reviewer configuration that earned it *(high)* | broken contract | **CONFIRMED (partial)** — *established:* `record-template.md:6-15` binds identity, product, family, dates, corpus and project — not reasoning effort, system prompt, context limit, or tool/sandbox configuration; `README.md:72-79` lists three expiry keys and "Product used" is not among them; the credited upstream binds model **and** effort, records the CLI version and refuses to proceed on an unresolvable model (RV-7, verified at the primary source). And the live evidence is in this very report's header: the intended reviewer could report only *"OpenAI Codex, GPT-5-based… the exact served model/version identifier is not exposed"* — so the scheme's **primary key was unavailable from the intended reviewer on its first real use**, and `README.md:64` makes that `UNKNOWN MODEL`, which does not pass. *Unestablished:* that a weaker configuration actually reviews worse. Partial echo — the configuration-binding half is new | **FIX NOW** — Q3 settled as option A (§5). **✔ executed 2026-08-21** — the record's identity block is now four fields — **model family · product and version · reasoning effort · reviewer self-report (verbatim)** — replacing a single self-reported key; `README.md` §The record says a model unable to name its own served version is normal rather than a failure, `UNKNOWN MODEL` narrows to a reviewer that will not name even its family, the expiry key covers family/version/effort drift, and a filename fallback (`openai-codex-cli-0.9.2-high.md`) is given so a record can be filed at all. `HOW-IT-WORKS.md:211` follows |
| F15 | The documented installation omits the calibration system *(high)* | broken contract | **CONFIRMED** — RV-3, executed twice. The two `README.md:120-121` commands install two `SKILL.md` files and three references and no calibration anything; four installed pointers name a bare relative `calibration/README.md`; and this machine's live install — the one this session loaded its own skill from — has no `calibration/`. **Independent finding**, and the highest-value confirmed item in the report | **FIX NOW** — make the pointer resolve. **✔ executed 2026-08-21** — all four in-skill pointers now name `https://github.com/Dzazaleo/adversarial-review-skills/tree/main/calibration` and say the corpus is not installed alongside the skill (verified: no bare `calibration/README.md` pointer remains in `skills/`); `README.md` §Install gains **"Keep the clone"** explaining that the two `cp -r` commands install the skills and nothing else |

### Process and prompt defects

**P1 — The brief's expected final status omits its own pre-existing input files.** *Reviewer-raised,
`low`.* **CONFIRMED** (RV-8): `EXTERNAL-REVIEW-PROMPT.md:371-373` lists the expected `git status` as
the five modified files, `calibration/` and the report, then declares "any other line is a finding
against you" — while `EXTERNAL-REVIEW-COVER-NOTE.md` and `EXTERNAL-REVIEW-PROMPT.md` sat untracked in
that tree 22 minutes before the report existed. A correct, untouched tree cannot satisfy the
assertion. **Cost to this run: none** — the reviewer read the conflict correctly, reported it as a
process finding rather than resolving it silently (which is exactly what `:375-376` asks for), and
did not attribute the files to itself. **Disposition: FIX NOW** — the durable fix is in the template,
not this spent brief: `references/prompt-template.md` prescribes the environment table at `:79` but
prescribes no expected-status line at all, so this brief's version was authored ad hoc. Add the rule
that the expected status is produced by *running* `git status --short` when the brief is written, and
that pre-existing untracked files are listed in it.

**P2 — The environment inventory undercounts Python files by half.** *Reviewer-raised, `low`.*
**CONFIRMED** (RV-8): `:91` says "four small Python files"; there are eight. The TypeScript count is
right. **Cost to this run: low** — the hash list at `:100-125` pins all eight, so recovery was cheap,
and the reviewer's own census found them. **Disposition: FIX NOW** — same template site: the
inventory is derived by enumerating the scoped tree, never described from recall.

**P-3 — The echo rule names residual doubts but not the brief's own §5 sub-questions.**
*Adjudicator-raised — this is not in the report; it was found while applying `SKILL.md:277-278` to
this report.* **CONFIRMED** (RV-6): the rule at `:277-278` discounts agreement only where "a brief
claim was the author's own suspicion — a residual doubt leaked into the brief." But the brief's §5
carries 22 claims, most with an italicised sub-question naming the suspected defect outright, and
**10 of this report's 15 findings are echoes of one** — an order of magnitude more author suspicion
than the residual-doubts channel the rule was written for. An adjudicator following the rule as
written would discount nothing here. **Disposition: FIX NOW** — extend `SKILL.md:277-278` to name the
brief's §5 sub-questions explicitly as a non-independence channel, and require the echo audit RV-6
performs: probe each finding against the brief with the finding's own identifiers, and record which
findings were free to surprise. *This is a finding against the skill that produced this ledger, and
it was found by using it.*

### Reviewer's could-not-verify items

**CNV-1 — Crowd-out in `trap-undelivered-goal` (brief claim 5).** Whether the loud
`NotImplementedError` at `src/reports.py:11` causes reviewers to stop before finding the quiet
undelivered Goal 2. **Verdict: COULD NOT DETERMINE** — both signals verifiably exist in the source;
reviewer stopping behaviour is not derivable from it, and this session ran no reviewer models.
**Disposition: VERIFY** — multiple fresh blinded runs of the case, recording whether reports naming
`NotImplementedError` also identify Goal 2's missing delivery. **Does not block** the fix queue; it
does bound what the trap may be said to measure.

**CNV-2 — Discriminative value of `trap-key-to-client` (brief claim 6).** Whether a single grep for
`SERVICE_ROLE` passes the case, making it a pattern-matching test. **Verdict: COULD NOT DETERMINE** —
the identifier is trivially greppable and the key's required assertion (`ANSWER-KEY.md:29`) demands
the browser-exposure and RLS-bypass reasoning on top; which of the two a real reviewer supplies is
not readable from the source. **Disposition: VERIFY** — score raw reports from a deliberately
shallow grep-oriented baseline against general reviewers, without answer-key access. **Does not
block.**

**CNV-3 — Scorer reproducibility of "score the assertion, not the vocabulary" (brief claim 8).**
**Verdict: COULD NOT DETERMINE** — no raw calibration reports, independently scored labels, edge-case
examples or inter-rater results exist anywhere in the repository; there is nothing to rescore.
**Disposition: VERIFY** — two blinded scorers apply `ANSWER-KEY.md:12-22` to the same archived
outputs, then repeat after a delay. **Does not block**, but note the dependency: the pass/fail
result every downstream rule keys on is currently a human judgement of unmeasured reliability.

### Disagreements with a prior internal review

**None raised.** Checked against the three prior findings the brief's §6 named
(`examples/audit-of-adversarial-review-prompt/EXTERNAL-REVIEW.md:134,138,140`): the report agrees
with all three and re-contests none. F7 explicitly *extends* the `:138` finding (post-hoc
justification defeats forced ranking) to pre-registration rather than disputing it, which is what
claim 18 asked for.

### Disagreements between reviewers

Not applicable — one reviewer this round.

---

## 4. Owner decisions required

### Q1 — Should `trap-unfalsifiable-test` gate on the truncated comparison, or on the untestable negative path?

**What turns on it:** whether one quarter of the detection gate measures the capability the answer
key names for it. Today it does not: the gate is the 8-character comparison, which is visible in
`checksum.py` with a comment defending it; the "reads a test for what it would catch" behaviour is
recorded but explicitly does not gate.

**Options:**
- **A — Make the untestable negative path co-primary.** A hit requires asserting *either* the
  truncation *or* that no test supplies a mismatching digest. Buys: the trap can be passed by
  demonstrating the capability the project says it leans on hardest. Costs: relaxes the gate
  slightly — a reviewer that finds only the false-green suite now passes a case it currently fails.
- **B — Swap primary and secondary.** The gate becomes the test-reading finding alone. Buys: exact
  agreement between the capability label and the gate. Costs: fails reviewers who correctly report
  a real 2³²-work forgery as the headline defect. The hardest gate of the four.
- **C — Relabel the capability column only.** `ANSWER-KEY.md:28` stops claiming "reads a test" and
  says what actually gates. Buys: one-line fix, no change to any recorded result. Costs: the corpus
  no longer tests the test-reading capability at all, and the four traps' "four distinct
  capabilities" claim gets weaker.

**Recommendation: A** — it is the only option that keeps the capability the project names as its own
hardest and keeps a defensible gate, and the record template already has a dedicated line for the
negative-path finding (`record-template.md:26-29`) that becomes meaningful rather than decorative.

**Blocks:** nothing. F3's row stays `PENDING OWNER` until answered.

### Q2 — Keep the "at least one of two clean cases" threshold, or require both?

**What turns on it:** a reviewer can raise a `high` or `critical` finding on 50% of the negative
controls and still be recorded as PASS. The stated basis is adoption, not measurement
(`ANSWER-KEY.md:74-76`).

**Options:**
- **A — Keep 1-of-2, fix only the overclaim.** Correct `:80-82` to say a pass establishes the
  reviewer spared **at least one** of two clean artifacts. Buys: the record stops claiming more than
  it measures; calibration stays cheap and gets run. Costs: a reviewer with a genuine
  high-severity false-positive tendency still passes.
- **B — Require both clean cases.** Buys: the clean-side claim becomes what `:80-82` already says.
  Costs: the author's own stated risk — one over-flagged clean case fails an otherwise good
  reviewer, and a calibration people find flaky is a calibration nobody runs.
- **C — Keep 1-of-2 but record the failure prominently.** PASS with a mandatory
  "high-severity false positive observed on N/2 controls" line the adjudicator must read.
  Buys: most of B's information at A's cost. Costs: another field the consumer must actually
  read — which is exactly the failure mode F5 and F8 document.

**Recommendation: A** — the defect established here is the overclaim, not the threshold; and C
should not be adopted until F8's "record says something the consumer never reads" pattern is fixed.

**Blocks:** nothing. F11's row stays `PENDING OWNER` until answered.

### Q3 — What should the calibration record's primary key be, given the intended reviewer cannot supply the current one?

**What turns on it:** whether the calibration system can produce a passing record for OpenAI Codex at
all. `calibration/README.md:59-64` keys the record on the model's own reported identity and makes
"where it will not say" an `UNKNOWN MODEL`, which does not pass. This report's own header is the
first real-world test of that: the reviewer reported "OpenAI Codex, GPT-5-based" and said its exact
served version is not exposed to it.

**Options:**
- **A — Add configuration fields and accept coarse identity.** Key on family + product version +
  reasoning effort, with the self-reported string recorded verbatim beside them. Buys: Codex can be
  calibrated; effort drift becomes visible, which is the half F14 adds that the brief never asked
  about. Costs: three more fields to fill; the key is coarser, so two different served versions
  under one product version look identical.
- **B — Keep the strict key.** Buys: nothing changes; the rule stays simple. Costs: fails closed
  forever for the exact reviewer this repository is built around — the mechanism is inert for its
  primary use case, not just under-specified.
- **C — Follow the credited upstream.** Read the configured model and effort from the CLI rather
  than asking the model, record the CLI version, and refuse calibration when the model cannot be
  resolved (`calibrate.sh`, verified in RV-7). Buys: the identity problem largely disappears.
  Costs: this repository is prose skills with no scripts — this is the first executable component,
  and it is per-CLI work that has to be written and maintained for each one.

**Recommendation: A** — it closes the immediate hole for the cost of three fields, and it is the only
option that captures reasoning effort, which is the part of F14 that no one had thought of. C is the
right long-term shape but it changes what this repository is.

**Blocks:** F14's row. Nothing else in the queue.

**Q-notes — two alternatives named but deliberately not raised as questions.** F7's larger remedy (a
durable pre-registration witness — an append-only event or a separate pre-run file) and F9's larger
remedy (the corpus-drift gate, `BACKLOG.md` §B-1) are both real options. Neither is put to the owner
here because in both cases a correct, cheap fix exists that closes the finding as stated, and
manufacturing a decision where the minimal fix is unambiguous is its own kind of noise.

## 5. Locked owner decisions from this adjudication

**2026-08-21 — owner, verbatim:**

> "I will follow your recommendations on everything. Proceed with the fixes"

This answers **Q1 → option A**, **Q2 → option A**, **Q3 → option A**, and is the explicit
authorisation for the `FIX NOW` queue in §6 to be executed. Recorded before any fix was applied.

- **Q1 (F3) — settled: option A.** The untestable negative path becomes co-primary in
  `trap-unfalsifiable-test`; a hit requires asserting either the truncated comparison or that no
  test supplies a mismatching digest.
- **Q2 (F11) — settled: option A.** The "at least one of two clean cases" threshold stands; the
  overclaim at `ANSWER-KEY.md:80-82` is corrected to what the rule establishes.
- **Q3 (F14) — settled: option A.** The record gains model-family, product-version and
  reasoning-effort fields, with the model's self-reported string recorded verbatim beside them
  rather than as the sole primary key.

## 6. Amendments required

The `FIX NOW` queue. **All 14 dispositions executed 2026-08-21**, on the owner's authorisation
recorded verbatim in §5. Nothing is committed — the repository was uncommitted before this round and
still is; the change is in the working tree, so the execution reference below is a file-and-change
note rather than a commit SHA, per the ledger template's rule for a target with nothing to cite.

| # | Answers | Landed in | State |
|---|---|---|---|
| 1 | **F15** | `README.md` §Install ("Keep the clone"); the four pointers in both `SKILL.md` files → public calibration URL | **✔ executed** |
| 2 | **F1** | `calibration/record-template.md` (`Corpus commit` → `Corpus digest`); `calibration/README.md` §Expiry | **✔ executed** |
| 3 | **F2** | `calibration/CALIBRATION-PROMPT.md:3-11` | **✔ executed** |
| 4 | **F4** | `skills/review-adjudication/SKILL.md` frontmatter (`Task` → `Agent`) and the third escalation rule | **✔ executed** |
| 5 | **F5** | `review-adjudication/SKILL.md` §1 calibration bullet; same bullet in `adversarial-review-prompt/SKILL.md` | **✔ executed** |
| 6 | **F6** | `review-adjudication/SKILL.md` §2 claim-card section | **✔ executed** |
| 7 | **F7** | `review-adjudication/SKILL.md` §5 pre-registration passage | **✔ executed** |
| 8 | **F8** | `calibration/record-template.md` §Verdict, severity line | **✔ executed** |
| 9 | **F10** | `HOW-IT-WORKS.md` §11, public-corpus bullet | **✔ executed** |
| 10 | **F12 + F13** | `calibration/README.md` §"The isolation rule" and §Expiry | **✔ executed** |
| 11 | **P1 + P2** | `skills/adversarial-review-prompt/references/prompt-template.md` §3 and §8b | **✔ executed** |
| 12 | **P-3** | `review-adjudication/SKILL.md` §5 "Discount non-independent agreement" | **✔ executed** |
| 13 | **F3** (Q1→A) | `calibration/ANSWER-KEY.md` traps table, secondary signals, pass rule; `record-template.md` §Traps | **✔ executed** |
| 14 | **F11** (Q2→A) | `calibration/ANSWER-KEY.md` §Pass rule and §What a pass establishes; `HOW-IT-WORKS.md:731` | **✔ executed** |
| 15 | **F14** (Q3→A) | `calibration/record-template.md` identity block; `calibration/README.md` §The record; `HOW-IT-WORKS.md:211` | **✔ executed** |

**F9** is the one row not in this queue: `FIX LATER`, backlogged at `BACKLOG.md` §B-1. Unchanged.

### Changes made beyond the named minimal fixes

Four edits were not in the queue. Each exists only because a fix above would otherwise have left a
document contradicting itself, and each is recorded here rather than absorbed silently:

- `HOW-IT-WORKS.md:197` and `calibration/README.md:13` said "four traps with **one** planted defect
  each". Q1 made one trap hold two. Both sentences corrected, and `:197-200` now describes the
  checksum case by both of its defects.
- `HOW-IT-WORKS.md:211-214` said the record is filed under "the model's own identity, never the
  product's name". Q3 replaced that key with four fields. The passage was rewritten to match,
  including why effort is in the key.
- `HOW-IT-WORKS.md:731` repeated the `ANSWER-KEY.md:80-82` overclaim that Q2 corrected, and now
  carries the corrected form plus the explicit note that a pass tolerates one serious false positive.
- `calibration/README.md` §The record gained a **filename fallback**
  (`<family>-<product><version>-<effort>.md`). The Q3 fix made it possible to record a reviewer that
  cannot name its own version, but both skills look the record up *by filename*, so without this the
  fix would have been unusable for exactly the reviewer it was written for. Flagged as the one place
  where executing the owner's decision required a judgement the decision did not cover.

### Verification after execution

- Both skills' YAML frontmatter re-parses; `allowed-tools` for `review-adjudication` reads
  `Read, Write, Edit, Grep, Glob, Bash, Agent`. No `Task` reference remains anywhere under `skills/`.
- No bare `calibration/README.md` pointer remains under `skills/`.
- Both case fixtures still green in scratchpad copies: `5 passed`, `3 passed`. No case file was
  touched by this round — the Q1 change is entirely in the answer key and the record template, so
  the artifacts the reviewer under test sees are byte-for-byte unchanged.
- The corpus digest command now prescribed by the record template runs and returns `45be0d8ac190`
  on the committed corpus.

  **A correction worth keeping, because the mechanism caught its own author.** An earlier run of
  this command during execution returned `dea42bea7fc9`, and that value was written into this
  ledger. One further edit to `calibration/README.md` followed — the filename fallback noted above
  — and the digest moved. The stale value was found when the digest was recomputed before
  committing, not by review. That is precisely the F1 failure mode the fix was written to prevent,
  reproduced accidentally on the fix itself: a recorded corpus identity that no longer identifies
  the corpus. Under the old `git rev-parse --short HEAD` scheme the value would have been `b993d5e`
  before the edit and `b993d5e` after it, and nothing would have surfaced.

## 7. Claims examined and upheld

The reviewer examined and upheld 7 of the brief's 22 load-bearing claims. **This reviewer has no
calibration record on file, so under `calibration/README.md:92-98` — the rule this change
introduces — none of these is coverage.** They are recorded as unverified, and the next brief's
"ground already walked" section inherits nothing from them:

- **Claim 2** — unbounded `sys.stdin.read()` in `clean-wordcount` is below `high` because the only
  specified caller is a local stdin CLI. *Unverified — not re-established here.*
- **Claim 3** — the deprecated `execCommand` fallback in `clean-copy-link` is below `high` because
  the plan detects failure and offers manual copy. *Unverified.*
- **Claim 4** — `trap-ghost-dependency` is solvable: the scope declares the whole directory, and
  `src/` holds only `api.py` and `store.py`. *Unverified.*
- **Claim 7** — the four traps require four different comparisons; traps 1 and 2 do not reduce to
  one. *Unverified.* Note the tension with F3, which this ledger confirmed: trap 3's gate does not
  test the capability its label claims, so "four distinct capabilities" is weaker than claim 7
  upheld it as, whichever way Q1 is answered.
- **Claim 11** — a missing calibration record is not behaviourally inert; it changes upheld claims to
  CNV and clean reports to inconclusive. *Unverified as a claim — though this ledger is itself a
  worked instance of the mechanism firing, which is weak evidence in its favour.*
- **Claim 21** — a blind subagent's genuine disagreement is evidence of unresolved truth, so
  `COULD NOT DETERMINE` preserves the row rather than losing the finding. *Unverified.*
- **Claim 22** — this ledger is a durable post-report record rather than a pre-human noise filter, so
  refusing the "default to refuted when uncertain" convention is defensible. *Unverified.*

Claims 1, 5, 6, 8–10, 12–20 were turned into findings F1–F15 and are ruled in §3. Claims 5, 6 and 8
are additionally carried as CNV-1 to CNV-3.

## 8. What this review could not settle, and why that is acceptable

- **Everything in CNV-1 to CNV-3.** All three need reviewer models run against the corpus, which
  neither the reviewer nor this session did. They are open with a named check each.
- **Every behavioural claim in the report.** F2, F5, F10, F11 and F14 each contain a half that turns
  on how models actually behave — whether an adversarial framing makes a reviewer manufacture a
  finding, whether performance degrades on a 434-line brief versus a 40-line one, whether a PASS
  means memorisation, what the false-pass rate is, whether a lower-effort configuration reviews
  worse. **None is established, and the rows say so.** The corpus was built precisely to answer
  questions of this shape and has never been run; that is the largest single gap under this ledger.
- **Whether a bare `Task` in `allowed-tools` still resolves** (F4). Settled by invoking the
  repository skill and exercising its escalation. Not done here; the rename is right regardless.
- **The reviewer's residual-doubts channel.** No residual-doubts hand-off exists on disk for this
  brief, so no doubt could be checked one by one and none is scored as independent corroboration.
  What was checkable — the brief's §5 — was checked in full (RV-6) and is why P-3 exists.
- **The line numbers in the reviewer's upstream citations** drifted (RV-7) while the substance held.
  Recorded so a later reader re-checking those two claims starts from the substance, not the cites.

Nothing in this ledger states whether this work is complete, correct, or ready to publish. That is
the owner's call and it is deliberately not made here.

---

# Round 1 — correction, appended 2026-08-21

The round above is closed and is left exactly as written. This block records a defect **introduced
by one of its own fixes**, found before the fixes were handed to the next reviewer.

### C-1 — The F14 fix left both consumers describing the key it replaced

**Found by:** authoring the round-2 patch-verification brief, while writing the claim that the
`FIX LATER`/lookup path still resolves. Not found by review.

**What was wrong.** Q3 (§5) replaced the record's single self-reported key with four fields —
family, product *and version*, reasoning effort, self-report — and added a filename fallback built
from the product and version (`openai-codex-cli-0.9.2-high.md`). Both skills that *read* the record
still said it is "keyed on the model's own identity **rather than the product's name**"
(`review-adjudication/SKILL.md:79`, `adversarial-review-prompt/SKILL.md:65-66`). After the fix those
sentences instructed the opposite of what the record and the protocol now say, and would have told
an adjudicator that the very filename the protocol prescribes is the wrong kind of name.

**Why it matters beyond the typo.** This is exactly the defect class the round-1 brief named as
most likely — an amendment contradicting a rule elsewhere in the same document — reproduced while
fixing a finding about a contradiction. Two rows in §3 (F5, F8) were dispositioned on the reasoning
that the consuming skills must be kept in step with the record; that reasoning was applied to the
size caveat and the severity note and not to the key itself.

**Fixed 2026-08-21**, in the same act: both bullets now describe the four-field key and the
filename fallback. `calibration/ANSWER-KEY.md:11` was corrected in the same sweep — its heading
still read "the reviewer must report **the** primary defect" after Q1 made one trap hold two.

**Verdict: CONFIRMED** · **Disposition: FIX NOW — ✔ executed 2026-08-21.** Supersedes nothing; it
records a gap in the execution of F14 and Q1 rather than a wrong ruling. The rows for F14 and F3
stand as written.

**Standing note for round 2.** A fix sweep that updates a rule must sweep every consumer that
*describes* that rule, not only those that act on it. Three of this round's fifteen findings (F5,
F8, F15) were a rule and its description drifting apart; the round then did it once more. Whether
any further instance survives is a question for the next reviewer, and it is claim 19 in the
round-2 brief.

