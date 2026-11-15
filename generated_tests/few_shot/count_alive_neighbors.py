import pytest


def make_grid(width, height, value=0):
    return [[value for _ in range(width)] for _ in range(height)]


def test_count_alive_neighbors_all_dead_interior():
    grid = make_grid(5, 5, 0)
    assert count_alive_neighbors(grid, 2, 2) == 0


def test_count_alive_neighbors_all_alive_interior():
    grid = make_grid(5, 5, 1)
    assert count_alive_neighbors(grid, 2, 2) == 8


def test_count_alive_neighbors_some_alive_interior():
    grid = make_grid(5, 5, 0)
    grid[1][1] = 1
    grid[3][3] = 1
    assert count_alive_neighbors(grid, 2, 2) == 2


def test_count_alive_neighbors_ignores_center_cell():
    grid = make_grid(5, 5, 0)
    grid[2][2] = 1
    assert count_alive_neighbors(grid, 2, 2) == 0


def test_count_alive_neighbors_x_is_column_y_is_row():
    grid = make_grid(7, 7, 0)
    grid[1][4] = 1  # row 1, column 4
    assert count_alive_neighbors(grid, 3, 2) == 1
    assert count_alive_neighbors(grid, 2, 3) == 0


def test_count_alive_neighbors_corner_counts_edges_as_alive():
    grid = make_grid(5, 5, 0)
    assert count_alive_neighbors(grid, 0, 0) == 7
    grid[1][1] = 1
    assert count_alive_neighbors(grid, 0, 0) == 8


def test_count_alive_neighbors_near_top_left_edge():
    grid = make_grid(5, 5, 0)
    assert count_alive_neighbors(grid, 1, 1) == 5


def test_count_alive_neighbors_near_bottom_right_edge():
    grid = make_grid(5, 5, 0)
    assert count_alive_neighbors(grid, 3, 3) == 5


def test_count_alive_neighbors_tiny_grid_all_border():
    grid = make_grid(3, 3, 0)
    assert count_alive_neighbors(grid, 1, 1) == 8


def test_count_alive_neighbors_non_square_grid():
    grid = make_grid(6, 4, 0)
    assert count_alive_neighbors(grid, 2, 1) == 3
    grid[2][3] = 1
    assert count_alive_neighbors(grid, 2, 1) == 4


def test_count_alive_neighbors_far_outside_grid():
    grid = make_grid(5, 5, 0)
    assert count_alive_neighbors(grid, 10, 10) == 8


def test_count_alive_neighbors_empty_grid_error():
    with pytest.raises(IndexError):
        count_alive_neighbors([], 0, 0)


def test_count_alive_neighbors_invalid_grid_type():
    with pytest.raises(TypeError):
        count_alive_neighbors(None, 1, 1)
