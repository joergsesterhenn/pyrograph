import pygame
from pygame import Surface
from pygame.color import Color
from pygame.event import Event


def main():
    screen: Surface = draw_screen()
    rotor: Rotor = Rotor(screen, radius=75, center_x=0, center_y=0)
    running: bool = True
    while running:
        for event in pygame.event.get():
            check_for_quit(event)
        draw_stator(screen)
        rotor.rotate()
        pygame.display.flip()
    pygame.quit()


def check_for_quit(event: Event):
    if event.type == pygame.QUIT:
        pygame.quit()


def draw_screen(
    background_color: Color = Color("white"), width: int = 1000, height: int = 750
) -> Surface:
    pygame.init()
    pygame.display.set_caption("pyrograph")
    screen: Surface = pygame.display.set_mode([width, height])
    screen.fill(background_color)
    return screen


def draw_stator(
    screen: Surface,
    radius: int = 100,
    line_width: int = 2,
    color: Color = Color("blue"),
):
    pygame.draw.circle(
        surface=screen,
        color=color,
        center=(screen.get_width() // 2, screen.get_height() // 2),
        radius=radius,
        width=line_width,
    )


class Rotor:
    def __init__(
        self,
        surface: Surface,
        radius: int,
        center_x: int,
        center_y: int,
        line_color=Color("red"),
        rotor_color=Color("black"),
    ):
        self.surface = surface
        self.radius = radius
        self.center_x = center_x
        self.center_y = center_y
        self.rotor_color = rotor_color
        self.line_color = line_color
        self.line: list[int:int] = []

    def center(self) -> tuple[int, int]:
        return (self.center_x, self.center_y)

    def rotate(self):
        # move rotor one step along stator
        self.center_x += 1
        self.center_y += 1
        self.line.append(self.center())
        # draw rotor
        self.draw_rotor()
        self.draw_line()

    def draw_rotor(self):
        pygame.draw.circle(
            self.surface, self.rotor_color, self.center(), self.radius, 2
        )

    def draw_line(self):
        if self.line and len(self.line) > 1:
            pygame.draw.lines(self.surface, self.line_color, False, self.line, 2)


if __name__ == "__main__":
    main()
