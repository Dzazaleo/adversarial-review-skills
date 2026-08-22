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
ERRORS, WARNS = [], []


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
        warn("frontmatter", "PyYAML not installed - skipped")
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
        granted = set(fm.get("allowed-tools") or [])
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
            target = os.path.normpath(os.path.join(os.path.dirname(f), m.group(1).strip()))
            if not os.path.exists(target):
                err("links", f"{rel(f)} -> {m.group(1).strip()} does not resolve")


# --------------------------------------------------------------------------- ledger

VERDICTS = ("CONFIRMED", "REFUTED", "COULD NOT DETERMINE", "SETTLED ALREADY",
            "OWNER RULING REQUIRED")
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
            in_code, count = False, 0
            for ch in line:
                if ch == "`":
                    in_code = not in_code
                elif ch == "|" and in_code:
                    count += 1
            if count:
                report = err if i > cur_line else warn
                where = "" if i > cur_line else " (closed round - append-only, cannot be repaired)"
                report("table", f"{rel(p)}:{i} has {count} unescaped pipe(s) inside inline "
                                f"code; the row will render with extra columns{where}")


VERDICT_RE = re.compile(r"\*\*(" + "|".join(re.escape(v) for v in VERDICTS) + r")")


def is_ruling_row(line):
    """A ruling row carries a **bolded** verdict. Prose that merely names one does not."""
    return bool(VERDICT_RE.search(line))


def last_round(text):
    """The final '# Round N' section, or the whole file if there are no round headings."""
    marks = [m.start() for m in re.finditer(r"^# Round \d+", text, re.M)]
    return text[marks[-1]:] if marks else text


def check_ledger_axes():
    """In the current round, every row carrying a verdict also carries a disposition."""
    for p in ledger_paths():
        section = last_round(read(p))
        for i, line in table_rows(section):
            if not is_ruling_row(line):
                continue
            if not any(d in line for d in DISPOSITIONS):
                err("two-axes", f"{rel(p)} row '{line[:44].strip()}...' has a verdict "
                                "but no disposition")


def check_no_action_legality():
    """NO ACTION is legal only under REFUTED or SETTLED ALREADY; no bare ACCEPTED."""
    for p in ledger_paths():
        section = last_round(read(p))
        for i, line in table_rows(section):
            if not is_ruling_row(line):
                continue
            if "NO ACTION" in line and not re.search(r"\*\*(REFUTED|SETTLED ALREADY)", line):
                err("disposition", f"{rel(p)} row '{line[:44].strip()}...' pairs NO ACTION "
                                   "with a verdict that does not permit it")
            if re.search(r"\*\*ACCEPTED\*\*(?!\s*AS-IS)", line):
                err("disposition", f"{rel(p)} row '{line[:44].strip()}...' uses a bare "
                                   "'ACCEPTED' - it means both 'real' and 'shipping with it'")


def check_counts():
    """The current round's stated findings-in equals its stated rows-out."""
    for p in ledger_paths():
        section = last_round(read(p))
        m = re.search(r"Findings in:\s*\*{0,2}(\d+)", section)
        n = re.search(r"Rows out:\s*\*{0,2}(\d+)", section)
        if not m or not n:
            warn("counts", f"{rel(p)} current round states no findings-in/rows-out pair")
            continue
        if m.group(1) != n.group(1):
            err("counts", f"{rel(p)} states {m.group(1)} findings in but {n.group(1)} rows out")


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
        m = re.search(r"Corpus digest\D+`([0-9a-f]{6,})`", read(r))
        if not m:
            warn("calibration", f"{rel(r)} has no Corpus digest row")
            continue
        if m.group(1) != actual:
            warn("calibration", f"{rel(r)} records digest {m.group(1)} but the instrument is "
                                f"{actual} - that record is stale and counts as missing")


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
]


def main():
    if "--list" in sys.argv:
        for name, _ in CHECKS:
            print(f"  {name}")
        return 0
    ran = set()
    for _, fn in CHECKS:
        if fn not in ran:
            fn()
            ran.add(fn)
    for w in WARNS:
        print(f"WARN  {w}")
    for e in ERRORS:
        print(f"ERROR {e}")
    if ERRORS:
        print(f"\n{len(ERRORS)} error(s), {len(WARNS)} warning(s)")
        return 1
    print(f"All {len(ran)} checks pass" + (f" ({len(WARNS)} warning(s))" if WARNS else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
