import json
from typing import Optional

from pyrograph.model.circle import Circle
from pyrograph.model.rotor import Rotor
from pyrograph.model.stator import Stator


def save_model_to_json(stators: list[Stator], filename: str):
    with open(filename, "w") as file:
        json.dump([stator.model_dump() for stator in stators], file, indent=2)


def load_model_from_json(filename: str) -> list[Stator]:
    with open(filename, "r") as file:
        data = json.load(file)
    stators = [circle_factory(s) for s in data]
    for stator in stators:
        assign_parents(stator, None)
    return stators


CIRCLE_TYPE_MAP = {
    "stator": Stator,
    "rotor": Rotor,
}


def circle_factory(data: dict) -> Circle:
    cls = CIRCLE_TYPE_MAP.get(data.get("type"))
    if cls is None:
        raise ValueError(f"Unknown circle type: {data.get('type')}")
    children_data = data.get("children", [])
    data["children"] = [circle_factory(child) for child in children_data]
    return cls(**data)


def assign_parents(circle: Circle, parent: Optional[Circle] = None):
    if isinstance(circle, Rotor):
        circle.parent = parent
    for child in circle.children:
        assign_parents(child, circle)
