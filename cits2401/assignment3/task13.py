""" task13 """

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
