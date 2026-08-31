#!/usr/bin/env python3
"""Executable invariant checks for this repository.

Every check here corresponds to a defect some review round found by reading prose.
The point is that they now fail instead of needing to be noticed.

    python3 scripts/validate.py            # check everything
    python3 scripts/validate.py --list     # show what it checks

Exits 1 if any ERROR is reported. WARNs do not fail the run.
Requires PyYAML for the frontmatter check; skips that check with a WARN if absent.
"""
import os, re, sys, glob, subprocess, hashlib, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERRORS, WARNS, SKIPPED = [], [], set()


def err(check, msg):
    ERRORS.append(f"{check}: {msg}")


def warn(check, msg):
    WARNS.append(f"{check}: {msg}")


def rel(p):
    return os.path.relpath(p, ROOT)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def skill_dirs():
    return sorted(glob.glob(os.path.join(ROOT, "skills", "*")))


# --------------------------------------------------------------------------- skills

WRITE_CAPABLE = {"Write", "Edit", "NotebookEdit", "Bash", "Agent"}
TOOL_NAME_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_-]*)")
# A budget, not a platform limit, and it is a proxy for something measured elsewhere. What
# decides whether a rule survives an auto-compaction is the ~5,000 tokens re-attached from the
# top of the file — roughly 15,500 characters, which each SKILL.md states as its own "treat
# everything past line ~N as gone" invariant. Total length has no bearing on that: a line below
# the cut is lost at 498 lines and at 540. This number only bounds how much a fully-loaded skill
# costs to read. Raised from 500 on 2026-08-24 to take the multi-reviewer, effort-capture and
# digest-platform rules; the detail behind each went to the references, which have no budget,
# and both files' stated cut estimates were re-measured and remain conservative.
MAX_SKILL_LINES = 540


def check_frontmatter():
    """Frontmatter parses, declares required keys, and grants nothing write-capable."""
    try:
        import yaml
    except ImportError:
        warn("frontmatter", "PyYAML not installed - frontmatter and permissions NOT verified")
        SKIPPED.add(check_frontmatter)
        return
    for d in skill_dirs():
        p = os.path.join(d, "SKILL.md")
        if not os.path.exists(p):
            err("frontmatter", f"{rel(d)} has no SKILL.md")
            continue
        text = read(p)
        if not text.startswith("---"):
            err("frontmatter", f"{rel(p)} does not open with a frontmatter block")
            continue
        # Round 7 codex7-9: split("---")[1] ended the block at any triple hyphen, so a valid
        # quoted description containing one was truncated into invalid YAML.
        block = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
        if not block:
            err("frontmatter", f"{rel(p)} frontmatter block is not closed by a --- line")
            continue
        try:
            fm = yaml.safe_load(block.group(1))
        except Exception as e:
            err("frontmatter", f"{rel(p)} frontmatter is not valid YAML: {e}")
            continue
        for key in ("name", "description", "allowed-tools"):
            if key not in fm:
                err("frontmatter", f"{rel(p)} is missing required key '{key}'")
        # A YAML *string* value made this a set of characters, so every grant passed (A6-4).
        raw = fm.get("allowed-tools") or []
        if isinstance(raw, str):
            raw = [x.strip() for x in raw.replace(",", " ").split()]
        if not isinstance(raw, list) or any(not isinstance(x, (str, int, float)) for x in raw):
            err("frontmatter", f"{rel(p)} allowed-tools must be a string or a flat list of tool "
                               f"names; got {type(raw).__name__} containing non-scalar values")
            continue
        # Claude Code accepts scoped rules such as Edit(/src/**), and the grant is the *tool*.
        # Intersecting exact strings let every scoped write grant through (round 7 codex7-1).
        granted = {m.group(1) for m in (TOOL_NAME_RE.match(str(x)) for x in raw) if m}
        bad = granted & WRITE_CAPABLE
        if bad:
            err("permissions", f"{rel(p)} pre-approves write-capable tool(s) {sorted(bad)} - "
                               "allowed-tools is a grant, not a restriction")


def check_skill_length():
    """SKILL.md stays under the documented 500-line guidance."""
    for d in skill_dirs():
        p = os.path.join(d, "SKILL.md")
        if not os.path.exists(p):
            continue
        n = len(read(p).split("\n"))
        if n >= MAX_SKILL_LINES:
            err("length", f"{rel(p)} is {n} lines; guidance is under {MAX_SKILL_LINES}")


