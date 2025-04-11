from abc import ABC, abstractmethod
from typing import Self

from pygame import Color, Surface, draw


class Circle(ABC):
    """
    Objects of a circular nature with a center and radius that can be drawn.
    Circles can have children that rotate around them.
    """

    def __init__(
        self,
        surface: Surface,
        circle_center: tuple[float:float],
        circle_radius: float,
        color: Color,
    ):
        super().__init__()
        self.surface: Surface = surface
        self._radius: float = circle_radius
        self._center: tuple[float, float] = circle_center
        self.color: Color = color
        self.children: list[Self] = []

    @abstractmethod
    def center(self) -> tuple[float, float]:
        pass

    def radius(self) -> float:
        return self._radius

    @abstractmethod
    def angular_velocity(self) -> float:
        pass

    def draw(self):
        draw.circle(
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
