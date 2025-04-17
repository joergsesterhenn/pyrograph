import pygame
import typer
from pyrograph.model.pyrograph import PyroGraph

START_WIDTH, START_HEIGHT = 1200, 800

app = typer.Typer()


@app.command()
def pyrograph():
    pygame.init()
    pygame.display.set_caption("PyroGraph")
    PyroGraph(
        surface=pygame.display.set_mode((START_WIDTH, START_HEIGHT), pygame.RESIZABLE),
    ).run()
    pygame.quit()
