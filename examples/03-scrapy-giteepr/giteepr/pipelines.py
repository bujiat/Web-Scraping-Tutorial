from itemadapter import ItemAdapter
import json


class GiteeprPipeline:
    def open_spider(self, spider):
        self.f = open("gitee.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        item_dict = dict(item)
        line = json.dumps(item_dict, ensure_ascii=False) + "\n"
        self.f.write(line)
        return item

    def close_spider(self, spider):
        self.f.close()
