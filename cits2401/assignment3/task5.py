""" task5 """

def empty_squares(board):
    """Return a list of the empty squares in the board, each as
       a (row, column) tuple"""
    empty = []

    for i, board_row in enumerate(board):
        for j, curr_square in enumerate(board_row):
            if curr_square == " ":
                empty.append((i, j))

    return empty
