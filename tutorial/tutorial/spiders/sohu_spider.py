import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from tutorial.items import SohuItem

class SohuSpider(CrawlSpider):
    name = "sohu"
    allowed_domains = ["m.sohu.com"]
    start_urls = [
        "http://m.sohu.com/",
    ]
    rules = (
        Rule(LinkExtractor(allow = r'n/'),callback='news_parse', follow=True),
    )

    def news_parse(self, response):
        sel = response.xpath('//article')
        item = SohuItem()
        item['link'] = response.url
        item['title'] = self.clear_tab(sel.xpath('h1[@class="h1"]/text()').extract())
        item['content'] = self.clear_tab(sel.xpath('p[@class="para"]/text()').extract())
        item['img_link'] = sel.xpath('div[@class="media-wrapper"]/div[@class="image"]/img/@src').extract()
        item['img_name'] = sel.xpath('div[@class="media-wrapper"]/div[@class="media-info"]/span/text()').extract()
        return item

    def clear_tab(self, sentence):
        return [x.strip() for x in sentence] 