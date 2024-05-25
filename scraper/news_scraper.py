# import requests
# from parsel import Selector
#
#
# # pip install parsel
# # pip install requests
# # pip install lxml==4.9.4
#
# class GrammarScraper:
#     URL = "https://test-english.com/grammar-points/"
#     HEADERS = {
#
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#         "Accept - Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
#     }
#
#     LINK_XPATH = '//div[@class="pill hoverable"]/a/@href'
#     IMAGE_XPATH = '//div[@class="pill hoverable"]//img/@src'
#     TITLE_XPATH = '//a[@class="w8_bx"]/text()'
#
#     def scrape_data(self):
#         response = requests.get(self.URL, headers=self.HEADERS)
#         print(response.text)
#         tree = Selector(text=response.text)
#         imgs = tree.xpath(self.IMAGE_XPATH).getall()
#         titles = tree.xpath(self.TITLE_XPATH).getall()
#         links = tree.xpath(self.LINK_XPATH).getall()
#         return links[:5]
#
#         # for link in links:
#         #     print(link)
#
#
# if __name__ == "__main__":
#     scraper = NewsScraper()
#     scraper.scrape_data()
