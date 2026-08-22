# Independent review

## Summary

Scope read: `BRIEF.md`, `README.md`, `wordcount.py`, and `test_wordcount.py`.

One low-impact documentation defect was confirmed. I found no defect in the counting implementation.
With the available `python3` interpreter, all five supplied tests passed. Independently of those
tests, I compared `count_words` with a transition-based word-count oracle over 111,111 generated
inputs containing ordinary characters, all ASCII whitespace classes, non-breaking space, and em
space. I also invoked the CLI separately and checked its count, trailing newline, empty stderr, and
zero exit status.

## Findings

### Low impact — documented commands require a missing executable

- **Location:** `README.md:6` and `README.md:10`
- **Mechanism:** Both usage instructions invoke `python`, without detecting it or documenting
  `python3` as an alternative. The reviewed environment has no `python` executable.
- **Trigger:** A user follows either command on a system that exposes Python 3 only as `python3`,
  including this review environment.
- **Consequence:** The example and documented test command fail immediately with
  `zsh: command not found: python`; users cannot run the tool or its tests as documented.
- **Status:** **CONFIRMED** — I ran both documented command forms in the supplied environment and
  observed exit status 127.

Coverage: read every supplied file; exercised the supplied suite, function-level tokenization and
edge cases, and stdin/stdout CLI behavior under `python3`; did not test other operating systems,
Python versions, resource exhaustion, or undecodable stdin bytes.
