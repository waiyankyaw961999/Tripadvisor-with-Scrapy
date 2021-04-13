import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from Tripadvisor.items import ThingstodoItem


class Tripadvisor(scrapy.Spider):
    name = 'thingstodo'
    script = '''
function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    treat = require('treat')
    result = {}
    for i=1,62,1
    do
        assert(splash:runjs('document.querySelector("#lithium-root main div._1I73Kb0a a").click()'))
        result[i]=splash:html()
    end
    return treat.as_array(result)
end  
    '''

    # //div[@class='_1gpq3zsA _1zP41Z7X'] >name
    # //div[@class='_3W_31Rvp _1nUIPWja _17LAEUXp _2b3s5IMB']/div[1]/text()  > famous for its
    def start_requests(self):
        url = "https://www.tripadvisor.com/Attractions-g294190-Activities-a_allAttractions.true-Myanmar.html"
        yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={'wait': 0.5})
        yield SplashRequest(url=url, callback=self.parse_other_pages, endpoint='execute',
                            args={'wait': 0.5, 'lua_source': self.script}, dont_filter=True)

    def parse(self, response):
        for title in response.xpath("//div[@class='oQFSuk9j']"):
            loader = ItemLoader(item=ThingstodoItem(), selector=title)
            loader.add_xpath('name', ".//div[@class='_1gpq3zsA _1zP41Z7X']")
            loader.add_xpath('viewer', ".//span[@class='DrjyGw-P _26S7gyB4 _14_buatE _1dimhEoy']/text()")
            loader.add_xpath('status', ".//div[@class='_3W_31Rvp _1nUIPWja _17LAEUXp _2b3s5IMB']/div[1]/text()")
            yield loader.load_item()

    def parse_other_pages(self, response):
        for page in response.data:
            sel = Selector(text=page)
            for title in sel.xpath("//div[@class='oQFSuk9j']"):
                loader = ItemLoader(item=ThingstodoItem(), selector=title)
                loader.add_xpath('name', ".//div[@class='_1gpq3zsA _1zP41Z7X']")
                loader.add_xpath('viewer', ".//span[@class='DrjyGw-P _26S7gyB4 _14_buatE _1dimhEoy']/text()")
                loader.add_xpath('status', ".//div[@class='_3W_31Rvp _1nUIPWja _17LAEUXp _2b3s5IMB']/div[1]/text()")
                yield loader.load_item()
