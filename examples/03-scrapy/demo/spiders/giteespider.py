import scrapy

from demo.items import GiteeItem


class GiteespiderSpider(scrapy.Spider):
    name = "giteespider"
    allowed_domains = ["gitee.com"]
    start_urls = ["http://gitee.com/customers"]

    def parse(self, response):
        nodeList = response.xpath('//*[@id="caseList"]/div/div[2]/div[1]/div')
        for node in nodeList:
            item = GiteeItem()
            item["title"] = node.xpath(
                './/a/div[2]/div/span/text()'
            ).get(default="").strip()
            item["name"] = node.xpath(
                './/a/div[2]/div[3]/h3/text()'
            ).get(default="").strip()
            yield item
