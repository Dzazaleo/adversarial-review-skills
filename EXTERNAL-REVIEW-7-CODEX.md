# External Review 7 (Codex) — scripts/validate.py

Reviewer identity: OpenAI GPT-5.6 family, Codex; product/version: Codex (exact product version not exposed); reasoning effort: not exposed; served model alias verbatim: not exposed to the model.

## Coverage

**20 of 20 claims engaged.** Read all 519 lines of `scripts/validate.py`, its complete pinned diff, the relevant ledger rounds and mutation record, the calibration record template and filed records, and the skill/template grammar consumed by the checks. Reproduced baseline (`12 of 12 checks pass (2 warning(s))`), broke all 12 implementations in a `/tmp` copy, ran more than 20 focused counterprobes, compared every ledger round's stated and parsed counts, ran the Python and shell digests, and performed a separate unseeded source pass. I did not run the calibration pytest fixtures because no validator path executes them; I changed no repository file other than this report.

The range inventory reproduces as 15 files, 491 insertions and 171 deletions only with all review artifacts excluded. The pre-range validator length does not reproduce; see finding 13.

| Claim | Outcome | Independent basis |
|---:|---|---|
| 1 | **REFUTED** | Two backslashes before a delimiter merge the next cell; executed missing-axis bypass. |
| 2 | **REFUTED** | Trailing empty/post-disposition cells make a ruling invisible; real ruling rows are four or five cells, while the ledger also has three-cell non-ruling tables. |
| 3 | **REFUTED** | `***CONFIRMED`, `CONFIRMED by execution`, and `CONFIRMEDLY` all match; `_**CONFIRMED**_` does not. |
| 4 | **REFUTED** | First-mention parsing returns quoted `NO ACTION` and returns nothing for the skill's compound `PENDING OWNER — proposed: ...` form. |
| 5 | **REFUTED** | Qualifiers containing commas/apostrophes are swallowed into an unknown token; periods and em dashes split real disposition spellings. Thirteen real main-ledger rulings return no declared disposition. |
| 6 | **REFUTED** | `| --- |`, `| : |`, and `| -- | :- |` are discarded wherever they occur, including a data-row position. |
| 7 | **REFUTED** | `C1-3`, `D7-2`, `Q-3`, and `A1-3` all match the auxiliary regex. |
| 8 | **REFUTED** | Parsed actuals: round 2 9/9, round 3 11/11, round 4 **26/27**, round 5 22/22, round 6 15/15; the pre-heading adjudication is omitted. |
| 9 | **REFUTED** | Deleting a closed round-5 ruling row was silent. |
| 10 | **REFUTED** | No-heading input is treated as current, but a last section with no census only warns; the real pre-heading first adjudication is not returned by `rounds()`. |
| 11 | **CONFIRMED** | Direct boundary probe: heading-line index warns, first possible row errors; a row cannot also occupy the heading line. |
| 12 | **CONFIRMED** | `last_round` and `current_round_line` use identical marks and agree at byte 0 and with/without a preface. |
| 13 | **CONFIRMED** | Closed-prefix violations warn and exit 0; this confirms behavior, not policy soundness, and finding 2 shows why position is not provenance. |
| 14 | **REFUTED** | Same record passed/failed by timezone; impossible `9999-99-99` passed. |
| 15 | **REFUTED** | Clean tree agrees at `775e1cc8c43f`; a tracked newline-bearing filename yields Python `c35660012344` versus shell `5f5a9b6f4f7f`. |
| 16 | **REFUTED** | Documented `Edit(/src/**)` grant is invisible; nested YAML crashes; quoted/block strings do expose bare `Write`; null becomes empty. |
| 17 | **REFUTED** | Angle-bracket and balanced-parenthesis destinations false-fail; a missing reference-style target is silent. |
| 18 | **CONFIRMED** | A marker split after `[^` across a newline is removed and the phrase is caught; none of the three retired phrases contains `_`, so underscore stripping does not change them. |
| 19 | **REFUTED** | Fenced content is suppressed, but valid two-backtick inline code false-fails and paired unmatched backticks can suppress intervening prose. |
| 20 | **REFUTED** | A caught digest exception still prints `1 of 1 checks pass`; an uncaught check exception aborts before any total. The `--list` subtraction counts excess names, though its wording is imprecise for three aliases. |

