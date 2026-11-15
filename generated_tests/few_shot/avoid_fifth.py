import pytest


def test_avoid_fifth_normal_lowercase():
    assert avoid_fifth("hello") == "hllo"
    assert avoid_fifth("bed") == "bd"


def test_avoid_fifth_normal_uppercase():
    assert avoid_fifth("HELLO") == "HLLO"
    assert avoid_fifth("Hello") == "Hllo"


def test_avoid_fifth_sentence_with_spaces():
    assert avoid_fifth("the cat") == "th cat"
    assert avoid_fifth("Hello World") == "Hllo World"


def test_avoid_fifth_no_e_unchanged():
    assert avoid_fifth("python") == "python"
    assert avoid_fifth("xyz 123") == "xyz 123"


def test_avoid_fifth_consecutive_e_in_middle():
    assert avoid_fifth("beef") == "bf"


def test_avoid_fifth_edge_empty_string():
    assert avoid_fifth("") == ""


def test_avoid_fifth_edge_single_non_e_char():
    assert avoid_fifth("a") == "a"


def test_avoid_fifth_edge_single_e_raises_index_error():
    with pytest.raises(IndexError):
        avoid_fifth("e")
    with pytest.raises(IndexError):
        avoid_fifth("E")


def test_avoid_fifth_error_non_string_input():
    with pytest.raises(TypeError):
        avoid_fifth(None)
    with pytest.raises(TypeError):
        avoid_fifth(123)
