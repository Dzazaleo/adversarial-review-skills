# External Review 4 (Grok) — audit of the round-3 fixes
Reviewer identity: xAI Grok 4.6, Grok Build TUI / Grok Code product, high reasoning effort; served model alias as given to this session: `Grok 4.6` (system prompt: "You are Grok 4.6 released by xAI"). No served-alias string beyond that was exposed.
Audit baseline: findings assessed against `fe9bbac..540c60a`; `HEAD` observed at `0d65b51f029c005a69b007b4ee907117232cda80` (`0d65b51 Add the Grok round-4 brief, and blind the two reviewers to each other`). `git diff --stat fe9bbac..540c60a` reproduced as **7 files changed, 951 insertions(+), 19 deletions(-)** — matches the brief.

Contamination disclosure: I have not opened `EXTERNAL-REVIEW-4-PROMPT.md`, `EXTERNAL-REVIEW-4-COVER-NOTE.md`, or `EXTERNAL-REVIEW-4.md`. I saw those three filenames in a directory listing and in `git status` (`?? EXTERNAL-REVIEW-4.md` is untracked; the other two exist on disk). I have not read their contents. I am using `EXTERNAL-REVIEW-4-PROMPT-GROK.md` as the brief.

---

## Coverage

**Read (in-scope, at `540c60a` and at `HEAD` where they differ):**
`skills/review-adjudication/SKILL.md` (572), `skills/adversarial-review-prompt/SKILL.md` (497), `skills/adversarial-review-prompt/references/prompt-template.md` (467), `calibration/README.md` (162), `BACKLOG.md` (93), `EXTERNAL-REVIEW-3.md` (119), `REVIEW-ADJUDICATION.md` (2480 lines at `540c60a`; 2601 at `HEAD` — the brief's "2,466 total" did not reproduce; see process finding 13). Round-3 section and the post-commit corrections §R3.15–§R3.16. Diff `fe9bbac..540c60a` for all seven files.

**Read (context, not under review):** `skills/review-adjudication/references/ledger-template.md` (217), `skills/adversarial-review-prompt/references/cover-note-template.md` (91), `README.md` (the residual-doubts paragraph at `:149-155`), `HOW-IT-WORKS.md` (opening), round-1/2 rows of `REVIEW-ADJUDICATION.md` (in particular round-2 `F4` at `:1468` and round-2 `F1` at `:1465`), `calibration/record-template.md:14`, `.gitignore`, YAML frontmatter of both skills.

**Did not read:** `EXTERNAL-REVIEW-4-PROMPT.md`, `EXTERNAL-REVIEW-4-COVER-NOTE.md`, `EXTERNAL-REVIEW-4.md`. Out-of-scope corpus cases, `EXTERNAL-REVIEW.md` / `EXTERNAL-REVIEW-2.md`, `examples/`.

**Ran:**
- `git diff --stat fe9bbac..540c60a` → `7 files changed, 951 insertions(+), 19 deletions(-)`
- YAML parse of both `skills/*/SKILL.md` → both `allowed-tools: ['Read', 'Write', 'Grep', 'Glob']`
- Digest as prescribed at `calibration/record-template.md:14` → `9fb019996546`
- Digest with `! -path '*__pycache__*'` (what §R3.15 ran) → `775e1cc8c43f`
- Digest via `git ls-files` of the same paths → `775e1cc8c43f`
- `python3 -m pytest -q` of the two fixtures, copied to `/tmp/adv-cal-test` so the repo was not written → `8 passed in 0.01s`
- Word/char heuristics for the 5,000-token cut (no Anthropic tokenizer available; no installs)
- Repository-wide grep: `COULD NOT VERIFY`, `blind`/`never saw`, `overwrite`, `continue`/`one word` in the prompt skill
- Official Claude Code docs (URLs cited per finding): [skills](https://code.claude.com/docs/en/skills), [permissions](https://code.claude.com/docs/en/permissions), [tools-reference](https://code.claude.com/docs/en/tools-reference.md)

**Could not reach:** an Anthropic tokenizer (tiktoken and `anthropic` Python packages absent; brief forbids installs), so the exact 5,000-token line is bounded, not pinned. Empirical spawn of a Claude Code subagent (already `R3-CNV-1`). Whether a live Claude Code session actually prompts on `python3 -m pytest` after Bash is dropped from `allowed-tools`.

Claims 1–24 all engaged below.

---

## Findings, ranked

### 1. The permission fix left an unrestricted `Write` grant over the same prose envelope
**Impact:** high
**Location:** `skills/adversarial-review-prompt/SKILL.md:5-10`; `skills/review-adjudication/SKILL.md:5-10` and invariant 1 at `:32-35`; `REVIEW-ADJUDICATION.md` §R3.3 `R3-F1`, §R3.13 Q1
**Mechanism:** Round-3 finding 1 was that `allowed-tools` is a permission *grant*, not an allowlist, so a prose write-envelope sitting over a broad grant is advisory. The executed fix dropped `Bash` / `Edit` / `Agent` and kept `Write` with no path specifier. Official docs, fetched 2026-08-22:

> The `allowed-tools` field grants permission for the listed tools during the turn that invokes the skill… **It does not restrict which tools are available: every tool remains callable**, and your permission settings still govern tools that are not listed.
> — https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill

> Workspace trust doesn't gate this field. Claude Code applies a project skill's `allowed-tools` whenever you or Claude invoke the skill, including in a `-p` run in a folder you've never trusted. **A skill can grant itself broad tool access.**
> — same page

> Claude Code checks file permissions against `Edit(path)` and `Read(path)` rules only. If you write a path rule for `Write`… Claude Code accepts the rule but **never consults it**.
> — https://code.claude.com/docs/en/permissions#read-and-edit

So: (a) `Write` still auto-approves writes to any path on the invoking turn; (b) a `Write(*.md)`-style restriction would not even be consulted; (c) Q1 never offered the one form that *would* path-scope writes (`Edit(<ledger-or-brief-path>)`); (d) invariant 1's "whatever the tool grants allow" is an accurate description of a wish. `disallowed-tools` exists in the same table — *"Tools removed from Claude's available pool while this skill is active"* — and is also turn-scoped; the ledger identified it, offered it as Q1(c), and the owner locked (b) without it. The remaining grant is the original defect, one capability smaller.
**Trigger:** Anyone clones this CC0 repo, Claude Code loads the project skills, and either skill is invoked — including `claude -p` in a folder that has never been trusted. The invoking turn may write anywhere without a prompt.
**Consequence:** Contract §4.1 (the fix closes the finding) and §4.4 (claims about enforcement are true). The write boundary is still a sentence.
**Status:** CONFIRMED — YAML parse of both frontmatters; docs quoted above. The owner locking Q1(b) makes this a chosen residual, not an accident; it is still the defect `R3-F1` named.

Why it ranks here: every invocation of a publicly distributed skill is the trigger, and the blast radius is the working tree, including in untrusted `-p` runs the docs specifically warn about.

---

### 2. The independence-sentence fix left the payoff line unconditional
**Impact:** high
**Location:** `skills/adversarial-review-prompt/references/prompt-template.md:39-40` (emitted block); branches at `:54-73`
**Mechanism:** `R3-F5` replaced *"You have a different architecture and different training"* with the placeholder `«independence sentence — one of the three branches below»`. The next sentence in the same emitted quote is still:

> **You will notice different things, and those things are the entire value of this exercise.**

That sentence is verbatim-worthy register, not an authoring instruction. For the same-family branch (`:63-66`) the author is told to write *"you do not bring a different architecture, so the blind spots you share with its author are the ones most likely to survive this review"* — and then the template still emits "You will notice different things" as the value of the exercise. The two sentences contradict. For unknown lineage they jointly overclaim. The three-branch machinery therefore does not close the "knowingly false framing" finding: it relocated the false claim one sentence later.
**Trigger:** Any brief this skill emits, and especially the explicitly-supported same-family route (`SKILL.md:105-109`, template `:57-59`).
**Consequence:** Contract §4.1. Same-family agreement is again laundered as evidence of an architectural difference the branch just denied.
**Status:** CONFIRMED — the quoted block is what the reviewer reads; grep shows the leftover line at `:40`.

Why it ranks here: this project's own supported path (another Claude session) hits it every time, and it is the exact defect `R3-F5` was supposed to close.

---

### 3. The operational blindness claim was not updated
**Impact:** high
**Location:** `skills/review-adjudication/SKILL.md:439`; contrast `:269-277` and invariant 5 at `:45-47`
**Mechanism:** The cited fix narrowed `:269-277` to "is never *handed* the report" and said that is not the same as being unable to read it. The site that actually fires the second opinion was not touched:

> **That same verdict also requires a second opinion that never saw the report.**

Grep of the skill for `blind` / `never saw` / `handed`: the qualified claim lives at `:47` (invariant) and `:269-277`; the original overclaim lives at the escalation rule. An adjudicator following §5's numbered rules reads `:439` at the moment of a high-impact `REFUTED`. Invariant 5 (`was not handed the report`) and `:439` (`never saw`) are the contradiction claim 7 asked about.
**Trigger:** `REFUTED` of a reviewer-rated high/critical finding in code this session authored — the expensive case the escalation exists for, and the case in which a false "blind" label is most costly.
**Consequence:** Contract §4.1 and §4.3. The ledger will describe as blind a check the same file admits is one `ls` away. Q4(b)'s recording obligation at `:467-476` is the intended mitigation and is itself past the compaction cut (finding 4) and has no template field (finding 11).
**Status:** CONFIRMED — grep, line read.

Why it ranks here: a high-impact `REFUTED` that records a blind second opinion it did not have is the failure mode this skill exists to prevent.

---

### 4. The compaction hoist put the new obligations on the side of the cut they were written to survive
**Impact:** high
**Location:** invariants at `adversarial-review-prompt/SKILL.md:22-45` and `review-adjudication/SKILL.md:26-50`; Q4(b) recording at `review-adjudication/SKILL.md:467-476`; overwrite *how-to* at `adversarial-review-prompt/SKILL.md:324-331`; files 463→497 and 523→572
**Mechanism:** Official docs confirm the cap:

> When the conversation is summarized to free context, Claude Code re-attaches the most recent invocation of each skill after the summary, **keeping the first 5,000 tokens of each**. Re-attached skills share a combined budget of 25,000 tokens.
> — https://code.claude.com/docs/en/skills#skill-content-lifecycle

The ledger's "well above the recomputed cut band" (`§R3.14`) is a word-count heuristic (`§R3.10` `R3-CNV-2` admits no tokenizer was run). I have no Anthropic tokenizer (packages absent; installs forbidden). Under the ledger's own 1.33 tokens/word heuristic, and under chars/4:

| File | era | lines | 5k via words×1.33 | fraction past | 5k via chars/4 | fraction past |
|---|---|---|---|---|---|---|
| prompt | `fe9bbac` | 463 | line 313 | 32.4% (150 lines) | line 279 | 39.7% |
| prompt | `540c60a` | 497 | line 324 | 34.8% (173 lines) | line 285 | 42.7% |
| adjudication | `fe9bbac` | 523 | line 312 | 40.3% (211 lines) | line 276 | 47.2% |
| adjudication | `540c60a` | 572 | line 304 | 46.9% (268 lines) | line 266 | 53.5% |

The invariants at lines 22–50 sit above every estimate. The *new* obligations of this round do not: Q4(b) "write beside the verdict that the verifier could have read the report" (`:467-476`), the overwrite *how-to* (`:324-331`, exactly on the word-heuristic cut in the prompt skill), and the sanitized-copy paragraph. After compaction the surviving copy of the adjudication skill says "was not handed the report" (invariant 5) and has lost both "never saw" *and* "record that they could have read it". The prompt skill keeps "never overwrite" and loses "check the path before writing". The files also got longer, so more of each tail is now past the cut than before the fix — which `§R3.14` recorded and did not treat as closing `R3-F2`.
**Trigger:** An adjudication or brief-authoring session that auto-compacts once, having invoked this skill and then others — the condition the invariants block itself describes at `:27-30` / `:23-25`.
**Consequence:** Contract §4.2. The round-3 fixes un-apply themselves under the condition they were added to survive. `review-adjudication` is 72 lines past the documented 500-line guidance (https://code.claude.com/docs/en/skills — "Keep `SKILL.md` under 500 lines").
**Status:** CONFIRMED for length, line positions, and the official 5,000-token cap. THEORETICAL for the exact tokenized line (no tokenizer). Heuristic bounds are enough: every new obligation of this round sits past line 266 in a 572-line file.

Why it ranks here: compaction is the documented fate of a 572-line skill, and the round's own safety patches are what get dropped.

---

### 5. The overwrite guard does not cover the report or the ledger, and "check the path" is not a mechanism
**Impact:** high
**Location:** `adversarial-review-prompt/SKILL.md:324-331, :414-417`; default report path at `:277, :349, :396`; `review-adjudication/SKILL.md:529` ("Completed rounds append only"); `cover-note-template.md:90-91`
**Mechanism:** The new guard names two files: the brief and the cover note. The reviewer is still told, in both the skill and the cover-note template, to write `NN-EXTERNAL-REVIEW.md`. `cover-note-template.md:90-91` already knows what happens: *"A follow-up or delta review. Point 1 must say whether to append to the existing report or start a new file, and name it. A reviewer left to guess will overwrite."* That warning was not promoted into the skill's new guard. Sequential rounds in one directory are this repository's actual workflow (`EXTERNAL-REVIEW.md`, `EXTERNAL-REVIEW-2.md`, `EXTERNAL-REVIEW-3.md`). The ledger's append-only rule is one prose sentence with no existence check; `Write` is granted (finding 1), so a `Write` of the whole file replaces a closed round rather than appending. "Check the path before writing" (`:324`) is an instruction to an agent that has already been pre-approved to write the path — the same prose-over-grant shape as `R3-F1`.
**Trigger:** A second brief over the same phase using the default unsuffixed names; or an adjudication that `Write`s `REVIEW-ADJUDICATION.md` rather than appending.
**Consequence:** Contract §4.2. Destroying a spent brief/report/ledger deletes the evidence the echo audit and the next "ground already walked" section are scored against, "and nothing downstream can tell that it happened" — the skill's own words, applied only to the two files it started guarding.
**Status:** CONFIRMED — the guard's text names two artifacts; the report path is still the unsuffixed default; no existence-check command is specified.

Why it ranks here: this repository runs sequential rounds in one directory, and a silent overwrite of `EXTERNAL-REVIEW.md` or the ledger is unrecoverable.

---

### 6. The chat-delivery "continue" instruction never reaches the operator checklist
**Impact:** medium
**Location:** `skills/adversarial-review-prompt/references/prompt-template.md:365-376`; `skills/adversarial-review-prompt/SKILL.md:462-497` (§10)
**Mechanism:** The template now tells the reviewer the operator will send one word to continue, and tells the *author* (`:374-376`) to say so in the hand-off because the instruction needs the operator. §10 is the enumerated list of what to tell the operator. A grep of `SKILL.md` for `continue` and `one word` returns no matches. The authoring agent that follows the checklist, not the template's aside, will not tell the operator. Round 3 of this repository *was* a chat-delivered review that the operator transcribed (`EXTERNAL-REVIEW-3.md` header).
**Trigger:** A no-filesystem reviewer hits its output limit, stops at a section boundary as instructed, and the operator reads that stop as the end.
**Consequence:** Contract §4.1. `R3-F9`'s stated cost — *"an operator who reads that stop as the end will file a truncated report as a complete one"* — is exactly what the missing checklist item was supposed to prevent.
**Status:** CONFIRMED — `grep -n 'continue\|one word' skills/adversarial-review-prompt/SKILL.md` exited 1.

Why it ranks here: truncated-as-complete is expensive, but the trigger is only the no-filesystem path, not every run.

---

### 7. The corpus digest is expired by the documented test command; pruning `__pycache__` by name repeats the round-2 shape
**Impact:** medium
**Location:** `calibration/record-template.md:14`; `REVIEW-ADJUDICATION.md` §R3.16; `.gitignore` (`.DS_Store` and `*.swp` only)
**Mechanism:** Three things, as asked.

(a) Both digests reproduce on this tree:
```
$ find calibration/cases calibration/CALIBRATION-PROMPT.md calibration/ANSWER-KEY.md \
    -type f ! -name .DS_Store -print0 | sort -z | xargs -0 shasum | shasum | cut -c1-12
9fb019996546

$ find … ! -name .DS_Store ! -path '*__pycache__*' …
775e1cc8c43f
```
Matches §R3.16.

(b) The distinction from round-2 `F1` is real as *mechanism* (`.DS_Store` vs pytest bytecode) and false as *shape*. `F1`'s fix pruned one artefact by name. This is the next artefact `find -type f` notices, created by following the calibration procedure itself. The earlier fix was too narrow and should have been ruled incomplete rather than executed-and-closed.

(c) The proposed minimal fix — prune `__pycache__` too — guarantees a third instance (`.pytest_cache`, `*.pyc` outside `__pycache__`, a `.mypy_cache`, a next pytest plugin). `git ls-files` of the same paths already yields `775e1cc8c43f` on this tree: the instrument digest, with no named-artefact list. `.gitignore` cannot save a `find`-based digest; it already ignores `.DS_Store` and the digest command still needed `! -name .DS_Store`. The ledger named `git ls-files` and an explicit manifest as Q5 and did not weigh that `git ls-files` is a one-line drop-in that already matches the record.
**Trigger:** Run the two-fixture pytest the README and this brief both instruct, then recompute the digest as `record-template.md:14` writes it.
**Consequence:** Every calibration record silently expires the first time anyone exercises the corpus. Both consuming skills treat a mismatch as "stale, counts as missing". This ledger's own round-3 header got this wrong twice.
**Status:** CONFIRMED — commands and outputs above. Pytest was run under `/tmp` (`8 passed in 0.01s`) and created `__pycache__` there; the repo copy was not written by this run.

Why it ranks here: it already mis-calibrated this ledger twice, but it is filed as `PENDING OWNER` and does not silently corrupt a review the way findings 1–5 do.

---

### 8. Residual doubts: the finding is restated as a user-paste, README still denies the dependency, and the fallback is a cheap exit
**Impact:** medium
**Location:** `review-adjudication/SKILL.md:145-154`; `README.md:152-153`; fallback at `:151-154`
**Mechanism:** `R3-F3` was that no durable source of the author's doubts exists, while adjudication requires ruling on them. The fix names the hand-off as a step-1 input and tells the adjudicator to ask the user to paste it. That is the same dependency with an ask in front of it. `README.md:152-153` was not updated:

> Everything it writes stands on its own, so nothing later depends on keeping this session open.

The fallback — *"where unavailable, record that and score no finding as independent corroboration"* — is one sentence the user can trigger by saying they no longer have the chat. Nothing makes the declaration costly or checkable: no hash, no "look in the session transcript path", no requirement to show a search. Q3(b)/(c) (private artifact / commitment hash) were not taken.
**Trigger:** The documented workflow: authoring session closed, adjudication "days later on another machine" (`README.md` / original `R3-F3`), user does not have the hand-off.
**Consequence:** Contract §4.1. Independent-corroboration scoring is silently disabled for the whole report, and the README tells the operator this is fine.
**Status:** CONFIRMED for the README line and the fallback text. THEORETICAL for an operator actually taking the cheap exit — the text permits it with no further check.

Why it ranks here: it reopens the corroboration channel this whole scheme is built on, but only when the user drops the chat, which is common and not every run.

---

### 9. Invariant 4 cannot be followed, and its author demonstrated that in the adjacent paragraph
**Impact:** medium
**Location:** `review-adjudication/SKILL.md:42-44` (invariant 4), `:211-212` (step 2), `:499` (§6); `REVIEW-ADJUDICATION.md` §R3.3 `R3-F6`
**Mechanism:** Step 2 requires writing the ledger *skeleton* to disk before any finding is judged. Invariant 4 / §6 require the `FIX LATER` artifact to be created **before the ledger is written**. Dispositions do not exist until after the skeleton exists. The two instructions cannot both be obeyed. The session that hoisted invariant 4 then wrote `BACKLOG.md` `B-3` after the ledger row, and recorded the slip. That is not a one-off miss: it is the procedure colliding with itself. The artifact in this case exists and is complete (Location, Mechanism, Consequence present; skill-level scope split from `B-1` is coherent), so the *instance* did not lose a deferral. The *rule* remains unsatisfiable for the next `FIX LATER`.
**Trigger:** Any adjudication that disposes a finding `FIX LATER` after following step 2, which is every such adjudication.
**Consequence:** Contract §4.3. The next slip happens in the gap the rule exists to close — between "queued" and "artifact on disk".
**Status:** CONFIRMED as a text contradiction (step 2 vs invariant 4) and as a recorded violation (`R3-F6` row). THEORETICAL as to a future lost deferral.

Why it ranks here: the next `FIX LATER` is the trigger, and a lost deferral is a finding that disappears; but this instance's artifact is complete.

---

### 10. Dropping `Agent` makes the mandatory second opinion a permission prompt with a documented `COULD NOT DETERMINE` exit
**Impact:** medium
**Location:** `review-adjudication/SKILL.md:5-10` (no `Agent`); escalation at `:439-447`; `REVIEW-ADJUDICATION.md` §R3.3 `R3-F1` ("Beyond the letter of Q1(b)… `Agent` was dropped too")
**Mechanism:** `allowed-tools` is a grant, not a restriction (finding 1, docs cited there). Dropping `Agent` does not remove the tool; it means a spawn prompts. The escalation at `:439` *requires* a subagent for high-impact self-refutation. The documented fallback when "no subagent is available" is `COULD NOT DETERMINE` (`:446-447`). A permission prompt is not unavailability, but it arrives at the exact moment the adjudicator is about to write down that a serious finding against its own work was wrong. The cheap, fully-documented exit is CNV. The ledger flagged the Agent drop as beyond Q1(b) and did not weigh this. (By contrast, dropping `Bash` is milder than §R3.14's hedge: https://code.claude.com/docs/en/permissions#read-only-commands lists `ls`, `cat`, `grep`, `find`, `wc`, and read-only `git` as unprompted in every mode, so much of §5 still runs quiet. `python3 -m pytest` and write-capable shell do not.)
**Trigger:** High/critical `REFUTED` of own code, in a session whose user is not staring at the permission dialog.
**Consequence:** Contract §4.2. Either the second opinion is skipped and the verdict becomes CNV (the honest fallback, a weaker record) or the prompt is dismissed and a `REFUTED` is written without the check (the dishonest one).
**Status:** THEORETICAL — I did not spawn a Claude Code subagent. Docs establish that unlisted tools fall through to permission settings and that `Agent` is a tool (https://code.claude.com/docs/en/permissions#agent-subagents).

Why it ranks here: the trigger is rare (high-impact self-refutation) and the honest path is CNV, which is conservative rather than a false `REFUTED`.

---

### 11. Q4(b)'s recording requirement has no field in the template the skill says to follow
**Impact:** medium
**Location:** `review-adjudication/SKILL.md:467-476`; `skills/review-adjudication/references/ledger-template.md:31-33`
**Mechanism:** Owner decision Q4(b) requires the ledger to record, beside the verdict, that the verifier could have read the report. The template the skill's §7 says to follow has a **Reviewer isolation** line at `:31`: *"which earlier artifacts this reviewer could read — the prior report, this ledger, another reviewer's findings"*. That is about *external reviewers*, not the subagent. There is no field, no example row, and no «guillemet» instruction for verifier exposure. An adjudicator filling the template will complete "Reviewer isolation" about Codex/Gemini and will not have a slot for "the verifier could have read the report". Combined with finding 4 (the requirement sits past the compaction cut) and finding 3 (the operational line still says "never saw"), the recording obligation is the part of `R3-F4` least likely to land.
**Trigger:** The first high-impact `REFUTED` after this round, with the adjudicator following `ledger-template.md`.
**Consequence:** Contract §4.1. Q4(b) was the owner's chosen substitute for real isolation; without a field it is a sentence in a 572-line file.
**Status:** CONFIRMED — template read; no matching field.

Why it ranks here: it is the enforcement of finding 3's mitigation, and it fails on contact with the template even before compaction.

---

### 12. The three independence branches do not cover real authorship, and the same-family sentence is an untested assertion
**Impact:** low
**Location:** `prompt-template.md:54-73`; author-family collection absent from `adversarial-review-prompt/SKILL.md` §1
**Mechanism:** The branches are (known-different family / same family / unknown *reviewer* lineage). There is no branch for a human-written target, a multi-model target, or an author family the session has not established. §1 requires the *reviewer's* identity and then says "say at hand-off when that family is the one that wrote the work" — it never asks who wrote the work. The provenance gate (`:26-29`) covers "inherited code, human edits, or third-party work" for the *first* sentence of the quote, not for the independence placeholder. The same-family branch then asserts *"the blind spots you share with its author are the ones most likely to survive this review."* Nothing in this repository establishes that. It is a plausible-sounding claim inserted into a document whose purpose is to stop those passing as fact. The unknown-lineage branch is the only honest one, and the skill has no step that would choose it for a human author.
**Trigger:** A brief about mixed-provenance or human-edited work, or any same-family review (the assertion fires even when the branch is correctly selected).
**Consequence:** Contract §4.1 for the coverage gap; the same-family assertion reintroduces the genre of claim `R3-F5` removed.
**Status:** CONFIRMED that author family is never collected and that the three branches are the only options. THEORETICAL that a human-authored target is a common use of this skill (the skill's own description includes "a red-team of their own code").

Why it ranks here: the common path in *this* repository is "Claude wrote it, someone else reviews it", which the known-different branch covers; the hole is real and untested.

---

### 13. This brief contradicts itself on pytest, and its inventory count for the ledger is wrong
**Impact:** low
**Location:** `EXTERNAL-REVIEW-4-PROMPT-GROK.md` §2 vs §8; §3 table vs `git show 540c60a:REVIEW-ADJUDICATION.md | wc -l`
**Mechanism:** Two process defects, wanted by the brief's own standing instruction.

(1) §2's executable test is `python3 -m pytest -q calibration/cases/clean-wordcount calibration/cases/trap-unfalsifiable-test`. §8 says modify nothing else in the repository, and notes that a bare pytest run writes `__pycache__`. Those two instructions cannot both be followed in-tree. I copied the fixtures to `/tmp` and ran them there (`8 passed`). That is a resolution I had to invent; the brief states both halves.

(2) §3 lists `REVIEW-ADJUDICATION.md` as "2,466 total" at `540c60a`. `git show 540c60a:REVIEW-ADJUDICATION.md | wc -l` is **2480**. The other six in-scope counts reproduced. This is round-2 `F9` (a refreshed brief carrying one inventory number forward) happening in the brief that cites `F9` as ground already walked.
**Trigger:** A reviewer that runs the §2 command in-tree writes `__pycache__` and, if they recompute the digest, expires the calibration record (finding 7). A reviewer that trusts the 2,466 figure audits the wrong size of the largest in-scope file.
**Consequence:** A prompt defect of the kind the template asks to report. The inventory miss is the more expensive half: it is the failure the round-2 fix was supposed to make mechanically impossible.
**Status:** CONFIRMED — `wc -l` at the pinned commit; pytest-in-`/tmp` vs the in-tree command as written.

Why it ranks here: it costs this run some reconstruction, not a wrong ruling on the skills.

---

## The unseeded pass

Read the `fe9bbac..540c60a` diff and both skills without using the claims list as a map. What that pass produced, and where it is *not* an echo of a numbered claim:

**The emitted "You will notice different things" line after the new placeholder** (finding 2). The claims list pointed at the placeholder and the three branches (`claim 14–16`). It did not point at the next sentence of the quote remaining unconditional. That is the one defect this pass reached that the directed list did not name.

**Invariant 4 vs step 2** (finding 9) is adjacent to claim 8 (the recorded slip) but is a different claim: not "the author broke the rule once" but "the procedure cannot obey the rule". I would have reported it from the collision of `:211-212` and `:42-44` without claim 8.

**`Edit(path)` is the only consulted write-path rule** is not in the claims list. It changes the reading of Q1: the option that would have actually path-scoped the remaining `Write` grant was never on the menu, and `Write(path)` would have been silently ignored. Folded into finding 1.

**Read-only Bash still runs unprompted** is not in the claims list and *cuts against* a strong reading of claim 4. Official docs, not a claim-list echo.

Considered and not raised as additional findings: the invariants' "roughly line 280 / 270" estimates are slightly stale relative to the post-fix heuristic bands (288–322 / 265–302) but biased *early*, which is the safe direction. `cover-note-template.md` was not in the seven-file change set; it already warned about report overwrite on delta reviews, which finding 5 uses as evidence that the skill's new guard is narrower than a file the author already had.

---

## Claims examined and upheld

1. **REFUTED** that dropping `Bash` closed `R3-F1`. Both grants are now `Read, Write, Grep, Glob` (YAML parse). `Write` is still unconditional; `allowed-tools` is still a grant (https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill); workspace trust does not gate it. The prose envelope over a broad grant is the same situation, one notch smaller. Finding 1.
2. **CONFIRMED** that the ledger identified `disallowed-tools` as a real restriction and deliberately did not adopt it (Q1(c) offered, Q1(b) locked). **REFUTED** that invariant 1 has a mechanism behind it: "whatever the tool grants allow" is an accurate description of a wish. Cost not weighed: `Write(path)` is never consulted; `Edit(path)` would have been, and was not offered. `disallowed-tools` is also turn-scoped (same page); the ledger did note that.
3. **CONFIRMED** that dropping `Agent` went beyond the locked keeps and is recorded as such. **CONFIRMED** that the escalation at `:439` still requires a subagent. **COULD NOT DETERMINE** empirically whether a prompt appears (no Claude Code spawn). Docs say unlisted tools fall through to permission settings. The documented fallback is `COULD NOT DETERMINE`. Finding 10.
4. **REFUTED** as a strong behavioural regression. Removing `Bash` from the grant does not remove Bash; it prompts, except for the built-in read-only set (`ls`, `cat`, `grep`, `find`, `wc`, read-only `git` — https://code.claude.com/docs/en/permissions#read-only-commands), which is most of a documentary re-verification. `pytest` and write-capable shell still prompt. Whether an adjudicator therefore runs fewer checks is unestablished; the ledger was right not to rule it from a static read. I rule the strong form unestablished and the narrow form (non-read-only Bash now prompts) documented.
5. **CONFIRMED** that the invariants sit at those lines. **CONFIRMED** that "well above the cut band" is a word-count heuristic (`R3-CNV-2`, RV-4). **COULD NOT DETERMINE** the exact 5,000-token line: no Anthropic tokenizer available, installs forbidden. Heuristic bounds: prompt cut in 257–324, adjudication cut in 233–304. Invariants at 22–50 are above all of those. Official cap: https://code.claude.com/docs/en/skills#skill-content-lifecycle. Finding 4.
6. **CONFIRMED** the lengthening (463→497, 523→572) and that `review-adjudication` is 72 lines past the documented 500-line guidance. Under the ledger's own heuristic, the fraction of each file past the cut *increased* (prompt 32.4%→34.8%; adjudication 40.3%→46.9%). Net regression on tail exposure; net improvement only for the 25–32-line summary. Finding 4.
7. **CONFIRMED** that invariant 4 and §6 agree ("created before the ledger is written"). **REFUTED** that invariant 5 and `:439` agree: invariant 5 is "was not handed the report"; `:439` is "never saw the report". Finding 3.
8. **CONFIRMED** the recorded slip (`R3-F6`). The instance's artifact is complete, so the loss the rule exists to prevent did not occur *this time*. The rule is unsatisfiable given step 2, which is why it was broken. Finding 9.
9. **REFUTED** that asking the user to paste the hand-off closes `R3-F3`. It restates the dependency. `README.md:152-153` still says nothing later depends on keeping the authoring session open. Finding 8.
10. **REFUTED** that the fallback is safe. Declaring the doubts unavailable is one sentence, removes the corroboration obligation, and is not checkable. Finding 8.
11. **REFUTED** that the blindness qualification reached every site. `:439` is the original claim. Finding 3.
12. **REFUTED** that `ledger-template.md:31` is the Q4(b) field. It is about external reviewers. No field for verifier exposure. Finding 11.
13. **REFUTED** that the sanitized copy is actionable enough to build. It is one sentence ("a scratch directory holding the claim card and only the source files the claim concerns") with no commands, no cwd change, no tool restriction, and Q4(b) saying the unisolated check still counts. Same species as the original finding: a named mechanism that is not a procedure.
14. **CONFIRMED** that the placeholder is `«independence sentence — one of the three branches below»` and that the skill's leftover-guillemet grep (`SKILL.md:314-316`) would catch it if left unfilled. Fail-closed works for this placeholder.
15. **REFUTED** that the three branches cover the real cases. Human author, several models, and undetermined *author* family are unhandled; author family is never collected. Finding 12.
16. **REFUTED** that the same-family branch text is established in this repository. It is an assertion. Finding 12. Separately, the emitted payoff line still says "You will notice different things" for every branch. Finding 2.
17. **REFUTED** that the overwrite guard covers the artefacts that matter for round-N destroying round-(N−1). Brief and cover note only. Report path still defaults to `NN-EXTERNAL-REVIEW.md`. Ledger append-only is one prose sentence. Finding 5.
18. **REFUTED** that "Check the path before writing" is an actionable mechanism. It is an instruction over a pre-approved `Write`. Finding 5 / claim 2's shape.
19. **REFUTED** that the fix works end-to-end. The operator-facing half lives in the template (`:374-376`) and is absent from §10's checklist. `grep` of the skill for `continue`/`one word` is empty. Finding 6.
20. **CONFIRMED** `calibration/README.md:151` reads `COULD NOT DETERMINE`. Repository-wide grep for `COULD NOT VERIFY` hits only history (`EXTERNAL-REVIEW-3.md`, the ledger, `BACKLOG.md`'s origin sentence). **CONFIRMED** `B-3` carries Location, Mechanism and Consequence and is scoped to the skill-level half, leaving `B-1` the corpus half.
21. **CONFIRMED** that none of the eleven numbered rows in §R3.3 leaned on uncalibrated status; they were ruled from primary sources. **CONFIRMED** that §R3.6's treatment of the five unsampled endorsements *did* lean on it, and §R3.15 names that and supersedes it. **CONFIRMED** that append-only discipline held (original header and §R3.12 left in place). §R3.12 and §R3.15 contradict each other by design of append-only correction; a reader who stops at CLOSED is told the reviewer is uncalibrated, which §R3.15/16 say is false. No verdict/disposition cell in §R3.3 changes, which is what the correction claimed.
22. **CONFIRMED** that expanding 5 numbered findings + 6 bullets into 11 rows is defensible: each bullet states a defect with a location, and dropping them for typography is the failure the skill exists to prevent. **REFUTED** "independent by construction" as a complete account. The operator's sentence named the subject ("claude skills to deal with external reviews"). That is topic priming, not defect priming: it does not name `allowed-tools`, compaction, or the architecture sentence. The eleven findings are still independent of a claims list. The "by construction" phrasing overclaims a true weaker fact.
23. **CONFIRMED** (a) both digests. **CONFIRMED** (b) not a duplicate of `F1` as mechanism; **REFUTED** that `F1`'s fix was complete — it was the same `find -type f` door, narrowed by one name. **REFUTED** (c) that pruning `__pycache__` by name is the right shape. `git ls-files` already yields `775e1cc8c43f`. Finding 7.
24. **CONFIRMED** that this round added words without adding enforcement. Ten of ten executed `FIX NOW` items are prose: an `<invariants>` summary, a qualification of "blind", a placeholder, a "check the path", an "ask the user", a vocabulary swap, a de-linked filename. Zero path-scoped grants, zero `disallowed-tools`, zero existence-check command, zero tokenizer, zero digest-command change, zero validator (`B-3` deferred). Evidence the author failed to follow the procedure just hoisted: invariant 4 (recorded), digest check modified until it matched (§R3.16), calibration header wrong twice, README not updated, `:439` not updated, §10 checklist not updated, this brief's own inventory count wrong (finding 13). `review-adjudication` at 572 lines: a shorter version would lose the history-of-failures that makes the rules motivated, and would lose nothing of *enforcement*, because there is none. Whether a competent operator still follows it: this round's own slips are the evidence they do not, including the session that wrote the invariants.

---

## Could not verify

- Exact 5,000-token line in either `SKILL.md`. No Anthropic tokenizer on the machine; brief forbids installs. Bounded by words×1.33 and chars/4 (finding 4). What would settle it: run both files through the tokenizer Claude Code uses and read off the line.
- Whether a live Claude Code session prompts on `Agent` spawn or on `python3 -m pytest` after the grant change. Docs say unlisted tools fall through to permission settings; the built-in read-only Bash set complicates the pytest/Bash case. What would settle it: invoke `review-adjudication` on a machine running current Claude Code and observe the permission dialogs. Already adjacent to `R3-CNV-1`.
- Whether a spawned subagent actually opens the report when not handed it (`R3-CNV-1`, not re-reported). Documentary contradiction at `:439` vs `:269-277` does not depend on it.
- Transcription fidelity of `EXTERNAL-REVIEW-3.md` (`R3-P2`, accepted as-is).
- Whether same-family reviewers actually share the author's blind spots (claim 16). Nothing in this repository measures it.
- Contents of `EXTERNAL-REVIEW-4.md` / the other brief / the other cover note, by instruction.

---

## Disagreements with the prior rounds

- **Round-2 `F1` (`REVIEW-ADJUDICATION.md:1465`) was ruled `FIX NOW` and executed as "prune `.DS_Store` by name".** That ruling was correct as scoped and incomplete as a closure. The same `find -type f` digest, with one more named exception, is now `R3-F12`. I would have required the digest to iterate tracked files or an explicit manifest rather than closing `F1` as executed. Finding 7.
- **Round-3 `R3-F1` executed as Q1(b) is recorded as closing the finding.** I disagree: the finding was prose-over-grant, and `Write` is still an unrestricted grant. The owner is entitled to accept that residual; the row should not read as closed. Finding 1.
- **Round-3 `R3-F4` executed as a qualification plus Q4(b).** The qualification missed the operational site (`:439`) and Q4(b) has no template field. The row reads `✔ executed`. Findings 3 and 11.
- **Round-3 `R3-F5` executed as three branches.** The payoff sentence in the emitted quote was not updated. Finding 2.
- **Round-3 `R3-F2` is the one row that already records its own incompleteness** (`§R3.14`: longer files, more tail past the cut). I agree with that recording and disagree with treating the invariants block as having closed the finding. Finding 4.
- **Round-3 §R3.4 "all eleven findings are independent by construction".** Independent of a claims list, yes; "by construction" erases the topic priming in the operator's sentence. Claim 22.
- **Round-3 `R3-F9` executed as a template edit.** The operator-facing half never reached the checklist the author follows. Finding 6.

No disagreement that the eleven-row expansion was right, that `R3-F8`/`R3-F10` are actually closed, that `B-3` is well-formed, or that the append-only corrections in §R3.15–16 were the right *shape* for a closed round (the content of §R3.16 is in scope and is finding 7).
