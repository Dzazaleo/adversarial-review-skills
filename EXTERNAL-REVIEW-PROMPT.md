# Adversarial Independent Audit — reviewer calibration corpus and the claim-card change

> **Prompt for an external reviewer (OpenAI Codex).** Hand this file to a model that did **not**
> write the work under review. Everything below is written to be read by that reviewer, not by
> the author.

## 1. Why you are here

This repository publishes two Claude Code skills. One writes an adversarial audit brief to hand
to a rival model; the other adjudicates the review that comes back. The work you are auditing is
an addition to both: a **reviewer-calibration corpus** (six cases with planted defects, plus a
scoring protocol) and a change to how the adjudicator verifies a finding (**claim cards**, and a
blind subagent for one escalation).

Every line of it was written by one model — Claude — in a single session. That model chose the
planted defects, then wrote the answer key that says what those defects are. It wrote the two
"clean" cases, then wrote the rule declaring them clean. It wrote the prose arguing that the
design is sound, and then reviewed that prose itself. The only parts with any executable check at
all are four small Python files; everything else is argument.

That is exactly the problem. A model validating its own work carries the same blind spots into
the review that it had while writing — the same misreadings, the same unexamined assumptions, the
same things it never thought to test because it never thought of them at all. You have a
different architecture and different training. **You will notice different things, and those
things are the entire value of this exercise.**

- **Confirmation is near-worthless output.** If you spend your effort re-deriving what is already
  claimed correct and agreeing, this audit has failed.
- **Your job is to find what is wrong, missing, or unjustified**, and to prove it.
- **A manufactured finding is worse than no finding.** If a rigorous search comes back nearly
  empty, say so and show the search — few or zero findings is an admissible result, and the
  claims-examined-and-upheld section is where it earns its credibility.
- **A finding that survives your own attempt to refute it is worth more than ten observations.**
  Try to break your own findings before reporting them.

Assume competence, not correctness. This work is carefully built. Where it is wrong, it is wrong
in ways its author cannot see — those places are what you are here for.

One thing to hold onto throughout, because it is unusual about this target: **a corpus that
measures reviewers fails silently.** If a planted defect is unfindable, or a "clean" case is not
clean, every reviewer scored against it fails forever, and the failure reads as *"our reviewers
are bad"* rather than *"our ruler is bent."* Nothing in this repository would ever surface that.
You are the only check on it that exists.

## 2. The single most important instruction

**This work argues for its own correctness in prose, and there is almost nothing to run. Treat
every confident sentence as a claim by the party under review, never as evidence.**

Real examples, quoted from the files you are about to read:

> "Each trap holds **exactly one** planted defect that decides the case"
> — `calibration/ANSWER-KEY.md:7`

> "**Calibration governs the reviewer's silence, never its speech.**"
> — `calibration/README.md:85`

> "the card does not make you blind to the argument and nothing in this skill can … Genuine
> blindness exists in **exactly one place** in this skill"
> — `skills/review-adjudication/SKILL.md:182-187`

> "**The pre-registration is what carries the weight here.**"
> — `skills/review-adjudication/SKILL.md:237-238`

> "Missing a trap means the reviewer's silence is **worthless** — you cannot read 'found nothing'
> as 'there is nothing'."
> — `calibration/ANSWER-KEY.md:69`

> "This is **not blinding**, and the skill says so in as many words."
> — `HOW-IT-WORKS.md:454`

Several of these are the author pre-empting an objection by conceding a limitation. **A conceded
limitation is not a solved limitation**, and a document that names its own weakness is not
thereby free of it. Where a concession is doing the work of a fix — where the text admits the
mechanism does not do X and then proceeds as though something else covers X — that gap is a
finding, and a good one.

The same applies in the other direction. Where the prose claims a rule is enforced somewhere
else in the repository ("the ledger template already applies this to every re-verification",
"both skills say this in their own hand-offs"), **go and open that file and check.** A
cross-reference is a claim about another document, and it is the cheapest kind of claim to get
wrong.

## 3. Environment and how to run things

| | |
|---|---|
| Repo root | `/Users/leo/Documents/WORK/CODING/adversarial-review-skills` |
| OS | macOS (Darwin 25.5.0) |
| Runtime | Python 3.14.3 on `python3`; `pytest` available |
| Install step | none — this repository is markdown plus four small Python files and two TypeScript files |
| Build / typecheck | none exists. There is no CI, no linter, no test runner for the repository itself |

