import scrapy
from scrapy.http import Request
from scrapy.loader.processors import Join,MapCompose,TakeFirst
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

class RunoobjSpider(scrapy.Spider):
    name = "newbie"
    start_urls = ['http://www.runoob.com']
    allowed_domains = ['runoob.com']
    custom_settings = {
        'ITEM_PIPELINES':{'tutorial.pipelines.NewbiePipeline':100,'tutorial.pipelines.JsonWriterPipeline':200},
    }

    def item_parse(self,response):
        item_loader = ItemLoader(item=response.meta['item'],response=response)
        item_loader.add_xpath('sub_lessons_menus','//div[@id="leftcolumn"]/a/@title')
        return item_loader.load_item()
    def parse(self, response):
        lessons = response.xpath('//div[contains(@class,"codelist-desktop")]')
        items = []
        for lesson in lessons:
            item = newbie_lessons_item()
            item['lesson_title'] = lesson.xpath('.//h2/text()').extract()
            item['sub_lessons'] = lesson.xpath('.//a/h4/text()').extract()
            item['sub_lessons_url'] = lesson.xpath('.//a/@href').extract()
            items.append(item)
        for data in items:
            urls = data['sub_lessons_url']
            for link in urls:
                yield Request("http://"+link,meta={'item':data},callback=self.item_parse)

class newbie_lessons_item(scrapy.Item):
    sub_lessons = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    lesson_title = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = Join(),
    )
    lesson_url = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    sub_lessons_url = scrapy.Field()
    sub_lessons_menus = scrapy.Field()