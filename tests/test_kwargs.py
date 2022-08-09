from typing import Optional

from jerde import JsonModel

class KwargsModel(JsonModel):
    key_1: int
    key_2: Optional[int]

class NestedModel(JsonModel):
    value: KwargsModel

def test_all() -> None:
    value = KwargsModel(key_1 = 1, key_2 = 2)

    assert value.key_1 == 1
    assert value.key_2 == 2

def test_optional() -> None:
    value = KwargsModel(key_1 = 1)

    assert value.key_1 == 1
    assert value.key_2 is None

def test_nested() -> None:
    value = NestedModel(
        value = KwargsModel(key_1 = 10)
    )

    assert value.value.key_1 == 10
    assert value.value.key_2 is None