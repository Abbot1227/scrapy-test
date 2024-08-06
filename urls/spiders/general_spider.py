import scrapy

import json
import os


class GeneralSpider(scrapy.Spider):
    name = 'general'

    custom_settings = {'FEED_URI': 'batch/%(name)s_%(batch_time)s.json',
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_BATCH_ITEM_COUNT': 10}



    def start_requests(self):
        reader = JsonReader('../urls.json', 10)
        for a in ArticlesIterator(reader, 10):
            yield scrapy.Request(url=a['news_url'], callback=self.parse, meta={'data': a})

    # Tried ScrapyContract for test
    def parse(self, response, **kwargs):
        """
        parse function traverses through urls from
        urls json and crawl articles from each

        @url https://apnews.com/
        @returns requests 10
        @scrapes title news_page_url
        """
        site = response.meta['data']
        for article in response.css('div' + site['main_div_news']):
            title = article.css(site['title']+'::text').get()
            news_page_url = article.css(site['news_page_url']).get()

            if site['relative_url'] == '1':
                news_page_url = site['main_url'][0:-2] + news_page_url

            yield {
                'title': title,
                'news_page_url': news_page_url,
            }

            yield scrapy.Request(url=news_page_url,
                                 callback=self.parse_article,
                                 meta={'title': title, 'url': news_page_url, 'data': site}
                                 )

    def parse_article(self, response):
        site = response.meta['data']
        title = response.meta['title']
        url = response.meta['url']
        published_date = response.css(site['published_date']+'::text').get()
        summary = response.css(site['summary']).get()
        tags = response.css(site['tags']+'::text').getall()
        author = response.css(site['author']+'::text').get()
        content = " ".join(response.css('div' + site['content_main_div'] + " " + site['content_para_P_if_not']).getall())

        scraped = {
            'title': title,
            'url': url,
            'published_date': published_date,
            'summary': summary,
            'tags': tags,
            'author': author,
            'content': content,
        }

        yield scraped


# JsonReader is used to read data
# of each news from json
class JsonReader:
    def __init__(self, path, start=-1):
        self.path = path
        self.ctr = start
        if not os.path.exists(self.path):
            raise FileNotFoundError
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f'{self.path} not found')

    def next(self):
        self.ctr += 1
        if self.ctr >= len(self.data):
            raise IndexError("end reached")
        return self.data[self.ctr]


# Iterator to traverse through new from json
# stop is to limit number of news
class ArticlesIterator:
    def __init__(self, reader: JsonReader, stop):
        self.reader = reader
        self._stop = stop
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            if self._index >= self._stop:
                raise StopIteration
            a = self.reader.next()
            self._index += 1
            return a
        except IndexError:
            raise StopIteration