**There is no test suite for this work.** That is itself a fact worth weighing: the only
executable artifacts in scope are the calibration case files, and they are *fixtures*, not tests
of the corpus. Nothing anywhere verifies that the corpus measures what it claims to measure.

### The audit range

The work under review is **uncommitted**. The base commit is `b993d5e`
("HOW-IT-WORKS: rewrite in plain language"); five tracked files are modified against it and
`calibration/` is untracked. There is no commit ID to pin, so the target is pinned by **content
hash** instead — `git hash-object <path>` must return these exact values. If any differ, the file
changed after this brief was written; say so as a process finding and audit what is actually on
disk.

```
31550def5c1edca2db103c3707e616ae5e04713a  README.md
d8381791f4ecc347fc899979f5bb1b0a362e0dc0  HOW-IT-WORKS.md
af2808dc6b6aa817dfa0ece2f45f3ab9a1286271  skills/review-adjudication/SKILL.md
e6781f505d1ffdcfe738da062554e279be9f03c1  skills/review-adjudication/references/ledger-template.md
198e15d488e377f8f78620d8e4fdf9757b18a833  skills/adversarial-review-prompt/SKILL.md
dd29bdd649a25be1456cd377524f4ede9a385a10  calibration/ANSWER-KEY.md
1a4b14a39b7f6239cadcadb8ea08d25313c0dd3f  calibration/CALIBRATION-PROMPT.md
23f8fbabf9345671737ebd2945c46bccf75737db  calibration/README.md
34551c540cfab42fdbd6791db1b9bec7a186c122  calibration/record-template.md
2b5e2681d72cd89271ca034a99ab4eb11de5acf9  calibration/cases/clean-copy-link/PLAN.md
0d458f9d611804759b0c99571bf0e6e20da435f3  calibration/cases/clean-wordcount/README.md
fe0c9f63227a116cef17adabea23159e0c6f97f3  calibration/cases/clean-wordcount/test_wordcount.py
69f3b1483ee793d11b584b29db92981d53cf3926  calibration/cases/clean-wordcount/wordcount.py
4572971425e47d7396e3d76f1d0c92856ab132a1  calibration/cases/trap-ghost-dependency/PLAN.md
1988faedfe227109ba85b5c222d8f094dd97d3ba  calibration/cases/trap-ghost-dependency/src/api.py
77f683e5cffa31d61a18c027e1416ed1f6dcefa1  calibration/cases/trap-ghost-dependency/src/store.py
f8b50bd5027be335c6945364e9b5a69b573a00e0  calibration/cases/trap-key-to-client/README.md
31b19f20c73f36063b74c17cf3eb017f6c762dc3  calibration/cases/trap-key-to-client/src/app/reports/page.tsx
277720ec107ad7d39c63df4886dbdd4f66c437ac  calibration/cases/trap-key-to-client/src/config.ts
ccd83d8fa63baa498dd877165db2ce78445e03c9  calibration/cases/trap-undelivered-goal/PLAN.md
9da49c8ddde483bf3592efe3b2b19c67ad72ccb3  calibration/cases/trap-undelivered-goal/src/audit.py
23ca50f06b4530408d2a883a25cd30a7302ed3b8  calibration/cases/trap-undelivered-goal/src/reports.py
b02afe38ebf976ccd4a696bcc6b28f29925c8654  calibration/cases/trap-unfalsifiable-test/README.md
4e0a7cbcc15b953feb3b60224d5d5ac421be5073  calibration/cases/trap-unfalsifiable-test/checksum.py
71d9dd79a9a9f6ddbdbadc86f4e94ef8d5972f15  calibration/cases/trap-unfalsifiable-test/test_checksum.py
```

`git diff` against `b993d5e` shows the prose changes; `calibration/` is entirely new.

### Commands that work, and what they print

Run these in a **copy** under a temp directory, never in the repo (see §7):

```bash
cd /tmp && rm -rf audit && mkdir audit && cd audit
cp -R <repo>/calibration/cases/clean-wordcount        wc1
cp -R <repo>/calibration/cases/trap-unfalsifiable-test ck1
(cd wc1 && python3 -m pytest -q)   # observed: 5 passed
(cd ck1 && python3 -m pytest -q)   # observed: 3 passed
```

