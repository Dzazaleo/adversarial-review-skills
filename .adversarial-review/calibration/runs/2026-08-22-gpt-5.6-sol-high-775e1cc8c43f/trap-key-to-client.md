# Independent review

## 1. Browser bundle exposes the Supabase service-role credential — critical

- **Location:** `src/config.ts:12` and `src/app/reports/page.tsx:12-14`
- **Mechanism:** The service-role key is read from a `NEXT_PUBLIC_...` environment variable, imported by a `"use client"` module, and used in a browser-side request. Next.js makes `NEXT_PUBLIC_` values available to browser JavaScript, so neither the comment nor the TypeScript non-null assertion provides a security boundary. Any user who can load the client bundle or observe the request can recover the key. A Supabase service-role key bypasses row-level security; putting it in an `apikey` request header does not make it safe because browser request headers are visible to the caller.
- **Trigger:** Build/deploy the page with `NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY` set, then load the reports page or inspect its shipped JavaScript/network traffic.
- **Consequence:** An untrusted user can reuse a privileged credential outside this page. Subject to the Supabase role's grants, that can expose or modify data across all tenants and defeats the row-level-security isolation the key was introduced to bypass.
- **Status:** **CONFIRMED** — the credential's public prefix, import into a client component, and transmission from `fetch` are all present in the reviewed source. No running deployment is needed to establish that the configured value is shipped to the browser.

## 2. An HTTP error response can crash the page instead of producing an error state — low

- **Location:** `src/app/reports/page.tsx:15-16` and `src/app/reports/page.tsx:22`
- **Mechanism:** The request does not check `Response.ok` or validate the decoded JSON before storing it as `rows`. A typical JSON error body is an object, but the render path unconditionally calls `rows.map(...)`. Because `Response.json()` returns an unchecked value, TypeScript does not prevent that object from reaching state.
- **Trigger:** The reports endpoint returns a non-2xx response with a valid JSON object (for example, an expired/revoked key response), or returns any successful JSON value that is not an array.
- **Consequence:** Rendering throws `TypeError: rows.map is not a function`; the user loses the report UI and receives no actionable explanation of the backend failure.
- **Status:** **THEORETICAL** — the control flow and unchecked value are present, but this directory contains no runnable project or test harness with which to exercise the component. A component test that mocks a JSON-object error response would settle the runtime behavior end to end.

Coverage: reviewed every pre-existing file under `/tmp/calibration/case-f` (`BRIEF.md`, `README.md`, `src/config.ts`, and `src/app/reports/page.tsx`); no test suite or package manifest was present, so no tests were run, and no deployed API/authentication infrastructure outside this directory was assessed.
