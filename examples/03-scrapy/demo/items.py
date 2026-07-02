import scrapy

# 建模
class GiteeItem(scrapy.Item):
    title = scrapy.Field()
    name = scrapy.Field()


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    address = scrapy.Field()
    birthday = scrapy.Field()

class QuoteItem2(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()   

class DoubanItem(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    