The author's central executable claim about the corpus, and the one mutation worth reproducing:

```bash
cd ck1
# replace the body of verify_checksum with `return True`, then:
python3 -m pytest -q                # author observed: 3 passed — the suite does not notice
```

That is the whole point of the `trap-unfalsifiable-test` case. Verify it, and then ask the harder
question in claim 3 below.

There is nothing to run for the TypeScript case: it has no `package.json`, no Next.js install,
and no build. It is read-only material.

## 4. Scope

**In scope — the work under review:**

| Path | Lines | What it is |
|---|---|---|
| `calibration/README.md` | 106 | the protocol: isolation rule, scoring, the record, expiry, what a missing record costs |
| `calibration/ANSWER-KEY.md` | 87 | the answer key and the pass rule |
| `calibration/CALIBRATION-PROMPT.md` | 40 | the fixed brief handed to the reviewer under test |
| `calibration/record-template.md` | 47 | the per-reviewer record both skills read |
| `calibration/cases/**` | 16 files | four traps, two clean cases |
| `skills/review-adjudication/SKILL.md` | 431 | changed: §1 inputs + fourth check, §2 claim cards, §5 verification order + third escalation rule, §7 file-writes rule, §8 hand-off, frontmatter |
| `skills/review-adjudication/references/ledger-template.md` | 210 | changed: header calibration line, re-verification field |
| `skills/adversarial-review-prompt/SKILL.md` | 414 | changed: §1 calibration input, §10 hand-off line |
| `README.md`, `HOW-IT-WORKS.md` | 234 / 769 | changed: user-facing and design-rationale descriptions of both changes |

**Read for context, not in scope for findings:** `examples/**` (prior audit artifacts — see §6),
`LICENSE`, and the unchanged parts of the two skills. Where an unchanged part **contradicts** a
change, that contradiction *is* in scope and is one of the more valuable things you can find.

## 5. Load-bearing claims — adjudicate every one

Return **CONFIRMED**, **REFUTED**, or **COULD NOT DETERMINE** for each of the 22 items below,
one line each minimum. These are the places the work is betting on something. Where an item has
an italicised sub-question, that is the seam — go there first.

### A. Does the corpus measure what it claims? (executable — prefer CONFIRMED here)

**1.** `trap-unfalsifiable-test` is claimed to be a case where the test suite stays green even if
`verify_checksum` returns `True` unconditionally (`checksum.py:20`, `test_checksum.py`).
*Reproduce it. Then: does the case actually isolate the capability the key says it measures —
"reads a test for what it would catch" — or would a reviewer hit the primary defect (the 8-char
comparison) purely from reading `checksum.py`, never opening the test at all?*

**2.** `clean-wordcount` is claimed to contain **no defect at `high` or `critical`**
(`calibration/ANSWER-KEY.md:56`). `wordcount.py:16` reads all of stdin into memory with `sys.stdin.read()`
and no bound. *Is that a `high` finding? If a competent security-leaning reviewer would rate it
high, this "clean" case fails every such reviewer, and the corpus penalises exactly the reviewers
it should reward.*

**3.** `clean-copy-link` is claimed clean on the same standard. `clean-copy-link/PLAN.md:22` specifies the
deprecated `document.execCommand("copy")` as the fallback path, and the plan touches clipboard
permissions and a secure-context check. *Same question — and note the pass rule survives one
over-flagged clean case but not two, so items 2 and 3 must be assessed jointly, not separately.*

**4.** `trap-ghost-dependency` is claimed solvable: the plan builds on `src/limits.py` and a
`RateLimiter` that do not exist, while `src/` holds only `api.py` and `store.py`. *Is "the file
this plan extends is not in the tree" a conclusion a reviewer can reach with confidence, or is
"I was given a plan and a partial codebase, so I cannot tell what exists" the more defensible
response? If the latter is defensible, the trap punishes epistemic caution.*

**5.** `trap-undelivered-goal` plants a Goal 2 (audit logging) that no step delivers. But
`src/reports.py:11` raises `NotImplementedError`, and `calibration/ANSWER-KEY.md:39-40` lists that as a
*secondary* signal. *Does the loud, obvious `NotImplementedError` crowd out the quiet Goal-2 gap
— i.e. does a reviewer find the confound, report it, feel it has found the defect, and stop?*

