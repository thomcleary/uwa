""" beat the unfair game """

import os

from telnetlib import Telnet


def main():

    # Get the random numbers needed
    if os.path.isfile("./nums.txt"):
        os.system("rm nums.txt")

    os.system("./macCheater")

    with Telnet("cits4projtg.cybernemosyne.xyz", 1001) as tn:
        with open("nums.txt", "r") as guesses:
            nums = []

            for num in guesses:
                nums.append(int(num))

            print("NUMBER OF NUMS {}".format(len(nums)))

        game_round = 0

        while game_round < len(nums):
            text = tn.read_until(b"Number: ")
            print(text.decode("utf-8"))

            num = bytes(str(nums[game_round]) + "\n", "utf-8")
            tn.write(num)
            print(num)

            game_round += 1



    with open("nums.txt", "r") as guesses:
        nums = []

        for num in guesses:
            nums.append(int(num))

    



if __name__ == "__main__":
    main()
