from fastapi import Depends

from src.infrastructure.db.mongo_db.mongo_repo.quotes_data_repo import QuotesDataRepo
from src.infrastructure.rest_api.depends.mg_depends import get_quotes_data_repo
from src.services.web_page_parcer import WebPageParser


def get_web_page_parser(quotes_data_repo: QuotesDataRepo=Depends(get_quotes_data_repo)) -> WebPageParser:
    return WebPageParser(quotes_data_repo=quotes_data_repo)