## Findings, ranked

### 1. Scoped write-capable grants bypass the permissions gate — Impact: high

**Rank rationale:** this silently defeats the repository's no-write permission invariant using syntax the target product explicitly documents, across either shipped skill.

**Location:** `scripts/validate.py:42`, `:72-79`. **Mechanism:** the gate intersects exact strings with `{"Write", "Edit", "NotebookEdit", "Bash", "Agent"}`; it never extracts a tool name from `ToolName(specifier)`. Claude Code says skill `allowed-tools` accepts that rule format and that `Edit(/src/**)` applies to Edit, Write, and NotebookEdit ([official tools reference](https://code.claude.com/docs/en/tools-reference)). **Trigger:** replace the clean list with `Read` and `Edit(/src/**)`. **Consequence:** a write-capable pre-approval ships under `12 of 12 checks pass`, violating contract items 1, 3, and 4. **Status: CONFIRMED** — executed; exit 0, only the two expected history warnings plus a host install-drift warning.

### 2. Line position is mistaken for historical provenance — Impact: high

**Rank rationale:** one ordinary-looking fenced example can downgrade every real current-round ledger error before it from build failure to non-failing history.

**Location:** `scripts/validate.py:151-169`, `:218-240`, `:295-345`. **Mechanism:** every source line matching `^# Round \d+` is a round boundary even inside a fenced code block; `reporter` then treats all lower line numbers as immutable history. The same position-only rule also lets a newly introduced corruption in a genuinely closed prefix warn instead of fail; it never establishes that the bytes are historical. **Trigger:** remove the disposition from real current row 4594, then append a fenced `# Round 999`. **Consequence:** the missing disposition becomes `WARN`, the fake round's missing census also only warns, and the final line is `12 of 12 checks pass (4 warning(s))`; contract items 1 and 4 fail. **Status: CONFIRMED** — executed end to end. The two permanent warnings at 2383–2384 were excluded from the finding.

### 3. The count check can be absent, can omit whole historical sections, and can reject a correct prior census — Impact: high

**Rank rationale:** the only check intended to bind input findings to output rows can certify no current census at all and has no stable interpretation across the repository's own round formats.

**Location:** `scripts/validate.py:295-349`. **Mechanism:** a missing current `Findings in`/`Rows out` pair calls `warn`, not `err`; `rounds()` drops everything before the first numbered heading; closed rounds skip actual row counts; and `count_finding_rows` cannot represent round 4's documented rule that its 27th reviewer finding was filed as process row `P-1`. **Triggers:** delete the round-6 census; change the pre-heading `Rows out: 15` to 99; delete a round-5 ruling row; truncate after round 4 so it becomes current. **Consequence:** the first three states exit 0 (the missing census still prints `12 of 12 checks pass`), while the correct round-4 27-row record false-fails as 26; contract items 1, 2, and 4 fail. **Status: CONFIRMED** — all four mutations executed.

### 4. Same-cell mentions still stand in for verdict and disposition commitments — Impact: high

**Rank rationale:** a row can be certified with an absent disposition or an illegal pairing, while the skill's prescribed compound `PENDING OWNER` form can be rejected.

**Location:** `scripts/validate.py:172-183`, `:242-283`. **Mechanism:** `check_ledger_axes` uses `any(d in cell ...)`; legality searches the entire verdict cell for any allowed verdict; `declared_disposition` selects the first bolded known token and cannot parse the documented `**PENDING OWNER — proposed: ...**` compound. **Triggers:** disposition `Nothing decided; explicitly not FIX NOW`; verdict `**CONFIRMED**; earlier reviewer said **REFUTED**` with `**NO ACTION**`; valid `**PENDING OWNER — proposed: NO ACTION**`. **Consequence:** the first two forbidden states exit 0; the valid compound exits 1 as an illegal `NO ACTION`, violating contract items 1–3. **Status: CONFIRMED** — all three directions executed. This is the next path through the round-6 whole-line-scan fix, not a re-report of that fixed bug.

### 5. A digest computation failure is still counted as a passing calibration check — Impact: medium

**Rank rationale:** the validator's most explicit stale-record gate can decline to compute its evidence and nevertheless increase the pass numerator.

**Location:** `scripts/validate.py:357-379`, `:496-514`. **Mechanism:** `check_calibration_digests` catches any digest exception, warns, and returns without adding itself to `SKIPPED`; `main` therefore includes it in `passed`. Separately, Python reconstructs `shasum` output instead of consuming the same byte stream, so Git-legal unusual names diverge. **Triggers:** force `corpus_digest()` to raise `OSError("git unavailable")`; add a tracked calibration filename containing a newline. **Consequence:** the first prints `1 of 1 checks pass (1 warning(s))`; the second gives Python `c35660012344` and template `5f5a9b6f4f7f`, violating contract items 1, 4, and 5. **Status: CONFIRMED** — executed; the present 19-file tree is the pass complement and agrees at `775e1cc8c43f`.

### 6. Expiry results depend on local timezone and impossible dates are accepted — Impact: medium

**Rank rationale:** valid calibration records near their boundary produce different build results on different machines, and malformed records can remain valid indefinitely.

**Location:** `scripts/validate.py:388-393`. **Mechanism:** the check lexically compares a regex-shaped string with local `date.today().isoformat()`; it neither selects a repository timezone nor parses a calendar date. **Triggers:** at the same instant, records expiring `2026-08-22` under `TZ=Pacific/Kiritimati` and `TZ=Pacific/Pago_Pago`; expiry `9999-99-99`. **Consequence:** the first machine exits 1, the second exits 0, and the impossible date exits 0, violating contract items 3 and 5. **Status: CONFIRMED** — executed end to end.

### 7. The link checker rejects valid inline links and ignores reference links — Impact: medium

**Rank rationale:** common, specification-valid documentation edits can either block the repository or ship with a broken target.

**Location:** `scripts/validate.py:109-123`. **Mechanism:** one regex stops at the first `)` and retains angle brackets as filename characters; it never parses link reference definitions. CommonMark permits pointy-bracket destinations, balanced parentheses, and reference links ([official CommonMark specification](https://spec.commonmark.org/spec)). **Triggers:** valid `<references/prompt-template.md>`; valid existing `references/a(b).md`; `[Broken][missing]` with `[missing]: references/does-not-exist.md`. **Consequence:** the first two exit 1 and the missing target exits 0, violating contract items 1–3. **Status: CONFIRMED** — all three executed.

### 8. The ruling-row parser does not implement GFM boundaries or exact verdict grammar — Impact: medium

**Rank rationale:** the parser can hide an absent ledger axis or reject a correct row solely because of valid delimiter spelling.

**Location:** `scripts/validate.py:138-141`, `:172-210`. **Mechanism:** `(?<!\\)\|` tests only the immediately preceding byte rather than backslash parity; `[1:-1]` unconditionally discards a trailing segment even though a trailing pipe is optional; `ruling_cells` assumes the last two cells rather than the table's headers; `^\**VERDICT` is a prefix rather than an exact cell grammar; and `table_rows` discards every all-dash/colon row without knowing whether it occupies the delimiter position. GFM explicitly permits inconsistent leading/trailing pipes and arbitrary-text data cells ([GFM table specification](https://github.github.com/gfm/#tables-extension-)). **Triggers:** a cell ending in the literal-backslash spelling `\\` immediately before a real delimiter, a valid row without a trailing pipe, a trailing empty/post-disposition cell, `CONFIRMEDLY`, `_**CONFIRMED**_`, or an all-punctuation data row. **Consequence:** later columns merge or disappear, non-verdict prose can become a ruling and marked-up verdicts can vanish; a missing disposition in a real auxiliary row was silent, while the no-trailing-pipe correct row false-failed the count 15→14, violating contract items 1–3. **Status: CONFIRMED** — direct cell traces plus end-to-end mutations.

### 9. Frontmatter extraction and type handling reject or crash on legal YAML text — Impact: medium

**Rank rationale:** routine description punctuation can block correct skills, while malformed field structure produces a traceback instead of a validator result.

**Location:** `scripts/validate.py:59-76`. **Mechanism:** `text.split("---")[1]` treats any triple hyphen inside frontmatter as the closing delimiter; `set(raw)` assumes a flat hashable sequence. **Triggers:** `---` inside the quoted description; nested sequence item `[Write]`. **Consequence:** the valid quoted scalar is truncated and false-fails; the nested value raises uncaught `TypeError` with no final summary, violating contract items 2–4. **Status: CONFIRMED** — both executed. Pass complements: quoted and block-scalar bare `Write` values normalize to `Write`; null becomes an empty grant.

### 10. Auxiliary-ID guessing excludes legitimate reviewer findings — Impact: medium

**Rank rationale:** plausible reviewer tags are silently reclassified, turning a correct census into a false build failure and making the counter unusable for that reviewer.

**Location:** `scripts/validate.py:286-317`. **Mechanism:** `^(CNV|[PDUACXQ])[0-9]*(-|$)` reserves seven single letters without consulting an explicit row class or ID grammar. **Triggers:** `C1-3`, `D7-2`, `Q-3`, or `A1-3`; renaming a real current finding to `C1-3`. **Consequence:** the correct finding is excluded and the count falls 15→14; round 4's `P-1` demonstrates the inverse real format problem, violating contract items 2 and 3. **Status: CONFIRMED** — direct classifications and end-to-end rename executed.

### 11. Single-backtick pseudo-parsing breaks two checks in opposite directions — Impact: medium

**Rank rationale:** less-common but fully valid code-span syntax both hides actual table corruption and blocks correct explanatory prose.

**Location:** `scripts/validate.py:153-165`, `:93-106`. **Mechanism:** `check_table_pipes` toggles state per backtick and `check_placeholders` removes only `` `...` `` pairs; CommonMark code delimiters are runs of one or more equal-length backticks ([code-span specification](https://spec.commonmark.org/spec#code-spans)). **Triggers:** current row ````| aux | ``unescaped | pipe`` |````; guillemets inside ```` ``«placeholder»`` ````. **Consequence:** the extra cell delimiter is silent, while valid inline code raises a placeholder error; contract items 1–3 fail. **Status: CONFIRMED** — both executed. A triple-backtick fence happens to pass, showing the recorded fence behavior is an accident of the regex rather than the stated inline-code rule.

### 12. Installed-copy output is intentionally machine-dependent despite contract item 5 — Impact: low

**Rank rationale:** it changes warning counts and final output across otherwise identical checkouts, but cannot itself fail the build.

**Location:** `scripts/validate.py:398-410`. **Mechanism:** the check reads `~/.claude/skills`, a per-user path outside the repository. **Trigger:** no installed directory, an identical installed copy, and a drifted installed copy. **Consequence:** the first two produce no install warning and the third does, so the reported result depends on the machine, contradicting contract item 5. **Status: CONFIRMED** — simulated with three temporary installed states. This appears deliberate; intention does not reconcile the stated contract.

### 13. The brief's validator baseline is not the pinned range's baseline — Impact: low

**Rank rationale:** the wrong size does not change code behavior, but it misstates how much executable code the review range added.

**Location:** `EXTERNAL-REVIEW-7-PROMPT-CODEX.md:3`, `:84` and the user's cover note. **Mechanism:** both say the file was 354 lines before `2565c08..d610112`; the pinned blob is 301 lines. **Trigger:** `git show 2565c08:scripts/validate.py | wc -l`. **Consequence:** the audit inventory is off by 53 lines and conflicts with the immutable range, a process-evidence defect rather than a product defect. **Status: CONFIRMED** — 301 at `2565c08`, 301 at its parent, 519 at `d610112`; numstat is 261 additions/43 deletions. The brief's `main` range also ends at nonexistent line 520 (the file ends at 519).

## Mutation results

All commands ran against copies under `/tmp/external-review-7-codex.PchSmt/`; the repository target was not mutated. The two consolidated commands were `python3 -u /tmp/external-review-7-codex.PchSmt/matrix.py` and `python3 -u /tmp/external-review-7-codex.PchSmt/probe_validate.py`.

| Implementation | Deliberate break that fired | Correct or adversarial complement |
|---|---|---|
| `check_frontmatter` | bare list `Write` → permissions error | baseline clean; scoped `Edit(...)` silent; quoted/block bare `Write` caught; nested list crashes; quoted `---` false-fails |
| `check_skill_length` | split-line count 500 → length error | baseline split-count 494/497 clean |
| `check_placeholders` | bare `«missing»` → placeholder error | single-backtick and fenced examples clean; valid two-backtick span false-fails |
| `check_links` | missing inline target → link error | titled existing links clean; angle/balanced valid links false-fail; reference-style missing target silent |
| `check_table_pipes` | single-backtick unescaped pipe → table error | escaped pipes clean; two-backtick unescaped pipe silent |
| `check_ledger_axes` | exact missing disposition → two-axes error | valid baseline clean; mere `FIX NOW` mention bypasses; even-backslash row bypasses |
| `check_no_action_legality` | exact `CONFIRMED` + `NO ACTION` → disposition error | legal baseline clean; quoted `REFUTED` bypasses; compound `PENDING OWNER` false-fails |
| `check_counts` | delete current numbered row → count error | baseline clean; missing header, pre-heading vandalism, and closed-row deletion all exit 0; round 4 false-fails if current |
| `check_calibration_digests` | digest `deadbeefdead` → calibration error | baseline digest/expiry clean; exception counts pass; timezone and invalid-date failures above |
| `check_installed_copies` | drifted simulated installed copy → install warning | absent and identical copies clean; machine changes output by design |
| `check_retired_wordings` | verbatim retired phrase in `README.md` → retired error | baseline and ledger-history quote clean; footnote-split phrase caught; no retired regex contains underscore |
| `check_invariant_backrefs` | `§1` → `§99` → backref error | baseline references clean |

Focused counterprobe outputs used in the findings:

| Probe | Observed |
|---|---|
| `Edit(/src/**)` grant | exit 0; `12 of 12 checks pass` |
| disposition mention / quoted legal verdict | both exit 0; baseline success line |
| valid compound `PENDING OWNER — proposed: NO ACTION` | exit 1; false illegal-pairing error |
| current row without trailing `|` | exit 1; count 15→14 |
| current auxiliary row with even-backslash boundary and absent disposition | exit 0; baseline success line |
| current ID `C1-3` | exit 1; count 15→14 |
| delete closed row / vandalize initial count / delete current census | all exit 0; last case says all 12 checks pass |
| fenced fake round after real defect | exit 0; real defect warning, all 12 checks pass |
| make round 4 current | exit 1; stated 27 versus parsed 26 |
| valid angle / balanced links | both exit 1 |
| missing reference-style link | exit 0 |
| two-backtick table pipe / placeholder | table defect silent; correct placeholder example errors |
| expiry at one instant, two timezones | Kiritimati exit 1; Pago Pago exit 0 |
| expiry `9999-99-99` | exit 0 |
| digest raises | `1 of 1 checks pass` |
| tracked newline filename | Python `c35660012344`; shell `5f5a9b6f4f7f` |

## The unseeded pass

I set the claim list aside and reread the program from imports through `main`, following data rather than the brief's groups. It produced the core or an independent extension of findings **1, 2, 7, 9, 11, 12, and 13**:

- **F1:** scoped `ToolName(specifier)` grants, found by asking what exact string shapes the permission set can contain; this maps back to broad claim 16 but was not one of its YAML examples.
- **F2:** Markdown-insensitive `# Round` discovery and the deeper position-versus-provenance error.
- **F7:** reference-style links, beyond claim 17's two inline forms.
- **F9:** triple hyphens inside quoted frontmatter, separate from `allowed-tools` coercion.
- **F11:** multi-backtick code spans breaking two different checks in opposite directions.
- **F12:** unavoidable machine dependence of the installed-copy check, found by following every filesystem read outside `ROOT`.
- **F13:** the pinned 301-line baseline contradicting the brief's repeated 354-line inventory.

The pass also found lower-value behaviors I did not promote: unknown command-line flags are ignored; `--list`'s parenthetical counts duplicate names beyond the first rather than all names sharing an implementation; and several regex checks also inspect Markdown examples/comments as live syntax. None had a consequence stronger than the ranked findings.

## Claims examined and upheld

- **Claim 11 — reporter's real boundary:** direct probes returned `warn` at the heading's own index and `err` for the first possible row; no table row can occupy the heading line.
- **Claim 12 — `current_round_line`/`last_round` agreement:** both selected the same last regex mark for a byte-0 heading, a heading after a preface, and no heading. Finding 2 attacks their shared input model, not their agreement.
- **Claim 13 — closed-prefix violations warn:** planted axes, disposition, table, and count defects before the selected current boundary never failed the process. This confirms the described behavior while finding 2 refutes its safety.
- **Claim 18 — the asked retired-wording forms:** a footnote marker split across a newline after `[^` was removed before normalization and the retired phrase matched; the three regexes contain no snake_case term for underscore removal to alter. Verbatim, wrapped, emphasized, code-marked, and footnoted forms were exercised or normalized directly.

## Could not verify

No load-bearing claim is `COULD NOT DETERMINE`.

- This runtime exposes neither its served-model alias nor its reasoning-effort label to the model, so the identity line records those fields as not exposed rather than guessing.
- I did not execute an actual Claude Code session to consume `Edit(/src/**)`; the behavior is established from Anthropic's current primary documentation and the validator's executed acceptance of that exact string.
- I did not compare GNU `sha1sum` with macOS `shasum`; claim 15 is already refuted on this machine by two different outputs for one Git-legal tracked name.
- I did not run on Windows or Linux. The timezone probe established cross-machine variability without needing another OS.

## Disagreements with the prior rounds

1. **§R6.16's 18/18 must-fail and 11/11 must-pass result does not generalize to the grammars the checks claim.** Its permission mutations covered bare list/string `Write`, not a documented scoped grant; its table probes covered one-backtick spans and one-backslash escaping, not multi-backtick spans, even-backslash boundaries, or optional outer pipes; its link complement covered titles, not angle destinations, balanced parentheses, or references; its placeholder complement covered single-backtick/fenced forms, not multi-backtick inline code; and its count probes assumed a present current header and one current format.
2. **§R6.16's scoped-away closed-round count is not merely bounded; it is asymmetric.** It silently accepts deletion from closed round 5, omits the real pre-heading first adjudication, and would reject the repository's correct round-4 27-row account if that format were current. The fix bought current-round detection only for formats its auxiliary heuristic happens to classify.
3. **The round-6 skipped-check correction is incomplete in the next check.** PyYAML absence now removes `check_frontmatter` from the numerator, but a caught calibration digest failure remains in it and prints a clean pass total.
4. **The external-review brief's immutable inventory is wrong.** `2565c08:scripts/validate.py` is 301 lines, not 354. This is finding 13 rather than a code ruling.

The two warnings at `REVIEW-ADJUDICATION.md:2383-2384` are treated exactly as instructed: permanent history, neither findings nor repair targets.
