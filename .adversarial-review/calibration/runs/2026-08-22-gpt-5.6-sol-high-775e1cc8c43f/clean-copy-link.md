# Independent review

## Findings

### Medium — manual-copy fallback has no viable input lifecycle

- **Location:** `PLAN.md:21-28`
- **Mechanism:** The plan calls the fallback input "temporary," but after both copy mechanisms fail the same URL field must remain present, focused, and selected so the user can copy from it manually. The plan does not say that the field becomes visible or when it is removed. The usual cleanup for a temporary `execCommand` input removes it immediately, which destroys the selection; retaining it instead also contradicts the claim that the button label is the only state the feature keeps.
- **Trigger:** `navigator.clipboard.writeText` is absent or rejects and `document.execCommand("copy")` returns false or throws.
- **Consequence:** An implementation following the temporary-input flow can display "Press Ctrl+C" while leaving no URL selected on screen, so the final acceptance criterion fails and the user still cannot copy the link.
- **Status:** `THEORETICAL` — there is no implementation to execute. An implementation specifying a visible, retained field (plus its cleanup point) would settle this.

### Low — overlapping clicks can corrupt or shorten feedback

- **Location:** `PLAN.md:17-27`
- **Mechanism:** Each click can start an asynchronous clipboard operation and, on success, a two-second restore timer, but the plan provides no ordering rule, in-flight guard, or cancellation of the previous timer. An older operation can therefore overwrite the result of a newer click, and an older timer can restore "Copy link" before two seconds have elapsed for the latest success.
- **Trigger:** The user clicks more than once before the previous clipboard promise and feedback timer have both settled. For example, clicks 1.5 seconds apart let the first click's timer clear the second click's "Copied" state after only 0.5 seconds.
- **Consequence:** The label may report the wrong result or fail to show "Copied" for the promised two seconds, making the feedback unreliable under ordinary repeated interaction.
- **Status:** `THEORETICAL` — no implementation exists to exercise. A single-flight implementation, or clearing/replacing the active timer and ignoring stale promise completions, would settle this.

## Coverage

Covered all contents of `BRIEF.md`, `PLAN.md`, and `viewer.html`; checked the proposed primary, legacy, manual-failure, feedback-timer, and repeated-click paths against the acceptance criteria. No tests or implementation were present to run, and browser-specific clipboard behavior could not be exercised. Nothing in scope was left unread.