def check_placeholders():
    """No unresolved guillemet placeholder ships in a SKILL.md.

    Templates under references/ legitimately contain them - they are the placeholders.
    A guillemet inside inline code in a SKILL.md is the skill talking *about* the check.
    """
    for d in skill_dirs():
        p = os.path.join(d, "SKILL.md")
        if not os.path.exists(p):
            continue
        # Fenced examples and multi-backtick spans are the skill talking *about* placeholders
        # (round 7 codex7-11); the fence behaviour was previously an accident of the regex.
        stripped = CODE_SPAN_RE.sub("", mask_escapes(defenced(read(p))))
        for i, line in enumerate(stripped.split("\n"), 1):
            if "«" in line or "»" in line:
                err("placeholder", f"{rel(p)}:{i} has an unresolved guillemet outside inline code")


# An inline destination is either <pointy-bracketed> or a run without spaces in which
# parentheses may be balanced one level deep - both are CommonMark, and both used to false-fail
# (round 7 codex7-7).
INLINE_LINK_RE = re.compile(r"\]\(\s*(<[^<>]*>|(?:[^()\s]|\([^()]*\))+)")
REF_LINK_RE = re.compile(r"\]\[([^\]]+)\]")
REF_DEF_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(<[^<>]*>|\S+)", re.M)


def _destination(raw):
    """The path part of a link destination, title stripped, angle brackets removed."""
    raw = raw.strip()
    if raw.startswith("<") and raw.endswith(">"):
        return raw[1:-1].strip()
    return raw.split()[0] if raw.split() else ""


def check_links():
    """Every relative markdown link under skills/ resolves - inline and reference alike."""
    for f in glob.glob(os.path.join(ROOT, "skills", "**", "*.md"), recursive=True):
        text = defenced(read(f))
        defs = {k.strip().lower(): _destination(v) for k, v in REF_DEF_RE.findall(text)}
        targets = [(_destination(m.group(1)), "") for m in INLINE_LINK_RE.finditer(text)]
        # Round 7 codex7-7: a reference link whose definition pointed nowhere was silent.
        for m in REF_LINK_RE.finditer(text):
            label = m.group(1).strip().lower()
            if label in defs:
                targets.append((defs[label], f" (reference link [{m.group(1)})"))
            else:
                err("links", f"{rel(f)} -> [{m.group(1)}] has no link reference definition")
        for path, note in targets:
            if not path or re.match(r"(https?:|#|mailto:|//)", path):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(f), path))
            if not os.path.exists(target):
                err("links", f"{rel(f)} -> {path} does not resolve{note}")


# --------------------------------------------------------------------------- ledger

VERDICTS = ("CONFIRMED", "REFUTED", "COULD NOT DETERMINE", "SETTLED ALREADY",
            "OWNER RULING REQUIRED", "TRUE, NOT A DEFECT")
NO_ACTION_OK = ("REFUTED", "SETTLED ALREADY", "TRUE, NOT A DEFECT")
DISPOSITIONS = ("FIX NOW", "FIX LATER", "ACCEPTED AS-IS", "NO ACTION", "VERIFY",
                "PENDING OWNER")


def ledger_paths():
    return sorted(glob.glob(os.path.join(ROOT, "**", "*REVIEW-ADJUDICATION.md"), recursive=True))


FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def defenced(text):
    r"""`text` with fenced code blocks blanked out, line numbering preserved.

    Round 7 codex7-2: `^# Round \d+` matched inside a fenced example, so appending four lines
    of illustration moved the current-round boundary and demoted every real error before it to
    a warning. Markdown examples are not live syntax and must not be parsed as such - this
    ledger's own R7.2 contains a planted ruling row that was being read as a real one.
    """
    out, fence = [], None
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)[0]
                out.append("")
                continue
            out.append(line)
        else:
            if m and m.group(1)[0] == fence:
                fence = None
            out.append("")
    return "\n".join(out)


ROUND_RE = re.compile(r"^# Round \d+")


def round_marks(text):
    """(0-based line index, heading text) for every real `# Round N` heading.

    Line indices rather than byte offsets: `defenced` blanks fenced lines, which preserves
    line numbering but not character offsets.
    """
    return [(i, ROUND_RE.match(l).group(0))
            for i, l in enumerate(defenced(text).split("\n")) if ROUND_RE.match(l)]


