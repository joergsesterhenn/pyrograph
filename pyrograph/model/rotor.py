import pygame
from typing import Optional
from pydantic import Field
from math import cos, sin
from pyrograph.model.circle import Circle


class Rotor(Circle):
    parent: Circle
    trace_radius: Optional[float] = 50
    inside: bool = False
    line_width: int = 1
    line_length: int = 1000
    trace: list[tuple[float, float]] = Field(default_factory=list, exclude=True)

    def get_theta(self, t):
        # Resolve parent position
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

    def get_position(self):
        return self.x, self.y

    def draw(self, surface, t):
        theta = self.get_theta(t)

        # Traced point
        if self.trace_radius is not None:
            x_trace = self.x + self.trace_radius * cos(theta)
            y_trace = self.y + self.trace_radius * sin(theta)
            self.trace.append((x_trace, y_trace))

        # Circle
        pygame.draw.circle(
            surface,
            pygame.Color("white"),
            (int(self.x), int(self.y)),
            self.radius,
            self.width,
        )

        # Rotation marker
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

        # Trace path
        if self.trace and len(self.trace) > 1:
            pygame.draw.lines(
                surface,
                pygame.Color(self.color),
                False,
                [(int(x), int(y)) for x, y in self.trace],
                self.line_width,
            )
        if len(self.trace) > self.line_length:
            self.trace.pop(0)


# Rotor.model_rebuild()
