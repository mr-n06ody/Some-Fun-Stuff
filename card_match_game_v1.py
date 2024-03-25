import sys
import os
import random
import time
import sqlite3 as sql

DATABASE_NAME = "car_match_game.db"
CARD_BACKS_TABLE = "card_backs_table"
CARD_BACKS_TABLE_FIELDS_SETUP = "card_back CHAR(1) PRIMARY KEY"
CARD_BACKS_TABLE_FIELDS = "card_back"
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

END_MSG = [
        r"                  ┏┳┓┓     ┓    ┏      ┏┓┓    •    ╻",
        r"                   ┃ ┣┓┏┓┏┓┃┏┏  ╋┏┓┏┓  ┃┃┃┏┓┓┏┓┏┓┏┓┃",
        r"                   ┻ ┛┗┗┻┛┗┛┗┛  ┛┗┛┛   ┣┛┗┗┻┗┫┗┛┗┗┫•",
        r"                                             ┛    ┛ "
    ]




def execute_sql(sqlScrypt: str, returnVals: bool=False, commitChanges: bool=False):
    with sql.connect(DATABASE_NAME) as conn:
        try:
            c = conn.cursor()
            c.execute(sqlScrypt)
            if commitChanges:
                conn.commit()
            if returnVals:
                result = c.fetchall()
        except Exception as error:
            print(error)
            conn.rollback()
            quit()
    if returnVals:
        return result

def database_create_table(table: str,   fields: str):
    execute_sql(sqlScrypt=f"CREATE TABLE IF NOT EXISTS {table} ({fields});", commitChanges=True)

