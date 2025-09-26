from src.infrastructure.db.mongo_db.mongo_connection import QuotesData
from src.infrastructure.db.mongo_db.mongo_repo.quotes_data_repo import QuotesDataRepo


def get_quotes_data_repo() -> QuotesDataRepo:
    return QuotesDataRepo(collection=QuotesData)