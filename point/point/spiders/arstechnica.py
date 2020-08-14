# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json


class ArstechnicaSpider(scrapy.Spider):
    name = 'arstechnica'
    # allowed_domains = ['https://arstechnica.com/reviews/']
    start_urls = ['https://arstechnica.com/reviews']

    def parse(self, response):
        wrapper = response.xpath('//header')

        for article in wrapper:
            urls = article.xpath('h2/a/@href').getall()
            dates = article.xpath('p/time/@datetime').getall()

            for date in dates:
                date = date.split('T')[0]

                if date:
                    for url in urls:
                        yield response.follow(url, callback=self.parse_review)

        next_page_xpath = '//div[@class="prev-next-links"]/a/@href'
        next_page = response.xpath(next_page_xpath).get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_review(self, response):
        # print('hello')
        title_xpath = '//meta[@property="og:title"]/@content'
        title = response.xpath(title_xpath).get()
        pic_xpath = '//meta[@property="og:image"]/@content'
        pic = response.xpath(pic_xpath).get()
        summary_xpath = '//meta[@property="og:description"]/@content'
        summary = response.xpath(summary_xpath).get()
        author_xpath = '//p[@itemprop="author creator"]/a/span/text()|//span[@class="author"]/text()'
        author = response.xpath(author_xpath).get()
        date_xpath = '//p[@class="byline"]/time/@datetime'
        date = response.xpath(date_xpath).get()
        date = date.split('T')[0]

        pros_xpath = "//*[contains(text(),'The good')]/following::ul[1]/li/text() |" \
                     "//*[contains(text(),'The Good')]/following::ul[1]/li/text()"
        cons_xpath = "//*[contains(text(),'The good')]/following::ul[2]/li/text() |" \
                     "//*[contains(text(),'The Good')]/following::ul[2]/li/text()"

        pros = response.xpath(pros_xpath).get()
        cons = response.xpath(cons_xpath).get()

        url = response.url

        # getting the ocn from the url
        start = url.find('com/') + len('.com')
        end = url.find('/2')

        ocn = url[start:end]

        data = json.loads(response.xpath("//meta[@name='parsely-metadata']/@content").get())
        sid = data['post_id']

        product_name = ''
        if 'review:' in title:
            product_name = title.split('review:')[0]
        else:
            product_name = title

        verdict_xpath = '//div[@itemprop="articleBody"]/p[last()]/text()'
        verdict = response.xpath(verdict_xpath).get()

        review = {'Title': title, 'PIC': pic, 'Summary': summary, 'Author': author, 'Date': date,
                  'Pros': pros, 'Cons': cons, 'URL': url, 'Source_internal_ID': sid, 'Product Name': product_name,
                  'Verdict': verdict, 'OCN': ocn}

        pros_cons_url_xpath = '//nav[@class="page-numbers"]/span/a[last()-1]/@href'
        pros_cons_url = response.xpath(pros_cons_url_xpath).get()

        if pros_cons_url:
            yield response.follow(pros_cons_url, callback=self.parse_pros_cons, meta={'review': review})
        else:
            yield review

    def parse_pros_cons(self, response):
        review = response.meta['review']
        pros_xpath = "//*[contains(text(),'The good')]/following::ul[1]/li/text() |" \
                     "//*[contains(text(),'The Good')]/following::ul[1]/li/text()"
        cons_xpath = "//*[contains(text(),'The good')]/following::ul[2]/li/text() |" \
                     "//*[contains(text(),'The Good')]/following::ul[2]/li/text()"

        pros = response.xpath(pros_xpath).get()
        cons = response.xpath(cons_xpath).get()

        review['Pros'] = pros
        review['Cons'] = cons

        verdict_xpath = '//div[@itemprop="articleBody"]/p[last()]/text()'
        verdict = response.xpath(verdict_xpath).get()

        review['Verdict'] = verdict

        yield review
