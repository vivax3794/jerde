import pytest

from jerde import JsonModel

class ModelA(JsonModel):
    key_a: int

class ModelB(JsonModel):
    key_b: int

class ParentModel(JsonModel):
    child: ModelA | ModelB


def test_model_a() -> None:
    value = ParentModel({"child": {"key_a": 1}})

    assert isinstance(value.child, ModelA)
    assert value.child.key_a == 1

def test_model_b() -> None:
    value = ParentModel({"child": {"key_b": 2}})

    assert isinstance(value.child, ModelB)
    assert value.child.key_b == 2
    
def test_invalid_type() -> None:
    with pytest.raises(TypeError):
        ParentModel({"child": {"key_a": []}})