def check_table_exists(table):
    result = len(execute_sql(sqlScrypt=f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';", returnVals=True))
    if result == 0:
        return False
    else:
        return True

def insert_into_table(table, columns, values):
    execute_sql(sqlScrypt=f"INSERT OR IGNORE INTO {table} ({columns}) VALUES ({values});", commitChanges=True)
    
def database_setup():
    if check_table_exists(CARD_BACKS_TABLE) == False:
        database_create_table(CARD_BACKS_TABLE, CARD_BACKS_TABLE_FIELDS_SETUP)
        insert_into_table(CARD_BACKS_TABLE, CARD_BACKS_TABLE_FIELDS, "'r'")

def update_table(table: str, fields: str, condition: str="", conditionActive: bool=False):
    if conditionActive:
        sqlString = f"UPDATE {table} SET {fields} WHERE {condition};"
    else:
        sqlString = f"UPDATE {table} SET {fields};"

    return execute_sql(sqlScrypt=sqlString, commitChanges=True)

def database_select(table: str, fields: str, condition: str="", conditionActive: bool=False):
    if conditionActive:
        sqlString = f"SELECT {fields} FROM {table} WHERE {condition};"
    else:
        sqlString = f"SELECT {fields} FROM {table};"

    return execute_sql(sqlScrypt=sqlString, returnVals=True)

def get_cards_to_flip(grid):
    gridLen = len(grid) * 5
    while True:
        sys.stderr.write("Please enter the card numbers you want to turn\n")
        try:
            error = False
            card1 = input("(1)... ")
            if card1 == "WIN!":
                return "EASTER1"
            card1 = int(card1)
            if card1 <= gridLen and card1 > 0:
                card1Cord = card1 - 1
                if card1Cord > 4:
                    if grid[1][card1Cord - 5] == 0:
                        error = True
                        sys.stderr.write("Card does not exist\n")
                else:
                    if grid[0][card1Cord] == 0:
                        error = True
                        sys.stderr.write("Card does not exist\n")
            else:
                sys.stderr.write("Card does not exist\n")
                error = True
            
            if error == False:
                card2 = int(input("(2)... "))
                if card2 <= gridLen or card2 < 1:
                    card2Cord = card2 - 1
                    if card2Cord > 4:
                        if grid[1][card2Cord - 5] == 0:
                            error = True
                            sys.stderr.write("Card does not exist\n")
                    else:
                        if grid[0][card2Cord] == 0:
                            error = True
                            sys.stderr.write("Card does not exist\n")
                else:
                    error = True
                    sys.stderr.write("Card does not exist\n")
            
            if card1Cord == card2Cord:
                error = True
                sys.stderr.write("Enter two different cards you cheat\n")

            if error == False:
                return card1Cord, card2Cord

        except:
            sys.stderr.write("Invalid input, please input an integer\n")

def get_card_back(all: bool=False):
    cardBackLst = [
        [
            r".-----------.",
            r"|  *     *  |",
            r"|     *     |",
            r"|  *     *  |", 
            r"|     *     |", 
            r"|  *     *  |",
            r"|     *     |",
            r"|  *     *  |",
            r"|     *     |", 
            r"`-----------'"
        ],[
            r".-----------.",
            r"|     *     |",
            r"|   *   *   |",
            r"| *      *  |", 
            r"|  *      * |", 
            r"|   *      *|",
            r"|    *   *  |",
            r"|      *    |",
            r"|           |", 
            r"`-----------'"
        ],[
            r".-----------.",
            r"|           |",
            r"|     *     |",
            r"|    ***    |", 
            r"|   *****   |", 
            r"|  *******  |",
            r"| ********* |",
            r"|    ***    |",
            r"|    ***    |", 
            r"`-----------'"
        ],[
            r".-----------.",
            r"|           |",
            r"|     █     |",
            r"|   █████   |",
            r"| █████████ |", 
            r"|███████████|", 
            r"| ███ | ███ |",
            r"| ███‾|‾███ |",
            r"| ███___███ |", 
            r"`-----------'"
        ]
    ]
    cardSetting = database_select(table=CARD_BACKS_TABLE, fields="*")[0][0]
    
    if all:
        return cardBackLst
    elif 48 <= ord(cardSetting) <= 57:
        displayIndex = int(cardSetting) - 1
    else:
        displayIndex = random.randint(0, 3)

    try:
        return cardBackLst[displayIndex]
    except:
        return cardBackLst[0]

def get_card_front(cardNum: int=1, hasSuit: bool=False):
    """ 
        r".-----------.",
        r"|           |", 
        r"|           |",
        r"|           |",
        r"|           |", 
        r"|           |", 
        r"|           |",
        r"|           |",
        r"|           |",
        r"`-----------'"

    """
    returnLst = []
    suitLst = ["<>", "<3", "{>", "-%", "Filler"]

    if hasSuit:
        suit = "<>"
        loopNum = 4
    else:
        suit = "  "
        loopNum = 1

    for i in range(loopNum):
        cardFrontLst = [[
            r".-----------.",
            fr"|{suit}         |",
            r"|     *     |",
            r"|    * *    |", 
            r"|   *   *   |", 
            r"|  *     *  |",
            r"| * * * * * |",
            r"| *       * |",
            r"| *       * |", 
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}         |",
            r"|           |",
            r"|   *  *    |",
            r"| *      *  |", 
            r"|        *  |", 
            r"|      *    |",
            r"|   *       |",
            r"| * * * * * |", 
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}         |", 
            r"|   * * *   |",
            r"|         * |",
            r"|         * |", 
            r"|   * * *   |", 
            r"|         * |",
            r"|         * |",
            r"|   * * *   |",
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}   *     |", 
            r"|    **     |",
            r"|   * *     |",
            r"|  *  *     |", 
            r"| *   *     |", 
            r"|* * ** * * |",
            r"|     *     |",
            r"|     *     |",
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}         |", 
            r"|           |",
            r"|  * * * *  |",
            r"|  *        |", 
            r"|   * * *   |", 
            r"|        *  |",
            r"|  *     *  |",
            r"|   * * *   |",
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}         |", 
            r"|    * * *  |",
            r"|  *        |",
            r"| *         |", 
            r"| * * * *   |", 
            r"| *       * |",
            r"| *       * |",
            r"|  * * * *  |",
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}         |", 
            r"|           |",
            r"|   * * * * |",
            r"|        *  |", 
            r"|       *   |", 
            r"|      *    |",
            r"|     *     |",
            r"|    *      |",
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}         |", 
            r"|    * *    |", 
            r"|  *     *  |",
            r"|  *     *  |",
            r"|    * *    |", 
            r"|  *     *  |",
            r"|  *     *  |",
            r"|    * *    |",
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}          |", 
            r"|     * *   |",
            r"|   *     * |",
            r"|   *     * |", 
            r"|     * * * |", 
            r"|         * |",
            r"|         * |",
            r"|    * * *  |",
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}         |",
            r"|           |",
            r"|  *  * * * |", 
            r"| ** *     *|",
            r"|* * *     *|",
            r"|  * *     *|", 
            r"|  * *     *|", 
            r"|  *  * * * |",
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}  █████  |", 
            r"|      █    |",
            r"|  █   █    |",
            r"|   ███     |",
            r"| o o O o o |",
            r"|  \ \|/ /  |", 
            r"| (++\@/++) |", 
            r"| '-------' |",
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit} .---.   |", 
            r"|   |.  |   |",
            r"|   `---\   |",
            r"|  o  O  o  |",
            r"| o \ | / o |", 
            r"|  \ \|/ /  |", 
            r"| (++\@/++) |",
            r"| '-------' |",
            r"`-----------'"
        ],[
            r".-----------.",
            fr"|{suit}██   ██  |", 
            r"|  ██  ██   |",
            r"|  █████    |",
            r"|  ██  ██   |",
            r"|  ██ _ ██  |",
            r"|/\  \*/  /\|", 
            r"|\*\_|O|_/*/|", 
            r"| \_______/ |",
            r"`-----------'"
        ]]
        for card in cardFrontLst:
            returnLst.append(card)
        suit = suitLst[i+1]

    if hasSuit == False:
        return returnLst[cardNum - 1]
    return returnLst

