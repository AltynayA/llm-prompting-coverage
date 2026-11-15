import pytest


def test_total_primes_below_10():
    # 2, 3, 5, 7 are all primes whose digits are prime
    assert get_total_primes(0, 10) == 4


def test_total_primes_below_100():
    # 2, 3, 5, 7, 23, 37, 53, 73
    assert get_total_primes(0, 100) == 8


def test_total_primes_below_1000():
    # 4 one-digit + 4 two-digit + 15 three-digit
    assert get_total_primes(0, 1000) == 23


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 100, 7),      # 3, 5, 7, 23, 37, 53, 73
        (10, 100, 4),     # 23, 37, 53, 73
        (24, 100, 3),     # 37, 53, 73
        (100, 1000, 15),  # all three-digit total primes
        (11, 20, 0),      # 11, 13, 17, 19 contain non-prime digits
        (7, 8, 1),        # only 7
    ],
)
def test_total_primes_with_lower_bound(a, b, expected):
    assert get_total_primes(a, b) == expected


def test_lower_bound_zero_and_one_are_equivalent():
    assert get_total_primes(0, 100) == get_total_primes(1, 100)
    assert get_total_primes(1, 100) == 8


def test_negative_lower_bound_behaves_like_zero():
    assert get_total_primes(-5, 10) == 4
    assert get_total_primes(-100, 100) == get_total_primes(0, 100)


def test_small_upper_bounds():
    assert get_total_primes(0, 2) == 1
    assert get_total_primes(0, 4) == 2   # 2, 3
    assert get_total_primes(0, 6) == 3   # 2, 3, 5


def test_lower_bound_greater_than_upper_bound_returns_zero():
    assert get_total_primes(50, 10) == 0


def test_result_is_non_decreasing_in_upper_bound():
    previous = 0
    for b in range(10, 600, 10):
        current = get_total_primes(0, b)
        assert current >= previous
        previous = current


def test_result_is_integer():
    result = get_total_primes(0, 100)
    assert isinstance(result, int)


def test_none_upper_bound_raises_type_error():
    with pytest.raises(TypeError):
        get_total_primes(0, None)


def test_none_lower_bound_raises_type_error():
    with pytest.raises(TypeError):
        get_total_primes(None, 100)


def test_string_upper_bound_raises_type_error():
    with pytest.raises(TypeError):
        get_total_primes(0, "100")


def test_negative_upper_bound_raises_type_error():
    # (-n) ** 0.5 yields a complex number, which int() cannot convert
    with pytest.raises(TypeError):
        get_total_primes(0, -10)