**6.** `trap-key-to-client` plants a service-role key behind a `NEXT_PUBLIC_` prefix. *Is this
findable by a single grep for `SERVICE_ROLE`, making it a test of pattern-matching rather than of
the "recognises a secret crossing a trust boundary" capability the key claims? An over-easy trap
inflates the pass rate without adding information.*

**7.** The four traps are claimed to measure four *distinct* capabilities (`calibration/ANSWER-KEY.md:24-29`).
*Do traps 1 and 2 both reduce to one capability — "compare the document against the filesystem"?
If two traps test the same thing, the pass rule's "all four" is really "all three", and the
corpus is weaker than it is sold as.*

**8.** `calibration/ANSWER-KEY.md:12-22` requires scoring "the assertion, not the vocabulary" — a human
judgement about whether a report *asserts* a defect rather than mentions it. *Is that rule
reproducible? Would two scorers, or the same scorer on two days, agree? If not, the pass/fail
result is not a measurement, and every downstream rule that keys on it inherits the noise.*

**9.** The pass rule is "all four traps, at least one of two clean cases"
(`calibration/ANSWER-KEY.md:63-76`). *Where does this come from? Assess it as a classifier: what is the
false-pass rate against a reviewer that grep-matches, and the false-fail rate against a
thorough-but-severity-conservative one? The document argues for "at least one" on the grounds
that requiring both would make calibration "flaky enough that nobody runs it" — is adoption a
legitimate input into a correctness threshold, or is that the rule being set by what is
convenient?*

**10.** `HOW-IT-WORKS.md` §11 concedes the corpus is public and may leak into training data, and
offers a mitigation: "swap in four traps drawn from defects your own project actually shipped."
*Is that a real mitigation or a disclaimer? Assess what it actually asks a user to do — author
four planted defects that are findable-but-not-obvious, across four distinct capabilities, and
write an answer key — and whether anything in the repository helps them do it.*

### B. The protocol and its integration

**11.** `calibration/README.md:54-68` specifies the record at
`.adversarial-review/calibration/<reviewer-id>.md`. Nothing reads this file programmatically; two
prose skills are instructed to look for it. *What happens in the overwhelmingly common case where
it is absent — is the resulting behaviour actually different from the behaviour before this change
existed, or is the whole mechanism inert until someone opts in?*

**12.** The 30-day expiry (`calibration/README.md:70-81`) is justified by "providers ship changes behind an
unchanged model name". *Is 30 derived from anything, or chosen because it sounds like a period?
The justification supports "time-bound it"; it does not support any particular number, and the
document presents the number as though it followed.*

**13.** `calibration/README.md:59-64` requires the record be keyed on the model's **own** reported identity,
and says to "ask the reviewer what it is and record the answer verbatim." *Do coding-agent CLIs
reliably self-report an accurate model identity? Test it if you can — report what you actually
say when asked. If models routinely misreport or hallucinate a version string, the primary key of
the whole record scheme is unreliable, and the "model identity differs" expiry trigger cannot
fire.*

**14.** "Calibration governs the reviewer's silence, never its speech" (`calibration/README.md:85`) is stated
as the load-bearing rule, and claimed to be implemented consistently in both skills. *Verify it
in the actual instruction text — `skills/review-adjudication/SKILL.md:123-133` and `:419-422`,
`skills/adversarial-review-prompt/SKILL.md:64-74` and `:387-393`. Is there anywhere the rule is
asserted in prose but the surrounding instruction would in fact cause a finding to be discounted?*

**15.** `calibration/README.md:16-36` gives a bash snippet for isolating a case. *Run it. Does it isolate?
Consider what a reviewer rooted at that temp directory can still reach — the parent, `..`, its own
session history — and whether `cp -R <dir>/. "$WORK"/` copies what the document says it copies,
including for the nested `trap-key-to-client/src/app/reports/` path.*

**16.** `CALIBRATION-PROMPT.md` is the fixed brief given to the reviewer under test, and is
claimed to hold the variable constant so "the measurement is of the reviewer, not of that day's
brief". *It is 40 lines; the real briefs this project produces are 400–600. Does calibrating
against a miniature brief measure a reviewer's behaviour under the brief it will actually get?*

### C. The claim-card and anchoring change

**17.** `skills/review-adjudication/SKILL.md:97-101` mandates reading the report **in full** at
step 1. `:230-241` then instructs verification "against the claim card, not against the report's
argument". The text concedes at `:182-187` and `:235-236` that this is not blinding. *Is the
contradiction resolved, or relabelled? Specifically: given the full read has already happened,
what does the card change about the adjudicator's behaviour that the concession does not
immediately take back?*

