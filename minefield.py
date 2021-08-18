from random import random


class MineField:

    def __init__(self, size, mines, illegal_indexes):
        self.num_mines = mines
        self.flags = mines
        self.size = size

        self.mines = []

        self.has_mine = [[False for _ in range(size)] for _ in range(size)]
        for i in range(mines):
            x = int(random() * size)
            y = int(random() * size)
            while self.has_mine[x][y] or (x * size + y) in illegal_indexes:
                x = int(random() * size)
                y = int(random() * size)
            self.has_mine[x][y] = True

    def check_mines(self):
        for mine in self.mines:
            if not mine.flagged:
                return False
        print("Game over!")
        return True

    # def generate_random_mines(self, num, illegal_indexes):
    #     locations = []
    #     for i in range(num):
    #         locations.append(self.generate_random_mine(illegal_indexes))
    #     return locations
    #
    # def generate_random_mine(self, illegal_indexes):
    #     x = int(random() * self.size)
    #     y = int(random() * self.size)
    #     while self.has_mine[x][y] and (x * self.size + y) in illegal_indexes:
    #         x = int(random() * self.size)
    #         y = int(random() * self.size)
    #     self.has_mine[x][y] = True
    #     return x, y
