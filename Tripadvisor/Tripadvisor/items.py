# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

def remove_quotations(value):
    return value.replace(u"\u201d", '').replace(u"\u201c", "")

class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    review_count = scrapy.Field(output_processor=TakeFirst())
    grading = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=TakeFirst())


"""
  text = scrapy.Field(input_processor=MapCompose(str.strip, remove_quotations),
                        output_processor=TakeFirst()
                        )
    author = scrapy.Field(input_processor=MapCompose(str.strip, remove_tags),
                          output_processor=TakeFirst()
                          )
    tags = scrapy.Field(input_processor=MapCompose(remove_tags),
                        output_processor=Join(',')
"""