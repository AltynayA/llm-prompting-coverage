import copy
import pytest


@pytest.fixture
def grid3():
    # buckets[y][x] == [10*y + x]
    return [
        [[0], [1], [2]],
        [[10], [11], [12]],
        [[20], [21], [22]],
    ]


# ---------- Happy path ----------

def test_center_cell_collects_all_eight_neighbors_and_itself(grid3):
    # order: left, up-left, up, up-right, right, down-right, down, down-left, center
    assert get_adjacent_buckets(1, 1, grid3) == [10, 0, 1, 2, 12, 22, 21, 20, 11]


def test_center_cell_contains_every_element_once(grid3):
    result = get_adjacent_buckets(1, 1, grid3)
    assert sorted(result) == [0, 1, 2, 10, 11, 12, 20, 21, 22]


# ---------- Corners ----------

def test_top_left_corner(grid3):
    assert get_adjacent_buckets(0, 0, grid3) == [1, 11, 10, 0]


def test_top_right_corner(grid3):
    assert get_adjacent_buckets(2, 0, grid3) == [1, 12, 11, 2]


def test_bottom_left_corner(grid3):
    assert get_adjacent_buckets(0, 2, grid3) == [10, 11, 21, 20]


def test_bottom_right_corner(grid3):
    assert get_adjacent_buckets(2, 2, grid3) == [21, 11, 12, 22]


# ---------- Edges ----------

def test_top_edge(grid3):
    assert get_adjacent_buckets(1, 0, grid3) == [0, 2, 12, 11, 10, 1]


def test_bottom_edge(grid3):
    assert get_adjacent_buckets(1, 2, grid3) == [20, 10, 11, 12, 22, 21]


def test_left_edge(grid3):
    assert get_adjacent_buckets(0, 1, grid3) == [0, 1, 11, 21, 20, 10]


def test_right_edge(grid3):
    assert get_adjacent_buckets(2, 1, grid3) == [11, 1, 2, 22, 21, 12]


# ---------- Special contents / sizes ----------

def test_single_cell_grid():
    assert get_adjacent_buckets(0, 0, [[[5]]]) == [5]


def test_single_cell_grid_empty_bucket():
    assert get_adjacent_buckets(0, 0, [[[]]]) == []


def test_all_empty_buckets_returns_empty_list():
    grid = [[[] for _ in range(3)] for _ in range(3)]
    assert get_adjacent_buckets(1, 1, grid) == []


def test_multiple_items_and_duplicates_preserved():
    grid = [
        [["a", "b"], ["c"]],
        [[], ["a", "d"]],
    ]
    # cx=0, cy=0: right ["c"], down-right ["a","d"], down [], center ["a","b"]
    assert get_adjacent_buckets(0, 0, grid) == ["c", "a", "d", "a", "b"]


def test_larger_grid_interior_cell():
    grid = [[[10 * y + x] for x in range(4)] for y in range(4)]
    result = get_adjacent_buckets(2, 2, grid)
    assert sorted(result) == sorted([11, 12, 13, 21, 22, 23, 31, 32, 33])
    assert result[-1] == 22


def test_input_not_mutated(grid3):
    original = copy.deepcopy(grid3)
    get_adjacent_buckets(1, 1, grid3)
    get_adjacent_buckets(0, 0, grid3)
    get_adjacent_buckets(2, 2, grid3)
    assert grid3 == original


def test_returns_new_list_not_bucket_reference(grid3):
    result = get_adjacent_buckets(0, 0, grid3)
    assert result is not grid3[0][0]
    result.append(999)
    assert grid3[0][0] == [0]


# ---------- Error cases ----------

def test_empty_buckets_raises_index_error():
    with pytest.raises(IndexError):
        get_adjacent_buckets(0, 0, [])


def test_none_buckets_raises_type_error():
    with pytest.raises(TypeError):
        get_adjacent_buckets(0, 0, None)


def test_none_coordinate_raises_type_error(grid3):
    with pytest.raises(TypeError):
        get_adjacent_buckets(None, 1, grid3)
    with pytest.raises(TypeError):
        get_adjacent_buckets(1, None, grid3)


def test_string_coordinate_raises_type_error(grid3):
    with pytest.raises(TypeError):
        get_adjacent_buckets("1", 1, grid3)


def test_cx_out_of_range_raises_index_error(grid3):
    with pytest.raises(IndexError):
        get_adjacent_buckets(5, 1, grid3)


def test_cy_out_of_range_raises_index_error(grid3):
    with pytest.raises(IndexError):
        get_adjacent_buckets(1, 5, grid3)


def test_non_square_grid_more_columns_than_rows_raises_index_error():
    # 2 rows x 3 columns: b_length = 3, so cy + 1 = 2 is treated as valid
    grid = [
        [[1], [2], [3]],
        [[4], [5], [6]],
    ]
    with pytest.raises(IndexError):
        get_adjacent_buckets(0, 1, grid)


def test_float_coordinate_raises_type_error(grid3):
    with pytest.raises(TypeError):
        get_adjacent_buckets(1.0, 1, grid3)
