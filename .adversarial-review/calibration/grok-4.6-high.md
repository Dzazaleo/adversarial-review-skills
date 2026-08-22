# Reviewer calibration record — grok-4.6 @ high effort

| | |
|---|---|
| **Model family** | xAI — Grok |
| **Product and version** | Grok 4.6, Grok Build TUI / Grok Code |
| **Reasoning effort** | high |
| **Reviewer self-report** | **Not captured in the calibration sessions.** Identity was established by the operator when asked, not read off any report, and not inferred. The nearest self-report on file is from a different session — this model's round-4 report at `EXTERNAL-REVIEW-4-GROK.md:2`: *"Reviewer identity: xAI Grok 4.6, Grok Build TUI / Grok Code product, high reasoning effort; served alias as given to this session: `Grok 4.6` (system prompt: 'You are Grok 4.6 released by xAI')."* It is consistent with what the operator gave, and it is **not** evidence about the six sessions scored here |
| **Run on** | 2026-08-22 |
| **Expires** | 2026-09-21 (run date + the default 30-day window) |
| **Corpus digest** | `775e1cc8c43f` |
| **Workload** | 6 cases, 17 files, 315 lines total (excluding the fixed brief). Per case: 40–63 lines across 2–3 files. Two cases were plans only; four shipped source. The six reports came back at 500 lines total |
| **Project** | `adversarial-review-skills` |
| **Result** | **PASS** |

## Traps

| Case | Primary defect reported | Impact it assigned | Notes |
|---|---|---|---|
| `trap-ghost-dependency` | yes | critical | Headline of finding 2: *"Planned reuse target `src/limits.py` / `RateLimiter` does not exist."* Asserts absence unambiguously and gives the runtime consequence — *"There is no `limits.py`. `import limits` raises `ModuleNotFoundError`. `api` has no `RateLimiter` symbol."* **Ranked it second**, behind "per-tenant cap is not implemented — 101st request is not 429", which is a defensible ordering and does not affect the score. Also caught the secondary: finding 3, counter persistence cannot survive a restart |
| `trap-undelivered-goal` | yes | high | Headline of finding 1: *"Goal 2 is delivered by no step — exports will not be audited."* All components present — Steps 1–3 named, `src/audit.py:6-18` `record` marked *"never called"*, `src/reports.py` marked *"no import of `audit`"*, and the acceptance criteria checked and found not to test it. **Secondary caught in full** — finding 2, *"Query layer always raises — nothing in the plan is runnable end to end"*, which is the `_query` `NotImplementedError` |
| `trap-unfalsifiable-test` | yes — **both** primaries | critical (truncation) / high (untestable path) | (a) *"Integrity check compares only the first 8 hex characters — SHA-256 is reduced to 32 bits"*, with the ~2³² forgery cost named against 2²⁵⁶, and the defending comment at `checksum.py:18-19` explicitly rejected rather than quoted approvingly. (b) *"No test ever supplies a mismatching digest — `verify_checksum` can return True unconditionally."* Both, and the second **proven by mutation** |
| `trap-key-to-client` | yes | critical | *"Supabase service-role key is shipped to the browser and sent on a client-side request."* Traces both hops — build-time inlining of `NEXT_PUBLIC_*` at `config.ts:12` into a `"use client"` module, then the value on an `apikey` header from the user's browser. **Did not fall for the authorizing comment** — names `config.ts:10-11` and treats it as the design's own claim rather than as settling the question. Honest about what it could not do: no build, so no `.next` chunk dumped to quote the inlined string |

**Which signal hit in `trap-unfalsifiable-test`** — **both**, and the untestable path was proven,
not asserted: the report carries a mutation table showing `return True` → *3 pass*, run as
`python3 -m pytest -v --cache-clear test_checksum.py`. That is the strongest available form of this
finding and the capability these skills lean on hardest.

## Clean cases

| Case | `critical`/`high` raised | Mediums raised | Notes |
|---|---|---|---|
| `clean-copy-link` | 0 | 0 | **Passed with zero findings of any severity.** *"None. Ranked list is empty."* Earns it with an unusually explicit discard list: the broader-than-accurate secure-context sentence at `PLAN.md:19-20`, the dual-failure path with no URL displayed, the hardcoded `Ctrl+C` on macOS, rapid re-click during the two-second window, missing `aria-live`, and deprecated `execCommand` — each named, reasoned about, and argued out rather than filed |
| `clean-wordcount` | 0 | 0 | **Passed with zero findings of any severity**, and verified rather than agreed. Ran the suite against **eight stand-in implementations** — `len(text.split(" "))`, `len(text.splitlines())`, always-`0`, always-`3`, `len(text)`, `text.count(" ")`, and others — recording which tests each one fails, to establish that the empty, whitespace-only and mixed-whitespace tests are real constraints rather than tautologies |

Zero mediums across both clean cases is a strong result and is worth reading with care in both
directions: it says this reviewer does not manufacture severity, and it also means nothing here
measures how it labels a genuine medium. Its four trap ratings — three `critical`, one `high`,
plus a `high` and a `low` on secondaries — are the only severity evidence on file.

## Verdict

**PASS.** All four traps hit a primary defect — one of them both primaries — and both clean cases
came back with no `critical` or `high` finding. The pass rule requires four of four and at least
one of two; this run cleared it on every case.

Mutation appeared on two cases rather than one: on `trap-unfalsifiable-test` to prove the suite
cannot distinguish the implementation from `return True`, and on `clean-wordcount` to prove the
opposite about a correct suite. A reviewer that reaches for the same technique to convict and to
acquit is doing the thing this corpus is trying to detect.

## The caveat this record must carry

**This model had previously read `calibration/ANSWER-KEY.md`.** On 2026-08-22, before these six
runs, a Grok session was rooted at the whole repository while answering `CALIBRATION-PROMPT.md`,
and it read the answer key — which names every planted defect in all six cases and where to look
for each. It disclosed this in full, unprompted, when asked what it had opened. That run is void
and is filed at `EXTERNAL-REVIEW-5-GROK-VOID.md`.

The six runs scored here were each rooted in an isolated single-case directory containing only that
case and the fixed brief, with no answer key and no sibling cases present — verified before the runs
and again after. A fresh session does not carry the earlier one's context, and the corpus tests
capability rather than recall.

**But this record is weaker than one earned with no prior exposure, and it should be read that
way.** Nothing here can establish that the earlier session left no trace. The honest remedy is a
private replacement corpus, which `BACKLOG.md` `B-1` already contemplates; until one exists, treat
this PASS as sound for detection capability and discount it where the question is whether the
reviewer could have been primed.

## What a pass does and does not establish

It establishes that this reviewer, at this effort, on work of roughly this size — 40–63 lines
across 2–3 files per case — detects planted defects it was not told about, and does not invent
severity on correct work. **That is what makes its silence mean something**, within that size.

It does not establish anything about a 5,000-line unscoped audit, about a domain this corpus does
not cover, or about the same model at a different reasoning effort. The record is keyed on effort
for that reason: `grok-4.6` at low effort is a different reviewer and has no record.
