""" task2 """

def hajanian_word_to_english(word):
    """converts hajanian word to english on the assumption that all inputs are
    in lower case.
    """

    word = word.strip() # Remove trailing whitespace

    food = ["sausage!", "bacon!", "ham!"]
    if word in food: # Rule 9
        return word[:-1]

    if word == "oy":   # Rule 5
        return "is"
    if word == "argh": # Rule 6
        return "are"
    if word == "hana": # Rule 7
        return "he"
    if word == "hami": # Rule 8
        return "his"

    word = word.replace("uwu", "oo") # Rule 4

    if word[-4:] == "yeeh": # Rule 1
        word = word[:-3]
    elif (word[-5:] == "ingah") or (word[-4:] == "shey"): # Rule 2 and 3
        word = word[:-2]

    return word


def main():
    """ test the above function """

    test_words = ["companyeeh", "bringah", "wishey", "uwu", "buwulean",
                  "shuwu", "oy", "argh", "hana", "hami", "sausage!", "ham!",
                  "bacon!"]

    print("Conversions")

    for word in test_words:
        print(word + ":\t" + hajanian_word_to_english(word))

if __name__ == "__main__":
    main()
    