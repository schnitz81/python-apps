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
    pos = 39
    while True:
        col1 = random.randint(1, 7)
        col2 = random.randint(1, 7)
        while col2 == col1:
            col2 = random.randint(1, 7)
        for x in range(1, 100):
            switch_back_color(col1)
            for i in range(0, pos):
                print(' ', end="")
            switch_back_color(col2)
            for i in range(0, 80 - pos):
                print(' ', end="")
            print(Back.RESET)  # newline
            rnd = random.randint(0, 2)
            if rnd == 0 and pos < 80 or pos <= 0:
                pos += 1
            elif rnd == 1 or pos >= 80:
                pos -= 1
            time.sleep(.03)


if __name__ == '__main__':
    waver()

