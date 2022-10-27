"""
DataForge framework is modular. The core of processor consists of basic funcionality for working with data and metadata. Any specific functions are placed in separate plug-ins.
"""

from abc import abstractmethod, ABC, ABCMeta
from types import ModuleType
from typing import Optional, Any, TypeVar, Union, Type

from core import Named
from meta import Meta
from task import Task
from typing import List
T = TypeVar("T")


class TaskPath:
    def __init__(self, path: Union[str, List[str]]):
        if isinstance(path, str):
            self._path = path.split(".")
        else:
            self._path = path

    @property
    def is_leaf(self):
        return len(self._path) == 1

    @property
    def sub_path(self):
        return TaskPath(self._path[1:])

    @property
    def head(self):
        return self._path[0]

    @property
    def name(self):
        return self._path[-1]

    def __str__(self):
        return ".".join(self._path)


class ProxyTask(Task[T]):

    def __init__(self, proxy_name, task: Task):
        self._name = proxy_name
        self._task = task

    @property
    def dependencies(self):
        return self._task.dependencies

    @property
    def specification(self):
        return self._task.specification

    def check_by_meta(self, meta: Meta):
        self._task.check_by_meta(meta)

    def transform(self, meta: Meta, /, **kwargs: Any) -> T:
        return self._task.transform(meta, **kwargs)


class IWorkspace(ABC, Named):

    @property
    @abstractmethod
    def tasks(self) -> dict[str, Task]:
        pass

    @property
    @abstractmethod
    def workspaces(self) -> set["IWorkspace"]:
        pass

    @classmethod
    def find_task(self, task_path: Union[str, TaskPath]) -> Optional[Task]:
        if not isinstance(task_path, TaskPath):
            task_path = TaskPath(task_path)
        if not task_path.is_leaf:
            for w in cls.workspaces:
                if w.name == task_path.head:
                    return w.find_task(task_path.sub_path)
            return None
        else:
            for task_name in cls.tasks:
                if task_name == task_path.name:
                    return cls.tasks[task_name]
            for w in cls.workspaces:
                if (t := w.find_task(task_path)) is not None:
                    return t
            return None   

    def has_task(self, task_path: Union[str, TaskPath]) -> bool:
        return self.find_task(task_path) is not None

    def get_workspace(self, name) -> Optional["IWorkspace"]:
        for workspace in self.workspaces:
            if workspace.name == name:
                return workspace
        return None

    def structure(self) -> dict:
        return {
            "name": self.name,
            "tasks": list(self.tasks.keys()),
            "workspaces": [w.structure() for w in self.workspaces]
        }

    @staticmethod
    def find_default_workspace(task: Task) -> "IWorkspace":
        if hasattr(task, '_stem_workspace') and task._stem_workspace != NotImplemented:
            return task._stem_workspace
        else:
            module = import_module(task.__module__)
            return IWorkspace.module_workspace(module)

    @staticmethod
    def module_workspace(module: ModuleType) -> "IWorkspace":
        try:
            return module.__stem_workspace #check if attribute exists
        except AttributeError:
        
            tasks = {}
            workspaces = set()
            
            for attr in dir(module):
                a = getattr(module, attr)
                if isinstance(a, Taks): #if Task
                    tasks[attr] = a
                if isinstance(a, type) and issubclass(a, IWorkspace):
                    workspaces.add(a)
                    
            #creating workspace
            module.__stem_workspace = create_workspace(module.__name__, tasks, workspace)
            return module.__stem_workspace


class ILocalWorkspace(IWorkspace):

    @property
    def tasks(self) -> dict[str, Task]:
        return self._tasks

    @property
    def workspaces(self) -> set["IWorkspace"]:
        return self._workspaces


class LocalWorkspace(ILocalWorkspace):

    def __init__(self, name,  tasks=(), workspaces=()):
        self._name = name
        self._tasks = tasks
        self._workspaces = workspaces


class Workspace(ABCMeta, ILocalWorkspace):
    def __new__(mcls: type["Workspace"], name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kwargs: Any) -> Type[IWorkspace]:

        if IWorkspace not in bases:
            bases += (IWorkspace,)

        cls: Type[IWorkspace] = super().__new__(mcls, name, bases, namespace, **kwargs)  

        cls.name = name

        try:
            cls.workspaces = set(cls.workspaces)
        except TypeError:
            cls.workspaces = set()

        for s, t in cls.__dict__.items():
            if isinstance(t, Task):
                if not callable(t):
                    t = ProxyTask(s, t) 
                    setattr(cls, s, t)
                t._stem_workspace = cls  

        cls.tasks = {
            s: t
            for s, t in cls.__dict__.items()
            if isinstance(t, Task)
        }

        def __new(userclass, *args, **kwargs):
            return userclass

        cls.__new__ = __new  

        return cls