def split_cells(line):
    r"""Split a markdown row on unescaped pipes, counting backslash *parity*.

    Round 7 codex7-8: `(?<!\\)\|` inspects one preceding byte, so a cell ending in the literal
    backslash spelling `\\` swallowed the next delimiter and merged the column after it.
    """
    cells, buf, esc = [], [], 0
    for ch in line:
        if ch == "\\":
            esc += 1
            buf.append(ch)
            continue
        if ch == "|" and esc % 2 == 0:
            cells.append("".join(buf))
            buf, esc = [], 0
            continue
        esc = 0
        buf.append(ch)
    cells.append("".join(buf))
    return cells


DELIMITER_RE = re.compile(r"^\|[\s:|-]+\|?$")


def walk_tables(text):
    """(line number, line, index within its table) for every row of every markdown table.

    A blank or non-pipe line ends a table, so each table's own header can be found - which is
    what `ruling_rows` needs and what a flat row stream cannot provide.
    """
    idx = -1
    for i, line in enumerate(defenced(text).split("\n"), 1):
        if not line.startswith("|"):
            idx = -1
            continue
        idx += 1
        yield i, line, idx


def table_rows(text):
    """Real table rows only - fenced examples and delimiter rows excluded.

    A delimiter row is recognised by *position* - index 1, directly under the header - rather
    than by shape, so a data row whose cells are all dashes is no longer discarded (codex7-8).
    """
    for i, line, idx in walk_tables(text):
        if idx == 1 and DELIMITER_RE.match(line):
            continue
        yield i, line


def check_table_pipes():
    """No unescaped pipe inside inline code in a table row - it silently splits the cell.

    Closed rounds are append-only history and cannot be repaired, so a defect there is a WARN.
    """
    for p in ledger_paths():
        text = read(p)
        cur_line = current_round_line(text)
        for i, line in table_rows(text):
            # A code span is a run of N backticks closed by a run of exactly N (round 7
            # codex7-11: toggling per backtick made ``a | b`` invisible and broke the
            # placeholder check in the opposite direction). Escaped characters are neutralised
            # first, so an escaped backtick cannot mis-pair the runs and an escaped pipe is
            # correctly not a defect - both spellings occur in closed rounds of this ledger.
            count = sum(m.group(2).count("|") for m in CODE_SPAN_RE.finditer(mask_escapes(line)))
            if count:
                report = err if i > cur_line else warn
                where = "" if i > cur_line else " (closed round - append-only, cannot be repaired)"
                report("table", f"{rel(p)}:{i} has {count} unescaped pipe(s) inside inline "
                                f"code; the row will render with extra columns{where}")


CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1", re.S)
ESCAPE_RE = re.compile(r"\\.", re.S)


def mask_escapes(text):
    r"""Backslash-escaped characters replaced by a neutral byte, positions preserved.

    `\|` is a literal pipe and not a defect; `` \` `` must not be mistaken for a code-span
    delimiter. Masking both before span-matching keeps each from corrupting the other.
    """
    return ESCAPE_RE.sub("xx", text)
BOLD_RE = re.compile(r"\*\*(.+?)\*\*", re.S)
# A whole-cell verdict: the term, optionally emphasised, optionally followed by prose after a
# separator. `CONFIRMEDLY` is not a verdict and `_**CONFIRMED**_` is (round 7 codex7-8).
BARE_VERDICT_RE = re.compile(r"^[*_\s]*(" + "|".join(re.escape(v) for v in VERDICTS) + r")(?![A-Z])")


def _leading_term(tok, terms):
    """The known term a bolded run opens with, or None. Admits qualifiers after the term."""
    for t in sorted(terms, key=len, reverse=True):
        if tok == t or re.match(re.escape(t) + r"(?![A-Z])", tok):
            return t
    return None


def declared_disposition(cell):
    """The disposition a cell *commits to* - the first bolded run that opens with a known term.

    Round 7 codex7-4: an `any(term in cell)` test made a *mention* into a commitment
    ("explicitly not FIX NOW" passed), while the skill's own documented compound spelling
    `**PENDING OWNER - proposed: NO ACTION**` could not be parsed at all.
    """
    for m in BOLD_RE.finditer(cell):
        t = _leading_term(m.group(1).strip(), DISPOSITIONS)
        if t:
            return t
    return None


def declared_verdict(cell):
    """The verdict a cell *commits to*, so a quoted verdict cannot legalise a pairing."""
    for m in BOLD_RE.finditer(cell):
        t = _leading_term(m.group(1).strip(), VERDICTS)
        if t:
            return t
    m = BARE_VERDICT_RE.match(cell)
    return m.group(1) if m else None


