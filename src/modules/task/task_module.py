from injector import Binder, Module, singleton

from .services.task_service import TaskService


class TaskModule(Module):
    def configure(self, binder: Binder):
        binder.bind(TaskService, to=TaskService, scope=singleton)
