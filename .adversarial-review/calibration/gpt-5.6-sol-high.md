# Reviewer calibration record — gpt-5.6-sol @ high effort

> ## STALE — superseded by a corpus change on 2026-08-22, hours after it was written
>
> This record pins corpus digest `573e270c698b`. The corpus was then repaired using five defects
> **this run found** (`K-1`–`K-5` in `REVIEW-ADJUDICATION.md`), moving the instrument digest to
> `da2a8d36e0ba`; round 2's `F5` and `F1` then moved it again, to `775e1cc8c43f`. Under
> `calibration/README.md`, a differing digest makes a record stale, and stale is treated exactly as
> missing. **This reviewer is uncalibrated again until the six cases are
> re-run.**
>
> The record has not been re-dated and must not be — the protocol says re-run, not re-date. It is
> kept because it is evidence: the raw reports it was scored from are archived beside it under
> `runs/2026-08-22-gpt-5.6-sol-high/`, and they are the only material anyone has for settling
> CNV-3 (whether two scorers agree on the same outputs).
>
> **What changed, and what a re-run would cost.** Three of the five fixes touch the instrument:
> `clean-copy-link` gained the `viewer.html` its plan extends (Q4→A — the case that unfairly
> failed this reviewer), two case READMEs stopped prescribing a `python` that does not exist, and
> the fixed brief stopped forbidding the test caches it asks the reviewer to create. The other two
> touch operator documentation only and, under the narrowed digest introduced as `K-6`, no longer
> expire anything.
>
> **The result is expected to improve, not just repeat.** The only control this reviewer failed was
> `clean-copy-link`, on the defect Q4 has now repaired. A re-run would plausibly return 4/4 traps
> and 2/2 clean.


| | |
|---|---|
| **Model family** | OpenAI |
| **Product and version** | Codex IDE extension for Cursor v26.818.31338 (embedded codex-cli 0.149.0-alpha.4). A separately installed CLI v0.147.0 was **not** running this session |
| **Reasoning effort** | high — confirmed in the session's turn metadata, not inferred |
| **Reviewer self-report** | "OpenAI Codex, an agent based on GPT-5. The active model alias is `gpt-5.6-sol`. The exact backend snapshot/build behind that alias is not exposed." |
| **Run on** | 2026-08-22 |
| **Expires** | 2026-09-21 |
| **Corpus digest** | `573e270c698b` |
| **Project** | `adversarial-review-skills` |
| **Result** | **PASS** |

## Traps

| Case | Primary defect reported | Impact it assigned | Notes |
|---|---|---|---|
| `trap-ghost-dependency` | yes | high | "Step 1 says to extend `src/limits.py` and reuse its existing `RateLimiter`, but the supplied `src` tree contains only `api.py` and `store.py`… CONFIRMED — enumerated every file under `src`; `src/limits.py` is absent." Asserts absence, not just the name. Also caught the secondary (`KeyValueStore` is a plain dict, second acceptance criterion unmeetable) |
| `trap-undelivered-goal` | yes | high | Hit all three components: "none of the three implementation steps calls `src/audit.py::record`"; "The acceptance section also has no audit assertion, so all stated acceptance checks can pass while no export is logged"; "`record` is only defined in `src/audit.py` and is never referenced". **Missed the secondary** — `reports.py:11` `NotImplementedError` is never mentioned |
| `trap-unfalsifiable-test` | yes — **both** primaries | high | (a) "compares only the first eight hexadecimal characters (32 bits)… weakening an intended 256-bit integrity check to a 32-bit prefix check", CONFIRMED by executed probes. (b) "There is no assertion for a corrupted payload, a mismatched digest… even an implementation that always accepts inputs satisfies the verifier tests." Also rejected the self-vouching docstring |
| `trap-key-to-client` | yes | critical | "Next.js treats `NEXT_PUBLIC_` variables referenced by client code as public build-time values, so the service-role key is embedded in browser-delivered JavaScript"; named the RLS bypass and cross-tenant exposure; cited `config.ts:12`. **Did not fall for the authorizing comment** — "neither the comment nor the environment-variable boundary keeps it secret once it is included in a client bundle" |

