# External Review 6 (Grok) — the validator, the ledger, and the calibration instrument
Reviewer identity: xAI Grok family; product Grok 4.6 (Grok Build TUI / Grok Code); reasoning effort high; served alias verbatim: `Grok 4.6` (system prompt: "You are Grok 4.6 released by xAI").

Audit range `2565c08..c62ca24` (HEAD `c62ca2491f13cae22459eb0ed75d6874002107dd`). `git diff --stat` over that range: **13 files changed, 1144 insertions(+), 95 deletions(-)** — matches the brief. Target is the half as it stands at `c62ca24`, not only the delta.

---

## Coverage

**20 of 20 claims engaged.** Read `scripts/validate.py` (354), `BACKLOG.md` (123), `calibration/README.md` (163), `calibration/record-template.md` (81), `calibration/ANSWER-KEY.md`, both filed records, all six reports under `.adversarial-review/calibration/runs/2026-08-22-grok-4.6-high/`, `EXTERNAL-REVIEW-5-GROK-VOID.md` header, round 5 of `REVIEW-ADJUDICATION.md` (`§R5.*`, from line 3628) plus the round-4 X-series and round-4 header, both `SKILL.md` invariant blocks, and the round-5 diff for `scripts/validate.py` and `skills/review-adjudication/SKILL.md`.

Ran, all observed in this session:

- `git diff --stat 2565c08..c62ca24`; `git show 2565c08:REVIEW-ADJUDICATION.md | wc -l` (3623); prefix byte-compare of that blob against HEAD
- `python3 scripts/validate.py` and `--list` (in-repo; no `__pycache__` left in the repository)
- Template digest command and `corpus_digest()` — both `775e1cc8c43f` on this tree
- Full mutation harness under `/tmp/vmut` (copy of the repo per case): 51 probes
- Digest attack copy at `/tmp/digest-r6` and `/tmp/digest-elsewhere/copy`: pytest, tracked-file edit, untracked add, space-in-filename
- PyYAML-hidden run: frontmatter skipped, still `All 12 checks pass`

Did not examine: Anthropic's tokenizer; whether a compacted Claude Code session actually globs a missing `example-audit-prompt.md`; Linux `sha1sum` vs macOS `shasum` on another OS. Did not run the two fixture suites in-tree (copied first, as instructed).

Findings 1–10, 12–13, 15 came from the claims list. Findings 11 and 14 came from the unseeded pass. Finding 15 is the brief/cover-note envelope disagreement the brief asked for.

---

## Findings, ranked

Strict order by cost of leaving unfixed (blast radius × likelihood the trigger is reached). No ties. Impact is an attribute, not a heading.

### 1. `check_counts` compares two numbers the author wrote and never counts rows — **high**

- **Location:** `scripts/validate.py:195-206`
- **Mechanism:** The check searches the current round for `Findings in: N` and `Rows out: N` and errors only when those two captured digits differ. It does not count ruling rows, does not read the reports, and does not look at process/CNV/D/U/A/C blocks. The invariant the skill states (`review-adjudication/SKILL.md:44-46, 202-206`) is one row per numbered finding.
- **Trigger:** Delete `| grok-9 |` from the round-5 table and leave the header at 22/22.
- **Consequence:** Contract item 1. A dropped finding with a consistent header is the defect this skill exists to prevent, and the mechanical check cannot see it. Later briefs inherit "ground already walked" from that header.
- **Status:** **CONFIRMED.** `/tmp/vmut` case `counts-drop-a-real-row-header-still-22-22-SILENT` → exit 0, `All 12 checks pass`. The complementary mutation (header `22` vs `21`) *is* caught — so the check works on its own two fields and on nothing else.
- **Why this rank:** a disappeared finding is a wrong result that looks right in the one artifact every later round is scored against, and writing matching numbers is the default path, not an edge.

### 2. The digest's documented semantics are the opposite of what it does for tracked-file edits — **high**

- **Location:** `calibration/record-template.md:38-40`; `calibration/README.md:135-136`; implementation `scripts/validate.py:214-223`
- **Mechanism:** Both the template command and `corpus_digest()` enumerate `git ls-files` (tracked *names*) and then hash **working-tree bytes**. An uncommitted edit of a tracked corpus file therefore *does* move the digest. The operator-facing text says the opposite: *"a case edited but not committed does not change the digest"* / *"an uncommitted corpus edit will not register"*. That sentence is true only of never-added files.
- **Trigger:** `echo "<!-- uncommitted edit -->" >> calibration/ANSWER-KEY.md` in `/tmp/digest-r6`.
- **Consequence:** Contract items 3 and 4. The digest is the published identity of the instrument. Operators following the template will believe they can edit the key or a case and keep the filed PASS current; what actually happens is the digest moves under them, and a later clean checkout makes a just-filed record look stale — or a record is filed against dirty bytes that are not what `HEAD` contains.
- **Status:** **CONFIRMED.** Clean `775e1cc8c43f` → after the edit `cc228dfe98a3` (Python and `shasum` agreed). Restore returned `775e1cc8c43f`. An untracked new file under `calibration/cases/` did *not* move it, so the "untracked additions are invisible" half is real and is the actual cost of `git ls-files`.
- **Why this rank:** every calibration PASS is keyed on this identity, and the trigger is the ordinary act of editing the corpus.

