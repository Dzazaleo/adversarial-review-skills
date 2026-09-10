"""wordcount — count whitespace-separated words read from stdin."""

import sys


def count_words(text: str) -> int:
    """Return the number of whitespace-separated tokens in text.

    Runs of any whitespace (spaces, tabs, newlines) separate tokens, and
    leading or trailing whitespace contributes nothing. Empty input is 0.
    """
    return len(text.split())


def main() -> int:
    # Decode as UTF-8 rather than the interpreter's default, which follows the
    # host's codepage: the count must not depend on the platform it runs on.
    print(count_words(sys.stdin.buffer.read().decode("utf-8")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
