# -*- coding: utf-8 -*-
import scrapy
import json


class NextpitSpider(scrapy.Spider):
    name = 'nextpit'
    allowed_domains = ['nextpit.de']
    start_urls = ['https://www.nextpit.de/tests/page/%d' % n for n in range(1, 82)]

    def parse(self, response):
        urls_xpath = '//h2/a/@href'
        urls = response.xpath(urls_xpath).getall()

        for url in urls:
            yield response.follow(url, callback=self.parse_page)

        # next_page_xpath = '//a[@class="arrow"]/@href'
        # next_page = response.xpath(next_page_xpath).get()
        #
        # if next_page:
        #     yield response.follow(next_page)

    def parse_page(self, response):
        # print('Hellllllllllllllo')
        url = response.url

        title_xpath = '//span[@class="article-title__text"]/text()'
        title = response.xpath(title_xpath).get()

        product_name = ''
        if ':' in title:
            product_name = title.split(':')[0]
        else:
            product_name = title

        author_xpath = '//span[@class="articleAuthorName"]/span/text()'
        author = response.xpath(author_xpath).get()

        date_xpath = 'substring-before(//time[@class="articlePublishedDate"]/@datetime, "T")'
        date = response.xpath(date_xpath).get()

        summary_xpath = '//meta[@property="og:description"]/@content'
        summary = response.xpath(summary_xpath).get()

        # json_ob_xpath = '//script[@type="application/ld+json"][2]/text()'
        # json_object = response.xpath(json_ob_xpath).get()
        #
        # data = json.loads(json_object)
        # rating = ''
        # if data:
        #     rating = data['reviewRating']['ratingValue']
        pros_xpath = '//ul[@class="goodList"]/li/span[@class="goodBadContent"]/text()'
        rx = response.xpath
        pros = rx(pros_xpath).get()

        cons_xpath = '//ul[@class="badList"]/li/span[@class="goodBadContent"]/text()'
        cons = rx(cons_xpath).get()

        verdict_xpath = '//div[@class="finalVerdictDesc"]/p[1]/text()'
        verdict = rx(verdict_xpath).get()

        pic_url_xpath = '//meta[@property="og:image"]/@content'
        pic_url = rx(pic_url_xpath).get()

        yield {'Title': title,
               'Product_Name': product_name,
               'URL': url,
               'Author': author,
               'Date': date,
               'Summary': summary,
               # 'Rating': rating,
               'Pros': pros,
               'Cons': cons,
               'Verdict': verdict,
               'Pic': pic_url

               }