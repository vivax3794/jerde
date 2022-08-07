from typing import Optional

from jerde import JsonModel

class OptionalModel(JsonModel):
    stuff: Optional[int]


def test_not_missing() -> None:
    value = OptionalModel({"stuff": 10})

    assert value.stuff == 10

def test_missing() -> None:
    value = OptionalModel({})

    assert value.stuff is None