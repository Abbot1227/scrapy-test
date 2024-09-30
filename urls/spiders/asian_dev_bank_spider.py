from email.policy import default
from typing import Any

from scrapy import Spider
from scrapy.http import Response

from urls.itemsloaders import WaterItemsLoader

from urls.items import WaterItem


class AsianDevBankSpider(Spider):
    name = "asian_bank"
    allowed_domains = ["www.adb.org"]
    start_urls = ["https://www.adb.org/projects/country/indonesia/sector/water-and-other-urban-infrastructure-and-services-1065/year/2024/year/2023/year/2022/year/2021/year/2020/year/2019/year/2018"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for div in response.css('div.item'):
            loader = WaterItemsLoader(item=WaterItem(), response=response)
            loader.add_value('name', div.css('div.item-title a::text').get())
            url = div.css('div.item-title a::attr(href)').get()
            url = response.urljoin(url)
            loader.add_value('source', url)
            loader.add_value('status', div.css('div.item-meta span + span::text').get())
            loader.add_value('approval_date', div.css('div.item-meta time::text').get())

            yield response.follow(url=url, callback=self.parse_details, meta={'loader': loader})

    def parse_details(self, response: Response, **kwargs: Any) -> Any:
        loader = response.meta['loader']
        for dt in response.css('div.xsl-formatter dt'):
            text = dt.css('::text').get()

            if text == 'Project Type / Modality of Assistance':
                loader.add_value('project_type', dt.xpath('following-sibling::dd[1]/text()').get())
            elif text == 'Source of Funding / Amount':
                dd = dt.xpath('following-sibling::dd[1]')
                budget = ''
                for tr in dd.css('tr'):
                    budget += tr.css('td::text').get(default='') + ' - ' + tr.css('td + td::text').get(default='') + '\n'
                loader.add_value('budget', budget)
            elif text == 'Operational Priorities':
                dd = dt.xpath('following-sibling::dd[1]')
                priorities = ''
                for li in dd.css('li'):
                    priorities += li.css('::text').get(default='') + '\n'
                loader.add_value('priorities', priorities)
            elif text == 'Description':
                dd = dt.xpath('following-sibling::dd[1]')
                loader.add_value('description', dd.css('::text').get())
            elif text == 'Geographical Location':
                dd = dt.xpath('following-sibling::dd[1]')
                loader.add_value('location', dd.css('::text').get())

        yield loader.load_item()