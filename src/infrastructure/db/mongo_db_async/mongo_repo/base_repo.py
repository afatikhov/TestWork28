from typing import Any, Optional
from pymongo.results import InsertOneResult, DeleteResult, InsertManyResult
from pymongo.collection import Collection

from logger import logger
from src.infrastructure.db.irepo import AbstractRepo


class BaseMgRepo(AbstractRepo):
    def __init__(self, collection: Collection):
        self.collection: Collection = collection

    def get(self, filter_fields_and_values: dict[str, Any]) -> Optional[dict[str, Any]]:
        try:
            result: Optional[dict[str, Any]] = self.collection.find_one(
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
            result: InsertOneResult = self.collection.insert_one(doc)
            logger.info(f"Added new data to mongo db: {result}")
            return result
        except Exception as e:
            logger.error("Error while adding data to mongo db", exc_info=True)

    def add_many(self, docs: list[dict[str, Any]]) -> InsertManyResult:
        try:
            result: InsertManyResult = self.collection.insert_many(docs)
            logger.info(f"Added new data to mongo db: {result}")
            return result
        except Exception as e:
            logger.error("Error while adding many data to mongo db", exc_info=True)

    def delete(self, doc: dict[str, Any]) -> DeleteResult:
        try:
            result: DeleteResult = self.collection.delete_one(doc)
            logger.info(f"Deleted data to mongo db: {result}")
            return result
        except Exception as e:
            logger.error("Error while deleting data to mongo db", exc_info=True)