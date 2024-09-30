from typing import Any

from scrapy import Spider
from scrapy.http import Response

from urls.itemsloaders import WaterItemsLoader

from urls.items import WaterItem


class KPPIPSpider(Spider):
    name = "kppip"
    allowed_domains = ["kppip.go.id"]
    start_urls = ["https://kppip.go.id/en/priority-projects/water-sanitation/jakarta-sewerage-system-jss/",
                  "https://kppip.go.id/en/priority-projects/water-sanitation/west-semarang-drinking-water-supply-system/",
                  "https://kppip.go.id/en/priority-projects/water-sanitation/national-capital-integrated-coastal-development-ncicd-phase-a/",
                  "https://kppip.go.id/en/priority-projects/water-sanitation/drinking-water-supply-system-spam-regional-jatiluhur/",
                  "https://kppip.go.id/en/priority-projects/water-sanitation/drinking-water-supply-system-spam-lampung/",
                  "https://kppip.go.id/proyek-prioritas/air-dan-sanitasi/pengolahan-air-limbah-jakarta/",
                  "https://kppip.go.id/proyek-prioritas/air-dan-sanitasi/spam-semarang-barat/",
                  "https://kppip.go.id/proyek-prioritas/air-dan-sanitasi/tanggul-laut/",
                  "https://kppip.go.id/proyek-prioritas/air-dan-sanitasi/sistem-penyediaan-air-minum-spam-regional-jatiluhur//",
                  "https://kppip.go.id/proyek-prioritas/air-dan-sanitasi/sistem-penyediaan-air-minum-spam-lampung//"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        loader = WaterItemsLoader(item=WaterItem(), response=response)
        loader.add_value('name', response.css('h1::text').get())
        loader.add_value('source', response.url)

        budget = ''
        for tr in response.css('table.table tr'):
            text = tr.css('td strong::text').get()
            print(text)
            if text == 'Project Status' or text == 'Status Terakhir':
                loader.add_value('status', tr.css('td + td + td::text').get())
            elif text == 'Investment Value' or text == 'Investasi Total' or text == 'Nilai Investasi':
                budget += tr.css('td + td + td::text').get() + ' - '
            elif text == 'Funding Scheme' or text == 'Skema Pendanaan':
                budget += tr.css('td + td + td::text').get()
            elif text == 'Project Owner':
                loader.add_value('owner', tr.css('td + td + td::text').get())
            elif text == 'Construction Commencement Plan' or text == 'Rencana Mulai Konstruksi':
                loader.add_value('construction_year', tr.css('td + td + td::text').get())
            elif text == 'Commercial Operation Date' or text == 'Rencana Mulai Operasi':
                loader.add_value('start_year', tr.css('td + td + td::text').get())
            elif text == 'Location' or text == 'Lokasi':
                loader.add_value('location', tr.css('td + td + td::text').get())
            elif text == 'Implementing Agency' or text == 'Penanggung Jawab Proyek':
                loader.add_value('contractor', tr.css('td + td + td::text').get())

        if budget:
            loader.add_value('budget', budget)

        # desc = response.css('div.page')[0]
        # loader.add_value('description', desc.css('p::text').getall())
        # significance = response.css('div.page')[1]
        # loader.add_value('significance', significance.css('p::text').getall())


        yield loader.load_item()
