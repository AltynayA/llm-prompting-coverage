import pytest


def make_entry(start, stop):
    return {"coordinates": {"start": start, "stop": stop}}


@pytest.fixture
def three_entries():
    return [make_entry(1, 10), make_entry(20, 30), make_entry(40, 50)]


def test_empty_list_returns_zero():
    assert coordinate_sorter(5, 10, []) == 0
    assert coordinate_sorter(5, 5, []) == 0


def test_point_inside_single_entry_returns_its_index():
    assert coordinate_sorter(15, 15, [make_entry(10, 20)]) == 0


def test_point_on_boundaries_is_inclusive():
    entries = [make_entry(10, 20)]
    assert coordinate_sorter(10, 10, entries) == 0
    assert coordinate_sorter(20, 20, entries) == 0


def test_point_inside_middle_entry(three_entries):
    assert coordinate_sorter(25, 25, three_entries) == 1
    assert coordinate_sorter(30, 30, three_entries) == 1
    assert coordinate_sorter(10, 10, three_entries) == 0
    assert coordinate_sorter(45, 45, three_entries) == 2


def test_point_beyond_all_entries_returns_len(three_entries):
    assert coordinate_sorter(60, 60, three_entries) == 3
    assert coordinate_sorter(51, 51, three_entries) == 3


def test_point_beyond_single_entry_returns_one():
    assert coordinate_sorter(25, 25, [make_entry(10, 20)]) == 1


def test_range_extending_past_last_entry_returns_len(three_entries):
    assert coordinate_sorter(5, 60, three_entries) == 3
    assert coordinate_sorter(5, 50, three_entries) == 3  # stop == last stop


def test_range_past_single_entry_returns_one():
    assert coordinate_sorter(5, 25, [make_entry(10, 20)]) == 1


def test_range_not_reaching_last_entry_returns_none(three_entries):
    assert coordinate_sorter(5, 25, three_entries) is None
    assert coordinate_sorter(0, 5, [make_entry(1, 10), make_entry(20, 30)]) is None


def test_point_before_all_entries_returns_none():
    assert coordinate_sorter(5, 5, [make_entry(10, 20)]) is None


def test_point_in_gap_between_entries_returns_none(three_entries):
    assert coordinate_sorter(15, 15, three_entries) is None


def test_string_coordinates_are_converted_to_int():
    entries = [make_entry("10", "20")]
    assert coordinate_sorter(15, 15, entries) == 0
    assert coordinate_sorter(25, 25, entries) == 1
    assert coordinate_sorter(5, 30, entries) == 1


def test_zero_coordinates():
    assert coordinate_sorter(0, 0, [make_entry(0, 0)]) == 0
    assert coordinate_sorter(1, 1, [make_entry(0, 0)]) == 1


def test_negative_coordinates():
    entries = [make_entry(-10, -5)]
    assert coordinate_sorter(-7, -7, entries) == 0
    assert coordinate_sorter(-1, -1, entries) == 1
    assert coordinate_sorter(-20, -20, entries) is None


def test_none_list_raises_type_error():
    with pytest.raises(TypeError):
        coordinate_sorter(1, 2, None)


def test_missing_coordinates_key_raises_key_error():
    with pytest.raises(KeyError):
        coordinate_sorter(1, 2, [{"other": 1}])


def test_missing_start_or_stop_key_raises_key_error():
    with pytest.raises(KeyError):
        coordinate_sorter(1, 1, [{"coordinates": {"stop": 5}}])
    with pytest.raises(KeyError):
        coordinate_sorter(1, 2, [{"coordinates": {"start": 5}}])


def test_non_numeric_coordinate_raises_value_error():
    with pytest.raises(ValueError):
        coordinate_sorter(1, 1, [make_entry("abc", "def")])


def test_non_dict_entries_raise_type_error():
    with pytest.raises(TypeError):
        coordinate_sorter(1, 2, [1, 2, 3])
