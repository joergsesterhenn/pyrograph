import logging
import random
import pygame
from pydantic import BaseModel, ConfigDict, Field, model_serializer
from rich.pretty import pprint
from pyrograph.model.circle import Circle
from pyrograph.model.model import (
    load_model_from_json,
)
from pyrograph.model.rotor import Rotor
from pyrograph.model.stator import Stator

FPS = 60
BACKGROUND_COLOR = pygame.Color("black")

logger = logging.getLogger(__name__)


class PyroGraph(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    stators: list[Stator] = [Stator()]
    drag: bool = False
    clock: pygame.time.Clock = Field(
        default_factory=lambda: pygame.time.Clock(), exclude=True
    )
    surface: pygame.Surface = Field(
        default_factory=lambda: pygame.Surface(), exclude=True
    )

    t: int = 0
    running: bool = True
    paused: bool = False

    @model_serializer
    def ser_model(self) -> list[Stator]:
        return self.stators

    def run(self):
        while self.running:
            self.running = self.handle_events()
            self.surface.fill(BACKGROUND_COLOR)
            self.draw()
            pygame.display.flip()
            if self.paused:
                continue
            self.t += 1
            self.clock.tick(FPS)

    def draw(self):
        for stator in self.stators:
            stator.draw(self.surface, self.t)
            for rotor in stator.children:
                rotor.draw_children(self.surface, self.t)

    def select_at_position(self, position: tuple[float, float]) -> Circle | None:
        for stator in self.stators:
            child_at_position = stator.get_child_encircling_position(position)
            if child_at_position is not None:
                self.select_circle(child_at_position)
                logger.debug(f"selected {child_at_position.id}")
                return child_at_position

    def select_circle(self, circle: Circle) -> Circle:
        self.unselect()
        for stator in self.stators:
            selected = stator.select_child(circle)
            if selected is not None:
                return selected

    def unselect(self):
        for stator in self.stators:
            stator.unselect()

    def selected(self) -> Circle | None:
        for stator in self.stators:
            selected = stator.get_selected_child()
            if selected is not None:
                return selected

    def remove(self, circle: Circle):
        if isinstance(circle, Stator):
            self.stators.remove(circle)
        else:
            for stator in self.stators:
                for child in stator.children:
                    child.remove_child(circle)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # quit
                    return False
                elif event.key == pygame.K_F2:
                    # save json
                    self.save("graphs/model.json")
                elif event.key == pygame.K_F4:
                    # load json
                    self.stators = load_model_from_json("graphs/model.json")
                    self.unselect()
                elif event.key == pygame.K_d:
                    # debug
                    pprint(self, max_length=5)
                elif event.key == pygame.K_r:
                    # add rotor
                    if isinstance(self.selected(), Circle):
                        self.selected().children.append(Rotor(parent=self.selected()))
                elif event.key == pygame.K_s:
                    # add stator
                    self.stators.append(Stator())
                elif event.key == pygame.K_DELETE:
                    # remove circle
                    if isinstance(self.selected(), Circle):
                        self.remove(self.selected())
                elif event.key == pygame.K_F12:
                    # save image
                    pygame.image.save(self.surface, "images/screenshot.jpeg")
                elif event.key == pygame.K_p:
                    # un/pause pyrograph
                    self.paused = not self.paused
                elif event.key == pygame.K_UP:
                    # select parent of current selection if available
                    selected = self.selected()
                    if isinstance(selected, Rotor):
                        self.select_circle(selected.parent)
                elif event.key == pygame.K_DOWN:
                    # select child of current selection if available
                    selected = self.selected()
                    if isinstance(selected, Circle) and len(selected.children) > 0:
                        self.select_circle(selected.children[0])
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    # select sibiling of current selection if available
                    selected = self.selected()
                    if isinstance(selected, Stator):
                        number_of_children = len(self.stators)
                        if number_of_children > 1:
                            selected_index = self.stators.index(selected)
                            if selected_index > 0 and event.key == pygame.K_LEFT:
                                self.select_circle(self.stators[selected_index - 1])
                            elif (
                                selected_index < number_of_children - 1
                                and event.key == pygame.K_RIGHT
                            ):
                                self.select_circle(self.stators[selected_index + 1])
                    elif isinstance(selected, Rotor):
                        number_of_children = len(selected.parent.children)
                        if number_of_children > 1:
                            selected_index = selected.parent.children.index(selected)
                            if selected_index > 0 and event.key == pygame.K_LEFT:
                                self.select_circle(
                                    selected.parent.children[selected_index - 1]
                                )
                            elif (
                                selected_index < number_of_children - 1
                                and event.key == pygame.K_RIGHT
                            ):
                                self.select_circle(
                                    selected.parent.children[selected_index + 1]
                                )
                elif event.key == pygame.K_TAB:
                    # switch between inner/outer mode
                    selected = self.selected()
                    if isinstance(selected, Rotor):
                        selected.inside = not selected.inside
                elif event.key == pygame.K_c:
                    # switch between inner/outer mode
                    selected = self.selected()
                    if isinstance(selected, Circle):
                        selected.color = f"#{random.randrange(0x1000000):06x}"
                elif event.key == pygame.K_PAGEUP:
                    # switch between inner/outer mode
                    selected = self.selected()
                    if isinstance(selected, Circle):
                        if selected.radius < 500:
                            selected.radius += 1
                elif event.key == pygame.K_PAGEDOWN:
                    # switch between inner/outer mode
                    selected = self.selected()
                    if isinstance(selected, Circle):
                        if selected.radius > 1:
                            selected.radius -= 1

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                if self.drag:
                    if isinstance(self.selected(), Stator):
                        self.selected().x, self.selected().y = mx, my

            elif event.type == pygame.MOUSEBUTTONUP:
                self.drag = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # select circle if hit
                if self.select_at_position(event.pos):
                    self.drag = True
                else:
                    self.unselect()
        return True

    def save(self, filename: str):
        with open(filename, "w") as file:
            file.write(self.model_dump_json(include=("stators",)))
