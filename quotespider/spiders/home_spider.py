import scrapy

BASE_URL = "http://quotes.toscrape.com/"


class HomeSpider(scrapy.Spider):
    name = "home-spider"
    start_urls = [BASE_URL]

    def parse(self, response):
        selectors = {
            "quote": ".quote",
            "text": ".text::text",
            "author": ".author::text",
            "about": ".author + a::attr(href)",
            "tags": ".tags > .tag::text",
            "next_page": ".pager .next a::attr(href)",
        }

        for quote in response.css(selectors["quote"]):
            item = {
                "text": quote.css(selectors["text"]).get(),
                "author": quote.css(selectors["author"]).get(),
                "tags": quote.css(selectors["tags"]).getall(),
            }

            about_page = BASE_URL + quote.css(selectors["about"]).get()
            yield {
                "item": item,
                "about_page": about_page,
            }

        next_page = response.css(selectors["next_page"]).get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page), callback=self.parse
            )
