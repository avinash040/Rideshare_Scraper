# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RidesharescraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class KijijiRideshareItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()

class kijijiRideshareData(scrapy.Item):
	url = scrapy.Field()
	title = scrapy.Field()
	date_listed = scrapy.Field()
	price = scrapy.Field()
	address = scrapy.Field()
	phone_number = scrapy.Field()
	full_text = scrapy.Field()
