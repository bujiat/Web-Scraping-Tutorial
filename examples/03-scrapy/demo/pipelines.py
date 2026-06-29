import json


class JsonWriterPipeline:
    def open_spider(self, spider):
        if spider.name != "qutoe2":
            self.f = open(f"{spider.name}.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        if spider.name != "qutoe2":
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.f.write(line)
        return item

    def close_spider(self, spider):
        if spider.name != "qutoe2":
            self.f.close()



class Quote2Pipeline:
    def open_spider(self, spider):
        if spider.name == "qutoe2":
            self.f = open(f"{spider.name}.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        if spider.name == "qutoe2":
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.f.write(line)
        return item

    def close_spider(self, spider):
        if spider.name == "qutoe2":
            self.f.close()