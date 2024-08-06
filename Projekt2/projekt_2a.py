"""
projekt_2a.py: druhý projekt do Engeto Online Python Akademie
author: Jaroslav Šafránek
email: jaroslav.safranek@rako.cz
discord: Joker055#6334
"""

import random, time

retryGame = True
playerStatistics = []

def startText() -> None:   
    line = "-" * 47
    print("Hi there!")
    print(line)
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print(line)
    print("Enter a number:")
    print(line)

def generateNumber() -> str:
    """
    Vygeneruje hádané číslo. Hádané číslo nezačíná 0, má délku 4 a každá číslice je unikátní.
    """
    goalNumber: str = ""
    while len(goalNumber) < 4:
        randomNumber = str(random.randint(0, 9))
        if randomNumber not in goalNumber:
            goalNumber = goalNumber + randomNumber
        if goalNumber[0] == "0":
            goalNumber = ""
    
    return goalNumber

def checkPlayerGuess() -> str:
    """
    Vyžádá si nový tip od uživatele a zkontroluje, zda zadaný tip splňuje podmínky: 
        Jde číslo o délce 4
        Nebylo již v rámci hry použito
        Nezačíná na 0
        Neobsahuje duplicity
    Vrací: validní tip uživatele
    """
    invalidGuess = True

    while invalidGuess:
        guess = input(">>>> ")
        uniqueDigits = set(guess)
        if not guess.isdigit():
            print("Please enter number.")
        elif len(guess) != 4:
            print("Please enter 4 digit number.")
        elif guess[0] == "0":
            print("Number cannot start with 0.")
        elif guess in previousGuesses:
            print(f"Enter unique digit. Previous guesses: {previousGuesses}.")
        elif len(guess) != len(uniqueDigits):
            print("All digits of number must be unique.")
        else:
            previousGuesses.append(guess)
            invalidGuess = False
    
    return guess

def compareGuess(guess: str, goalNumber: str) -> None:
    """
    Porovná tip uživatele s cílovým číslem. Vypíše počet bulls a cows.
    """
    numberOfCows = 0
    numberOfBulls = 0
    guessChecked = [False] * 4
    goalChecked = [False] * 4

    for i in range(4):
        if guess[i] == goalNumber[i]:
            numberOfBulls += 1
            guessChecked[i] = True
            goalChecked[i] = True

    for i in range(4):
        if not guessChecked[i]:
            for j in range(4):
                if not goalChecked[j] and guess[i] == goalNumber[j]:
                    numberOfCows += 1
                    goalChecked[j] = True
                    break

    if numberOfBulls == 1 and numberOfCows ==1:
        print(f"{numberOfBulls} bull, {numberOfCows} cow")
    elif numberOfBulls == 1:
        print(f"{numberOfBulls} bull, {numberOfCows} cows")
    elif numberOfCows == 1:
        print(f"{numberOfBulls} bulls, {numberOfCows} cow")
    else:
        print(f"{numberOfBulls} bulls, {numberOfCows} cows")

while retryGame:
    incorrectGuess = True
    previousGuesses = []

    startText()
    goalNumber = generateNumber()
    # print(goalNumber)

    startTime = time.time()

    while incorrectGuess:
        guess = checkPlayerGuess()
        if guess == goalNumber:
            endTime = time.time()

            print(f"Correct, you've guessed the right number in {len(previousGuesses)} guesses!")
            print(f"Time of game: {int(endTime - startTime)}s")
            playerStatistics.append(len(previousGuesses))
            print(f"Your current statistics (number of guesses) are: {playerStatistics}")
            playAgain = input("Do you want to play again? Type y to play again. ")
            incorrectGuess = False
        else:
            compareGuess(guess, goalNumber)

    if playAgain != "y":
        retryGame = False
        print(f"Thank you for playing! Your final statistics are: {playerStatistics}")
    