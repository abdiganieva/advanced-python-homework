"""
Pull data flow model is implemented in DataForge by workplaces and tasks. The task execution consists of three steps, namely:
        1) Task model (the system calculates an acyclic dependency graph of tasks and data).
        2) Lazy computation model (a ’Goal’ object is created for each specific computation).
        3) Computation (when the top level goal is triggered, it invokes computation of all goals in chain behind it).
"""
from typing import TypeVar, Union, Tuple, Callable, Optional, Generic, Any, Iterator
from abc import ABC, abstractmethod
from core import Named
from meta import Specification, Meta

T = TypeVar("T")


class Task(ABC, Generic[T], Named):
    dependencies: Tuple[Union[str, "Task"], ...]
    specification: Optional[Specification] = None
    settings: Optional[Meta] = None

    def check_by_meta(self, meta: Meta):
        pass

    @abstractmethod
    def transform(self, meta: Meta, /, **kwargs: Any) -> T:
        pass


class FunctionTask(Task[T]):
    def __init__(self, name: str, func: Callable, dependencies: Tuple[Union[str, "Task"], ...],
                 specification: Optional[Specification] = None,
                 settings: Optional[Meta] = None):
        self._name = name
        self._func = func
        self.dependencies = dependencies
        self.specification = specification
        self.settings = settings

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def transform(self, meta: Meta, /, **kwargs: Any) -> T:
        return self._func(meta, **kwargs)


class DataTask(Task[T]):
    dependencies = ()

    @abstractmethod
    def data(self, meta: Meta) -> T:
        pass

    def transform(self, meta: Meta, /, **kwargs: Any) -> T:
        return self.data(meta)


class FunctionDataTask(DataTask[T]):
    def __init__(self, name: str, func: Callable,
                 specification: Optional[Specification] = None,
                 settings: Optional[Meta] = None):
        self._name = name
        self._func = func
        self.specification = specification
        self.settings = settings

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def data(self, meta: Meta) -> T:
        return self._func(meta)


def data(func: Callable[[Meta], T], specification: Optional[Specification] = None, **settings) -> FunctionDataTask[T]:

    
    def inner(name):
        return FunctionDataTask(name, func, specification, **settings)
        
    if func is None:
        inner
    else:
        return FunctionDataTask(func.__name__, func, specification, **settings)



def task(func: Callable[..., T], specification: Optional[Specification] = None, **settings) -> FunctionTask[T]:
    
    def inner(name, dependencies):
        return FunctionDataTask(name, func, dependencies, specification, **settings)
    
    nometa = tuple(arg for arg in func.__code__.co_varnames if arg != 'meta')
        
    if func is None:
        inner
    else:
        return FunctionTask(func.__name__, func, nometa, specification, **settings)
    


class MapTask(Task[Iterator[T]]):
    def __init__(self, func: Callable, dependence : Union[str, "Task"]):
        self.func = func
        
        if isinstance(dependence, str):
                self.dependence_name = dependence
        else:
                self.dependence_name = dependence.name
        
        self._name = 'map_' + self.dependence_name
    
    def transform(self, meta: Meta, /, **kwargs: Any) -> T:
        return map(self._func, *(kwargs.values())) 



class FilterTask(Task[Iterator[T]]):
    def __init__(self, key: Callable, dependence: Union[str, "Task"]):
        
        self.key = key
        
        if isinstance(dependence, str):
                self.dependence_name = dependence
        else:
                self.dependence_name = dependence.name
        
        self._name = 'filter_' + self.dependence_name
        
    def transform(self, meta: Meta, /, **kwargs: Any) -> T:
        return filter(self.key, kwargs[self.dependence_name])

class ReduceTask(Task[Iterator[T]]):
    def __init__(self, func: Callable, dependence: Union[str, "Task"]):
        
        self.func = func
        
        if isinstance(dependence, str):
                self.dependence_name = dependence
        else:
                self.dependence_name = dependence.name
        
        self._name = 'reduce_' + self.dependence_name
        
    
    def transform(self, meta: Meta, /, **kwargs: Any) -> T:
        return reduce(self.func, kwargs[self.dependence_name])
