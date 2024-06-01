"""Tic Tac Toe assignment for CITS2401
   Rewritten by Jin Hong
   1 Nov 2019
"""
from random import randint


# Define two constants, the values used to select a diagonal
TOP_LEFT_BOTTOM_RIGHT = 0
TOP_RIGHT_BOTTOM_LEFT = 1

# **********************************************************************
#
# Define all the functions that manipulate the board.
# Only these functions should 'know' the board representation.
# These functions don't "know" anything about noughts and crosses;
# only that it's played on a 3 x 3 board of 'O's and 'X's (and blanks).
#
# **********************************************************************
def new_board():
    """ Generate and return a new empty board """
    return [[" "] * 3 for _ in range(3)]


def display(board):
    """Display the given board"""
    separator = '+---+---+---+'
    print(separator)
    for row in board:
        print('|', end='')
        for col in row:
            print(' {} |'.format(col), end='')
        print('\n' + separator)
    print()


def square(board, row, column):
    """Return the contents of square (row, column) of board.
       The value is either 'O', 'X' or ' '
    """
    return board[row][column]


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


# **********************************************************************
#
# Now we have some functions that test the board state in various
# ways. These are related to the rules of noughts and crosses.
# They do not "know" about the represention used for a board.
#
# **********************************************************************
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


# **********************************************************************
#
# Now the top-level functions that implement the logic of
# noughts and crosses.
#
# **********************************************************************
def game_result(board):
    """Return 'Won by O', 'Won by X' or 'Draw' according to the
       state of board. It is assume the game is over."""
    game_winner = winner(board)

    if game_winner == "X":
        return "Won by X"
    if game_winner == "O":
        return "Won by O"

    return "Draw" # If game_winner is None


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


def make_computer_move(current_player, board):
    """Given a board state and the computer piece ('O' or 'X')
       choose a square for the computer to play in and
       make the move (i.e., update the board accordingly).
    """
    candidates = empty_squares(board)
    choice = randint(0, len(candidates) - 1)
    row, column = candidates[choice]
    print("Computer plays at ({},{})".format(row, column))
    board[row][column] = current_player


def play_game(human_player, board):
    """Play until a win or a draw"""
    current_player = human_player

    while not game_over(board):
        display(board)
        play_one_turn(board, current_player, human_player)
        current_player = other_player(current_player)

    return game_result(board)


def play_one_turn(board, current_player, human_player):
    """Given a board state and the current
       player ('O' or 'X'), play one move
    """
    if human_player == current_player:
        make_human_move(current_player, board)
    else:
        make_computer_move(current_player, board)


def other_player(player):
    """Return X if player is O else return O"""
    if player == "X":
        return "O"
    return "X"


# ASK WHAT THIS FUNCTION IS MEANT TO RETURN
# NOT CLEAR IN ASSIGNMENT INSTRUCTIONS
def get_O_or_X():
    """Ask the human if they want to play O or X and return their
       choice"""
    shapes = ["X", "O"]
    player_shape = ""

    while player_shape not in shapes:
        player_shape = input("Would you like to play O or X? ")

    return player_shape


def main():
    """Play a game of noughts and crosses"""
    board = new_board()
    human_player = get_O_or_X()

    try:
        result = play_game(human_player, board)
        display(board)
        print(result)
    except ValueError:
        print("The program has encountered an error and needs to die. Bye.")


main()
