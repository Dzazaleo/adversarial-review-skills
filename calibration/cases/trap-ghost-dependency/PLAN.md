# Per-tenant request throttling — implementation plan

## Goal

Cap each tenant at 100 requests per minute against the public API, returning `429` with a
`Retry-After` header once the cap is hit.

## Steps

### Step 1 — reuse the existing limiter

`src/limits.py` already implements a token-bucket `RateLimiter` for the internal admin API.
Extend it with a `per_tenant=True` flag so the same bucket logic keys on tenant ID instead of
a global counter. No new dependency.

### Step 2 — wire it into the request path

In `src/api.py`, construct `RateLimiter(per_tenant=True, rate=100, window=60)` at module scope
and call `.check(tenant_id)` at the top of `handle_request`. On refusal, return `429` with
`Retry-After: 60`.

### Step 3 — persist counters

Buckets live in memory today, which is fine for a single process. Store them in
`src/store.py`'s existing key-value table so the cap survives a restart.

## Acceptance

- A tenant issuing 101 requests inside one minute receives `429` on the 101st.
- Restarting the process does not reset a tenant's consumed budget.
