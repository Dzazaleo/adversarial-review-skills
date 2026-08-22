# Independent review — wordcount

Reviewer: Grok 4.6 (xAI), Grok Build TUI.
Target: this directory — `wordcount.py` (21 lines), `test_wordcount.py` (21 lines), `README.md`, `BRIEF.md`.

## Result

Nothing worth reporting. The implementation matches the contract it states, the tests would fail under the nearby-wrong implementations I tried, and the CLI path does what the README shows.

I looked for a wrong count, an unfalsifiable test, and a CLI that tests do not actually exercise. I did not find a user-visible defect.

## Claims checked

`wordcount.py` asserts, in the module docstring, the `count_words` docstring, and `README.md`:

1. Whitespace-separated tokens; runs of any whitespace (space, tab, newline) are one separator.
2. Leading and trailing whitespace contribute nothing.
3. Empty input is 0.
4. Punctuation is not a separator (test name: stays attached to its token).
5. The program reads stdin and prints that count.

Implementation is `len(text.split())` with no arguments — Python's Unicode-whitespace split, which is the standard realization of (1)–(4). `main` is `print(count_words(sys.stdin.read())); return 0`.

## Execution

Suite, from this directory:

```
python3 -m pytest -v --cache-clear test_wordcount.py
```

5 passed (`test_counts_space_separated_words`, `test_empty_input_is_zero`, `test_whitespace_only_is_zero`, `test_runs_of_whitespace_do_not_inflate_the_count`, `test_punctuation_stays_attached_to_its_token`).

CLI, same process that `if __name__ == "__main__"` uses:

| input | output |
|---|---|
| `echo "one two three"` (README example) | `3` |
| empty stdin | `0` |
| `   \t\n  ` | `0` |
| `  a\t\tb\n\nc  ` | `3` |
| `hello, world!` | `2` |
| `one two three` with no trailing newline | `3` |

`main()` captured via `io.StringIO` on stdin/stdout: exit `0`, stdout `f"{n}\n"`, matching `count_words` on the same string. Importing `wordcount` does not read stdin or print.

`str.split()` on the test vectors: `""` → `[]`, `"   \t\n  "` → `[]`, `"  a\t\tb\n\nc  "` → `['a','b','c']`, `"hello, world!"` → `['hello,','world!']`.

Also probed, not claimed by the work: CR, CRLF, form-feed, vertical tab, NBSP, em-space, ZWSP, Unicode words, hyphen, apostrophe. All consistent with `str.split()` / `str.isspace()`. ZWSP is not whitespace in Python, so `"a\u200bb"` is one token.

## Would the tests fail if the claim were false?

The brief forbids signing a test off by quoting its name. I ran the five assertions against stand-in implementations (no file was edited):

| stand-in | suite |
|---|---|
| `len(text.split())` (actual) | all pass |
| `len(text.split(" "))` | fails empty, whitespace-only, runs-of-whitespace |
| `len(text.strip().split(" "))` if non-empty else 0 | fails runs-of-whitespace (`"  a\t\tb\n\nc  "` is not three space-separated fields) |
| `len(text.splitlines())` | fails several |
| always `0` / always `3` / `len(text)` / `text.count(" ")` / `int(bool(text.strip()))` | each fails at least one test |

So the empty, whitespace-only, and mixed-whitespace tests are real constraints, not tautologies. A split-on-space-only bug would not survive.

Two stand-ins *do* pass the whole suite: `len(re.findall(r'\S+', text))` (same token rule as `split()`) and `len(re.findall(r'\w+', text))`. The latter is a different tokenizer (punctuation and hyphens become breaks: `"hello,world"` and `"don't"` count as 2 instead of 1). The punctuation test uses `"hello, world!"` — a space already separates the two words — so the count is 2 whether the comma stays on `hello` or is stripped. The function only returns a count, so that input cannot observe attachment.

That is a gap in how strongly the *name* `test_punctuation_stays_attached_to_its_token` is enforced, not a bug in `count_words`: the docstring's rule is whitespace-separated tokens, `split()` implements it, and the test still fails if a comma produced an extra token on that string. I am not filing it.

The suite never calls `main` or stdin. A CLI that ignored stdin would still collect 5 passes. I treated that as a hole to close by running the script, not as a defect in the script. The README example and the captured-`main` checks above close it.

## Candidates considered and discarded

- **README says `python`, this host has only `python3`.** Documentation convention; the test stanza already uses `python3`. Not a defect in the program.
- **No shebang / not executable.** Invocation in the README is `python wordcount.py`.
- **Full-stdin `read()`.** Matches the stated tool; no bound is claimed.
- **Default text-mode decoding.** Binary stdin is outside the contract.
- **Always exit 0.** There is no specified error path.

## Coverage

Covered: `wordcount.py` (`count_words`, `main`, `__main__` guard), `test_wordcount.py` (all five tests, including whether they fail under wrong implementations), `README.md` example and claimed interface, stdin CLI path.

Did not reach: a second Python implementation / `python` binary (absent here), and any environment where `sys.stdin` encoding is not UTF-8.

No findings.
