# -*- coding: utf-8 -*-
import scrapy


class MacworldSpider(scrapy.Spider):
    name = 'macworld'
    allowed_domains = ['www.macworld.com']
    start_urls = ['https://www.macworld.com/reviews/']

    def parse(self, response):
        load_more_xpath = "//a[@id='more-stories-btn']/@href"
        review_url_xpath = '//div[@id="crawlLatestResults"]/div/a/@href'
        review_urls = response.xpath(review_url_xpath).getall()

        for review in review_urls:
            yield response.follow(review, callback=self.parse_review)

        load_more = response.xpath(load_more_xpath).get()
        if review_urls:
            yield response.follow(load_more, callback=self.parse())

    def parse_review(self, response):
        print('Hellllllllllllloooooooo')