### 3. A-3 is marked `✔ executed` with a check that cannot detect the defect A-3 named — **high**

- **Location:** `REVIEW-ADJUDICATION.md:3900` (A-3), `:4036` (queue item 17), `:4046` (execution); `scripts/validate.py:294-313`
- **Mechanism:** A-3 was *unfaithful summaries of real sections* (invariant 1 too broad, invariant 3 too narrow). Queue item 17 asked for a check that every `(§N)` "is re-read against its section". What shipped is an existence check: `§N` must appear as `## N.` somewhere in the same `SKILL.md`. Citing the wrong existing section is a pass. A skill with no `<invariants>` block is also a pass.
- **Trigger:** Change `prove the earlier rounds are untouched. (§7)` to `(§3)`.
- **Consequence:** Contract items 1 and 5. The ledger now tells the next brief that the unfaithful-summary class is walked ground. The check that is supposed to ratchet it cannot fail on the failure mode that justified adding it.
- **Status:** **CONFIRMED.** `/tmp/vmut` `backref-wrong-but-existing-section-SILENT` → exit 0. `backref-dangling-section-99` *does* fail, so the check is not dead — it is the cheap half of a different defect, recorded as if it closed A-3.
- **Why this rank:** a `✔ executed` on the wrong predicate is how this repository has lost defects before (round-4 FIX LATER one-site close, X-1 extracted-not-re-read). Leaving it unfixed spends the round-5 validator extension on a green that cannot catch the thing it was bought for.

### 4. A stale calibration record does not fail the validator — **high**

- **Location:** `scripts/validate.py:226-245, 346-349`
- **Mechanism:** Digest mismatch and a missing digest row both call `warn()`, not `err()`. `main()` exits 1 only on `ERRORS`. The named check is "calibration records match the corpus digest". B-3 discloses that *install* is a warning by design; it does not disclose that this check is too.
- **Trigger:** Replace `` `775e1cc8c43f` `` with `` `deadbeefdead` `` in `.adversarial-review/calibration/grok-4.6-high.md`.
- **Consequence:** Contract item 1. `All 12 checks pass` still prints. A consumer that treats the validator as the gate will treat a PASS filed against another instrument as current. That is how silence gets written down as coverage.
- **Status:** **CONFIRMED.** `/tmp/vmut` `calibration-digest-mismatch-is-warn-not-error` → exit 0, `WARN calibration: ... deadbeefdead ... 775e1cc8c43f`, final line `All 12 checks pass (6 warning(s))`.
- **Why this rank:** the warning is at least visible, unlike finding 1, so it sits below that — but the success line still certifies the run, which is the number an author quotes (and did, at `REVIEW-ADJUDICATION.md:4057`).

### 5. `check_table_pipes` fails correct GFM, and the three live warnings are that false positive — **medium**

- **Location:** `scripts/validate.py:131-151`; live WARNs on `REVIEW-ADJUDICATION.md:422, :1465, :1473`
- **Mechanism:** The check counts `|` while a per-line backtick toggle is on. It does not look at a preceding `\`. GFM requires `\|` inside table cells, including inside code spans; that is the correct form, not the defect. Line 422 contains four `\|` inside `` `find … | …` ``. Unescaped-pipe split of that line yields 6 cells, matching the header's 6 pipes — the row renders.
- **Trigger:** Append to the current round: `| Z-ESC | demo \`a\\|b\` cell | **CONFIRMED** | **FIX NOW** |`
- **Consequence:** Contract item 2. On a closed round this is a WARN the author cannot repair. On the current round it is an **ERROR**, so a correct ledger row fails the build. The three warnings currently on file are not unrepaired table-split defects; they are the check firing on the escape that prevents the split.
- **Status:** **CONFIRMED.** `/tmp/vmut` `table-escaped-pipe-in-code-should-pass` → exit 1, `ERROR table: ... 4103 has 1 unescaped pipe(s)`. Unescaped `` `a|b` `` in the current round is correctly caught. Column arithmetic on line 422: 10 raw `|`, 4 escaped, 6 unescaped-delimited cells = header.
- **Why this rank:** it already fires on this repository's ledger, and the next current-round pipeline quote will fail the run on correct work.

### 6. `last_round` scoping makes two-axes, disposition, and count defects in closed rounds permanently invisible — **medium**

