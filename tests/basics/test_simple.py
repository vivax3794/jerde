import pytest

from jerde import JsonModel

class SimpleModel(JsonModel):
    name: str
    age: int

def test_deserialize() -> None:
    value = SimpleModel({"name": "vivax", "age": 1000})

    assert value.name == "vivax"
    assert value.age == 1000

def test_serialize() -> None:
    data = {"name": "vivax", "age": 1000}
    assert SimpleModel(data).to_json() == data

def test_missing_keys() -> None:
    with pytest.raises(TypeError):
        SimpleModel({"name": "vivax"})

def test_wrong_types() -> None:
    with pytest.raises(TypeError):
        SimpleModel({"name": 123, "age": "hello"})