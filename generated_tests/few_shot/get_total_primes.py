import pytest


def test_get_total_primes_normal_up_to_100():
    # primes < 100 with all-prime digits: 2, 3, 5, 7, 23, 37, 53, 73
    assert get_total_primes(0, 100) == 8


def test_get_total_primes_normal_lower_bound_excludes_small_primes():
    # a > 2: excludes 2; remaining 3, 5, 7, 23, 37, 53, 73
    assert get_total_primes(3, 100) == 7
    # only two-digit ones: 23, 37, 53, 73
    assert get_total_primes(10, 100) == 4


def test_get_total_primes_range_200_to_300():
    # 223, 227, 233, 257, 277
    assert get_total_primes(200, 300) == 5


def test_get_total_primes_a_below_two_includes_two():
    assert get_total_primes(0, 10) == 4
    assert get_total_primes(1, 10) == 4


def test_get_total_primes_no_total_primes_in_range():
    # 11, 13, 17, 19 all contain non-prime digits
    assert get_total_primes(10, 20) == 0
    # no primes at all in these ranges
    assert get_total_primes(8, 10) == 0
    assert get_total_primes(24, 28) == 0


def test_get_total_primes_single_prime_range():
    assert get_total_primes(23, 24) == 1


def test_get_total_primes_no_total_primes_in_hundreds_starting_with_one():
    # primes in 100-199 all start with digit 1, so none qualify
    assert get_total_primes(100, 200) == 0
    assert get_total_primes(0, 200) == 8


def test_get_total_primes_additive_over_split_ranges():
    whole = get_total_primes(3, 100)
    split = get_total_primes(3, 50) + get_total_primes(50, 100)
    assert whole == split == 7


def test_get_total_primes_monotonic_in_lower_bound():
    assert get_total_primes(0, 100) >= get_total_primes(10, 100)
    assert get_total_primes(10, 100) >= get_total_primes(50, 100)


def test_get_total_primes_result_is_int_and_nonnegative():
    result = get_total_primes(10, 100)
    assert isinstance(result, int)
    assert result >= 0


def test_get_total_primes_error_string_lower_bound():
    with pytest.raises(TypeError):
        get_total_primes("a", 10)


def test_get_total_primes_error_string_upper_bound():
    with pytest.raises(TypeError):
        get_total_primes(1, "10")


def test_get_total_primes_error_none_upper_bound():
    with pytest.raises(TypeError):
        get_total_primes(1, None)


def test_get_total_primes_error_negative_upper_bound():
    # square root of a negative number yields a complex value, int() fails
    with pytest.raises(TypeError):
        get_total_primes(0, -4)
