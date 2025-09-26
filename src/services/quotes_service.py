from typing import Optional

from infrastructure.db.mongo_db_async.mongo_repo.quotes_data_repo import AsyncQuotesDataRepo
from logger import logger


class QuotesService:
    def __init__(self, async_quotes_data_repo: AsyncQuotesDataRepo):
        self.async_quotes_data_repo: AsyncQuotesDataRepo = async_quotes_data_repo

    async def get_quotes_by_filer(self, author: str,
                                  tag: str) -> list[dict]:
        filters: dict = dict()
        if author:
            filters["author"] = author
        if tag:
            filters["tags"] = {"$in": [tag]}

        result: list[dict] = await self._get_quotes_by_filter(filters=filters)
        return result

    async def _get_quotes_by_filter(self, filters: dict) -> list[dict]:
        try:
            result: list[dict] = await self.async_quotes_data_repo.get(filters=filters)
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e
        return result