""" task 3 """

def valid_words(dictionary, sentence):
    """ returns all words in dictionary that appear in sentence """

    dictionary = dictionary.split()
    sentence = sentence.split()

    valid = []

    for word in sentence:
        if word in dictionary:
            valid.append(word)

    return valid


def main():
    """ tests above function """
    dictionary = "a aa apple banana pear strawberry mango"
    sentence = "hello mango and banana yum apple!"
    print(valid_words(dictionary, sentence))
    print()

    print(valid_words(dictionary, dictionary))


if __name__ == "__main__":
    main()
