import pygame
import sys
from time import perf_counter

import variables
import event_handlers
import button
import text


background: pygame.Surface
screen: pygame.display
entities = []
flags_text: text.Text
won = False
playing = True

prev_time: float


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
    if not playing:
        return

    global prev_time, flags_text
    dt = perf_counter() - prev_time

    flags_text.set_text("Flags: " + (str(button.mines.flags) if not button.first_click else str(button.num_mines)))

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

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        event_handlers.show_mines()

    for entity in entities:
        background.blit(entity.img, (entity.x, entity.y))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    prev_time = perf_counter()
