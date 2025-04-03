import pygame
from pygame import Surface
from pygame.color import Color
from pygame.event import Event


def main():
    screen: Surface = draw_screen()
    running: bool = True
    while running:
        for event in pygame.event.get():
            running = check_for_quit(event)
            draw_stator(screen)
            pygame.display.flip()

    pygame.quit()


def check_for_quit(event: Event):
    if event.type == pygame.QUIT:
        return False


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


if __name__ == "__main__":
    main()
