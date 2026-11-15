import pytest


def test_simple_range_inside():
    assert is_degree_in_degree_range(90, 0, 45) is True
    assert is_degree_in_degree_range(180, -90, 0) is True


def test_simple_range_outside():
    assert is_degree_in_degree_range(90, 0, 100) is False
    assert is_degree_in_degree_range(90, 0, -1) is False


def test_boundaries_inclusive_when_clockwise_greater():
    assert is_degree_in_degree_range(90, 0, 0) is True
    assert is_degree_in_degree_range(90, 0, 90) is True


def test_range_crossing_zero_inside():
    assert is_degree_in_degree_range(-10, 10, 20) is True
    assert is_degree_in_degree_range(-10, 10, -20) is True
    assert is_degree_in_degree_range(-10, 10, 180) is True
    assert is_degree_in_degree_range(-10, 10, 10) is True
    assert is_degree_in_degree_range(-10, 10, -10) is True


def test_range_crossing_zero_outside():
    assert is_degree_in_degree_range(-10, 10, 0) is False
    assert is_degree_in_degree_range(-10, 10, 5) is False
    assert is_degree_in_degree_range(0, 10, 5) is False


def test_equal_endpoints_and_same_sign_ascending():
    assert is_degree_in_degree_range(50, 50, 50) is False
    assert is_degree_in_degree_range(0, 0, 0) is False
    assert is_degree_in_degree_range(10, 20, 15) is False
    assert is_degree_in_degree_range(-20, -10, -15) is False


def test_zero_clockwise_edge():
    assert is_degree_in_degree_range(0, 10, 0) is True
    assert is_degree_in_degree_range(0, 10, 10) is True


@pytest.mark.parametrize(
    "a, b, c, expected",
    [
        (270, 10, 180, True),     # 270 -> -90, range wraps through 180
        (190, 10, -175, True),    # 190 -> -170
        (190, 10, 0, False),
        (360, 90, 100, True),     # 360 -> 0
        (90, 0, 360, True),       # c: 360 -> 0
        (90, 0, 450, True),       # c: 450 -> 90
        (90, 0, -270, True),      # c: -270 -> 90
        (90, 0, 540, False),      # c: 540 -> -180
    ],
)
def test_normalization_of_out_of_range_values(a, b, c, expected):
    assert is_degree_in_degree_range(a, b, c) is expected


def test_minus_180_is_normalized_to_180():
    assert is_degree_in_degree_range(-180, 0, 90) is True
    assert is_degree_in_degree_range(-180, 0, -90) is False
    assert is_degree_in_degree_range(90, 0, -180) is False


def test_float_inputs():
    assert is_degree_in_degree_range(45.5, 10.25, 30.0) is True
    assert is_degree_in_degree_range(45.5, 10.25, 50.0) is False


def test_invalid_types_raise():
    with pytest.raises(TypeError):
        is_degree_in_degree_range("a", 0, 0)
    with pytest.raises(TypeError):
        is_degree_in_degree_range(0, None, 0)
    with pytest.raises(TypeError):
        is_degree_in_degree_range(0, 0, [1])


def test_missing_arguments_raise():
    with pytest.raises(TypeError):
        is_degree_in_degree_range(10, 20)
