from fastapi import Depends

from infrastructure.db.mongo_db_async.mongo_repo.quotes_data_repo import AsyncQuotesDataRepo
from infrastructure.rest_api.depends.mg_depends import get_async_quotes_data_repo
from services.quotes_service import QuotesService



def get_quotes_service(async_quotes_data_repo: AsyncQuotesDataRepo=Depends(get_async_quotes_data_repo)):
    return QuotesService(async_quotes_data_repo=async_quotes_data_repo)