def numbers(grid, rowCount: int):
    salt = rowCount*5
    for i in range(0, len(grid)):
        count = i + 1 + salt
        if grid[i] == 1:
            sys.stderr.write(f"      {str(count)}      ")
        else:
            sys.stderr.write(f"             ")
    sys.stderr.write("\n")

def generate_card_positions():
    numLst = [i for i in range(1, 14)]
    returnLst = []
    setLst = []
    for _ in range(5):
        num = random.choice(numLst)
        numLst.remove(num)
        setLst.append(num)
        returnLst.append(num)
    for _ in range(5):
        num = random.choice(setLst)
        setLst.remove(num)
        returnLst.append(num)
    
    return returnLst

def seperator():
    for i in range(5):
        sys.stderr.write("--------------")
    sys.stderr.write("\n")

def display_hidden_line(grid, displayStr):
    for card in grid:
        if card == 1:
            sys.stderr.write(f"{displayStr}")
        else:
            sys.stderr.write("             ")
    sys.stderr.write("\n")

def display_hidden_grid(grid: list, displayLst: list):
    for i, row in enumerate(grid):
        numbers(row, i)
        for i in range(10):
            display_hidden_line(row, displayLst[i])

def display_non_hidden_line(grid, displayStr, cardPos: tuple, cardDisplay1: str, cardDisplay2: str, start: int):
    for i, card in enumerate(grid):
        pos = i + start
        if card == 1:
            if pos == cardPos[0]:
                sys.stderr.write(f"{cardDisplay1}")
            elif pos == cardPos[1]:
                sys.stderr.write(f"{cardDisplay2}")
            else:
                sys.stderr.write(f"{displayStr}")
        else:
            sys.stderr.write("             ")
    sys.stderr.write("\n")

def display_card_on_grid(grid: list, displayLst: list, cardDisplay: tuple, cardPos: tuple):
    start = 0
    for i, row in enumerate(grid):
        numbers(row, i)
        for i in range(10):
            display_non_hidden_line(row, displayLst[i], cardPos, cardDisplay[0][i], cardDisplay[1][i], start)
        start += 5

def flip_cards_top(displayGrid, numGrid, cardBack):
    coords = get_cards_to_flip(displayGrid)
    if isinstance(coords, tuple) == False:
        if coords == "EASTER1":
            return "EASTER1"
        else:
            sys.stderr.write("Encountered Error\n")
            coords = get_cards_to_flip(displayGrid)
    num1 = numGrid[coords[0]]
    num2 = numGrid[coords[1]]
    os.system('cls' if os.name == 'nt' else 'clear')
    seperator()
    display_card_on_grid(displayGrid, cardBack, (get_card_front(num1), get_card_front(num2)), coords)
    if num1 == num2:
        index1 = 0
        cords1 = coords[0]
        if cords1 > 4:
            cords1 -= 5
            index1 += 1
        
        index2 = 0
        cords2 = coords[1]
        if cords2 > 4:
            cords2 -= 5
            index2 += 1

        displayGrid[index1][cords1] = 0
        displayGrid[index2][cords2] = 0
    return displayGrid

