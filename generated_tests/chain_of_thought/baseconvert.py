import pytest

BIN = "01"
HEX = "0123456789abcdef"


def test_zero_default_digits():
    assert baseconvert(0, 1) == "A"


def test_single_digit_default_alphabet():
    assert baseconvert(1, 1) == "C"
    assert baseconvert(19, 1) == "Y"


def test_multi_digit_default_alphabet():
    assert baseconvert(20, 1) == "CA"
    assert baseconvert(21, 1) == "CC"
    assert baseconvert(400, 1) == "CAA"


def test_custom_digits_binary_and_hex():
    assert baseconvert(5, 0, BIN) == "101"
    assert baseconvert(255, 0, BIN) == "11111111"
    assert baseconvert(255, 0, HEX) == "ff"
    assert baseconvert(0, 0, HEX) == "0"


def test_padding_with_k():
    assert baseconvert(1, 4) == "AAAC"
    assert baseconvert(5, 8, BIN) == "00000101"
    assert baseconvert(0, 3) == "AAA"


def test_k_smaller_than_length_no_truncation():
    assert baseconvert(255, 2, BIN) == "11111111"
    assert baseconvert(20, 1) == "CA"
    assert baseconvert(20, 2) == "CA"


def test_k_exactly_length():
    assert baseconvert(5, 3, BIN) == "101"


def test_negative_returns_empty():
    assert baseconvert(-1, 1) == ""
    assert baseconvert(-100, 5, BIN) == ""


def test_non_numeric_n_returns_empty():
    assert baseconvert("abc", 1) == ""
    assert baseconvert(None, 1) == ""
    assert baseconvert([], 1) == ""
    assert baseconvert("", 1) == ""


def test_numeric_string_and_float_n_are_coerced():
    assert baseconvert("5", 0, BIN) == "101"
    assert baseconvert(5.9, 0, BIN) == "101"


def test_invalid_base_returns_empty():
    # base 1 (<2)
    assert baseconvert(5, 1, "A") == ""
    # base 37 (>36)
    assert baseconvert(5, 1, "abcdefghijklmnopqrstuvwxyz0123456789!") == ""


def test_max_base_36_allowed():
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    assert baseconvert(35, 1, digits) == "z"
    assert baseconvert(36, 1, digits) == "10"


def test_empty_digits_uses_default():
    assert baseconvert(1, 1, "") == "C"
    assert baseconvert(1, 1, None) == "C"


def test_k_none_with_valid_n_raises_type_error():
    # len(s) < None is invalid in Python 3
    with pytest.raises(TypeError):
        baseconvert(5)
    with pytest.raises(TypeError):
        baseconvert(5, None, BIN)


def test_invalid_input_returns_empty_even_without_k():
    # early returns happen before the k comparison
    assert baseconvert(-1) == ""
    assert baseconvert("xyz") == ""
    assert baseconvert(5, None, "A") == ""