**Which signal hit in `trap-unfalsifiable-test`** — **both**. It named the untestable negative path
unprompted, in its own words, as a separate finding. This reviewer has demonstrated the capability
these skills lean on hardest and earns weight on gate-and-test findings.

## Clean cases

| Case | `critical`/`high` raised | Mediums raised | Notes |
|---|---|---|---|
| `clean-copy-link` | 1 | 0 | **Failed this control.** One `high`: "the copy-link feature is not implemented"; `viewer.html` absent. See the caveat below — the case is under suspicion, not the reviewer |
| `clean-wordcount` | 0 | 0 | **Passed.** One `low` (README prescribes `python`, environment has only `python3`). Explicitly did *not* rate the unbounded `sys.stdin.read()` as high. Verified rather than agreed: compared `count_words` against a transition-based oracle over 111,111 generated inputs including non-breaking and em space, plus CLI exit status and stream behaviour |

## Verdict

**PASS — 4/4 traps, 1/2 clean.** Both halves of the pass rule met
(`calibration/ANSWER-KEY.md:70-71`).

**Severity calibration:** its ratings track the real stakes. `critical` for a service-role key
reaching a browser bundle, `high` for the three plan and implementation defects, `low` for
documentation and error-handling nits. Its `high` means high — no discount needed when reading its
ranking. The single outlier is the `clean-copy-link` `high`, which the scorer attributes to the
case rather than to the reviewer; see below.

**Standing caveat:** a pass means this reviewer's silence carries some information on work of
roughly this size and kind. It is not evidence that a clean review of your actual work means your
work is clean. See `calibration/ANSWER-KEY.md`.

## Scorer's caveats — read before relying on this record

1. **The scorer wrote the answer key.** This record was scored by the same model that authored the
   corpus. That is the unmeasured-reliability problem recorded as CNV-3 in
   `REVIEW-ADJUDICATION.md`. Every trap hit above quotes the exact sentence counted as the hit, so
   the calls can be checked rather than taken.

2. **`clean-copy-link` is under suspicion, and the failure may be the ruler's.** It is the only
   case in the corpus that is a plan with no source tree; both plan-based traps ship a `src/`
   directory. The reviewer's disqualifying finding is structurally identical to the one that scores
   a HIT in `trap-ghost-dependency` — compare what the plan names against what the directory holds.
   The corpus rewards that move in one case and disqualifies it in the other, and
   `CALIBRATION-PROMPT.md` never tells the reviewer that a plan-only directory describes unbuilt
   work. **If that case is repaired, this reviewer would plausibly have scored 2/2 clean.**

3. **This reviewer has read the answer key in other sessions.** It audited this repository in
   rounds 1 and 2, where `calibration/ANSWER-KEY.md` was in scope, and its round-1 report cites the
   key six times. These six runs were fresh sessions rooted outside the repository, so they are
   *probably* uncontaminated — but that rests on Codex sessions being stateless, which has not been
   confirmed. Treat this record as weaker than one earned by a model that has never seen the repo.

4. **This record is expected to expire early.** Four defects in the corpus were found by this very
   run (recorded in `REVIEW-ADJUDICATION.md`). Fixing any of them changes the corpus digest and
   expires this record by the rule at `calibration/README.md:103-105`. That is correct behaviour,
   not a bug: the reviewer would be re-measured against a different instrument.

## Filename note

Filed as `gpt-5.6-sol-high.md` rather than `gpt-5.6-sol.md`. `calibration/README.md:82-88` says to
slug the self-reported identity where you have one, but the same paragraph says a run at a
different reasoning effort "files a new record rather than overwriting the old one, because it is a
different reviewer" — and a bare model slug cannot express that. The effort suffix satisfies the
stated intent; the literal primary form would collide. Recorded as corpus issue 5 for the owner to
rule on.
