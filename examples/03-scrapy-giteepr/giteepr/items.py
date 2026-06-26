import scrapy


class GiteeprItem(scrapy.Item):
    title = scrapy.Field()
    name = scrapy.Field()