def display_all_backs(backsOnly: bool=False):
    singleGrid = [1, 0, 0, 0, 0]
    doubleGrid = [1, 1, 0, 0, 0]
    cardBackLst = get_card_back(all=True)
    for cardBack in cardBackLst:
        for line in cardBack:
            display_hidden_line(singleGrid, line)
    
    if backsOnly == False:
        for i in range(1, 13, 2):
            card1 = get_card_front(i)
            card2 = get_card_front(i+1)
            for i in range(10):
                card1Back = card1[i]
                card2Back = card2[i]
                display_non_hidden_line(doubleGrid, "", (0, 1), card1Back, card2Back, 0)

        card = get_card_front(13)
        for i in range(10):
            cardBack = card[i]
            display_non_hidden_line(singleGrid, "", (0, 0), cardBack, "", 0)

def display_end_msg():
    sys.stderr.write("\n\n")
    for line in END_MSG:
        sys.stderr.write(line)
        sys.stderr.write("\n")
        time.sleep(0.1)

def sub_menu():
    displayLst = [[
        r"      ███    ██ ███████ ██     ██      ██████   █████  ███    ███ ███████        ███    ██ ",
        r"      ████   ██ ██      ██     ██     ██       ██   ██ ████  ████ ██      ██     ████   ██ ",
        r"      ██ ██  ██ █████   ██  █  ██     ██   ███ ███████ ██ ████ ██ █████          ██ ██  ██ ",
        r"      ██  ██ ██ ██      ██ ███ ██     ██    ██ ██   ██ ██  ██  ██ ██      ██     ██  ██ ██ ",
        r"      ██   ████ ███████  ███ ███       ██████  ██   ██ ██      ██ ███████        ██   ████ ",
    ],[
        r"███    ███  █████  ██ ███    ██     ███    ███ ███████ ███    ██ ██    ██        ███    ███ ",
        r"████  ████ ██   ██ ██ ████   ██     ████  ████ ██      ████   ██ ██    ██ ██     ████  ████ ",
        r"██ ████ ██ ███████ ██ ██ ██  ██     ██ ████ ██ █████   ██ ██  ██ ██    ██        ██ ████ ██ ",
        r"██  ██  ██ ██   ██ ██ ██  ██ ██     ██  ██  ██ ██      ██  ██ ██ ██    ██ ██     ██  ██  ██ ",
        r"██      ██ ██   ██ ██ ██   ████     ██      ██ ███████ ██   ████  ██████         ██      ██ "

    ],[
        r"     ██████  ██    ██ ██ ████████      ██████   █████  ███    ███ ███████         ██████  ",
        r"    ██    ██ ██    ██ ██    ██        ██       ██   ██ ████  ████ ██      ██     ██    ██ ",
        r"    ██    ██ ██    ██ ██    ██        ██   ███ ███████ ██ ████ ██ █████          ██    ██ ",
        r"    ██ ▄▄ ██ ██    ██ ██    ██        ██    ██ ██   ██ ██  ██  ██ ██      ██     ██ ▄▄ ██ ",
        r"     ██████   ██████  ██    ██         ██████  ██   ██ ██      ██ ███████         ██████  ",
        r"         ▀▀                                                                           ▀▀   "
            ]]
    
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stderr.write("\n\n")

    for item in displayLst:
        for line in item:
            sys.stderr.write(line)
            sys.stderr.write("\n")
            time.sleep(0.05)
        time.sleep(0.3)
        sys.stderr.write("\n")
        
    answer = str(input("             ... "))
    while True:
        
        if answer == "N" or answer == "n":
            game_loop()
        elif answer == "M" or answer == "m":
            main_menu()
        elif answer == "Q" or answer == "q":
            os.system('cls' if os.name == 'nt' else 'clear')
            display_end_msg()
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            quit()
        else:
            sys.stderr.write(CURSOR_UP_ONE)
            sys.stderr.write(ERASE_LINE)
            sys.stderr.write("Invalid input")
            time.sleep(1)
            sys.stderr.write(ERASE_LINE)
            answer = str(input("... "))

