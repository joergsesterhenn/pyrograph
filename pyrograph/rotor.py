from math import cos, sin

import pygame
from pygame import Surface
from pygame.color import Color
from pygame.key import ScancodeWrapper

from pyrograph.circle import Circle
from pyrograph.line import Line


class Rotor(Circle):
    """
    Rotating object that draws lines.
    """

    def __init__(
        self,
        surface: Surface,
        parent: Circle,
        rotor_radius: int,
        line_color=Color("red"),
        line_width=2,
        color=Color("black"),
    ):
        x, y = parent.center()
        y += parent.radius() + rotor_radius
        super().__init__(surface, (x, y), rotor_radius, 0.02, color)
        self.line: Line = Line(surface=surface, color=line_color, width=line_width)
        self.parent: Circle = parent
        parent.add_child(self)

    def center(self) -> tuple[int, int]:
        return self._center

    def rotate(self, t: int):
        self.parent.draw()
        # move rotor one step along parent
        (x_parent, y_parent) = self.parent.center()

        center_x = x_parent + (self.parent.radius() + self.radius()) * cos(
            self.parent.angular_velocity() * t
        )
        center_y = y_parent + (self.parent.radius() + self.radius()) * sin(
            self.parent.angular_velocity() * t
        )
        self._center = (center_x, center_y)
        self.draw()

        # Calculate tracing point
        self._angular_velocity = (
            -((self.parent.radius() + self.radius()) / self.radius())
            * self.parent.angular_velocity()
            * t
        )
        (x, y) = self.center()
        x_line = x + self.radius() * cos(self.angular_velocity())
        y_line = y + self.radius() * sin(self.angular_velocity())

        self.line.add(x_line, y_line)
        self.line.draw()
        for child in self.children:
            child.rotate(t)

    def check_for_change(self, keys: ScancodeWrapper):
        if keys[pygame.K_LEFT] and self._radius > 5:
            self._radius -= 1
            self.line = Line(self.surface, points=[])
        if keys[pygame.K_RIGHT] and self._radius < 200:
            self._radius += 1
            self.line = Line(self.surface, points=[])
        if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.line = Line(self.surface, points=[])
