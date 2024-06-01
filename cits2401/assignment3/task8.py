""" task8 """


TOP_LEFT_BOTTOM_RIGHT = 0
TOP_RIGHT_BOTTOM_LEFT = 1
BOARD_X_WIN = [["X", "X", " "], ["X", "O", "O"], ["X", "O", "O"]]
BOARD_O_WIN = [["O", "X", " "], ["X", "O", "X"], ["X", " ", "O"]]
BOARD_NO_WIN = [["O", "X", " "], ["X", " ", "X"], ["X", " ", "O"]]


def row(board, row_num):
    """Return the given numbered row (0 - 2) of board"""
    return board[row_num]


def column(board, col_num):
    """Return the given numbered column (0 - 2) of board"""
    return [board[i][col_num] for i in range(3)]


def diagonal(board, diagonal_selector):
    """Return the 3 element diagonal of the board selected by
       diagonal_selector, one of TOP_LEFT_BOTTOM_RIGHT or
       TOP_RIGHT_BOTTOM_LEFT
    """

    if diagonal_selector == TOP_LEFT_BOTTOM_RIGHT:
        return [board[i][i] for i in range(3)]

    return [board[i][j] for (i, j) in zip(range(3), range(2, -1, -1))]


def empty_squares(board):
    """Return a list of the empty squares in the board, each as
       a (row, column) tuple"""
    empty = []

    for i, board_row in enumerate(board):
        for j, curr_square in enumerate(board_row):
            if curr_square == " ":
                empty.append((i, j))

    return empty


def line_winner(line):
    """Return 'O' or 'X' if all elements in the 3-element list line
       are the same and non-blank. Otherwise return None"""
    first_square = line[0]

    if first_square == " ":
        return None

    for curr_square in line[1:]:
        if curr_square != first_square:
            return None

    return first_square


def winner(board):
    """Return 'O' or 'X' if either of those has won the game.
       Otherwise return None. It is assumed there can be only a
       single winning line."""

    # Check rows
    for row_num in range(3):
        result = line_winner(row(board, row_num))
        if result is not None:
            return result

    # Check columns
    for col_num in range(3):
        result = line_winner(column(board, col_num))
        if result is not None:
            return result

    # Check TOP_LEFT_BOTTOM_RIGHT
    result = line_winner(diagonal(board, TOP_LEFT_BOTTOM_RIGHT))
    if result is not None:
        return result

    # Check TOP_RIGHT_BOTTOM_LEFT
    result = line_winner(diagonal(board, TOP_RIGHT_BOTTOM_LEFT))
    if result is not None:
        return result

    return None # No winner found


def game_over(board):
    """Given a board state return true iff there's a winner or
       if the game is drawn."""
    return (winner(board) is not None) or (len(empty_squares(board)) == 0)
