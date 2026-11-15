import copy
import pytest


def _entry(start, stop):
    return {'coordinates': {'start': start, 'stop': stop}}


@pytest.fixture
def two_ranges():
    return [_entry(1, 5), _entry(10, 15)]


# ---------- empty list ----------
def test_empty_list_returns_zero():
    assert coordinate_sorter(1, 5, []) == 0


def test_empty_list_returns_zero_even_with_none_positions():
    assert coordinate_sorter(None, None, []) == 0


# ---------- point queries (start == stop) inside ranges ----------
def test_point_inside_first_range(two_ranges):
    assert coordinate_sorter(3, 3, two_ranges) == 0


def test_point_inside_second_range(two_ranges):
    assert coordinate_sorter(12, 12, two_ranges) == 1


@pytest.mark.parametrize("point, expected", [(1, 0), (5, 0), (10, 1), (15, 1)])
def test_point_on_range_boundaries_inclusive(two_ranges, point, expected):
    assert coordinate_sorter(point, point, two_ranges) == expected


def test_point_in_overlapping_ranges_returns_first_match():
    lst = [_entry(1, 10), _entry(5, 15)]
    assert coordinate_sorter(7, 7, lst) == 0


def test_negative_coordinates_point_inside():
    lst = [_entry(-10, -5), _entry(0, 4)]
    assert coordinate_sorter(-7, -7, lst) == 0
    assert coordinate_sorter(2, 2, lst) == 1


def test_string_coordinates_are_converted_to_int():
    lst = [_entry('1', '5'), _entry('10', '15')]
    assert coordinate_sorter(12, 12, lst) == 1
    assert coordinate_sorter(20, 20, lst) == 2


# ---------- point queries beyond / outside ----------
def test_point_beyond_last_range_returns_len(two_ranges):
    assert coordinate_sorter(20, 20, two_ranges) == 2


def test_point_in_gap_between_ranges_returns_none(two_ranges):
    assert coordinate_sorter(7, 7, two_ranges) is None


def test_point_before_all_ranges_returns_none():
    assert coordinate_sorter(0, 0, [_entry(1, 5)]) is None


# ---------- range queries (start != stop) ----------
def test_range_stop_beyond_last_stop_returns_len(two_ranges):
    assert coordinate_sorter(2, 20, two_ranges) == 2


def test_range_stop_equal_last_stop_returns_len(two_ranges):
    assert coordinate_sorter(2, 15, two_ranges) == 2


def test_range_single_element_stop_ge_returns_one():
    assert coordinate_sorter(3, 5, [_entry(1, 5)]) == 1


def test_range_stop_less_than_last_stop_returns_none(two_ranges):
    assert coordinate_sorter(2, 7, two_ranges) is None


def test_range_query_does_not_match_inside_branch():
    # start != stop so the "inside range" branch is never used
    lst = [_entry(1, 5), _entry(10, 15)]
    assert coordinate_sorter(2, 3, lst) is None


# ---------- no side effects ----------
def test_input_list_not_mutated(two_ranges):
    snapshot = copy.deepcopy(two_ranges)
    coordinate_sorter(3, 3, two_ranges)
    coordinate_sorter(2, 20, two_ranges)
    assert two_ranges == snapshot


# ---------- error cases ----------
def test_none_list_raises_type_error():
    with pytest.raises(TypeError):
        coordinate_sorter(1, 2, None)


def test_missing_coordinates_key_raises_key_error():
    with pytest.raises(KeyError):
        coordinate_sorter(1, 2, [{'foo': 'bar'}])


def test_missing_start_or_stop_key_raises_key_error():
    with pytest.raises(KeyError):
        coordinate_sorter(1, 1, [{'coordinates': {'stop': 5}}])


def test_non_numeric_coordinate_raises_value_error():
    with pytest.raises(ValueError):
        coordinate_sorter(1, 1, [_entry('abc', 'def')])


def test_none_coordinate_value_raises_type_error():
    with pytest.raises(TypeError):
        coordinate_sorter(1, 1, [_entry(None, None)])


def test_none_positions_with_nonempty_list_raise_type_error(two_ranges):
    with pytest.raises(TypeError):
        coordinate_sorter(None, None, two_ranges)


def test_non_comparable_stop_raises_type_error(two_ranges):
    with pytest.raises(TypeError):
        coordinate_sorter(1, 'x', two_ranges)
