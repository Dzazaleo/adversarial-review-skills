from wordcount import count_words


def test_counts_space_separated_words():
    assert count_words("one two three") == 3


def test_empty_input_is_zero():
    assert count_words("") == 0


def test_whitespace_only_is_zero():
    assert count_words("   \t\n  ") == 0


def test_runs_of_whitespace_do_not_inflate_the_count():
    assert count_words("  a\t\tb\n\nc  ") == 3


def test_punctuation_stays_attached_to_its_token():
    assert count_words("hello, world!") == 2
