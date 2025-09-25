from typing import Optional, Callable, Any

from celery import Celery


class CeleryWorker:
    def __init__(self, broker_url: str):
        self.broker_url: str = broker_url
        self.celery: Optional[Celery] = None

    def _ensure_celery(self):
        if self.celery is None:
            self.celery: Celery = Celery(
                "test",
                broker=self.broker_url
            )

    def task(self, func: Callable):
        self._ensure_celery()
        return self.celery.task(func)

    def send_task(self, task_name: str, args: list = None, kwargs: dict[str, Any] = None):
        args = args or []
        kwargs = kwargs or {}
        return self.celery.send_task(task_name, args=args, kwargs=kwargs)