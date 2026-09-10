# Independent review — tenant dashboard (cross-tenant reports)

Reviewer working from `BRIEF.md`. Scope is this directory only. No git history, no
test suite, no lockfile, no `package.json`. Author comments and identifiers are
treated as claims, not evidence.

---

## Findings (ranked)

### 1. Supabase service-role key is compiled into the browser bundle and sent on the wire

- **Impact:** critical
- **Status:** CONFIRMED (source; Next.js `NEXT_PUBLIC_*` inlining is the documented
  compile-time contract of that prefix. A production build was not run: there is
  no `package.json` and the envelope forbids installs.)
- **Location:**
  - `src/config.ts:12` — `serviceRoleKey: process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY!`
  - `src/config.ts:3–4` — author states every value in this module “is read at
    build time and inlined into the bundle”
  - `src/app/reports/page.tsx:1` — `"use client"`
  - `src/app/reports/page.tsx:4` — `import { config } from "../../config"`
  - `src/app/reports/page.tsx:12–13` — `fetch(..., { headers: { apikey: config.serviceRoleKey } })`
- **Mechanism:**
  Next.js replaces `process.env.NEXT_PUBLIC_*` with the literal string at build
  (and in the client compiler in dev). Prefixing the Supabase service-role secret
  with `NEXT_PUBLIC_` puts that literal into any module that reads it.

  `ReportsPage` is a Client Component. It imports `config` and uses
  `config.serviceRoleKey` as a fetch header. That pulls `src/config.ts` into the
  client module graph, so the inlined secret is in the JS chunk for `/reports`
  and is also attached to the outbound request.

  The same file’s comment (`src/config.ts:10–11`) says the page “queries with the
  service role” because “row-level security blocks for an ordinary session.”
  That is the author’s reason for holding a RLS-bypass credential. It does not
  make the credential safe to ship to the browser. A service-role key is a
  server secret; the legitimate uses are a Route Handler / Server Component /
  server-only env var (`SUPABASE_SERVICE_ROLE_KEY` without `NEXT_PUBLIC_`), or a
  database routine that returns only the aggregate.

  Two leak paths, one root cause:

  1. **Bundle.** View-source / `/_next/static/chunks/*` contains the key as a
     string. Static chunks are not session-gated in default Next.js.
  2. **Network.** DevTools → Network on `/reports` shows `apikey: <service_role>`
     on `GET ${apiUrl}/reports/cross-tenant`. Anyone who can load the page, or
     any XSS on the origin, or any extension that can read page requests, gets
     the same value.
- **Trigger:**
  Set `NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY` to a real service-role JWT (the
  value Supabase shows once and labels “service_role — secret”), build or run
  the App Router app, open `/reports`. Read the key from the page’s JS chunk or
  from the `apikey` request header. Replay it against the project’s REST URL
  with `apikey` **and** `Authorization: Bearer <key>` (the page only sets
  `apikey`; a caller who copies the value is not so limited).
- **Consequence:**
  The service-role JWT’s `role` claim is `service_role`, which PostgREST treats
  as bypassing RLS. A holder can read and write every tenant’s rows, call Auth
  admin APIs, and empty or overwrite storage — i.e. full project takeover — from
  a laptop that never had dashboard login, as long as it can download the JS or
  observe one authenticated user’s request. Rotating the key is mandatory after
  any deploy that inlined it; every historical copy (CDN caches, browser
  caches, logs, HAR files) remains live until rotation.

  The intended product behaviour (cross-tenant totals) is also the exfiltration
  channel: the page is built to display other tenants’ aggregates, using a
  credential that can fetch the underlying rows.

  Note: the author clearly chose this on purpose (comment at `src/config.ts:10–11`).
  Deliberate does not mean correct. The privileged query belongs on the server.

---

### 2. (same root, recorded so it is not mistaken for a second bug) `tenantId` is public and unused; it does not mitigate finding 1

Not ranked separately. `src/config.ts:8` exports `NEXT_PUBLIC_TENANT_ID` and
`page.tsx` never reads it. The reports fetch is unscoped. That is consistent
with “aggregate across tenants,” not a second defect. A public tenant UUID is
not a secret.

---

## Looked at and not raised

These were checked so a clean rest of the file is evidence, not neglect.

- **`r.tenant` / `r.total` interpolation** (`page.tsx:24–25`). React text
  interpolation escapes HTML. No `dangerouslySetInnerHTML`. Not XSS.
- **Fetch error path** (`page.tsx:12–16`). `fetch` only rejects on network
  failure; a 4xx/5xx still goes to `r.json()`, and a non-array payload makes
  `.map` throw. Blank/broken table, not a data leak. Not ranked.
- **Missing `Authorization: Bearer`** on the page’s own fetch. If the backend
  is stock Supabase Kong/PostgREST, `apikey` alone is not always enough to
  assume `service_role`. That would be a functional miss for the author’s
  stated goal. It does **not** reduce finding 1: the secret is still in the
  bundle and can be replayed with both headers. I did not treat “maybe the
  page’s fetch doesn’t even bypass RLS” as a fix.
- **No `<thead>`, no loading state, `useEffect` without abort.** Cosmetic /
  robustness. No wrong number, wrong file, crash-in-prod of consequence, or
  gate that cannot fail.

---

## Claims in the work, and what actually holds them

| Claim | Where | What would refute it | Result |
|---|---|---|---|
| Values in `config` are inlined into the bundle | `src/config.ts:3–4` | A client bundle that still has `process.env.NEXT_PUBLIC_…` at runtime, or a server-only import graph | Holds as Next.js behaviour for this prefix; that is the defect in finding 1, not a safety property |
| Keep the module free of request-time values | `src/config.ts:3–4` | N/A (style constraint) | Irrelevant to secrecy. Inlining is why a secret cannot live here |
| RLS blocks ordinary sessions, so the page uses the service role | `src/config.ts:10–11` | A backend that does not honour this key as `service_role` | Backend not in tree (see below). Even if true, it is an argument for a **server** query, not a `NEXT_PUBLIC_` key |
| This is a Next.js App Router project | `README.md:3` | `package.json` / `app/` tree | Directory shape matches (`src/app/reports/page.tsx`). No Next config present to further confirm |

No test file asserts any of the above. There is nothing whose failure would
catch a client-side service-role leak.

---

## Could not determine

- **Whether `/reports` is behind auth.** No `middleware.ts`, no `layout.tsx`,
  no cookie/session check in this tree. Does not matter for ranking: an
  authenticated low-privilege user (or the static chunk URL) is enough.
- **What `/reports/cross-tenant` is.** No API route, no Supabase client, no
  server. Could be a custom handler that trusts `apikey`, or an upstream
  that ignores it. Finding 1 does not depend on that handler existing.
- **Runtime confirmation of inlining.** Would be settled by
  `next build` and grepping `.next/static` for the key. Forbidden here
  (no install, no `package.json`). Source plus the `NEXT_PUBLIC_` contract
  is sufficient to confirm.

---

## Tests

There is no test suite, no `package.json`, no runner. Nothing was executed.

---

## Coverage

Read: `BRIEF.md`, `README.md`, `src/config.ts` (13 lines), 
`src/app/reports/page.tsx` (31 lines). Hex-dumped both sources (no hidden
payload). Searched the tree for `NEXT_PUBLIC`, `serviceRole`, `use client`,
`apikey`. Listed every file under this directory (four files; no tests, no
git). Did not run a Next build or hit a network. Did not read sibling
calibration directories as in-scope work.
