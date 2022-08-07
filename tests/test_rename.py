from typing import Annotated

from jerde import JsonModel, RenameField


class RenamedModel(JsonModel):
    stuff: Annotated[int, RenameField("foo")]


def test_deserialize() -> None:
    value = RenamedModel({"foo": 1})

    assert value.stuff == 1

def test_serialize() -> None:
    data = {"foo": 1}

    assert RenamedModel(data).to_json() == data