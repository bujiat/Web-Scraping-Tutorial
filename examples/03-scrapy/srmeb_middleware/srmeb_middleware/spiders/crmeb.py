import scrapy


class CrmebSpider(scrapy.Spider):
    name = "crmeb"
    allowed_domains = ["pro.crmeb.net"]
    start_urls = ["https://pro.crmeb.net/adminapi/home/header"]

    def parse(self, response):
        pass
