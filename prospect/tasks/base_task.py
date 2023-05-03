from abc import ABC, abstractmethod
from datetime import date
from typing import Any

class BaseTask(ABC):
    idx_count = -1
    priority: float
    required_task_ids: list[int]
    data: Any # Result from self.run() method is stored here

    time_launch: date = None
    time_emit: date = None
    time_finish: date = None
    emitted_by: int = None

    def __init__(self, required_task_ids=[]):
        self.id = BaseTask.idx_count
        if self.id < 0:
            raise ValueError('Tried initializing a task with negative id, probably because emit_tasks was called by a worker process.')
        for req in required_task_ids:
            if req >= self.id:
                raise ValueError(f'Cannot require non-existent task of ID {req}.')
            elif req < 0:
                raise ValueError('Required task ID is negative.')
        self.required_task_ids = required_task_ids
        BaseTask.idx_count += 1

    @abstractmethod
    def run(self) -> None:
        pass

    def emit_tasks(self):
        # Any required information must be stored in self.data during call to run()
        return []

    def run_return_self(self, *args):
        self.run(*args)
        return self

    def __lt__(self, other):
        # Largest numerical value of priority is greatest
        return self.priority > other.priority

    @property
    def type(self) -> str:
        return self.__class__.__name__