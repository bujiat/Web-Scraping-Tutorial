import scrapy


class GiteecookiespiderSpider(scrapy.Spider):
    name = "giteeCookieSpider"
    allowed_domains = ["gitee.com"]
    start_urls = ["https://gitee.com/bujiatang_ft/valuelens"]
    def start_requests(self):
        # 控制台获取
        ck="YOUR_COOKIE"
        ck = {i.split("=")[0]:i.split("=")[1] for i in ck.spilt("; ")}
        yield scrapy.Request(self.start_urls[0], callback=self.parse, cookies=ck)

    def parse(self, response):
        with open("giteeCk.html", "wb") as f:
            f.write(response.body)
