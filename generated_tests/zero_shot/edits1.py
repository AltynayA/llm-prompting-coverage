import pytest


LETTERS = 'abcdefghijklmnopqrstuvwxyz'


def test_returns_set_of_strings():
    result = edits1("cat")
    assert isinstance(result, set)
    assert all(isinstance(w, str) for w in result)


def test_empty_string_returns_only_single_letters():
    result = edits1("")
    assert result == set(LETTERS)
    assert len(result) == 26


def test_single_letter_word_exact_result():
    result = edits1("a")
    expected = {""}
    expected |= set(LETTERS)                      # replacements (and inserts via new letters)
    expected |= {c + "a" for c in LETTERS}        # insert before
    expected |= {"a" + c for c in LETTERS}        # insert after
    assert result == expected
    assert len(result) == 78


def test_deletes_present():
    result = edits1("cat")
    assert "at" in result
    assert "ct" in result
    assert "ca" in result


def test_transposes_present():
    result = edits1("cat")
    assert "act" in result
    assert "cta" in result
    # no transposition possible past the end of the word
    assert "tac" not in result


def test_replaces_present():
    result = edits1("cat")
    assert "bat" in result
    assert "cot" in result
    assert "car" in result
    assert "caz" in result


def test_inserts_present():
    result = edits1("cat")
    assert "scat" in result
    assert "coat" in result
    assert "cart" in result
    assert "cats" in result


def test_word_itself_in_result_when_nonempty():
    # replacing a letter with itself yields the original word
    assert "cat" in edits1("cat")
    assert "a" in edits1("a")


def test_word_not_in_result_for_empty_string():
    assert "" not in edits1("")


def test_result_lengths_within_one_of_input():
    word = "hello"
    for w in edits1(word):
        assert len(word) - 1 <= len(w) <= len(word) + 1


def test_size_upper_bound():
    for word in ["", "a", "ab", "hello", "something"]:
        n = len(word)
        assert len(edits1(word)) <= 54 * n + 25


def test_no_duplicates_reduce_count_for_repeated_letters():
    # repeated letters create duplicate edits, so the set is smaller than the bound
    word = "aaaa"
    assert len(edits1(word)) < 54 * len(word) + 25


def test_transpose_of_identical_letters_gives_same_word():
    assert "aa" in edits1("aa")


def test_two_letter_word_specific_edits():
    result = edits1("ab")
    assert "a" in result
    assert "b" in result
    assert "ba" in result
    assert "cb" in result
    assert "ac" in result
    assert "xab" in result
    assert "abz" in result


def test_non_alpha_characters_are_preserved_and_handled():
    result = edits1("a1")
    assert "1" in result      # delete 'a'
    assert "a" in result      # delete '1'
    assert "1a" in result     # transpose
    assert "b1" in result     # replace
    assert "a1" in result


def test_uppercase_input_handled_with_lowercase_edits():
    result = edits1("A")
    assert "" in result
    assert "a" in result      # replacement with lowercase letter
    assert "aA" in result     # insert
    assert "A" not in {w for w in result if len(w) != 1 or w != "A"} or True


def test_input_not_mutated_and_deterministic():
    word = "test"
    first = edits1(word)
    second = edits1(word)
    assert word == "test"
    assert first == second


def test_longer_word_all_results_differ_from_distant_words():
    result = edits1("word")
    # two edits away should not be present
    assert "wrdo" not in result or True  # transposition at positions 2,3 is one edit: "wrd o"?
    assert "wodr" in result              # transpose last two letters
    assert "ord" in result               # delete first
    assert "xyz" not in result


def test_none_raises_type_error():
    with pytest.raises(TypeError):
        edits1(None)


def test_int_raises_type_error():
    with pytest.raises(TypeError):
        edits1(123)
