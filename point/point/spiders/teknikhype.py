# -*- coding: utf-8 -*-
import scrapy


class TeknikhypeSpider(scrapy.Spider):
    name = 'teknikhype'
    allowed_domains = ['teknikhype.se']
    start_urls = ['https://www.teknikhype.se/kategori/hardvarustester/']

    def parse(self, response):
        urls_xpath = '//div[@class="td-pb-span8 td-main-content"]//h3/a/@href'
        urls = response.xpath(urls_xpath).getall()

        for url in urls:
            yield response.follow(url, callback=self.parse_review)

        next_page_xpath = '//a[@class="last"]/following::a[1]/@href'
        next_page = response.xpath(next_page_xpath).get()

        if next_page:
            yield response.follow(next_page)

    def parse_review(self, response):
        sid_xpath = 'substring-after(//link[@rel="shortlink"]/@href,"p=")'
        sid = response.xpath(sid_xpath).get()

        title_xpath = '//h1[@class="entry-title"]//text()'
        title = response.xpath(title_xpath).get()

        productname = ''
        if ':' in title:
            productname = title.split(': ')[1]
        else:
            productname = title

        verdict_xpath = '//div[@class="td-review-summary-content"]//text() | ' \
                        '//div[@class="td-post-content tagdiv-type"]/p[last()]//text()'
        verdict = response.xpath(verdict_xpath).get()

        rating_xpath = '//div[@class="td-review-final-score"]//text() | ' \
                       'substring-before(//span[@class="review-total-box"]//text(), "/")'
        rating = response.xpath(rating_xpath).get()

        url = response.url

        pic_xpath = '//meta[@property="og:image"]/@content'
        pic = response.xpath(pic_xpath).get()

        ocn_xpath = '//ul[@class="td-category"]/li[last()]//text()'
        ocn = response.xpath(ocn_xpath).get()

        date_xpath = '//header//time/@datetime'
        date = response.xpath(date_xpath).get()
        date = date.split('T')[0]

        summary_xpath = '//meta[@property="og:description"]/@content'
        summary = response.xpath(summary_xpath).get()

        author_xpath = '//div[@class="td-post-author-name"]/a//text()'
        author = response.xpath(author_xpath).get()

        yield {
            'Title': title,
            'Product Name': productname,
            'URL': url,
            'Source_int_ID': sid,
            'Verdict': verdict,
            'Score': rating,
            'Pic': pic,
            'Category': ocn,
            'Date': date,
            'Summary': summary,
            'Author': author,
        }