def credits():
    lineDisplayLst = [[
        r" ██████╗",
        r"██╔════╝",
        r"██║     ",
        r"██║     ",
        r"╚██████╗",
        r" ╚═════╝"
    ], [
        r" ██████╗ █████╗ ",
        r"██╔════╝██╔══██╗",
        r"██║     ███████║",
        r"██║     ██╔══██║",
        r"╚██████╗██║  ██║",
        r" ╚═════╝╚═╝  ╚═╝"
    ], [
        r" ██████╗ █████╗ ██████╗ ",
        r"██╔════╝██╔══██╗██╔══██╗",
        r"██║     ███████║██████╔╝",
        r"██║     ██╔══██║██╔══██╗",
        r"╚██████╗██║  ██║██║  ██║",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝"
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ",
        r"██║     ███████║██████╔╝██║  ██║    ",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     "
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ███╗   ███╗",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║",
        r"██║     ███████║██████╔╝██║  ██║    ██╔████╔██║",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝"
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗",
        r"██║     ███████║██████╔╝██║  ██║    ██╔████╔██║███████║",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝"
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ████████╗",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗╚══██╔══╝",
        r"██║     ███████║██████╔╝██║  ██║    ██╔████╔██║███████║   ██║   ",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║   ██║   ",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║   ██║   ",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   "
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ████████╗ ██████╗",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗╚══██╔══╝██╔════╝",
        r"██║     ███████║██████╔╝██║  ██║    ██╔████╔██║███████║   ██║   ██║     ",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║   ██║   ██║     ",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╗",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝"
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ████████╗ ██████╗██╗  ██╗",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗╚══██╔══╝██╔════╝██║  ██║",
        r"██║     ███████║██████╔╝██║  ██║    ██╔████╔██║███████║   ██║   ██║     ███████║",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║   ██║   ██║     ██╔══██║",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╗██║  ██║",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝"
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ████████╗ ██████╗██╗  ██╗     ██████╗ ",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗╚══██╔══╝██╔════╝██║  ██║    ██╔════╝ ",
        r"██║     ███████║██████╔╝██║  ██║    ██╔████╔██║███████║   ██║   ██║     ███████║    ██║  ███╗",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║   ██║   ██║     ██╔══██║    ██║   ██║",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╗██║  ██║    ╚██████╔╝",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝     ╚═════╝ "
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ████████╗ ██████╗██╗  ██╗     ██████╗  █████╗ ",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗╚══██╔══╝██╔════╝██║  ██║    ██╔════╝ ██╔══██╗",
        r"██║     ███████║██████╔╝██║  ██║    ██╔████╔██║███████║   ██║   ██║     ███████║    ██║  ███╗███████║",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║   ██║   ██║     ██╔══██║    ██║   ██║██╔══██║",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╗██║  ██║    ╚██████╔╝██║  ██║",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝"
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ████████╗ ██████╗██╗  ██╗     ██████╗  █████╗ ███╗   ███╗",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗╚══██╔══╝██╔════╝██║  ██║    ██╔════╝ ██╔══██╗████╗ ████║",
        r"██║     ███████║██████╔╝██║  ██║    ██╔████╔██║███████║   ██║   ██║     ███████║    ██║  ███╗███████║██╔████╔██║",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║   ██║   ██║     ██╔══██║    ██║   ██║██╔══██║██║╚██╔╝██║",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╗██║  ██║    ╚██████╔╝██║  ██║██║ ╚═╝ ██║",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝"
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ████████╗ ██████╗██╗  ██╗     ██████╗  █████╗ ███╗   ███╗███████╗",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗╚══██╔══╝██╔════╝██║  ██║    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝",
        r"██║     ███████║██████╔╝██║  ██║    ██╔████╔██║███████║   ██║   ██║     ███████║    ██║  ███╗███████║██╔████╔██║█████╗  ",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║   ██║   ██║     ██╔══██║    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╗██║  ██║    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝"
    ], [
        r" ██████╗ █████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ████████╗ ██████╗██╗  ██╗     ██████╗  █████╗ ███╗   ███╗███████╗██╗",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗╚══██╔══╝██╔════╝██║  ██║    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝██║",
        r"██║     ███████║██████╔╝██║  ██║    ██╔████╔██║███████║   ██║   ██║     ███████║    ██║  ███╗███████║██╔████╔██║█████╗  ██║",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║   ██║   ██║     ██╔══██║    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ╚═╝",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╗██║  ██║    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗██╗",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝"
    ]]

    personsLst = [
        r"          _  __     __           __    ",
        r"  ___    / |/ /__  / /  ___  ___/ /_ __",
        r" |___|  /    / _ \/ _ \/ _ \/ _  / // /",
        r"       /_/|_/\___/_.__/\___/\_,_/\_, / ",
        r"                              /___/    "
    ]

    creditsDisplayLst = [[
        r"   ___               _    _        ",
        r"  / __|_ _ __ _ _ __| |_ (_)__ ___ ",
        r" | (_ | '_/ _` | '_ \ ' \| / _(_-< ",
        r"  \___|_| \__,_| .__/_||_|_\__/__/ ",
        r"               |_|                 "
    ], [
        r"  ___                                    _           ",
        r" | _ \_ _ ___  __ _ _ _ __ _ _ __  _ __ (_)_ _  __ _ ",
        r" |  _/ '_/ _ \/ _` | '_/ _` | '  \| '  \| | ' \/ _` |",
        r" |_| |_| \___/\__, |_| \__,_|_|_|_|_|_|_|_|_||_\__, |",
        r"              |___/                            |___/ "
    ],[
        r"  ___ _                ",
        r" / __| |_ ___ _ _ _  _ ",
        r" \__ \  _/ _ \ '_| || |",
        r" |___/\__\___/_|  \_, |",
        r"                  |__/ "
    ],[
        r"  ___                  _   _    _           ",
        r" | __|_ _____ _ _ _  _| |_| |_ (_)_ _  __ _ ",
        r" | _|\ V / -_) '_| || |  _| ' \| | ' \/ _` |",
        r" |___|\_/\___|_|  \_, |\__|_||_|_|_||_\__, |",
        r"                  |__/                |___/ "
    ]]

    

    for i, segment in enumerate(lineDisplayLst):
        os.system('cls' if os.name == 'nt' else 'clear')
        for line in segment:
            sys.stderr.write(line)
            sys.stderr.write("\n")
        if i == 13:
            for i in range(4):
                time.sleep(0.05)
                os.system('cls' if os.name == 'nt' else 'clear')
                time.sleep(0.05)
                for line in segment:
                    sys.stderr.write(line)
                    sys.stderr.write("\n")
                  
        time.sleep(0.22)
    
    for credit in creditsDisplayLst:
        sys.stderr.write("\n")
        for i, line in enumerate(credit):
            sys.stderr.write(line)
            sys.stderr.write(personsLst[i])
            sys.stderr.write("\n")
            time.sleep(0.2)
        sys.stderr.write("\n")

    time.sleep(0.75)

    display_end_msg()

    time.sleep(1.5)
    start_screen()

