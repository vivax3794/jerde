from jerde import JsonModel


class SuperModel(JsonModel):
    first: int

    def method(self) -> int:
        return 10

class ChildModel(SuperModel):
    second: int

def test_deserialize() -> None:
    value = ChildModel({"first": 1, "second": 2})

    assert value.first == 1
    assert value.second == 2

def test_serialize() -> None:
    data = {"first": 1, "second": 2}

    assert ChildModel(data).to_json() == data

def test_method() -> None:
    value = ChildModel({"first": 1, "second": 2})

    assert value.method() == 10