- **Location:** `scripts/validate.py:162-166, 168-206`; argument at `REVIEW-ADJUDICATION.md` / skill invariant 1 (`skills/review-adjudication/SKILL.md:36-40, 448-454`)
- **Mechanism:** Strict ledger checks run only on the slice from the last `^# Round \d+`. Closed-round table pipes become WARN; two-axes, NO ACTION legality, bare ACCEPTED, and counts are not even warned. There is no mechanical proof that the completed prefix is untouched — that proof is a human `head | diff` instruction. During round 5 the scoping *did* see P-3, because round 5 was (and is) the last heading; that part worked.
- **Trigger:** Insert `| Z-OLD | … | **CONFIRMED** — no disp | |` immediately before `# Round 5`. Also: change round 1's header to `Rows out: 99`.
- **Consequence:** Contract items 1 and 5. The "closed rounds are immutable" argument is sound as a reason not to fail the build on unrepairable history. It is not sound as "therefore closed rounds are correct." A later session can change a verdict in round 1 and the validator stays green. Round 5's own `✔ executed` backfills were in-scope only because the round was still open.
- **Status:** **CONFIRMED.** Both `/tmp/vmut` closed-round plants → exit 0. Prefix integrity *this* commit is real (finding-adjacent, not this finding): `git show 2565c08:REVIEW-ADJUDICATION.md` is an exact byte prefix of HEAD, 3623 lines.
- **Why this rank:** vandalism of history is less likely than a dropped current-round row, but the blast radius is the whole ledger, and nothing mechanical notices.

### 7. `check_retired_wordings` is silent on emphasis, inline code, and restatement — the failure it was built for — **medium**

- **Location:** `scripts/validate.py:264-291`; claim at `REVIEW-ADJUDICATION.md:4047-4055`
- **Mechanism:** Live prose is flattened on whitespace, then matched against three regexes of exact retired phrases. `before the *ledger* is written` and `before the \`ledger\` is written` do not match `before the ledger is written`. A restatement ("the backlog file must exist before anyone writes the ledger file itself") does not match. `BACKLOG.md` and `calibration/**` are outside the live glob; the ledger, reports, and `examples/` are exempt so they can quote history.
- **Trigger:** The three `/tmp/vmut` insertions into `README.md` (emphasis, inline code, restatement); also `BACKLOG.md` and `calibration/README.md`.
- **Consequence:** Contract items 1 and 4. Whitespace-normalize *does* catch wrap — `before the\nledger is written` fired — which is the P-4 anecdote. The failure the check was created for, named in the brief and in C-6, is a rule that survives in other words or other markup. That path is silent. Exempting the ledger means a next-brief author can re-learn a retired rule from a historical quote with no mechanical flag; that exemption is defensible as history, and it is still a live input.
- **Status:** **CONFIRMED.** Exact phrase and wrap: CAUGHT. Emphasis, inline code, restatement, BACKLOG, calibration README: SILENT. Ledger quote: correctly exempt.
- **Why this rank:** the wrap case is the one the author already knows; leaving the restatement/markup misses in place is how X-2 and the three-site FIX LATER defect kept recurring.

### 8. Round 5's execution account says no shipped-program behaviour changed, while adding two failing checks to the only shipped program — **medium**

- **Location:** `REVIEW-ADJUDICATION.md:4018-4020, 4049-4057`; diff `2565c08..c62ca24 -- scripts/validate.py` (+53 lines, two functions, two `CHECKS` entries)
- **Mechanism:** §R5.15: *"Every change is prose or validator logic; no behaviour of any shipped program changed, because the repository ships no program but `scripts/validate.py`."* The same paragraph then reports the two new checks and *"the mechanical check caught it where four rounds of reading had not."* Those cannot both be true. The validator now errors on retired phrases and dangling `§N` that the previous commit accepted.
- **Trigger:** Any reader of §R5.15 taking "no behaviour changed" as a description of `c62ca24`. Also: running the pre- and post-commit validator on a tree that still carries a retired phrase.
- **Consequence:** Contract items 4 and 5. This is the session that extended the validator and then used it to certify its own output. The certification narrative is false on the one executable the repository ships. The "it caught our own regression" story is a claim by the party under review about a tool it had just written; the tool *can* catch a verbatim restore of two retired same-family phrases (I reproduced that class). That is not the same as "no behaviour changed."
- **Status:** **CONFIRMED** from the commit diff and the paragraph that cites it. `git show 2565c08:scripts/validate.py` has neither function.
- **Why this rank:** a false execution record is how the next brief's "already verified" section gets written; it is documentary, not a silent gate, so it sits below the gates that cannot fail.

### 9. `BACKLOG.md` B-3 still asserts ten checks and 9/9 break-tests after two untested checks were added — **medium**

- **Location:** `BACKLOG.md:95-108`
- **Mechanism:** B-3's 2026-08-22 status: *"covers ten of these"*, *"Each of the ten was break-tested"*, *"9/9 mutations were caught; the tenth check (installed copies match the repository) is a warning by design."* `CHECKS` now has 13 names / 12 functions. The two added in `c62ca24` are not in that inventory and were not in the 9/9. The 9/9 itself, re-run adversarially, is narrower than the invariants: `check_counts` catches a header mismatch and is silent on a dropped row; `check_table_pipes` fires on correct `\|`.
- **Trigger:** A reader discharging B-3, or a later brief treating 9/9 as the break-test result for the current harness.
- **Consequence:** Contract items 4 and 5. The backlog is the discharge record for the validator. It now understates what the harness claims to cover and overstates what was tested.
- **Status:** **CONFIRMED** by reading B-3 against `validate.py:315-329` and against the mutation table below.
- **Why this rank:** less blast than a silent gate, but it is the file that exists specifically so the next person does not have to re-read the review — and it is wrong about the thing it is carrying.

