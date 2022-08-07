from jerde import JsonModel

class DefaultModel(JsonModel):
    stuff: int = 100


def test_defaultnon_missing() -> None:
    value = DefaultModel({"stuff": 10})

    assert value.stuff == 10

def test_missing() -> None:
    value = DefaultModel({})

    assert value.stuff == 100


