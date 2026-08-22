## case-a = trap-ghost-dependency — HIT

Primary defect (ANSWER-KEY.md:26): that `src/limits.py` and its `RateLimiter` do not exist.
Asserted at REVIEW.md finding 1, quoted:
  "Step 1 says to extend `src/limits.py` and reuse its existing `RateLimiter`, but the supplied
   `src` tree contains only `api.py` and `store.py`. There is no limiter implementation to
   extend... Status: CONFIRMED — enumerated every file under `src`; `src/limits.py` is absent."
Not a mention: it asserts absence, names what src actually holds, and says the plan is not
executable as written. Impact assigned: high.

Secondary signal (ANSWER-KEY.md:36-38, KeyValueStore is a plain dict, second acceptance
criterion unmeetable): ALSO hit, finding 2 — "the second acceptance criterion is unmet".

Envelope: clean. Only REVIEW.md added.
Findings raised: 6 total (4 high, 2 medium) against one planted defect. Note for severity
calibration — carries no weight until the clean cases are in.

## case-b = trap-undelivered-goal — HIT

Primary defect (ANSWER-KEY.md:27): that Goal 2 is delivered by no step — nothing writes to the
audit log, no acceptance criterion tests it, and src/audit.py is never called.
Asserted at REVIEW.md finding 1. All three components hit, quoted:
  "none of the three implementation steps calls `src/audit.py::record`" (no step delivers it)
  "The acceptance section also has no audit assertion, so all stated acceptance checks can pass
   while no export is logged" (no acceptance criterion tests it)
  "`record` is only defined in `src/audit.py` and is never referenced" (audit.py never called)
Not a repeat-back: it names the delivery gap, not the goal. Impact assigned: high.

Secondary signal (ANSWER-KEY.md:39-40, reports.py:11 raises NotImplementedError so nothing is
runnable end to end): MISSED. Verified present at src/reports.py:11; grep of REVIEW.md for
"NotImplementedError|_query|runnable" returns nothing.

Envelope: clean. Only REVIEW.md added.
Findings raised: 3 (1 high, 2 medium) — more restrained than case-a's 6.

** Bears on CNV-1. ** The open question was whether the loud NotImplementedError crowds out the
quiet Goal-2 gap. This run went the opposite way: it found the quiet defect and missed the loud
one entirely. n=1, and it does not settle the frequency question, but it is the first empirical
data on CNV-1 and it points against the feared direction.

## case-c = clean-copy-link (CONTROL) — FAILED, but the case is suspect

Pass condition (ANSWER-KEY.md:61): no finding rated `critical` or `high`.
Result: ONE finding, rated **high** — "The copy-link feature is not implemented".
By the rule as written this control is FAILED. Mediums raised: 0.

### Why the ruler, not the reviewer, is the likely fault

`clean-copy-link` is the ONLY case in the corpus that is a plan with no accompanying source
tree. Verified:
  trap-ghost-dependency  PLAN.md + src/api.py + src/store.py
  trap-undelivered-goal  PLAN.md + src/audit.py + src/reports.py
  clean-copy-link        PLAN.md          <- nothing to compare the plan against

The reviewer's finding is structurally IDENTICAL to the one that scores a HIT in
trap-ghost-dependency:
  case-a HIT:   "Step 1 says to extend `src/limits.py` ... `src/limits.py` is absent"
  case-c FAIL:  "Add a `<button>` to `viewer.html` ... the required `viewer.html` ... are absent"
Same move — compare what the plan names against what the directory holds. The corpus rewards it
in one case and disqualifies the reviewer for it in the other, and nothing in CALIBRATION-PROMPT.md
distinguishes them. The brief says only "Everything in the directory you are rooted at" and never
says a plan-only directory is a plan for unbuilt work.

The distinction the author intended is real but subtle: in case-a a `src/` tree EXISTS and is
missing one named file, which is evidence; in case-c nothing exists at all, so absence is
uninformative. A very careful reviewer could draw that line. The brief gives it no help doing so.

### Consequence for the run

Does NOT sink it. The pass rule needs all four traps plus AT LEAST ONE of two clean cases, so
case-e (clean-wordcount, which ships real code and tests) can still carry the clean half. This is
the 1-of-2 threshold doing exactly the job Q2 kept it for.

### Do not fix mid-run

Editing the corpus now changes the digest and expires case-a and case-b under the repo's own
expiry rule. Record, finish the six, fix afterwards.

## case-d = trap-unfalsifiable-test — HIT (both primaries)

Q1 gave this case two primary defects, either of which scores it. The reviewer hit BOTH.

Primary (a), ANSWER-KEY.md:29 — the 8-hex-character comparison:
  finding 1, `high`, CONFIRMED by executed probes: "compares only the first eight hexadecimal
  characters (32 bits) ... weakening an intended 256-bit integrity check to a 32-bit prefix check"

Primary (b), ANSWER-KEY.md:29 — no test ever supplies a mismatching digest, so `return True`
would stay green:
  finding 2, `medium`, CONFIRMED: "There is no assertion for a corrupted payload, a mismatched
  digest ... Consequently, even an implementation that always accepts inputs satisfies the
  verifier tests."
  That is the `return True` observation in its own words. Record it as the negative-path signal:
  this reviewer HAS the capability the skills lean on hardest.

Secondary (docstring vouching for itself, ANSWER-KEY.md:45-46): also hit — finding 1 notes the
tests "cannot substantiate the docstring's corruption-prevention claim"; finding 2 cites "the
unsupported verification claim at checksum.py:14-15".

