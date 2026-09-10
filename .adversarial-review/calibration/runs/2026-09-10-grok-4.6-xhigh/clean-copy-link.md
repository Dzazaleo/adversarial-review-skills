# Independent review — copy-link shared-page viewer

Reviewer: Grok (this run). Target: the work in this directory (`PLAN.md`, `viewer.html`). `BRIEF.md` is the audit envelope, not the work.

Work present: `PLAN.md` (39 lines), `viewer.html` (16 lines). No git history, no other source files, no test suite.

Findings are ranked by the cost of leaving them unfixed. Impact is an attribute, not a bucket heading.

---

## Findings (ranked by impact)

### 1. The copy-link feature is not implemented

- **Impact:** critical
- **Location:** `viewer.html:1–16` (entire file); specified in `PLAN.md:10–35`
- **Mechanism:** The plan’s only implementation vehicle is `viewer.html` (`PLAN.md:12–13`: add `<button id="copy-link">Copy link</button>` to that file, no new files). The delivered file is a static stub: `<h1 id="page-title">`, an `<article id="page-body">`, and one paragraph. There is no button, no `id="copy-link"`, no `<script>`, no `navigator.clipboard.writeText`, no `document.execCommand("copy")`, and no label swap to "Copied" or "Press Ctrl+C".
- **Trigger:** Any reader opening the shared page. No special state is required.
- **Consequence:** The goal in `PLAN.md:5–6` is unmet. All three acceptance criteria (`PLAN.md:32–35`) fail: there is no click that puts the URL on the clipboard, no fallback copy, and no failure-path selection or label. The reader cannot copy the page URL in one click and cannot tell from a button whether a copy succeeded, because there is no button.
- **Status:** CONFIRMED. Read `viewer.html` in full. Parsed it with Python’s `html.parser` (tags: `html`, `head`, `meta`×2, `title`, `body`, `main`, `h1#page-title`, `article#page-body`, `p` — no `button`, no `script`). Grepped the directory for `copy-link`, `clipboard`, `execCommand`, `Copied`, `Copy link`, `Ctrl+C`: hits only in `PLAN.md` (and this report). No test suite to run.

### 2. Failure-path “select the URL text” has no URL text to select

- **Impact:** medium
- **Location:** `PLAN.md:26–27`, `PLAN.md:35`; `viewer.html:10–13`
- **Mechanism:** On failure of both copy paths, the plan requires swapping the label to "Press Ctrl+C" **and selecting the URL text** so the reader can copy by hand (`PLAN.md:26–27`). Acceptance repeats it: “the URL is selected on screen” (`PLAN.md:35`). The delivered markup has no URL in it. Visible text is the title "Shared page" and "This page has been shared with you." Step 1 (`PLAN.md:12`) only adds a button next to the title — still no URL. The only URL-bearing node the steps introduce is a “temporary `<input>`” used for `execCommand` (`PLAN.md:21`). A temporary input is normally created, used, and removed (and, in the usual pattern, taken off-screen / `display:none` so it does not flash a form control). After that node is gone or invisible, there is nothing on screen whose selection is the page URL.
- **Trigger:** Both copy paths fail — the case `PLAN.md:19–20` itself flags as the reason for a fallback (`file://` / non-secure context with Clipboard API absent, **and** `execCommand("copy")` returning false). That is also the path iOS Safari often takes with a detached or hidden input.
- **Consequence:** The reader who most needs the manual recovery (clipboard API missing, fallback copy failed) is told to press a shortcut with either nothing selected, or a selection that is not visible. Acceptance criterion 3 cannot be met by executing the stated steps against the stated markup without inventing a persistent, visible URL node the plan never asks for.
- **Status:** CONFIRMED that the document contains no URL text and that the steps never add a persistent visible URL. The claim that a typical “temporary input” will not remain visible on screen is reasoning from the usual `execCommand` pattern, not from running an implementation (there isn’t one).

### 3. Specified recover-from-reject path calls `execCommand` after an awaited `writeText` rejection

