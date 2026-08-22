# Independent review

## Findings

### 1. High — The plan never implements or accepts the required audit event

- **Location:** `PLAN.md:6-7`, `PLAN.md:9-24`, and `PLAN.md:26-29`
- **Mechanism:** Goal 2 requires every export to record actor, time, and filter, and `src/audit.py` exposes the logging entry point. None of the three implementation steps calls that entry point or otherwise records an export, and neither acceptance criterion checks the audit log. An implementation that follows every listed step and passes every listed acceptance check can therefore omit auditing completely.
- **Trigger:** The plan is implemented as written, with the endpoint serializing report rows and the button invoking it, but without an additional unlisted audit integration.
- **Consequence:** CSV exports can occur with no operations-log evidence of who exported which filtered data, defeating the explicit accountability requirement.
- **Status:** **CONFIRMED** — I compared every goal with every implementation and acceptance item and inspected the complete source inventory; auditing exists only as an uncalled generic helper.

### 2. Medium — Re-running only the filters cannot guarantee that the export matches the displayed rows

- **Location:** `PLAN.md:18-19`, `PLAN.md:28`, and `src/reports.py:4-7`
- **Mechanism:** The button is planned to send the active filter parameters to an endpoint, which necessarily performs another live report query. Filters identify a query, not the snapshot of rows the user saw. There is no snapshot/version token or displayed-row identifier in the request, despite the acceptance criterion requiring the downloaded rows to match those on screen.
- **Trigger:** A matching row is inserted, updated so it enters or leaves the filter, or deleted after the page query completes but before the export endpoint queries the warehouse.
- **Consequence:** The downloaded CSV can contain a different population from the one the user reviewed, making the export unreliable for reconciliation or evidence-taking.
- **Status:** **THEORETICAL** — the race follows from the two independent queries described by the plan, but the production warehouse implementation needed to exercise it is not present.

### 3. Medium — The audit logger silently selects its destination from process state

- **Location:** `src/audit.py:21-23`
- **Mechanism:** `_append` opens the relative path `audit.log`, so the destination is the process's current working directory rather than a configured, stable operations-log sink. Different launch directories produce different logs without an error.
- **Trigger:** Web workers, a task runner, or a local invocation starts with a working directory other than the one expected by whoever collects `audit.log` (or code changes the working directory).
- **Consequence:** Export events can be written successfully yet be absent from the log that operators inspect, undermining the new audit guarantee.
- **Status:** **CONFIRMED** — I imported the module, changed into a temporary directory, called `record`, and observed that it created `audit.log` in that temporary current directory. The temporary directory was then removed.

### 4. Medium — Spreadsheet-bound text is not protected against formula interpretation

- **Location:** `PLAN.md:13-14` and `PLAN.md:21-24`
- **Mechanism:** The plan specifies CSV serialization and formatting only for dates and money. It has no policy for text cells beginning with spreadsheet formula markers such as `=`, `+`, `-`, or `@`. CSV quoting handles delimiters and newlines but does not stop a spreadsheet from interpreting such a cell as a formula.
- **Trigger:** Any report field containing attacker-controlled or otherwise untrusted text begins with a formula marker and a user opens the export in a spreadsheet that evaluates it.
- **Consequence:** The workbook can execute an injected formula, potentially misleading the user or causing data disclosure through spreadsheet-supported external references.
- **Status:** **THEORETICAL** — there is no report schema, serializer, sample data, or target spreadsheet in the directory with which to determine whether exported fields are untrusted or whether the eventual implementation mitigates the case.

## Coverage

Covered every file in the directory, mapped both stated goals to all plan steps and acceptance criteria, inspected the report-query and audit-log code, inventoried the tree for tests and implementation files, and directly exercised the audit destination behavior. There is no test suite or export/UI implementation to run; production warehouse behavior, report schemas, authentication context, and a target spreadsheet were not available.
