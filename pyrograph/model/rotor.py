from __future__ import annotations
import pygame
from typing import Optional
from pydantic import Field
from math import cos, sin
from pyrograph.model.circle import Circle

TYPE = "rotor"


class Rotor(Circle):
    parent: Optional[Circle] = Field(default=None, exclude=True)
    type: str = TYPE
    inside: bool = False
    line_width: int = 1
    line_length: int = 1000
    trace: list[tuple[float, float]] = Field(default_factory=list, exclude=True)
    children: list[Rotor] = Field(default_factory=list)

    def remove_child(self, circle: Circle):
        if self == circle:
            self.parent.children.remove(circle)
        else:
            for child in self.children:
                child.remove_child(circle)

    def draw_children(self, surface, t):
        self.draw(surface, t)
        for child in self.children:
            child.draw_children(surface, t)

    def draw(self, surface, t):
        theta = self.get_theta(t)
        self.trace_point(theta)
        self.draw_circle(surface)
        self.draw_selection(surface)
        self.draw_rotation_marker(surface, theta)
        self.draw_line(surface)

    def get_theta(self, t):
        px, py = self.parent.get_position()

        # Rotation direction & distance
        sign = -1 if self.inside else 1
        distance = (
            self.parent.radius - self.radius
            if self.inside
            else self.parent.radius + self.radius
        )

        # Rotor center
        angle = self.omega * t
        self.x = px + distance * cos(angle)
        self.y = py + distance * sin(angle)

        # Rotor's own spin (rolling without slipping)
        return -sign * (distance / self.radius) * self.omega * t

    def trace_point(self, theta):
        if self.radius is not None:
            x_trace = self.x + self.radius * cos(theta)
            y_trace = self.y + self.radius * sin(theta)
            self.trace.append((x_trace, y_trace))

    def draw_circle(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface,
            pygame.Color("white"),
            (int(self.x), int(self.y)),
            self.radius,
            self.width,
        )

    def draw_rotation_marker(self, surface: pygame.Surface, theta):
        marker_length = self.radius - 5
        x_marker = self.x + marker_length * cos(theta)
        y_marker = self.y + marker_length * sin(theta)
        pygame.draw.line(
            surface,
            pygame.Color(self.color),
            (int(self.x), int(self.y)),
            (int(x_marker), int(y_marker)),
            2,
        )

    def draw_line(self, surface: pygame.Surface):
        if self.trace and len(self.trace) > 1:
            pygame.draw.lines(
                surface,
                pygame.Color(self.color),
                False,
                [(int(x), int(y)) for x, y in self.trace],
                self.line_width,
            )
        # trim tail
        if len(self.trace) > self.line_length:
            self.trace.pop(0)
