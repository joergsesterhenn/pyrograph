import pygame
from pygame import Surface
from pygame.color import Color
from pygame.key import ScancodeWrapper


class Stator:
    def __init__(self, surface: Surface, radius: int = 100, omega: float = 0.02):
        self.radius = radius
        self.surface = surface
        self.omega = omega

    def draw(
        self,
        line_width: int = 1,
        color: Color = Color("blue"),
    ):
        pygame.draw.circle(
            surface=self.surface,
            color=color,
            center=self.center(),
            radius=self.radius,
            width=line_width,
        )

    def center(self) -> tuple[int, int]:
        return (self.surface.get_width() // 2, self.surface.get_height() // 2)

    def check_for_change(self, keys: ScancodeWrapper):
        if keys[pygame.K_DOWN] and self.radius > 5:
            self.radius -= 1
        if keys[pygame.K_UP] and self.radius < 200:
            self.radius += 1
