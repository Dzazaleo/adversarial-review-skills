# Reviewer calibration record — gpt-5.6-sol @ high effort

| | |
|---|---|
| **Model family** | OpenAI — self-reported as "GPT-5.6, Sol variant" |
| **Product and version** | Codex IDE extension 26.818.31338 in Cursor, using embedded codex-cli 0.149.0-alpha.4 |
| **Reasoning effort** | high |
| **Reviewer self-report** | Verbatim, asked in the first session after it wrote its report: "1. Model family: GPT-5.6, Sol variant. 2. Product/version: Codex IDE extension 26.818.31338 in Cursor, using embedded codex-cli 0.149.0-alpha.4. 3. Reasoning effort: high. 4. Served model alias, verbatim: `gpt-5.6-sol`. These values come from this session's metadata, not inferred defaults." |
| **Run on** | 2026-08-22 |
| **Expires** | 2026-09-21 (run date + the default 30-day window) |
| **Corpus digest** | `775e1cc8c43f` |
| **Workload** | 6 cases, 17 files, 315 lines total (excluding the fixed brief). Per case: 40–63 lines across 2–3 files. Two cases were plans only; four shipped source. The six reports came back at 157 lines total |
| **Project** | `adversarial-review-skills` |
| **Result** | **PASS** |

## Traps

| Case | Primary defect reported | Impact it assigned | Notes |
|---|---|---|---|
| `trap-ghost-dependency` | yes | high | "The `src/limits.py` implementation that the plan says to reuse is also absent from the reviewed directory." Asserts absence, which is what the key gates on. **Weaker in form than the rest of this run:** the absence sits inside the *mechanism* of a broader finding headlined "the public request path does not enforce any request limit", and the report never says outright that Steps 1–2 cannot be built as written. Scored a hit because the key's discriminator — naming the file is not the finding, saying it is absent is — is met unambiguously and tied to the plan's reuse instruction. Also caught the secondary (`KeyValueStore` is a plain dict; the restart-persistence criterion cannot be met) |
| `trap-undelivered-goal` | yes | high | Headline: "The plan never implements or accepts the required audit event." All three components: "None of the three implementation steps calls that entry point or otherwise records an export, and neither acceptance criterion checks the audit log"; "auditing exists only as an uncalled generic helper." **Secondary only partially caught** — `reports.py:_query` raising `NotImplementedError` appears as a *verification limitation* ("the production warehouse implementation needed to exercise it is not present"), never named or raised as a finding |
| `trap-unfalsifiable-test` | yes — **both** primaries | high (truncation) / medium (untestable path) | (a) "compares only `actual[:8]` with `expected[:8]`, reducing SHA-256 verification from 256 bits to a 32-bit prefix", with the 2³² forgery cost named. (b) "There is no mismatched-payload/digest assertion… the suite cannot distinguish the implementation from an always-`True` verifier plus a constant, non-SHA-256 checksum function." Also rejected the self-vouching docstring |
| `trap-key-to-client` | yes | critical | "The service-role key is read from a `NEXT_PUBLIC_...` environment variable, imported by a `"use client"` module, and used in a browser-side request… **A Supabase service-role key bypasses row-level security**"; consequence names cross-tenant exposure; cites `config.ts:12` and `page.tsx:12-14`. **Did not fall for the authorizing comment** — "neither the comment nor the TypeScript non-null assertion provides a security boundary" |

**Which signal hit in `trap-unfalsifiable-test`** — **both**, and the untestable negative path was
not merely asserted but **proven by mutation**: "I rebound the two imported functions in memory to
an always-`True` verifier and a constant `"not-sha256"` checksum, then invoked all three test
functions; every test passed." That is the strongest available form of this finding. This reviewer
has demonstrated the capability these skills lean on hardest and earns weight on gate-and-test
findings.

## Clean cases

| Case | `critical`/`high` raised | Mediums raised | Notes |
|---|---|---|---|
| `clean-copy-link` | 0 | 1 | **Passed.** One `medium` (the `execCommand` fallback's "temporary" input — the plan never says whether it is visible or when it is removed, and the usual immediate cleanup destroys the selection the third acceptance criterion needs; it also spots that retaining the field contradicts the plan's own "the label is the only state the feature keeps") and one `low` (no in-flight guard or timer cancellation across repeated clicks). Both legitimate underspecification, both labelled `THEORETICAL` with what would settle them |
| `clean-wordcount` | 0 | 0 | **Passed with zero findings of any severity** — "No defects worth reporting were found", with the coverage line the brief requires. Verified rather than agreed: built an independent token-transition oracle and compared against `count_words` across 137,257 exhaustive inputs of length 0–6 over an alphabet including tab, newline, non-breaking space, em space and NUL; exercised the CLI as a subprocess for exit status, exact stdout and empty stderr; named what it did not reach (malformed-stdin decoding) and argued it out of contract |

## Verdict

**PASS — 4/4 traps, 2/2 clean.** Both halves of the pass rule met, and the clean half was met
outright rather than on the one-of-two allowance (`calibration/ANSWER-KEY.md:70-71`).

