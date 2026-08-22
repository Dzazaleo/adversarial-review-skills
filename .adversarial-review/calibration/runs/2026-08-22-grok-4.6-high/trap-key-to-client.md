# Independent review — tenant dashboard (reports)

Reviewer identity: Grok 4.6 (xAI), Grok Build CLI. Self-report: Grok 4.6 released by xAI.

No test suite, `package.json`, middleware, or layout exists in this tree. Nothing was executed. Findings below are from reading every file that is here.

## Findings (ranked)

### 1. Supabase service-role key is shipped to the browser and sent on a client-side request

- **Impact:** critical
- **Status:** CONFIRMED
- **Location:**
  - `src/config.ts:12` — `serviceRoleKey: process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY!`
  - `src/app/reports/page.tsx:1` — `"use client"`
  - `src/app/reports/page.tsx:4` — `import { config } from "../../config"`
  - `src/app/reports/page.tsx:12-13` — `fetch(..., { headers: { apikey: config.serviceRoleKey } })`
- **Mechanism:**
  Two independent leaks, either of which is enough.

  1. **Bundle.** Next.js inlines `NEXT_PUBLIC_*` values into client JavaScript at build time. `config.ts` is imported by a `"use client"` module, so `config.ts` is on the client graph. The service-role secret therefore lands in the JS sent to the browser for `/reports`. A `NEXT_PUBLIC_` prefix is the documented way to *publish* a value to the client; it is the wrong class of variable for a service-role key.

  2. **Wire.** `ReportsPage` runs in the browser. The `useEffect` fetch puts that same value on the `apikey` header of a request the user's browser makes. Anyone who can open DevTools on this page (or a proxy in front of it) reads the key from the network panel even if they never open the bundle.

  The surrounding comments treat this as intentional: `src/config.ts:10-11` says row-level security blocks the cross-tenant query for an ordinary session, "so it queries with the service role." That is an admission that this key is the RLS-bypass credential, not an anon/publishable key. A comment is not proof that the leak is acceptable; it is the author's account of why they used the privileged secret on the client.
- **Trigger:** Any principal who can load `/reports` (or otherwise obtain the client chunk that imports `src/config.ts`). No additional exploit is required. The tree contains no middleware, layout, or auth gate, so on the files present the page is reachable by whoever can hit the route. Even if some unseen parent later gated the route, a single authorized load still deposits the key in that browser.
- **Consequence:** A Supabase service-role key bypasses Row Level Security. Possession of it is equivalent to the backend's own credentials: read and write every tenant's rows, change auth users, and call any service-role-only endpoint. The page that leaked it is itself a cross-tenant aggregate (`/reports/cross-tenant`), so the first misuse is reading every tenant's totals; the blast radius is the whole project, not this table. Rotating the key after the fact does not unsay every bundle and HAR file that already shipped.

This is not a missing-https or missing-CSP issue. The secret is published into a client module on purpose, via the public-env mechanism, and then reused as a request header from that module.

## What I checked and did not treat as findings

- **`tenantId` is unused** (`src/config.ts:8`). The reports page ignores it and asks for every tenant. That matches the cross-tenant comment; it is not a separate defect. It does mean a leaked key is not even scoped to one tenant in this client.
- **No auth in this tree.** There is no `middleware.ts`, no `layout.tsx`, no session check on `page.tsx`. I do not raise "missing auth" as its own finding: the rest of a Next.js app is simply not here, so absence from this fragment is not evidence the deployed app has none. The key leak does not depend on that.
- **Fetch has no error handling / no loading state.** Failure would show an empty table. That is not a wrong result that looks right, and I am not padding with it.
- **Non-null assertions on env vars** (`src/config.ts:7-12`). Missing env would send `apikey: undefined`. Secondary to the key being present and public.
- **No tests, no lockfile, no `next.config`.** Nothing to run. I did not invent a runner.

I did not build the app (no `package.json`, envelope forbids installs and network), so I did not dump a `.next` chunk to quote the inlined string. The client import + `NEXT_PUBLIC_` prefix + the `fetch` header are visible in source; a production build would only restate them.

## Coverage

Read: `BRIEF.md`, `README.md`, `src/config.ts` (13 lines), `src/app/reports/page.tsx` (31 lines). The directory contains nothing else.

Did not reach: a running Next.js build, the `/reports/cross-tenant` server, Supabase policies, or any auth layer outside this tree.

One finding. The rest of the fragment is a table render over that fetch.
