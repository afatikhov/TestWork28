from typing import Any, Optional
from pymongo.results import InsertOneResult, DeleteResult, InsertManyResult
from pymongo.collection import Collection
from src.infrastructure.db.irepo import AbstractRepo


class BaseMgRepo(AbstractRepo):
    def __init__(self, collection: Collection):
        self.collection: Collection = collection

    def get(self, filter_fields_and_values: dict[str, Any]) -> Optional[dict[str, Any]]:
        result: Optional[dict[str, Any]] = self.collection.find_one(
            filter_fields_and_values
        )
        return result

    def get_all(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = self.collection.find(
            {}
        ).to_list(length=None)
        return result

    def add(self, doc: dict[str, Any]) -> InsertOneResult:
        result: InsertOneResult = self.collection.insert_one(doc)
        return result

    def add_many(self, docs: list[dict[str, Any]]) -> InsertManyResult:
        result: InsertManyResult = self.collection.insert_many(docs)
        return result

    def delete(self, doc: dict[str, Any]) -> DeleteResult:
        result: DeleteResult = self.collection.delete_one(doc)
        return result