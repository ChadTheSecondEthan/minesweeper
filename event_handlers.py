import pygame
import sys

import button
import game_loop


def handle_mouse_down(event):
    if game_loop.won:
        return

    pos = pygame.mouse.get_pos()
    mouse_button = event.button
    button_clicked = button.button_in_grid(pos)
    if button_clicked:
        if mouse_button == 1:
            if button.first_click:
                button_clicked.on_first_click()
                button.first_click = False
            button_clicked.mine()
        elif not button.first_click:
            button_clicked.flag()


def show_mines():
    for b in button.grid:
        if b.is_mine():
            b.set_color((128, 128, 128))


event_handlers = {
    pygame.QUIT: lambda event: sys.exit(),
    pygame.MOUSEBUTTONDOWN: lambda event: handle_mouse_down(event),
}
