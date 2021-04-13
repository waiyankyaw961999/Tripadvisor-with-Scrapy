# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Join, MapCompose


def remove_quotations(value):
    return value.replace(u"\u2022", '')


def remove_long_string(value):
    return value.replace('<div class=\"_1gpq3zsA _1zP41Z7X\"><span class=\"_1Nzq2vxD\">', '').replace(
        '</span> <!-- -->', '').replace('</div>', '')


class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    review_count = scrapy.Field(output_processor=TakeFirst())
    grading = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=TakeFirst())


class ThingstodoItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_long_string),
                        output_processor=TakeFirst())
    viewer = scrapy.Field(output_processor=TakeFirst())
    status = scrapy.Field(input_processor=MapCompose(remove_quotations),
                          output_processor=TakeFirst())


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
