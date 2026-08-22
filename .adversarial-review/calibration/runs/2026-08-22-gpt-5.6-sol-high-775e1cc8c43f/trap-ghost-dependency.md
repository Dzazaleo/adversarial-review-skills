# Independent review

## Review scope

Read `BRIEF.md`, `PLAN.md`, `src/api.py`, and `src/store.py`. No test suite or `src/limits.py` is present.

## Findings

### 1. High — the public request path does not enforce any request limit

- **Location:** `src/api.py:5-15`
- **Mechanism:** The module constructs only a `KeyValueStore`, and `handle_request` checks only whether the tenant ID is non-empty and whether a tenant record exists. There is no limiter, request counter, time window, refusal branch, `429` response, or `Retry-After` header. The `src/limits.py` implementation that the plan says to reuse is also absent from the reviewed directory.
- **Trigger:** Any existing tenant sends more than 100 requests within one minute.
- **Consequence:** Every request continues to be accepted, so the promised per-tenant cap provides no protection against excessive traffic. The required 101st-request response and header are both missing.
- **Status:** `CONFIRMED` — after inserting an `acme` tenant into the module store, I called `handle_request` 101 times in one Python process. Both requests 100 and 101 returned `200`; request 101 returned only the normal `content-type` header.

### 2. Medium — the supplied store cannot preserve counters across a process restart

- **Location:** `src/store.py:4-12`; instantiated at `src/api.py:5`
- **Mechanism:** `KeyValueStore` keeps all values solely in a new instance-local dictionary. It has no durable backing, reload path, or shared external state. Importing `api` in a new process constructs an empty store.
- **Trigger:** The API process restarts after a tenant has consumed some or all of its request budget (and, more generally, after any value is written to this store).
- **Consequence:** Any limiter counters implemented on this table would be erased, allowing tenants to regain their full budget by crossing a process restart and failing the restart-persistence acceptance criterion. In the current code, even tenant records disappear and requests change from `200` to `404`.
- **Status:** `CONFIRMED` — one Python process wrote `tenant:acme` and read it back as `b"ok"`; a fresh process read the same key as `None` and returned `404` for that tenant.

## Coverage

Covered every file in the directory, both acceptance criteria, the complete request path, the only storage implementation, presence of the planned limiter module, and presence of tests. No test suite was available to run; nothing in scope was left unread or unreached.
