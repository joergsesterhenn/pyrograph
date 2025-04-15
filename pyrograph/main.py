import pygame
from rich.pretty import pprint
import typer
from pygame.color import Color

from pyrograph.model.circle import Circle
from pyrograph.model.model import (
    load_model_from_json,
    save_model_to_json,
)
from pyrograph.model.pyrograph import PyroGraph
from pyrograph.model.rotor import Rotor
from pyrograph.model.stator import Stator


FPS = 60
START_WIDTH, START_HEIGHT = 1200, 800
SIDEBAR_WIDTH = 400
BACKGROUND_COLOR = Color("black")

input_boxes = []
toggle_rects = []
color_buttons = []
app = typer.Typer()


@app.command()
def pyrograph():
    pyrograph = PyroGraph()
    pygame.init()
    screen = pygame.display.set_mode((START_WIDTH, START_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("PyroGraph")

    main_loop(screen, pyrograph)


def main_loop(
    screen: pygame.Surface,
    pyrograph: PyroGraph,
):
    t: int = 0
    running: bool = True
    clock: pygame.time.Clock = pygame.time.Clock()

    while running:
        screen.fill(BACKGROUND_COLOR)

        width, height = screen.get_size()
        draw_area: pygame.Rect = pygame.Rect(0, 0, width, height)
        pyrograph.draw(screen, t)

        running = handle_events(pyrograph, draw_area, screen)
        pygame.display.flip()
        t += 1
        clock.tick(FPS)

    pygame.quit()


def handle_events(pyrograph: PyroGraph, draw_area: pygame.Rect, screen: pygame.Surface):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # quit
                return False
            elif event.key == pygame.K_F2:
                # save json
                save_model_to_json(pyrograph.stators, "graphs/model.json")
            elif event.key == pygame.K_F4:
                # load json
                pyrograph.stators = load_model_from_json("graphs/model.json")
                pyrograph.unselect()
            elif event.key == pygame.K_d:
                # debug
                pprint(pyrograph, max_length=5)
            elif event.key == pygame.K_r:
                # add rotor
                if isinstance(pyrograph.selected(), Circle):
                    pyrograph.selected().children.append(
                        Rotor(parent=pyrograph.selected())
                    )
            elif event.key == pygame.K_s:
                # add stator
                pyrograph.stators.append(Stator())
            elif event.key == pygame.K_DELETE:
                # remove circle
                if isinstance(pyrograph.selected(), Circle):
                    pyrograph.remove(pyrograph.selected())
            elif event.key == pygame.K_F12:
                # save image
                pygame.image.save(screen, "images/screenshot.jpeg")

        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            if pyrograph.drag and draw_area.collidepoint(mx, my):
                if isinstance(pyrograph.selected(), Stator):
                    pyrograph.selected().x, pyrograph.selected().y = mx, my

        elif event.type == pygame.MOUSEBUTTONUP:
            pyrograph.drag = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # select circle if hit
            if pyrograph.select_at_position(event.pos):
                pyrograph.drag = True
            else:
                pyrograph.unselect()
    return True
