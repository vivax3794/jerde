import pytest

from jerde import JsonModel

class SubModel(JsonModel):
    value: int

class MainModel(JsonModel):
    sub: SubModel


def test_deserialize() -> None:
    value = MainModel({"sub": {"value": 10}})

    assert isinstance(value.sub, SubModel)
    assert value.sub.value == 10

def test_serialize() -> None:
    data = {"sub": {"value": 10}}

    assert MainModel(data).to_json() == data

def test_wrong_type() -> None:
    with pytest.raises(TypeError):
        MainModel({"sub": 123})