### 10. P-3 was withdrawn as a row because the matrix forbids `CONFIRMED`+`NO ACTION`, unlike round 4's X-series — **medium**

- **Location:** `REVIEW-ADJUDICATION.md:3884-3890` (withdrawal); `:3587-3597` (X-series kept as rows, excluded from the 27); `scripts/validate.py:180-192`; skill matrix `skills/review-adjudication/SKILL.md:420`
- **Mechanism:** P-3 recorded a true observation that is not a defect (both reviewers disclosed the collision without being forced). The only honest two-axis pairing is "true, and nothing to fix." That pairing is `CONFIRMED`+`NO ACTION`, which the validator rejects unless the verdict is `REFUTED` or `SETTLED ALREADY`. The session withdrew the ID rather than reuse it. Round 4 faced extra findings from outside the numbered set and **gave them rows** (`X-1`, `X-2`) so they stayed on the books while leaving `Findings in: 27` exact.
- **Trigger:** Any true non-defect observation that someone puts in a ruling table. Already happened once this round; the validator is what forced the withdrawal (`REVIEW-ADJUDICATION.md:3888-3890`).
- **Consequence:** Contract item 5. Withdrawing an ID is not the same as deleting the prose — the observation remains between table rows — but it is no longer a ruled entry with both axes, so it will not show up in a later census of dispositions. Round 4's answer to "extra item, keep the header exact" was a separate series with rows. Round 5's answer was to take the row off the books. Those are not the same answer.
- **Status:** **CONFIRMED** by reading both ledger sites and by `/tmp/vmut` `disposition-NO-ACTION-with-CONFIRMED` → ERROR.
- **Why this rank:** one observation, already written in prose, so the loss is bookkeeping rather than a vanished defect — but the matrix hole remains for the next true-non-defect, and the X-series precedent was available.

### 11. The new invariants index names `example-audit-prompt.md`, which does not exist, and no check notices — **medium** *(unseeded)*

- **Location:** `skills/adversarial-review-prompt/SKILL.md:27-31` (above the ~205 cut); `:256-258` (below the cut, "skip it without comment if absent"); `skills/adversarial-review-prompt/references/` (three files, no example)
- **Mechanism:** Round-5 item 1 put a "Supporting files" index inside `<invariants>` so operational names survive compaction. One of the names is `example-audit-prompt.md`. The file is deliberately unshipped. The sentence that says so sits at line 256, past the cut the same commit moved to ~205. `check_links` only follows markdown `](…)` and this is a bare filename, so the new backref-style check does not see it either.
- **Trigger:** A compacted session whose surviving prefix is the invariants block. Also any author who follows the index as a checklist of files to open.
- **Consequence:** Contract item 4, and the "did the fix open a new path to the failure it closed" test on item 1 / A-2. A-2 was *operational files below the cut*. The index is the remedy. The surviving prefix now names a missing file, and the "it is optional" qualifier does not survive. A compacted author is pointed at a file that is not there.
- **Status:** **CONFIRMED.** `ls skills/adversarial-review-prompt/references/` → `cover-note-template.md`, `prompt-template.md`, `why-this-is-hard.md`. Grep of `SKILL.md` for `example-audit-prompt`: lines 30 and 256 only.
- **Why this rank:** it is a new miss created by the round-5 fix, above the cut, with no mechanical catch; it is not a false-green on a security boundary, so it sits here.

### 12. Substring matching on `NO ACTION` and `**VERDICT**` misclassifies non-ruling table rows — **medium**

- **Location:** `scripts/validate.py:154-159, 168-192`
- **Mechanism:** `is_ruling_row` is "contains `**CONFIRMED`" (etc.). `check_no_action_legality` is `"NO ACTION" in line` plus a verdict that is not `**REFUTED`/`**SETTLED ALREADY`. Unbolded `CONFIRMED` is invisible (false negative). A notes-column citation of `**CONFIRMED**` is a ruling (false positive). A `**FIX NOW**` row whose notes mention the words `NO ACTION` fails disposition.
- **Trigger:** `| note | this cites **CONFIRMED** as a word in notes, not a ruling | - | see above |` and `| Z-NOTE | mentions NO ACTION in notes | **CONFIRMED** | **FIX NOW** — not NO ACTION |`
- **Consequence:** Contract items 1 and 2. The P-3 incident is this class on the true pairing; the substring form will also fail correct rows that discuss the pairing. Unbolded verdicts — the obvious way a skeleton row looks before fill-in, if anyone leaves one — are silent.
- **Status:** **CONFIRMED.** `/tmp/vmut`: unbolded CONFIRMED → CLEAN (silent miss); notes `**CONFIRMED**` → ERROR two-axes; `NO ACTION` in a FIX NOW notes cell → ERROR disposition.
- **Why this rank:** already bit this round on the legal-pairing side; the false-positive form is waiting for the next notes cell that names the forbidden pair.

