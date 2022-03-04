import json

import scrapy


class QuotesSpider2(scrapy.Spider):
    name = "quote"

    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        # quotes = response.css('div.quote')
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('./span/small/text()').extract_first()
            }
            next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
            if next_page:
                yield response.follow(next_page, self.parse)

    def load_json(self, filename):
        quotes = json.load(open(filename))
        for quote in quotes:
            print(quote['text'], quote['author'])