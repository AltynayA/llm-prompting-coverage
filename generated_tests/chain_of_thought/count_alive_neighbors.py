import copy
import pytest


def make_grid(width, height, value=0):
    return [[value for _ in range(width)] for _ in range(height)]


# ---------- Happy path ----------

def test_all_dead_interior_cell_has_zero_alive_neighbors():
    grid = make_grid(5, 5, 0)
    assert count_alive_neighbors(grid, 2, 2) == 0


def test_all_alive_interior_cell_has_eight_alive_neighbors():
    grid = make_grid(5, 5, 1)
    assert count_alive_neighbors(grid, 2, 2) == 8


def test_single_alive_neighbor_is_counted():
    grid = make_grid(5, 5, 0)
    grid[1][2] = 1  # y=1, x=2 -> directly above the center
    assert count_alive_neighbors(grid, 2, 2) == 1


def test_multiple_alive_neighbors_counted():
    grid = make_grid(5, 5, 0)
    grid[1][1] = 1
    grid[3][3] = 1
    grid[2][3] = 1
    assert count_alive_neighbors(grid, 2, 2) == 3


def test_center_cell_itself_is_not_counted():
    grid = make_grid(5, 5, 0)
    grid[2][2] = 1
    assert count_alive_neighbors(grid, 2, 2) == 0


def test_values_other_than_one_are_not_counted():
    grid = make_grid(5, 5, 0)
    grid[2][3] = 2
    grid[1][2] = -1
    assert count_alive_neighbors(grid, 2, 2) == 0


def test_grid_is_not_mutated():
    grid = make_grid(5, 5, 0)
    grid[1][2] = 1
    original = copy.deepcopy(grid)
    count_alive_neighbors(grid, 2, 2)
    assert grid == original


# ---------- Boundary behaviour ----------

def test_cell_next_to_border_counts_border_as_alive():
    grid = make_grid(5, 5, 0)
    # neighbors at x=0 or y=0 are border -> 5 alive; remaining 3 are dead interior
    assert count_alive_neighbors(grid, 1, 1) == 5


def test_cell_at_origin_counts_border_neighbors():
    grid = make_grid(5, 5, 0)
    # all neighbors except (1,1) are out of / on the border
    assert count_alive_neighbors(grid, 0, 0) == 7


def test_border_cells_count_alive_even_if_grid_value_is_zero():
    grid = make_grid(5, 5, 0)
    # center at (3,3): neighbors include x=4 and y=4 which are border (>= size-1)
    assert count_alive_neighbors(grid, 3, 3) == 5


def test_border_cells_alive_regardless_of_actual_grid_values():
    grid_dead = make_grid(5, 5, 0)
    grid_alive = make_grid(5, 5, 0)
    for i in range(5):
        grid_alive[0][i] = 1
        grid_alive[4][i] = 1
        grid_alive[i][0] = 1
        grid_alive[i][4] = 1
    assert count_alive_neighbors(grid_dead, 1, 1) == count_alive_neighbors(grid_alive, 1, 1)


def test_3x3_grid_center_all_neighbors_are_border():
    grid = make_grid(3, 3, 0)
    assert count_alive_neighbors(grid, 1, 1) == 8


def test_coordinates_far_outside_grid_return_eight():
    grid = make_grid(5, 5, 0)
    assert count_alive_neighbors(grid, 100, 100) == 8


def test_negative_coordinates_return_eight():
    grid = make_grid(5, 5, 0)
    assert count_alive_neighbors(grid, -5, -5) == 8


# ---------- Non-square grid: x indexes columns, y indexes rows ----------

def test_non_square_grid_uses_x_for_column_and_y_for_row():
    grid = make_grid(6, 4, 0)  # width 6, height 4
    # center (2,1): row y=0 is border (3 alive); others interior and dead
    assert count_alive_neighbors(grid, 2, 1) == 3
    grid[1][3] = 1  # y=1, x=3 -> right neighbor of (2,1)
    assert count_alive_neighbors(grid, 2, 1) == 4


def test_non_square_grid_wide_right_edge():
    grid = make_grid(6, 4, 0)
    # center (4,1): x=5 is border (>= width-1) -> 3 alive; y=0 border adds more
    # neighbors: x in 3..5, y in 0..2
    # border: y=0 row (3) + x=5 for y=1,2 (2) = 5; interior dead: (3,1),(3,2),(4,2)
    assert count_alive_neighbors(grid, 4, 1) == 5


# ---------- Error cases ----------

def test_empty_grid_raises_index_error():
    with pytest.raises(IndexError):
        count_alive_neighbors([], 0, 0)


def test_none_grid_raises_type_error():
    with pytest.raises(TypeError):
        count_alive_neighbors(None, 1, 1)


def test_none_coordinate_raises_type_error():
    grid = make_grid(5, 5, 0)
    with pytest.raises(TypeError):
        count_alive_neighbors(grid, None, 2)


def test_float_coordinate_raises_type_error_for_interior_access():
    grid = make_grid(5, 5, 0)
    with pytest.raises(TypeError):
        count_alive_neighbors(grid, 2.0, 2.0)


def test_string_coordinate_raises_type_error():
    grid = make_grid(5, 5, 0)
    with pytest.raises(TypeError):
        count_alive_neighbors(grid, "2", 2)
