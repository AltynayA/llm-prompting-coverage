import pytest


def test_filesizeformat_single_byte():
    assert do_filesizeformat(1) == "1 Byte"
    assert do_filesizeformat(1.0) == "1 Byte"
    assert do_filesizeformat("1") == "1 Byte"


def test_filesizeformat_small_values_decimal():
    assert do_filesizeformat(0) == "0 Bytes"
    assert do_filesizeformat(2) == "2 Bytes"
    assert do_filesizeformat(100) == "100 Bytes"
    assert do_filesizeformat(999) == "999 Bytes"


def test_filesizeformat_small_values_binary():
    assert do_filesizeformat(0, binary=True) == "0 Bytes"
    assert do_filesizeformat(1, binary=True) == "1 Byte"
    assert do_filesizeformat(1023, binary=True) == "1023 Bytes"


def test_filesizeformat_string_and_float_input():
    assert do_filesizeformat("100") == "100 Bytes"
    assert do_filesizeformat(1.5) == "1 Bytes"
    assert do_filesizeformat(999.9) == "999 Bytes"


def test_filesizeformat_negative_value():
    assert do_filesizeformat(-5) == "-5 Bytes"
    assert do_filesizeformat(-1) == "-1 Bytes"


def test_filesizeformat_threshold_decimal_prefix():
    result = do_filesizeformat(1000)
    assert result.endswith(" kB")
    assert not result.endswith("Bytes")
    assert result == "%.1f kB" % (1000 / 1000 ** 2)


def test_filesizeformat_threshold_binary_prefix():
    result = do_filesizeformat(1024, binary=True)
    assert result.endswith(" KiB")
    assert result == "%.1f KiB" % (1024 / 1024 ** 2)


def test_filesizeformat_prefix_progression_decimal():
    assert do_filesizeformat(10 ** 6).endswith(" MB")
    assert do_filesizeformat(10 ** 9).endswith(" GB")
    assert do_filesizeformat(10 ** 12).endswith(" TB")
    assert do_filesizeformat(10 ** 15).endswith(" PB")


def test_filesizeformat_prefix_progression_binary():
    assert do_filesizeformat(1024 ** 2, binary=True).endswith(" MiB")
    assert do_filesizeformat(1024 ** 3, binary=True).endswith(" GiB")
    assert do_filesizeformat(1024 ** 4, binary=True).endswith(" TiB")


def test_filesizeformat_huge_value_uses_largest_prefix():
    result = do_filesizeformat(10 ** 30)
    assert result.endswith(" YB")
    assert result.startswith("1000.0")
    result_bin = do_filesizeformat(1024 ** 10, binary=True)
    assert result_bin.endswith(" YiB")


def test_filesizeformat_invalid_string_raises_value_error():
    with pytest.raises(ValueError):
        do_filesizeformat("abc")


def test_filesizeformat_none_raises_type_error():
    with pytest.raises(TypeError):
        do_filesizeformat(None)


def test_filesizeformat_list_raises_type_error():
    with pytest.raises(TypeError):
        do_filesizeformat([1, 2, 3])
