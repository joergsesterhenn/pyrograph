import pygame
from pydantic import Field

from pyrograph.model.circle import Circle
from pyrograph.model.rotor import Rotor

TYPE = "stator"


class Stator(Circle):
    x: int = 400
    y: int = 300
    width: int = 0
    type: str = TYPE
    children: list[Rotor] = Field(default_factory=list)

    def draw(self, surface, t=0):
        if self.drawn and not self.hidden:
            self.draw_disc(surface)
            self.draw_selection(surface)

    def draw_disc(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface,
            pygame.Color(self.color),
            (int(self.x), int(self.y)),
            self.radius,
            self.width,
        )
