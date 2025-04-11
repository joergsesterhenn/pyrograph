import pygame
from pydantic import Field

from pyrograph.model.circle import Circle
from pyrograph.model.rotor import Rotor


class Stator(Circle):
    x: int = 400  # default screen center
    y: int = 300
    width: int = 0
    type: str = "stator"
    children: list[Rotor] = Field(default_factory=list)

    def get_position(self):
        return self.x, self.y

    def draw(self, surface, t=0):
        pygame.draw.circle(
            surface,
            pygame.Color(self.color),
            (int(self.x), int(self.y)),
            self.radius,
            self.width,
        )
