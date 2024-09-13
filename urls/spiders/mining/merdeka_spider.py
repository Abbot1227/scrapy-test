from typing import Any

from scrapy import Spider
from scrapy.http import Response

from urls.itemsloaders import WikiMineItemsLoader
from urls.items import MiningItem


class MerdekaSpider(Spider):
    name = "merdeka"
    allowed_domains = ["merdekacoppergold.com"]
    start_urls = ["https://merdekacoppergold.com/en/our-business/wetar-copper-mine/",
                  "https://merdekacoppergold.com/en/our-business/tujuh-bukit-gold-mine/",
                  "https://merdekacoppergold.com/en/our-business/tujuh-bukit-copper-project/",
                  "https://merdekacoppergold.com/en/our-business/pani-gold-project/"]


    def parse(self, response: Response, **kwargs: Any) -> Any:
        loader = WikiMineItemsLoader(item=MiningItem(), response=response)
        loader.add_value('name', response.css('h4.lqd-simple-heading::text').get())
        loader.add_value('source', response.url)
        loader.add_value()
