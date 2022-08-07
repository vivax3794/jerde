import pytest

from jerde import JsonModel

class ModelA(JsonModel):
    key: int

class ModelB(JsonModel):
    key: str

class ParentModel(JsonModel):
    child: ModelA | ModelB


def test_model_a() -> None:
    value = ParentModel({"child": {"key": 1}})

    assert isinstance(value.child, ModelA)
    assert value.child.key == 1

def test_model_b() -> None:
    value = ParentModel({"child": {"key": "hello"}})

    assert isinstance(value.child, ModelB)
    assert value.child.key == "hello"
    
def test_invalid_type() -> None:
    with pytest.raises(TypeError):
        ParentModel({"child": {"key": []}})