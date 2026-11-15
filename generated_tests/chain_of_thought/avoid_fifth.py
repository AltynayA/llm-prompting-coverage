import pytest


# Analysis summary (kept as comments):
# - The function intends to strip 'e'/'E' from a string, using two passes.
# - Strings with no 'e'/'E' are returned unchanged (nothing is ever modified).
# - 'e'/'E' in the interior of a string (not last char) is removed.
# - Because of the new[i - 1] lookup (index -1 wraps to the last char), a string
#   ending in 'e' gets corrupted (e.g. "ae" -> "aa"), and a string that shrinks to
#   empty during the loop raises IndexError (e.g. "e").
# - Non-string input (None, int) raises TypeError at len().


def test_empty_string_returns_empty():
    assert avoid_fifth("") == ""


@pytest.mark.parametrize("text", ["abc", "xyz 123", "Python!", "a", "   ", "12345"])
def test_strings_without_e_unchanged(text):
    assert avoid_fifth(text) == text


def test_lowercase_e_in_middle_removed():
    assert avoid_fifth("hello") == "hllo"


def test_uppercase_E_in_middle_removed():
    assert avoid_fifth("HELLO") == "HLLO"


def test_mixed_case_sentence():
    assert avoid_fifth("Hello World") == "Hllo World"


def test_leading_e_removed():
    assert avoid_fifth("ea") == "a"
    assert avoid_fifth("elephant") == "lphant"


def test_consecutive_es_in_middle_removed():
    assert avoid_fifth("beet") == "bt"
    assert avoid_fifth("eel") == "l"


def test_result_is_string_and_no_e_in_normal_case():
    result = avoid_fifth("elephant")
    assert isinstance(result, str)
    assert "e" not in result and "E" not in result


def test_trailing_e_quirk_wraps_around():
    # Documented buggy behaviour: new[-1] lookup at i=0 duplicates content
    assert avoid_fifth("ae") == "aa"


@pytest.mark.parametrize("text", ["e", "E"])
def test_single_e_raises_index_error(text):
    with pytest.raises(IndexError):
        avoid_fifth(text)


def test_all_e_string_raises_index_error():
    with pytest.raises(IndexError):
        avoid_fifth("EEE")


@pytest.mark.parametrize("bad", [None, 123, 4.5, ["e"]])
def test_non_string_input_raises_type_error(bad):
    with pytest.raises(TypeError):
        avoid_fifth(bad)
