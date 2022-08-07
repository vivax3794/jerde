import pytest

from jerde import JsonModel


class DictModel(JsonModel):
    stuff: dict[str, int]


def test_deserialize() -> None:
    value = DictModel({"stuff": {"hello": 1, "world": 2}})

    assert value.stuff == {"hello": 1, "world": 2}

def test_invalid_type() -> None:
    with pytest.raises(TypeError):
        DictModel({"stuff": "nice"})

def test_invalid_item_type() -> None:
    with pytest.raises(TypeError):
        DictModel({"stuff": {"nice": "cat"}})

def test_invalid_typehint() -> None:
    with pytest.raises(TypeError):
        class InvalidModel(JsonModel):
            stuff: dict[int, int]

        InvalidModel({"stuff": {1: 2}})  # type: ignore
