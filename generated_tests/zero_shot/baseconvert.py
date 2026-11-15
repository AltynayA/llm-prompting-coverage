import pytest


HEX = "0123456789abcdef"
DEFAULT_DIGITS = "ACDEFGHIKLMNPQRSTVWY"


def test_default_digits_single_digit_values():
    assert baseconvert(0, 1) == "A"
    assert baseconvert(1, 1) == "C"
    assert baseconvert(10, 1) == "M"
    assert baseconvert(19, 1) == "Y"


def test_default_digits_multi_digit_values():
    assert baseconvert(20, 1) == "CA"
    assert baseconvert(399, 1) == "YY"
    assert baseconvert(400, 1) == "CAA"


def test_custom_digits_hex_and_binary():
    assert baseconvert(255, 1, digits=HEX) == "ff"
    assert baseconvert(16, 1, digits=HEX) == "10"
    assert baseconvert(5, 1, digits="01") == "101"
    assert baseconvert(1023, 1, digits="01") == "1" * 10


def test_padding_with_k():
    assert baseconvert(0, 4) == "AAAA"
    assert baseconvert(5, 5, digits="01") == "00101"
    assert baseconvert(1, 3) == "AAC"


def test_k_smaller_or_equal_than_length_does_not_truncate():
    assert baseconvert(399, 1) == "YY"
    assert baseconvert(399, 2) == "YY"
    assert baseconvert(399, 0) == "YY"
    assert baseconvert(399, -5) == "YY"


def test_input_coercion_to_int():
    assert baseconvert("10", 1) == "M"
    assert baseconvert(7.9, 1) == "I"
    assert baseconvert("255", 1, digits=HEX) == "ff"


def test_empty_digits_falls_back_to_default():
    assert baseconvert(10, 1, digits="") == "M"
    assert baseconvert(10, 1, digits=None) == "M"


def test_negative_n_returns_empty_string():
    assert baseconvert(-1, 1) == ""
    assert baseconvert(-100, 3, digits=HEX) == ""
    # returns before k is ever compared
    assert baseconvert(-1) == ""


def test_invalid_n_returns_empty_string():
    assert baseconvert("abc", 1) == ""
    assert baseconvert(None, 1) == ""
    assert baseconvert("", 1) == ""
    assert baseconvert([1, 2], 1) == ""
    assert baseconvert(None) == ""


def test_invalid_base_returns_empty_string():
    # base 1 is too small
    assert baseconvert(5, 1, digits="0") == ""
    # base 37 is too large
    assert baseconvert(5, 1, digits="abcdefghijklmnopqrstuvwxyz0123456789!") == ""


def test_boundary_bases_are_allowed():
    # base 2
    assert baseconvert(2, 1, digits="ab") == "ba"
    # base 36
    digits36 = "0123456789abcdefghijklmnopqrstuvwxyz"
    assert len(digits36) == 36
    assert baseconvert(35, 1, digits=digits36) == "z"
    assert baseconvert(36, 1, digits=digits36) == "10"


def test_k_none_raises_type_error_for_valid_input():
    # default k=None is compared with an int length, which fails in Python 3
    with pytest.raises(TypeError):
        baseconvert(5)
    with pytest.raises(TypeError):
        baseconvert(0, None)
