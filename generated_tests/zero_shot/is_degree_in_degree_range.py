import pytest


@pytest.mark.parametrize(
    "a, b, c",
    [
        (90, 0, 45),
        (90, 0, 0),    # equals counterclock boundary
        (90, 0, 90),   # equals clockwise boundary
        (180, -170, 0),
        (45, -45, 0),
        (90.5, 0.5, 45.25),
    ],
)
def test_range_with_a_greater_than_b_true(a, b, c):
    assert is_degree_in_degree_range(a, b, c) is True


@pytest.mark.parametrize(
    "a, b, c",
    [
        (90, 0, 100),
        (90, 0, -1),
        (45, -45, 60),
        (45, -45, -60),
        (180, 0, -90),
    ],
)
def test_range_with_a_greater_than_b_false(a, b, c):
    assert is_degree_in_degree_range(a, b, c) is False


@pytest.mark.parametrize(
    "a, b, c",
    [
        (-10, 10, 170),    # c >= b
        (-10, 10, -170),   # c <= a
        (-10, 10, 10),     # boundary b
        (-10, 10, -10),    # boundary a
        (0, 10, 10),
        (0, 10, 0),
        (-90, 90, 180),
    ],
)
def test_wraparound_range_true(a, b, c):
    assert is_degree_in_degree_range(a, b, c) is True


@pytest.mark.parametrize(
    "a, b, c",
    [
        (-10, 10, 0),
        (-10, 10, 5),
        (-10, 10, -5),
        (0, 10, 5),
        (-90, 90, 0),
    ],
)
def test_wraparound_range_false(a, b, c):
    assert is_degree_in_degree_range(a, b, c) is False


@pytest.mark.parametrize(
    "a, b, c",
    [
        (10, 20, 15),     # both positive, a < b
        (10, 20, 100),
        (-20, -10, -15),  # both negative, a < b
        (-20, -10, 0),
        (50, 50, 50),     # equal bounds
        (0, 0, 0),
        (-30, -30, 10),
    ],
)
def test_cases_that_fall_through_return_false(a, b, c):
    assert is_degree_in_degree_range(a, b, c) is False


@pytest.mark.parametrize(
    "a, b, c, expected",
    [
        (370, 0, 5, True),       # 370 -> 10
        (370, 0, 15, False),
        (190, 170, 180, True),   # 190 -> -170, wraparound; c >= b
        (190, 170, 0, False),
        (-160, 160, 190, True),  # c 190 -> -170 <= -160
        (-160, 160, 0, False),
        (360, -10, -5, True),    # 360 -> 0
        (360, -10, 5, False),
        (-180, 0, 90, True),     # -180 -> 180
        (180, -180, 0, False),   # -180 -> 180, equal bounds
        (90, 450, 45, False),    # 450 -> 90, equal bounds
    ],
)
def test_out_of_range_angles_are_normalized(a, b, c, expected):
    assert is_degree_in_degree_range(a, b, c) is expected


def test_large_and_negative_out_of_range_values():
    # -190 -> 170, -360 -> 0, -540 -> 180
    assert is_degree_in_degree_range(170, 0, 100) is True
    assert is_degree_in_degree_range(-190, 0, 100) is True
    assert is_degree_in_degree_range(-190, 0, -100) is False
    assert is_degree_in_degree_range(-360, -10, -5) is True
    assert is_degree_in_degree_range(-540, 0, 90) is True


def test_returns_boolean_type():
    assert isinstance(is_degree_in_degree_range(90, 0, 45), bool)
    assert isinstance(is_degree_in_degree_range(90, 0, 100), bool)
    assert isinstance(is_degree_in_degree_range(-10, 10, 0), bool)


@pytest.mark.parametrize(
    "args",
    [
        (None, 0, 0),
        (0, None, 0),
        (0, 0, None),
        (None, None, None),
    ],
)
def test_none_raises_type_error(args):
    with pytest.raises(TypeError):
        is_degree_in_degree_range(*args)


@pytest.mark.parametrize(
    "args",
    [
        ("90", 0, 45),
        (90, "0", 45),
        (90, 0, "45"),
        ([90], 0, 45),
    ],
)
def test_non_numeric_raises_type_error(args):
    with pytest.raises(TypeError):
        is_degree_in_degree_range(*args)


def test_missing_arguments_raises_type_error():
    with pytest.raises(TypeError):
        is_degree_in_degree_range(10, 20)
