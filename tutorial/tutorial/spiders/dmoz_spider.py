import scrapy
from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="site-item "]/div[@class="title-and-desc"]'):
            item = DmozItem()
            item['title'] = self.clear_tab(sel.xpath('a/div[@class="site-title"]/text()').extract())
            item['link'] = self.clear_tab(sel.xpath('a/@href').extract())
            item['desc'] = self.clear_tab(sel.xpath('div[@class="site-descr "]/text()').extract())
            yield item

    def clear_tab(self, sentence):
        return [x.strip() for x in sentence] 