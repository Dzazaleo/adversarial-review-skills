# Independent review — per-tenant request throttling plan

The work under review is `PLAN.md` plus the existing code it claims to extend (`src/api.py`, `src/store.py`). There is no test suite, no prior review, and no `src/limits.py`.

Claims in comments, docstrings, and the plan are treated as assertions to falsify. Current request-path behaviour was executed, not inferred.

---

## Findings (ranked)

### 1. Plan Step 1 reuses `src/limits.py` / `RateLimiter`, which do not exist

- **Impact:** critical
- **Location:** `PLAN.md:12–14`, `PLAN.md:18–19`; `src/` contains only `api.py` and `store.py`
- **Mechanism:** Step 1 is “reuse the existing limiter”: it states that `src/limits.py` already implements a token-bucket `RateLimiter` for an internal admin API, and that adding `per_tenant=True` is enough. Step 2 then constructs `RateLimiter(per_tenant=True, rate=100, window=60)` at module scope in `src/api.py` and calls `.check(tenant_id)`. Neither the module, the class, the admin API, nor any import of them exists. `src/api.py` imports only `KeyValueStore`. A directory listing of `src/` is `api.py` and `store.py`.
- **Trigger:** An implementer follows the plan as written (`from limits import RateLimiter`, or opening `src/limits.py` to add the flag).
- **Consequence:** Step 1 cannot be performed. The constructor, `per_tenant` flag, `.check` contract, token-bucket parameters, and refill/burst behaviour are unspecified except by reference to a file that is not there. The rest of the plan (wiring, 429, persistence) has nothing to attach to. Anyone executing the plan must invent the limiter from scratch; the plan gives no algorithm, capacity vs. refill split, or storage interface for that invention, while claiming “no new dependency.”
- **Status:** CONFIRMED. `ls src/` shows two files. `python3` with `sys.path` including `src` raised `ModuleNotFoundError: No module named 'limits'` for both `import limits` and `from limits import RateLimiter`. `grep` over the directory finds `RateLimiter` / `limits.py` only in `PLAN.md`.

### 2. Step 3 cannot make the cap survive a restart: the “existing key-value table” is an in-memory dict, and the Step 2 constructor never receives it

