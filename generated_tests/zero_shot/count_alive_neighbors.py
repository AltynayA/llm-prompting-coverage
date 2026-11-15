import pytest


def make_grid(width, height, fill=0):
    return [[fill for _ in range(width)] for _ in range(height)]


def test_all_dead_interior_cell_has_zero_neighbors():
    grid = make_grid(5, 5, 0)
    assert count_alive_neighbors(grid, 2, 2) == 0


def test_all_alive_interior_cell_has_eight_neighbors():
    grid = make_grid(5, 5, 1)
    assert count_alive_neighbors(grid, 2, 2) == 8


def test_center_cell_itself_is_not_counted():
    grid = make_grid(5, 5, 0)
    grid[2][2] = 1
    assert count_alive_neighbors(grid, 2, 2) == 0


@pytest.mark.parametrize("n_alive", [1, 2, 3, 5])
def test_partial_alive_neighbors_counted(n_alive):
    grid = make_grid(7, 7, 0)
    # neighbors of (3, 3) as (x, y)
    neighbors = [(2, 2), (3, 2), (4, 2), (2, 3), (4, 3), (2, 4), (3, 4), (4, 4)]
    for nx, ny in neighbors[:n_alive]:
        grid[ny][nx] = 1
    assert count_alive_neighbors(grid, 3, 3) == n_alive


def test_grid_indexed_as_y_then_x_on_non_square_grid():
    # width 7, height 5
    grid = make_grid(7, 5, 0)
    grid[1][4] = 1  # y=1, x=4 -> neighbor of (3, 2)
    assert count_alive_neighbors(grid, 3, 2) == 1
    grid2 = make_grid(7, 5, 0)
    grid2[2][3] = 1  # the cell itself
    assert count_alive_neighbors(grid2, 3, 2) == 0


def test_cell_near_top_left_edge_counts_border_as_alive():
    grid = make_grid(5, 5, 0)
    # Neighbors with x==0 or y==0 are treated as alive: 5 of them
    assert count_alive_neighbors(grid, 1, 1) == 5


def test_cell_near_bottom_right_edge_counts_border_as_alive():
    grid = make_grid(5, 5, 0)
    # neighbors with x==4 or y==4 are border: 5 of 8
    assert count_alive_neighbors(grid, 3, 3) == 5


def test_corner_cell_all_dead_interior():
    grid = make_grid(5, 5, 0)
    # Only neighbor (1,1) is interior and dead; other 7 are out-of-bounds/edge
    assert count_alive_neighbors(grid, 0, 0) == 7


def test_corner_cell_with_alive_interior_neighbor():
    grid = make_grid(5, 5, 0)
    grid[1][1] = 1
    assert count_alive_neighbors(grid, 0, 0) == 8


def test_three_by_three_grid_center_always_eight():
    assert count_alive_neighbors(make_grid(3, 3, 0), 1, 1) == 8
    assert count_alive_neighbors(make_grid(3, 3, 1), 1, 1) == 8


def test_single_cell_grid_returns_eight():
    assert count_alive_neighbors([[0]], 0, 0) == 8


def test_coordinates_far_outside_grid_count_all_alive():
    grid = make_grid(5, 5, 0)
    assert count_alive_neighbors(grid, 100, 100) == 8
    assert count_alive_neighbors(grid, -50, -50) == 8


def test_values_other_than_one_are_not_counted():
    grid = make_grid(5, 5, 0)
    grid[1][1] = 2
    grid[1][2] = -1
    grid[1][3] = 1
    assert count_alive_neighbors(grid, 2, 2) == 1


def test_empty_grid_raises_index_error():
    with pytest.raises(IndexError):
        count_alive_neighbors([], 0, 0)


def test_none_grid_raises_type_error():
    with pytest.raises(TypeError):
        count_alive_neighbors(None, 1, 1)


def test_none_coordinates_raise_type_error():
    grid = make_grid(5, 5, 0)
    with pytest.raises(TypeError):
        count_alive_neighbors(grid, None, 2)
    with pytest.raises(TypeError):
        count_alive_neighbors(grid, 2, None)


def test_string_coordinates_raise_type_error():
    grid = make_grid(5, 5, 0)
    with pytest.raises(TypeError):
        count_alive_neighbors(grid, "2", 2)
