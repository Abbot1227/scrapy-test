import scrapy

class RechargeSpider(scrapy.Spider):
    name = 'recharge'
    allowed_domains = ['rechargenews.com', 'windpowermonthly.com']
    start_urls = ['https://www.rechargenews.com/latest', 'https://www.windpowermonthly.com/news']

    custom_settings = {'FEED_URI': 'recharge_%(time)s.json',
                       'FEED_FORMAT': 'json'}

    def parse(self, response):
        for article in response.css('.teaser-body'):
            title = article.css('h2.teaser-title a::text').get()
            news_page_url = article.css('h2.teaser-title a::attr(href)').get()

            news_page_url = 'https://www.rechargenews.com' + news_page_url

            yield scrapy.Request(url=news_page_url, callback=self.parse_article, meta={'title': title, 'url': news_page_url})

    def parse_article(self, response):
        title = response.meta['title']
        url = response.meta['url']
        published_date = response.css('span.published::text').get()
        summary = response.css('div.dn-article-top p.lead::text').get()
        tags = response.css('div.dn-article-top a.tag span::text').getall()
        author = response.css('ul.author-list a::text, div.author-subtle span::text').get()
        content = " ".join(response.css('p.dn-text::text').getall())

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
