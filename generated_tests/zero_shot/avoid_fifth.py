import pytest


# ---------- Happy path ----------

def test_no_e_characters_unchanged():
    assert avoid_fifth("python") == "python"


def test_removes_lowercase_e_in_word():
    assert avoid_fifth("hello") == "hllo"


def test_removes_uppercase_E_in_word():
    assert avoid_fifth("HELLO") == "HLLO"


def test_multiple_words_with_e():
    assert avoid_fifth("hello world") == "hllo world"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("bed", "bd"),
        ("eat", "at"),
        ("ex", "x"),
        ("Ex", "x"),
        ("Eagles", "agls"),
    ],
)
def test_e_removed_in_various_positions(text, expected):
    assert avoid_fifth(text) == expected


# ---------- Edge cases ----------

def test_empty_string_returns_empty():
    assert avoid_fifth("") == ""


def test_single_non_e_character():
    assert avoid_fifth("a") == "a"


def test_non_alphabetic_characters_unchanged():
    assert avoid_fifth("xyz 123 !?") == "xyz 123 !?"


def test_consecutive_e_characters_removed():
    assert avoid_fifth("beet") == "bt"


def test_result_has_no_e_for_simple_input():
    result = avoid_fifth("hello world")
    assert "e" not in result.lower()


def test_return_type_is_str():
    assert isinstance(avoid_fifth("cat"), str)


# ---------- Error cases ----------

@pytest.mark.parametrize("text", ["e", "E"])
def test_single_e_raises_index_error(text):
    # Removing the only character leaves an empty string, then new[i - 1] fails
    with pytest.raises(IndexError):
        avoid_fifth(text)


def test_none_input_raises_type_error():
    with pytest.raises(TypeError):
        avoid_fifth(None)


def test_integer_input_raises_type_error():
    with pytest.raises(TypeError):
        avoid_fifth(12345)