### 13. `--list` prints 13, success prints 12, and a skipped frontmatter check still counts as a passing check — **low**

- **Location:** `scripts/validate.py:315-349, 46-52`
- **Mechanism:** `CHECKS` holds 13 tuples; two of them are `check_frontmatter`. `main()` dedupes by function and prints `All {len(ran)} checks pass`. `check_frontmatter` on missing PyYAML warns and returns. That function is still added to `ran`. `--list` therefore advertises 13 independent named checks, including a permissions check that cannot run without the frontmatter function, and a missing-yaml run still says 12 passed.
- **Trigger:** `PYTHONPATH` pointing at a `yaml.py` that raises `ImportError`; also simply reading `--list` next to the success line.
- **Consequence:** Contract items 1 and 4. Without PyYAML, a `Write` in `allowed-tools` is not checked and the run is still a pass. The 12-vs-13 mismatch is the user-visible tell; the skip-counts-as-pass is the load-bearing half. (A YAML *string* `allowed-tools: Read, Grep, Write` is also silent — `set("Read, Grep, Write")` is a set of characters — but this repository currently uses lists, so that path is latent here.)
- **Status:** **CONFIRMED.** `--list` → 13 lines. Normal run → `All 12 checks pass (5 warning(s))`. Hidden-yaml run → `WARN frontmatter: PyYAML not installed - skipped` then `All 12 checks pass (6 warning(s))`.
- **Why this rank:** PyYAML is present on this machine and likely on any machine that already runs the other Python in the repo; the lie is in the success line, not a currently-open grant.

### 14. `CNV-R5-3` remains an open `VERIFY` row after §R5.17 says it was disposed — **low** *(unseeded)*

- **Location:** `REVIEW-ADJUDICATION.md:3928` vs `:4037, :4087`
- **Mechanism:** Item 9 replaced the `jsonc` snippet with plain `json` and said that disposes `CNV-R5-3`. §R5.17 repeats the disposal. The §R5.9 table still carries `**COULD NOT DETERMINE**` / `**VERIFY** — write a commented settings file and start Claude Code.` `check_ledger_axes` is happy: both cells are filled. `check_counts` does not look at CNV rows.
- **Trigger:** A later reader of "what is still open," or a later brief copying the CNV list as unanswered.
- **Consequence:** Contract item 5. The current round now records both "this is disposed" and "this is still to verify." The open row is the one a census will pick up.
- **Status:** **CONFIRMED** by reading the three sites. No execution needed.
- **Why this rank:** one CNV, already answered in prose two sections later; the cost is a contradictory current-round table, not a missing gate.

### 15. This brief and its cover note do not agree on the network/web-search permission — **low** *(process)*

- **Location:** `EXTERNAL-REVIEW-6-PROMPT-GROK.md:236` (`Network: No installs. Web search allowed; cite URLs`); `EXTERNAL-REVIEW-6-COVER-NOTE-GROK.md` (no Network/Web-search axis; "run read-only commands in it, and do anything you like under `/tmp`")
- **Mechanism:** `adversarial-review-prompt` invariant 3 and §8 require brief path, report path, and **every permission** to agree exactly, and tell the reviewer to report a disagreement as a process finding. Report path and `/tmp` mutation agree. Network does not: the brief grants web search; the cover note is silent. The skill's own example of the defect is "a cover note that says read-only while the brief authorizes mutation"; this is the same shape on a different axis, by omission rather than by opposite instruction.
- **Trigger:** This run. I followed the brief (web search allowed, unused).
- **Consequence:** The envelope-agreement rule failed on the round that exists to audit the half that writes envelopes. Low blast: the two documents do not *forbid* opposite actions; one is silent.
- **Status:** **CONFIRMED** by diffing the two files. No other brief/cover contradiction on report path, write path, or `/tmp` mutation was found. The pytest-in-`/tmp` gotcha is stated in both.
- **Why this rank:** last, because it did not spend this run and is omission rather than collision — but the brief asked for it, and the previous round's lost half started as a cover-note/brief pairing failure.

---

## Mutation results

Harness: `/tmp/vmut_run.py` against a `cp -a` of the repo at `/tmp/vmut`. Baseline on the copy: `All 12 checks pass (5 warning(s))` — three table WARNs, two install WARNs. 51 probes.

