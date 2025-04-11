import pygame

from pyrograph.model.rotor import Rotor
from pyrograph.model.stator import Stator


# Colors
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GRAY = pygame.Color("gray")
BLUE = pygame.Color("dodgerblue")
LIGHT_GRAY = pygame.Color("lightgray")
COLOR_OPTIONS = ["red", "green", "blue", "yellow", "purple", "orange", "black"]


def draw_text(surface, text, x, y, color=BLACK):
    font = pygame.font.SysFont(None, 24)
    label = font.render(text, True, color)
    surface.blit(label, (x, y))


def draw_button(surface, text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, BLUE, rect)
    draw_text(surface, text, x + 5, y + 5, WHITE)
    return rect


def draw_slider(surface, label, val, min_val, max_val, x, y, w=200):
    draw_text(surface, f"{label}: {round(val, 2)}", x, y)
    bar_rect = pygame.Rect(x, y + 20, w, 10)
    pygame.draw.rect(surface, GRAY, bar_rect)
    pos = int((val - min_val) / (max_val - min_val) * w)
    knob_rect = pygame.Rect(x + pos - 5, y + 15, 10, 20)
    pygame.draw.rect(surface, BLUE, knob_rect)
    return bar_rect, min_val, max_val


def draw_toggle(surface, label, state, x, y):
    draw_text(surface, f"{label}:", x, y)
    rect = pygame.Rect(x + 100, y, 40, 20)
    pygame.draw.rect(surface, BLUE if state else GRAY, rect)
    return rect


def draw_color_picker(surface, label, current_color, x, y):
    draw_text(surface, f"{label}: {current_color}", x, y)
    buttons = []
    for i, c in enumerate(COLOR_OPTIONS):
        btn_rect = pygame.Rect(x + i * 30, y + 20, 20, 20)
        pygame.draw.rect(surface, pygame.Color(c), btn_rect)
        if c == current_color:
            pygame.draw.rect(surface, BLACK, btn_rect, 2)
        buttons.append((btn_rect, c))
    return buttons


def draw_tree(surface, stators: list[Stator], x: int, y: int, selected):
    dy = 30
    for stator_index, stator in enumerate(stators):
        rect = pygame.Rect(x, y, 200, 24)
        pygame.draw.rect(surface, BLUE if selected == stator else WHITE, rect)
        draw_text(surface, f"Stator {stator_index}", x + 5, y + 2)
        stator._ui_rect = rect

        delete_btn = pygame.Rect(x + 160, y + 2, 20, 20)
        pygame.draw.rect(surface, pygame.Color("red"), delete_btn)
        draw_text(surface, "X", x + 164, y + 2, WHITE)
        stator._delete_btn = delete_btn

        y += dy
        for rotor_index, rotor in enumerate(stator.children):
            y = draw_rotor_node(surface, rotor, x + 20, y, f"R{rotor_index}", selected)
    return y


def draw_rotor_node(surface, rotor: Rotor, x: int, y: int, label: str, selected):
    rect = pygame.Rect(x, y, 200, 24)
    pygame.draw.rect(surface, BLUE if selected == rotor else WHITE, rect)
    draw_text(surface, f"Rotor {label}", x + 5, y + 2)
    rotor._ui_rect = rect

    delete_btn = pygame.Rect(x + 160, y + 2, 20, 20)
    pygame.draw.rect(surface, pygame.Color("red"), delete_btn)
    draw_text(surface, "X", x + 164, y + 2, WHITE)
    rotor._delete_btn = delete_btn

    y += 30
    for i, child in enumerate(rotor.children):
        y = draw_rotor_node(surface, child, x + 20, y, f"{label}.{i}", selected)
    return y


def draw_property_editor(surface, selected_obj, x, y):
    global slider_rects, toggle_rects, color_buttons
    slider_rects = []
    toggle_rects = []
    color_buttons = []
    if not selected_obj:
        draw_text(surface, "No item selected", x, y)
        return
    draw_text(surface, f"Editing {type(selected_obj).__name__}", x, y)
    y += 30
    for field_name, value in selected_obj.dict().items():
        if isinstance(value, (int, float)):
            min_val = 0 if value == 0 else value * 0.1
            max_val = value * 10 if value != 0 else 100
            bar_rect, min_val, max_val = draw_slider(
                surface, field_name, value, min_val, max_val, x, y
            )
            slider_rects.append((bar_rect, field_name, min_val, max_val))
            y += 50
        elif isinstance(value, bool):
            toggle_rect = draw_toggle(surface, field_name, value, x, y)
            toggle_rects.append((toggle_rect, field_name))
            y += 30
        elif field_name == "color":
            buttons = draw_color_picker(surface, field_name, value, x, y)
            color_buttons.extend((btn, field_name, c) for btn, c in buttons)
            y += 50
