import typing
import types
import abc
from typing import Mapping, Sequence, TypeAlias, TypeVar

_JSON_DATA: TypeAlias = str | int | None | Sequence["_JSON_DATA"] | Mapping[str, "_JSON_DATA"]
T = TypeVar("T")


class RenameField:
    """
    Lets you rename the field a value has in the json structure.

    example:
    >>> from typing import Annotated
    >>> class RenameExmaple(JsonModel):
    ...     value: Annotated[int, RenameField("other")]
    >>> x = RenameExample({"other": 10})
    >>> x.value
    10
    >>> x.value = 20
    >>> x.to_json()
    {"other": 20}

    """
    def __init__(self, json_name: str) -> None:
        self.json_name = json_name

    def __repr__(self) -> str:
        return f"RenameField({self.json_name!r})"


def _get_fields(cls: type) -> list[tuple[str, str, type]]:
    fields: list[tuple[str, str, type]] = []

    for name, annotation in typing.get_type_hints(cls   , include_extras=True).items():
        json_key = name

        if typing.get_origin(annotation) == typing.Annotated:
            annotation, *args = typing.get_args(annotation)
            for arg in args:
                if isinstance(arg, RenameField):
                    json_key = arg.json_name

        fields.append((name, json_key, annotation))

    return fields


def _deserialize_union(name: str, value: object, expected_type: object) -> object:
    accepted_types: tuple[type, ...] = typing.get_args(expected_type)

    if isinstance(value, list):
        errors: list[str] = []
        for possible in accepted_types:
            if typing.get_origin(possible) == list:
                exp_type: type = typing.get_args(possible)[0]
                try:
                    return [_deserialize_value(f"{name}.{index}", elem, exp_type) for index, elem in enumerate(value)]  # type: ignore
                except TypeError as err:
                    errors.append(f"'{str(possible)}': {err}")
        
        if errors:
            error_padding = "\n".join(errors).replace("\n", "\n\t")
            raise TypeError(f"{name!r} did not match '{expected_type}'\n\t{error_padding}")
            
    elif isinstance(value, dict):
        errors: list[str] = []
        for possible in accepted_types:
            if typing.get_origin(possible) == dict:
                exp_type: type = typing.get_args(possible)[1]
                try:
                    return {key: _deserialize_value(f"{name}.{key}", item, exp_type) for key, item in value.items()}  # type: ignore
                except TypeError as err:
                    errors.append(f"'{str(possible)}': {err}")
            elif issubclass(possible, JsonModel):
                try:
                    return _deserialize_value(name, value, possible)
                except (TypeError, ValueError, KeyError) as err:
                    errors.append(f"'{possible}': {err}")
        
        if errors:
            error_padding = "\n".join(errors).replace("\n", "\n\t")
            raise TypeError(f"{name!r} did not match '{expected_type}'\n\t{error_padding}")

    if type(value) not in accepted_types:
        raise TypeError(f"Expected {name!r} to be one of '{expected_type}', but got {type(value)}")

    return value  # type: ignore

def _deserialize_value(name: str, value: _JSON_DATA, expected_type: type) -> object:
    if typing.get_origin(expected_type) == list:
        if not isinstance(value, list):
            raise TypeError(f"Expected {name!r} to be {expected_type}, but got: {type(value)}")

        list_members: type = typing.get_args(expected_type)[0]
        return [_deserialize_value(f"{name}.{index}", elem, list_members) for index, elem in enumerate(value)]  # type: ignore
    
    if typing.get_origin(expected_type) == dict:
        if not isinstance(value, dict):
            raise TypeError(f"Expected {name!r} to be {expected_type}, but got: {type(value)}")
        
        key_type, value_type = typing.get_args(expected_type)
        if key_type != str:
            raise TypeError(f"Dict key type must be str, got {key_type}, in type hint for {name!r}")
        
        return {key: _deserialize_value(f"{name}.{key}", item, value_type) for key, item in value.items()}

    if typing.get_origin(expected_type) in {typing.Union, types.UnionType}:
        return _deserialize_union(name, value, expected_type)

    if issubclass(expected_type, JsonModel):
        return expected_type(value)

    if issubclass(expected_type, JsonConverterModel):
        if not hasattr(expected_type, "__orig_bases__"):
            raise TypeError(f"Cannot perform inspection of type {expected_type}")
        bases: tuple[type, ...] = expected_type.__orig_bases__ # type: ignore
        json_type: None | type = None
        for base in bases:
            if issubclass(typing.get_origin(base) or int, JsonConverterModel):
                json_type = typing.get_args(base)[0]
        if json_type is None:
            raise TypeError("Unable to determine converter base type from provided bases: {bases}")
        
        return expected_type(_deserialize_value(name, value, json_type))  # type: ignore

    if not isinstance(value, expected_type):
        raise TypeError(f"Expected {name!r} to be '{expected_type}', but got: {type(value)}")
    
    return value 