- **Impact:** high
- **Location:** `PLAN.md:22–26`, `PLAN.md:30`; `src/store.py:1–12`; `PLAN.md:18`; `src/api.py:3–5`
- **Mechanism:** Two independent holes, either of which falsifies acceptance bullet 2 (“Restarting the process does not reset a tenant's consumed budget”).
  1. `KeyValueStore` is documented and implemented as a process-local `dict[str, bytes]`. The public surface is `get` / `put` only. There is no file, socket, database, `atexit` hook, or load path. A value written in one interpreter is gone in the next.
  2. The only construction the plan specifies is `RateLimiter(per_tenant=True, rate=100, window=60)` at module scope. No store is passed in. `src/api.py` already holds a module-level `store = KeyValueStore()`, but Step 2 does not mention it. Even if `limits.py` existed, following the written constructor leaves buckets inside the limiter.
- **Trigger:** Follow Step 3 (put counters in `KeyValueStore`) and then restart the process, as the acceptance line requires. Or follow Step 2’s constructor literally and never persist at all.
- **Consequence:** After any restart, deploy, or crash, every tenant’s consumed budget is zero. The 100 req/min cap is enforceable only within a single process lifetime. A tenant (or a burst of tenants) can exceed the published cap by the length of downtime; operators who bounce the service reset the throttle for everyone. The plan presents this as already solved by “the existing key-value table.”
- **Status:** CONFIRMED.
  - `KeyValueStore.put('bucket:acme', b'99')` then `get` in the same process returned `b'99'`; a fresh process’s `get('bucket:acme')` returned `None` and `list(s._data.keys())` was `[]`.
  - `dir` on the live store is `['get', 'put']`.
  - Source of `__init__` is `self._data: dict[str, bytes] = {}` (`src/store.py:5–6`).

### 3. Token-bucket reuse contradicts the 101st-request acceptance line

- **Impact:** medium
- **Location:** `PLAN.md:12` (“token-bucket `RateLimiter`”); `PLAN.md:18` (`rate=100, window=60`); `PLAN.md:29` (“101 requests inside one minute receives `429` on the 101st”)
- **Mechanism:** A token bucket that holds 100 tokens and refills 100 per 60s admits a burst of 100 and then further requests as tokens accrue. At one token per 0.6s, request 101 inside the same minute is allowed. The acceptance line is a fixed-window (or full-window sliding) test: 101 calls in 60s, last one is `429`. Those two descriptions do not name the same limiter. Because `src/limits.py` is missing (finding 1), there is no implementation to measure; the contradiction is in the plan’s own words.
- **Trigger:** An implementer who, after discovering the ghost module, faithfully builds a token bucket with `rate=100, window=60` and then runs the acceptance check.
- **Consequence:** The 101st request in a minute returns `200`. The published cap is not the cap the first acceptance bullet describes. A fixed-window implementation would pass that bullet and violate the “reuse the token-bucket” instruction; a token bucket would do the reverse. The plan gives no rule for which one wins.
- **Status:** THEORETICAL. No `RateLimiter` exists to run. Settled by either producing the claimed module and measuring 101 requests / 60s, or by rewriting the plan to a single algorithm (fixed window vs. bucket capacity and refill).

---

## Not ranked (checked, no behavioural defect on their own)

- **`Retry-After: 60` is a constant** (`PLAN.md:20`). Coarse but not a wrong status code. Remaining-window would be tighter; not reported as a defect.
- **Current `handle_request` never returns 429.** Executed: 101 calls for a stored tenant `acme` produced `{200: 101}`, headers only `content-type: application/json`, no `Retry-After`. That is the pre-plan public API, not a failure of a plan that has not been applied. It does confirm Steps 2–3 are not already present in the tree.
- **Unknown tenants 404, empty `tenant_id` 401** (`src/api.py:10–14`). Pre-existing routing. The plan’s “top of `handle_request`” check would sit above this; not a new hole.
- **No tests.** There is no suite whose names could be mistaken for proof. Absence of tests is not a wrong result on its own here.

---

## Claims examined

| Claim | Where | Outcome |
|---|---|---|
| `src/limits.py` already implements token-bucket `RateLimiter` | `PLAN.md:12` | **False.** File and module missing (`ModuleNotFoundError`). |
| Extending it with `per_tenant=True` rekeys the same buckets | `PLAN.md:13–14` | **Cannot be true** without the class. No existing global-counter limiter to extend. |
| “No new dependency” | `PLAN.md:14` | **Vacuous / false.** The named dependency is not in the tree; executing the plan requires adding one. |
| Construct `RateLimiter(...)` at module scope and `.check(tenant_id)` | `PLAN.md:18–19` | **Not present** in `src/api.py`; blocked by finding 1. |
| Store buckets in `src/store.py` so the cap survives restart | `PLAN.md:24–26`, `PLAN.md:30` | **False** of the existing store (finding 2). Fresh process empty. |
| 101st request in one minute is `429` | `PLAN.md:29` | **Not met** by current code (101× `200`). **Internally inconsistent** with “token-bucket” (finding 3). |

---

## Coverage

**Read:** `BRIEF.md`, `PLAN.md`, `src/api.py`, `src/store.py`. Full `src/` listing, including after the import (a `__pycache__` from this run only).

**Executed:** import of `api` / `store`; failed import of `limits`; empty-tenant `401`, unknown-tenant `404`, known-tenant `200` with body echo; in-process store put/get; cross-process store miss; 101 sequential `handle_request` calls.

**Did not reach:** inventing a `RateLimiter` to mutation-test bucket refill; multi-process / multi-worker behaviour (nothing in-tree is multi-process); any file outside this directory as a substitute for the missing limiter.
