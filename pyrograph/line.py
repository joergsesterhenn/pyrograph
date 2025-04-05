from pygame import Color, Surface
import pygame


class Line:
    """
    List of points that can be drawn.
    """

    def __init__(
        self,
        surface: Surface,
        color: Color = Color("red"),
        points: list[int:int] = [],
        width=1,
    ):
        self.points: list[int:int] = points
        self.color: Color = color
        self.surface = surface
        self.width = width

    def add(self, x: int, y: int):
        self.points.append((x, y))

    def draw(self):
        if self.points and len(self.points) > 1:
            pygame.draw.lines(self.surface, self.color, False, self.points, self.width)
