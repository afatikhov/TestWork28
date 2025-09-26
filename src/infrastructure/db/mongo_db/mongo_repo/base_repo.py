from datetime import datetime
from typing import Any, Optional
from pymongo.results import InsertOneResult, DeleteResult, InsertManyResult
from pymongo.collection import Collection

from logger import logger
from src.infrastructure.db.irepo import AbstractRepo


class BaseMgRepo(AbstractRepo):
    def __init__(self, collection: Collection):
        self.collection: Collection = collection

    def get(self, filter_fields_and_values: dict[str, Any]) -> Optional[list[dict[str, Any]]]:
        try:
            result: Optional[list[dict[str, Any]]] = self.collection.find(
                filter_fields_and_values
            )
            return result
        except Exception as e:
            logger.error("Error while getting data from mongo db", exc_info=True)

    def get_all(self) -> list[dict[str, Any]]:
        try:
            result: list[dict[str, Any]] = self.collection.find(
                {}
            ).to_list(length=None)
            return result
        except Exception as e:
            logger.error("Error while getting all data from mongo db", exc_info=True)

    def add(self, doc: dict[str, Any]) -> InsertOneResult:
        try:
            doc_with_created_at: dict[str, Any] = self._add_created_add(doc)
            result: InsertOneResult = self.collection.insert_one(doc_with_created_at)
            logger.info(f"Added new data to mongo db: {result}")
            return result
        except Exception as e:
            logger.error("Error while adding data to mongo db", exc_info=True)

    def add_many(self, docs: list[dict[str, Any]]) -> InsertManyResult:
        try:
            docs_with_created_at: dict[str, Any] = self._add_created_add(docs)
            result: InsertManyResult = self.collection.insert_many(docs_with_created_at)
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

    def delete(self, doc: dict[str, Any]) -> DeleteResult:
        try:
            result: DeleteResult = self.collection.delete_one(doc)
            logger.info(f"Deleted data to mongo db: {result}")
            return result
        except Exception as e:
            logger.error("Error while deleting data to mongo db", exc_info=True)