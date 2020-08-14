# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime


class RtingsComSpider(scrapy.Spider):
    name = 'rtings_com'
    # allowed_domains = ['https://www.rtings.com/tv/reviews']
    start_urls = ['https://www.rtings.com/tv/reviews/',
                  'https://www.rtings.com/headphones/reviews',
                  'https://www.rtings.com/monitor/reviews',
                  'https://www.rtings.com/soundbar/reviews']

    def parse(self, response):
        urls_xpath = '//li[@class="silo_reviews_page-product"]/a[1]/@href'
        urls = response.xpath(urls_xpath).getall()

        for url in urls:
            full_url = response.urljoin(url)
            # print(full_url)
            yield response.follow(full_url, callback=self.parse_review)

    def parse_review(self, response):
        # print('Helllllllooo')
        pic_xpath = '//meta[@property="og:image"]/@content'
        pic = response.xpath(pic_xpath).get()
        title_xpath = '//meta[@property="og:title"]/@content'
        title = response.xpath(title_xpath).get()
        author_xpath = '//span[@itemprop="author"]/a/text()'
        author = response.xpath(author_xpath).get()
        pros_xpath = '//div[@data-id="1"]/ul/li/div/text()'
        pros = response.xpath(pros_xpath).get()
        cons_xpath = '//div[@data-id="-1"]/ul/li/div/text()'
        cons = response.xpath(cons_xpath).get()
        ocn_xpath = '//ol[@class="breadcrumbs-list"]/li[2]/a/span/text()'
        ocn = response.xpath(ocn_xpath).get()
        summary_xpath = '//meta[@property="og:description"]/@content'
        summary = response.xpath(summary_xpath).get()

        date_xpath = '//meta[@property="article:modified_time"]/@content'
        date = response.xpath(date_xpath).get()
        date = date.split('T')[0]
        date_format = '%Y-%m-%d'
        review_date = datetime.strptime(date, date_format)
        # date = review_date.isoformat().split('T')[0]

        # try:
        #     data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
        #     rating = data['review']['reviewRating']['ratingValue']
        #     scale = data['review']['reviewRating']['bestRating']
        #     pub_date = data['review']['datePublished'].split('T')[0]
        #     date_format = '%Y-%m-d'
        #     review_date = datetime.strptime(pub_date, date_format)
        #
        # except KeyError:
        #     rating = ''
        #     scale = ''

        verdict_xpath = '//div[@class="usage_card-summary-text"]/div/p/text()'

        verdict = response.xpath(verdict_xpath).get()
        url = response.url

        rating_xpath = '//div[@data-node="score_card"]/div[1]/span/text()'
        rating = response.xpath(rating_xpath).get()
        SCALE = 10

        sid = response.url.split("reviews/")[-1]

        productname = title
        if 'Review' in title:
            productname = title.replace(' Review', '')

        yield {'PIC': pic, 'Title': title, 'Author': author, 'Pros': pros, 'Cons': cons,
               'OCN': ocn, 'Summary': summary, 'Verdict': verdict, 'URL': url, 'Date': date,
               'Review_Date': review_date, 'Score': rating, 'Scale': SCALE, 'SID': sid,
               'Product_Name': productname}
