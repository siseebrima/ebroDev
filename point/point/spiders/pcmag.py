# -*- coding: utf-8 -*-
import scrapy


class ReviewsSpider(scrapy.Spider):
    name = 'pcmag'
    start_urls = ['http://www.pcmag.com/reviews/']
    page_number = 2

    def parse(self, response):
        links = response.xpath("//h2[@class='text-base md:text-xl font-brand font-bold']/a/@href")
        for link in links:
            yield response.follow(link, callback=self.parge_page)

        next_page = 'https://www.pcmag.com/reviews?page=' + str(ReviewsSpider.page_number)
        if ReviewsSpider.page_number <= 616:
            yield response.follow(next_page, callback=self.parse)

    def parge_page(self, response):
        title_x = '//meta[@property="og:title"]/@content'
        title = response.xpath(title_x).extract_first()

        author_x = "//a[@data-element='author-name']/text()"
        author = response.xpath(author_x).extract_first()

        date_xpa = "//span[@class='font-semibold']/text()"
        date_ = response.xpath(date_xpa).extract_first().strip()
        date = date_.split('T')[0]

        pic_x = '//meta[@property="og:image"]/@content'
        image = response.xpath(pic_x).extract_first()

        price_ = "//div[contains(@class,'my-4 flex-1')]//div[@class='text-xs font-brand text-gray-base']/text()"
        price = response.xpath(price_).extract_first()

        score_ = "//span[@class='text-xl ml-2 inline-block font-bold font-brand']/text()"
        score = response.xpath(score_).extract_first()

        description_x = '//meta[@property="og:description"]/@content'
        description = response.xpath(description_x).extract_first()

        pros_ = "//div[@class='w-full md:w-1/2']//li/text()"
        pros = response.xpath(pros_).extract_first().strip()

        con_ = "//div[@class='w-full md:w-1/2 md:pl-4']//li/text()/text()"
        cons = response.xpath(con_).extract_first()

        conclusion_x = "//p[@class='leading-loose']/text()"
        conclusion = response.xpath(conclusion_x).extract_first()

        url = response.url

        yield {'Title': title, 'Author': author, 'Description': description, 'Date': date, 'Price': price,
               'Score': score, 'URL': url, 'Image': image,'Pros': pros, 'Cons': cons, 'conclusion': conclusion,}










