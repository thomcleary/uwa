""" task4 """

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

def main():
    """ tests above function """

    sentence = "?hello !mango!! and, ban,ana yum apple!"
    punctuation = "?!,"

    beautified = beautify_sentence(sentence, punctuation)
    print(beautified)

    expected = "hello mango and ban,ana yum apple"
    print(beautified == expected)

if __name__ == "__main__":
    main()
