# Independent review — copy-link shared-page viewer

Reviewer working from `/Users/leo/grok-calibration/2-clean-copy-link`.
In-scope files: `BRIEF.md` (envelope only), `PLAN.md` (39 lines), `viewer.html` (16 lines).
No test suite, no JavaScript, no extra assets. The artifact under review is a plan plus the existing markup it would change — not a finished implementation.

## Findings

None. Ranked list is empty.

## What was checked (and discarded)

The plan was read as a design, not as shipped code. `viewer.html` has no copy control and no script; that is the starting page Step 1 would edit, not an undelivered feature.

**Plan vs. existing markup.** `viewer.html` is well-formed HTML5 (parsed; no unclosed tags, no duplicate ids). Attachment point `h1#page-title` exists. There is no `<form>`, so the specified `<button>` without `type` cannot submit. There is no CSP, permissions policy, or existing script that would block an inline click handler. Step 1's "no new files, no dependency" constraint is compatible with putting the handler in this file.

**Internal consistency of the three steps against acceptance.** Primary path (`navigator.clipboard.writeText(location.href)` + label "Copied" for two seconds) matches the HTTPS acceptance bullet. Fallback (absent clipboard or rejected write → temporary `<input>` + `document.execCommand("copy")`, same success/failure signal) matches the second bullet. Dual-failure (label "Press Ctrl+C" and URL selected) matches the third. Out-of-scope lines do not contradict the goal. The only client state named is the button label; nothing is specified to be stored or sent.

**Clipboard rationale vs. specified control.** `PLAN.md:19–20` says the Clipboard API is unavailable on `file://` or plain HTTP. That sentence is broader than the secure-context rule (localhost HTTP is a secure context). It does not affect the specified behavior: the plan feature-detects `navigator.clipboard` and treats a rejected write as a fallback trigger, rather than sniffing the protocol. Not raised as a defect.

**Dual-failure "select the URL text" with no URL in the current page.** `viewer.html` does not display the page URL. Step 2 already creates a selected temporary `<input>` holding that URL. The dual-failure instruction is reachable from that element still being selected; the plan specifies the user-visible outcome, not a missing control. Not raised as a defect.

**"Press Ctrl+C" on macOS/iOS.** The failure label is an acceptance string (`PLAN.md:27`, `PLAN.md:35`). The load-bearing recovery on that path is the selected URL, which still copies via the platform shortcut or the native selection menu. Treating the hardcoded modifier as a defect would be arguing with a stated label, not catching a path that loses the URL. Not raised.

**Rapid re-click during the two-second "Copied" window, missing `aria-live`, deprecated `execCommand`.** These are implementation footguns or platform noise. The plan states the visible contract (label for two seconds; both copy paths share one signal; `execCommand` as the named fallback). None of them falsifies a step or an acceptance bullet.

## Coverage

Covered: both files of the work (`PLAN.md`, `viewer.html`); plan steps 1–3 against the three acceptance bullets and the out-of-scope line; `viewer.html` structure, ids, and absence of form/CSP/script; secure-context / fallback / dual-failure reading of Step 2–3.

Did not reach: a browser click of the feature (there is no script to run); live Clipboard or `execCommand` behavior in a specific engine (envelope: no network; no implementation); any test suite (none present).