- **Impact:** medium
- **Location:** `PLAN.md:17–22`
- **Mechanism:** The happy path is `navigator.clipboard.writeText(location.href)` (`PLAN.md:17`). Feature-detect is: when `navigator.clipboard` is **absent** *or the write **rejects***, fall back to a temporary input + `document.execCommand("copy")` (`PLAN.md:20–22`). `writeText` returns a Promise; a rejection is handled in a microtask/async continuation, not in the original click handler. `document.execCommand("copy")` is a synchronous, user-activation-gated command. Calling it from the rejection handler is the standard footgun: the fallback the plan promises for a failed Clipboard write is no longer in the user-gesture stack that `execCommand` expects. (The **absent** branch can still be synchronous — `navigator.clipboard` is `[SecureContext]` and is undefined on non-secure pages — so this is specifically the **reject** branch, not the unavailable branch.)
- **Trigger:** Secure context (HTTPS), `navigator.clipboard` present, `writeText` rejects — typical cases: the user previously denied clipboard permission; the document is not focused; a browser policy blocks the async clipboard write. The plan explicitly tells the implementer to fall back in that situation.
- **Consequence:** `execCommand` returns false even though a synchronous copy from the same click would likely have succeeded (`execCommand` does not use the Clipboard permission that just failed). The UI then takes the double-failure path (“Press Ctrl+C”) for a user who could have been served by the fallback. Combined with finding 2, that recovery may also have nothing visible to copy.
- **Status:** THEORETICAL. Reasoned from the specified sequence (`writeText` then, on reject, `execCommand`) and from `execCommand`’s user-activation requirement. Not executed: there is no implementation, and headless Chrome in this environment failed before it could dump DOM (`Failed to create a unique user data directory`, then Crashpad `Operation not permitted` / exit 139). A click-and-deny-permission probe in Safari or Chrome would settle it.

### 4. Failure-path label is “Press Ctrl+C” on platforms where that is not how you copy

- **Impact:** low
- **Location:** `PLAN.md:27`, `PLAN.md:35`
- **Mechanism:** Both the step and the acceptance criterion freeze the failure label as the string "Press Ctrl+C". On macOS the copy shortcut is **Cmd+C**. On iOS/Android there is no Ctrl+C. The plan does not vary the string by platform.
- **Trigger:** Both copy paths fail, on a Mac or a phone — the same recovery path as findings 2 and 3. This review machine is macOS.
- **Consequence:** The only remaining instruction is wrong for a large share of readers of a “shared page.” If a visible selection actually exists, a Mac user who ignores the label and presses Cmd+C (or a phone user who long-presses) can still copy; if finding 2 holds, they have a wrong instruction **and** nothing useful selected.
- **Status:** CONFIRMED as specified text. The platform mismatch is not in dispute; what was not executed is a user following the label (no button exists to produce it).

---

## Notes (not ranked)

These are claims whose falsity does not by itself put the wrong bytes on the clipboard. They are not findings.

- **`PLAN.md:19–20`** — “The Clipboard API is only available in a secure context, so a page opened over `file://` or plain HTTP will not have it.” The premise is right; the “so” is not. `http://localhost` and `http://127.0.0.1` are secure contexts: `navigator.clipboard` **is** available there. Feature-detect as specified still does the right thing; a protocol check in place of feature-detect would not. Not ranked.
- **No tests.** There is no test suite. Nothing claimed a test as proof of a guarantee. Absence of tests is not a substitute for finding 1.

---

## Coverage

**Read:** `PLAN.md` (all 39 lines), `viewer.html` (all 16 lines), directory listing (those two plus `BRIEF.md` only). Parsed `viewer.html` with Python `html.parser`. Grepped the tree for the feature’s identifiers and copy-related strings.

**Ran:** no test suite exists. Headless Chrome was attempted against `viewer.html` and a `/tmp` clipboard probe; both failed in this sandbox (Crashpad permission / exit 139). No network, no installs.

**Did not reach:** any actual click, clipboard write, `execCommand` return value, or 2-second label timer — there is no script to exercise, and the browser would not run here. Cross-browser fallback behavior (Safari iOS hidden-input copy, permission-denied `writeText` then `execCommand`) was not executed; finding 3 is marked THEORETICAL for that reason.

**Not in scope / not searched:** parent and sibling directories, git (none), production hosts.
