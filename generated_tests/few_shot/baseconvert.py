import pytest

HEX = "0123456789abcdef"
BIN = "01"
DEC = "0123456789"


def test_baseconvert_default_digits_single_digit():
    assert baseconvert(0, 1) == "A"
    assert baseconvert(1, 1) == "C"
    assert baseconvert(5, 1) == "G"
    assert baseconvert(19, 1) == "Y"


def test_baseconvert_default_digits_multi_digit():
    # default alphabet has 20 symbols, so 20 -> "CA"
    assert baseconvert(20, 1) == "CA"
    assert baseconvert(21, 1) == "CC"
    # 400 = 1*400 -> "CAA"
    assert baseconvert(400, 1) == "CAA"


def test_baseconvert_custom_digits():
    assert baseconvert(255, 1, digits=HEX) == "ff"
    assert baseconvert(5, 1, digits=BIN) == "101"
    assert baseconvert(123, 1, digits=DEC) == "123"
    assert baseconvert(0, 1, digits=BIN) == "0"


def test_baseconvert_padding():
    assert baseconvert(0, 4) == "AAAA"
    assert baseconvert(5, 3) == "AAG"
    assert baseconvert(5, 8, digits=BIN) == "00000101"


def test_baseconvert_k_smaller_than_length_no_truncation():
    assert baseconvert(255, 2, digits=BIN) == "11111111"
    assert baseconvert(255, 2, digits=HEX) == "ff"
    assert baseconvert(255, 0, digits=HEX) == "ff"


def test_baseconvert_input_coercion():
    assert baseconvert("10", 1, digits=BIN) == "1010"
    assert baseconvert(7.9, 1, digits=BIN) == "111"
    assert baseconvert("255", 1, digits=HEX) == "ff"


def test_baseconvert_empty_digits_uses_default():
    assert baseconvert(5, 1, digits="") == "G"
    assert baseconvert(5, 1, digits=None) == "G"


def test_baseconvert_max_base_36():
    digits36 = "0123456789abcdefghijklmnopqrstuvwxyz"
    assert baseconvert(35, 1, digits=digits36) == "z"
    assert baseconvert(36, 1, digits=digits36) == "10"


def test_baseconvert_invalid_number_returns_empty():
    assert baseconvert("abc", 1) == ""
    assert baseconvert(None, 1) == ""
    assert baseconvert([1, 2], 1) == ""


def test_baseconvert_negative_returns_empty():
    assert baseconvert(-1, 1) == ""
    assert baseconvert(-100, 3, digits=HEX) == ""
    # returns before k is ever compared
    assert baseconvert(-1) == ""


def test_baseconvert_invalid_base_returns_empty():
    # base of 1 is too small
    assert baseconvert(5, 1, digits="0") == ""
    # base of 37 is too large
    digits37 = "0123456789abcdefghijklmnopqrstuvwxyz!"
    assert len(digits37) == 37
    assert baseconvert(5, 1, digits=digits37) == ""


def test_baseconvert_k_none_raises_type_error():
    # default k=None is compared with an int, which fails in Python 3
    with pytest.raises(TypeError):
        baseconvert(5)
