#encoding = utf-8
import scrapy
from scrapy.http import Request

class runoobSpider(scrapy.Spider):
    name = "runoob"
    allowed_domains = ["runoob.com"]
    start_urls = ["http://www.runoob.com"]
    def item_parse(self,response):
        item = response.meta['item']
        item['sub_menus'] = response.xpath('//div[@id="leftcolumn"]/a/@title').extract()
        return item
    def parse(self, response):
        left_div = response.xpath('//div[@id="main-left-cloumn"]')
        right_div = response.xpath('//div[contains(@class,"codelist-desktop")]')
        item0 = LeftItem()
        for content in left_div:
            item0['id'] = content.xpath('//div[@class="design"]/@id').extract()
            item0['text'] = content.xpath('//div[@class="navto-nav"]/text()').extract()
            item0['result'] = []
            # yield {
            #     "text" : content.xpath('//div[@class="navto-nav"]/text()').extract(),
            #     "id" : content.xpath('//div[@class="design"]/@id').extract(),
            #     "result" : []
            # }
        item = DmozItem()
        for codelist in right_div:
            item['title'] = codelist.xpath('.//a/h4/text()').extract()
            item['desc'] = codelist.xpath('.//a/strong/text()').extract()
            item['link'] = codelist.xpath('.//a/@href').extract()
        yield item0
        yield item
        for link in item['link']:
            yield Request("http://"+link,meta={'item':item},callback=self.item_parse)
            # yield {
            #     "title" :codelist.xpath('a/h4/text()').extract(),
            #     "description":codelist.xpath('a/strong/text()').extract(),
            #     "url":codelist.xpath('a/@href').extract()
            # }
class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    sub_menus = scrapy.Field()
class LeftItem(scrapy.Item):
    id = scrapy.Field()
    text = scrapy.Field()
    result = scrapy.Field()
