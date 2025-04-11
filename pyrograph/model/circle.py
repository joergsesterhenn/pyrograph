from __future__ import annotations
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field


class Circle(BaseModel, ABC):
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
