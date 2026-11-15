import pytest


# ---------- Happy path ----------

def test_total_primes_below_10_from_zero():
    # primes: 2,3,5,7 -> all digits prime -> 4 (a < 2, so 2 is counted)
    assert get_total_primes(0, 10) == 4


def test_total_primes_below_30_from_zero():
    # primes: 2,3,5,7,11,13,17,19,23,29 -> total primes: 2,3,5,7,23
    assert get_total_primes(0, 30) == 5


def test_total_primes_below_100_from_zero():
    # total primes: 2,3,5,7,23,37,53,73
    assert get_total_primes(0, 100) == 8


def test_total_primes_lower_bound_three():
    # 3,5,7,23
    assert get_total_primes(3, 30) == 4


def test_total_primes_mid_range():
    # primes >= 8 and < 30: 11,13,17,19,23,29 -> only 23 is total
    assert get_total_primes(8, 30) == 1


def test_total_primes_two_digit_only():
    # 23, 37, 53, 73
    assert get_total_primes(10, 100) == 4


def test_total_primes_a_one_equals_a_zero():
    assert get_total_primes(1, 10) == get_total_primes(0, 10) == 4


# ---------- Edge cases / boundaries ----------

def test_a_equal_two_excludes_two_current_behavior():
    # for a >= 2 the function always subtracts 1 (the leading 2), even if a == 2
    assert get_total_primes(2, 10) == 3


def test_a_greater_than_b_returns_zero():
    assert get_total_primes(50, 30) == 0


def test_tiny_upper_bounds_with_low_a():
    # the sieve is empty/trivial, only the hard-coded 2 remains
    assert get_total_primes(0, 0) == 1
    assert get_total_primes(0, 1) == 1
    assert get_total_primes(0, 2) == 1
    assert get_total_primes(0, 3) == 1


def test_tiny_upper_bounds_with_a_at_least_two():
    assert get_total_primes(2, 2) == 0
    assert get_total_primes(3, 3) == 0
    assert get_total_primes(5, 2) == 0


def test_odd_upper_bound_is_exclusive():
    # 11 is prime but not total anyway; 7 is the last prime below 11
    assert get_total_primes(0, 11) == 4


def test_even_upper_bound_includes_odd_below():
    # 11 is included in the list of primes but is not a total prime
    assert get_total_primes(0, 12) == 4
    assert get_total_primes(2, 12) == 3


def test_float_upper_bound_matches_int():
    assert get_total_primes(0, 10.0) == get_total_primes(0, 10)


def test_result_is_int_and_non_negative():
    res = get_total_primes(0, 50)
    assert isinstance(res, int)
    assert res >= 0


# ---------- Error cases ----------

def test_none_upper_bound_raises_type_error():
    with pytest.raises(TypeError):
        get_total_primes(0, None)


def test_string_upper_bound_raises_type_error():
    with pytest.raises(TypeError):
        get_total_primes(0, "10")


def test_negative_upper_bound_raises_type_error():
    # (-5) ** 0.5 is complex, int(complex) raises TypeError
    with pytest.raises(TypeError):
        get_total_primes(0, -5)


def test_none_lower_bound_raises_type_error():
    # comparison between None and int raises TypeError when the sieve has odd candidates
    with pytest.raises(TypeError):
        get_total_primes(None, 30)


def test_upper_bound_nine_raises_value_error_due_to_slice_mismatch():
    # known defect: extended-slice assignment size mismatch for b == 9
    with pytest.raises(ValueError):
        get_total_primes(0, 9)
