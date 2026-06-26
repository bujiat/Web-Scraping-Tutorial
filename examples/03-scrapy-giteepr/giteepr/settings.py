# Scrapy settings for giteepr project

BOT_NAME = "giteepr"

SPIDER_MODULES = ["giteepr.spiders"]
NEWSPIDER_MODULE = "giteepr.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "giteepr.pipelines.GiteeprPipeline": 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
