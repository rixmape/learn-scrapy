import scrapy

BASE_URL = "http://quotes.toscrape.com/"


class QuoteSpider(scrapy.Spider):
    name = "quote-spider"
    start_urls = [BASE_URL]

    def parse(self, response):
        QUOTE_SELECTOR = ".quote"
        TEXT_SELECTOR = ".text::text"
        AUTHOR_SELECTOR = ".author::text"
        ABOUT_SELECTOR = ".author + a::attr(href)"
        TAGS_SELECTOR = ".tags > .tag::text"
        NEXT_SELECTOR = ".pager .next a::attr(href)"

        for quote in response.css(QUOTE_SELECTOR):
            yield {
                "text": quote.css(TEXT_SELECTOR).get(),
                "author": quote.css(AUTHOR_SELECTOR).get(),
                "about": BASE_URL + quote.css(ABOUT_SELECTOR).get(),
                "tags": quote.css(TAGS_SELECTOR).getall(),
            }

        next_page = response.css(NEXT_SELECTOR).get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page), callback=self.parse
            )
