import pytest


def make_grid(n):
    """Build an n x n grid where each cell is a list holding its 'yx' label."""
    return [[[f"{y}{x}"] for x in range(n)] for y in range(n)]


def test_center_cell_returns_all_neighbors_in_order():
    buckets = make_grid(3)
    result = get_adjacent_buckets(1, 1, buckets)
    assert result == ["10", "00", "01", "02", "12", "22", "21", "20", "11"]
    assert len(result) == 9


def test_top_left_corner():
    buckets = make_grid(3)
    assert get_adjacent_buckets(0, 0, buckets) == ["01", "11", "10", "00"]


def test_bottom_right_corner():
    buckets = make_grid(3)
    assert get_adjacent_buckets(2, 2, buckets) == ["21", "11", "12", "22"]


def test_top_right_corner():
    buckets = make_grid(3)
    assert get_adjacent_buckets(2, 0, buckets) == ["01", "12", "11", "02"]


def test_bottom_left_corner():
    buckets = make_grid(3)
    assert get_adjacent_buckets(0, 2, buckets) == ["10", "11", "21", "20"]


def test_top_edge_cell():
    buckets = make_grid(3)
    assert get_adjacent_buckets(1, 0, buckets) == ["00", "02", "12", "11", "10", "01"]


def test_left_edge_cell():
    buckets = make_grid(3)
    assert get_adjacent_buckets(0, 1, buckets) == ["00", "01", "11", "21", "20", "10"]


def test_single_cell_grid():
    buckets = [[["a", "b"]]]
    assert get_adjacent_buckets(0, 0, buckets) == ["a", "b"]


def test_empty_cells_return_empty_list():
    buckets = [[[] for _ in range(3)] for _ in range(3)]
    assert get_adjacent_buckets(1, 1, buckets) == []


def test_cells_with_multiple_items_are_concatenated():
    buckets = [
        [[1, 2], [3], []],
        [[], [4, 5], [6]],
        [[7], [], [8, 9]],
    ]
    result = get_adjacent_buckets(1, 1, buckets)
    # left, up-left, up, up-right, right, down-right, down, down-left, center
    assert result == [] + [1, 2] + [3] + [] + [6] + [8, 9] + [] + [7] + [4, 5]
    assert sorted(result) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_does_not_mutate_input_buckets():
    buckets = make_grid(3)
    get_adjacent_buckets(1, 1, buckets)
    assert buckets == make_grid(3)


def test_returns_new_list_not_cell_reference():
    buckets = make_grid(3)
    result = get_adjacent_buckets(0, 0, buckets)
    assert result is not buckets[0][0]
    result.append("x")
    assert buckets[0][0] == ["00"]


def test_larger_grid_interior_cell():
    buckets = make_grid(5)
    result = get_adjacent_buckets(2, 3, buckets)
    expected_cells = {"32", "22", "23", "24", "34", "44", "43", "42", "33"}
    assert set(result) == expected_cells
    assert len(result) == 9
    assert result[-1] == "33"


def test_empty_buckets_raises_index_error():
    with pytest.raises(IndexError):
        get_adjacent_buckets(0, 0, [])


def test_none_buckets_raises_type_error():
    with pytest.raises(TypeError):
        get_adjacent_buckets(0, 0, None)


def test_none_coordinate_raises_type_error():
    buckets = make_grid(3)
    with pytest.raises(TypeError):
        get_adjacent_buckets(None, 1, buckets)


def test_cx_out_of_range_raises_index_error():
    buckets = make_grid(3)
    with pytest.raises(IndexError):
        get_adjacent_buckets(5, 1, buckets)


def test_cy_out_of_range_raises_index_error():
    buckets = make_grid(3)
    with pytest.raises(IndexError):
        get_adjacent_buckets(1, 5, buckets)


def test_non_square_grid_raises_index_error():
    # 2 rows x 3 columns: b_length is 3, so a row index of 2 is probed and fails
    buckets = [
        [["a"], ["b"], ["c"]],
        [["d"], ["e"], ["f"]],
    ]
    with pytest.raises(IndexError):
        get_adjacent_buckets(1, 1, buckets)
