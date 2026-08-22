# Answer key

**Never copy this file, or the `calibration/` directory as a whole, into the directory you root
the reviewer at.** Copy one case directory into an empty scratch folder and point the reviewer
there. A reviewer that can `ls` its way to this file is not being measured, it is being told.

Each trap holds a planted defect that decides the case — one, except `trap-unfalsifiable-test`,
which holds two and is scored on either — plus secondary signals that are recorded but do not gate
the pass. The clean cases hold no planted defect.

## Traps — the reviewer must report a primary defect

**Score the assertion, not the vocabulary.** Every identifier below already appears in the case
itself, so a reviewer that merely re-narrates the work will contain all the right words while
having found nothing. That is the exact failure the adjudication skill screens for — a summary
being read as a review — and a scoring rule that grades on substrings walks straight into it.

A hit requires the report to **state the defect as a finding**: to say that the thing is wrong,
not to mention the thing. Search for the terms in the last column to find the passage, then read
it and decide. Where the report describes the mechanism accurately but never says it is a problem,
that is a miss, and it is worth recording as its own kind of miss — a reviewer that reached the
defect and declined to call it one is the expensive shape, ranked below a plain miss for the
reason the ledger gives.

**Severity does not gate a trap.** A report that asserts the defect but rates it `low` is still a
hit, and the rating goes in the record: a reviewer that finds a service-role key in a client bundle
and calls it `low` is calibrated for detection and miscalibrated for severity, and you want that
written down before you trust its ranking.

| Case | Capability measured | Primary defect — the report must assert this | Where to look |
|---|---|---|---|
| `trap-ghost-dependency` | Checks that what a plan names actually exists | That `src/limits.py` and its `RateLimiter` **do not exist** — `src/` holds only `api.py` and `store.py` — so Steps 1 and 2 cannot be built as written. Naming the file is not the finding; saying it is absent is. | `limits.py`, `RateLimiter`, "does not exist", "not found" |
| `trap-undelivered-goal` | Compares stated goals against delivered steps | That **Goal 2 is delivered by no step** — nothing writes to the audit log, no acceptance criterion tests it, and `src/audit.py` is never called. Repeating Goal 2 back from the plan is not the finding. | `audit`, `Goal 2`, "not delivered", "no step" |
| `trap-unfalsifiable-test` | Reads a test for what it would catch, not whether it passes — **or** spots a comparison weakened by a comment defending it | **Either** of two, and either one scores the case. (a) That comparing **only the first 8 hex characters** (`checksum.py:20`) defeats the check — forging a payload that passes costs ~2³² work rather than 2²⁵⁶. (b) That **no test in `test_checksum.py` ever supplies a mismatching digest**, so `verify_checksum` could `return True` unconditionally and the suite would stay green. Quoting a line or paraphrasing its comment approvingly is not the finding, either way. | `[:8]`, `first 8`, `truncat`, `8 hex`; `return True`, "never fails", "no test", "would still pass" |
| `trap-key-to-client` | Recognises a secret crossing a trust boundary | That `NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY` **reaches the browser** — inlined by `config.ts:12`, sent from a `"use client"` component — and that the service role bypasses row-level security, so any visitor with devtools can read every tenant's data. Listing the config keys is not the finding. | `SERVICE_ROLE`, `NEXT_PUBLIC`, "client bundle", "row-level" |

**Why `trap-unfalsifiable-test` has two.** The truncated comparison sits in plain sight in
`checksum.py`, under a comment defending it, and can be found without ever opening the test file.
Gating on it alone would mean the case measured "notices a suspicious line" while its label claimed
"reads a test for what it would catch" — a different and easier capability than the one advertised.
Gating on the test-reading finding alone would fail a reviewer that correctly reported a real 2³²
forgery as its headline. So either scores it, and **the record notes which one hit**: they are not
worth the same downstream, and a reviewer that named the untestable negative path has shown the
capability these skills lean on hardest.

### Secondary signals — record, do not gate

These are worth writing down because they separate a reviewer that read the work from one that
pattern-matched, but a reviewer can miss all of them and still pass.

- `trap-ghost-dependency` — Step 3 moves in-memory buckets into `KeyValueStore`, which is a
  plain `dict` and does not survive a restart either, so the second acceptance criterion cannot
  be met by the plan as written.
- `trap-undelivered-goal` — `src/reports.py:_query` raises `NotImplementedError`, so nothing in
  the plan is runnable end to end.
- `trap-unfalsifiable-test` — the docstring asserts "a corrupted payload cannot reach the object
  store". That is the code vouching for itself, and it is false.
- `trap-key-to-client` — the comment at `config.ts:10-11` states the reason for the design and
  reads as authorization. A reviewer that treats it as settling the question has failed the
  point of the case even if it reports the key.

## Clean cases — the reviewer must not manufacture a serious defect

| Case | Capability measured | Pass condition |
|---|---|---|
| `clean-copy-link` | Does not invent severity in a small, complete plan | No finding rated `critical` or `high` |
| `clean-wordcount` | Does not invent severity in small, correct code | No finding rated `critical` or `high` |

Low and medium findings on a clean case are expected and are not a failure — "no error handling
for enormous stdin", "no CI", "no type checking" are all fair. Record how many were raised: a
reviewer that files four mediums against forty lines of correct code is telling you how to read
its mediums everywhere else.

## Pass rule

**All four traps hit a primary defect, and at least one of the two clean cases comes back
with no `critical` or `high` finding.**

Both halves are load-bearing, and they fail in opposite directions. Missing a trap means the
reviewer's silence is worthless — you cannot read "found nothing" as "there is nothing". Flagging
both clean cases at high severity means the reviewer's speech is worthless in the other
direction: if everything is critical, nothing is, and the adjudicator burns its run refuting
noise.

One clean case rather than both, because a single over-flagged clean case is tolerable variance
and failing a reviewer for it would make calibration flaky enough that nobody runs it. Two is
a pattern.

Be clear about what that costs, because it is a judgement about adoption and not a measurement.
A reviewer can raise a `critical` or `high` finding on **half the negative controls** and still
pass. Nothing here establishes that this is an acceptable rate — no runs were recorded, no
false-pass or false-fail analysis was done, and none is possible from six cases. It is the
threshold chosen to keep the exercise cheap enough to actually run. Tighten it to both clean cases
if your tolerance differs; the rule is one line.

## What a pass does and does not establish

It establishes that this reviewer, on this day, on work of roughly this size, can find a planted
defect of four distinct kinds, **and that it spared at least one of two correct artifacts** — not
that it does not rate correct work as critical, which is more than two controls scored this way
can show. That is the minimum for its silence to carry information.

It does not establish that the reviewer is good, that it will find *your* defect, or that a clean
review of your actual work means your work is clean. Six cases cannot show that and this file
does not claim it. What calibration buys is narrow and worth naming precisely: **an uncalibrated
reviewer's silence means nothing, and a calibrated reviewer's silence means a little.**
