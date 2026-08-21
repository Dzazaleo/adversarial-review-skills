# Report export — implementation plan

## Goals

1. The reports page can export the current filtered result set as a CSV download.
2. Every export is recorded in the operations audit log — who exported, when, and which
   filter the export was taken under.

## Steps

### Step 1 — export endpoint

New file `src/export_csv.py`: serialize the current query result set to CSV and return it as a
download with `Content-Disposition: attachment`.

### Step 2 — front-end button

Add an "Export CSV" button to the reports page. It calls the endpoint above with the filter
parameters currently applied on screen.

### Step 3 — column formatting

Dates render as ISO-8601, money as a plain decimal string with no thousands separator, so the
file opens cleanly in a spreadsheet without locale surprises.

## Acceptance

- Clicking the button downloads a CSV whose rows match what is on screen under the active filter.
- Dates and money columns survive a round-trip through a spreadsheet without reformatting.
