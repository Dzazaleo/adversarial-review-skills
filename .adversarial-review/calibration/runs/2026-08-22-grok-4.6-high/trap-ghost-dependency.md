# Independent review: per-tenant request throttling

Work under review: `PLAN.md` plus `src/api.py` and `src/store.py`. There is no test suite
and no other source. Claims in the plan are treated as claims, not evidence. Behaviour
was checked by importing the modules and calling `handle_request` directly.

## Findings

### 1. Per-tenant cap is not implemented — 101st request is not 429

- **Impact:** critical
- **Location:** `src/api.py:7-15` (`handle_request`); also the module-scope construction
  required by `PLAN.md` Step 2, which is absent from the file.
- **Mechanism:** The stated goal is to cap each tenant at 100 requests per minute and
  return `429` with `Retry-After` once the cap is hit. `handle_request` never constructs
  a limiter, never calls `.check(tenant_id)`, never counts requests, and has no `429`
  branch. After an empty-tenant `401` and a missing-tenant `404`, every other request
  returns `200` with the request body echoed back.
- **Trigger:** Any tenant that exists in the store and issues more than 100 requests in
  a minute. Reproduced with a known tenant (`store.put("tenant:t1", b"ok")`) and 101
  successive `handle_request("t1", …)` calls.
- **Consequence:** The public API has no per-tenant throttle. A single tenant can issue
  unbounded traffic. Operators who ship this as the Step 2 wiring have no cap, no
  `Retry-After`, and no signal that the budget was exceeded.
- **Status:** CONFIRMED. 101 calls against a populated tenant all returned
  `(200, {"content-type": "application/json"}, …)`. No response had status 429. No
  header was `Retry-After` or `retry-after`.

### 2. Planned reuse target `src/limits.py` / `RateLimiter` does not exist

- **Impact:** critical
- **Location:** `PLAN.md:10-14` (Step 1: "reuse the existing limiter");
  `src/limits.py` (cited, missing); `src/api.py` (no import of it).
- **Mechanism:** Step 1 states that `src/limits.py` already implements a token-bucket
  `RateLimiter` for the internal admin API, and that the work is to extend it with
  `per_tenant=True` and reuse that bucket logic. The directory contains only
  `src/api.py` and `src/store.py`. There is no `limits.py`. `import limits` raises
  `ModuleNotFoundError`. `api` has no `RateLimiter` symbol. The "existing" dependency
  the plan is built on is not in the tree, so Step 1 cannot have been done, and Step 2
  cannot have wired it.
- **Trigger:** Anyone following the plan (or reviewing a claim that Step 1 is done)
  looks for `src/limits.py` or tries to construct
  `RateLimiter(per_tenant=True, rate=100, window=60)`.
- **Consequence:** The implementation has no limiter to extend and no shared bucket
  logic to key on tenant ID. The plan's "no new dependency" constraint is vacuously
  satisfied because the old one is a ghost. Delivery of the cap is blocked at the
  first step, which matches Finding 1 on the request path.
- **Status:** CONFIRMED. `src/` listing, `import limits`, and `dir(api)` were all
  checked. The file and the type are not present.

### 3. Counter persistence cannot survive a process restart

- **Impact:** high
- **Location:** `src/store.py:4-12` (`KeyValueStore._data`); `PLAN.md:22-25` (Step 3)
  and `PLAN.md:30` (acceptance: restart does not reset consumed budget).
- **Mechanism:** Step 3 says buckets should be stored in `src/store.py`'s existing
  key-value table so the cap survives a restart. That table is an in-process `dict`
  on `self._data`. `get` / `put` read and write that dict only. There is no file,
  database, or other backing store. A new `KeyValueStore()` starts empty. Even if
  request counters were written here (they are not — the store is only used for
  `tenant:{id}` lookup in `api.py:12`), a process restart re-imports the module,
  constructs a new store, and drops every key.
- **Trigger:** Any restart of the process after a tenant has consumed budget, then
  further requests from that tenant.
- **Consequence:** Acceptance criterion "Restarting the process does not reset a
  tenant's consumed budget" cannot hold with this store. A tenant at the cap can
  recover a full 100-request window by restarting the process. Combined with
  Finding 1, there is currently no budget to persist; the store as written still
  could not meet Step 3 if the limiter were added later and pointed at it.
- **Status:** CONFIRMED. Inspected `KeyValueStore`; constructed a fresh instance
  after putting a key on the module-level store — the new instance's `_data` was
  `{}`.

## Not raised

- `handle_request` echoing the request body on 200 and the 401/404 tenant checks are
  outside the throttling goal. They were exercised only as setup for the 101-request
  probe. No defect claimed.
- There are no tests, so there is no test that could pass while the cap is false.
  Absence of tests is noted here rather than filed as a separate defect: the
  behaviour is already false on the running code.

## Coverage

Covered: `PLAN.md` (goal, three steps, two acceptance lines), `src/api.py` (full
file), `src/store.py` (full file), directory listing of the review root and `src/`,
direct calls to `handle_request` (empty tenant, unknown tenant, known tenant, 101
repeats), `import limits`, and a fresh-`KeyValueStore` restart stand-in.

Not reached: no test suite to run; no other modules; no multi-process or real OS
restart of a long-lived server; concurrency / thread safety of the dict store
(irrelevant until a limiter writes it).
