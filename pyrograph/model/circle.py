from __future__ import annotations
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, field_validator


class Circle(BaseModel, ABC):
    type: str = Field(..., description="Type of Circle")
    x: float = Field(default=0, exclude=True)
    y: float = Field(default=0, exclude=True)
    radius: float = 50
    omega: float = 0.2
    color: str = "yellow"
    width: int = 1
    children: list[Circle] = Field(default_factory=list)

    @abstractmethod
    def draw(self, surface, t=0):
        pass

    @abstractmethod
    def get_position(self):
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
