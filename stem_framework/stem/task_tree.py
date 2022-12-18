from typing import TypeVar, Optional, Generic

from task import Task
from workspace import IWorkspace

T = TypeVar("T")


class TaskNode(Generic[T]):
    #task: Task[T]
    def __init__(self, task: Task[T], workspace: Optional[IWorkspace] = None):
        self.task = task
        self.workspace = IWorkspace.find_default_workspace(task) if workspace is None else workspace

    @property
    def dependencies(self) -> list["TaskNode"]:
        resolved = []
        for dependency in self.task.dependencies:
            if self.workspace.has_task(dependency):
                resolved.append(TaskNode(self.workspace.find_task(dependency), self.workspace) )
        return resolved

    @property
    def is_leaf(self) -> bool:
        return self.dependencies == []

    @property
    def unresolved_dependencies(self) -> list["str"]:
        unresolved = []
        for dependency in self.task.dependencies:
            if not self.workspace.has_task(dependency):
                unresolved.append(dependency)
        return unresolved

    @property
    def has_dependence_errors(self) -> bool:
        if self.unresolved_dependencies:
            return True
        for dependency in self.dependencies:
            if dependency.has_dependence_errors:
                return True  
        return False

class TaskTree:
    def __init__(self, root: Task, workspace=None):
        self.root = TaskNode(root, workspace)

    def find_task(self, task, workspace=None) -> TaskNode[T]:
        _workspace = IWorkspace.find_default_workspace(task) if workspace is None else workspace

        if task == self.root.task and self.root.workspace == _workspace:
            return self.root
        else:
            for dependency in self.root.dependencies:
                tree = TaskTree(dependency.task, dependency.workspace)
                node = tree.find_task(task, workspace)
                if node is not None:
                    return node
        return None        
        
    def resolve_node(self, task: Task[T], workspace: Optional[IWorkspace] = None) -> TaskNode[T]:
        _workspace = IWorkspace.find_default_workspace(task) if workspace is None else workspace
        node = self.find_task(task, _workspace)
        if node is None:
            return TaskNode(task, workspace)
        else:
            return node