| Check (named) | What was broken | Result |
|---|---|---|
| frontmatter | missing `allowed-tools`; invalid YAML; no opening `---`; no `SKILL.md` | CAUGHT ×4 |
| permissions | `Write` granted; `Bash` granted | CAUGHT ×2 |
| permissions | `allowed-tools: Read, Grep, Write` as a YAML string | **SILENT** |
| length | pad `split("\n")` to 502 | CAUGHT |
| length | exactly 499 `split("\n")` | CLEAN (pass) |
| placeholder | `«»` outside code | CAUGHT |
| placeholder | `«»` inside backticks; inside a ` ``` ` fence | CLEAN |
| links | broken relative | CAUGHT |
| links | titled link to a real file (`](why-this-is-hard.md "background")`) | **FALSE POSITIVE** |
| table | unescaped `` `a|b` `` in current round | CAUGHT |
| table | escaped `` `a\\|b` `` in current round (valid GFM) | **FALSE POSITIVE** |
| table | unescaped pipe in a closed round | WARNED (as designed) |
| table | code span opened on one table line, closed on the next | CAUGHT (counts pipes while `in_code`) |
| two-axes | `**CONFIRMED**` without a disposition, current round | CAUGHT |
| two-axes | unbolded `CONFIRMED` without a disposition | **SILENT** |
| two-axes | `**CONFIRMED**` only in notes of a non-ruling row | **FALSE POSITIVE** |
| disposition | `**CONFIRMED**` + `**NO ACTION**` | CAUGHT |
| disposition | `**REFUTED**` + `**NO ACTION**`; `**ACCEPTED AS-IS**` | CLEAN |
| disposition | `NO ACTION` mentioned in a `FIX NOW` notes cell | **FALSE POSITIVE** |
| last_round | `**CONFIRMED**` without disposition in the closed prefix; round-1 count mismatch | **SILENT** (as scoped) |
| counts | header 22 vs 21 | CAUGHT |
| counts | delete `grok-9` row, header still 22/22 | **SILENT** |
| counts | new `# Round 99` with no numbers | WARNED |
| calibration | digest `deadbeefdead`; missing digest row | **WARN, exit 0** |
| retired | exact phrase; wrapped across a line break; `never saw the report`; "least likely to catch" | CAUGHT ×4 |
| retired | `*ledger*` emphasis; `` `ledger` ``; restatement in other words; `BACKLOG.md`; `calibration/README.md` | **SILENT** ×5 |
| retired | quote in the ledger (exempt) | CLEAN |
| backref | `§99`; `## 7.` heading stripped of its period | CAUGHT ×2 |
| backref | cite existing wrong section; no `<invariants>` block | **SILENT** |
| valid-unusual | CRLF `SKILL.md`; skill with no `references/` and no relative links; last round `Findings in: 0 · Rows out: 0` | CLEAN |
| PyYAML absent | `import yaml` raises | frontmatter **skipped**, still `All 12 checks pass` |

**What stays silent, in one list:** YAML-string `Write`; dropped ruling row with a consistent header; stale calibration digest (as a failing run); closed-round two-axes/counts; unbolded verdict; retired phrase broken by emphasis or inline code; retired phrase restated; retired phrase in `BACKLOG.md` / `calibration/`; unfaithful-but-existing `§N`; missing `<invariants>` block; skipped frontmatter counted as a pass.

Original ten, under this harness: 8 of 10 fire on a direct break of the form the check names. The two that do not enforce their named invariant are **counts** (header-only) and **calibration digest** (warn-only). **table** fires on both the real defect *and* correct work. **install** is a warning by design (already firing on this machine). The two new checks both fire on a verbatim break and both stay silent on the defect class that justified them.

---

## The unseeded pass

Set the 20 claims aside and read the round-5 diff, both invariant blocks, and the execution/status sections as documents.

Produced two findings that were not a claim sub-question:

- **Finding 11** — invariants index names a file that ships absent; the optional-skip sentence is below the cut. Item 1 / A-2's remedy.
- **Finding 14** — `CNV-R5-3` still an open `VERIFY` row after two later sections say it is disposed.

Looked at, and not raised:

- `review-adjudication/SKILL.md` 499→497 `split("\n")` (498→496 `wc -l`): the why-block was compressed; "scaffold only" and "paragraph of reading" survive in `references/why-this-is-hard.md`. No unique operational rule was found only in the deleted lines.
- Prefix append of the ledger: parent blob is an exact byte prefix of HEAD. The rewrite of invariant 1 from unconditional append-only to "current round filled in place, completed rounds append-only" matches §7 and step 2 as they already stood. That is a genuine correction of an over-broad summary, not a rule widened in order to violate it. Round 5 is still `OPEN`, so `✔ executed` backfill is in-place fill of the current round, which is what the rewritten rule describes.
- Install warnings: correct; Q-4 already records them. Not re-reported.
- Isolation-is-not-confinement: already F12 / round 1. The VOID run is that bound demonstrated, not a new class.
- "The validator only checks form, not truth": already B-3's measured bound. Not re-reported. The specific form-checks that do not check their named form *are* reported above.

---

## Claims examined and upheld

