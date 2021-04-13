import scrapy.spiders
from scrapy.loader import ItemLoader
from Tripadvisor.items import TripadvisorItem
from scrapy import Request


class Tripadvisor(scrapy.Spider):
    name = 'tripadvisor'

    start_urls = ["https://www.tripadvisor.com/Hotels-g294190-Myanmar-Hotels.html"]

    # //div[@class="listing_title"]/a/@href      > for reviews for single hotel
    # //h1[@class="_1mTlpMC3"]/text()            > name of hotel
    # //div[@class="_36QMXqQj"][1]/text()        > price
    # //div[@class="kVNDLtqL"]/span/text()       > rating
    # //div[@class="_2-OvcgvB"]/text()           > grading
    # //span[@class="_3jEYFo-z"]/text()          >reviewers
    # //span[@class="_3ErVArsu jke2_wbp"]/text() >address

    def parse(self, response):

        for title in response.xpath("//div[@class='listing_title']/a/@href").extract():
            page = response.urljoin(title)
            yield scrapy.Request(url=page,callback=self.parse_review_page)

        next_page = response.selector.xpath("//a[@class='nav next ui_button primary']/@href").extract_first()
        if next_page is not None:
            pages = response.urljoin(next_page)
            yield scrapy.Request(url=pages[:-8], callback=self.parse)

    def parse_review_page(self,response):
        loader = ItemLoader(item=TripadvisorItem(),response=response)
        loader.add_xpath('name', ".//h1[@class='_1mTlpMC3']/text()")
        loader.add_xpath('price',".//div[@class='_36QMXqQj']/text()")
        loader.add_xpath('rating', ".//div[@class='kVNDLtqL']/span/text()")
        loader.add_xpath('review_count',".//span[@class='_3jEYFo-z']/text()")
        loader.add_xpath('grading',".//div[@class='_2-OvcgvB']/text()")
        loader.add_xpath('address', ".//span[@class='_3ErVArsu jke2_wbp']/text()")
        yield loader.load_item()


