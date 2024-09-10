# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class RemoveEmptyValuesPipeline:
    def process_item(self, item, spider):
        # TODO modify to avoid null item error
        # adapter = ItemAdapter(item)
        #
        # if adapter.get('name') in [None, '']:
        #     return None
        #
        # if spider.name == 'global_energy':
        #     if adapter.get('plant_type') in [None, 'Please Select']:
        #         adapter['plant_type'] = ''
        #     if adapter.get('secondary_fuel') in [None, 'Please Select']:
        #         adapter['secondary_fuel'] = ''
        #     if adapter.get('status') in [None, 'Please Select']:
        #         adapter['status'] = ''

        return item

class RemoveLessThan100Pipeline:
    def process_item(self, item, spider):
        # adapter = ItemAdapter(item)
        #
        # try:
        #     capacity = adapter.get('capacity')
        #     capacity = int(capacity)
        # except:
        #     return None
        #
        # if capacity < 100:
        #     return None
        return item
