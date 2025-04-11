from math import cos, sin

import pygame
from pygame import Surface
from pygame.color import Color
from pygame.key import ScancodeWrapper
import rich

from pyrograph.circle import Circle
from pyrograph.line import Line


class Rotor(Circle):
    """
    Rotatable object that draws lines.
    """

    def __init__(
        self,
        surface: Surface,
        parent: Circle,
        rotor_radius: float,
        line_color: Color = Color("red"),
        line_width: int = 2,
        color: Color = Color("black"),
    ):
        self.parent: Circle = parent
        self.line: Line = Line(surface=surface, color=line_color, width=line_width)
        parent.add_child(self)
        super().__init__(surface, self.get_tracing_point(0), rotor_radius, color)

    def center(self) -> tuple[float, float]:
        return self._center

    def angular_velocity(self) -> float:
        return -(
            ((self.parent.radius() + self.radius()) / self.radius())
            * self.parent.angular_velocity()
        )

    def get_tracing_point(self, t):
        self._angular_position = self.angular_velocity() * t

        (x, y) = self.center()
        x_line = x + self.radius() * cos(self._angular_position)
        y_line = y + self.radius() * sin(self._angular_position)

        return (x_line, y_line)

    def rotate(self, t: int):
        # self.parent.draw()
        # move rotor one step along parent
        (x_parent, y_parent) = self.parent.center()

        center_x = x_parent + (self.parent.radius() + self.radius()) * cos(
            self.parent.angular_velocity() * t
        )
        center_y = y_parent + (self.parent.radius() + self.radius()) * sin(
            self.parent.angular_velocity() * t
        )
        self._center = (center_x, center_y)
        rich.inspect(self)
        self.draw()
        self.line.add(self.get_tracing_point(t))
        rich.inspect(self.line)
        self.line.draw()
        for child in self.children:
            rich.inspect(child)
            child.rotate(t)
        # breakpoint()

    def check_for_change(self, keys: ScancodeWrapper):
        if keys[pygame.K_LEFT] and self._radius > 5:
            self._radius -= 1
            self.line = Line(self.surface, points=[])
        if keys[pygame.K_RIGHT] and self._radius < 200:
            self._radius += 1
            self.line = Line(self.surface, points=[])
        if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.line = Line(self.surface, points=[])
