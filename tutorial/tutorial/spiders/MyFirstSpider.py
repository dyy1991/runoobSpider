import scrapy
class MyFirstSpider(scrapy.Spider):
    name = "dmoztools"
    # allowed_domains = ["http://dmoztools.net/"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open(filename,'wb') as f:
        #     f.write(response.body)
        for quote in response.css("div.quote"):
            yield {
                'test': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }
        next_page_url = response.css("li.next>a::attr(href").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
        # for sel in response.xpath("//div[@class='children']/section"):
        #     item = DmozItem()
        #     item['title'] = sel.xpath("a/div/text()").extract()
        #     item['link'] = sel.xpath("a/@href").extract()
        #     item['desc'] = sel.xpath("a/text()").extract()
        #     print(item)
class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()