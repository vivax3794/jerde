import pytest

from jerde import JsonModel

class EmptyModel(JsonModel):
    pass


def test_deserialize() -> None:
    assert isinstance(EmptyModel({}), EmptyModel)

def test_serialize() -> None:
    assert EmptyModel({}).to_json() == {}

def test_extra_keys() -> None:
    with pytest.raises(ValueError):
        EmptyModel({"extra": 123})
 
def test_wrong_type() -> None:
    with pytest.raises(TypeError):
        EmptyModel("should be a dict")