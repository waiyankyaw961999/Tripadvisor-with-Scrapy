import scrapy.spiders
from scrapy.loader import ItemLoader
from Tripadvisor.items import TripadvisorItem
from scrapy import Request


class Tripadvisor(scrapy.Spider):
    name = 'tripadvisor'

    start_urls = ["https://www.tripadvisor.com/Hotels-g294191-Yangon_Rangoon_Yangon_Region-Hotels.html",    # 1Yangon
                  "https://www.tripadvisor.com/Tourism-g295408-Mandalay_Mandalay_Region-Vacations.html",    # 2Mandalay
                  "https://www.tripadvisor.com/Hotels-g739122-Sagaing_Sagaing_Region-Hotels.html",          # 3Sagaing
                  "https://www.tripadvisor.com/Hotels-g2036450-Naypyidaw_Mandalay_Region-Hotels.html",      # 4Naypyidaw
                  "https://www.tripadvisor.com/Hotels-g1381170-Shan_State-Hotels.html",                     # 5Shan
                  "https://www.tripadvisor.com/Tourism-g3576018-Tanintharyi_Region-Vacations.html",         # 6Tanintharyi
                  "https://www.tripadvisor.com/Hotels-g3576023-Rakhine_State-Hotels.html",                  # 7Rakhine
                  "https://www.tripadvisor.com/Hotels-g3576030-Kachin_State-Hotels.html",                   # 8Kachin
                  "https://www.tripadvisor.com/Hotels-g3576046-Mon_State-Hotels.html",                      # 9Mon
                  "https://www.tripadvisor.com/Hotels-g3576052-Kayin_State-Hotels.html",                    # 10Kayin
                  "https://www.tripadvisor.com/Hotels-g4586016-Kayah_State-Hotels.html",                    # 11Kayah
                  "https://www.tripadvisor.com/Hotels-g303655-Bago_Bago_Region-Hotels.html",                # 12Bago
                  "https://www.tripadvisor.com/Hotels-g3576010-Ayeyarwady_Region-Hotels.html",              # 13Ayeyarwaddy
                  "https://www.tripadvisor.com/Hotels-g739118-Magway_Magway_Region-Hotels.html"             # 14Magway
                  ]

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


