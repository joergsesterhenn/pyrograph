from typing import Optional, Union
import pygame
import typer
from pygame.color import Color

from pyrograph.model.circle import Circle
from pyrograph.model.model import (
    load_model_from_json,
    save_model_to_json,
)
from pyrograph.model.rotor import Rotor
from pyrograph.model.stator import Stator
from pyrograph.ui.ui import draw_button, draw_property_editor, draw_text, draw_tree


FPS = 60
START_WIDTH, START_HEIGHT = 1200, 800
SIDEBAR_WIDTH = 400
BACKGROUND_COLOR = Color("black")
SIDEBAR_BACKGROUND_COLOR = Color("grey")
input_boxes = []
toggle_rects = []
color_buttons = []
app = typer.Typer()


@app.command()
def pyrograph():
    stators: list[Stator] = [Stator()]
    selected: Optional[Union[Stator, Rotor]] = None
    pygame.init()
    screen = pygame.display.set_mode((START_WIDTH, START_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("PyroGraph")
    main_loop(screen, stators, selected)


def draw(surface, stators, t):
    for stator in stators:
        stator.draw(surface)
        for circle in stator.children:
            circle.draw(surface, t)


def main_loop(screen, stators, selected):
    t = 0
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BACKGROUND_COLOR)

        width, height = screen.get_size()
        draw_area = pygame.Rect(0, 0, width - SIDEBAR_WIDTH, height)
        draw(screen, stators, t)

        # Draw sidebar background
        sidebar = pygame.Rect(width - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, height)
        pygame.draw.rect(screen, SIDEBAR_BACKGROUND_COLOR, sidebar)
        draw_text(screen, "...::: Editor :::...", sidebar.x + 10, 10)
        y_offset = draw_tree(screen, stators, sidebar.x + 10, 40, selected)

        draw_text(screen, "Properties:", sidebar.x + 10, y_offset + 10)
        draw_property_editor(
            surface=screen,
            selected_obj=selected,
            x=sidebar.x + 10,
            y=y_offset + 40,
            toggle_rects=toggle_rects,
            color_buttons=color_buttons,
            input_boxes=input_boxes,
        )

        # Add buttons
        add_stator_btn = draw_button(
            screen, "+ Stator", sidebar.x + 10, height - 80, 100, 30
        )
        add_rotor_btn = draw_button(
            screen, "+ Rotor", sidebar.x + 120, height - 80, 100, 30
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_s:
                    save_model_to_json(stators, "model.json")
                elif event.key == pygame.K_l:
                    stators = load_model_from_json("model.json")
                    selected = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if draw_area.collidepoint(mx, my):
                    if isinstance(selected, Stator):
                        selected.x, selected.y = mx, my

                if add_stator_btn.collidepoint(mx, my):
                    stators.append(Stator())

                if add_rotor_btn.collidepoint(mx, my):
                    if isinstance(selected, Circle):
                        selected.children.append(Rotor(parent=selected))

                for stator in stators[:]:
                    if hasattr(stator, "_ui_rect") and stator._ui_rect.collidepoint(
                        mx, my
                    ):
                        selected = stator
                    if hasattr(
                        stator, "_delete_btn"
                    ) and stator._delete_btn.collidepoint(mx, my):
                        stators.remove(stator)
                        if selected == stator:
                            selected = None
                    for rotor in stator.children[:]:

                        def check_rotor_click(r, parent_list):
                            if hasattr(r, "_ui_rect") and r._ui_rect.collidepoint(
                                mx, my
                            ):
                                nonlocal selected
                                selected = r
                            if hasattr(r, "_delete_btn") and r._delete_btn.collidepoint(
                                mx, my
                            ):
                                parent_list.remove(r)
                                if selected == r:
                                    selected = None
                            for child in r.children[:]:
                                check_rotor_click(child, r.children)

                        check_rotor_click(rotor, stator.children)

                # for rect, field, min_val, max_val in input_boxes:
                #     if rect.collidepoint(mx, my) and selected:
                #         rel_x = mx - rect.x
                #         pct = rel_x / rect.width
                #         new_val = min_val + pct * (max_val - min_val)
                #         setattr(selected, field, int(new_val))

                for rect, field in toggle_rects:
                    if rect.collidepoint(mx, my) and selected:
                        current_val = getattr(selected, field)
                        setattr(selected, field, not current_val)

                for rect, field, color in color_buttons:
                    if rect.collidepoint(mx, my) and selected:
                        setattr(selected, field, color)
            for box in input_boxes:
                box.handle_event(event, selected)
        pygame.display.flip()
        t += 1
        clock.tick(FPS)

    pygame.quit()
