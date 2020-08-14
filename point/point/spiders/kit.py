# -*- coding: utf-8 -*-
import scrapy


class KitSpider(scrapy.Spider):
    name = 'kit'
    # allowed_domains = ['http://www.kitguru.net/reviews/?category_name=mobile']
    start_urls = ['http://www.kitguru.net/reviews/?category_name=mobile']

    def parse(self, response):
        next_page_xpath = "//div/span[@id='tie-next-page']/a/@href"
        review_url_xpath = "//h2[@class='post-box-title']/a/@href"
        review_urls = self.extract_list(response.xpath(review_url_xpath))

        for review_url in review_urls:
            # review_url = get_full_url(response, review_url)
            request = Request(review_url, callback=self.parse_review)
            yield request

        next_page = self.extract(response.xpath(next_page_xpath))
        if next_page:
            next_page = get_full_url(response, next_page)
            request = Request(next_page, callback=self.parse)
            yield request
