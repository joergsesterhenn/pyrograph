from pydantic import BaseModel

from pyrograph.model.circle import Circle
from pyrograph.model.stator import Stator


class PyroGraph(BaseModel):
    stators: list[Stator] = [Stator()]
    drag: bool = False

    def draw(self, surface, t):
        for stator in self.stators:
            stator.draw(surface)
            for rotor in stator.children:
                rotor.draw(surface, t)

    def select_at_position(self, position: tuple[float, float]) -> Circle | None:
        for stator in self.stators:
            if stator.encircles(position):
                self.unselect()
                stator.selected = True
                return stator
            for rotor in stator.children:
                if rotor.encircles(position):
                    self.unselect()
                    rotor.selected = True
                    return rotor

    def select_circle(self, circle: Circle) -> Circle:
        self.unselect()
        for stator in self.stators:
            if stator == circle:
                stator.selected = True
                return stator
            for rotor in stator.children:
                if rotor == circle:
                    rotor.selected = True
                    return rotor

    def unselect(self):
        for stator in self.stators:
            stator.selected = False
            for rotor in stator.children:
                rotor.selected = False

    def selected(self) -> Circle:
        for stator in self.stators:
            if stator.selected:
                return stator
            for rotor in stator.children:
                if rotor.selected:
                    return rotor

    def remove(self, circle: Circle):
        if isinstance(circle, Stator):
            self.stators.remove(circle)
        else:
            for stator in self.stators:
                if circle in stator.children:
                    stator.children.remove(circle)