def row_cells(line):
    """The cells of a markdown table row.

    The trailing pipe is optional in GFM, so it is stripped only when actually present -
    round 7 codex7-8, where an unconditional `[1:-1]` dropped the last column of a valid row
    and made a real ruling row invisible to the census.
    """
    line = line.strip()
    parts = split_cells(line)
    if parts and not parts[0].strip():
        parts = parts[1:]
    if parts and line.endswith("|"):
        parts = parts[:-1]
    return [c.strip() for c in parts]


def _axis_columns(header):
    """(verdict index, disposition index) named by a table's own header row, or None.

    Round 7 codex7-8: assuming the last two cells is right for this ledger's tables and wrong
    in general - a trailing notes column silently moved both axes. The header is asked first
    and the last two are the fallback.
    """
    low = [c.strip().lower().strip("*") for c in header]
    if "verdict" in low and "disposition" in low:
        return low.index("verdict"), low.index("disposition")
    return None


def ruling_rows(text):
    """(line number, line, verdict cell, disposition cell) for every ruling row.

    Round 6 g6-12: scanning the whole line made any row *quoting* a bolded verdict a ruling.
    Both axes are read from their own columns instead - named by **that table's own** header
    where it names them, otherwise the last two - and vertical two-cell detail blocks, whose
    disposition sits on a separate row, are not rows to rule on at all.
    """
    cols = None
    for i, line, idx in walk_tables(text):
        cells = row_cells(line)
        if idx == 0:                      # this table's header
            cols = _axis_columns(cells)
            continue
        if idx == 1 and DELIMITER_RE.match(line):
            continue
        if len(cells) < 3:
            continue
        vi, di = cols if cols and max(cols) < len(cells) else (-2, -1)
        verdict, disposition = cells[vi], cells[di]
        if BARE_VERDICT_RE.match(verdict):
            yield i, line, verdict, disposition


def ruling_cells(line):
    """(verdict cell, disposition cell) for a standalone row, or None. Header-blind."""
    cells = row_cells(line)
    if len(cells) < 3:
        return None
    return (cells[-2], cells[-1]) if BARE_VERDICT_RE.match(cells[-2]) else None


def is_ruling_row(line):
    """A ruling row opens its verdict column with a verdict - bolded or, if half-filled, not."""
    return ruling_cells(line) is not None


def last_round(text):
    """The final '# Round N' section, or the whole file if there are no round headings."""
    marks = round_marks(text)
    return "\n".join(text.split("\n")[marks[-1][0]:]) if marks else text


def current_round_line(text):
    """Line number of the current round's heading; 0 when the file has no round headings."""
    marks = round_marks(text)
    return marks[-1][0] + 1 if marks else 0


def reporter(i, cur_line):
    """Errors in the current round, warnings in the closed prefix.

    Round 6 g6-6: scoping these checks to the last round meant a defect introduced into an
    earlier one was not merely unrepairable but invisible. Closed rounds are append-only
    history and must not fail the build - but silence is not the same as looking.
    """
    if i > cur_line:
        return err, ""
    return warn, " (closed round - append-only history, not repairable)"


def check_ledger_axes():
    """Every row carrying a verdict also carries a disposition, in its own column."""
    for p in ledger_paths():
        text = read(p)
        cur_line = current_round_line(text)
        for i, line, _verdict, disposition in ruling_rows(text):
            # A *commitment*, not a mention: "explicitly not FIX NOW" is not a disposition
            # (round 7 codex7-4).
            if declared_disposition(disposition) is None:
                report, where = reporter(i, cur_line)
                report("two-axes", f"{rel(p)}:{i} row '{line[:44].strip()}...' has a verdict "
                                   f"but no disposition{where}")


NO_ACTION_RE = re.compile(r"\*\*(" + "|".join(re.escape(v) for v in NO_ACTION_OK) + r")")

# Round 7 A7-4: operators are told which closed-round warnings are expected and permanent, so an
# unexpected one would otherwise arrive among them unremarked. Anything not pinned here is
# flagged as new.
# Pinned by row *identity*, not by line: appending anywhere above shifts every line number
# below it, and pinning on those re-flagged known rows as new the first time it was tested.
# The IDs are stable because closed rounds are immutable.
# Empty since 2026-08-31: the two pinned rows (R3-P3, R3-P4, documented at R6.15) lived in the
# seven-round working ledger, which was removed from the repository along with the raw report
# corpus. Recover from commit ef74e91 at the pre-move root paths if that history is ever needed.
# The guard stays live for the ledgers that remain under examples/, which raise none today.
EXPECTED_HISTORY = set()


