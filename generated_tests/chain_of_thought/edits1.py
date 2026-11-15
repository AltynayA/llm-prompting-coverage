import pytest

LETTERS = 'abcdefghijklmnopqrstuvwxyz'


# ---------- Happy path ----------

def test_returns_set_of_strings():
    result = edits1("abc")
    assert isinstance(result, set)
    assert all(isinstance(w, str) for w in result)


def test_deletes_present():
    result = edits1("abc")
    assert "bc" in result
    assert "ac" in result
    assert "ab" in result


def test_transposes_present():
    result = edits1("abc")
    assert "bac" in result
    assert "acb" in result


def test_replaces_present():
    result = edits1("abc")
    assert "xbc" in result
    assert "azc" in result
    assert "abz" in result


def test_inserts_present():
    result = edits1("abc")
    assert "xabc" in result   # beginning
    assert "axbc" in result   # middle
    assert "abxc" in result   # middle
    assert "abcz" in result   # end


def test_original_word_included_via_identity_replacement():
    # replacing a char with itself yields the original word
    assert "hello" in edits1("hello")


def test_distance_two_words_excluded():
    result = edits1("hello")
    assert "heoll" not in result
    assert "hlloe" not in result
    assert "hellooo" not in result
    assert "hll" not in result


def test_hello_specific_edits():
    result = edits1("hello")
    assert "helo" in result      # delete
    assert "ehllo" in result     # transpose
    assert "helol" in result     # transpose
    assert "hallo" in result     # replace
    assert "helloo" in result    # insert
    assert "shello" in result    # insert


def test_result_lengths_within_one_of_input():
    word = "python"
    n = len(word)
    result = edits1(word)
    assert all(n - 1 <= len(w) <= n + 1 for w in result)
    assert any(len(w) == n - 1 for w in result)
    assert any(len(w) == n for w in result)
    assert any(len(w) == n + 1 for w in result)


def test_size_upper_bound():
    for word in ["a", "ab", "abc", "hello"]:
        n = len(word)
        assert len(edits1(word)) <= 54 * n + 25


def test_deterministic_and_input_not_modified():
    word = "test"
    r1 = edits1(word)
    r2 = edits1(word)
    assert r1 == r2
    assert word == "test"


# ---------- Edge cases ----------

def test_empty_string_returns_only_single_letters():
    result = edits1("")
    assert result == set(LETTERS)
    assert len(result) == 26
    assert "" not in result


def test_single_char_exact_result():
    result = edits1("a")
    expected = {""}
    expected |= set(LETTERS)                      # replacements (includes "a")
    expected |= {c + "a" for c in LETTERS}        # inserts before
    expected |= {"a" + c for c in LETTERS}        # inserts after
    assert result == expected
    assert len(result) == 78


def test_single_char_has_no_transposes_and_includes_empty_deletion():
    result = edits1("z")
    assert "" in result
    assert "z" in result


def test_repeated_characters_deduplicated():
    result = edits1("aa")
    assert "a" in result
    assert "aa" in result
    assert "aaa" in result
    assert len(result) < 54 * 2 + 25  # duplicates collapsed by set


def test_uppercase_input_not_normalised():
    result = edits1("A")
    assert "" in result
    assert "aA" in result
    assert "Aa" in result
    assert "A" not in result   # replacements/inserts only use lowercase letters
    assert "a" in result


def test_non_letter_characters_handled():
    result = edits1("a1")
    assert "1a" in result    # transpose
    assert "a" in result     # delete '1'
    assert "1" in result     # delete 'a'
    assert "ab" in result    # replace '1' with 'b'


def test_unicode_characters_handled():
    result = edits1("é")
    assert "" in result
    assert "aé" in result
    assert "éa" in result
    assert "a" in result


def test_whitespace_word():
    result = edits1(" ")
    assert "" in result
    assert "a" in result
    assert "a " in result
    assert " a" in result


# ---------- Error cases ----------

def test_none_raises_type_error():
    with pytest.raises(TypeError):
        edits1(None)


def test_int_raises_type_error():
    with pytest.raises(TypeError):
        edits1(123)


def test_float_raises_type_error():
    with pytest.raises(TypeError):
        edits1(1.5)


def test_list_of_strings_raises_type_error():
    # list slicing works but concatenating list + str fails / results unhashable
    with pytest.raises(TypeError):
        edits1(["a", "b"])
