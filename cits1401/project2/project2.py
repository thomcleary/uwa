# CITS1401: Computational Thinking with Python
# Project 2

# Name: Thomas Cleary
# Student Number: 21704985


import math


# Takes a filename and trys to open it.
# Returns None if there is an error opening the file.
# Else returns String of the contents of the file.
def read_file(file_name):

    try:
        text_file = open(file_name, "r")

    except FileNotFoundError:
        error("File Not Found")
        return None

    text = text_file.read().strip("\n") + " "
    text_file.close()
    return text


# Takes String of a text file and Boolean normalize
# Returns None if there is not atleast 1 complete sentence in the text.
# Else returns the Profile of the text as a dictionary.
def create_profile(text, normalize):

    counted = ["also", "although", "and", "as", "because", "before", "but",
               "for", "if", "nor", "of", "or", "since", "that", "though",
               "until", "when", "whenever", "whereas", "which", "while",
               "yet", ",", ";", "'", "-", "sents_per_para", "words_per_sent"]

    profile = {}
    for item in counted:
        profile[item] = 0

    text = list(text)
    num_sentences = 0
    index = 0

    for char in text:
        remove = False

        # Removes extra new line characters so paragraph spaces are
        # only ever '\n\n'
        if char == "\n":
            if text[index + 2] == "\n":
                remove = True

        elif char in [".", "?", "!"]:
            if text[index+1] in [" ", "\t", "\n", '"', "'"]:
                num_sentences += 1
            remove = True

        elif char in [",", ";"]:
            profile[char] += 1
            remove = True

        elif char in ["'", "-"]:
            if (text[index-1] + text[index+1]).isalnum():
                profile[char] += 1
            else:
                remove = True

        elif char in ['"', "#", "$", "%", "&", "(", ")", "*", "+", "/", ":",
                      "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`",
                      "{", "|", "}", "~"]:

            remove = True

        if remove:
            text[index] = " "

        index += 1

    if num_sentences == 0:
        error("File Does Not Contain A Complete Sentence.")
        return None

    clean_text = "".join(text)
    num_paragraphs = clean_text.count("\n\n") + 1

    words = clean_text.split()

    num_words = len(words)

    profile["sents_per_para"] = num_sentences / num_paragraphs
    profile["words_per_sent"] = num_words / num_sentences

    for word in words:
        word = word.lower()
        if word in counted:
            profile[word] += 1

    if normalize:
        normalize_profile(profile, num_sentences)

    return profile


# Takes a text file's profile and the number of sentences in the file.
# Returns a normalized version of the profile.
def normalize_profile(profile, num_sentences):
    for key in profile:
        if key in ["sents_per_para", "words_per_sent"]:
            continue

        profile[key] = profile[key] / num_sentences


# Takes 2 profiles of text files
# Returns the overall distance between the values in each profile.
def profile_distance(profile1, profile2):
    total = 0

    for key in profile1.keys():
        total += (profile1[key] - profile2[key]) ** 2

    distance = math.sqrt(total)

    return distance


# Takes a profile and the corresponding file name
# Displays a listing of the values within that profile.
def display_listing(profile, filename):
    keys = profile.keys()

    title = "Profile of " + filename

    print("{0}".format(title))
    print("-" * len(title))

    for key in keys:
        print("{0}\t\t{1}".format(key, profile[key]))


# Returns a customer error message.
def error(message):
    if message is None:
        print("Program ended.")
    else:
        print("Error: " + message + "\nEnding program...")


def main(textfile1, arg2, normalize=False):

    if not isinstance(normalize, bool):
        print("Non boolean value passed to argument - normalize.")
        print("Data will not be normalized.\n")
        normalize = False

    profile1_text = read_file(textfile1)

    if profile1_text is None:
        error(profile1_text)
        return

    profile1 = create_profile(profile1_text, normalize)

    if profile1 is None:
        error(profile1)
        return

    if arg2.lower() != "listing":
        profile2_text = read_file(arg2)

        if profile2_text is None:
            error(profile2_text)
            return

        profile2 = create_profile(profile2_text, normalize)

        if profile2 is None:
            error(profile2)
            return

        distance = profile_distance(profile1, profile2)
        print("The distance between the 2 texts is: {0:.4f}".format(distance))

    else:
        display_listing(profile1, textfile1)


main("sample1.txt", "listing", False)
