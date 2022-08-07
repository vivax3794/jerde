import pytest

from jerde import JsonModel


class ListModel(JsonModel):
    people: list[str]


def test_deserialize() -> None:
    value = ListModel({"people": ["hello", "world"]})

    assert value.people == ["hello", "world"]

def test_serialize() -> None:
    data = {"people": ["hello", "world"]}
    
    assert ListModel(data).to_json() == data

def test_wrong_type() -> None:
    with pytest.raises(TypeError):
        ListModel({"people": "hello"})

def test_wrong_subtype() -> None:
    with pytest.raises(TypeError):
        ListModel({"people": [1, 2, 3]})

def test_nested() -> None:
    class NestedModel(JsonModel):
        stuff: list[list[int]]
    
    value = NestedModel({"stuff": [[1, 2], [3, 4]]})

    assert value.stuff == [[1, 2], [3, 4]]