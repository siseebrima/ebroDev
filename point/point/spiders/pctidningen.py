# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request


class PctidningenSpider(scrapy.Spider):
    name = 'pctidningen'
    allowed_domains = ['test.pctidningen.se']
    start_urls = ['https://test.pctidningen.se/cms/wp-admin/admin-ajax.php'
                  '?action=product-search&price_from=0&price_to=0&orderby=' \
                  'review_date&order=desc&page=%d' % n for n in range(1, 92)]

    def parse(self, response):
        review_data = json.loads(response.text)
        data = review_data['data']['rows']
        urls = []
        for row in data:
            urls.append(row['url'])

        for url in urls:
            yield Request(url=url, callback=self.parse_p)

    def parse_p(self, response):
        title_xpath = '//h1[@class="h1"]//text()'
        title = response.xpath(title_xpath).get()

        date_xpath = '//time/@datetime'
        date = response.xpath(date_xpath).get()

        rating_xpath = '//span[@itemprop="ratingValue"]//text()'
        rating = response.xpath(rating_xpath).get()

        author_xpath = '//div[@class="meta-information"]/span//text()'
        author = response.xpath(author_xpath).get()

        summary_xpath = '//meta[@property="og:description"]/@content'
        summary = response.xpath(summary_xpath).get()

        ocn_xpath = '//span[@class="tags"]/a//text()'
        ocn = response.xpath(ocn_xpath).get()
        ocn = ocn[1:]

        pros_xpath = '//font[@color="green"]/following-sibling::text()[1] |' \
                     ' //span[@style="color: green;"]/following-sibling::text()[1]'
        pros = response.xpath(pros_xpath).get()

        cons_xpath = '//font[@color="red"]/following-sibling::text()[1] |' \
                     ' //span[@style="color: red;"]/following-sibling::text()[1]'
        cons = response.xpath(cons_xpath).get()

        verdict_xpath = '//div[@itemprop="description"]/p[last()-1]/text()'
        verdict = response.xpath(verdict_xpath).get()

        url = response.url

        yield {'Title': title,
               'Date': date,
               'Rating': rating,
               'Author': author,
               'Summary': summary,
               'OCN': ocn,
               'Pros': pros,
               'Cons': cons,
               'Verdict': verdict,
               'Url': url
               }