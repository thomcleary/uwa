""" task3 """

def row(board, row_num):
    """Return the given numbered row (0 - 2) of board"""
    return board[row_num]


def column(board, col_num):
    """Return the given numbered column (0 - 2) of board"""
    return [board[i][col_num] for i in range(3)]
