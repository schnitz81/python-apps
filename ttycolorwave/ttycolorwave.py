import time
import random
from colorama import Back


def switch_back_color(rndnbr):
    if rndnbr == 1:
        print(Back.RED, end="")
    elif rndnbr == 2:
        print(Back.GREEN, end="")
    elif rndnbr == 3:
        print(Back.YELLOW, end="")
    elif rndnbr == 4:
        print(Back.BLUE, end="")
    elif rndnbr == 5:
        print(Back.MAGENTA, end="")
    elif rndnbr == 6:
        print(Back.CYAN, end="")
    elif rndnbr == 7:
        print(Back.WHITE, end="")


def waver():
    pos1 = 26
    pos2 = 52

    while True:
        col1 = random.randint(1, 7)
        col2 = random.randint(1, 7)
        col3 = random.randint(1, 7)
        while col1 == col2:
            col2 = random.randint(1, 7)
        while col3 == col1 or col3 == col2:
            col3 = random.randint(1, 7)
        for x in range(1, 200):
            switch_back_color(col1)

            for i in range(0, pos1):
                print(' ', end="")
            switch_back_color(col2)
            for i in range(0, pos2 - pos1):
                print(' ', end="")
            switch_back_color(col3)
            for i in range(0, 80 - pos2):
                print(' ', end="")
            print(Back.RESET)  # newline

            # pos1 movement
            rnd = random.randint(0, 2)
            if rnd == 0 and pos1 < 80 and pos1 < pos2 or pos1 <= 0:
                pos1 += 1
            elif rnd == 1 or pos1 >= 80:
                pos1 -= 1

            # pos2 movement
            rnd = random.randint(0, 2)
            if rnd == 0 and pos2 < 80 or pos2 <= 0:
                pos2 += 1
            elif rnd == 1 and pos2 > pos1 or pos2 >= 80:
                pos2 -= 1

            time.sleep(.02)


if __name__ == '__main__':
    waver()

