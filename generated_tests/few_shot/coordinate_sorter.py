import pytest


def _make(*pairs):
    return [{'coordinates': {'start': s, 'stop': e}} for s, e in pairs]


def test_coordinate_sorter_empty_list_returns_zero():
    assert coordinate_sorter(5, 5, []) == 0
    assert coordinate_sorter(1, 10, []) == 0


def test_coordinate_sorter_point_inside_interval():
    items = _make((1, 10), (20, 30))
    assert coordinate_sorter(5, 5, items) == 0
    assert coordinate_sorter(25, 25, items) == 1


def test_coordinate_sorter_point_on_interval_boundaries():
    items = _make((1, 10), (20, 30))
    assert coordinate_sorter(1, 1, items) == 0
    assert coordinate_sorter(10, 10, items) == 0
    assert coordinate_sorter(20, 20, items) == 1
    assert coordinate_sorter(30, 30, items) == 1


def test_coordinate_sorter_point_after_last_interval_returns_length():
    items = _make((1, 10), (20, 30))
    assert coordinate_sorter(50, 50, items) == 2


def test_coordinate_sorter_point_in_gap_returns_none():
    items = _make((1, 10), (20, 30))
    assert coordinate_sorter(15, 15, items) is None


def test_coordinate_sorter_point_before_all_intervals_returns_none():
    items = _make((10, 20), (30, 40))
    assert coordinate_sorter(1, 1, items) is None


def test_coordinate_sorter_point_in_overlapping_intervals_returns_first_match():
    items = _make((1, 10), (5, 8))
    assert coordinate_sorter(6, 6, items) == 0


def test_coordinate_sorter_range_reaching_last_stop_returns_length():
    items = _make((1, 10), (20, 30))
    assert coordinate_sorter(5, 40, items) == 2
    assert coordinate_sorter(5, 30, items) == 2
    assert coordinate_sorter(1, 5, _make((1, 3))) == 1


def test_coordinate_sorter_range_not_reaching_last_stop_returns_none():
    items = _make((1, 10), (20, 30))
    assert coordinate_sorter(5, 25, items) is None


def test_coordinate_sorter_string_coordinates_are_converted():
    items = [
        {'coordinates': {'start': '1', 'stop': '10'}},
        {'coordinates': {'start': '20', 'stop': '30'}},
    ]
    assert coordinate_sorter(5, 5, items) == 0
    assert coordinate_sorter(22, 22, items) == 1
    assert coordinate_sorter(100, 100, items) == 2


def test_coordinate_sorter_missing_coordinates_key_raises():
    with pytest.raises(KeyError):
        coordinate_sorter(5, 5, [{'other': 1}])


def test_coordinate_sorter_missing_start_or_stop_raises():
    with pytest.raises(KeyError):
        coordinate_sorter(5, 5, [{'coordinates': {'start': 1}}])


def test_coordinate_sorter_non_numeric_coordinate_raises_value_error():
    items = [{'coordinates': {'start': 'abc', 'stop': 'def'}}]
    with pytest.raises(ValueError):
        coordinate_sorter(5, 5, items)


def test_coordinate_sorter_invalid_list_items_raise_type_error():
    with pytest.raises(TypeError):
        coordinate_sorter(5, 5, [1, 2, 3])


def test_coordinate_sorter_none_list_raises_type_error():
    with pytest.raises(TypeError):
        coordinate_sorter(1, 2, None)
