""" task6 """

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
