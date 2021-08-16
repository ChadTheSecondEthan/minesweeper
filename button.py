import entity
import fonts
import game_loop

W = 50
H = 50
grid = []


class Button(entity.Entity):

    def __init__(self, x, y, index_x, index_y):
        super().__init__(x, y, W, H)
        self.index_x = index_x
        self.index_y = index_y
        self.mined = self.flagged = False
        self.mines_around = self.get_mines_around()

        if self.mines_around != 0 and not self.is_mine():
            self.img.blit(fonts.main_font.render(str(self.mines_around), False, (0, 0, 0)), (5, 3))

        if self.is_mine():
            game_loop.minefield.mines.append(self)

    def mine(self):
        if not self.flagged:
            self.mined = True
            self.set_color((0, 0, 0))
            if self.is_mine():
                print("Mine mined! You lose!")
            else:
                self.mine_surrounding()

    def flag(self):
        game_loop.minefield.flags -= 1
        if self.flagged:
            game_loop.minefield.flags += 1
            self.flagged = False
            self.set_color((255, 255, 255))
        elif not self.mined:
            self.flagged = True
            self.set_color((255, 0, 0))
            game_loop.minefield.check_mines()

    def mine_surrounding(self):
        for button in self.get_buttons_around():
            if not button.mined:
                button.mine()

    def is_mine(self):
        return game_loop.minefield.has_mine[self.index_x][self.index_y]

    def get_mines_around(self):
        mines = 0
        for x in range(max(self.index_x - 1, 0), min(self.index_x + 2, game_loop.minefield.size), 1):
            for y in range(max(self.index_y - 1, 0), min(self.index_y + 2, game_loop.minefield.size), 1):
                if (x != self.index_x or y != self.index_y) and game_loop.minefield.has_mine[x][y]:
                    mines += 1
        return mines

    def get_buttons_around(self):
        buttons = []
        for x in range(max(self.index_x - 1, 0), min(self.index_x + 2, game_loop.minefield.size), 1):
            for y in range(max(self.index_y - 1, 0), min(self.index_y + 2, game_loop.minefield.size), 1):
                if x != self.index_x or y != self.index_y:
                    buttons.append(grid[x][y])
        return buttons


def create_grid(pos, length):
    global grid
    for i in range(length):
        for j in range(length):
            grid.append(Button(pos[0] + i * (W + 5), pos[1] + j * (H + 5), i, j))
    return grid


def button_in_grid(pos):
    for button in grid:
        if button.intersects_point(pos):
            return button
