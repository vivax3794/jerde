import pytest

from jerde import JsonModel


class DictUnionModel(JsonModel):
    stuff: dict[str, dict[str, int | str]] | dict[str, str]

def test_deserialize_nested() -> None:
    value = DictUnionModel({"stuff": {"nice": {"what": 1, "hmm": "123"}}})

    assert value.stuff == {"nice": {"what": 1, "hmm": "123"}}

def test_deserialize_simple() -> None:
    value = DictUnionModel({"stuff": {"nice": "hmm"}})

    assert value.stuff == {"nice": "hmm"}

def test_invalid_nested_type() -> None:
    with pytest.raises(TypeError):
        DictUnionModel({"stuff": {"nice": {"hmm": 1}, "wrong": {"no": []}}})

def test_invalid_simple_type() -> None:
    with pytest.raises(TypeError):
        DictUnionModel({"stuff": {"nice": 1}})