from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field, field_validator
import pygame

SELECTION_COLOR = "red"


class Circle(BaseModel, ABC):
    type: str = Field(..., description="Type of Circle")
    id: UUID4 = Field(default_factory=lambda: uuid4(), exclude=True)
    x: float = Field(default=0, exclude=True)
    y: float = Field(default=0, exclude=True)
    radius: float = 50
    omega: float = 0.2
    color: str = "yellow"
    width: int = 1
    selected: bool = Field(default=False, exclude=True)
    children: list[Circle] = Field(default_factory=list)

    def get_position(self):
        return self.x, self.y

    def draw_selection(self, surface: pygame.Surface):
        if self.selected:
            pygame.draw.circle(
                surface,
                pygame.Color(SELECTION_COLOR),
                (int(self.x), int(self.y)),
                self.radius,
                5,
            )

    def encircles(self, position: tuple[float, float]):
        return (
            pygame.Vector2(self.get_position()).distance_to(pygame.Vector2(position))
            < self.radius
        )

    def get_selected_child(self) -> Circle | None:
        if self.selected:
            return self
        else:
            for child in self.children:
                selected = child.get_selected_child()
                if selected is not None:
                    return selected

    def select_child(self, circle: Circle) -> Circle | None:
        if self == circle:
            self.selected = True
            return self
        else:
            for child in self.children:
                selected = child.select_child(circle)
                if selected is not None:
                    return selected

    def get_child_encircling_position(
        self, position: tuple[float, float]
    ) -> Circle | None:
        if self.encircles(position):
            return self
        else:
            for child in self.children:
                selected = child.get_child_encircling_position(position)
                if selected is not None:
                    return selected

    def unselect(self):
        if self.selected:
            self.selected = False
        else:
            for child in self.children:
                child.unselect()

    def __eq__(self, value):
        return self.id == value.id

    def __hash__(self) -> int:
        return hash(self.id)

    @abstractmethod
    def draw(self, surface, t=0):
        pass

    @field_validator("children", mode="before")
    @classmethod
    def validate_children(cls, value):
        if isinstance(value, list):
            from pyrograph.model.model import circle_factory

            return [
                circle_factory(child) if isinstance(child, dict) else child
                for child in value
            ]
        return value
