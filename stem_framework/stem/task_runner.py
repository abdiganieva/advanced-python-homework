import os
from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from meta import Meta, get_meta_attr
from task_tree import TaskNode

T = TypeVar("T")
class TaskRunner(ABC, Generic[T]):
    @abstractmethod
    def run(self, meta: Meta, task_node: TaskNode[T]) -> T:
        pass

class SimpleRunner(TaskRunner[T]):
    def run(self, meta: Meta, task_node: TaskNode[T]) -> T:
        assert not task_node.has_dependence_errors

        kwargs = {t.task.name: self.run(get_meta_attr(meta, t.task.name, {}), t) for t in task_node.dependencies}

        return task_node.task.transform(meta, **kwargs)


class ProcessingRunner(TaskRunner[T]):
    MAX_WORKERS = os.cpu_count()
