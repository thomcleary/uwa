""" task4 """

TOP_LEFT_BOTTOM_RIGHT = 0
TOP_RIGHT_BOTTOM_LEFT = 1

def diagonal(board, diagonal_selector):
    """Return the 3 element diagonal of the board selected by
       diagonal_selector, one of TOP_LEFT_BOTTOM_RIGHT or
       TOP_RIGHT_BOTTOM_LEFT
    """
    if diagonal_selector == TOP_LEFT_BOTTOM_RIGHT:
        return [board[i][i] for i in range(3)]

    return [board[i][j] for (i, j) in zip(range(3), range(2, -1, -1))]
