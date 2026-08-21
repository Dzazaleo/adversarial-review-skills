# "Copy link" button for the shared-page viewer

## Goal

A reader looking at a shared page can copy that page's URL to the clipboard in one click, and
can tell from the button whether the copy succeeded.

## Steps

### Step 1 — the button

Add a `<button id="copy-link">Copy link</button>` to `viewer.html`, next to the page title. It
is a plain button in the existing markup; no new files, no dependency.

### Step 2 — the copy

On click, call `navigator.clipboard.writeText(location.href)`.

The Clipboard API is only available in a secure context, so a page opened over `file://` or
plain HTTP will not have it. Feature-detect: when `navigator.clipboard` is absent or the write
rejects, fall back to selecting the URL in a temporary `<input>` and calling
`document.execCommand("copy")`. Both paths resolve to the same success/failure signal.

### Step 3 — the feedback

On success, swap the button label to "Copied" for two seconds, then restore it. On failure of
both paths, swap it to "Press Ctrl+C" and select the URL text so the reader can copy by hand.
The label is the only state the feature keeps; nothing is stored or sent anywhere.

## Acceptance

- On an HTTPS page, clicking the button puts the page URL on the clipboard and the label reads
  "Copied" for two seconds.
- With `navigator.clipboard` unavailable, the fallback path copies and reports identically.
- With both paths failing, the URL is selected on screen and the label says "Press Ctrl+C".

## Out of scope

Copying anything other than the current page URL; short links; any server involvement.
