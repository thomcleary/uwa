import codecs

"find passwords in rockyou with cat as substring"

question = """Rocking cats Man cats absolutely wild Last Saturday house party feral feline screaming password hash tune We Will Rock You Queen telling pretty dumb idea leak hashed password everyone insisted fine 32 characters long brute forced teach feline fleabag lesson crack"""
question = question.lower()

possible_words = question.split(" ")

with codecs.open("rockyou.txt", "r", encoding="utf-8", errors="ignore") as rockyou:
    with open("catwords.txt", "w", encoding="utf-8") as catwords:

        iterator_has_next = True
        count = 0
        
        while iterator_has_next:
            try:
                line = next(rockyou)
            except UnicodeDecodeError:
                continue
            except StopIteration:
                iterator_has_next = False
                continue
            
            if len(line.strip()) == 32:
                print("{} - {}".format(count, line))
                catwords.write(line)
                count += 1

