import pytest

from jerde import JsonModel


class ListUnionModel(JsonModel):
    foo: list[int | list[int]] | list[str]


def test_deserialize_str() -> None:
    value = ListUnionModel({"foo": ["hello", "world"]})

    assert value.foo == ["hello", "world"]

def test_deserialize_list() -> None:
    value = ListUnionModel({"foo": [1, [4, 5], 3]})

    assert value.foo == [1, [4, 5], 3]

def test_wrong_base_type() -> None:
    with pytest.raises(TypeError):
        ListUnionModel({"foo": "wrong"})

def test_wrong_nested_type() -> None:
    with pytest.raises(TypeError):
        ListUnionModel({"foo": [1, 2, "abc"]})

def test_wrong_nested_nsted_type() -> None:
    with pytest.raises(TypeError):
        ListUnionModel({"foo": [1, 2, [4, "nice", 6]]})