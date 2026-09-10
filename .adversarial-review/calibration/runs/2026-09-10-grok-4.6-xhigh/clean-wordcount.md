# Independent review — wordcount

Reviewer: Grok 4.6 (xAI). Work under review: `wordcount.py`, `test_wordcount.py`, `README.md`. `BRIEF.md` is the audit brief, not the work.

No ranked findings. The implementation matches the contract it states. What follows is the search that makes that admissible rather than agreement with the author.

## Ranked findings

None.

## Claims, checked independently

Author comments, docstrings, test names, and green tests are treated as claims, not proof. Each item below was re-derived from the implementation and from inputs I supplied, not from quoting the suite.

| Claim | Where | What I did | Result |
|---|---|---|---|
| Whitespace-separated count of `"one two three"` is 3 | README:5–7, `count_words` | `count_words('one two three')`; `python3 wordcount.py` on `b'one two three\n'` | `3` and stdout `b'3\n'`, exit 0 |
| Empty input is 0 | docstring L10, test name | `count_words('')`; `printf '' \| python3 wordcount.py`; stdin `DEVNULL` | 0, exit 0 |
| Leading/trailing whitespace contribute nothing; whitespace-only is 0 | docstring L8–10 | `count_words('   \t\n  ')`; same bytes through the CLI | 0 |
| Runs of mixed whitespace do not inflate | docstring L8–9, test L16–17 | `count_words("  a\t\tb\n\nc  ")` | 3 (`a`,`b`,`c`) |
| Punctuation stays attached | test L20–21 | `count_words("hello, world!")` | 2 |
| `str.split()` with no args is the whole function | `wordcount.py:12` | Compared to `split(' ')` on the same fixtures | `split(' ')` yields `['']` on empty and inflates the mixed-whitespace fixture; the shipped call does not |
| Multiplicity, not unique tokens | implied by “count” | `count_words('a a a')` and `printf 'a a a\n' \| python3 wordcount.py` | 3, not 1 |
| Every Unicode `str.isspace()` character is a separator | “any whitespace”, L8 | For all 29 code points with `isspace() True` (U+0000..U+10FFFF), `count_words('a'+c+'b')==2` and `count_words(c*3)==0` | 0 mismatches |
| CLI is `print(count_words(sys.stdin.read()))` then exit 0 | `wordcount.py:15–20` | Ran the script; also called `main()` with `StringIO('one two three')` | prints `3\n`, returns 0 |
| No third-party imports | README L3, source | Read `wordcount.py` | only `sys` |

## Would the tests fail if the claim were false?

`python3 -m pytest -v` from this directory: 5 collected, 5 passed, pytest 9.0.2, Python 3.14.3. The imported module was `/Users/leo/grok-calibration-xhigh/4-clean-wordcount/wordcount.py` (no site-packages shadow).

- `test_empty_input_is_zero` and `test_whitespace_only_is_zero` **would fail** if `count_words` used `str.split(' ')` (`''.split(' ') == ['']`; the whitespace-only fixture splits into empty strings and a `\t\n` token). Those two tests actually police the separator algorithm.
- `test_counts_space_separated_words` **would fail** an off-by-one or a line-count implementation (`"one two three"` as one line). It **would not fail** `len(set(text.split()))`: every fixture uses distinct tokens. I did not treat that as a product defect; the shipped body is `len(text.split())`, and `'a a a'` is 3 when executed.
- `test_runs_of_whitespace_do_not_inflate_the_count` **would fail** `split(' ')` on `"  a\t\tb\n\nc  "` (that call returns `['', '', 'a\t\tb\n\nc', '', '']`, length 5, not 3).
- `test_punctuation_stays_attached_to_its_token` **would fail** if commas/bangs were treated as separators. It does not prove word-character class beyond that one string.
- None of the tests import `main`, read stdin, or spawn the script. A broken CLI with an intact `count_words` would still be green. I ran the CLI myself (empty, whitespace-only, no trailing newline, multi-line, duplicates, form-feed/vertical-tab, README bytes). It matched `count_words`. That is a suite hole, not a wrong number from the program as written.

## Hypotheses that did not become findings

**wc(1) disagreement on exotic separators.** Under both `C.UTF-8` and `en_US.UTF-8`, macOS `wc -w` counts `a\x1cb`, `a\u0085b`, `a\u2003b`, `a\u3000b`, `a\u2028b` as **one** word; this program counts **two**. The program never claims POSIX `wc` identity. It claims whitespace-separated tokens; CPython `str.split()` / `str.isspace()` is that claim (C0 0x1C–0x1F are whitespace because their Unicode bidi classes are B/S). Ranking a Python Unicode split against BSD `iswspace` would be inventing a contract. Common cases (space, tab, CR, LF, FF, VT, NBSP, ZWSP, BOM-only, duplicates, punctuation, missing final newline) **matched** `wc -w`.

**UTF-8 BOM-only stdin → 1.** Confirmed (`b'\xef\xbb\xbf'` → `1`). `wc -w` also prints 1. Default stdin codec is `utf-8` with `surrogateescape`, not `utf-8-sig`, so U+FEFF is a token. Not a divergence from the platform word counter, and not a documented empty file.

**Invalid byte / non-UTF-8 stdin.** Default: `b'hello \xff world\n'` → exit 0, count 3 (surrogateescape turns `0xFF` into a token). With `PYTHONIOENCODING=utf-8:strict`, same bytes raise `UnicodeDecodeError` from `sys.stdin.read()` at L16 and exit 1. With `ascii:strict`, UTF-8 `café` does the same. That is the interpreter’s TextIOWrapper, not a logic error in `count_words`. The tool does not claim to count binary.

**Slurping all of stdin.** L16 is one `read()`. A large stream can OOM where a streaming counter would not. The documented interface is a 21-line stdin filter with no size claim. Not ranked.

**Extra argv ignored.** `python3 wordcount.py /etc/passwd <<< 'a b c'` prints `3` and does not read the file. README specifies stdin only. Not ranked.

**README example uses `python`.** On this host `python` is not on `PATH`; `python3` is. Line 10 of the same README already says `python3 -m pytest`. Environment, not a wrong count.

**Broken pipe.** `python3 wordcount.py | head -n 0` surfaces `BrokenPipeError` while flushing stdout (CPython default). Same class of issue as any `print` CLI; the count path had already finished.

**Library type holes.** `count_words(None)` / `count_words(123)` raise `AttributeError`. `count_words(b'a b')` returns 2 because `bytes.split()` also splits on ASCII whitespace. CLI always passes `str`. No typed public API is advertised beyond the function.

## Coverage

Read every file in the tree (`wordcount.py` 21 lines, `test_wordcount.py` 21, `README.md` 10, plus the brief). Ran `python3 -m pytest -v` (5/5 passed). Exercised `count_words` and the CLI on empty, whitespace-only, mixed runs, punctuation, duplicates, C0/C1 controls, all 29 Unicode whitespace code points, ZWSP and other non-space lookalikes, UTF-8 BOM, invalid bytes under default and strict encodings, closed stdin, `python3 -m wordcount`, and comparison with `wc -w`. Confirmed no second `wordcount` module on `sys.path`.

Did not reach: Windows/locale code pages, a stream large enough to OOM, mutating the suite (envelope forbids changing files that were already here), or any machine other than this macOS / Python 3.14.3 host.
