from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.cursor import AsyncCursor
from pymongo.results import InsertOneResult, DeleteResult, InsertManyResult
from pymongo.collection import Collection
from pymongo.synchronous.cursor import Cursor

from exceptions.custom_http_exceptions import QuoteDataNotFound
from logger import logger
from src.infrastructure.db.irepo import AbstractRepo


class AsyncBaseMgRepo(AbstractRepo):
    def __init__(self, collection: AsyncCollection):
        self.collection: AsyncCollection = collection

    async def get(self, filters: dict[str, Any]) -> Optional[list[dict[str, Any]]]:
        try:
            cursor: AsyncCursor = (self.collection.find(
                filters
            ))
            result: Optional[list[dict[str, Any]]] = await cursor.to_list(length=None)
            if not result:
                raise QuoteDataNotFound(message=f"No doc with filters: {filters} was found!")

            return self._convert_objectid(result)
        except Exception as e:
            logger.error("Error while getting data from mongo db", exc_info=True)
            raise e

    async def get_all(self) -> list[dict[str, Any]]:
        try:
            result: list[dict[str, Any]] = await self.collection.find(
                {}
            ).to_list(length=None)
            return result
        except Exception as e:
            logger.error("Error while getting all data from mongo db", exc_info=True)
            raise e

    def _convert_objectid(self, doc: list | dict) -> list | dict:
        if isinstance(doc, list):
            return [self._convert_objectid(d) for d in doc]
        if isinstance(doc, dict):
            return {k: self._convert_objectid(v) for k, v in doc.items()}
        if isinstance(doc, ObjectId):
            return str(doc)
        return doc

    async def add(self, doc: dict[str, Any]) -> InsertOneResult:
        try:
            doc_with_created_at: dict[str, Any] = self._add_created_add(doc)
            result: InsertOneResult = await self.collection.insert_one(doc_with_created_at)
            logger.info(f"Added new data to mongo db: {result}")
            return result
        except Exception as e:
            logger.error("Error while adding data to mongo db", exc_info=True)

    async def add_many(self, docs: list[dict[str, Any]]) -> InsertManyResult:
        try:
            docs_with_created_at: list[dict[str, Any]] = self._add_created_add(docs)
            result: InsertManyResult = await self.collection.insert_many(docs_with_created_at)
            logger.info(f"Added new data to mongo db: {result}")
            return result
        except Exception as e:
            logger.error("Error while adding many data to mongo db", exc_info=True)

    def _add_created_add(self, doc_or_docs: list | dict) -> list | dict:
        now: datetime = datetime.utcnow()
        if isinstance(doc_or_docs, dict):
            doc_or_docs["created_at"] = now
        if isinstance(doc_or_docs, list):
            for doc in doc_or_docs:
                doc["created_at"] = now
        return doc_or_docs

    async def delete(self, doc: dict[str, Any]) -> DeleteResult:
        try:
            result: DeleteResult = await self.collection.delete_one(doc)
            logger.info(f"Deleted data to mongo db: {result}")
            return result
        except Exception as e:
            logger.error("Error while deleting data to mongo db", exc_info=True)