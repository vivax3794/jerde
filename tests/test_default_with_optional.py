from typing import Optional
from jerde import JsonModel

class OptionalDefaultModel(JsonModel):
    stuff: Optional[int] = 100

def test_supplied() -> None:
    value = OptionalDefaultModel({"stuff": 10})

    assert value.stuff == 10

def test_none() -> None:
    value = OptionalDefaultModel({"stuff": None})

    assert value.stuff is None

def test_missing() -> None:
    value = OptionalDefaultModel({})

    assert value.stuff == 100