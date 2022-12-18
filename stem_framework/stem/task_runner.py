import os
import asyncio
import threading
from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from meta import Meta, get_meta_attr
from task_tree import TaskNode


from collections import deque
from multiprocessing import Process

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

    activeThreadsTasks = deque()

    threadsContent = dict()

    def _task_in_thread(self, number, task_node, meta, **kwargs):
        self.threadsContent[number] = task_node.task.transform(task_node, meta, **kwargs)

    def _thread_running(self, task_node: TaskNode[T], meta: Meta, **kwargs):
        thread_number = len(self.activeThreadsTasks)
        thread = threading.Thread(target=task_node.task.transform, args=(task_node, meta, *kwargs))
        self.activeThreadsTasks.append(thread)
        self.threadsContent[thread_number] = None
        thread.start()
        thread.join()
        ret = self.threadsContent[thread_number]
        self.activeThreadsTasks.remove(thread)
        self.threadsContent.pop(thread_number)
        return ret

    def _start_thread_run(self, task_node: TaskNode[T], meta: Meta, **kwargs) -> T:
        result: T
        if len(self.activeThreadsTasks) < self.MAX_WORKERS:
            result = self._thread_running(task_node=task_node, meta=meta, **kwargs)
        else:
            while True:
                if len(self.activeThreadsTasks) < self.MAX_WORKERS:
                    result = self._thread_running(task_node=task_node, meta=meta, **kwargs)
                    break
                time.sleep(0.1)

        assert result is not None
        return result

    def run(self, meta: Meta, task_node: TaskNode[T]) -> T:
        kwargs = {t.task.name: self.run(get_meta_attr(meta, t.task.name, {}), t) for t in task_node.dependencies}

        result: T = None
        if len(task_node.dependencies) == 0:
            result = self._start_thread_run(task_node=task_node, meta=meta, **kwargs)
        assert result is not None
        return result


class AsyncRunner(TaskRunner[T]):
    loop = asyncio.get_event_loop()

    def run(self, meta: Meta, task_node: TaskNode[T]) -> T:
        result = self.loop.run_until_complete(self._make_tasks(meta, task_node))
        self.loop.close()
        return result

    async def _make_tasks(self, meta: Meta, task_node: TaskNode[T]) -> list[T]:
        await asyncio.sleep(0)
        kwargs = {t.task.name: self.loop.create_task(self._make_tasks(get_meta_attr(meta, t.task.name, {}), t)) for t in task_node.dependencies}

        for t in task_node.dependencies:
            await kwargs[t.task.name]

        result: T = None
        if len(task_node.dependencies) == 0:
            result = await self._async_transform(task_node, meta)
        assert result is not None
        return result

    async def _async_transform(self, task_node: TaskNode[T], meta: Meta, **kwargs) -> T:
        return task_node.task.transform(meta, **kwargs)


class ProcessingRunner(TaskRunner[T]):
    MAX_WORKERS = os.cpu_count()

    activeProcessTasks = deque()

    processContent = dict()

    def _task_in_process(self, number, task_node, meta, **kwargs):
        self.processContent[number] = task_node.task.transform(task_node, meta, **kwargs)

    def _process_running(self, task_node: TaskNode[T], meta: Meta, **kwargs):
        process_number = len(self.activeProcessTasks)
        process = Process(target=task_node.task.transform, args=(task_node, meta, *kwargs))
        self.activeProcessTasks.append(process)
        self.processContent[process_number] = None
        process.start()
        process.join()
        ret = self.processContent[process_number]
        self.activeProcessTasks.remove(process)
        self.processContent.pop(process_number)
        return ret

    def _start_process_run(self, task_node: TaskNode[T], meta: Meta, **kwargs) -> T:
        result: T
        if len(self.activeProcessTasks) < self.MAX_WORKERS:
            result = self._process_running(task_node=task_node, meta=meta, **kwargs)
        else:
            while True:
                if len(self.activeProcessTasks) < self.MAX_WORKERS:
                    result = self._process_running(task_node=task_node, meta=meta, **kwargs)
                    break
                time.sleep(0.1)

        assert result is not None
        return result

    def run(self, meta: Meta, task_node: TaskNode[T]) -> T:
        kwargs = {t.task.name: self.run(get_meta_attr(meta, t.task.name, {}), t) for t in task_node.dependencies}

        result: T = None
        if len(task_node.dependencies) == 0:
            result = self._start_process_run(task_node=task_node, meta=meta, **kwargs)
        assert result is not None
        return result