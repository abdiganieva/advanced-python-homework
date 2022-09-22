"""
Metadata (user-defined tree of values) provides information about other data.
DataForge introduces the principle of metadata processor, id est during data processing only data and metadata are allowed to be used as input. No scripts or manual intermediate steps are allowed.
"""
from dataclasses import dataclass, is_dataclass
from typing import Optional, Any, Union, Type, Tuple
from stem.core import Dataclass

Meta = Union[dict, Dataclass]

SpecificationField = Tuple[object, Union[Type, Tuple[Type, ...]]]

Specification = Union[Type[Dataclass], Tuple[SpecificationField, ...]]


class SpecificationError(Exception):
    pass


@dataclass
class MetaFieldError:
    required_key: str
    required_types: Optional[tuple[type]] = None
    presented_type: Optional[type] = None
    presented_value: Any = None


class MetaVerification:

    def __init__(self, *errors: Union[MetaFieldError, "MetaVerification"]):
        self.error = errors

    @property
    def checked_success(self):
        if self.error == []:
            return True
        else:
            return False

    @staticmethod
    def verify(meta: Meta,
               specification: Optional[Specification] = None) -> "MetaVerification":

        if is_dataclass(specification):
            #if type dataclass
            spec_keys = specification.__dataclass_fields__.keys()
        else:
            #tuple (in order to work let's convert tuple to dict
            spec_dict = dict(specification)
            spec_keys = spec_dict.keys()

        if is_dataclass(meta):
            meta_keys = meta.__dataclass_fields__.keys()
        else:
            meta_keys = meta.keys()

        errs = []





def get_meta_attr(meta : Meta, key : str, default : Optional[Any] = None) -> Optional[Any]:
    #meta can be either Dataclass or dict
    #checking Dataclass, it should have dataclass fiels
    try:
        return getattr(meta, key)
    except AttributeError:
        return default
    except TypeError:
        pass

    try:
        return meta[key]
    except KeyError:
         return default


def update_meta(meta: Meta, **kwargs):
    #behaviour depends on whether meta is dataclass or dict
    if is_dataclass(meta) and not isinstance(meta, type):
        for key, value in kwargs.items():
            setattr(meta, key, value)
    else:
        for key, value in kwargs.items():
            meta[key] = value
