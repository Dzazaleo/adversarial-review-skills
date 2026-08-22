#!/usr/bin/env python3
"""Executable invariant checks for this repository.

Every check here corresponds to a defect some review round found by reading prose.
The point is that they now fail instead of needing to be noticed.

    python3 scripts/validate.py            # check everything
    python3 scripts/validate.py --list     # show what it checks

Exits 1 if any ERROR is reported. WARNs do not fail the run.
Requires PyYAML for the frontmatter check; skips that check with a WARN if absent.
"""
import os, re, sys, glob, subprocess, hashlib

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
MAX_SKILL_LINES = 500


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
        try:
            fm = yaml.safe_load(text.split("---")[1])
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
        granted = set(raw)
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
        stripped = re.sub(r"`[^`]*`", "", read(p))
        for i, line in enumerate(stripped.split("\n"), 1):
            if "«" in line or "»" in line:
                err("placeholder", f"{rel(p)}:{i} has an unresolved guillemet outside inline code")


def check_links():
    """Every relative markdown link under skills/ resolves."""
    for f in glob.glob(os.path.join(ROOT, "skills", "**", "*.md"), recursive=True):
        for m in re.finditer(r"\]\((?!https?:|#|mailto:)([^)#]+)", read(f)):
            # A quoted title after the path is valid CommonMark and is not part of the path
            # (round 6 A6-3). An unbracketed path cannot contain a space, so the first token
            # is the whole of it.
            parts = m.group(1).strip().split()
            if not parts:
                continue
            path = parts[0]
            target = os.path.normpath(os.path.join(os.path.dirname(f), path))
            if not os.path.exists(target):
                err("links", f"{rel(f)} -> {path} does not resolve")


# --------------------------------------------------------------------------- ledger

VERDICTS = ("CONFIRMED", "REFUTED", "COULD NOT DETERMINE", "SETTLED ALREADY",
            "OWNER RULING REQUIRED", "TRUE, NOT A DEFECT")
NO_ACTION_OK = ("REFUTED", "SETTLED ALREADY", "TRUE, NOT A DEFECT")
DISPOSITIONS = ("FIX NOW", "FIX LATER", "ACCEPTED AS-IS", "NO ACTION", "VERIFY",
                "PENDING OWNER")


def ledger_paths():
    return sorted(glob.glob(os.path.join(ROOT, "**", "*REVIEW-ADJUDICATION.md"), recursive=True))


def table_rows(text):
    for i, line in enumerate(text.split("\n"), 1):
        if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", line):
            yield i, line


def check_table_pipes():
    """No unescaped pipe inside inline code in a table row - it silently splits the cell.

    Closed rounds are append-only history and cannot be repaired, so a defect there is a WARN.
    """
    for p in ledger_paths():
        text = read(p)
        marks = [m.start() for m in re.finditer(r"^# Round \d+", text, re.M)]
        cur_line = text[:marks[-1]].count("\n") + 1 if marks else 0
        for i, line in table_rows(text):
            in_code, count, escaped = False, 0, False
            for ch in line:
                if escaped:
                    escaped = False
                    continue
                if ch == "\\":
                    escaped = True
                elif ch == "`":
                    in_code = not in_code
                elif ch == "|" and in_code:
                    count += 1
            if count:
                report = err if i > cur_line else warn
                where = "" if i > cur_line else " (closed round - append-only, cannot be repaired)"
                report("table", f"{rel(p)}:{i} has {count} unescaped pipe(s) inside inline "
                                f"code; the row will render with extra columns{where}")


VERDICT_RE = re.compile(r"\*\*(" + "|".join(re.escape(v) for v in VERDICTS) + r")")
BARE_VERDICT_RE = re.compile(r"^\**(" + "|".join(re.escape(v) for v in VERDICTS) + r")")
DISPOSITION_RE = re.compile(r"\*\*([A-Z][A-Z ,'-]*?)\*\*")