def history_note(p, cells):
    """'' for a known permanent warning, a loud marker for any other closed-round one."""
    raw = re.sub(r"[*`]", "", cells[0]).strip() if cells else ""
    if (rel(p), raw) in EXPECTED_HISTORY:
        return " (expected permanent history, documented at R6.15)"
    return " (NOT one of the expected history warnings - this is new, review it)"


def check_no_action_legality():
    """NO ACTION is legal only under the verdicts that permit it; no bare ACCEPTED.

    Both axes are read from their own columns: a row whose *notes* discuss the forbidden
    pairing is discussing it, not committing it (round 6 g6-12).
    """
    for p in ledger_paths():
        text = read(p)
        cur_line = current_round_line(text)
        for i, line, verdict, disposition in ruling_rows(text):
            report, where = reporter(i, cur_line)
            declared = declared_disposition(disposition)
            says_no_action = (declared == "NO ACTION" if declared
                              else "NO ACTION" in disposition)
            # The verdict the row *commits to* - a quoted REFUTED elsewhere in the cell no
            # longer legalises the pairing (round 7 codex7-4).
            if says_no_action and declared_verdict(verdict) not in NO_ACTION_OK:
                mark = where if i > cur_line else history_note(p, row_cells(line))
                report("disposition", f"{rel(p)}:{i} row '{line[:44].strip()}...' pairs NO ACTION "
                                      f"with a verdict that does not permit it{mark}")
            if re.search(r"\*\*ACCEPTED\*\*(?!\s*AS-IS)", disposition):
                report("disposition", f"{rel(p)}:{i} row '{line[:44].strip()}...' uses a bare "
                                      f"'ACCEPTED' - it means both 'real' and 'shipping with it'{where}")


# The ID namespace, declared rather than guessed (round 7 Q7-1, closing codex7-10 and A7-3).
# Auxiliary series are these eight uppercase tags and nothing else; a numbered finding carries a
# lowercase reviewer tag (`codex7-1`, `grok-3`, `g6-1`), the historical `F<n>` of rounds 1-3, or a
# bare integer as the worked example under examples/ uses. All three spellings were read off the
# corpus rather than invented - the rule is a description of the data, not a preference.
# An ID that is neither is reported rather than silently classified - which is what the old
# `^(CNV|[PDUACXQ])` guess did, dropping any finding whose tag began with a reserved letter.
AUX_SERIES = ("CNV", "P", "D", "U", "A", "X", "Q", "C")
AUX_ID_RE = re.compile(r"^(CNV|[PDUACXQ])[0-9]*(-|$)")
NUMBERED_ID_RE = re.compile(r"^([a-z][a-z0-9]*-?[0-9]+|F[0-9]+|[0-9]+)$")

# Censuses history records that the namespace rule cannot derive. Immutable rounds cannot be
# edited to declare themselves, so the exception lives here, dated and reasoned, rather than the
# rule being relaxed until history passes.
COUNT_EXCEPTIONS = {
    # Round 4 filed its 27th reviewer finding as `P-1 (grok-13)` because the fix landed in the
    # brief rather than the code; round 4's own header says so. Adjudicated 2026-08-22.
    "# Round 4": (27, 26, "grok-13 is filed under the process ID P-1; round 4's header records it"),
}


def bare_id(cell):
    """An ID cell reduced to its series - emphasis stripped, round prefix dropped."""
    ident = re.sub(r"[*`]", "", cell).strip()
    ident = re.sub(r"\s*\(.*\)$", "", ident)          # `P-1 (grok-13)` -> `P-1`
    return re.sub(r"^R\d+-", "", ident)


def classify_id(cell):
    """'aux', 'numbered', or None when the ID matches no declared series."""
    b = bare_id(cell)
    if AUX_ID_RE.match(b):
        return "aux"
    if NUMBERED_ID_RE.match(b):
        return "numbered"
    return None


