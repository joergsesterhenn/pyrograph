from abc import ABC, abstractmethod
from typing import Self

import pygame


class Circle(ABC):
    """
    Objects of a circular nature with a center and radius that can be drawn.
    Circles can have children.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        circle_center: tuple[int:int],
        circle_radius: int,
        circle_angular_velocity: int,
        color: pygame.Color,
    ):
        super().__init__()
        self.surface = surface
        self._angular_velocity = circle_angular_velocity
        self._center = circle_center
        self._radius = circle_radius
        self.color = color
        self.children: list[Self] = []

    @abstractmethod
    def center(self) -> tuple[int, int]:
        pass

    def radius(self) -> int:
        return self._radius

    def angular_velocity(self) -> float:
        return self._angular_velocity

    def draw(self):
        pygame.draw.circle(
            surface=self.surface,
            color=self.color,
            center=self.center(),
            radius=self.radius(),
            width=1,
        )

    def add_child(self, circle: Self):
        self.children.append(circle)

    def get_child(self, index: int) -> Self | None:
        if -1 < index < len(self.children):
            return self.children[index]
