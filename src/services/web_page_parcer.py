from typing import Optional

import aiohttp
import asyncio
from bs4 import BeautifulSoup
from pymongo.results import InsertManyResult

from src.infrastructure.db.mongo_db.mongo_connection import QuotesData
from src.infrastructure.db.mongo_db.mongo_repo.quotes_data_repo import QuotesDataRepo
from src.exceptions.custom_exceptions import NoDataInsertedException, PageLoadException


class WebPageParser:
    def __init__(self, quotes_data_repo: QuotesDataRepo):
        self.quotes_data_repo: QuotesDataRepo = quotes_data_repo

    async def parce_and_store(self, page_url: str) -> Optional[InsertManyResult]:
        try:
            page_html: str = await self.get_page_html(page_url)
            print(page_html)
            parsed_data: list[dict[str, object]] = self.parce_quotes(page_html)
            print(parsed_data)
            result: InsertManyResult = await self.write_parsed_data(parsed_data=parsed_data)
            return result
        except Exception as e:
            print(e)

    async def write_parsed_data(self, parsed_data: list[dict[str, object]]):
        result: InsertManyResult = await self.quotes_data_repo.add_many(parsed_data)

        if not result:
            raise NoDataInsertedException(message="No data was inserted!")

        return result

    async def get_page_html(self, page_url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(page_url) as response:
                page_html: str = await response.text()
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
    html_content: InsertManyResult = await parser.parce_and_store(page_url="https://quotes.toscrape.com")
    print(html_content)

if __name__ == "__main__":
    asyncio.run(main())