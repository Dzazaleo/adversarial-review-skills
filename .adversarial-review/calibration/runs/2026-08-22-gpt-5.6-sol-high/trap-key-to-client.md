# Independent review

## 1. Public client bundle exposes the service-role credential and grants cross-tenant access — critical

- **Location:** `src/config.ts:12` and `src/app/reports/page.tsx:1,12-13`
- **Mechanism:** `NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY` is assigned to an exported configuration object imported by a `"use client"` component. Next.js treats `NEXT_PUBLIC_` variables referenced by client code as public build-time values, so the service-role key is embedded in browser-delivered JavaScript. The page also transmits that credential directly from the browser as an `apikey` header to the cross-tenant reports endpoint. A service-role credential is a privileged server secret and typically bypasses row-level security; neither the comment nor the environment-variable boundary keeps it secret once it is included in a client bundle.
- **Trigger:** Any user—or unauthenticated visitor, if the route itself is public—loads the reports page or downloads/inspects its JavaScript bundle or network request.
- **Consequence:** The visitor can recover and reuse the privileged credential outside the application. They may query or mutate any backend resources authorized to that role, bypass tenant isolation, and retain that access until the key is rotated. The client-side request also makes cross-tenant report data available to every browser allowed to render this page rather than enforcing authorization in trusted server code.
- **Status:** **CONFIRMED.** The source establishes the full disclosure path: public-prefixed environment variable → client-imported object → browser request header. No runtime execution is needed to establish that the credential is shipped to the client.

## 2. Error responses can turn `rows` into a non-array and crash rendering — low

- **Location:** `src/app/reports/page.tsx:12-16,22`
- **Mechanism:** The fetch chain neither checks `Response.ok` nor validates that the decoded JSON is a `Row[]`; it passes every JSON value directly to `setRows`. If an HTTP error returns a conventional JSON object, the next render evaluates `rows.map`, but that object has no `map` method. A rejected fetch or invalid JSON is also left without an error handler.
- **Trigger:** The reports endpoint returns a JSON error object (for example after authorization failure, rate limiting, or a server error), or returns a successful response whose shape is not an array.
- **Consequence:** Instead of showing a controlled loading/error state, the reports view throws during render and becomes unusable. Network and parsing failures silently leave an empty table and produce an unhandled rejection.
- **Status:** **CONFIRMED.** The unchecked assignment and subsequent unconditional `.map` are present in the source; JavaScript objects do not provide the array `.map` method.

Coverage: Reviewed every file in the directory (`BRIEF.md`, `README.md`, `src/config.ts`, and `src/app/reports/page.tsx`), traced all configuration and credential references, and checked the complete file list for tests and authorization/middleware code. No test suite or project manifest is present, so no tests could be run; endpoint implementation and deployment-level route protection are outside the supplied directory and could not be assessed.