def declared_disposition(cell):
    """The disposition a cell *commits to* - its first bolded known term, not any mention."""
    for m in DISPOSITION_RE.finditer(cell):
        tok = m.group(1).strip()
        if tok in DISPOSITIONS:
            return tok
    return None


CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")


def row_cells(line):
    """The cells of a markdown table row, outer pipes stripped.

    Splits on *unescaped* pipes only. A `\\|` is a literal pipe inside a cell, not a column
    boundary; splitting on it shifted every column after it and mis-read both axes.
    """
    return [c.strip() for c in CELL_SPLIT_RE.split(line)[1:-1]]


def ruling_cells(line):
    """(verdict cell, disposition cell) for a ruling row, or None.

    Round 6 g6-12: scanning the whole line made any row *quoting* a bolded verdict a ruling,
    and any row whose notes named a disposition carry that disposition. Both axes are read
    from their own columns instead - the last two - and vertical two-cell detail blocks, whose
    disposition sits on a separate row, are not rows to rule on at all.
    """
    cells = row_cells(line)
    if len(cells) < 3:
        return None
    verdict, disposition = cells[-2], cells[-1]
    return (verdict, disposition) if BARE_VERDICT_RE.match(verdict) else None


def is_ruling_row(line):
    """A ruling row opens its verdict column with a verdict - bolded or, if half-filled, not."""
    return ruling_cells(line) is not None


def last_round(text):
    """The final '# Round N' section, or the whole file if there are no round headings."""
    marks = [m.start() for m in re.finditer(r"^# Round \d+", text, re.M)]
    return text[marks[-1]:] if marks else text


def current_round_line(text):
    """First line number of the current round; 0 when the file has no round headings."""
    marks = [m.start() for m in re.finditer(r"^# Round \d+", text, re.M)]
    return text[:marks[-1]].count("\n") + 1 if marks else 0


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
        for i, line in table_rows(text):
            cells = ruling_cells(line)
            if cells is None:
                continue
            if not any(d in cells[1] for d in DISPOSITIONS):
                report, where = reporter(i, cur_line)
                report("two-axes", f"{rel(p)}:{i} row '{line[:44].strip()}...' has a verdict "
                                   f"but no disposition{where}")


NO_ACTION_RE = re.compile(r"\*\*(" + "|".join(re.escape(v) for v in NO_ACTION_OK) + r")")


def check_no_action_legality():
    """NO ACTION is legal only under the verdicts that permit it; no bare ACCEPTED.

    Both axes are read from their own columns: a row whose *notes* discuss the forbidden
    pairing is discussing it, not committing it (round 6 g6-12).
    """
    for p in ledger_paths():
        text = read(p)
        cur_line = current_round_line(text)
        for i, line in table_rows(text):
            cells = ruling_cells(line)
            if cells is None:
                continue
            verdict, disposition = cells
            report, where = reporter(i, cur_line)
            declared = declared_disposition(disposition)
            says_no_action = (declared == "NO ACTION" if declared
                              else "NO ACTION" in disposition)
            if says_no_action and not NO_ACTION_RE.search(verdict):
                report("disposition", f"{rel(p)}:{i} row '{line[:44].strip()}...' pairs NO ACTION "
                                      f"with a verdict that does not permit it{where}")
            if re.search(r"\*\*ACCEPTED\*\*(?!\s*AS-IS)", disposition):
                report("disposition", f"{rel(p)}:{i} row '{line[:44].strip()}...' uses a bare "
                                      f"'ACCEPTED' - it means both 'real' and 'shipping with it'{where}")


AUX_ID_RE = re.compile(r"^(CNV|[PDUACXQ])[0-9]*(-|$)")


def bare_id(cell):
    """An ID cell reduced to its series - emphasis stripped, round prefix dropped."""
    ident = re.sub(r"[*`]", "", cell).strip()
    return re.sub(r"^R\d+-", "", ident)