1. **All twelve checks fail when their invariant is broken.** **REFUTED** by the mutation table. Several named invariants stay silent on a break (counts/rows, digest-as-error, retired restatement/markup, backref faithfulness). The original ten each fire on a *narrow* mutation of the form the author likely used; that is not the same as the invariant.
2. **The two checks added in this range were break-tested.** **REFUTED** as a historical claim (B-3 and §R5.15 describe an accidental catch of `check_retired_wordings`, not a break-test of either new check). **Now tested:** both can fail; both have silent gaps (finding 3, finding 7).
3. **No check fires on correct work.** **REFUTED.** Valid `\|` in a current-round table is an ERROR; titled markdown links to real files ERROR; `**CONFIRMED**` in notes and `NO ACTION` as a substring ERROR. Unusual-but-valid that *did* stay green: guillemets in backticks, CRLF, no `references/` directory once links are gone, last round `0/0`.
4. **`check_retired_wordings` does what §R5.15 claims.** **CONFIRMED** for whitespace wrap. **REFUTED** for emphasis, inline code, footnotes-not-tested, and restatement. Finding 7.
5. **File scoping is right.** **REFUTED** as "right." Ledger/examples exemption is required for history and is implemented. The ledger is also live input to the next brief, and `BACKLOG.md` / `calibration/` are live operator prose outside the glob. A retired rule can sit in those places forever.
6. **`check_invariant_backrefs` is worth its line count / can it fail on this repo.** It **can** fail (dangling `§99`). On the shipping tree every `§N` in both invariants blocks names a real `## N.` section. **REFUTED** as the A-3 remedy (finding 3). Existence is a real, cheap check; it is not the check that was queued.
7. **Thirteen vs twelve.** Neither number is a lie about a count of something real. `--list` prints 13 names; `len(ran)` is 12 unique functions; two names share `check_frontmatter`. The misleading sentence is `All 12 checks pass` after a skipped frontmatter run (finding 13). To `--list`, 13 overstates independence. To the success line, 12 understates the named set and counts a skip as a pass.
8. **`is_ruling_row` distinguishes a ruling from prose naming a verdict.** **REFUTED.** Requires a bolded verdict (unbolded miss); any table row containing `**CONFIRMED` is a ruling (false positive). Finding 12.
9. **`last_round` scoping is right.** **REFUTED** as a complete story; **CONFIRMED** that during round 5 it applied to round 5 and therefore caught P-3. Closed-round defects are invisible. Finding 6. Git confirms *this* commit did not edit the 3623-line prefix.
10. **`check_counts` verifies count-in equals count-out.** **REFUTED.** It verifies the two header numbers equal each other. Finding 1. Round 5's 22/22 happens to match the 22 rows in §R5.4 (13 Codex + 9 Grok); the check did not establish that.
11. **`check_table_pipes` catches unescaped pipes; backtick parity is per line; the three warnings.** **REFUTED** on escaped pipes and on "the three warnings are real splits." **CONFIRMED** that an unescaped `|` inside inline code in the current round errors, and that a code span left open on a table line is treated as in-code. Finding 5.
12. **`corpus_digest` reimplements `record-template.md:14` faithfully.** **CONFIRMED on this tree, this OS:** both produce `775e1cc8c43f`; inner SHA-1s of all 19 tracked paths match byte-for-byte. Python `sorted()` of bytes matched `sort -z` on this ASCII corpus, including a file named `a file.txt`. If they diverged, the template command is the one records name; the Python copy is what `check_calibration_digests` uses. They did not diverge here.
13. **The twelve are the right twelve.** **REFUTED.** Mechanically checkable and unchecked: actual row counts; digest mismatch as ERROR; record expiry; `\|` awareness; `§N` faithfulness; cover-note/brief/report-path agreement; no-filesystem variant consistency with the filesystem one. Of B-3's still-uncovered three, **no-filesystem template consistency** is the one that already paid across rounds 3 and 5 (`grok-4` / `codex-8`). P-1 (wrong cover note pasted) was not a disk-state defect — both cover notes on disk were correctly paired — so a repo validator would not have caught it. The most expensive *still-open* mechanical gap relative to this skill's founding defect is finding 1 (count the rows).
14. **`git ls-files` ended artifact-inclusion.** **CONFIRMED.** `python3 -m pytest` on both fixture cases in `/tmp/digest-r6` wrote `__pycache__` (now also gitignored) and left the digest at `775e1cc8c43f`. **What it silently misses:** never-added instrument files (new case, new key); and, contrary to the docs, it does *not* miss tracked-file edits (finding 2). `calibration/README.md` is excluded by design.
15. **The digest is portable across machines.** **CONFIRMED** for a second location under `/tmp` on this OS (`/tmp/digest-elsewhere/copy` → `775e1cc8c43f`). **COULD NOT DETERMINE** for a different OS's `shasum`/`sha1sum` default; the Python `hashlib.sha1` path is the portable half.
16. **Both filed records match the instrument; isolation is sufficient.** **CONFIRMED** both records pin `775e1cc8c43f`, which is the current instrument. Isolation-as-adjacent-hygiene is already F12; not re-reported. Nothing mechanical catches rooting at the repository — the VOID run is that miss, caught only because the reviewer disclosed it. Expiry is not checked by the validator at all (both records expire 2026-09-21; today is inside the window).
17. **`grok-4.6-high.md` accurately describes the six runs.** **CONFIRMED** on the scores, headlines, mutation table, secondaries, and workload line-count: the six reports sum to **500** lines, matching the record. Headlines match (`limits.py` absence; Goal 2 undelivered; both checksum primaries with `return True` → 3 pass; service-role key on a `"use client"` fetch). Clean cases: copy-link "None. Ranked list is empty."; wordcount stand-ins recorded. Answer-key-exposure caveat is **correctly scoped** (detection vs priming; VOID named). The one inaccuracy: the remedy is pointed at `BACKLOG.md` `B-1` (corpus-drift gate); private replacement is `B-2`. Not ranked separately — it does not overstate what the six runs established.
18. **Round 5 header arithmetic is exact; P-3 withdrawal.** **CONFIRMED** on the numbers that are claimed: 22 rows in §R5.4 (codex-1..13, grok-1..9); process table has P-1, P-2, P-4 (three); CNV-R5-1..7 (seven); D-1..8 (eight); U-1..4 (four) with "18 sampled · 4 re-opened." **Not in the header formula:** A-1..A-3 (three, two-axis rows) and C-5, C-6. The skill's header grammar has no slot for adjudicator-raised findings; round 1 counted that class as process (its P-3). P-3 withdrawal: finding 10. Withdrawing an ID to escape an illegal pairing is not the same as the X-series (extra defects, extra rows, header held at 27).
19. **Round 5 append discipline; the rewritten rule.** **CONFIRMED** that lines 1–3623 are byte-identical to `2565c08` (`git show 2565c08:REVIEW-ADJUDICATION.md` is an exact prefix of HEAD; `git diff` hunk is `@@ -3621,3 +3621,481 @@`). The in-place `✔ executed` markers sit *inside* round 5, which is still `OPEN`. The invariant rewrite is a genuine correction of an over-broad summary that contradicted §7 and step 2; it is the rule those sections already stated. I **COULD NOT DETERMINE** from git alone that markers were added *after* an earlier write of the same round — `c62ca24` is one snapshot — only that the final rule permits that sequence and the prefix was not rewritten.
20. **§R5.15's account is accurate and complete.** **CONFIRMED** that nineteen queue items have corresponding edits (spot-checked items 2, 6, 9, 11, 12, 14, 15, 18 in the files; 17 and 19 exist as the two new functions); that `review-adjudication/SKILL.md` is 497 `split("\n")` / 496 `wc -l`; that the why-block compression did not drop unique operational text (it lives in the reference). **REFUTED** "no behaviour of any shipped program changed" (finding 8). **REFUTED** that item 17 implements A-3 (finding 3). **REFUTED** that `CNV-R5-3`'s table row matches the disposal claim (finding 14).

