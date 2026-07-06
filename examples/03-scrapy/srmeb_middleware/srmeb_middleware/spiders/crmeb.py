import scrapy


class CrmebSpider(scrapy.Spider):
    name = "crmeb"
    allowed_domains = ["pro.crmeb.net"]
    start_urls = ["https://pro.crmeb.net/adminapi/home/header"]

    def parse(self, response):
        yield Scrapy.FormRequest(url="https://pro.crmeb.net/admin/login", callback=self.parse1, formdata={"username": "demo"}, method="put")
    def parse1(self, response):
        print(response.text)