# -*- coding: utf-8 -*-
import scrapy


class PctidningenSpider(scrapy.Spider):
    name = 'pctidningen'
    allowed_domains = ['https://test.pctidningen.se/cms/wp-admin/admin-ajax.php?action=product-search&price_from=0&price_to=0&orderby=review_date&order=desc&page=1']
    start_urls = ['http://https://test.pctidningen.se/cms/wp-admin/admin-ajax.php?action=product-search&price_from=0&price_to=0&orderby=review_date&order=desc&page=1/']

    def parse(self, response):
        pass
