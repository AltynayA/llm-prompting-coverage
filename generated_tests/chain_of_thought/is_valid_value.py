import copy
import pytest


def make_empty_board():
    return [[0 for _ in range(9)] for _ in range(9)]


def make_solved_board():
    # Standard valid pattern for a solved sudoku
    return [[(r * 3 + r // 3 + c) % 9 + 1 for c in range(9)] for r in range(9)]


def make_partial_board():
    return [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7],
    ]


# ---------- Happy path ----------

def test_empty_board_any_number_valid():
    bo = make_empty_board()
    for num in range(1, 10):
        assert is_valid_value(bo, num, (4, 4)) is True


def test_partial_board_valid_number():
    bo = make_partial_board()
    assert is_valid_value(bo, 3, (0, 2)) is True


def test_solved_board_every_cell_valid_at_own_position():
    bo = make_solved_board()
    for r in range(9):
        for c in range(9):
            assert is_valid_value(bo, bo[r][c], (r, c)) is True


def test_number_in_different_row_col_box_is_valid():
    bo = make_empty_board()
    bo[0][0] = 5
    assert is_valid_value(bo, 5, (4, 4)) is True


# ---------- Conflicts ----------

def test_column_conflict():
    bo = make_empty_board()
    bo[7][2] = 5
    assert is_valid_value(bo, 5, (0, 2)) is False


def test_row_conflict():
    bo = make_empty_board()
    bo[3][8] = 5
    assert is_valid_value(bo, 5, (3, 0)) is False


def test_box_conflict_only():
    bo = make_empty_board()
    bo[0][0] = 5
    # (1,1): different row and column, same box
    assert is_valid_value(bo, 5, (1, 1)) is False


def test_box_conflict_middle_and_last_boxes():
    bo = make_empty_board()
    bo[3][3] = 7
    assert is_valid_value(bo, 7, (5, 5)) is False
    bo2 = make_empty_board()
    bo2[6][6] = 7
    assert is_valid_value(bo2, 7, (8, 8)) is False


def test_adjacent_box_is_not_conflict():
    bo = make_empty_board()
    bo[0][2] = 5
    # (1,3) is in a different box and different row/col
    assert is_valid_value(bo, 5, (1, 3)) is True


@pytest.mark.parametrize("num,expected", [
    (3, True),    # no conflict
    (7, False),   # row conflict
    (9, False),   # column conflict
    (6, False),   # box conflict
    (4, False),   # row conflict
])
def test_partial_board_parametrized(num, expected):
    bo = make_partial_board()
    assert is_valid_value(bo, num, (0, 2)) is expected


# ---------- Own cell handling ----------

def test_own_cell_is_ignored_with_tuple_pos():
    bo = make_empty_board()
    bo[4][4] = 9
    assert is_valid_value(bo, 9, (4, 4)) is True


def test_list_pos_does_not_match_tuple_in_box_check():
    # (rows, cols) != pos is always True when pos is a list,
    # so the cell's own value is counted in the box check.
    bo = make_empty_board()
    bo[4][4] = 9
    assert is_valid_value(bo, 9, [4, 4]) is False


# ---------- Edge cases ----------

def test_zero_conflicts_with_other_zeros():
    bo = make_empty_board()
    assert is_valid_value(bo, 0, (0, 0)) is False


def test_non_matching_type_num_is_valid():
    bo = make_empty_board()
    bo[0][0] = 5
    assert is_valid_value(bo, "5", (0, 1)) is True


def test_board_not_mutated():
    bo = make_partial_board()
    original = copy.deepcopy(bo)
    is_valid_value(bo, 3, (0, 2))
    is_valid_value(bo, 6, (0, 2))
    assert bo == original


def test_corner_positions():
    bo = make_empty_board()
    bo[8][8] = 2
    assert is_valid_value(bo, 2, (0, 8)) is False  # same column
    assert is_valid_value(bo, 2, (8, 0)) is False  # same row
    assert is_valid_value(bo, 2, (0, 0)) is True


# ---------- Errors ----------

def test_row_out_of_range_raises_index_error():
    bo = make_empty_board()
    with pytest.raises(IndexError):
        is_valid_value(bo, 1, (9, 0))


def test_col_out_of_range_raises_index_error():
    bo = make_empty_board()
    with pytest.raises(IndexError):
        is_valid_value(bo, 1, (0, 9))


def test_empty_board_raises_index_error():
    with pytest.raises(IndexError):
        is_valid_value([], 1, (0, 0))


def test_none_pos_raises_type_error():
    bo = make_empty_board()
    with pytest.raises(TypeError):
        is_valid_value(bo, 1, None)


def test_none_board_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_value(None, 1, (0, 0))


def test_short_pos_raises_index_error():
    bo = make_empty_board()
    with pytest.raises(IndexError):
        is_valid_value(bo, 1, (0,))