**Severity calibration:** its ratings track the real stakes. `critical` for a service-role key
reaching a browser bundle, `high` for the three plan and implementation defects, `medium`/`low` for
the rest. Its `high` means high — no discount needed when reading its ranking. One judgement worth
knowing: it rated the untestable negative path `medium` while rating the truncated comparison it
sits underneath `high`. That is defensible — the truncation is the live vulnerability and the test
gap is what let it survive — but a reader who ranks by severity alone will see this reviewer's
test-coverage findings a notch below its vulnerability findings.

**Evidence discipline — the strongest signal in this run.** The six cases produced 12 findings:
7 `CONFIRMED`, 5 `THEORETICAL`. Five of the 12 are confirmed by **executed probes** rather than
inspection: 101 calls through `handle_request`; a two-process write/read proving `KeyValueStore` is
not durable; a `chdir` proving `audit.log` resolves against the working directory; an altered
full-length digest still returning `True`; and the mutation test above. The other two `CONFIRMED`
findings rest on inspection alone, correctly — that no plan step calls the audit entry point, and
that Next.js inlines `NEXT_PUBLIC_` values into the bundle, are both settled by reading rather than
running, and it said so ("No running deployment is needed to establish that the configured value is
shipped to the browser"). Where it could not settle a question either way it said `THEORETICAL` and
named what would settle it. Nothing was labelled `CONFIRMED` on evidence it did not have.

**Discrimination, not posture.** It applied the brief's evidence rule — would this test fail if the
thing it proves were false? — to both `trap-unfalsifiable-test` and `clean-wordcount`, and reached
opposite, correct conclusions: "the suite cannot distinguish the implementation from an always-`True`
verifier" against "each assertion directly checks the claimed result; the tests are narrow but not
falsely evidentiary." A reviewer running a fixed sceptical posture fires on both. This one did not.

**Envelope compliance:** clean in all six. Every pre-existing file was verified byte-identical
against `calibration/cases/` after the runs. Nothing was written but `REVIEW.md`, plus
`.pytest_cache/` and `__pycache__/` in the one case with a suite — leavings the fixed brief
explicitly permits. The `case-b` session called `audit.record` in a temporary directory and removed
it afterwards rather than leaving `audit.log` behind.

**Standing caveat:** a pass means this reviewer's silence carries some information on work of
roughly this size and kind — the **Workload** row above says what that size actually was, in
numbers, so a later reader can compare it with the work being adjudicated rather than guess at
"roughly". It is not evidence that a clean review of your actual work means your work is clean.
See `calibration/ANSWER-KEY.md`.

## Relationship to the previous record

This supersedes the record of the same name pinning digest `573e270c698b`, archived with its raw
reports under `runs/2026-08-22-gpt-5.6-sol-high/`. That record was already **stale, not overwritten
while live**: the corpus moved to `775e1cc8c43f` after repairs, and under
`calibration/README.md` a differing digest expires a record and stale is treated exactly as missing.

The previous run scored **4/4 traps, 1/2 clean**, failing `clean-copy-link` with one `high` —
"the copy-link feature is not implemented"; `viewer.html` absent. Its scorer attributed that failure
to the case rather than the reviewer, noting the case was the only plan in the corpus shipping no
source tree, and predicted: *"If that case is repaired, this reviewer would plausibly have scored
2/2 clean."* The case was repaired by adding the `viewer.html` its plan extends. **This run returned
2/2 clean, and the same reviewer raised no `critical` or `high` on that case.** The prediction held.

Read that as a modest, real result and not more: one confirmed prediction on one repaired case,
scored by the same author as the fix. It is consistent with the failure having been the ruler's, not
the reviewer's. It does not independently establish it.

## Scorer's caveats — read before relying on this record

1. **The scorer wrote the answer key.** This record was scored by the same model family that
   authored the corpus — the unmeasured-reliability problem recorded as CNV-3 in
   `REVIEW-ADJUDICATION.md`. Every trap hit above quotes the exact sentence counted as the hit, so
   the calls can be checked rather than taken. The `trap-ghost-dependency` call is the one most
   worth a second opinion: it is the only hit in this run whose defect assertion is not the
   finding's headline.

2. **This reviewer has read the answer key in other sessions.** It audited this repository in
   rounds 1 and 2, where `calibration/ANSWER-KEY.md` was in scope, and its round-1 report cites the
   key six times. These six runs were fresh sessions rooted at `/tmp/calibration/case-*`, outside
   the repository, with no answer key present — verified before the runs. So they are *probably*
   uncontaminated, but that rests on Codex sessions being stateless, which has not been confirmed.
   Treat this record as weaker than one earned by a model that has never seen the repo.

3. **The identity fields were not independently verified by the scorer.** The reviewer asserted
   that its model, product version and effort "come from this session's metadata, not inferred
   defaults". Under this project's own evidence rule that is a claim by the party under review, not
   proof, and the scorer had no access to the session to check it. The operator relayed it from the
   first session before closing it, as the protocol requires.

4. **The cases were blinded to the scorer at run time only in labelling, not in content.** Cases
   were presented as `case-a` … `case-f` and mapped back to their real names by content hash after
   the reports landed. The scorer had read the answer key before scoring, which the protocol
   intends — the key is the ruler — but it means these are not blind gradings.
