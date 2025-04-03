import pygame
from pygame import Surface
from pygame.color import Color


class Stator:
    def __init__(self, surface: Surface, radius: int):
        self.radius = radius
        self.surface = surface

    def draw(
        self,
        radius: int = 100,
        line_width: int = 1,
        color: Color = Color("blue"),
    ):
        pygame.draw.circle(
            surface=self.surface,
            color=color,
            center=self.center(),
            radius=radius,
            width=line_width,
        )

    def center(self) -> tuple[int, int]:
        return (self.surface.get_width() // 2, self.surface.get_height() // 2)
