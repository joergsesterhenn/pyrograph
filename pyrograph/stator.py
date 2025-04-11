import pygame
from pygame import Surface
from pygame.color import Color
from pygame.key import ScancodeWrapper

from pyrograph.circle import Circle


class Stator(Circle):
    """
    Unmovable Object.
    """

    def __init__(
        self,
        surface: Surface,
        x: float,
        y: float,
        stator_radius: float = 100,
        stator_angular_velocity: float = 0.002,
        color=Color("blue"),
    ):
        super().__init__(
            surface,
            (surface.get_width() // 2, surface.get_height() // 2),
            stator_radius,
            color,
        )
        self._angular_velocity = stator_angular_velocity
        self.x = x
        self.y = y

    def center(self) -> tuple[float, float]:
        return (self.x, self.y)

    def angular_velocity(self) -> float:
        return self._angular_velocity

    def check_for_change(self, keys: ScancodeWrapper):
        if keys[pygame.K_DOWN] and self._radius > 5:
            self._radius -= 1
        if keys[pygame.K_UP] and self._radius < 200:
            self._radius += 1
