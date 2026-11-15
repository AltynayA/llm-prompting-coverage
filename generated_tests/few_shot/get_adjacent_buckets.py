import pytest


@pytest.fixture
def grid3():
    return [
        [[1], [2], [3]],
        [[4], [5], [6]],
        [[7], [8], [9]],
    ]


def test_get_adjacent_buckets_center(grid3):
    result = get_adjacent_buckets(1, 1, grid3)
    assert result == [4, 1, 2, 3, 6, 9, 8, 7, 5]
    assert sorted(result) == list(range(1, 10))


def test_get_adjacent_buckets_top_left_corner(grid3):
    assert get_adjacent_buckets(0, 0, grid3) == [2, 5, 4, 1]


def test_get_adjacent_buckets_bottom_right_corner(grid3):
    assert get_adjacent_buckets(2, 2, grid3) == [8, 5, 6, 9]


def test_get_adjacent_buckets_top_right_corner(grid3):
    assert get_adjacent_buckets(2, 0, grid3) == [2, 6, 5, 3]


def test_get_adjacent_buckets_bottom_left_corner(grid3):
    assert get_adjacent_buckets(0, 2, grid3) == [4, 5, 8, 7]


def test_get_adjacent_buckets_top_edge(grid3):
    assert get_adjacent_buckets(1, 0, grid3) == [1, 3, 6, 5, 4, 2]


def test_get_adjacent_buckets_bottom_edge(grid3):
    assert get_adjacent_buckets(1, 2, grid3) == [7, 4, 5, 6, 9, 8]


def test_get_adjacent_buckets_single_cell():
    buckets = [[[1, 2]]]
    assert get_adjacent_buckets(0, 0, buckets) == [1, 2]


def test_get_adjacent_buckets_all_empty_cells():
    buckets = [[[], [], []], [[], [], []], [[], [], []]]
    assert get_adjacent_buckets(1, 1, buckets) == []


def test_get_adjacent_buckets_multi_element_cells():
    buckets = [[[1, 2], [3]], [[], [4, 5]]]
    assert get_adjacent_buckets(0, 0, buckets) == [3, 4, 5, 1, 2]


def test_get_adjacent_buckets_does_not_mutate_input(grid3):
    result = get_adjacent_buckets(1, 1, grid3)
    result.append(100)
    assert grid3 == [
        [[1], [2], [3]],
        [[4], [5], [6]],
        [[7], [8], [9]],
    ]
    assert result is not grid3[1][1]


def test_get_adjacent_buckets_x_out_of_range(grid3):
    with pytest.raises(IndexError):
        get_adjacent_buckets(5, 1, grid3)


def test_get_adjacent_buckets_y_out_of_range(grid3):
    with pytest.raises(IndexError):
        get_adjacent_buckets(0, 5, grid3)


def test_get_adjacent_buckets_empty_buckets():
    with pytest.raises(IndexError):
        get_adjacent_buckets(0, 0, [])


def test_get_adjacent_buckets_non_square_grid_raises():
    buckets = [[[1], [2], [3]], [[4], [5], [6]]]
    with pytest.raises(IndexError):
        get_adjacent_buckets(1, 1, buckets)


def test_get_adjacent_buckets_invalid_type():
    with pytest.raises(TypeError):
        get_adjacent_buckets(0, 0, None)
