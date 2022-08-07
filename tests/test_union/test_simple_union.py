import pytest

from jerde import JsonModel


class SimpleUnionModel(JsonModel):
    foo: int | str


def test_deserialize_int() -> None:
    value = SimpleUnionModel({"foo": 1})

    assert value.foo == 1

def test_deserialize_str() -> None:
    value = SimpleUnionModel({"foo": "nice"})

    assert value.foo == "nice"

def test_wrong_type() -> None:
    with pytest.raises(TypeError):
        SimpleUnionModel({"foo": []})