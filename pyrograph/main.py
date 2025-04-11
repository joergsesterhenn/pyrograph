import pygame
from pygame import Surface
from pygame.color import Color
from pygame.event import Event
import typer

from pyrograph.rotor import Rotor
from pyrograph.stator import Stator

app = typer.Typer()


@app.command()
def pyrograph():
    pygame.init()
    pygame.display.set_caption("pyrograph")
    surface: Surface = pygame.display.set_mode([1024, 768])
    clock = pygame.time.Clock()
    draw_surface(surface)
    stator: Stator = Stator(
        surface=surface,
        stator_radius=100,
        x=surface.get_width() // 2,
        y=surface.get_height() // 2,
    )
    rotor: Rotor = Rotor(
        surface=surface,
        parent=stator,
        rotor_radius=75,
        color=Color("black"),
        line_width=3,
        line_color=Color("red"),
    )
    # rotor2: Rotor = Rotor(
    #     surface=surface,
    #     parent=rotor,
    #     rotor_radius=50,
    #     color=Color("brown"),
    #     line_width=3,
    #     line_color=Color("green"),
    # )
    time: int = 0
    while True:
        for event in pygame.event.get():
            check_for_quit(event)
        keys = pygame.key.get_pressed()
        # rotor.check_for_change(keys)
        # stator.check_for_change(keys)
        draw_surface(surface)
        if not keys[pygame.K_SPACE]:
            stator.draw()
            rotor.rotate(time)
            pygame.display.flip()
            time += 1
        clock.tick(3)


def check_for_quit(event: Event):
    if event.type == pygame.QUIT:
        pygame.quit()


def draw_surface(
    surface: Surface,
    background_color: Color = Color("white"),
):
    surface.fill(background_color)
    return surface
