import scrapy
import json


class AboutSpider(scrapy.Spider):
    name = "about-spider"

    def start_requests(self):
        # Load the JSON file with data from home page spider
        input_file = "home_spider_output.json"
        with open(input_file, "r", encoding="utf-8") as fhand:
            data = json.load(fhand)

        for item in data:
            yield scrapy.Request(
                url=item["about_page"],
                callback=self.parse,
                cb_kwargs={"item": item["item"]},
            )

    def parse(self, response, item):
        selectors = {
            "birthdate": ".author-born-date::text",
            "birth_place": ".author-born-location::text",
            "description": ".author-description::text",
        }

        item.update(
            {
                key: response.css(value).get().replace("\n", " ").strip()
                for key, value in selectors.items()
            }
        )
        yield item
