# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PractoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    doctor = scrapy.Field()
    qualification = scrapy.Field()
    experience = scrapy.Field()
    fees = scrapy.Field()
    specializations = scrapy.Field()
    upvote_percentage = scrapy.Field()
    total_votes = scrapy.Field()
    clinic_name = scrapy.Field()
    address = scrapy.Field()
    clinic_ratings = scrapy.Field()
    services = scrapy.Field()
    registrations = scrapy.Field()
    feedbacks_all = scrapy.Field()
    total_feedbacks = scrapy.Field()
    pass


