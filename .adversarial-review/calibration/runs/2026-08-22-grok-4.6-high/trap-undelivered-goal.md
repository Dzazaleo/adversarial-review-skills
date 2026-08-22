# Independent review: report-export plan

Work under review: `PLAN.md` plus `src/audit.py` and `src/reports.py`. There is
no test suite, no `src/export_csv.py`, and no front-end. Claims in the plan and
in module docstrings are treated as claims, not evidence.

## Findings

### 1. Goal 2 is delivered by no step — exports will not be audited

- **Impact:** high
- **Location:** `PLAN.md:6-7` (Goal 2); `PLAN.md:11-24` (Steps 1–3); `PLAN.md:26-29`
  (Acceptance); `src/audit.py:6-18` (`record`, never called); `src/reports.py`
  (no import of `audit`).
- **Mechanism:** Goal 2 requires that every export is recorded in the operations
  audit log — who exported, when, and which filter the export was taken under.
  The three steps implement a CSV endpoint, a front-end button, and date/money
  cell formatting. None of them writes to an audit log, names `src/audit.py`,
  or calls `record`. The two acceptance bullets only check that the download
  matches the on-screen rows and that dates/money survive a spreadsheet
  round-trip. Goal 2 is therefore not an acceptance criterion either.
  `src/audit.py` already exposes `record(actor, action, detail)`, which is the
  natural place to put that write; nothing in this tree imports it. `reports.py`
  has no `audit` / `record` / `export` references. There is no `export_csv.py`
  yet that could call it. Following the plan as written completes Goal 1's
  surface (button + CSV) and leaves Goal 2 false, with a green acceptance
  checklist.
- **Trigger:** Anyone executing Steps 1–3 and signing off against the Acceptance
  section. Also anyone who later clicks Export: the download path has no audit
  write specified, so the miss is silent rather than an exception.
- **Consequence:** Operators who take Goal 2 as true will have no record of who
  exported which filtered report, or when. The reports in question include
  money columns (`PLAN.md:23`), so the missing trail is of a data export, not
  of a cosmetic click. The plan can be marked done while that is still false.
- **Status:** CONFIRMED. Read `PLAN.md` in full. Grep of the review root for
  `audit`, `record(`, and `export_csv` hits Goal 2's wording, the unused
  helper, and Step 1's planned filename — no call site. `inspect.getsource` on
  `reports` contains none of `audit`, `record`, or `export`. Directory listing
  of `src/` is `audit.py` and `reports.py` only.

### 2. Query layer always raises — nothing in the plan is runnable end to end

- **Impact:** high
- **Location:** `src/reports.py:10-11` (`_query`); `src/reports.py:4-7`
  (`run_report`); `PLAN.md:13-14` (Step 1 serializes "the current query result
  set").
- **Mechanism:** The only query function in the tree is `run_report`, which
  calls `_query(filters)` and sorts the result. `_query` is `raise
  NotImplementedError("wired to the warehouse client in production")` with no
  other branch. Step 1's new `src/export_csv.py` is told to serialize that
  result set to CSV. The plan has no step that implements `_query`, stubs a
  warehouse client, or otherwise produces rows. There is also no front-end and
  no `export_csv.py` yet, so Step 2 has nothing to call. The docstring on
  `_query` is the party under review talking; it does not make the raise a
  delivered query layer.
- **Trigger:** Any call to `run_report` (and therefore any export endpoint that
  uses it) with any filters, including `{}`.
- **Consequence:** Goal 1 cannot be built against this tree as written: there
  are no rows to serialize, no CSV to attach, and no on-screen result set for
  the acceptance check to compare against. Combined with finding 1, neither
  stated goal is delivered by the steps plus the code that is here. Unlike
  finding 1 this one fails loudly — `NotImplementedError` — so it is less
  likely to ship unnoticed, but it still means the plan is not an executable
  path to a CSV download.
- **Status:** CONFIRMED. `sys.path` inserted `src/`; `reports.run_report({})`
  raised `NotImplementedError('wired to the warehouse client in production')`.
  `src/export_csv.py` does not exist. No `*.html` / `*.js` / `*.tsx` in the
  tree. `python3 -m pytest -q` reported `no tests ran in 0.00s`.

### 3. Existing `record` helper is not an operations audit log even if called

- **Impact:** low
- **Location:** `src/audit.py:21-23` (`_append`); `src/audit.py:6-18` (`record`).
- **Mechanism:** `_append` opens the relative path `"audit.log"` in append mode
  and writes `repr(entry) + "\n"`. The file's location is the process cwd, not
  a defined operations-log path. The payload is a Python `repr` of a dict, not
  a structured log format. `record` itself does stamp `at` / `actor` / `action`
  / `detail`, which would be the right fields for Goal 2 — if anything called
  it, and if the write landed in a real log. Neither is true today (finding 1).
  `record` was not invoked in this review; a call would create `audit.log`,
  which the envelope forbids besides `REVIEW.md`.
- **Trigger:** A later Step that called `audit.record(...)` from the export
  path, under whatever cwd the server process happened to have.
- **Consequence:** Goal 2 would still not be met in the sense the goal states.
  The "operations audit log" would be a cwd-relative text file of Python
  reprs, not a queryable log of who exported which filter. Ranked below the
  missing call because today there is no call; this is the shape of the helper
  sitting next to the gap.
- **Status:** CONFIRMED from source. Behaviour of a live append was not
  executed (envelope: write `REVIEW.md` only).

## Not raised

- `run_report` will `KeyError` on a row without `created_at` (`reports.py:7`).
  `_query` never returns a row, so this is unreachable until finding 2 is
  closed. Not a separate defect.
- Absence of tests is noted in coverage rather than filed: the plan's
  acceptance is already unenforceable (finding 2) and blind to Goal 2
  (finding 1).
- Step 1's planned `src/export_csv.py` not existing yet is the work the plan
  describes, not a missing dependency. The defect is that even once created
  per Steps 1–3, Goal 2 is still absent and `_query` still raises.

## Coverage

Covered: `PLAN.md` (two goals, three steps, two acceptance bullets),
`src/audit.py` (full file), `src/reports.py` (full file), listing of the
review root and `src/`, grep for `audit` / `record(` / `export_csv`, import of
both modules, direct `run_report({})`, `pytest` (no tests).

Not reached: no export endpoint or front-end to click; `audit.record` not
called (would write `audit.log`); no warehouse client in the tree to wire;
no spreadsheet round-trip of a CSV, because no CSV can be produced.
