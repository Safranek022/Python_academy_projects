"""
projekt_2b.py: druhý projekt do Engeto Online Python Akademie
author: Jaroslav Šafránek
email: jaroslav.safranek@rako.cz
discord: Joker055#6334
"""

line = "=" * 44
gameBoard = [" "] * 9
activePlayer = " X "
gameNotFinished = True
invalidNumber = True 

def startText() -> None:
    print("Welcome to Tic Tac Toe")
    print(line)
    print("""GAME RULES
Each player can place one mark (or stone)
per turn on the 3x3 grid. The WINNER is
who succeeds in placing three of their
marks in a:
* horizontal,
* vertical or
* diagonal row""")
    print(line)
    print("Let's start the game")
    print(line)

def printBoard() -> None:
    """
    Zobrazí aktuální stav hrací plochy 3x3. Pole jsou odděleny | a číslovány od 1 do 9
    """
    
    print("+---+---+---+")
    print("|" + "|".join(gameBoard[:3]) + "|")
    print("+---+---+---+")
    print("|" + "|".join(gameBoard[3:6]) + "|")
    print("+---+---+---+")
    print("|" + "|".join(gameBoard[6:]) + "|")
    print("+---+---+---+")
    
def checkPlayerMove(player: str) -> int:
    """
    Vypíše oznámení pro hráče a zkontroluje, že je zadaný vstup validní.
    """

    print(line)
    playerMove = input(f"Player {player} | Please enter your move number:")
    if not playerMove.isdigit() or int(playerMove) not in range(1, 10):
        print("Please enter digit between 1 - 9.")
    else:
        return int(playerMove) - 1
    print(line)

def moveIfFieldIsEmpty(move: int) -> bool:
    """
    Vyhodnotí, zda je zadané pole volné. Pokud ano, tak zaznamená hráčův tah. 
    """

    if move in range(0, 9):
        if gameBoard[move] == " ":
            gameBoard[move] = activePlayer
            return False
        else:
            print("This field is already taken. Please choose another.")
            return True
    else:
        return True

def switchPlayer(player: str) -> str:
    """
    Přepne na protihráče
    """
    players = [" X ", " O "]
    if player == players[0]:
        return players[1]
    else:
        return players[0]

def checkWinningCondition(player: str) -> bool:
    """
    Zkontroluje, zda je na poli výherní kombinace. Pokud ano, tak ukončí hru. Pokud ne a jsou volná pole, tak hra pokračuje.
    Pokud již není žádné volné pole, tak ukončí hru a oznámí remízu.
    """
    
    # Výpis všech výherních kombinací. Při zvětšení herní plochy nutné přepracovat logiku.
    winningConditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # horizontální
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # vertikální
        [0, 4, 8], [2, 4, 6]              # diagonální
    ]

    for condition in winningConditions:
        if gameBoard[condition[0]] != " " and gameBoard[condition[0]] == gameBoard[condition[1]] == gameBoard[condition[2]]:
            print(f"Congratulations, the player {player.strip()} WON!")
            return False
        
    if " " not in gameBoard:
        print(f"No empty field on game board, it is a TIE!")
        return False
    else:
        return True

startText()
printBoard()
while gameNotFinished:
    while invalidNumber:
        playerMove = checkPlayerMove(activePlayer)
        invalidNumber = moveIfFieldIsEmpty(playerMove)
    printBoard()
    gameNotFinished = checkWinningCondition(activePlayer)
    activePlayer = switchPlayer(activePlayer)
    invalidNumber = True