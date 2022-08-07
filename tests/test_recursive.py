from jerde import JsonModel

class FinalModel(JsonModel):
    last: int


RecursiveAlias = FinalModel | list["RecursiveAlias"]

class RecursiveTest(JsonModel):
    value: RecursiveAlias


def test_deserialize() -> None:
    value = RecursiveTest({"value": [{"last": 10}]})

    assert value.value[0].last == 10