def _serialize_value(value: object) -> _JSON_DATA:
    if isinstance(value, JsonModel):
        return {json_key: _serialize_value(getattr(value, name)) for name, json_key, _ in _get_fields(value.__class__)}
    elif isinstance(value, JsonConverterModel):
        return value.to_json()
    elif isinstance(value, list):      
        v: list[object] = value  
        return [_serialize_value(elem) for elem in v]
    elif isinstance(value, (int, str)):
        return value        
    else:
        raise TypeError(f"Can not serialize value of type {type(value)}")

class JsonModel:
    """
    This class is the main thing that does stuff.

    It lets you define the structure of your json and use it as a normal class as well.
    This class wil automatically parse json data in its __init__ and raise a TypeError if the structure does not match.

    >>> class SimpleExample(JsonModel):
    ...     stuff: int
    >>> SimpleExample({"stuff": 10}).stuff
    10
    >>> SimpleExample({"stuff": "wrong"})
    TypeError: ...

    It also supports unions (both `typing.Union` and 3.10 `|` syntax).
    >>> class UnionExample(JsonModel):
    ...     stuff: int | str
    >>> UnionExample({"stuff": "hi"}).stuff
    "hi"

    We also have support for Optional!
    >>> from typing import Optional
    >>> class OptionalExample(JsonModel):
    ...     stuff: Optional[int]
    >>> OptionalExample({"stuff": 10}).stuff
    10
    >>> OptionalExample({}).stuff
    None

    You can also have default values for fields, implicitly making them optional!
    >>> class DefaultExample(JsonModel):
    ...     stuff: int = 10
    >>> DefaultExample({}).stuff
    10
    """

    def __init__(self, data: _JSON_DATA):
        if not isinstance(data, dict):
            raise TypeError("Expected dict")
        
        # error check data
        fields = _get_fields(self.__class__)

        unused_keys = data.keys() - {json_key for _, json_key, _ in fields}
        if len(unused_keys) != 0:
            raise ValueError(f"Unexpected keys: {unused_keys}")

        for name, json_key, expected_type in fields:
            if hasattr(self.__class__, name) and json_key not in data:
                setattr(self, name, getattr(self.__class__, name))
                continue

            setattr(self, name, _deserialize_value(json_key, data.get(json_key), expected_type))

    
    def to_json(self) -> _JSON_DATA:
        """
        Convert from the model into the json.

        This does the reverse from `__init__`.

        >>> class SimpleExample(JsonModel):
        ...     stuff: int
        >>> x = SimpleExample({"stuff": 10})
        >>> x.stuff = 20
        >>> x.to_json()
        {"stuff": 20}
        """            
        return _serialize_value(self)


class JsonConverterModel(typing.Generic[T], abc.ABC):
    """
    Allows you to define custom converts for json values.
    Giving you more control of how you data is loaded!

    You need to specify the expected structure of the json, this can be any of the same typehints used in normal json fields.
    And the value will be converted into the expected value before being passed to init.
    This means you can use other models as a value, even other converter models!

    >>>  # we expect the json to just be a int
    >>> class Converter(JsonConverterModel[int]): 
    ...     def __init__(self, data: int) -> None:
    ...         self.value = data + 10  # lets do some custom logic
    ...     def to_json(self) -> int:
    ...         return self.value - 10
    >>> class ConverterExample(JsonModel):
    ...     stuff: Converter
    >>> x = ConverterExample({"stuff": 10})
    >>> x.stuff.value
    20
    >>> x.to_json()
    {"stuff": 10}
    
    **Note:** it is good practice (but not enforced) to make sure that:
    >>> Converter(something).to_json() == something
    True
    """

    @abc.abstractmethod
    def __init__(self, data: T) -> None: ...
    @abc.abstractmethod
    def to_json(self) -> T: ...