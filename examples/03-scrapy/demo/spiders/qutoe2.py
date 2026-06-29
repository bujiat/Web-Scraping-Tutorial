import scrapy
from demo.items import QuoteItem2

class Qutoe2Spider(scrapy.Spider):
    name = "qutoe2"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        nodeList = response.xpath('//div[@class="quote"]')
        for node in nodeList:
            item = QuoteItem2()
            item['content'] = node.xpath('./span[1]/text()').extract_first()
            item['name'] = node.xpath('./span[2]/small/text()').extract_first()
            item['link'] = node.xpath('./span[2]/a/@href').extract_first()
            yield item
        nextPage = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if nextPage:
            nextPage = response.urljoin(nextPage)
            # https://docs.scrapy.org/en/latest/topics/request-response.html
            yield scrapy.Request(url=nextPage, callback=self.parse)
        