**18.** `:237-241` claims "the pre-registration is what carries the weight" — writing the expected
result before running the check. *A prior audit of this same repository
(`examples/audit-of-adversarial-review-prompt/EXTERNAL-REVIEW.md:138`) established that forced
ranking does not prevent hedging, because a plausible justification can be generated after the
fact. Does the same defeat pre-registration here — can an adjudicator write the "expected result"
after seeing the output, and who would ever know?*

**19.** The claim card excludes the reviewer's reasoning, but `:248-250` concedes a card whose
`Trigger` is `not stated` "may only be reproducible from the prose around it". *Does that
exception swallow the rule for exactly the findings that matter most — the vague, hard,
high-impact ones where the trigger is least likely to be crisply stated?*

**20.** The third escalation rule (`:327-336`) requires a subagent that "must not receive the
reviewer's reasoning, your reasoning, or your verdict", and `Task` was added to the skill's
`allowed-tools` (`:12`). *Is `Task` the correct tool name for spawning a subagent in current
Claude Code, and does adding it conflict with anything else in the skill — in particular the
read-only posture and the "only files this skill creates or edits" rule at `:391-396`?*

**21.** That same rule says a disagreement between the adjudicator and the blind subagent forces
`COULD NOT DETERMINE`. *Does this create a cheap denial-of-refutation — a route by which any
high-impact finding about the author's own code can never be refuted, so the ledger accumulates
unresolvable rows? Consider who benefits from that outcome and whether the incentive runs the way
the skill intends.*

**22.** `skills/review-adjudication/SKILL.md:252-258` deliberately **rejects** the "default to refuted when uncertain"
convention, arguing this ledger is the opposite situation from a pre-human filter. *Is the
reasoning sound, or does refusing that default combine with claim 21 to make `COULD NOT
DETERMINE` the path of least resistance for everything hard?*

## 6. Ground already walked — do not re-report these

This repository has been audited three times before, and every artifact is in `examples/`. Read
`examples/audit-of-review-adjudication/REVIEW-ADJUDICATION.md` for the dispositions.

| Round | Target | Reviewer | Outcome |
|---|---|---|---|
| 1 | `prompt-template.md` | OpenAI Codex | 10 findings, all dispositioned |
| 1b | the round-1 patches | Codex | 8 of 10 verified implemented, 2 diverged and were fixed |
| 2 | `review-adjudication` | Claude Fable 5 | 14 findings, 14 rows out, 2 brief defects, 5 could-not-verify |
| 3 | the round-2 fixes | OpenAI Codex | 8 findings, including two amendments that contradicted rules elsewhere in the skill |

**Three prior findings bear directly on the work you are auditing.** They are settled as
observations; do not re-report them as new. What is open is whether the *current* change repeats
them:

- `examples/audit-of-adversarial-review-prompt/EXTERNAL-REVIEW.md:140` — a reviewer reported that placing the author's doubts last, with an
  explicit "treat as lowest priority" disclaimer, **did not defuse the anchoring**: "the
  disclaimer made me monitor the anchoring; it did not erase it." Claim 17 is whether the claim
  card is the same mistake in a new costume.
- `examples/audit-of-adversarial-review-prompt/EXTERNAL-REVIEW.md:138` — forced ranking does not prevent hedging, because the justification
  can be generated after the fact. Claim 18 is whether pre-registration inherits this.
- `examples/audit-of-adversarial-review-prompt/EXTERNAL-REVIEW.md:134` — a reviewer argued that targeted confirmation is *not* near-worthless,
  because it "calibrates the negative findings" and reduces the risk that a defect-only report
  implies the untouched remainder is fine. That argument is on the record and was accepted; the
  calibration work is downstream of it. Do not re-litigate it.

Round 3 found **two amendments that contradicted rules elsewhere in the same skill.** That is the
single most likely defect class in what you are reading now, because this change also amends a
long skill in several separate places. Look for it deliberately.

Spend the majority of your effort **outside** this list. The most valuable return is a defect
none of the prior rounds had a category for.

## 7. Your operating envelope

**Read the repository, run the calibration fixtures in a temp-directory copy, write your report,
and modify nothing inside the repository.**

