BOT_NAME = "demo"

SPIDER_MODULES = ["demo.spiders"]
NEWSPIDER_MODULE = "demo.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "demo.pipelines.JsonWriterPipeline": 300,
    "demo.pipelines.Quote2Pipeline": 301,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
