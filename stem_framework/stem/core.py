from typing import Protocol, Any, Optional
from re import sub

def pascal_case_to_snake_case(name: str) -> str:
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
        sub('([A-Z]+)', r' \1',
        s.replace('-', ' '))).split()).lower()

class Dataclass(Protocol):
    __dataclass_fields__: Any


class Named():
    _name: Optional[str] = None

    @property
    def name():
        if (self._name is not None):
            return self._name
        else:
            return pascal_case_to_snake_case(self.__class__.__name__)
