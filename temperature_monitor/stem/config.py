from pathlib import Path
from typing import TypeVar, Type, Union
import os
import dataclasses
from yaml import load, Loader, dump, Dumper

T = TypeVar("T")


def from_dict(data: dict, factory: Type[T]) -> T:
    pass  # TODO(Assignment 14)


def resolve_config(factory: Type[T], user_path: Union[str,Path], default_path : Union[str,Path]) -> T:
    # TODO(Assignment 14)
    return factory() # Dummy fro 12-13