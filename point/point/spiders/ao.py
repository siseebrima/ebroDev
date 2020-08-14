# -*- coding: utf-8 -*-
import scrapy


class AoSpider(scrapy.Spider):
    name = 'ao'
    # allowed_domains = ['https://ao.com/']
    start_urls = ['https://ao.com/']

    def parse(self, response):
        cat_url_xpaths = '//a[@data-lazy-target]/@href'
        cat_urls = response.xpath(cat_url_xpaths).getall()
        cat_urls = cat_urls[:-1]

        # print(len(cat_urls))

        for cat_url in cat_urls:
            yield response.follow(cat_url, callback=self.parse_category)

    def parse_category(self, response):
        print('hello')

