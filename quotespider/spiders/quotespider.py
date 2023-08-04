import scrapy

BASE_URL = "http://quotes.toscrape.com/"


class QuoteSpider(scrapy.Spider):
    name = "quote-spider"
    start_urls = [BASE_URL]

    def parse_about(self, response, item):
        BIRTHDATE_SELECTOR = ".author-born-date::text"
        BIRTH_PLACE_SELECTOR = ".author-born-location::text"
        DESCRIPTION_SELECTOR = ".author-description::text"

        item["birthdate"] = response.css(BIRTHDATE_SELECTOR).get()
        item["birth_place"] = response.css(BIRTH_PLACE_SELECTOR).get()
        item["description"] = (
            response.css(DESCRIPTION_SELECTOR).get().replace("\n", " ").strip()
        )
        return item

    def parse(self, response):
        QUOTE_SELECTOR = ".quote"
        TEXT_SELECTOR = ".text::text"
        AUTHOR_SELECTOR = ".author::text"
        ABOUT_SELECTOR = ".author + a::attr(href)"
        TAGS_SELECTOR = ".tags > .tag::text"
        NEXT_SELECTOR = ".pager .next a::attr(href)"

        for quote in response.css(QUOTE_SELECTOR):
            item = {
                "text": quote.css(TEXT_SELECTOR).get(),
                "author": quote.css(AUTHOR_SELECTOR).get(),
                "tags": quote.css(TAGS_SELECTOR).getall(),
            }

            about_page = BASE_URL + quote.css(ABOUT_SELECTOR).get()
            yield scrapy.Request(
                about_page, callback=self.parse_about, cb_kwargs=dict(item=item)
            )

        next_page = response.css(NEXT_SELECTOR).get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page), callback=self.parse
            )
