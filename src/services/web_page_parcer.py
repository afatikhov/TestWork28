from typing import Optional
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from kombu.asynchronous.http import Response
from pydantic import HttpUrl
from pymongo.results import InsertManyResult
from infrastructure.db.mongo_db.mongo_connection import QuotesData
from infrastructure.db.mongo_db.mongo_repo.quotes_data_repo import QuotesDataRepo
from exceptions.custom_exceptions import NoDataInsertedException, PageLoadException
from logger import logger
import requests


class WebPageParser:
    def __init__(self, quotes_data_repo: QuotesDataRepo):
        self.quotes_data_repo: QuotesDataRepo = quotes_data_repo

    def parce_and_store(self, page_url: HttpUrl) -> Optional[InsertManyResult]:
        try:
            page_html: str = self.get_page_html(page_url)
            print(page_html)
            parsed_data: list[dict[str, object]] = self.parce_quotes(page_html)
            print(parsed_data)
            result: InsertManyResult = self.write_parsed_data(parsed_data=parsed_data)
            return result
        except Exception as e:
            logger.error(f"Error while parsing: {e}", exc_info=True)
            return None

    def write_parsed_data(self, parsed_data: list[dict[str, object]]):
        result: InsertManyResult = self.quotes_data_repo.add_many(parsed_data)

        if not result:
            raise NoDataInsertedException(message="No data was inserted!")

        return result

    def get_page_html(self, page_url: HttpUrl) -> str:

        response: Response = requests.get(page_url)
        if response.status_code != 200:
            raise PageLoadException(url=page_url)

        page_html: str = response.text
        if not page_html:
            raise PageLoadException(url=page_url)

        return page_html


    def parce_quotes(self, page_html: str) -> list[dict[str, object]]:
        soup: BeautifulSoup = BeautifulSoup(page_html, "html.parser")
        quotes_list: list[dict[str, object]] = list()

        for quote_data in soup.select(".quote"):
            text: str = quote_data.select_one(".text").get_text(strip=True)
            author: str = quote_data.select_one(".author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote_data.select(".tags .tag")]

            quotes_list.append({
                "text": text,
                "author": author,
                "tags": tags
            })
        if not quotes_list:
            raise NoDataInsertedException(message="No data to insert!")

        return quotes_list

async def main() -> None:
    quotes_data_repo: QuotesDataRepo = QuotesDataRepo(collection=QuotesData)
    parser = WebPageParser(quotes_data_repo=quotes_data_repo)
    html_content: InsertManyResult = parser.parce_and_store(page_url="https://quotes.toscrape.com")
    print(html_content)

if __name__ == "__main__":
    asyncio.run(main())