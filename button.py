import entity
import event_handlers
import fonts
import minefield
import game_loop

W = 50
H = 50
grid = []
first_click = True
mines: minefield.MineField
mine_size = 10
num_mines = 20


class Button(entity.Entity):
    mines_around: int

    def __init__(self, x, y, index_x, index_y):
        super().__init__(x, y, W, H)
        self.index_x = index_x
        self.index_y = index_y
        self.mined = self.flagged = False

        self.set_color((255, 255, 255))

    def mine(self):
        if not self.flagged:
            self.mined = True
            self.set_color((0, 0, 0))
            if self.is_mine():
                for b in grid:
                    if b.is_mine():
                        b.set_color((128, 128, 128))
                    elif b.flagged:
                        b.set_color((255, 255, 255))
                game_loop.playing = False
            elif self.mines_around == 0:
                self.mine_surrounding()
            elif self.mines_around != 0:
                self.show_mine_number()

            check_win()

    def flag(self):
        if self.flagged:
            mines.flags += 1
            self.flagged = False
            self.set_color((255, 255, 255))
            self.show_mine_number()
        elif not self.mined and mines.flags > 0:
            mines.flags -= 1
            self.flagged = True
            self.set_color((255, 0, 0))
            mines.check_mines()

    def mine_surrounding(self):
        for button in self.get_all_buttons_around():
            if not button.mined and not button.flagged and not button.is_mine():
                button.mine()

    def show_mine_number(self):
        if self.mines_around != 0 and not self.is_mine():
            self.img.blit(fonts.main_font.render(str(self.mines_around), False, (255, 255, 255)), (5, 3))

    def is_mine(self):
        return mines.has_mine[self.index_x][self.index_y]

    def get_mines_around(self):
        num = 0
        for x in range(max(self.index_x - 1, 0), min(self.index_x + 2, mine_size), 1):
            for y in range(max(self.index_y - 1, 0), min(self.index_y + 2, mine_size), 1):
                if (x != self.index_x or y != self.index_y) and mines.has_mine[x][y]:
                    num += 1
        return num

    def get_buttons_around(self):
        buttons = []
        for x in range(max(self.index_x - 1, 0), min(self.index_x + 2, mine_size), 1):
            for y in range(max(self.index_y - 1, 0), min(self.index_y + 2, mine_size), 1):
                if (x + y) % 2 != (self.index_y + self.index_x) % 2:
                    buttons.append(grid[mine_size * x + y])
        return buttons

    def get_all_buttons_around(self, num_spaces=1):
        buttons = []
        for index in self.get_surrounding_indexes(num_spaces):
            buttons.append(grid[index])
        return buttons

    def on_first_click(self):
        global mines
        indexes = self.get_surrounding_indexes(2)
        indexes.append(self.index_x * mine_size + self.index_y)
        mines = minefield.MineField(mine_size, num_mines, indexes)

        for button in grid:
            if button.is_mine():
                mines.mines.append(button)
            button.mines_around = button.get_mines_around()

    def get_surrounding_indexes(self, num_spaces=1):
        indexes = []
        for x in range(max(self.index_x - num_spaces, 0), min(self.index_x + num_spaces + 1, mine_size), 1):
            for y in range(max(self.index_y - num_spaces, 0), min(self.index_y + num_spaces + 1, mine_size), 1):
                if x != self.index_x or self.index_y != y:
                    indexes.append(x * mine_size + y)
        return indexes


def check_win():
    for button in grid:
        if not button.is_mine():
            if not button.mined:
                return
    game_loop.won = True


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