def rounds(text):
    """(name, first-line-number, body) for each section, opening adjudication included.

    Round 7 codex7-3: slicing only from the first `# Round N` heading put everything above it -
    this ledger's entire first adjudication - in no section at all, where its census could be
    vandalised in complete silence.
    """
    lines = text.split("\n")
    marks = round_marks(text)
    if not marks:
        return [("(no round heading)", 1, text)]
    out = []
    if "\n".join(lines[:marks[0][0]]).strip():
        out.append(("(opening adjudication)", 1, "\n".join(lines[:marks[0][0]])))
    for k, (idx, name) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(lines)
        out.append((name, idx + 1, "\n".join(lines[idx:end])))
    return out


def count_finding_rows(section):
    """(numbered rows, [undeclared IDs]) - auxiliary series are counted separately."""
    n, unknown = 0, []
    for _, line, _v, _d in ruling_rows(section):
        cells = row_cells(line)
        if not cells:
            continue
        kind = classify_id(cells[0])
        if kind == "aux":
            continue
        if kind is None:
            unknown.append(bare_id(cells[0]))
            continue
        n += 1
    return n, unknown


def check_counts():
    """Stated findings-in equals stated rows-out, and rows-out equals the rows that exist.

    Round 6 g6-1: comparing the two header numbers to each other established nothing about
    reality - five ruling rows could be deleted with the header left alone and the run stayed
    green. The rows are counted now.
    """
    for p in ledger_paths():
        text = read(p)
        last = rounds(text)[-1][0]
        for name, start, section in rounds(text):
            current = name == last
            report = err if current else warn
            where = "" if current else f" in the closed {name} (history, not repairable)"
            actual, unknown = count_finding_rows(section)
            for u in unknown:
                report("counts", f"{rel(p)} {name} has ruling row ID '{u}', which matches no "
                                 f"declared series - it is counted as neither a numbered finding "
                                 f"nor an auxiliary entry{where}")
            m = re.search(r"Findings in:\s*\*{0,2}(\d+)", section)
            n = re.search(r"Rows out:\s*\*{0,2}(\d+)", section)
            if not m or not n:
                # A round with no rows to account for has nothing to state (round 1 is a
                # correction). A round carrying rulings must state its census.
                if actual:
                    report("counts", f"{rel(p)} {name} states no findings-in/rows-out pair but "
                                     f"carries {actual} numbered finding row(s){where}")
                continue
            if m.group(1) != n.group(1):
                report("counts", f"{rel(p)} states {m.group(1)} findings in but "
                                 f"{n.group(1)} rows out{where}")
            # Closed rounds are counted too (round 7 codex7-3: scoping this to the current
            # round meant a row could be deleted from a closed one in silence).
            stated = int(n.group(1))
            exc = COUNT_EXCEPTIONS.get(name)
            if exc and (stated, actual) == exc[:2]:
                continue
            if stated != actual:
                report("counts", f"{rel(p)} {name} states {stated} rows out but {actual} "
                                 f"numbered finding rows are present{where}")


# --------------------------------------------------------------------------- corpus

DIGEST_PATHS = ["calibration/cases", "calibration/CALIBRATION-PROMPT.md",
                "calibration/ANSWER-KEY.md"]


def corpus_digest():
    """Digest the tracked instrument, mirroring calibration/record-template.md."""
    out = subprocess.run(["git", "ls-files", "-z"] + DIGEST_PATHS,
                         cwd=ROOT, capture_output=True)
    # Round 7 A7-1: without this, a tree with no .git returns empty, the digest becomes the
    # hash of nothing, and every filed record is reported stale - a false statement, raised
    # with no exception for the caller to catch.
    if out.returncode != 0:
        raise RuntimeError(f"git ls-files exited {out.returncode}: "
                           f"{out.stderr.decode('utf-8', 'replace').strip()[:120]}")
    # Byte order, so the digest does not depend on the shell's collation. `sort` under
    # en_US.UTF-8 orders README.md against its lowercase siblings differently from LC_ALL=C,
    # and on this very corpus that is the difference between 775e1cc8c43f and bf13a2b6c2ff.
    files = sorted(f for f in out.stdout.split(b"\0") if f)
    inner = b""
    for f in files:
        # Working-tree bytes, so a CRLF checkout hashes differently and every record filed
        # against it reads as permanently stale. The repository's root `.gitattributes` marks
        # every path `-text` to pin the checkout whatever the cloner's core.autocrlf says.
        h = hashlib.sha1(open(os.path.join(ROOT, f.decode()), "rb").read()).hexdigest()
        # Two spaces, always, and that is the point of building the stream here rather than
        # shelling out. The documented command pipes through `shasum`, whose separator is
        # platform-dependent: text mode (two spaces) by default on macOS and Linux, binary
        # (` *`) by default on Windows. Identical corpus, 775e1cc8c43f here against
        # 676b43331561 there. `-t` is in the documented command for that reason; this function
        # is the authority wherever the two disagree. Found 2026-08-24, after a Windows session
        # read two valid, in-date records as stale on this alone.
        inner += f"{h}  {f.decode()}\n".encode()
    return hashlib.sha1(inner).hexdigest()[:12]


