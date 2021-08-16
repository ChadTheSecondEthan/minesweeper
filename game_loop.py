import pygame
import sys
from time import perf_counter

import variables
import event_handlers
import button
import text
from minefield import MineField


background: pygame.Surface
screen: pygame.display
entities = []
flags_text: text.Text

prev_time: float
minefield = MineField(10, 10)


def start(s):
    global prev_time, background, screen, flags_text

    prev_time = perf_counter()

    screen = s

    background = pygame.Surface(variables.SCREEN_SIZE)
    background = background.convert()

    entities.extend(button.create_grid((5, 45), 10))

    flags_text = text.Text("Flags: ", 10, 10)
    entities.append(flags_text)


def update():
    global prev_time, flags_text
    dt = perf_counter() - prev_time

    flags_text.set_text("Flags: " + str(minefield.flags))

    for entity in entities:
        entity.update(dt)

    background.fill(variables.BG_COLOR)
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()

    for event in pygame.event.get():
        try:
            event_handlers.event_handlers[event.type](event)
        except KeyError:
            continue

    for entity in entities:
        background.blit(entity.img, (entity.x, entity.y))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    prev_time = perf_counter()