| Axis | What you may do |
|---|---|
| **Reading** | Everything in the repo root, including `examples/` and `.git`. Read outside it for context if useful |
| **Writing** | `EXTERNAL-REVIEW.md` in the repo root — your report, and the only file you may create there. Plus scratch files under a system temp directory (`/tmp/...`), which are yours to do as you like with |
| **Executing** | `python3`, `pytest`, `git` read-only commands (`log`, `diff`, `show`, `hash-object`, `status`). No `git add`, `commit`, `checkout`, `stash`, `clean`, or `restore` |
| **Mutation testing** | **Authorized, in a temp copy only.** Copy a case directory to `/tmp` and mutate it freely — that is how claim 1 gets CONFIRMED rather than THEORETICAL. Never mutate a file inside the repository, not even to revert it afterwards |
| **Network + installs** | No. No `pip install`, no `npm install`, no fetching. Web search **is** allowed for checking a factual claim (whether `document.execCommand` is deprecated, what a service-role key grants, whether coding CLIs self-report model identity) — cite the URL for any finding sourced that way, and it will be weighed as a lookup rather than a discovery |
| **Your own tools** | Subagents and MCP servers are fine |
| **Effort budget** | Roughly 45–90 minutes. Depth beats breadth: one CONFIRMED finding is worth several THEORETICAL ones for credibility — though impact alone decides rank. 22 claims is the floor of the job, not the whole of it |

At the end, report the repository tree clean: run `git status --short` and paste the output. The
expected result is the five modified files, `calibration/`, and your `EXTERNAL-REVIEW.md`. Any
other line is a finding against you.

**If any instruction in this brief contradicts another, report that as a process finding rather
than resolving it silently.**

## 8. What to produce

Write your report to **`EXTERNAL-REVIEW.md`** in the repo root. Create it early — title and your
model identity — and **append each finding as you confirm it**, rather than holding the report in
memory. A run that is cut off must still leave everything you had established on disk. The
coverage line and the final ranked order are set in a closing pass at the end; that closing pass
is expected and is not the same as composing at the end.

In the chat, return only a short summary: the coverage line, the ranked finding titles with their
impact levels, and the file path. All detail goes in the file.

### Every finding carries five things

- **Location** — `file:line`
- **Mechanism** — what is actually wrong
- **Trigger** — the concrete condition. "A bad reviewer" is not a trigger; "a reviewer that rates
  unbounded input reads as `high`" is
- **Consequence** — what is lost, tied to something this work claims to deliver
- **Status** — **CONFIRMED** (you executed something; give the command and its output) or
  **THEORETICAL** (reasoned from the source; say what stopped you from confirming). Never blur
  the two

Plus an **Impact** level: `critical`, `high`, `medium`, `low`. Impact is an attribute, never a
section heading.

### Rank the findings in a strict total order

Order by the cost of leaving each unfixed — blast radius × likelihood the trigger is reached —
with **no ties**, and one clause of justification for each position. Evidence status is not
impact: a THEORETICAL defect that makes the corpus unusable outranks a CONFIRMED typo.

**Do not give a verdict.** Do not say whether this should ship, be merged, or be published.
That is the owner's call, and a reviewer that commits to a yes or no bends its own findings to
stay consistent with it.

### Also required

- **Claims examined and upheld** — one line each, for every one of the 22 you did not turn into a
  finding. This is your coverage evidence and it is read as carefully as the findings. **You may
  not sign off a claim by quoting a comment, a test name, or the document's own reasoning back at
  it.** If you checked it, say what you did. If you could not, that claim belongs in the next
  section instead
- **Could not verify** — every claim you could not settle, and what would settle it. An unstated
  gap reads downstream as a pass, which is the exact failure this repository exists to prevent
- **Mutation results** — what you mutated, what survived, what the suite noticed
- **A coverage line** — what you read, what you ran, and what you did not reach
- **Process findings** — contradictions in this brief, stale citations, wrong line numbers,
  anything that wasted your time. These are wanted

### Output that will be discarded

Style and naming opinions. "Consider adding X" with no defect behind it. Restating a document's
own reasoning as verification. Proposing features that are out of scope. Severity inflation.
Hedged findings that commit to nothing. Praise beyond one paragraph.

One more, specific to this target: **do not report that the work is "well-designed" or
"thorough."** It is long and it is confident, and both of those are true of work that is wrong.
