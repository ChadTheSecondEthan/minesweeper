import pygame
import sys

import button


def handle_mouse_down(event):
    pos = pygame.mouse.get_pos()
    mouse_button = event.button
    button_clicked = button.button_in_grid(pos)
    if button_clicked:
        if mouse_button == 1:
            button_clicked.mine()
        else:
            button_clicked.flag()


event_handlers = {
    pygame.QUIT: lambda event: sys.exit(),
    pygame.MOUSEBUTTONDOWN: lambda event: handle_mouse_down(event),
}
