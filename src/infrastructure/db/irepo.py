import abc
from abc import abstractmethod
from typing import Any


class AbstractRepo(abc.ABC):

    @abstractmethod
    async def get(self, filter_fields_and_values: dict[str, Any]):
        raise NotImplementedError

    @abstractmethod
    async def add(self, doc: dict[str, Any]):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, doc: dict[str, Any]):
        raise NotImplementedError