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
        stator_radius: int = 100,
        stator_angular_velocity: float = 0.02,
        color=Color("blue"),
    ):
        super().__init__(
            surface,
            (surface.get_width() // 2, surface.get_height() // 2),
            stator_radius,
            stator_angular_velocity,
            color,
        )

    def center(self) -> tuple[int, int]:
        return (self.surface.get_width() // 2, self.surface.get_height() // 2)

    def check_for_change(self, keys: ScancodeWrapper):
        if keys[pygame.K_DOWN] and self._radius > 5:
            self._radius -= 1
        if keys[pygame.K_UP] and self._radius < 200:
            self._radius += 1
