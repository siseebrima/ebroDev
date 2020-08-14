# -*- coding: utf-8 -*-
import scrapy
import re


class HdtvsandmoreComSpider(scrapy.Spider):
    name = 'hdtvsandmore_com'
    allowed_domains = ['hdtvsandmore.com']
    start_urls = ['https://hdtvsandmore.com/category/reviews']

    def parse(self, response):
        review_urls_xpath = '//h2[@class="post-title"]/a/@href'
        review_urls = response.xpath(review_urls_xpath).getall()

        for url in review_urls:
            yield response.follow(url, callback=self.parse_review)

        next_page_xpath = '//a[@class="next page-numbers"]/@href'
        next_page = response.xpath(next_page_xpath).get()

        if next_page:
            yield response.follow(next_page)

    def parse_review(self, response):
        date_xpath = '//span[@class="meta-date"]/a/time/@datetime'
        full_date = response.xpath(date_xpath).get()
        date = full_date.split('T')[0]

        author_xpath = '//a[@rel="author"]/text()'
        author = response.xpath(author_xpath).get()

        title_xpath = '//h2[@class="post-title"]/text()'
        title = response.xpath(title_xpath).get()

        # productname_xpath = '//ul[@class="review-list"]/li/span/text()'
        # productname = response.xpath(productname_xpath).get()

        product_name = ''
        revs = ['REVIEW', 'Review', 'review']
        for item in revs:
            if item in title:
                product_name = title.replace(item, '').strip()
            # else:
                # product_name = title

        pros_xpath = '//div[@class="review-pros wpr-col-1-2 pr-10"]/ul/li/text() | ' \
                     '//*[contains(text(),"Pros:")]/following::text()[1] | ' \
                     '//strong[contains(text(),"Pros")]/following::ul/li//text()'
        pros = response.xpath(pros_xpath).get()

        cons_xpath = '//div[@class="review-cons wpr-col-1-2 pl-10"]/ul/li/text() | ' \
                     '//*[contains(text(),"Cons:")]/following::text()[1] | ' \
                     '//strong[contains(text(),"Cons")]/following::ul/li//text()'
        cons = response.xpath(cons_xpath).get()

        summary_xpath = '//meta[@name="description"]/@content'
        summary = response.xpath(summary_xpath).get()

        verdict_xpath = '//div[@class="entry clearfix"]/p[last() -1]/text() | ' \
                        '//span[contains(text(),"Conclusion")]/following::p[1]//text()'
        verdict = response.xpath(verdict_xpath).get()

        yield {'Product Name': product_name,
               'Title': title,
               'Author': author,
               'Date': date,
               'Pros': pros,
               'Cons': cons,
               'Summary': summary,
               'Verdict': verdict}
