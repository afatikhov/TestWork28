import asyncio
from typing import Optional, Callable, Any

from celery import Celery
from pydantic import HttpUrl

from src.config import settings
from src.infrastructure.db.mongo_db.mongo_connection import QuotesData
from src.infrastructure.db.mongo_db.mongo_repo.quotes_data_repo import QuotesDataRepo


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

celery_worker = CeleryWorker(settings.get_url_redis)