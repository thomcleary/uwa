""" task5 """

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


def valid_words(dictionary, sentence):
    """ returns all words in dictionary that appear in sentence """

    dictionary = dictionary.split()
    sentence = sentence.split()

    valid = []

    for word in sentence:
        if word in dictionary:
            valid.append(word)

    return valid


def beautify_sentence(sentence, punctuation):
    """ removes characters in punctuation from the beginning and end of words
    in sentence
    """

    sentence = sentence.split()

    beautified = []
    for word in sentence:
        while word[0] in punctuation:
            word = word[1:]
        while word[-1] in punctuation:
            word = word[:-1]

        beautified.append(word)

    beautified_sentence = " ".join(beautified)
    return beautified_sentence


def translate(sentence, dictionary, punctuation, language):
    """ Translates sentence from english->hajanian if language == "english"
    or hajanian->english if language == "hajanian".
    Returns the translated sentence else an empty string if an invalid language
    is given.
    """
    if sentence != "":
        sentence = beautify_sentence(sentence, punctuation)

    if dictionary == "":
        dictionary = sentence

    sentence_valid_words = valid_words(dictionary, sentence)

    translated_words = []

    if language.lower() == "english":
        for word in sentence_valid_words:
            translated_words.append(english_word_to_hajanian(word))

    elif language.lower() == "hajanian":
        for word in sentence_valid_words:
            translated_words.append(hajanian_word_to_english(word))

    else:
        print("invalid language.")
        return ""

    return " ".join(translated_words)


def main():
    """ tests translate() """
    print("Test 1")
    sentence = "?hello boolean bring, !mango! and, country ban,ana wish yum apple!"
    dictionary = "a aa apple banana pear strawberry mango country wish boolean bring"
    punctuation = "?!,"
    language = "english"
    expected = "buwulean bringah mango countryeeh wishey apple"
    translated = translate(sentence, dictionary, punctuation, language)
    print("Translated: " + translated)
    print("Equals expected: " + str(translated == expected) + "\n")

    print("Test 2")
    sentence = "hello mango and banana yum apple!"
    dictionary = "a aa apple banana pear strawberry mango country wish boolean bring"
    punctuation = "?!,"
    language = "english"
    expected = "mango banana apple"
    translated = translate(sentence, dictionary, punctuation, language)
    print("Translated: " + translated)
    print("Equals expected: " + str(translated == expected) + "\n")

    print("Test 3")
    sentence = "hello mango and banana yum apple!"
    dictionary = "a aa apple banana pear strawberry mango country wish boolean bring"
    punctuation = "?!,"
    language = "german"
    expected = ""
    translated = translate(sentence, dictionary, punctuation, language)
    print("Translated: " + translated)
    print("Equals expected: " + str(translated == expected) + "\n")


if __name__ == "__main__":
    main()
