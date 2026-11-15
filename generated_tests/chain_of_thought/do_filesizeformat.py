import pytest


# Step 1 (summary): do_filesizeformat converts a number (or numeric string) to a
# human-readable size string. Pure function, no side effects.
# Note: unit = base * base ** (i + 1) == base ** (i + 2), and the result is not
# multiplied by base, so e.g. 500000 -> "0.5 kB". Tests below assert the actual
# behaviour of the code as written.


def test_one_byte_singular():
    assert do_filesizeformat(1) == "1 Byte"
    assert do_filesizeformat(1.0) == "1 Byte"
    assert do_filesizeformat("1") == "1 Byte"
    assert do_filesizeformat(1, binary=True) == "1 Byte"


def test_zero_and_small_values_are_bytes():
    assert do_filesizeformat(0) == "0 Bytes"
    assert do_filesizeformat(2) == "2 Bytes"
    assert do_filesizeformat(999) == "999 Bytes"
    assert do_filesizeformat(1.9) == "1 Bytes"  # %d truncates


def test_binary_base_boundary_bytes():
    assert do_filesizeformat(1000, binary=True) == "1000 Bytes"
    assert do_filesizeformat(1023, binary=True) == "1023 Bytes"


def test_negative_values_are_bytes():
    assert do_filesizeformat(-5) == "-5 Bytes"
    assert do_filesizeformat(-1) == "-1 Bytes"


def test_numeric_string_input():
    assert do_filesizeformat("100") == "100 Bytes"
    assert do_filesizeformat("500000") == "0.5 kB"


def test_decimal_prefixes():
    assert do_filesizeformat(500000) == "0.5 kB"
    assert do_filesizeformat(1000) == "0.0 kB"
    assert do_filesizeformat(500000000) == "0.5 MB"
    assert do_filesizeformat(500000000000) == "0.5 GB"


def test_decimal_unit_boundaries_move_to_next_prefix():
    assert do_filesizeformat(10 ** 6) == "0.0 MB"
    assert do_filesizeformat(10 ** 9) == "0.0 GB"


def test_binary_prefixes():
    assert do_filesizeformat(1024 ** 2 // 2, binary=True) == "0.5 KiB"
    assert do_filesizeformat(1024 ** 3 // 2, binary=True) == "0.5 MiB"
    assert do_filesizeformat(1024 ** 4 // 2, binary=True) == "0.5 GiB"


def test_binary_vs_decimal_suffixes_differ():
    dec = do_filesizeformat(500000)
    binr = do_filesizeformat(500000, binary=True)
    assert dec.endswith("kB")
    assert binr.endswith("KiB")


def test_huge_value_uses_largest_prefix():
    assert do_filesizeformat(1e30) == "1000.0 YB"
    assert do_filesizeformat(float(1024 ** 9), binary=True) == "1.0 YiB"


def test_infinity_and_nan():
    assert do_filesizeformat(float("inf")) == "inf YB"
    assert do_filesizeformat(float("nan")) == "nan YB"


def test_none_raises_type_error():
    with pytest.raises(TypeError):
        do_filesizeformat(None)


def test_non_numeric_string_raises_value_error():
    with pytest.raises(ValueError):
        do_filesizeformat("abc")
    with pytest.raises(ValueError):
        do_filesizeformat("")


def test_unsupported_types_raise_type_error():
    with pytest.raises(TypeError):
        do_filesizeformat([])
    with pytest.raises(TypeError):
        do_filesizeformat({"a": 1})