def game_loop():
    gameOver = False
    currentGrid = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
    blankGrid = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    cardBack = get_card_back()
    cardPos = generate_card_positions()
    t1 = time.time()

    while gameOver == False:
        os.system('cls' if os.name == 'nt' else 'clear')
        seperator()
        display_hidden_grid(currentGrid, cardBack)
        seperator()
        currentGrid = flip_cards_top(currentGrid, cardPos, cardBack)
        if isinstance(currentGrid, str) == True:
            if currentGrid == "EASTER1":
                currentGrid = blankGrid
            else:
                sys.stderr.write("Encountered Error\n")
                currentGrid = flip_cards_top(currentGrid, cardPos, cardBack)
        seperator()
        time.sleep(3)
        if currentGrid == blankGrid:
            os.system('cls' if os.name == 'nt' else 'clear')
            gameOver = True
            timeTaken = time.time() - t1
            extension = "s"
            for i in range(2):
                if timeTaken >= 60:
                    timeTaken /= 60
                    if i == 0:
                        extension = " mins"
                    if i == 1:
                        extension = " hours?!"

            timeTaken = str(timeTaken)
            decimalIndex = timeTaken.find(".")
            timeTaken = timeTaken[:decimalIndex+3] + extension

            sys.stderr.write(f"\n\n\n\n\n\nGame Completed!\nTime Taken: {timeTaken}\n\n\n")
            input("Press enter to continue... ")
            sub_menu()

