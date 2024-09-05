# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class RemoveEmptyValuesPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('name') in [None, '']:
            return None

        if spider.name == 'global_energy':
            if adapter.get('plant_type') in [None, 'Please Select']:
                adapter['plant_type'] = ''
            if adapter.get('secondary_fuel') in [None, 'Please Select']:
                adapter['secondary_fuel'] = ''

        return item