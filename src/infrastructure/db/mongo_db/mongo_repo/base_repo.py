from typing import Any, Optional
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.results import InsertOneResult, DeleteResult, InsertManyResult

from src.infrastructure.db.irepo import AbstractRepo


class BaseMgRepo(AbstractRepo):
    def __init__(self, collection: AsyncCollection):
        self.collection: AsyncCollection = collection

    async def get(self, filter_fields_and_values: dict[str, Any]) -> Optional[dict[str, Any]]:
        result: Optional[dict[str, Any]] =  await self.collection.find_one(
            filter_fields_and_values
        )
        return result

    async def get_all(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = await self.collection.find(
            {}
        ).to_list(length=None)
        return result

    async def add(self, doc: dict[str, Any]) -> InsertOneResult:
        result: InsertOneResult = await self.collection.insert_one(doc)
        return result

    async def add_many(self, docs: list[dict[str, Any]]) -> InsertManyResult:
        result: InsertManyResult = await self.collection.insert_many(docs)
        return result

    async def delete(self, doc: dict[str, Any]) -> DeleteResult:
        result: DeleteResult = await self.collection.delete_one(doc)
        return result