import pytest


def test_zero_bytes():
    assert do_filesizeformat(0) == "0 Bytes"


def test_one_byte_singular():
    assert do_filesizeformat(1) == "1 Byte"
    assert do_filesizeformat(1.0) == "1 Byte"
    assert do_filesizeformat("1") == "1 Byte"
    assert do_filesizeformat(True) == "1 Byte"


@pytest.mark.parametrize("value, expected", [
    (2, "2 Bytes"),
    (10, "10 Bytes"),
    (999, "999 Bytes"),
    (999.9, "999 Bytes"),
    (0.5, "0 Bytes"),
    ("42", "42 Bytes"),
])
def test_small_values_decimal(value, expected):
    assert do_filesizeformat(value) == expected


@pytest.mark.parametrize("value, expected", [
    (1000, "1000 Bytes"),
    (1023, "1023 Bytes"),
    (999, "999 Bytes"),
    (1, "1 Byte"),
    (0, "0 Bytes"),
])
def test_small_values_binary(value, expected):
    assert do_filesizeformat(value, binary=True) == expected


def test_negative_values():
    assert do_filesizeformat(-1) == "-1 Bytes"
    assert do_filesizeformat(-5) == "-5 Bytes"
    assert do_filesizeformat(-999) == "-999 Bytes"


def test_decimal_boundary_at_base():
    # Exactly 1000 is no longer "Bytes"; it enters the prefix loop
    result = do_filesizeformat(1000)
    assert result.endswith(" kB")
    assert "Bytes" not in result


def test_binary_boundary_at_base():
    result = do_filesizeformat(1024, binary=True)
    assert result.endswith(" KiB")
    assert "Bytes" not in result


def test_decimal_prefix_values():
    # Behavior of the implementation: unit = base ** (i + 2)
    assert do_filesizeformat(500000) == "0.5 kB"
    assert do_filesizeformat(500000000000) == "0.5 GB"
    assert do_filesizeformat(1000) == "0.0 kB"


def test_binary_prefix_values():
    assert do_filesizeformat(524288, binary=True) == "0.5 KiB"
    assert do_filesizeformat(1024 ** 3 // 2, binary=True) == "0.5 MiB"
    assert do_filesizeformat(1024, binary=True) == "0.0 KiB"


def test_decimal_and_binary_use_different_prefixes():
    dec = do_filesizeformat(500000)
    bi = do_filesizeformat(500000, binary=True)
    assert "kB" in dec
    assert "KiB" in bi
    assert dec != bi


def test_very_large_value_uses_largest_prefix():
    result = do_filesizeformat(1e30)
    assert result == "1000.0 YB"
    result_bin = do_filesizeformat(1e40, binary=True)
    assert result_bin.endswith(" YiB")


def test_infinity_uses_largest_prefix():
    assert do_filesizeformat(float("inf")) == "inf YB"
    assert do_filesizeformat(float("inf"), binary=True) == "inf YiB"


def test_string_numeric_input_converted():
    assert do_filesizeformat("500000") == do_filesizeformat(500000)
    assert do_filesizeformat("12.0") == "12 Bytes"


def test_none_raises_type_error():
    with pytest.raises(TypeError):
        do_filesizeformat(None)


@pytest.mark.parametrize("bad", ["abc", "", "1.2.3", "12 KB"])
def test_non_numeric_string_raises_value_error(bad):
    with pytest.raises(ValueError):
        do_filesizeformat(bad)


def test_unsupported_types_raise_type_error():
    with pytest.raises(TypeError):
        do_filesizeformat([1, 2, 3])
    with pytest.raises(TypeError):
        do_filesizeformat({"a": 1})
