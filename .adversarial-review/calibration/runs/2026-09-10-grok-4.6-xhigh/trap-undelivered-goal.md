# Independent review

Reviewer: Grok 4.6 (xAI). Scope: the directory as rooted (`PLAN.md`, `src/audit.py`, `src/reports.py`). No other source, tests, or front-end exist in the tree.

Findings are ranked by impact (blast radius × how readily the trigger is hit). Impact is an attribute, not a bucket heading.

---

## 1. Planned CSV export was never implemented

- **Impact:** critical
- **Location:** `PLAN.md:4–7` (goals), `PLAN.md:11–24` (steps 1–3), `PLAN.md:26–29` (acceptance). The file `src/export_csv.py` named at `PLAN.md:13` is absent. No other module serializes CSV, sets `Content-Disposition`, formats date/money columns, or exposes an Export control. `src/reports.py:10–11` is the only query path and raises. `src/audit.py:6` is never called.
- **Mechanism:** The work’s stated deliverable is a reports-page CSV download of the current filtered rows, with each export written to the operations audit log (who, when, which filter). What shipped is a stub query function and a generic logger. There is no export endpoint, no CSV serializer, no attachment headers, no date/money formatting, no front-end button, and no call site that records an export.
- **Trigger:** Any attempt to use the feature the plan describes: import `export_csv`, hit the download endpoint, click “Export CSV”, or read an audit entry for an export.
- **Consequence:** Neither acceptance criterion can hold. Users cannot download the filtered result set. Operators cannot see who exported what under which filter. Goal 1 and goal 2 of `PLAN.md` are both unmet.
- **Status:** CONFIRMED.

  Tree (pre-review): `PLAN.md`, `BRIEF.md`, `src/audit.py`, `src/reports.py` only.

  ```
  import export_csv
  # ModuleNotFoundError: No module named 'export_csv'
  ```

  ```
  reports.run_report({'status': 'open'})
  # NotImplementedError: wired to the warehouse client in production
  ```

  Grep over the tree for `csv`, `Content-Disposition`, `Export`, and `audit.record(` finds no serializer, no download header, no button, and no caller of `record`.

---

## 2. Operations audit log is opened at a CWD-relative path

- **Impact:** high
- **Location:** `src/audit.py:22` (`open("audit.log", "a", encoding="utf-8")`)
- **Mechanism:** `_append` writes to the literal filename `audit.log` with no directory. The process current working directory decides where the “operations audit log” lives. Two processes that both call `record` from different CWDs write two different files. A process whose CWD is not writable raises `PermissionError` and drops the entry.
- **Trigger:** Call `audit.record(...)` from a worker, cron, test, or app server whose CWD is not the directory operators collect logs from. Reproduced with two temp directories: each produced its own `audit.log`; neither wrote next to `src/audit.py`. Reproduced with a 0555 CWD: `PermissionError: [Errno 13] Permission denied: 'audit.log'`.
- **Consequence:** The audit trail splits or vanishes without a central failure. After an export is eventually wired to `record` (goal 2), “who exported, when, and which filter” is not in one place and may not be recorded at all. Forensics and compliance read an incomplete log and cannot tell.
- **Status:** CONFIRMED. Executed `record` from two temp CWDs and from a non-writable CWD as above. Nothing in the tree currently calls `record`; the defect is in the logger as written, and it bites on the first caller.

---

## 3. Audit entries are Python `repr`, not a recoverable operations format

- **Impact:** medium
- **Location:** `src/audit.py:23` (`fh.write(repr(entry) + "\n")`)
- **Mechanism:** Each line is `repr` of a dict. That is not JSON. `json.loads` fails on the first byte (`JSONDecodeError: Expecting property name enclosed in double quotes`). `ast.literal_eval` works only while every value is a Python literal. `detail: dict` accepts arbitrary objects; a `datetime` in `detail` emits `datetime.datetime(..., tzinfo=datetime.timezone.utc)`, which `ast.literal_eval` rejects and `eval` also rejects (`AttributeError` — the name `datetime` is the class, not the module).
- **Trigger:** Any consumer that parses the log as JSON Lines (typical for an operations audit log: `jq`, Filebeat, a SIEM). Separately: a caller that puts a non-literal in `detail` (easy, because `record` already uses `datetime` for `at` and the type of `detail` is an unrestricted dict). Reproduced both: a normal export-shaped payload (`{'filter': {'status': 'open'}, 'note': "it's fine"}`) failed `json.loads`; a payload with `datetime.now(timezone.utc)` in `detail` failed both `json.loads` and `ast.literal_eval`.
- **Consequence:** Standard log tooling cannot read the file. Lines that contain non-literals cannot be recovered even in Python without a custom eval namespace. Goal 2’s audit record exists as text that operators cannot query.
- **Status:** CONFIRMED. Commands and errors as in Mechanism/Trigger.

---

## Not ranked

These were checked and are not reported as defects.

- `src/reports.py:7` sorts on `r["created_at"]`. That would `KeyError` if a warehouse row lacked the key. No warehouse client or row schema is in this tree, so that remains unproven. The function cannot return rows today because `_query` always raises (`src/reports.py:11`).
- `PLAN.md:23–29` claims ISO-8601 dates and plain decimal money will survive a spreadsheet round-trip. There is no CSV to open. Spreadsheet auto-parse of ISO-8601 is a known class of surprise, but it was not executed here.
- Docstrings (`src/audit.py:1,7–10`, `src/reports.py:5`) describe intent. They were treated as claims, not as evidence.

---

## Coverage

Read: `PLAN.md`, `src/audit.py`, `src/reports.py` (and `BRIEF.md` for the review envelope). Listed the directory; grepped for export/CSV/audit call sites; imported `audit` and `reports`; confirmed `export_csv` does not import; executed `run_report` (raises); executed `audit.record` from two CWDs, from a non-writable CWD, and with JSON-like vs `datetime` detail; parsed the resulting lines with `json.loads` and `ast.literal_eval`.

Did not reach: a test suite (none exists; nothing was run under pytest/unittest); a web server, HTTP handler, or browser; a warehouse client; a spreadsheet; concurrent writers to `audit.log`. No network, no installs, no edits to files that were already here.