def options():
    titleLst = [[
        r" ██████╗ █████╗ ██████╗ ██████╗ ",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗",
        r"██║     ███████║██████╔╝██║  ██║",
        r"██║     ██╔══██║██╔══██╗██║  ██║",
        r"╚██████╗██║  ██║██║  ██║██████╔╝",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ "
    ],[
        r" ██████╗ █████╗ ██████╗ ██████╗     ██████╗  █████╗  ██████╗██╗  ██╗",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝",
        r"██║     ███████║██████╔╝██║  ██║    ██████╔╝███████║██║     █████╔╝ ",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██╔══██╗██╔══██║██║     ██╔═██╗ ",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██████╔╝██║  ██║╚██████╗██║  ██╗",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝"
    ],[
        r" ██████╗ █████╗ ██████╗ ██████╗     ██████╗  █████╗  ██████╗██╗  ██╗     ██████╗ ██████╗ ████████╗██╗ ██████╗ ███╗   ██╗███████╗",
        r"██╔════╝██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝    ██╔═══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝",
        r"██║     ███████║██████╔╝██║  ██║    ██████╔╝███████║██║     █████╔╝     ██║   ██║██████╔╝   ██║   ██║██║   ██║██╔██╗ ██║███████╗",
        r"██║     ██╔══██║██╔══██╗██║  ██║    ██╔══██╗██╔══██║██║     ██╔═██╗     ██║   ██║██╔═══╝    ██║   ██║██║   ██║██║╚██╗██║╚════██║",
        r"╚██████╗██║  ██║██║  ██║██████╔╝    ██████╔╝██║  ██║╚██████╗██║  ██╗    ╚██████╔╝██║        ██║   ██║╚██████╔╝██║ ╚████║███████║",
        r" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ╚═════╝ ╚═╝        ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝"
    ]]
    displayLst = [[
        r"███████ ██ ██   ██ ███████ ██████          ██        ██████         ██████  ",
        r"██      ██  ██ ██  ██      ██   ██ ██     ███             ██             ██ ",
        r"█████   ██   ███   █████   ██   ██         ██         █████          █████  ",
        r"██      ██  ██ ██  ██      ██   ██ ██      ██        ██                  ██ ",
        r"██      ██ ██   ██ ███████ ██████          ██ ▄█     ███████ ▄█     ██████  "

    ],[
        r"██████   █████  ███    ██ ██████   ██████  ███    ███        ██████  ",
        r"██   ██ ██   ██ ████   ██ ██   ██ ██    ██ ████  ████ ██     ██   ██ ",
        r"██████  ███████ ██ ██  ██ ██   ██ ██    ██ ██ ████ ██        ██████  ",
        r"██   ██ ██   ██ ██  ██ ██ ██   ██ ██    ██ ██  ██  ██ ██     ██   ██ ",
        r"██   ██ ██   ██ ██   ████ ██████   ██████  ██      ██        ██   ██ "
            ]]

    for word in titleLst:
        os.system('cls' if os.name == 'nt' else 'clear')
        for line in word:
            sys.stderr.write(line)
            sys.stderr.write("\n")
        time.sleep(0.65)

    sys.stderr.write("\n\n\n")
    
    for option in displayLst:
        for line in option:
            sys.stderr.write(line)
            sys.stderr.write("\n")
        time.sleep(0.5)
        sys.stderr.write("\n")
    time.sleep(0.5)

    cardBacksLst = get_card_back(all=True)

    sys.stderr.write("\n")
    numbers([1, 1, 1], 0)
    
    for i in range(len(cardBacksLst[0])):
        for j in range(3):
            sys.stderr.write(cardBacksLst[j][i])
        sys.stderr.write("\n")
        time.sleep(0.15)
    time.sleep(0.5)

    while True:
        answer = input("... ")
        if answer == "r" or answer == "R" or answer == "Random" or answer == "random":
            update_table(CARD_BACKS_TABLE, f"card_back='r'")
            break
        elif answer == "1":
            update_table(CARD_BACKS_TABLE, f"card_back='1'")
            break
        elif answer == "2":
            update_table(CARD_BACKS_TABLE, f"card_back='2'")
            break
        elif answer == "3":
            update_table(CARD_BACKS_TABLE, f"card_back='3'")
            break
    main_menu()
            
