import pytest


# Step 1: The function normalises three angles (degrees) into roughly (-180, 180],
#   then checks whether degree_c lies on the arc between degree_a (clockwise bound)
#   and degree_b (counter-clockwise bound). It returns a bool and has no side effects.
# Step 2: Edge cases: zero, boundaries at +/-180, values beyond 180, negative wraparound,
#   a == b, floats, None and strings.
# Step 3: Happy paths: c inside a normal range, c inside a range that crosses the 180 boundary.
# Step 4: Errors: None or str inputs raise TypeError from the comparisons.


def test_c_inside_simple_range():
    assert is_degree_in_degree_range(90, 0, 45) is True


def test_c_on_range_boundaries():
    assert is_degree_in_degree_range(90, 0, 90) is True
    assert is_degree_in_degree_range(90, 0, 0) is True


def test_c_outside_simple_range():
    assert is_degree_in_degree_range(90, 0, 100) is False
    assert is_degree_in_degree_range(90, 0, -10) is False


def test_range_crossing_180_boundary():
    # a=-90 < b=90, a <= 0, b > 0 -> c must be >= b or <= a
    assert is_degree_in_degree_range(-90, 90, 180) is True
    assert is_degree_in_degree_range(-90, 90, 100) is True
    assert is_degree_in_degree_range(-90, 90, -100) is True
    assert is_degree_in_degree_range(-90, 90, 0) is False


def test_wraparound_range_with_near_180_values():
    assert is_degree_in_degree_range(-170, 170, 175) is True
    assert is_degree_in_degree_range(-170, 170, -175) is True
    assert is_degree_in_degree_range(-170, 170, 0) is False


def test_zero_start_wrap_range():
    assert is_degree_in_degree_range(0, 90, 100) is True
    assert is_degree_in_degree_range(0, 90, -10) is True
    assert is_degree_in_degree_range(0, 90, 0) is True
    assert is_degree_in_degree_range(0, 90, 45) is False


def test_equal_a_and_b_returns_false():
    assert is_degree_in_degree_range(50, 50, 50) is False
    assert is_degree_in_degree_range(0, 0, 0) is False


def test_ascending_range_not_crossing_zero_returns_false():
    assert is_degree_in_degree_range(10, 20, 15) is False
    assert is_degree_in_degree_range(-20, -10, -15) is False


def test_normalization_of_a_above_180():
    # 270 -> -90; a=-90 > b=-100, so c must be in [-100, -90]
    assert is_degree_in_degree_range(270, -100, -95) is True
    assert is_degree_in_degree_range(270, -100, 0) is False


def test_normalization_full_rotation():
    # 450 -> 90, 360 -> 0
    assert is_degree_in_degree_range(450, 0, 45) is True
    assert is_degree_in_degree_range(90, -90, 360) is True


def test_normalization_of_c_beyond_range():
    # c=190 -> -170, c=-190 -> 170
    assert is_degree_in_degree_range(-170, 170, 190) is True
    assert is_degree_in_degree_range(-170, 170, -190) is True
    assert is_degree_in_degree_range(-90, 90, 190) is True  # -170 <= -90


def test_minus_180_normalizes_to_180():
    assert is_degree_in_degree_range(0, 180, -180) is True
    assert is_degree_in_degree_range(0, 180, 180) is True
    assert is_degree_in_degree_range(0, 180, 90) is False


def test_540_normalizes_to_minus_180():
    # a=540 -> -180, b=-190 -> 170
    assert is_degree_in_degree_range(540, -190, 175) is True
    assert is_degree_in_degree_range(540, -190, 0) is False


def test_float_inputs():
    assert is_degree_in_degree_range(90.5, 0.5, 45.0) is True
    assert is_degree_in_degree_range(90.5, 0.5, 91.0) is False


def test_returns_bool_type():
    assert isinstance(is_degree_in_degree_range(10, 20, 30), bool)
    assert isinstance(is_degree_in_degree_range(90, 0, 45), bool)


def test_none_input_raises_type_error():
    with pytest.raises(TypeError):
        is_degree_in_degree_range(None, 0, 0)
    with pytest.raises(TypeError):
        is_degree_in_degree_range(0, None, 0)
    with pytest.raises(TypeError):
        is_degree_in_degree_range(0, 0, None)


def test_string_input_raises_type_error():
    with pytest.raises(TypeError):
        is_degree_in_degree_range("90", 0, 45)
    with pytest.raises(TypeError):
        is_degree_in_degree_range(90, 0, "45")
