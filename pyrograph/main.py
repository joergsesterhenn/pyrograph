import pygame
from pygame import Surface
from pygame.color import Color
from pygame.event import Event

from pyrograph.stator import Stator
from pyrograph.rotor import Rotor


def main():
    pygame.init()
    pygame.display.set_caption("pyrograph")
    surface: Surface = pygame.display.set_mode([1024, 768])
    draw_surface(surface)
    stator: Stator = Stator(surface, 100)
    rotor: Rotor = Rotor(surface, stator, 75)
    running: bool = True
    time: int = 0
    while running:
        for event in pygame.event.get():
            check_for_quit(event)
        draw_surface(surface)
        stator.draw()
        rotor.rotate(time)
        pygame.display.flip()
        time += 1
    pygame.quit()


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
    main()
