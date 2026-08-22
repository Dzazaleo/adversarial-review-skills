# Independent review

## Findings

### 1. High — the plan depends on a limiter module that does not exist

- **Location:** `PLAN.md:10-14`
- **Mechanism:** Step 1 says to extend `src/limits.py` and reuse its existing `RateLimiter`, but the supplied `src` tree contains only `api.py` and `store.py`. There is no limiter implementation to extend or bucket behavior to reuse.
- **Trigger:** An implementer follows Step 1 in this repository.
- **Consequence:** The plan is not executable as written. The implementer must invent a new limiter and its time/window/concurrency semantics, so the stated "reuse" and "same bucket logic" provide no real design guidance and the resulting behavior cannot be assessed against the plan.
- **Status:** `CONFIRMED` — enumerated every file under `src`; `src/limits.py` is absent.

### 2. High — the proposed persistence layer cannot survive a process restart

- **Location:** `PLAN.md:22-25`; `src/store.py:5-12`
- **Mechanism:** Step 3 proposes storing buckets in the "existing key-value table" so they survive a restart, but `KeyValueStore` is only an instance-owned Python dictionary. `api.py` constructs a fresh store at module import. There is no durable backing, reload path, or external shared state.
- **Trigger:** The API process restarts after a tenant has consumed any part of its request budget.
- **Consequence:** All counters are reset, so a tenant can exceed the intended cap across restarts and the second acceptance criterion is unmet.
- **Status:** `CONFIRMED` — inspected the complete store implementation and found no persistence mechanism.

### 3. High — token-bucket semantics do not enforce the stated per-minute cap

- **Location:** `PLAN.md:3-6,12-14,29`
- **Mechanism:** The goal says to cap a tenant at 100 requests per minute, but the selected token-bucket algorithm normally replenishes tokens continuously. With a capacity of 100 and a refill rate of 100 per 60 seconds, a tenant can spend 100 tokens, wait just under a minute, and spend roughly another 99; those requests still fall within one rolling 60-second interval. The single acceptance example only checks a burst of 101 and therefore does not distinguish token-bucket behavior from a strict fixed or rolling-window cap.
- **Trigger:** A tenant spaces requests so tokens refill during a rolling one-minute interval instead of sending all 101 as one burst.
- **Consequence:** The API can admit substantially more than 100 requests in a minute despite satisfying the listed acceptance example.
- **Status:** `THEORETICAL` — this follows for a conventional continuously refilled token bucket; the claimed existing implementation is missing, so its exact refill semantics cannot be checked.

### 4. High — the available store API cannot make counter updates atomic

- **Location:** `PLAN.md:18-25`; `src/store.py:8-12`
- **Mechanism:** Persisting a bucket requires a read/modify/write operation, while `KeyValueStore` exposes only independent `get` and `put` calls and no transaction, compare-and-swap, increment, or lock. Two request handlers can read the same available-token state, both accept, and then overwrite one another's update. Module-local locking would still not coordinate multiple processes.
- **Trigger:** Two or more requests for the same tenant are checked concurrently (or separate worker processes use the backing store envisioned by Step 3).
- **Consequence:** Requests above the cap can be accepted and consumed-budget updates can be lost.
- **Status:** `THEORETICAL` — no limiter implementation exists to exercise, but the only supplied persistence interface cannot perform an atomic bucket transition.

### 5. Medium — the fixed `Retry-After` value does not match the proposed limiter

- **Location:** `PLAN.md:18-20`
- **Mechanism:** The plan always returns `Retry-After: 60`. In the proposed continuously refilled token bucket, the next token would ordinarily become available after about 0.6 seconds; even under a fixed-window design, the correct delay is the time remaining in the current window, not always a fresh 60 seconds.
- **Trigger:** A conforming client receives a refusal at any point where capacity will become available in less than 60 seconds.
- **Consequence:** Clients that honor the header wait much longer than necessary, reducing usable throughput and making retries inconsistent with actual limiter state.
- **Status:** `THEORETICAL` — the header value is explicit, but the missing limiter prevents checking its exact next-admission time.

### 6. Medium — limiting before tenant validation permits unbounded bogus buckets

- **Location:** `PLAN.md:18-20`; `src/api.py:10-14`
- **Mechanism:** The plan calls `check(tenant_id)` at the top of `handle_request`, ahead of the existing empty-ID and tenant-record validation. If checking a new key creates the per-tenant bucket that Step 3 says to retain, arbitrary nonexistent tenant IDs each create persistent limiter state before returning `404`; even the empty ID can be rate-limited before the existing `401` check.
- **Trigger:** An unauthenticated caller submits many distinct fabricated tenant IDs, or repeatedly submits an empty ID.
- **Consequence:** The caller can grow limiter storage without bound and can change authentication/not-found responses into `429` responses. Validation needs to precede bucket creation, or bucket allocation and eviction need explicit safeguards.
- **Status:** `THEORETICAL` — this follows from the stated call order if `check` creates buckets, but the missing limiter implementation prevents direct execution.

## Coverage

Covered all files in the directory, including the complete plan and both source modules; checked the tree for limiter and test files and found neither. No test suite was available to run. Nothing in scope was left unread.