def rounds(text):
    """(name, first-line-number, body) for each '# Round N' section, or one unnamed section."""
    marks = [(m.start(), m.group(0)) for m in re.finditer(r"^# Round \d+", text, re.M)]
    if not marks:
        return [("(no round heading)", 1, text)]
    out = []
    for k, (pos, name) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(text)
        out.append((name, text[:pos].count("\n") + 1, text[pos:end]))
    return out


def count_finding_rows(section):
    """Ruling rows for *numbered findings* - auxiliary series are counted separately."""
    n = 0
    for _, line in table_rows(section):
        if not is_ruling_row(line):
            continue
        cells = row_cells(line)
        if cells and AUX_ID_RE.match(bare_id(cells[0])):
            continue
        n += 1
    return n


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
            m = re.search(r"Findings in:\s*\*{0,2}(\d+)", section)
            n = re.search(r"Rows out:\s*\*{0,2}(\d+)", section)
            if not m or not n:
                if current:
                    warn("counts", f"{rel(p)} current round states no findings-in/rows-out pair")
                continue
            if m.group(1) != n.group(1):
                report("counts", f"{rel(p)} states {m.group(1)} findings in but "
                                 f"{n.group(1)} rows out{where}")
            if not current:
                continue
            actual = count_finding_rows(section)
            if int(n.group(1)) != actual:
                err("counts", f"{rel(p)} states {n.group(1)} rows out but {actual} numbered "
                              f"finding rows are present")


# --------------------------------------------------------------------------- corpus

DIGEST_PATHS = ["calibration/cases", "calibration/CALIBRATION-PROMPT.md",
                "calibration/ANSWER-KEY.md"]


def corpus_digest():
    """Digest the tracked instrument, mirroring calibration/record-template.md."""
    out = subprocess.run(["git", "ls-files", "-z"] + DIGEST_PATHS,
                         cwd=ROOT, capture_output=True)
    files = sorted(f for f in out.stdout.split(b"\0") if f)
    inner = b""
    for f in files:
        h = hashlib.sha1(open(os.path.join(ROOT, f.decode()), "rb").read()).hexdigest()
        inner += f"{h}  {f.decode()}\n".encode()
    return hashlib.sha1(inner).hexdigest()[:12]


def check_calibration_digests():
    """Every filed calibration record's digest matches the current instrument."""
    records = sorted(glob.glob(os.path.join(ROOT, ".adversarial-review", "calibration", "*.md")))
    if not records:
        warn("calibration", "no calibration records on file")
        return
    try:
        actual = corpus_digest()
    except Exception as e:
        warn("calibration", f"could not compute the corpus digest: {e}")
        return
    for r in records:
        text = read(r)
        m = re.search(r"Corpus digest\D+`([0-9a-f]{6,})`", text)
        if not m:
            err("calibration", f"{rel(r)} has no Corpus digest row")
        elif m.group(1) != actual:
            err("calibration", f"{rel(r)} records digest {m.group(1)} but the instrument is "
                               f"{actual} - that record is stale and counts as missing")
        e = re.search(r"\*\*Expires\*\*\s*\|\s*(\d{4}-\d{2}-\d{2})", text)
        if not e:
            err("calibration", f"{rel(r)} has no Expires row")
        elif e.group(1) < __import__("datetime").date.today().isoformat():
            err("calibration", f"{rel(r)} expired {e.group(1)} - a record past its window is "
                               "stale and counts as missing")


# --------------------------------------------------------------------------- install

def check_installed_copies():
    """Where the skills are installed, they match the repository."""
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
    ("current round: every verdict has a disposition", check_ledger_axes),
    ("current round: NO ACTION legality, no bare ACCEPTED", check_no_action_legality),
    ("current round: findings in equals rows out", check_counts),
    ("calibration records match the corpus digest", check_calibration_digests),
    ("installed copies match the repository", check_installed_copies),
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
