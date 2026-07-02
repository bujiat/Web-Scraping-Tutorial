import scrapy
from demo.items import DoubanItem

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        print(response.request.headers['user-agent'])
        nodeList = response.xpath("//ol[@class='grid_view']/li")
        for node in nodeList:
            item = DoubanItem()
            item["name"] = node.xpath("./div/div[2]/div/a/span[1]/text()").get()
            item["score"] = node.xpath("//span[@class='rating_num']/text()").get()
            yield item
        nextUrl = response.xpath("//span[@class='next']/a/@href").get()
        if nextUrl is not None:
            nextUrl = response.urljoin(nextUrl)
            yield scrapy.Request(nextUrl, callback=self.parse)