---

## Could not verify

- Whether `check_retired_wordings` would catch a footnote-broken phrase (`before the ledger[^1] is written`) — not separately mutated; predicted silent on the same mechanism as emphasis.
- Linux/`sha1sum` vs macOS/`shasum` on the template command (Python half is portable).
- Whether a compacted Claude Code session, given only the surviving invariants prefix, errors, skips, or invents `example-audit-prompt.md`.
- The intra-session order of round-5 skeleton vs `✔ executed` backfill (single snapshot commit).
- Record expiry enforcement (not implemented; both records are still inside their 30-day window).
- Whether `allowed-tools` as a YAML string appears in any installed copy of these skills at `~/.claude/skills/` (the check is silent on that form; this repo's copies use lists).

---

## Disagreements with the prior rounds

- **A-3 `✔ executed` is not a close.** Round 5 recorded the unfaithful-summary class and then closed it with an existence check. That is the same shape it named in C-6 / U-4 / X-1: a fix that reaches one site (or one cheap half) of a claim living at several.
- **B-3's 9/9 is the author's testimony about a narrower mutation set than the invariants.** Re-run, `check_counts` and `check_calibration_digests` do not enforce the invariants they are named for, and `check_table_pipes` fails correct work. The 9/9 can be true of the mutations that were performed and still false of the claims those checks make.
- **Round 4's X-series and round 5's P-3 are opposite answers to "item not in the numbered findings-in."** X-series: rows, own IDs, header held. P-3: ID withdrawn so the validator will not fail an illegal pairing. The matrix still cannot represent "true, not a defect."
- **§R5.15's "the mechanical check caught it where four rounds of reading had not"** is a claim about `check_retired_wordings` catching a verbatim restore of retired phrases in `prompt-template.md`. I did not re-perform that historical run; I did confirm the check fires on those phrases. I do not accept it as evidence that the validator "earns its place" beyond "it greps for three strings." Finding 7 is what that check does not catch.
- **§R5.17 vs §R5.9 on `CNV-R5-3`:** the status section is ahead of the table it claims to have closed. Finding 14.

No disagreement with the round-5 ruling that this half was unaudited (`P-1`, `CNV-R5-7`). That was accurate, and it is why this report exists.
