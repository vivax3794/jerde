import pytest

from jerde import JsonModel

class ModelA(JsonModel):
    key: int

class ParentModel(JsonModel):
    child: ModelA | dict[str, int]


def test_model_a() -> None:
    value = ParentModel({"child": {"key": 1}})

    assert isinstance(value.child, ModelA)
    assert value.child.key == 1

def test_dict() -> None:
    value = ParentModel({"child": {"nice": 1}})

    assert isinstance(value.child, dict)
    assert value.child == {"nice": 1}
    
def test_invalid_type() -> None:
    with pytest.raises(TypeError):
        ParentModel({"child": {"hmm": "what"}})