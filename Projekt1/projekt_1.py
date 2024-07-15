"""
projekt_1.py: první projekt do Engeto Online Python Akademie
author: Jaroslav Šafránek
email: jaroslav.safranek@rako.cz
discord: Joker055#6334
"""

import re

TEXTS = ['''
Situated about 10 miles west of Kemmerer,
Fossil Butte is a ruggedly impressive
topographic feature that rises sharply
some 1000 feet above Twin Creek Valley
to an elevation of more than 7500 feet
above sea level. The butte is located just
north of US 30N and the Union Pacific Railroad,
which traverse the valley. ''',
'''At the base of Fossil Butte are the bright
red, purple, yellow and gray beds of the Wasatch
Formation. Eroded portions of these horizontal
beds slope gradually upward from the valley floor
and steepen abruptly. Overlying them and extending
to the top of the butte are the much steeper
buff-to-white beds of the Green River Formation,
which are about 300 feet thick.''',
'''The monument contains 8198 acres and protects
a portion of the largest deposit of freshwater fish
fossils in the world. The richest fossil fish deposits
are found in multiple limestone layers, which lie some
100 feet below the top of the butte. The fossils
represent several varieties of perch, as well as
other freshwater genera and herring similar to those
in modern oceans. Other fish such as paddlefish,
garpike and stingray are also present.'''
]

userDatabase = {
    "bob": "123",
    "ann": "pass123",
    "mike": "password123",
    "liz": "pass123"
}

line = "-" * 40

loginName = input("username: ")
loginPassword = input("password: ")

if (loginName in userDatabase and userDatabase[loginName] == loginPassword):
    print(line)
    print(f"""Welcome to the app, {loginName}
We have 3 texts to be analyzed.""")
    print(line)    
else:
    print("unregistered user, terminating the program..")
    exit()

textNumber = input("Enter a number btw. 1 and 3 to select: ")
if not textNumber.isdigit() or int(textNumber) not in range(1, 4):
    print("input must be number between 1 and 3, terminating the program..")
    exit()

print(line)

selectedText = TEXTS[int(textNumber) - 1]
selectedText = re.sub(r'[^\w\s]', '', selectedText)
numberOfWords = len(selectedText.split())

titlecaseWords = 0
uppercaseWords = 0
lowercaseWords = 0
numericStrings = 0
sumOfnumericStrings = 0
wordsLengths = []
maxLength = 0

for word in selectedText.split():
    if re.match(r'^[A-Z].*', word):
        titlecaseWords += 1
    if word.isupper() and word.isalpha():
        uppercaseWords += 1
    if word.islower() and word.isalpha():
        lowercaseWords += 1
    if word.isdigit():
        numericStrings += 1
        sumOfnumericStrings += int(word)
    wordsLengths.append(len(word))
    if len(word) > maxLength:
        maxLength = len(word)

print(f"There are {numberOfWords} words in the selected text.")

if titlecaseWords == 1:
    print(f"There is {titlecaseWords} titlecase word.")
else:
    print(f"There are {titlecaseWords} titlecase words.")

if uppercaseWords == 1:
    print(f"There is {uppercaseWords} uppercase word.")
else:
    print(f"There are {uppercaseWords} uppercase words.")

if lowercaseWords == 1:
    print(f"There is {lowercaseWords} lowercase word.")
else:
    print(f"There are {lowercaseWords} lowercase words.")

if numericStrings == 1:
    print(f"There is {numericStrings} numeric string.")
else:
    print(f"There are {numericStrings} numeric strings.")

print(f"The sum of all the numbers {sumOfnumericStrings}.")
print(line)
print(f"LEN| {"OCCURENCES":^17}  |NR.")
print(line)

for i in range(1, maxLength + 1):
    print(f"{i:>3}| {"*" * wordsLengths.count(i):<17}  |{wordsLengths.count(i):<3}")