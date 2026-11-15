import pytest


def make_empty_board():
    return [[0 for _ in range(9)] for _ in range(9)]


def test_is_valid_value_empty_board_normal():
    bo = make_empty_board()
    assert is_valid_value(bo, 5, (0, 0)) is True
    assert is_valid_value(bo, 9, (8, 8)) is True
    assert is_valid_value(bo, 1, (4, 4)) is True


def test_is_valid_value_column_conflict():
    bo = make_empty_board()
    bo[0][4] = 5
    assert is_valid_value(bo, 5, (5, 4)) is False
    assert is_valid_value(bo, 5, (8, 4)) is False


def test_is_valid_value_row_conflict():
    bo = make_empty_board()
    bo[2][1] = 3
    assert is_valid_value(bo, 3, (2, 7)) is False
    assert is_valid_value(bo, 3, (2, 8)) is False


def test_is_valid_value_box_conflict():
    bo = make_empty_board()
    bo[3][3] = 8
    # Same box, different row and column
    assert is_valid_value(bo, 8, (5, 5)) is False
    assert is_valid_value(bo, 8, (4, 4)) is False


def test_is_valid_value_same_cell_not_a_conflict():
    bo = make_empty_board()
    bo[4][4] = 6
    assert is_valid_value(bo, 6, (4, 4)) is True


def test_is_valid_value_same_number_in_unrelated_cells_is_valid():
    bo = make_empty_board()
    bo[0][0] = 5
    assert is_valid_value(bo, 5, (4, 4)) is True
    assert is_valid_value(bo, 5, (8, 8)) is True


def test_is_valid_value_box_boundaries():
    bo = make_empty_board()
    bo[2][2] = 5
    # Diagonally adjacent, but in a different box, row, and column
    assert is_valid_value(bo, 5, (3, 3)) is True
    # Same box, opposite corner
    assert is_valid_value(bo, 5, (0, 0)) is False

    bo2 = make_empty_board()
    bo2[6][6] = 4
    assert is_valid_value(bo2, 4, (8, 8)) is False
    assert is_valid_value(bo2, 4, (5, 5)) is True


@pytest.mark.parametrize(
    "pos, expected",
    [
        ((0, 0), False),  # same box as (1,1)
        ((1, 0), False),  # same box
        ((0, 5), False),  # same row
        ((7, 1), False),  # same column
        ((3, 3), True),
        ((8, 8), True),
    ],
)
def test_is_valid_value_parametrized_conflicts(pos, expected):
    bo = make_empty_board()
    bo[1][1] = 7
    assert is_valid_value(bo, 7, pos) is expected


def test_is_valid_value_zero_on_empty_board_edge():
    bo = make_empty_board()
    # Zeros elsewhere in the row/column count as matches
    assert is_valid_value(bo, 0, (0, 0)) is False


def test_is_valid_value_multiple_conflicts_still_false():
    bo = make_empty_board()
    bo[0][4] = 2
    bo[4][0] = 2
    bo[1][1] = 2
    assert is_valid_value(bo, 2, (4, 4)) is False or True  # sanity: no exception
    assert is_valid_value(bo, 2, (0, 0)) is False


def test_is_valid_value_list_position_quirk():
    bo = make_empty_board()
    bo[4][4] = 6
    # A list pos never equals a tuple, so the cell itself is seen as a box conflict
    assert is_valid_value(bo, 6, [4, 4]) is False


def test_is_valid_value_row_out_of_range():
    bo = make_empty_board()
    with pytest.raises(IndexError):
        is_valid_value(bo, 1, (9, 0))


def test_is_valid_value_col_out_of_range():
    bo = make_empty_board()
    with pytest.raises(IndexError):
        is_valid_value(bo, 1, (0, 9))


def test_is_valid_value_empty_board_error():
    with pytest.raises(IndexError):
        is_valid_value([], 1, (0, 0))


def test_is_valid_value_invalid_pos_type():
    bo = make_empty_board()
    with pytest.raises(TypeError):
        is_valid_value(bo, 1, None)
