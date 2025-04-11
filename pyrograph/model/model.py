import json

from pyrograph.model.stator import Stator


def save_model_to_json(stators: list[Stator], filename: str):
    with open(filename, "w") as f:
        json.dump([s.dict() for s in stators], f, indent=2)


def load_model_from_json(filename: str) -> list[Stator]:
    with open(filename, "r") as f:
        data = json.load(f)
    return [Stator(**s) for s in data]
