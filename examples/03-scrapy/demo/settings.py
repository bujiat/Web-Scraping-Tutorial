BOT_NAME = "demo"

SPIDER_MODULES = ["demo.spiders"]
NEWSPIDER_MODULE = "demo.spiders"


USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0"
]
# ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "demo.pipelines.JsonWriterPipeline": 300,
    "demo.pipelines.Quote2Pipeline": 301,
}

DOWNLOADER_MIDDLEWARES = {
    "demo.middlewares.DoubanUA": 543,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