def main_menu():
    optionsDisplayLst = [[
        r"███████ ████████  █████  ██████  ████████      ██████   █████  ███    ███ ███████        ███████ ",
        r"██         ██    ██   ██ ██   ██    ██        ██       ██   ██ ████  ████ ██      ██     ██      ",
        r"███████    ██    ███████ ██████     ██        ██   ███ ███████ ██ ████ ██ █████          ███████ ",
        r"     ██    ██    ██   ██ ██   ██    ██        ██    ██ ██   ██ ██  ██  ██ ██      ██          ██ ",
        r"███████    ██    ██   ██ ██   ██    ██         ██████  ██   ██ ██      ██ ███████        ███████ "
    ],[
        r"                           ██████  ██████  ████████ ██  ██████  ███    ██ ███████         ██████  ",
        r"                          ██    ██ ██   ██    ██    ██ ██    ██ ████   ██ ██      ██     ██    ██ ",
        r"                          ██    ██ ██████     ██    ██ ██    ██ ██ ██  ██ ███████        ██    ██ ",
        r"                          ██    ██ ██         ██    ██ ██    ██ ██  ██ ██      ██ ██     ██    ██ ",
        r"                           ██████  ██         ██    ██  ██████  ██   ████ ███████         ██████  "
    ],[
        r"             ██████  ██    ██ ██ ████████      ██████   █████  ███    ███ ███████         ██████  ",
        r"            ██    ██ ██    ██ ██    ██        ██       ██   ██ ████  ████ ██      ██     ██    ██ ",
        r"            ██    ██ ██    ██ ██    ██        ██   ███ ███████ ██ ████ ██ █████          ██    ██ ",
        r"            ██ ▄▄ ██ ██    ██ ██    ██        ██    ██ ██   ██ ██  ██  ██ ██      ██     ██ ▄▄ ██ ",
        r"             ██████   ██████  ██    ██         ██████  ██   ██ ██      ██ ███████         ██████  ",
        r"                ▀▀                                                                           ▀▀   "
    ]]

    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stderr.write("\n\n")
    for option in optionsDisplayLst:
        for line in option:
            sys.stderr.write(line)
            sys.stderr.write("\n")
            time.sleep(0.05)
        time.sleep(0.3)
        sys.stderr.write("\n")

    answer = input("             ... ")

    while True:
        if answer == "S" or answer == "s":
            os.system('cls' if os.name == 'nt' else 'clear')
            game_loop()
        elif answer == "Q" or answer == "q":
            os.system('cls' if os.name == 'nt' else 'clear')
            display_end_msg()
            time.sleep(2.5)
            quit()
        elif answer == "O" or answer == "o":
            os.system('cls' if os.name == 'nt' else 'clear')
            options()
        else:
            sys.stderr.write("Invalid Input")
        sys.stderr.write(ERASE_LINE)
        sys.stderr.write(CURSOR_UP_ONE)
        sys.stderr.write(ERASE_LINE)
        answer = input("... ")

def start_screen():
    database_setup()
    os.system('cls' if os.name == 'nt' else 'clear')
    welcomeTextLst = [[
        r"             _    _      _                            _          _   _           ",
        r"            | |  | | ___| | ___ ___  _ __ ___   ___  | |_ ___   | |_| |__   ___  ",
        r"            | |/\| |/ _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | __| '_ \ / _ \ ",
        r"            \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |_| | | |  __/ ",
        r"             \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \__|_| |_|\___| "
    ],
    [
        r"                _____               _   _____                           _ ",
        r"               /  __ \             | | |  __ \                         | |",
        r"               | /  \/ __ _ _ __ __| | | |  \/ __ _ _ __ ___   ___  ___| |",
        r"               | |    / _` | '__/ _` | | | __ / _` | '_ ` _ \ / _ \/ __| |",
        r"               | \__/\ (_| | | | (_| | | |_\ \ (_| | | | | | |  __/\__ \_|",
        r"                \____/\__,_|_|  \__,_|  \____/\__,_|_| |_| |_|\___||___(_)"
        r"                                                    (Only One)"

                    ]]
    
    for i in range(2):
        for line in welcomeTextLst[i]:
            sys.stderr.write(line)
            sys.stderr.write("\n")
            time.sleep(0.1)
        sys.stderr.write("\n")


    time.sleep(1)
    answer = input("                            Press enter to start... ")
    while True:
        if answer == "":
            main_menu()
            break
        elif answer == "credits":
            credits()
            break
        elif answer == "egg":
            start_1()
            break
        sys.stderr.write(CURSOR_UP_ONE)
        sys.stderr.write(ERASE_LINE)
        answer = input("                            Press ENTER to start!... ")

lst = [
            r".-----------.",
            r"|           |",
            r"|           |",
            r"|           |",
            r"|           |", 
            r"|           |", 
            r"|           |",
            r"| ███‾|‾███ |",
            r"| ███___███ |", 
            r"`-----------'"
]

if __name__ == "__main__":
    start_screen()
