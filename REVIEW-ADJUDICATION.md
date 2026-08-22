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

### S-1 — Scoping note: the cadre-derived rules have never been externally reviewed

Not a finding and not deferred work. A gap in what two rounds of review were *asked* to look at,
recorded here because the next brief's scope section is written from this file.

**What entered, and when.** Two commits below the round-1 audit base imported material from
[VibeCodyH/code-review-cadre](https://github.com/VibeCodyH/code-review-cadre) and then rewrote it:

- `50da1fe` "Adopt four rules from code review cadre" — all five skill files, +139/−15
- `1100680` "Rewrite the cadre-derived passages in our own words" — +46/−44

**Why both rounds missed it.** Both commits are ancestors of `b993d5e`, the base the round-1 brief
pinned against, so relative to that audit range they were unchanged text. The round-1 brief's §4
put "the unchanged parts of the two skills" out of scope for findings, and round 2's range
(`8c1d737..9d892d0`) sits above them too. Neither reviewer declined to look; neither was asked.

**Where the four rules live now**, verified 2026-08-21 — the wording is the repository's own, so a
search for cadre's vocabulary will not find them:

| Cadre idea | Current home |
|---|---|
| Spotting a defect then arguing it away | `adversarial-review-prompt/SKILL.md:195` (no sign-off on a nearby comment) **and** `review-adjudication/SKILL.md:477` (upheld list sampled, not transcribed) |
| A non-review must not be adjudicated as clean | `review-adjudication/SKILL.md:121` |
| A reviewer that stopped early approved nothing | `review-adjudication/SKILL.md:128` |
| Agreement between reviewers that could read each other | `references/ledger-template.md:28-30`, rationale at `:44-48` |

**One correction to the record.** An earlier reading of `50da1fe`'s commit subject treated `DEFER`
as a rule that had been adopted and then lost, since the word appears in no skill file today. That
was wrong, and wrong by the shortcut this repository exists to prevent: a rule was inferred from a
commit subject without opening the diff. `DEFER` only ever appeared in one line of `HOW-IT-WORKS.md`
describing what *cadre* calls that failure mode, and `1100680` rewrote the sentence. Nothing was
lost. The commit subject was naming borrowed ideas in the source's vocabulary, not listing
additions.

Note also that the ledger header's **Reviewer isolation** line is cadre-derived, and the
**Reviewer calibration** line that the work under review added sits directly beneath it and takes
the same shape — a fact about what the report's *silence* may close, not about what its findings are
worth (`ledger-template.md:44-48`). The new mechanism was modelled on an unaudited one.

**What a future brief should do.** Scope `50da1fe..1100680` explicitly, or name those four passages
as in-scope by `file:line`. The question worth putting is not whether the ideas are good — cadre
measured them — but whether the rewrite that made them the repository's own preserved what made
them work, and whether four rules from a tool answering a *different* question (which reviewers to
seat, graded against keys mined from fix commits) transfer to this one intact.

**Verdict: N/A — scoping note, not a finding.** **Disposition: carried into the next brief's scope
section.** No action in this round.

---

# Calibration run — findings against the corpus, 2026-08-22

Not an adjudication of a review. These are defects in the **corpus itself**, found by running it
for the first time: six cases against OpenAI Codex (`gpt-5.6-sol` at high effort), scored in
`.adversarial-review/calibration/gpt-5.6-sol-high.md`. The run returned **PASS — 4/4 traps, 1/2
clean**, and produced five findings about the instrument that produced it.

Recorded here rather than fixed silently, because three of the five are things the author of the
corpus would otherwise be quietly correcting in their own work — which is the disposition reflex
this ledger exists to make expensive. IDs are `K-n`. Both axes on every entry.

### K-1 — `clean-copy-link` disqualifies the reviewer for the move that scores a hit next door

**Location:** `calibration/cases/clean-copy-link/` (contents); `calibration/ANSWER-KEY.md:61`;
`calibration/CALIBRATION-PROMPT.md:15`.

**Mechanism:** `clean-copy-link` is the only case in the corpus that is a plan with **no
accompanying source tree** — verified: both plan-based traps ship a `src/` directory, this ships
`PLAN.md` alone. Its plan says to add a button to `viewer.html`, a file that is not present. A
reviewer therefore reports that the feature is unimplemented and the named file absent, which is
*structurally the same observation* that earns a HIT in `trap-ghost-dependency`:

> case-a, scored HIT — "Step 1 says to extend `src/limits.py`… `src/limits.py` is absent"
> case-c, scored FAIL — "Add a `<button>` to `viewer.html`… the required `viewer.html` [is] absent"

`CALIBRATION-PROMPT.md:15` says only "Everything in the directory you are rooted at" and never
tells the reviewer that a plan-only directory describes unbuilt work. The distinction the author
intended is real but unstated: in the trap a `src/` tree exists and is missing one named file,
which is evidence; here nothing exists, so absence is uninformative.

**Trigger:** any reviewer that compares a plan against the filesystem — the behaviour
`trap-ghost-dependency` exists to reward.

**Consequence:** a competent reviewer fails a negative control for being competent. This is the
bent-ruler failure the round-1 brief named in its first section and said nothing in the repository
would ever surface. It surfaced on first use, by costing a reviewer half its clean score.

**Status: CONFIRMED** by execution — case-c, 2026-08-22. The reviewer raised exactly one finding,
rated `high`, on that basis, and passed the other control (`clean-wordcount`) with zero findings
above `low`.

**Verdict: CONFIRMED · Disposition: PENDING OWNER — proposed: FIX NOW.** Does not block; the run
already passed on the 1-of-2 rule. See Q4.

### K-2 — two case READMEs prescribe an interpreter the prescribed environment does not have

**Location:** `calibration/cases/clean-wordcount/README.md:10`;
`calibration/cases/trap-unfalsifiable-test/README.md:6`.

**Mechanism:** both say "Run the suite with `python -m pytest` from this directory." The macOS
environment the corpus is documented against exposes Python only as `python3`; `python` is not on
`PATH`.

**Trigger:** any reviewer that follows the documented command — which the brief invites, since it
says to run the test suite if there is one.

**Consequence:** every run of either case yields the same true-but-worthless `low` finding, adding
constant noise to the record and spending reviewer effort on the corpus's own typo. Both cases did
exactly this on 2026-08-22 (case-d finding 3, case-e finding 1).

**Status: CONFIRMED** — reproduced directly: `which python` → `python not found`.

**Verdict: CONFIRMED · Disposition: FIX NOW** — `python` → `python3` in both READMEs.

### K-3 — the fixed brief tells the reviewer to run the tests and to write nothing but its report

**Location:** `calibration/CALIBRATION-PROMPT.md:45`.

**Mechanism:** one sentence gives two instructions that cannot both be obeyed:
"Read anything inside this directory. **Run the test suite if there is one. Write `REVIEW.md` and
nothing else.**" pytest writes `.pytest_cache/` and `__pycache__/` as a side effect of running.

**Trigger:** either of the two cases that ship a test suite (`clean-wordcount`,
`trap-unfalsifiable-test`).

**Consequence:** reviewers resolve the contradiction inconsistently, and the inconsistency is the
harm: on 2026-08-22 case-e left both directories behind while case-d ran the suite and left
neither. A scorer checking envelope compliance cannot tell a disobedient reviewer from an obedient
one. Same defect class as round-1 F2 — two instructions in one 40-line fixed brief that contradict
each other.

**Status: CONFIRMED** by execution — `find` over both run directories, 2026-08-22.

**Verdict: CONFIRMED · Disposition: FIX NOW** — minimal fix is to name the exception rather than
loosen the rule: write `REVIEW.md`, and change no file that was already here; test-runner caches
are expected and fine.

### K-4 — identity has to be captured before the sessions are closed, and nothing says so

**Location:** `calibration/README.md:72-80`; `calibration/CALIBRATION-PROMPT.md` (whole).

**Mechanism:** the record's primary key is four fields — family, product and version, reasoning
effort, self-report. None of the six `REVIEW.md` files carries any of them, because the fixed brief
never asks, and it *should* not ask: a review brief that requests the reviewer's model identity
signals that the session is an evaluation, which is the one thing this corpus must not disclose.
So identity is the operator's job, which `README.md:72-80` does say — but it does not say *when*,
and the information lives in a session that gets closed.

**Trigger:** an operator who runs all six cases, closes the sessions, and then opens the record
template. Reasoning effort in particular is not recoverable from the reports.

**Consequence:** the record cannot be reconstructed from the artifacts and must be rebuilt from
memory, or the run is wasted. This nearly happened on 2026-08-22 — the record was blocked until the
operator supplied product version and effort out of band.

**Status: CONFIRMED (partial)** — *established:* no report carries identity, verified across all
six. *Refuted:* the stronger claim that the record "cannot be filled" — it can, by the operator, as
the protocol intends.

**Verdict: CONFIRMED (partial) · Disposition: FIX NOW** — one line in `calibration/README.md`:
capture the four identity fields from the first session **before closing it**, not after the sixth.
Do **not** add an identity question to the fixed brief.

### K-5 — the record filename rule contradicts its own stated intent

**Location:** `calibration/README.md:82-88`.

**Mechanism:** the paragraph says to name the file from the self-reported identity slug where you
have one (`gpt-5.6-codex.md`), and in the same breath that "a run under a different effort or a
bumped product version files a new record rather than overwriting the old one — which is the
behaviour you want, because it is a different reviewer." A bare model slug cannot express effort,
so the primary form cannot deliver the behaviour the paragraph promises. Only the fallback form,
used when the model *cannot* name itself, encodes effort.

**Trigger:** the first real record — reached immediately on 2026-08-22.

**Consequence:** a second run of the same model at a different effort silently overwrites the
first, or the scorer invents a third filename form. The scorer did the latter, filing
`gpt-5.6-sol-high.md`, and flagged it.

**Status: CONFIRMED** — reached in practice while writing
`.adversarial-review/calibration/gpt-5.6-sol-high.md`. This is text written on 2026-08-21 as the
Q3 fix, and it is the same rule-versus-description drift recorded as C-1 and S-1.

**Verdict: CONFIRMED · Disposition: PENDING OWNER — proposed: FIX NOW.** Does not block. See Q5.

## Owner decisions from the calibration run

### Q4 — How should `clean-copy-link` be repaired?

**What turns on it:** whether the corpus keeps failing competent reviewers on a control. The case
currently punishes the exact behaviour `trap-ghost-dependency` rewards.

**Options:**
- **A — Give the case the file its plan extends.** Add a minimal `viewer.html` so the plan names
  something that exists. Buys: the ambiguity disappears, the case still measures "does not invent
  severity in a small, complete plan", and no other case changes. Costs: the corpus gains a file;
  the case stops being a pure plan.
- **B — Tell the reviewer, in the fixed brief, that a plan-only directory describes unbuilt work.**
  Buys: fixes the class rather than the instance. Costs: changes the constant for all six cases,
  and it hands `trap-ghost-dependency` a hint — a reviewer told to think about plan-versus-tree is
  likelier to find the ghost dependency, which inflates that trap's pass rate.
- **C — Retire the case and write a different clean control.** Buys: a control with no known
  ambiguity. Costs: authoring a new clean case is the hard problem F10 says the repo does not help
  anyone with, and it invalidates comparison with this record.

**Recommendation: A** — it is local, it removes the ambiguity without touching the constant, and it
is the only option that does not either help a trap or throw away a case.

**Blocks:** nothing. K-1 stays `PENDING OWNER` until answered.

### Q5 — Should a calibration record's filename encode reasoning effort?

**What turns on it:** whether one model can hold several records at once, or whether an effort
change makes its single record stale.

**Options:**
- **A — Filename includes effort** (`gpt-5.6-sol-high.md`), matching what the paragraph already
  promises. Buys: parallel records per configuration; you can see at a glance that the high-effort
  run passed and the low-effort one was never measured. Costs: more files; consumers must know
  which effort they are about to use before they can find the record.
- **B — Filename is the model slug alone** (`gpt-5.6-sol.md`), and an effort change simply expires
  the record via the existing expiry key. Buys: one file per model, simplest lookup. Costs: you
  lose the earlier result on every effort change, and a reviewer alternating between efforts
  re-runs calibration constantly.

**Recommendation: A**, which is what the text already promises and what the record was filed under;
the fix is to make the primary filename form say so.

**Blocks:** nothing, though the record's filename is provisional until answered.

## Locked owner decisions — calibration run

**2026-08-22 — owner, verbatim:**

> "you decide the best aapproach"

Delegation, following a hand-off that named both questions with options, costs and a stated
recommendation. Taken as **Q4 → option A** and **Q5 → option A** — the two recommendations as
written — and as authorization to execute `K-1`–`K-5`. Recorded before any fix was applied.

Backfilled dispositions: **K-1 FIX NOW ✔**, **K-2 FIX NOW ✔**, **K-3 FIX NOW ✔**,
**K-4 FIX NOW ✔**, **K-5 FIX NOW ✔** — all executed 2026-08-22.

- **K-1** · `calibration/cases/clean-copy-link/viewer.html` added: a minimal, defect-free page with
  the `#page-title` the plan says the button sits next to. The plan's "no new files… existing
  markup" is now true rather than aspirational, and the plan-versus-filesystem move that scores a
  HIT in `trap-ghost-dependency` no longer disqualifies a reviewer here.
- **K-2** · `python -m pytest` → `python3 -m pytest` in `clean-wordcount/README.md:10` and
  `trap-unfalsifiable-test/README.md:6`. Both fixture suites re-run green (`5 passed`, `3 passed`).
- **K-3** · `CALIBRATION-PROMPT.md` envelope now reads "Write `REVIEW.md`, and change no file that
  was already here. A test runner leaving its own caches behind is expected and is not a
  violation." The exception is named rather than the rule loosened.
- **K-4** · `calibration/README.md` now says to capture all four identity fields from the **first**
  session before closing it, and says explicitly not to put the question in the fixed brief,
  because a brief that asks a reviewer what model it is announces that the session is an
  evaluation.
- **K-5** · the filename rule's primary form now ends with the effort — `<identity>-<effort>.md`,
  e.g. `gpt-5.6-codex-high.md` — which is what the paragraph already promised and what the first
  real record was filed under.

### K-6 — the corpus digest was over-broad, and expired records for edits no reviewer can see

Raised by this session while executing the five above, not by the run.

**Location:** `calibration/record-template.md` (Corpus digest row); `calibration/README.md`
(expiry).

**Mechanism:** the F1 fix digested `find calibration -type f` — the whole directory. That includes
`README.md` and `record-template.md`, which are operator documentation the reviewer never sees.
Executing `K-4` and `K-5`, both of which touch only those two files, would therefore have expired
every calibration record on file while changing nothing about the measurement.

**Trigger:** any edit to the protocol docs — a typo fix suffices.

**Consequence:** records are thrown away for free, and the protocol becomes costly to improve,
which is a quiet pressure not to improve it.

**Status: CONFIRMED** by execution — appending one HTML comment to `calibration/README.md` moved
the digest from `573e270c698b` to `0dbe74b4d4a7`; the file was then restored and the digest
returned to `573e270c698b`.

**Verdict: CONFIRMED · Disposition: FIX NOW — ✔ executed 2026-08-22.** The digest now covers the
instrument only — `calibration/cases`, `calibration/CALIBRATION-PROMPT.md`,
`calibration/ANSWER-KEY.md` — stated in both places that name it. New instrument digest:
`da2a8d36e0ba`.

### Consequence for the record just earned: it is stale, and correctly so

Three of the five fixes touch the instrument, so
`.adversarial-review/calibration/gpt-5.6-sol-high.md` no longer matches and is stale, which the
protocol treats exactly as missing. **This reviewer is uncalibrated again until the six cases are
re-run.** The record was not re-dated — `calibration/README.md` says re-run, not re-date — and
carries a STALE banner naming what changed.

It is kept rather than deleted because it is evidence. The six raw reports it was scored from are
archived at `.adversarial-review/calibration/runs/2026-08-22-gpt-5.6-sol-high/`, one per case, with
the scoring notes beside them. **That archive is the only material anyone has for settling CNV-3**
— whether two scorers applying `ANSWER-KEY.md:12-22` to the same outputs agree. It was previously
unanswerable for want of any archived run.

One cost, recorded rather than hidden: publishing model-written reports against a published answer
key adds to the recall exposure F10 describes. The key was already public, so the increment is
small, and CNV-3 cannot be settled without them.

**A re-run is expected to score better, not merely the same.** The only control this reviewer
failed was `clean-copy-link`, on the ambiguity `K-1` has now removed.


---

# Round 2 — audit of the round-1 fixes, adjudicated 2026-08-22

**Reports found:** the step-1 census globbed the repository root for `*EXTERNAL*` report families
excluding `*PROMPT*`, `*COVER-NOTE*`, `*ADJUDICATION*` and `*RESPONSE*`. It returned two:
`EXTERNAL-REVIEW.md` — *adjudicated in round 1 above; not re-adjudicated here* — and
`EXTERNAL-REVIEW-2.md` — ***adjudicated in this round***. `examples/**` holds four further reports
(`audit-of-adversarial-review-prompt/EXTERNAL-REVIEW.md`,
`audit-of-review-adjudication/EXTERNAL-REVIEW.md`, `-2.md`, `-FABLE.md`) — *not adjudicated here:
they are prior rounds against a different target, already dispositioned in
`examples/audit-of-review-adjudication/REVIEW-ADJUDICATION.md`, and are read this round only as
settled ground.*

**Review:** `EXTERNAL-REVIEW-2.md` (OpenAI Codex, GPT-5-based — the reviewer again reported that its
served model version and Codex product version are not exposed to it; 2026-08-22). **Envelope
honoured.** Verified: `git status --short` before this ledger was appended showed exactly
`?? EXTERNAL-REVIEW-2.md` and nothing else; no `__pycache__` or `.pytest_cache` anywhere in the
tree; all mutation was under `/tmp`.

**Brief:** `EXTERNAL-REVIEW-2-PROMPT.md` (557 lines, 24 load-bearing claims, pinned diff
`8c1d737..e1fc88b`).

**Reviewer calibration:** **stale, which the protocol treats exactly as missing.**
`.adversarial-review/calibration/gpt-5.6-sol-high.md` pins corpus digest `573e270c698b`; the
instrument digest today is `da2a8d36e0ba` (reproduced below, RV-1). Per `calibration/README.md:110`
this reviewer is uncalibrated. Consequence, applied: its **findings are adjudicated normally and at
the usual standard**, and its *silence* closes nothing — its fourteen claims-examined-and-upheld
entries are **not coverage**. Five of the fourteen were sampled independently anyway (§R2.6); the
other nine are recorded as unverified.

**Lookup note, first-hand:** this session found that record by listing
`.adversarial-review/calibration/`, **not** by deriving its filename. Had it followed the skill's
own lookup rule from this reviewer's self-report — "OpenAI Codex, GPT-5-based" — it would have
looked for `openai-codex-gpt-5-based-<effort>.md` and concluded *no record on file*. That is
finding `F3`'s consequence, experienced live by the consumer the fix was written for.

**Report completeness:** **complete.** Nine numbered findings, one process finding, a strict ranked
order (ten positions, no ties), a 24-claim adjudication, an independent re-score table, a
claims-upheld section, a could-not-verify section, a mutation section, a coverage line and a final
repository status. No truncation.

**Adjudicated:** 2026-08-22, by a fresh session that did not write the work under review. It is the
same model *family* that wrote it, so every refutation below carries execution evidence rather than
prose.

**ID collision notice:** this round's findings are numbered `F1`–`F9` by the reviewer; round 1's were
`F1`–`F15`. They are different findings. Outside this round, qualify as `R2-F1`. Auxiliary entries
carry explicit `R2-` IDs.

**Findings in: 9 · Rows out: 9 · +2 process, +3 CNV, +1 prior-review disagreement ruled**

No findings merged. `R2-P1` is reviewer-raised; `R2-P2` is adjudicator-raised — found by running the
echo audit this skill mandates, and not present in the report.

---

## R2.1 — Situation in one paragraph

Round 1 produced fifteen confirmed findings; fourteen were fixed, one deferred. The corpus was then
run for the first time, passed, and found six defects in itself, five of which were fixed in the
same range. The same model wrote the work, the fixes, and the fixes-to-fixes, with nobody looking in
between. Codex was handed a 557-line brief with 24 load-bearing claims and asked whether the fixes
close the findings or only read as though they do. It returned nine numbered findings — four rated
`high`, five `low` — one process finding, three declared gaps, fourteen upheld claims, an
independent re-score of all six calibration outputs, and six mutation results. Six of its nine
findings were confirmed here without qualification, two confirmed with a supporting sub-claim
corrected, one confirmed with its diagnosis corrected. Every executed figure it reported reproduced
exactly; both of its claims that something was *absent* failed to reproduce. Nothing in this ledger
says whether the work should ship.

## R2.2 — Re-verification performed before accepting anything

Every command was run read-only against the repository or inside a scratch copy at
`/private/tmp/claude-501/.../scratchpad/r2/`. Nothing in the repository was written, edited or
reverted; the only file this session touched is this ledger. Expectations are stated **before** each
command.

### RV-1 — the instrument digest reproduces

*Expectation: the documented `K-6` command returns `da2a8d36e0ba`, the value the calibration-run
block above records.*

```bash
$ cd <scratch>/r2/current
$ find calibration/cases calibration/CALIBRATION-PROMPT.md calibration/ANSWER-KEY.md -type f \
    | sort | xargs shasum | shasum | cut -c1-12
da2a8d36e0ba
```

Reproduces. The reviewer's figure is exact.

### RV-2 — a scoring-procedure edit leaves the identity unchanged (`F1`, half A)

*Expectation: changing the pass threshold in `calibration/README.md` from one clean case to both
does not move the digest, because `K-6` excluded that file.*

```bash
$ sed -i '' 's/and at least one clean case with nothing above `medium`/and BOTH clean cases with nothing above `medium`/' calibration/README.md
$ grep -n '^\*\*Pass:\*\*' calibration/README.md
59:**Pass:** all four traps hit, and BOTH clean cases with nothing above `medium`. The
$ find calibration/cases calibration/CALIBRATION-PROMPT.md calibration/ANSWER-KEY.md -type f \
    | sort | xargs shasum | shasum | cut -c1-12
da2a8d36e0ba
```

Confirmed. **One correction to the reviewer's mechanism:** it calls
`calibration/README.md` the file that "defines the operative trap/clean scoring procedure". The two
rules that decide a result — *score the assertion, not the vocabulary* and the pass rule itself —
are **also** in `calibration/ANSWER-KEY.md:12-22` and `:69-71`, which **is** digested. So the defect
is not that the scoring rule sits outside the digest; it is that it sits in **two places, one
digested and one not**, so an operator who edits only the undigested copy produces silent drift
between the two and expires nothing. That is this project's recurring defect class, arriving inside
the fix for a different instance of it.

### RV-3 — a whitespace pathname is silently dropped, exit 0 (`F1`, half B)

*Expectation: `xargs` splits the name, `shasum` errors on two nonexistent paths, the pipeline still
exits 0, and the digest is unchanged — so a new case file is silently omitted from the identity.*

```bash
$ printf 'a planted case with a space in its name\n' > 'calibration/cases/added case.md'
$ find calibration/cases calibration/CALIBRATION-PROMPT.md calibration/ANSWER-KEY.md -type f \
    | sort | xargs shasum | shasum | cut -c1-12
shasum: calibration/cases/added: No such file or directory
shasum: case.md: No such file or directory
da2a8d36e0ba
$ echo "pipeline exit status: $?"
pipeline exit status: 0
```

Confirmed, byte-identical to the reviewer's report.

### RV-4 — the proposed minimal fix costs no record and closes the hole

*Expectation: a `-print0`/`-0` variant returns the **same** `da2a8d36e0ba` on a clean tree — so
adopting it does not expire any record — and **does** move when the spaced file is present.*

```bash
$ find calibration/cases calibration/CALIBRATION-PROMPT.md calibration/ANSWER-KEY.md -type f -print0 \
    | sort -z | xargs -0 shasum | shasum | cut -c1-12
da2a8d36e0ba
$ printf 'x\n' > 'calibration/cases/added case.md'
$ find ... -print0 | sort -z | xargs -0 shasum | shasum | cut -c1-12
95bee60976d2
$ rm -f 'calibration/cases/added case.md'
$ find ... -print0 | sort -z | xargs -0 shasum | shasum | cut -c1-12
da2a8d36e0ba
```

Both halves confirmed. The fix is free.

### RV-5 — the digest moves for a file nobody authored (adjudicator-raised, bears on `F1`'s fix)

*Expectation: an incidental `.DS_Store` inside `calibration/cases` changes the identity, which is the
failure `F1` names in the other direction — expiring records for no reason.*

```bash
$ printf '\0\0junk' > calibration/cases/.DS_Store
$ find ... | sort | xargs shasum | shasum | cut -c1-12
5f2fe1ba364b
$ rm -f calibration/cases/.DS_Store
$ find ... | sort | xargs shasum | shasum | cut -c1-12
da2a8d36e0ba
```

Confirmed. The brief's claim 1 asked about this and the reviewer did not answer it. It is not filed
as a separate finding — it is folded into `F1`'s fix, which must be correct in both directions.

### RV-6 — no consumer checks the digest, and the ledger template still says commit (`F2`)

*Expectation: neither skill instructs the consumer to recompute or compare the corpus digest, and
`ledger-template.md` still asks for `corpus «commit»`.*

```bash
$ grep -rn 'digest' skills/
$ grep -n 'corpus\|Corpus' skills/review-adjudication/references/ledger-template.md
31:**Reviewer calibration:** «PASS, run «date», expires «date», corpus «commit» — from
```

Confirmed, and **stronger than reported**: the string `digest` does not appear *anywhere* in
`skills/` — zero hits, not merely no comparison instruction. `review-adjudication/SKILL.md:83-84`
reads result, expiry, identity and workload size; `adversarial-review-prompt/SKILL.md:68` reads
result and expiry. The one check capable of noticing an instrument change is never performed by
either consumer, and the template still names the field the fix replaced.

### RV-7 — three incompatible filename forms (`F3`)

*Expectation: the always-suffixed rule, the unsuffixed skill example, and the real record's name do
not agree.*

Read side by side:

| Source | Form it gives |
|---|---|
| `calibration/README.md:67` | "`<reviewer-id>` is the model's **own** identity, slugged — `gpt-5.6-codex`, `gemini-3-pro`, `claude-fable-5`" — **three examples, no effort suffix**, in the sentence that *defines* the term |
| `calibration/README.md:89-93` | "always end with the reasoning effort … `<identity>-<effort>.md`" — `gpt-5.6-codex-high.md` |
| `skills/review-adjudication/SKILL.md:81` | `gpt-5.6-codex.md` — **no effort** |
| `skills/adversarial-review-prompt/SKILL.md:66-67` | "the filename is a model slug or, failing that, built from the rest" — **effort not mentioned at all** |
| on disk | `gpt-5.6-sol-high.md` |

Confirmed: `K-5`'s rule contradicts the defining sentence twelve lines above it in its own file, and
neither consuming skill was updated. Same defect class again.

**One correction to the reviewer's supporting sentence.** `F3` says the record uses "an alias not
present in that self-report". The record's own verbatim self-report is:

```
| **Reviewer self-report** | "OpenAI Codex, an agent based on GPT-5. The active model alias is
  `gpt-5.6-sol`. The exact backend snapshot/build behind that alias is not exposed." |
```

— `.adversarial-review/calibration/gpt-5.6-sol-high.md:32`. So the primary rule *did* produce
`gpt-5.6-sol-high.md` from what that session actually said; the scorer did not improvise, which is
what the brief's claim 4 asked. The real mechanism is **session-to-session variance in the
self-report of one product** — the calibration session named its alias, this round's session could
not — and that mechanism is demonstrated live by the two reports side by side. The finding stands;
one sentence of its support does not.

### RV-8 — the subagent boundary names no mechanism, and one exists (`F4`)

*Expectation: the skill's frontmatter grants write tools, the delegation rule names no restriction
mechanism, and Claude Code supplies one.*

```bash
$ sed -n '5,13p' skills/review-adjudication/SKILL.md
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
$ sed -n '382,385p' skills/review-adjudication/SKILL.md
  ... So spawn it read-only where the tool grants let you, and say the boundary in the delegation
  message itself ...
$ claude --version
2.1.239 (Claude Code)
$ head -4 ~/.claude/agents/gsd-plan-checker.md
name: gsd-plan-checker
tools: Read, Bash, Glob, Grep, Skill
```

Confirmed. The rule says "where the tool grants let you" and never says how. The mechanism is
concrete, current, and present on this machine: a subagent definition declaring a `tools:` allowlist
without `Write`/`Edit`/`NotebookEdit` (demonstrated by `gsd-plan-checker.md:4`), or a built-in
read-only agent type — this session's own agent roster lists `Explore` as "All tools except Agent,
Artifact, ExitPlanMode, Edit, Write, NotebookEdit". An unnamed general-purpose subagent is `Tools:
*` and inherits everything. The reviewer's `claude --version` figure is exact.

### RV-9 — the envelope permits arbitrary new files (`F5`)

*Expectation: adding a non-cache `EXTRA.md` to a case copy satisfies "change no file that was already
here" literally — every pre-existing file compares byte-equal.*

```bash
$ cp -R <repo>/calibration/cases/clean-wordcount <scratch>/envelope/wc1 && cd <scratch>/envelope/wc1
$ printf 'arbitrary non-cache artifact\n' > EXTRA.md
$ # cmp every pre-existing file against the repository original
pre-existing files all byte-identical: yes
extra artifact present: EXTRA.md
```

Confirmed. The envelope at `calibration/CALIBRATION-PROMPT.md:45-47` reads "Write `REVIEW.md`, and
change no file that was already here." — a bound on modification, none on creation.

### RV-10 — the expiry contradiction (`F6`) and the workload rule (`F7`)

*Expectation: the template hard-codes 30 days with no field for a chosen window; and no threshold or
size field exists anywhere.*

```bash
$ sed -n '13p' calibration/record-template.md
| **Expires** | «YYYY-MM-DD — run date + 30 days» |
$ sed -n '107p' calibration/README.md
  nothing here can. Shorten it freely; the cost of a shorter window is one twenty-minute rerun.
$ grep -n 'Expires\|window\|30' calibration/record-template.md
13:| **Expires** | «YYYY-MM-DD — run date + 30 days» |
$ grep -rn 'far larger\|size of work\|roughly this size' skills/ calibration/
skills/review-adjudication/SKILL.md:83, :89-90 ; calibration/ANSWER-KEY.md:93 ; calibration/record-template.md:64
```

Both confirmed. `F6`: one file says shorten freely, the only file an operator fills says run date +
30, and there is no field to record what was chosen. `F7`: "far larger" appears once, with no
threshold; the record carries a prose standing caveat (`record-template.md:63-65`) and **no workload
field**; the ledger template header (`:20-38`) has **no size-gap field**. Both reproduce exactly.

### RV-11 — the install, and what the URL actually does (`F8`)

*Expectation: the two documented `cp -r` commands install the two skills and no calibration artifact,
and the hard-coded corpus URL does not resolve.*

```bash
$ cp -r <repo>/skills/adversarial-review-prompt  <sandbox>/home/.claude/skills/
$ cp -r <repo>/skills/review-adjudication        <sandbox>/home/.claude/skills/
$ find home -type f | sort
home/.claude/skills/adversarial-review-prompt/SKILL.md
home/.claude/skills/adversarial-review-prompt/references/cover-note-template.md
home/.claude/skills/adversarial-review-prompt/references/prompt-template.md
home/.claude/skills/review-adjudication/SKILL.md
home/.claude/skills/review-adjudication/references/ledger-template.md
$ find home -name 'ANSWER-KEY.md' -o -name 'CALIBRATION-PROMPT.md' -o -name 'record-template.md' | wc -l
0
$ curl -s -o /dev/null -w "%{http_code}\n" -L https://github.com/Dzazaleo/adversarial-review-skills/tree/main/calibration
404
```

Five files, zero calibration artifacts, 404 — all three reproduce exactly.

**The reviewer's diagnosis does not.** It wrote: "search does not find the named public repository"
and "the repository URL itself is unavailable."

```bash
$ curl -s -o /dev/null -w "repo root: %{http_code}\n" -L https://github.com/Dzazaleo/adversarial-review-skills
repo root: 200
$ curl -s -o /dev/null -w "api: %{http_code}\n" https://api.github.com/repos/Dzazaleo/adversarial-review-skills
api: 200
$ git remote -v
origin	https://github.com/Dzazaleo/adversarial-review-skills.git (fetch)
$ git ls-tree --name-only origin/main
.gitignore  HOW-IT-WORKS.md  LICENSE  README.md  examples  skills
$ git rev-list --left-right --count origin/main...HEAD
0	8
```

The repository is public and reachable — it is this clone's `origin`. The `/tree/main/calibration`
path 404s because `calibration/` exists only on the local branch
`calibration-corpus-and-claim-cards`, which is **8 commits ahead of `origin/main` and unpushed**.
The consequence the finding names survives intact; its cause and therefore its remedy change
completely — this is publish ordering, not a broken pointer.

### RV-12 — the inventory count (`F9`) and the range assertion (`R2-P1`)

*Expectation: the brief's stated 416 lines is wrong against the pinned blob, and `e1fc88b` is not
`HEAD`.*

```bash
$ git show e1fc88b:skills/adversarial-review-prompt/SKILL.md | wc -l
418
$ sed -n '167p' EXTERNAL-REVIEW-2-PROMPT.md
| `skills/adversarial-review-prompt/SKILL.md` | 416 | ...
$ git show 3ec5baf:skills/review-adjudication/SKILL.md | wc -l
485
$ git show 3ec5baf:EXTERNAL-REVIEW-2-PROMPT.md | sed -n '145p'
| `skills/review-adjudication/SKILL.md` | 482 | ...
$ git rev-parse HEAD
2ddf6d30064bc6e28c46b2833ca9dc23cdef883d
$ git diff --name-status e1fc88b..HEAD
M	EXTERNAL-REVIEW-2-PROMPT.md
$ sed -n '120p' EXTERNAL-REVIEW-2-PROMPT.md
`e1fc88b` is `HEAD`. There is nothing above the range.
```

Both confirmed exactly. **One figure the reviewer did not supply, which bounds `F9`:** the other
eleven counts in that inventory table were checked against their pinned blobs and **all eleven are
correct** (101, 47, 142, 65, 16, 485, 373, 781, 239, 1078, 59). The rule mostly worked; the single
wrong entry is the one **carried forward** from the earlier version of the brief while its neighbour
(482 → 485) was corrected in the same refresh. That is the precise failure mode, and it names the
fix.

### RV-13 — working state after re-verification

```bash
$ git status --short
 M REVIEW-ADJUDICATION.md
?? EXTERNAL-REVIEW-2.md
$ find . -name '__pycache__' -o -name '.pytest_cache' -not -path './.git/*'
(no output)
```

`REVIEW-ADJUDICATION.md` is this ledger — the only file this session wrote.
`EXTERNAL-REVIEW-2.md` is the reviewer's report. No other repository file changed; all mutation was
in the scratch copy.

## R2.3 — Adjudication

Screened first against settled ground (`CLAUDE.md`: none exists; the three owner decisions `Q1`–`Q3`
locked in §5 above; the `Q4`/`Q5` calibration-run decisions; `BACKLOG.md` §B-1 and §B-2;
`HOW-IT-WORKS.md:700-704`). **No finding this round relitigates a locked decision.** `F3` and `F6`
touch the *implementations* of `Q3` and of round-1 `F13`, which the brief expressly puts in scope at
`:207-209`. No `SETTLED ALREADY` verdict is issued, and none was available.

| ID | Finding *(reviewer impact)* | Verdict | Disposition |
|---|---|---|---|
| F1 | The narrowed corpus digest excludes a scoring rule and silently ignores filenames containing spaces *(high)* | **CONFIRMED (partial)** — RV-2, RV-3, RV-5, all executed. *Established:* the whitespace path is silently dropped with exit 0 and an unchanged digest, byte-identical to the report; and a scoring-threshold edit in `calibration/README.md` leaves the identity unchanged. *Corrected:* the two rules that decide a result are **also** in the digested `ANSWER-KEY.md:12-22,69-71`, so the defect is duplication across a digested and an undigested file, not exclusion of the sole authority. *Added by this session (RV-5):* the identity also moves for a `.DS_Store` nobody authored — the same failure in the other direction, which the fix must close too | **FIX NOW** — two edits, both verified free of record cost by RV-4. (a) `calibration/record-template.md:14` and `calibration/README.md:112`: `-type f -print0 \| sort -z \| xargs -0 shasum`, with `.DS_Store` pruned. Returns the same `da2a8d36e0ba` on a clean tree, so no record is expired. (b) `calibration/README.md:46-60`: stop restating the assert-not-mention rule and the pass threshold — point at `ANSWER-KEY.md`, so the operative text lives only in a digested file. Do **not** re-broaden the digest to include `README.md`: that reverts `K-6`, whose reason still holds **✔ executed 2026-08-22** — (a) `record-template.md:14` now runs `-type f ! -name .DS_Store -print0 \| sort -z \| xargs -0 shasum`; (b) the one rule that lived only in the undigested README — severity does not gate a trap — moved into `ANSWER-KEY.md:24-28`, and `calibration/README.md` §Scoring now restates **nothing**, stating instead that every deciding rule lives in the key and only there, with the reason (the key is digested, that file is not) |
| F2 | Neither consuming skill checks the corpus digest before accepting a record *(high)* | **CONFIRMED** — RV-6, and stronger than reported: `grep -rn 'digest' skills/` returns **zero hits**. `review-adjudication/SKILL.md:83-84` reads result, expiry, identity, workload; `adversarial-review-prompt/SKILL.md:68` reads result and expiry; `ledger-template.md:31` still asks for `corpus «commit»`, the field `F1`/`K-6` replaced. The only check that can notice an instrument change is never performed end to end. **Independent on its core half** (§R2.4) | **FIX NOW** — three sites, all already touched this round. Both consumer bullets gain the digest: recompute it from the corpus and compare with the record's; a differing digest is stale and counts as missing. `ledger-template.md:31` `corpus «commit»` → `corpus digest «12-char»`. **And name the case the fix cannot cover:** an installed skill has no `calibration/` (`F8`), so it cannot recompute — the honest instruction there is to record that staleness was *unknowable*, not to pass the record **✔ executed 2026-08-22** — both consumer bullets now read the corpus digest, recompute it and compare, and say staleness was *unknowable* where the corpus is absent (`review-adjudication/SKILL.md:87-96`, `adversarial-review-prompt/SKILL.md:68-76`); `ledger-template.md:31-32` `corpus «commit»` → `corpus digest «12-char» — recomputed and matches / differs / not checkable` |
| F3 | The same reviewer still has several valid filenames, so lookup is not reproducible *(high)* | **CONFIRMED (partial)** — RV-7. *Established:* four incompatible forms, including `calibration/README.md:67` giving three unsuffixed examples in the sentence that defines the term, twelve lines above `K-5`'s "always end with the reasoning effort"; and both consuming skills carrying unsuffixed/effortless forms. *Demonstrated live:* this adjudication would have missed the existing record by following the written rule (see header). *Corrected:* the record's own verbatim self-report **does** contain `gpt-5.6-sol` (`gpt-5.6-sol-high.md:32`), so the rule produced that filename from what that session said; the scorer did not improvise. The real mechanism is session-to-session variance in one product's self-report | **FIX NOW** — one rule in one place. Suffix the three examples at `calibration/README.md:67` or make that sentence defer to `:89`; `review-adjudication/SKILL.md:81` `gpt-5.6-codex.md` → `gpt-5.6-codex-high.md`; `adversarial-review-prompt/SKILL.md:66-67` gains the effort. Then the part that actually closes the finding: a **precedence order** over the four recorded fields (self-reported alias where the session exposes one, else family + product + version), and one line telling the consumer to **list the directory before concluding a record is absent** — because no naming rule can make two sessions of one product report themselves identically **✔ executed 2026-08-22** — `calibration/README.md:67` no longer gives unsuffixed examples; `:89-113` carries one rule with a three-step precedence order (served alias → family+product+version → family alone) and the directory-listing rule, and names the 2026-08-22 two-session divergence as the reason no naming rule closes it. Both skills follow |
| F4 | The read-only subagent boundary remains advisory even though Claude Code supplies an enforceable mechanism *(high)* | **CONFIRMED** — RV-8. The frontmatter grants `Write`, `Edit`, `Bash`, `Agent`; the rule at `:382-385` says "spawn it read-only where the tool grants let you" and never says how; an unnamed general-purpose subagent is `Tools: *`. The mechanism exists, is current on `2.1.239` (the reviewer's version figure is exact) and is present on this machine: a `tools:` allowlist in a subagent definition (`~/.claude/agents/gsd-plan-checker.md:4`), or a built-in read-only agent type. The reviewer marked this `THEORETICAL` because it declined to bill a subagent to demonstrate a documented default — that is honest, and the finding is documentary anyway, so nothing turns on it | **FIX NOW** — one paragraph at `skills/review-adjudication/SKILL.md:382-385`: name the mechanism (spawn with a tool allowlist that excludes `Write`/`Edit`/`NotebookEdit`, or a subagent type already defined that way), and say what to do when you cannot — record in the ledger that the second opinion ran unbounded, rather than leaving the reader to infer a configuration the skill never states **✔ executed 2026-08-22** — `review-adjudication/SKILL.md:396-412`: spawn with a tool allowlist excluding `Write`/`Edit`/`NotebookEdit`, the mechanism named (a subagent definition whose frontmatter declares `tools:`; an unnamed general-purpose subagent inherits everything), pick an agent type already defined read-only rather than the default, and where you cannot restrict tools, record in the ledger that the verifier ran unbounded |
| F5 | The K-3 envelope now permits arbitrary new files, not only test-runner caches *(low)* | **CONFIRMED** — RV-9, executed. "Write `REVIEW.md`, and change no file that was already here" bounds modification and not creation; an arbitrary `EXTRA.md` satisfies it literally while leaving an unauthorized non-cache artifact. `K-3` named the cache exception but loosened the surrounding rule | **FIX NOW** — `calibration/CALIBRATION-PROMPT.md:45-47`: "Write `REVIEW.md` and no other file, and change no file that was already here. A test runner leaving its own caches behind is expected and is not a violation." **Sequencing, not deferral:** this edits the fixed brief, so it moves the instrument digest. The only record on file is *already* stale and awaiting a re-run, so the cost is zero **if it lands before that re-run** — batch it with `F1`(a) and land both first **✔ executed 2026-08-22, first in the queue** — `calibration/CALIBRATION-PROMPT.md:45-47` now reads "Write `REVIEW.md` and no other file, and change no file that was already here." Instrument digest moved `da2a8d36e0ba` → `775e1cc8c43f`; the only record on file was already stale, so no record was lost |
| F6 | The advertised shorter expiry conflicts with the only record-filling instruction *(low)* | **CONFIRMED** — RV-10. `calibration/README.md:107` says "Shorten it freely"; `calibration/record-template.md:13`, the only file an operator fills, says "run date + 30 days"; `grep` finds no field anywhere recording a chosen window. Following the template defeats the choice; exercising the choice means disobeying it. Reviewer's `THEORETICAL` status is correct — nothing runtime reads the date | **FIX NOW** — one line. `record-template.md:13` → «YYYY-MM-DD — run date + the window you chose; 30 days is the default», and the row carries the window so a later reader can see which was used **✔ executed 2026-08-22** — `record-template.md:13`: «run date + the window you chose. 30 days is the default, not a requirement; say which you used and why if it was not 30» |
| F7 | The workload-gap rule supplies neither a threshold nor a place to record the compared workload *(low)* | **CONFIRMED** — RV-10. "Far larger" occurs once (`SKILL.md:90`) with no file, line, token or artifact threshold; the record has a prose standing caveat and no workload field; the ledger-template header has no size-gap field. An adjudicator satisfies the instruction by writing a sentence regardless of the facts, and a private replacement corpus cannot be reconstructed from a 12-character digest | **FIX NOW** — the option consistent with this project's own stance on unmeasured constants (`F13`: name the number honestly rather than invent a better one). Add a **workload field** to `calibration/record-template.md` (what the six cases actually are — file count and rough line count) and a **size line** to the ledger-template header; rewrite `SKILL.md:88-91` from "far larger" to "state both sizes and let the reader judge". No invented threshold. *The alternative — picking a multiple, e.g. 10× — is available and is named in the hand-off; it is not recommended, because nothing here measured it* **✔ executed 2026-08-22** — `record-template.md:15` gains a **Workload** row ("6 cases, 14 files, ~400 lines total"); `ledger-template.md:34-35` gains a **Workload gap** header line taking both numbers; `review-adjudication/SKILL.md:99-105` replaces "far larger" with state-both-sizes-in-numbers and forbids characterising the gap. No threshold invented |
| F8 | F15's replacement pointer does not currently resolve *(high)* | **CONFIRMED (partial)** — RV-11. *Established, all reproduced exactly:* the documented install yields five files and zero calibration artifacts; `/tree/main/calibration` returns 404; a user on the documented path cannot reach the procedure. *Refuted:* "search does not find the named public repository" and "the repository URL itself is unavailable" — the repo is public (`200` on both the HTML and the API), it is this clone's `origin`, and the 404 is because `calibration/` lives only on the unpushed local branch, **8 commits ahead of `origin/main`**. The consequence stands; the diagnosis does not, and the remedy it implies is the wrong one | **PENDING OWNER — proposed: FIX NOW by publishing.** Pushing `calibration-corpus-and-claim-cards` to `main` makes all four pointers resolve with **no document change at all**. That is a publishing decision, not an adjudicator's. See **Q6**. **Does not block** the rest of the queue. *Not recommended:* copying the corpus into each skill directory — it doubles the corpus, and an answer key adjacent to the skill is the adjacency the protocol exists to prevent |
| F9 | The inventory-enumeration fix failed on the next brief that used it *(low)* | **CONFIRMED** — RV-12, exact. `418` at the pinned blob against `416` in the brief, at both `3ec5baf` and the refreshed `2ddf6d3`; and `485` against `482` in the earlier version. *Bounding figure the report did not supply:* the other **eleven** inventory counts are all correct. The rule worked; one entry was **carried forward** across a refresh while its neighbour was corrected in the same pass. **Genuinely independent** — the only finding this round the brief did not name (§R2.4) | **FIX NOW** — `skills/adversarial-review-prompt/references/prompt-template.md:79-84`: the inventory is produced by running a count over the scoped paths **at the pinned commit**, and **a refreshed brief re-runs it rather than carrying numbers forward**. That last clause is the actual defect. Lands in the same paragraph as `R2-P1`'s fix. The spent brief itself is history and is not edited **✔ executed 2026-08-22** — `references/prompt-template.md:86-93`: counts are run against the pinned commit (`git show <commit>:<path> \| wc -l`), and **a refreshed brief re-runs the whole table** rather than carrying numbers forward, with this round's 418-as-416 named as the case. `R2-P1`'s clause landed in the same paragraph |

### Process and prompt defects

**R2-P1 — The refreshed brief incorrectly says its pinned endpoint is HEAD.** *Reviewer-raised,
`low`.* **Verdict: CONFIRMED** (RV-12, exact): `EXTERNAL-REVIEW-2-PROMPT.md:120` asserts "`e1fc88b`
is `HEAD`. There is nothing above the range", while `git rev-parse HEAD` returns `2ddf6d3` and
`git diff --name-status e1fc88b..HEAD` returns one line — the brief itself. **Cost to this run:
none** — the reviewer resolved the range correctly, filed it as a process finding rather than
silently, and audited the right commits. Note what this is: a *branch relation* re-entering a range
that commit `c054c1a` deliberately pinned to immutable commit IDs, precisely so a moving `HEAD`
could never make the range ambiguous. **Disposition: FIX NOW** — same template paragraph as `F9`:
state the range only by commit ID, and where `HEAD` is mentioned at all, produce it by running
`git rev-parse HEAD` at authoring time rather than asserting it.

**R2-P2 — The brief's §6 sub-questions did the finding again: about one of nine findings is an
independent discovery.** *Adjudicator-raised — not in the report; found by running the echo audit
this skill mandates at `SKILL.md:324-336`, which is itself one of the fixes under review.*
**Verdict: CONFIRMED** — §R2.4 records the per-finding audit with the query beside each result. Six
of nine findings are stated in the brief's own §6 sub-questions, two of them nearly verbatim
(`F6`, `F7`). Exactly one finding — `F9`, rated `low` — was reached without the brief pointing at
it. Round 1 was 10 of 15; this round is 6 or 7 of 9, so the ratio did not improve, it worsened.
**What this does and does not mean:** it does not weaken a single confirmed finding — each was
re-established here from primary evidence. It bounds what the reviewer's **silence** is worth: this
round supplies almost no evidence about the parts of the range nobody pointed at, and the fourteen
upheld claims are already discounted to nothing by the stale calibration record. Two rounds now say
the brief is doing the finding. **Disposition: PENDING OWNER — proposed: FIX NOW → settled as Q7 option A (§R2.10); ✔ executed
2026-08-22.** `references/prompt-template.md` gains **§6b — The unseeded pass**, required whenever a
claims list exists: the reviewer sets §6 aside, searches the range on its own reading, and reports
that pass under its own heading, with a considered "nothing" declared a result rather than a
failure. `adversarial-review-prompt/SKILL.md:144-151` requires the author to ask for it and carries
the two measured ratios as the reason. §6 is not weakened — both rounds say the directed questions
are where the confirmed defects come from. **Did not block.**

### Reviewer's could-not-verify items

**R2-CNV-1 — Digest byte-stability off macOS.** The reviewer did not establish that the command
returns an identical value under non-macOS `find`/`sort`/`xargs`/`shasum`; it reports that default
locale and `LC_ALL=C` agree on this host. **Verdict: COULD NOT DETERMINE** — not settled here
either; this session ran only macOS. It matters more than the reviewer allows: a digest that differs
by platform makes every record unverifiable by an operator on another OS, which is the same
end-state as `F2`. **Disposition: VERIFY** — run the documented command (and the `-print0` variant
from RV-4) on a Linux host under both `LC_ALL=C` and an unset locale, and compare against
`da2a8d36e0ba`. **Does not block** the queue, but it should be run before anyone treats a digest as
portable evidence.

**R2-CNV-2 — Whether an unrestricted subagent actually writes.** The reviewer declined to bill a
Claude subagent to demonstrate a documented default, and marked `F4` `THEORETICAL` rather than
overstate it. **Verdict: COULD NOT DETERMINE**, and correctly declared. **It is not material to
`F4`'s disposition:** the finding is documentary — the skill names no restriction mechanism — and
RV-8 establishes that documentarily, so the fix does not depend on the runtime demonstration.
**Disposition: VERIFY** — spawn one subagent of each kind and compare their available tool sets, if
anyone wants the runtime half on record. **Does not block, and is not required for the fix.**

**R2-CNV-3 — One agreeing re-score is not a scorer agreement rate.** The reviewer independently
re-scored all six archived outputs and agreed with all six recorded calls, then said plainly that
this is one agreeing score and not an inter-rater estimate. **Verdict: COULD NOT DETERMINE** — the
rate is still unknown. **The reviewer is right to disclaim it, and it is still the most this project
has ever had.** This session sampled `clean-copy-link` — the one case whose score is a judgement
rather than a lookup — read the archived report cold, and independently reached **FAIL (one high)**,
agreeing with both the record and the reviewer; the report's sole finding is explicitly rated
`high`, and the rule at `calibration/README.md:59` fails a clean case on any `critical`/`high`.
**Disposition: VERIFY** — two blinded scorers on the same archive, then repeat after a delay.
**Does not block.**

**Supersedes round-1 `CNV-3`,** which was ruled `COULD NOT DETERMINE` on the ground that "no raw
calibration reports, independently scored labels, edge-case examples or inter-rater results exist
anywhere in the repository; there is nothing to rescore." That ground no longer holds: the archive
exists, and **three independent scorers now agree** on the sampled case (original scorer, this
reviewer, this session). The original row stands as written; this entry records what changed.

### Disagreements with a prior internal review

**R2-D-1 — Claim 20: ledger §8's "largest gap" is historical.** The reviewer disputes round-1 §8's
statement that the largest gap under the round is that the calibration corpus has never been run,
arguing it is now historical and the larger current gap is operational: records cannot reliably
expire when the instrument changes (`F1`, `F2`) and cannot reliably be found by the consumers
(`F3`). **Verdict: CONFIRMED.** §8 was written before the run; the run has happened; the claim is
factually superseded by events. The replacement gap is supported by three findings confirmed above,
and by this session's own first-hand lookup failure recorded in the header. **Disposition: FIX NOW —
✔ executed in this ledger.** The durable act is the record itself: round-1 §8's largest-gap
statement is superseded as of 2026-08-22, and the current largest gap is that a calibration record
can be neither reliably expired nor reliably found. Round-1 §8 stands as written; this entry
supersedes it. No separate code change — `F1`/`F2`/`F3` are the code change.

### Disagreements between reviewers

Not applicable — one reviewer this round.

## R2.4 — Echo audit: what the brief had already named

Required by `skills/review-adjudication/SKILL.md:324-336`. Each finding was probed against the
**brief and the cover note** using **the finding's own identifiers**, not a paraphrase.

| Finding | Query | Result | Independence |
|---|---|---|---|
| F1 | `-print0`, `xargs`, `containing a space`, `excludes \`calibration/README.md\``, `how cases are scored` | brief `:223-224` and `:229-231` — both halves stated, including "what happens with a filename containing a space" and "If an operator changes how cases are scored, should every record survive that?" | **echo — none.** Executed verification of the author's own hypothesis |
| F2 | `recompute`, `compare the digest`, `consumer.*digest`, `corpus «commit»` | no line found for the consumer-omission half. Brief `:288`, `:383` name `ledger-template.md` as untouched and direct a sweep | **independent on its core half**, directed on the template half |
| F3 | `same filename`, `two different names`, `lookup misses`, `by filename`, `gpt-5.6-sol` | brief `:256-262` — the mechanism nearly verbatim, including "the lookup misses and the record reads as absent" and "or whether the scorer had to improvise" | **echo — none.** Its one novel sub-claim is the one that failed to reproduce |
| F4 | `read-only`, `restrict a subagent`, `instruction or a wish` | brief `:267-269` — "is that an instruction or a wish? Does the skill say anywhere how to actually restrict a subagent's tools" | **echo — none.** The brief also pre-authorized the web lookup at `:486` and pre-labelled it "a lookup rather than a discovery" |
| F5 | `envelope`, `change no file that was already here`, `violate it without noticing` | brief `:411-412` — "Does that resolve the contradiction or relocate it? … say whether a reviewer could now violate it without noticing" | **partial** — the question is the author's, the new-file route is the reviewer's |
| F6 | `Shorten it freely`, `run date + 30`, `shorter window` | brief `:313-316` — "still computes `Expires` as run date + 30 days with no way to record that a shorter window was chosen" | **echo — none.** Stated verbatim |
| F7 | `far larger`, `threshold at which this fires`, `measured how` | brief `:337-340` — "'Far larger' than what, measured how? … Is there any threshold at which this fires, or has an unfalsifiable instruction been added" | **echo — none.** Stated verbatim |
| F8 | `resolve for the skill`, `Reproduce the install`, `left to find it`, `404` | brief `:274-277` directs the install reproduction and asks whether the URL resolves; **no line found** for the 404 itself | **partial** — the observation is the reviewer's, and its diagnosis is wrong |
| F9 | `inventory`, `enumerated`, `416`, `418`, `line count` | brief `:63`, `:167` **contain the stale number itself**; nothing anywhere says it is wrong | **independent — the only one this round** |
| R2-P1 | `is \`HEAD\``, `nothing above the range`, `completely clean` | brief `:120` makes the false assertion; `:491-497` invites the reviewer to run the check and report a difference | **invited** — the brief asked for exactly this check |

**Score: 1 of 9 fully independent, 2 partial, 6 echoes.** Every confirmed finding stays confirmed —
each was re-established here from primary sources, which is what the rule requires. What is
discounted is the reviewer's coverage: outside the seams the brief named, this round establishes
almost nothing. Ruled as `R2-P2`.

## R2.5 — Reviewer's figures: what reproduced

Nine of nine executed figures reproduced **exactly**: the digest `da2a8d36e0ba`; the whitespace
mutation's two error lines, exit 0 and unchanged digest; `418` vs the brief's `416`; `485` vs the
earlier brief's `482`; `claude --version` `2.1.239`; the install's five files and zero calibration
artifacts; `/tree/main/calibration` 404; `git rev-parse HEAD` and the one-file diff above the range;
the envelope's literal satisfaction by an added `EXTRA.md`. The independent re-score of
`clean-copy-link` was sampled and agreed.

**Two claims failed to reproduce, and both are claims of *absence*:**

1. "search does not find the named public repository" — false. Public, `200` on HTML and API, and
   this clone's `origin` (RV-11). This is the reviewer's **top-ranked** finding, and it is the
   claim that determines what the remedy is.
2. `F3`'s "an alias not present in that self-report" — the record's verbatim self-report contains
   `gpt-5.6-sol` (RV-7). Strictly read against *this session's* self-report the sentence is true,
   but the record was open in front of the reviewer for claim 24 and the omission supports the
   inference the brief explicitly asked about ("or whether the scorer had to improvise").

**What that pattern is worth.** Everything this reviewer *executed* held up under repetition,
without exception — the executed half of this report earns real weight. Both failures are the same
shape: an absence asserted without running the check that would have settled it. That is the same
asymmetry this skill already records about authors certifying absence in their own briefs, now
observed in a reviewer. Weight its positive executed claims highly; verify every claim that
something does not exist.

## R2.6 — Claims examined and upheld — what was sampled

The reviewer adjudicated all 24 load-bearing claims: 10 refuted (each mapped to a finding above, or
to `R2-D-1`), 14 upheld. **Its calibration record is stale, so those fourteen are not coverage.**
Five were sampled independently here; the other nine stand **unverified**.

**Sampled: 5 of 14 · re-opened: 0.**

- **Claim 2** *(the counterweight to "agreement means failure")* — read `CALIBRATION-PROMPT.md:1-12`
  in order. The counterweight sits immediately after and names the pressure outright: "Do not go
  looking for something serious to say because the paragraph above told you agreement is failure."
  **Upheld.**
- **Claim 9** *(the pass-rule overclaim, corrected consistently)* — read both homes.
  `ANSWER-KEY.md:93-96` and `HOW-IT-WORKS.md:733-737` both now say "spared at least one of two
  correct artifacts", and both carry the tolerated-false-positive cost. No drift between them.
  **Upheld.**
- **Claim 18** *(disclosure complete)* — `git diff --name-status 8c1d737..e1fc88b` returns 24 paths;
  every one is accounted for by a ledger row, a disclosed consistency edit, the run archive, or the
  brief and cover note themselves. **No unaccounted path found.** **Upheld.**
- **Claim 21** *(`K-1` did not break the negative control)* — read `clean-copy-link` cold.
  `viewer.html` is 16 lines: no script, no external resource, no form, no input. Nothing a competent
  reviewer rates `high` or `critical`. The plan's "next to the page title" now resolves — the page
  supplies `<h1 id="page-title">` — and "no new files" describes the implementation, which the
  pre-existing `viewer.html` does not contradict. **Upheld.**
- **Claim 24 / CNV-3** *(the recorded scoring)* — sampled `clean-copy-link`, the one case whose score
  is a judgement rather than a lookup. Read the archived report cold: its sole finding is explicitly
  under `## High impact`, so the case is **FAIL** under `calibration/README.md:59`. Agrees with the
  record and with the reviewer. **Upheld.**

Unverified, recorded as such rather than as coverage: claims 3, 7, 8, 10, 12, 13, 15, 17, 23.

## R2.7 — Owner decisions required

### Q6 — How should the calibration corpus be made reachable from a normal install?

**What turns on it:** `F8`. A user following `README.md:118-122` today installs five files, none of
them calibration, and the URL the skills hand them returns 404 — because `calibration/` exists only
on an unpushed local branch that is 8 commits ahead of `origin/main`. The repository itself is
public and fine.

| Option | What it costs |
|---|---|
| **A — Push the branch to `main`** *(recommended)* | All four pointers resolve immediately, **with no document change at all**. Cost: it publishes the work, which the cover note says has not happened yet, and publishing the answer key is the recall exposure round-1 `F10` describes and `BACKLOG.md` §B-2 keeps open. That exposure is already accepted for the corpus; this adds the six archived model reports to it |
| **B — Ship the corpus inside each skill directory** | The install carries the procedure. Cost: the corpus is duplicated in two places and drifts; and an answer key sitting adjacent to the installed skill is exactly the adjacency `ANSWER-KEY.md:3-5` exists to prevent |
| **C — Leave it, and say so** | Zero work. Cost: the fix stays broken at its highest-frequency boundary until publication, and `F8` would need `ACCEPTED AS-IS` with your words on record |

**Recommendation: A.** It is the only option where the fix as written becomes true rather than
being rewritten, and the exposure it adds is an increment on one already taken.

**Blocks:** nothing. `F8` stays `PENDING OWNER` until answered; the other eight fixes are
independent of it.

### Q7 — Should the next brief keep naming the seams?

**What turns on it:** `R2-P2`, and what these reviews are actually buying. Two rounds now: round 1,
10 of 15 findings were echoes of the brief's sub-questions; round 2, 6 of 9, with exactly **one**
independent discovery — `F9`, rated `low`. Every finding is real and worth fixing. But a reviewer
that only ever confirms where it was pointed tells you nothing about anywhere else, and the parts of
this range nobody pointed at have now been through two audits without evidence either way.

| Option | What it costs |
|---|---|
| **A — Split the brief: a directed half and a blind half** *(recommended)* | Keep §6 as it is, and add an explicit unseeded pass — "here is the range, here are no questions" — scored separately. Cost: reviewer effort is finite, so the directed half gets less; and the blind half may return nothing, which is itself the datum currently missing |
| **B — Keep naming the seams** | Highest confirmed-defect yield per run, which two rounds have demonstrated. Cost: independent coverage stays near zero, and every future ledger must keep discounting the reviewer's silence to nothing — which makes calibration, whose only purpose is to price that silence, buy nothing |
| **C — Stop naming them** | Maximum independence. Cost: round 1 and round 2 both suggest the yield collapses; the author's suspicions are load-bearing and would go unchecked |

**Recommendation: A.** The echo rule already discounts directed agreement to zero independent
discovery; A is the cheapest way to stop that discount from applying to the *whole* report.

**Blocks:** nothing. This changes the next brief, not this queue.

## R2.8 — Amendments queued

The `FIX NOW` queue — **eight rows plus `R2-P1`, plus row 10 from Q7. All executed 2026-08-22**, on
the owner's authorisation recorded verbatim in §R2.10 and only after it was recorded. The
adjudication above was written before any fix was applied; this section is the backfill. Two of them are cheap doc edits in
sites this round already touched, and none is deferred: no `FIX LATER` row exists this round, so no
new backlog artifact was created. `BACKLOG.md` §B-1 and §B-2 are unchanged.

**Sequence matters for exactly two of them.** `F1`(a) and `F5` touch files inside the instrument
digest, so they move it. The only record on file is already stale and awaiting a re-run, so landing
them **before** that re-run costs nothing and landing them after costs the whole re-run. Everything
else — `F1`(b), `F2`, `F3`, `F4`, `F6`, `F7`, `F9`, `R2-P1` — touches operator documentation or the
skills, which `K-6` deliberately excluded from the digest, and expires nothing.

| # | Row | Site | Effect on the instrument digest |
|---|---|---|---|
| 1 | F5 | `calibration/CALIBRATION-PROMPT.md:45-47` | **moves it** — land before the re-run |
| 2 | F1(a) | `calibration/record-template.md:14`, `calibration/README.md:112` | none (`-print0` returns the same value, RV-4) |
| 3 | F1(b) | `calibration/README.md:46-60` | none |
| 4 | F3 | `calibration/README.md:67`, both `SKILL.md` | none |
| 5 | F6 | `calibration/record-template.md:13` | none |
| 6 | F7 | `record-template.md`, `ledger-template.md`, `review-adjudication/SKILL.md:88-91` | none |
| 7 | F2 | both `SKILL.md`, `ledger-template.md:31` | none |
| 8 | F4 | `review-adjudication/SKILL.md:382-385` | none |
| 9 | F9 + R2-P1 | `references/prompt-template.md:79-84` | none |
| 10 | R2-P2 *(Q7→A)* | `references/prompt-template.md` §6b, `adversarial-review-prompt/SKILL.md:144-151` | none |

**Instrument digest after the queue: `da2a8d36e0ba` → `775e1cc8c43f`.** Two instrument files moved —
`CALIBRATION-PROMPT.md` (`F5`) and `ANSWER-KEY.md` (`F1`(b)'s rule move). The only record on file was
already stale and awaiting a re-run, so nothing was lost; the record's banner was updated to name the
new value rather than continue asserting the old one. Both fixture suites re-run green in a scratch
copy afterwards: `5 passed in 0.01s` and `3 passed in 0.01s`.

`F8` is executed separately — it is a publish, not an edit; see §R2.11.

## R2.9 — What this round did not settle

- **Whether the corpus measures anything outside the seams a brief names.** `R2-P2`. Two rounds, one
  independent discovery between them at `low` impact. This is now the largest open question about
  the method, and it is larger than any single row above.
- **Whether the digest is portable.** `R2-CNV-1`. Unrun off macOS; a platform-dependent value would
  reproduce `F2`'s end-state by a different route.
- **The scorer agreement rate.** `R2-CNV-3`. Three independent scorers now agree on the sampled
  case, which is three more than existed a day ago and still not a rate.
- **Nine of the reviewer's fourteen upheld claims.** Unverified, and not coverage, because the
  reviewer's calibration record is stale.
- **`BACKLOG.md` §B-1 and §B-2** remain open and untouched: no corpus-drift gate exists, and no
  construction procedure for a private replacement corpus exists. `F1` and `F2` would both be
  cheaper to keep correct if §B-1 existed.

Nothing in this round establishes that the work is complete, correct, or ready to publish. That is
the owner's call, and it is not made here.

## R2.10 — Locked owner decisions from this round

**2026-08-22 — owner, verbatim:**

> "ok proceed with recommended options"

Following a hand-off that named both questions with their options, their costs and a stated
recommendation for each. Taken as **Q6 → option A**, **Q7 → option A**, and as the explicit
authorisation for the `FIX NOW` queue in §R2.8 to be executed. Recorded **before any fix was
applied.**

- **Q6 (F8) — settled: option A.** The branch is published to `main`, which makes all four in-skill
  calibration pointers resolve with no document change. The recall exposure this adds — the six
  archived model reports joining an already-public answer key — is accepted, and remains tracked at
  `BACKLOG.md` §B-2. **Sequenced last**, after the queue lands, so what is published is the repaired
  state rather than the state carrying nine confirmed findings.
- **Q7 (R2-P2) — settled: option A.** The brief template gains an unseeded pass alongside its
  directed §6, scored separately, so that a future round's independent coverage is not structurally
  zero. This becomes queue row 10.
