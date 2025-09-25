import aiohttp
import asyncio
from bs4 import BeautifulSoup


class WebPageParser:
    def __init__(self):
        pass

    async def parce_and_store(self, page_url: str) -> None:
        page_html: str = await self.get_page_html(page_url)
        print(page_html)
        parsed_data: list[dict[str, object]] = self.parce_quotes(page_html)
        print(parsed_data)

    async def get_page_html(self, page_url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(page_url) as response:
                page_html: str = await response.text()
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

        return quotes_list

async def main() -> None:
    parser = WebPageParser()
    html_content: str = await parser.parce_and_store(page_url="https://quotes.toscrape.com")
    print(html_content)

if __name__ == "__main__":
    asyncio.run(main())