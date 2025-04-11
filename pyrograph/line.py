from pygame import Color, Surface, draw


class Line:
    """
    List of points that can be drawn.
    """

    def __init__(
        self,
        surface: Surface,
        color: Color = Color("red"),
        points: list[float:float] = [],
        width: float = 1,
    ):
        self.points: list[float:float] = points
        self.color: Color = color
        self.surface: Surface = surface
        self.width: float = width

    def add(self, point: tuple[float, float]):
        self.points.append(point)

    def draw(self):
        if self.points and len(self.points) > 1:
            draw.lines(self.surface, self.color, False, self.points, self.width)
