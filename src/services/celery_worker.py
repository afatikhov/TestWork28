from typing import Optional, Callable, Any
from celery import Celery
from config import settings
from infrastructure.db.mongo_db.mongo_connection import QuotesData
from infrastructure.db.mongo_db.mongo_repo.quotes_data_repo import QuotesDataRepo
from logger import logger
from services.web_page_parcer import WebPageParser


celery_worker = Celery(
                "test",
                broker=settings.get_url_redis,
                backend=settings.get_url_redis
            )

@celery_worker.task
def parse_and_store_task(page_url: str):
    logger.info(f"parse and store task start: {page_url}")
    quotes_data_repo = QuotesDataRepo(collection=QuotesData)
    parser = WebPageParser(quotes_data_repo=quotes_data_repo)
    parser.parce_and_store(page_url=page_url)