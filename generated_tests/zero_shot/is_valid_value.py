import copy
import pytest


@pytest.fixture
def board():
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


def test_valid_number_in_empty_cell(board):
    assert is_valid_value(board, 3, (0, 2)) is True


def test_valid_number_bottom_right_corner(board):
    assert is_valid_value(board, 3, (8, 8)) is True


def test_column_conflict(board):
    # 9 already exists in column 2 (row 8); not in row 0 or top-left box
    assert is_valid_value(board, 9, (0, 2)) is False


def test_row_conflict(board):
    # 2 already exists in row 0 (col 7); not in column 2 or top-left box
    assert is_valid_value(board, 2, (0, 2)) is False


def test_box_conflict(board):
    # 6 exists in the top-left box at (1, 0); not in row 0 or column 2
    assert is_valid_value(board, 6, (0, 2)) is False


def test_box_conflict_bottom_right(board):
    # 1 exists in bottom-right box at (6, 7); not in row 8 or column 8
    assert is_valid_value(board, 1, (8, 8)) is False


def test_existing_value_at_own_position_is_valid(board):
    # The cell itself must be ignored when checking (tuple position)
    assert is_valid_value(board, 7, (0, 0)) is True
    assert is_valid_value(board, 5, (4, 4)) is True


def test_list_position_does_not_match_tuple_self_check(board):
    # (rows, cols) != pos is always True when pos is a list, so the cell
    # itself is treated as a conflict in the box check
    assert is_valid_value(board, 7, [0, 0]) is False


def test_zero_is_conflict_when_other_empty_cells_exist(board):
    # Zero represents empty cells, so placing 0 conflicts with other zeros
    assert is_valid_value(board, 0, (0, 2)) is False


def test_board_not_mutated(board):
    original = copy.deepcopy(board)
    is_valid_value(board, 3, (0, 2))
    is_valid_value(board, 9, (0, 2))
    assert board == original


def test_empty_board_raises_index_error():
    with pytest.raises(IndexError):
        is_valid_value([], 1, (0, 0))


def test_row_out_of_range_raises_index_error(board):
    with pytest.raises(IndexError):
        is_valid_value(board, 3, (9, 0))


def test_column_out_of_range_raises_index_error(board):
    with pytest.raises(IndexError):
        is_valid_value(board, 3, (0, 9))


def test_none_position_raises_type_error(board):
    with pytest.raises(TypeError):
        is_valid_value(board, 3, None)


def test_none_board_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_value(None, 3, (0, 0))
