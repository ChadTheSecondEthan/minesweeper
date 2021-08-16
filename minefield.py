from random import random


class MineField:

    def __init__(self, size, mines):
        self.num_mines = mines
        self.flags = mines
        self.size = size

        self.mines = []

        self.has_mine = [[False for _ in range(size)] for _ in range(size)]
        for i in range(size):
            x = int(random() * size)
            y = int(random() * size)
            while self.has_mine[x][y]:
                x = int(random() * size)
                y = int(random() * size)
            self.has_mine[x][y] = True

    def check_mines(self):
        for mine in self.mines:
            if not mine.flagged:
                return False
        print("Game over!")
        return True
