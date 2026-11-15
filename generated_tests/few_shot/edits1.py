import pytest


def test_edits1_returns_set():
    result = edits1("cat")
    assert isinstance(result, set)
    assert all(isinstance(w, str) for w in result)


def test_edits1_normal_contains_each_edit_type():
    result = edits1("cat")
    # deletes
    assert {"at", "ct", "ca"} <= result
    # transposes
    assert {"act", "cta"} <= result
    # replaces
    assert "cut" in result
    assert "cab" in result
    assert "bat" in result
    # inserts
    assert "cart" in result
    assert "cats" in result
    assert "scat" in result


def test_edits1_lengths_within_one():
    word = "hello"
    result = edits1(word)
    assert all(len(word) - 1 <= len(w) <= len(word) + 1 for w in result)


def test_edits1_empty_string():
    result = edits1("")
    assert result == set("abcdefghijklmnopqrstuvwxyz")
    assert len(result) == 26


def test_edits1_single_char():
    result = edits1("a")
    assert "" in result
    assert "a" in result  # replacing with the same letter
    assert "b" in result
    assert "aa" in result
    assert "ba" in result
    assert "ab" in result
    assert len(result) == 78


def test_edits1_two_chars_exact_count():
    result = edits1("ab")
    assert len(result) == 130
    assert "ba" in result
    assert "a" in result and "b" in result
    assert "aab" in result and "abb" in result


def test_edits1_repeated_letters_deduplicated():
    result = edits1("aa")
    # transposing identical letters yields the same word; set has no duplicates
    assert "aa" in result
    assert "aaa" in result
    assert "a" in result
    assert len(result) == len(set(result))


def test_edits1_excludes_distance_two_and_non_letters():
    result = edits1("cat")
    assert "dog" not in result
    assert "ca" in result and "c" not in result
    assert "tac" not in result  # requires more than one edit
    assert all(ch in "abcdefghijklmnopqrstuvwxyz" for w in result for ch in w)


def test_edits1_uppercase_input_preserved_and_lowercase_inserted():
    result = edits1("Ab")
    assert "b" in result
    assert "A" in result
    assert "bA" in result
    assert "Aab" in result
    assert "Ab" not in {w for w in result if w != "Ab"}


def test_edits1_error_none():
    with pytest.raises(TypeError):
        edits1(None)


def test_edits1_error_int():
    with pytest.raises(TypeError):
        edits1(123)
