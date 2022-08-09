import pytest
from typing import Literal
from jerde import JsonModel


class LiteralModel(JsonModel):
    stuff: Literal[1]

def test_deserialize() -> None:
    value = LiteralModel({"stuff": 1})

    assert value.stuff == 1

def test_invalid_literal() -> None:
    with pytest.raises(ValueError):
        LiteralModel({"stuff": 2})
