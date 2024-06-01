""" task10 """


BOARD_X_WIN = [["X", "X", " "], ["X", "O", "O"], ["X", "O", "O"]]
BOARD_O_WIN = [["O", "X", " "], ["X", "O", "X"], ["X", " ", "O"]]
BOARD_NO_WIN = [["O", "X", " "], ["X", " ", "X"], ["X", " ", "O"]]


def empty_squares(board):
    """Return a list of the empty squares in the board, each as
       a (row, column) tuple"""
    empty = []

    for i, board_row in enumerate(board):
        for j, curr_square in enumerate(board_row):
            if curr_square == " ":
                empty.append((i, j))

    return empty


def make_human_move(current_player, board):
    """Given a board state and the human piece ('O' or 'X')
       ask the player for a location to play in. Repeat until a
       valid response is given. Then make the move, i.e., update
       the board by setting the chosen square to the player's piece.
    """
    print("{}'s move".format(current_player))

    valid_move = False

    while not valid_move:
        move = input("Enter row and column [0 - 2]: ").split()

        for index, num in enumerate(move):
            move[index] = int(num)

        if (move[0] < 0 or move[0] > 2) or \
           (move[1] < 0 or move[1] > 2) or \
           (tuple(move) not in empty_squares(board)):
            print("Illegal move. Try again.")

        else:
            valid_move = True

    board[move[0]][move[1]] = current_player
