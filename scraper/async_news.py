import httpx
import asyncio
from parsel import Selector


# pip install parsel
# pip install requests
# pip install lxml==4.9.4

class GrammarScraper:
    URL = "https://24may.newdeaf.co/film/"
    MAIN_URL = "https://24may.newdeaf.co/film/page/2/"
    HEADERS = {

        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    }

    LINK_XPATH = '//a[@class="card__img img-fit-cover"]/@href '
    # IMAGE_XPATH = '//div[@class="pill hoverable"]//img/@src'
    # TITLE_XPATH = '//a[@class="w8_bx"]/text()'

    async def fetch_page(self, client, page):
        url = self.URL.format(page=page)
        response = await client.get(url, timeout=20.0)
        print("page: ", page)
        # print(response.text)
        return Selector(response.text)

    async def scrape(self, selector):
        links = selector.xpath(self.LINK_XPATH).getall()
        print(links)

    async def get_pages(self, limit=40):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            get_page_tasks = [self.fetch_page(client, page) for page in range(1, limit + 1)]
            pages = await asyncio.gather(*get_page_tasks)
            scraping_tasks = [self.scrape(selector) for selector in pages if pages is not None]
            await asyncio.gather(*scraping_tasks)


if __name__ == "__main__":
    scraper = GrammarScraper()
    asyncio.run(scraper.get_pages())