def calibration_records():
    """Every record either consumer could resolve, in lookup order, tagged by where it lives.

    Two locations, because a record is now filed at `~/.adversarial-review/calibration/` by
    default and only pinned under a project root deliberately - see `calibration/README.md`.
    Home records are **machine** state, not repository state, so a stale one can only warn: the
    same checkout must not pass on one machine and fail on another. That is the rule
    `check_installed_copies` already runs under. A pinned record is tracked-adjacent repository
    state and keeps the hard failure.
    """
    here = os.path.join(ROOT, ".adversarial-review", "calibration")
    home = os.path.expanduser("~/.adversarial-review/calibration")
    out = [(p, rel(p), err) for p in sorted(glob.glob(os.path.join(here, "*.md")))]
    if os.path.realpath(home) != os.path.realpath(here):
        out += [(p, "~/" + os.path.relpath(p, os.path.expanduser("~")), warn)
                for p in sorted(glob.glob(os.path.join(home, "*.md")))]
    return out


def check_calibration_digests():
    """Every filed calibration record's digest matches the current instrument."""
    records = calibration_records()
    if not records:
        warn("calibration", "no calibration records on file in ./ or ~/")
        return
    try:
        actual = corpus_digest()
    except Exception as ex:
        warn("calibration", f"could not compute the corpus digest: {ex}")
        SKIPPED.add(check_calibration_digests)   # round 7 codex7-5
        return
    for r, name, report in records:
        text = read(r)
        m = re.search(r"Corpus digest\D+`([0-9a-f]{6,})`", text)
        if not m:
            report("calibration", f"{name} has no Corpus digest row")
        elif m.group(1) != actual:
            report("calibration", f"{name} records digest {m.group(1)} but the instrument is "
                                  f"{actual} - that record is stale and counts as missing")
        e = re.search(r"\*\*Expires\*\*\s*\|\s*(\d{4}-\d{2}-\d{2})", text)
        if not e:
            report("calibration", f"{name} has no Expires row")
            continue
        # Round 7 codex7-6: a lexical compare against *local* today made one record pass on one
        # machine and fail on another at the same instant, and let 9999-99-99 never expire.
        try:
            expires = datetime.date.fromisoformat(e.group(1))
        except ValueError:
            report("calibration", f"{name} has an Expires value that is not a real date: "
                                  f"{e.group(1)}")
            continue
        if expires < datetime.datetime.now(datetime.timezone.utc).date():
            report("calibration", f"{name} expired {e.group(1)} (UTC) - a record past its window "
                                  "is stale and counts as missing")


# --------------------------------------------------------------------------- install

def check_installed_copies():
    """Where the skills are installed, they match the repository.

    This check reads `~/.claude/skills`, so its output is a statement about this machine rather
    than about the repository, and it can only ever warn - it never fails the build. Round 7
    codex7-12 is right that this sits outside "nothing depends on which machine it runs on";
    it is kept because knowing the version you actually run is stale is worth a warning line.
    """
    home = os.path.expanduser("~/.claude/skills")
    if not os.path.isdir(home):
        return
    for d in skill_dirs():
        inst = os.path.join(home, os.path.basename(d))
        if not os.path.isdir(inst):
            continue
        r = subprocess.run(["diff", "-rq", d, inst], capture_output=True, text=True)
        if r.returncode:
            warn("install", f"{rel(d)} differs from the installed copy at {inst} - "
                            "the version you actually run is not this one")


