""" task1 """

def english_word_to_hajanian(word):
    """ Converts an English word into a Hahanian word on the assumption that
     words area always given in lower case.
     """

    word = word.strip() # Remove trailing whitespace

    oy_ = ["is"]
    argh = ["are"]
    hana = ["he", "she", "it"]
    hami = ["his", "her"]
    food = ["ham", "sausage", "bacon"]

    if word in oy_:     # Rule 5
        return "oy"
    if word in argh: # Rule 6
        return "argh"
    if word in hana: # Rule 7
        return "hana"
    if word in hami: # Rule 8
        return "hami"
    if word in food: # Rule 9
        return word + "!"

    word = word.replace("oo", "uwu") # Rule 4

    if word[-1] == "y":      # Rule 1
        word += "eeh"

    elif word[-3:] == "ing": # Rule 2
        word += "ah"

    elif word[-2:] == "sh":  # Rule 3
        word += "ey"

    return word


def main():
    """ tests the above function """
    test_words = ["company", "bring", "wish", "boolean", "shoo", "is", "are", \
                  "he", "she", "it", "his", "her", "ham", "sausage", "bacon"]

    print("Conversions")

    for word in test_words:
        print(word + ":\t" + english_word_to_hajanian(word))

if __name__ == "__main__":
    main()
