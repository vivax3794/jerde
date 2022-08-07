from jerde import JsonModel, JsonConverterModel


class Converter(JsonConverterModel[int]):
    def __init__(self, data: int) -> None:
        self.value = data + 10

    def to_json(self) -> int:
        return self.value - 10


class HasConverterModel(JsonModel):
    stuff: Converter

def test_deserialize() -> None:
    value = HasConverterModel({"stuff": 5})

    assert isinstance(value.stuff, Converter)
    assert value.stuff.value == 15 

def test_serialize() -> None:
    data = {"stuff": 5}

    assert HasConverterModel(data).to_json() == data