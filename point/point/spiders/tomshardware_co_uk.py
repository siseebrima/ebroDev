# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json


class TomshardwareCoUkSpider(scrapy.Spider):
    name = 'tomshardware_co_uk'
    # allowed_domains = ['https://www.tomshardware.com/reviews']
    start_urls = ['https://www.tomshardware.com/uk/reviews']
    page_number = 2

    def parse(self, response):
        urls_xpath = '//div[@class="listingResults mixed"]/div/a/@href'
        urls = response.xpath(urls_xpath).getall()

        for url in urls:
            yield response.follow(url, callback=self.parse_review)

        # next_page_url = 'https://www.tomshardware.com/uk/reviews/page/2'
        # I want to scrape a max number of 30 pages so that the oldest date is in late 2018

        next_page = 'https://www.tomshardware.com/uk/reviews/page/' + str(self.page_number)
        if self.page_number <= 30:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)

        # next_page_xpath = '//div[@class="box pagination internal current-prev-next"]/span[2]/a/@href'
        # next_page = response.xpath(next_page_xpath).get()
        #
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_review(self, response):
        title_xpath = '//meta[@property="og:title"]/@content'
        pic_xpath = '//meta[@property="og:image"]/@content'
        summary_xpath = '//meta[@property="og:description"]/@content'

        pub_date_xpath = '//meta[@name="pub_date"]/@content'
        pub_date = response.xpath(pub_date_xpath).get()
        pub_date = pub_date.split('T')[0]
        date_format = '%Y-%m-%d'
        review_date = datetime.strptime(pub_date, date_format)

        title = response.xpath(title_xpath).get()
        pic = response.xpath(pic_xpath).get()
        summary = response.xpath(summary_xpath).get()

        product_name = ''
        if 'Review:' in title:
            product_name = title.split(' Review:')[0]

        else:
            product_name = title

        sid_xpath = '//article[@class="review-article"]/@data-id'
        sid = response.xpath(sid_xpath).get()

        ocn_xpath = '//meta[@name="parsely-section"]/@content'
        ocn = response.xpath(ocn_xpath).get()

        url = response.url

        author_xpath = '//meta[@name="parsely-author"]/@content'
        author = response.xpath(author_xpath).get()

        verdict_xpath = '//div[@class="sub-box full"]/p/text()'
        verdict = response.xpath(verdict_xpath).get()

        data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
        rating = data['review']['reviewRating']['ratingValue']
        scale = data['review']['reviewRating']['bestRating']

        pros_xpath = '//div[@class="box contrast less-space pro-con"]/div[1]/ul/li/text()'
        cons_xpath = '//div[@class="box contrast less-space pro-con"]/div[2]/ul/li/text()'

        pros = response.xpath(pros_xpath).get()
        pros = pros.strip()
        cons = response.xpath(cons_xpath).get()
        cons = pros.strip()

        if rating:
            try:

                yield {'Title': title, 'PIC': pic, 'Date': pub_date, 'Summary': summary, 'Date Format': review_date,
                       'Product_Name': product_name, 'Source_internal_id': sid, 'OCN': ocn, 'URL': url,
                       'Author': author, 'Rating': rating, 'Scale': scale, 'Verdict': verdict, 'Pros': pros,
                       'Cons': cons}

            except KeyError:
                pass
