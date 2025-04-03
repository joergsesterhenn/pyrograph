import pygame
from math import cos, sin
from pygame import Surface
from pygame.color import Color
from pyrograph.stator import Stator


class Rotor:
    def __init__(
        self,
        surface: Surface,
        stator: Stator,
        radius: int,
        line_color=Color("red"),
        rotor_color=Color("black"),
    ):
        self.surface = surface
        self.radius = radius
        self.stator = stator
        (x, y) = stator.center()
        y += (stator.radius) + radius
        self.center_x = x
        self.center_y = y
        self.rotor_color = rotor_color
        self.line_color = line_color
        self.line: list[int:int] = []

    def center(self) -> tuple[int, int]:
        return (self.center_x, self.center_y)

    def rotate(self, t: int):
        # move rotor one step along stator
        (x_stator, y_stator) = self.stator.center()
        self.center_x = x_stator + (self.stator.radius + self.radius) * cos(
            self.stator.omega * t
        )
        self.center_y = y_stator + (self.stator.radius + self.radius) * sin(
            self.stator.omega * t
        )

        # Calculate tracing point
        theta_rotor = (
            -((self.stator.radius + self.radius) / self.radius) * self.stator.omega * t
        )
        (x, y) = self.center()
        x_line = x + self.radius * cos(theta_rotor)
        y_line = y + self.radius * sin(theta_rotor)

        self.line.append((x_line, y_line))
        # draw rotor
        self.draw_rotor()
        self.draw_line()

    def draw_rotor(self):
        pygame.draw.circle(
            self.surface, self.rotor_color, self.center(), self.radius, 1
        )

    def draw_line(self):
        if self.line and len(self.line) > 1:
            pygame.draw.lines(self.surface, self.line_color, False, self.line, 1)