def check_retired_wordings():
    """A rule that was changed must not survive anywhere in its old wording.

    This is the mechanical form of R4.14's "grep the repository for the claim, not for the
    file you were told about" - corrected per round 5's P-4, because a line-oriented grep
    misses any rule whose wording wraps across a line break, which is most of them here.
    Whitespace is normalized before matching for exactly that reason.

    Live prose only. The ledger, the external reports and examples/ quote retired wordings
    as history and must keep them verbatim.
    """
    retired = [
        (r"before the ledger is written|written before the ledger",
         "FIX LATER ordering; superseded by 'before the row receives its FIX LATER disposition'"),
        (r"never saw the report|never seen the report",
         "blindness claim; superseded by 'was not handed the report'"),
        (r"blind spots you share with its author are the ones most likely to survive|"
         r"is one this review is least likely to catch",
         "same-family assertion; the branch now states the uncertainty instead"),
    ]
    live = []
    for pat in ("skills/**/*.md", "README.md", "HOW-IT-WORKS.md", "BACKLOG.md",
                "calibration/*.md"):
        live += glob.glob(os.path.join(ROOT, pat), recursive=True)
    for f in sorted(set(live)):
        # Whitespace was normalized for the line-wrap case (P-4). Emphasis markers and code
        # spans broke the same phrases just as silently (round 6 g6-7), and a footnote marker
        # broke them in the one spelling that fix did not reach (B-4). All three go.
        flat = re.sub(r"\[\^[^\]]*\]", "", read(f))
        flat = re.sub(r"[*_`]", "", re.sub(r"\s+", " ", flat))
        for rx, why in retired:
            if re.search(rx, flat, re.I):
                err("retired", f"{rel(f)} still carries a retired wording - {why}")


def check_invariant_backrefs():
    """Every (SS N) back-reference in an <invariants> block names a section that exists.

    Round 5 found two invariants that summarized their own sections wrongly - one too narrow,
    one too broad. Whether a summary is faithful is not mechanically checkable; whether it
    points at a real section is, and a dangling pointer is the cheap half of the same defect.
    """
    for d in skill_dirs():
        p = os.path.join(d, "SKILL.md")
        if not os.path.exists(p):
            continue
        text = read(p)
        m = re.search(r"<invariants>(.*?)</invariants>", text, re.S)
        if not m:
            err("backref", f"{rel(p)} has no <invariants> block - the block that survives "
                           "compaction is missing entirely")
            continue
        sections = set(re.findall(r"^##\s+(\d+)\.", text, re.M))
        for ref in re.findall(r"\u00a7(\d+)", m.group(1)):
            if ref not in sections:
                err("backref", f"{rel(p)} invariants cite \u00a7{ref}, which has no section")


CHECKS = [
    ("frontmatter parses, required keys present", check_frontmatter),
    ("no write-capable tool is pre-approved", check_frontmatter),
    ("SKILL.md under the 500-line guidance", check_skill_length),
    ("no unresolved guillemet ships in a SKILL.md", check_placeholders),
    ("every relative link under skills/ resolves", check_links),
    ("no unescaped pipe inside a ledger table cell", check_table_pipes),
    ("every verdict has a disposition (closed rounds warn)", check_ledger_axes),
    ("NO ACTION legality, no bare ACCEPTED (closed rounds warn)", check_no_action_legality),
    ("findings in equals rows out, every round (closed rounds warn)", check_counts),
    ("calibration records match the corpus digest and are in date", check_calibration_digests),
    ("installed copies match the repository (environment report; warns only)",
     check_installed_copies),
    ("no retired rule wording survives in live prose", check_retired_wordings),
    ("every invariant back-reference names a real section", check_invariant_backrefs),
]


def main():
    if "--list" in sys.argv:
        for name, _ in CHECKS:
            print(f"  {name}")
        n_names, n_fns = len(CHECKS), len({fn for _, fn in CHECKS})
        print(f"\n  {n_names} named invariants over {n_fns} checks "
              f"({n_names - n_fns} name(s) share an implementation)")
        return 0
    ran = set()
    for _, fn in CHECKS:
        if fn not in ran:
            fn()
            ran.add(fn)
    # A check that could not run has not passed (round 6 g6-13).
    passed = ran - SKIPPED
    for w in WARNS:
        print(f"WARN  {w}")
    for e in ERRORS:
        print(f"ERROR {e}")
    if ERRORS:
        print(f"\n{len(ERRORS)} error(s), {len(WARNS)} warning(s)")
        return 1
    tail = f" ({len(WARNS)} warning(s))" if WARNS else ""
    if SKIPPED:
        names = sorted(n for n, fn in CHECKS if fn in SKIPPED)
        tail += f"; {len(SKIPPED)} check SKIPPED and NOT counted - " + "; ".join(names)
    print(f"{len(passed)} of {len({fn for _, fn in CHECKS})} checks pass{tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
