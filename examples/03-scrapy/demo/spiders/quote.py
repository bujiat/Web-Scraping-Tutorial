import scrapy

from demo.items import QuoteItem


class QuoteSpider(scrapy.Spider):
    name = "quote"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        nodeList = response.xpath('//div[@class="quote"]')
        for node in nodeList:
            item = QuoteItem()
            item['content'] = node.xpath('./span[1]/text()').extract_first()
            item['name'] = node.xpath('./span[2]/small/text()').extract_first()
            item['link'] = node.xpath('./span[2]/a/@href').extract_first()
            authorUrl = response.urljoin(item['link'])
            yield scrapy.Request(url=authorUrl, callback=self.parse_author, meta={'item': item},dont_filter=True)
        nextPage = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if nextPage:
            nextPage = response.urljoin(nextPage)
            # https://docs.scrapy.org/en/latest/topics/request-response.html
            yield scrapy.Request(url=nextPage, callback=self.parse)
        
    def parse_author(self, response):
        item = response.meta['item']
        item['address'] = response.xpath('//p[1]/span[1]/text()').extract_first()
        item['birthday'] = response.xpath('//p[1]//span[2]/text()').extract_first()
        yield item