# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import re


class CnetSpider(scrapy.Spider):
    name = 'cnet'
    # allowed_domains = ['https://www.cnetfrance.fr/produits/telephones-mobiles/']
    start_urls = ['https://www.cnetfrance.fr/produits/telephones-mobiles/']

    def parse(self, response):
        reviews = response.xpath('//div[@class="col-6 prodInfo"]')

        for review in reviews:
            revs = review.xpath('.//div[@class="reviewInfo"]//text()').getall()
            date = None
            for rev in revs:
                if re.search(r'\d', rev) and 'star' not in rev:

                    date = rev.strip().split(' à')[0].split(' ')[1]

            f = '%d/%m/%Y'

            date = datetime.strptime(date, f)
            url = review.xpath('.//a/@href').get()
            if date > last_stored_date:
                yield response.follow(url, callback=self.parse_page)