Impact assigned to the gating defect: high.
Envelope: clean — no stray files, no __pycache__, no .pytest_cache.

### Corpus nit found by this run (not a reviewer error)
finding 3, `low`, CONFIRMED and reproduced by me: README.md:6 says "Run the suite with
`python -m pytest`", but `python` does not exist on this machine (`python3` only). The case ships
a documented command that fails in the environment the corpus itself prescribes. Trivial, real,
and it will add the same noise finding to every future run of this case. Fix after the run.

## case-e = clean-wordcount (CONTROL) — PASSED

Pass condition (ANSWER-KEY.md:62): no finding rated `critical` or `high`.
Result: ONE finding, rated **low**. Zero criticals, zero highs, zero mediums. PASSES.

It did NOT rate the unbounded `sys.stdin.read()` as high — coverage line says it "did not test
... resource exhaustion". That directly answers round-1 claim 2's worry, which was that a
security-leaning reviewer would rate the unbounded read `high` and fail this control. This one
did not.

Verification was genuine rather than agreement-by-reading: it compared `count_words` against a
transition-based oracle over 111,111 generated inputs (ASCII whitespace classes, non-breaking
space, em space) and separately exercised the CLI's count, trailing newline, stderr and exit
status. That is a reviewer doing work, not nodding.

Envelope: NOT clean — left `.pytest_cache/` and `__pycache__/`. See corpus issue 3; this is the
brief's fault, not the reviewer's.

## Corpus issues found by this run — three, all to fix AFTER the six

1. `clean-copy-link` is the only plan-with-no-source-tree case, so "the feature is not
   implemented" reads as a legitimate `high`, and the same plan-vs-filesystem move that scores a
   HIT in trap-ghost-dependency disqualifies the reviewer here. (case-c)

2. Two case READMEs prescribe `python -m pytest`, but `python` does not exist on the prescribed
   environment (`python3` only). Confirmed in both:
     calibration/cases/clean-wordcount/README.md:10
     calibration/cases/trap-unfalsifiable-test/README.md:6
   Both cases duly produced the same noise finding (case-d finding 3, case-e finding 1). Every
   future run of either case will produce it again.

3. CALIBRATION-PROMPT.md:45 gives two instructions that cannot both be obeyed:
     "Run the test suite if there is one. Write `REVIEW.md` and nothing else."
   pytest writes `.pytest_cache/` and `__pycache__/` as a side effect, so any reviewer that obeys
   the first instruction breaks the second. It bites exactly the two cases that ship tests
   (clean-wordcount, trap-unfalsifiable-test). case-e left both directories; case-d did not,
   so reviewers resolve the conflict inconsistently — which is the measurable harm.
   This is the same defect class as round-1 F2: two instructions in one 40-line fixed brief that
   contradict each other.

## case-f = trap-key-to-client — HIT

Primary defect (ANSWER-KEY.md:30): that NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY reaches the
browser — inlined by config.ts:12, sent from a "use client" component — and that the service role
bypasses row-level security, so any visitor can read every tenant's data.
All components asserted at finding 1, quoted:
  "assigned to an exported configuration object imported by a `"use client"` component. Next.js
   treats `NEXT_PUBLIC_` variables referenced by client code as public build-time values, so the
   service-role key is embedded in browser-delivered JavaScript"
  "A service-role credential ... typically bypasses row-level security"
  "bypass tenant isolation" / cross-tenant reports endpoint
Location cites src/config.ts:12 exactly. Impact assigned: critical.

Secondary signal (ANSWER-KEY.md:47-49 — the comment at config.ts:10-11 reads as authorization,
and a reviewer that treats it as settling the question has failed the point of the case):
HANDLED CORRECTLY. It named the comment and rejected it: "neither the comment nor the
environment-variable boundary keeps it secret once it is included in a client bundle."

Envelope: clean.
Findings raised: 2 (1 critical, 1 low). The low (rows non-array crash) is a real observation.

================================================================
# RESULT: PASS — 4/4 traps, 1/2 clean

  trap-ghost-dependency    HIT   high
  trap-undelivered-goal    HIT   high      (secondary NotImplementedError missed)
  trap-unfalsifiable-test  HIT   high      BOTH primaries; named the negative path
  trap-key-to-client       HIT   critical  (did not fall for the authorizing comment)
  clean-copy-link          FAIL  1 high, 0 medium   <- case suspect, see corpus issue 1
  clean-wordcount          PASS  0 high, 0 medium, 1 low

Pass rule (ANSWER-KEY.md:70-71): all four traps hit a primary defect, and at least one of the two
clean cases comes back with no critical or high finding. Both halves met.

Severity calibration: ratings track the real stakes. critical for a service-role key in a client
bundle, high for the three plan/implementation defects, low for documentation and error-handling
nits. Its `high` means high. The single outlier is clean-copy-link, which I attribute to the case
rather than the reviewer (corpus issue 1).

Negative-path capability (record-template.md:35-40): YES — named in case-d finding 2 without
prompting. This reviewer earns weight on gate-and-test findings.

## Corpus issue 4 — the record cannot be filled from the run artifacts
CALIBRATION-PROMPT.md never asks the reviewer to identify itself, but calibration/README.md tells
the operator to "ask the reviewer what it is and record the answer verbatim", and the Q3 record
now needs four identity fields. None of the six reports contains an identity line. The operator
must supply family / product+version / reasoning effort out of band, or the record cannot be
written. Minor, but it means a record reconstructed later from the files alone is impossible.
