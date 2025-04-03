import pygame
from pygame import Surface
from pygame.color import Color
from pygame.event import Event

from pyrograph.rotor import Rotor
from pyrograph.stator import Stator


def pyrograph():
    pygame.init()
    pygame.display.set_caption("pyrograph")
    surface: Surface = pygame.display.set_mode([1024, 768])
    draw_surface(surface)
    stator: Stator = Stator(surface, 100)
    rotor: Rotor = Rotor(surface, stator, 75)
    time: int = 0
    while True:
        for event in pygame.event.get():
            check_for_quit(event)
        keys = pygame.key.get_pressed()
        rotor.check_for_change(keys)
        stator.check_for_change(keys)
        draw_surface(surface)
        stator.draw()
        if not keys[pygame.K_SPACE]:
            rotor.rotate(time)
            pygame.display.flip()
        time += 1


def check_for_quit(event: Event):
    if event.type == pygame.QUIT:
        pygame.quit()


def draw_surface(
    surface: Surface,
    background_color: Color = Color("white"),
):
    surface.fill(background_color)
    return surface


if __name__ == "__main__":
    pyrograph()
