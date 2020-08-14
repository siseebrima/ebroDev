# -*- coding: utf-8 -*-
import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['thepoint.gm']
    start_urls = ['http://thepoint.gm/']

    def parse(self, response):
        urls = response.xpath('//h4/a/@href')

        for url in urls:
            yield response.follow(url, callback=self.parse_page)

    def parse_page(self, response):
        print('Hello Berekilibaaaaaaaa')
