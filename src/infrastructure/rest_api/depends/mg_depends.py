from infrastructure.db.mongo_db_async.mongo_repo.quotes_data_repo import AsyncQuotesDataRepo
from infrastructure.db.mongo_db_async.mongo_connection import QuotesData


def get_async_quotes_data_repo() -> AsyncQuotesDataRepo:
    return AsyncQuotesDataRepo(collection=QuotesData)