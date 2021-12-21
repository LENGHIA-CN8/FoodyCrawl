# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ResId = scrapy.Field()
    RevId = scrapy.Field()
    UserId = scrapy.Field()
    UserName = scrapy.Field()
    Rating = scrapy.Field()
    Comment = scrapy.Field()
    image_url = scrapy.Field()
    streetAddress = scrapy.Field()
    district = scrapy.Field()
    region = scrapy.Field()
    Res_pos_score = scrapy.Field()
    Res_price_score = scrapy.Field()
    Res_food_score = scrapy.Field()
    Res_atmosphere_score = scrapy.Field()
    Res_services_score = scrapy.Field()
    Food_score_cmt = scrapy.Field()
    Services_score_cmt = scrapy.Field()
    Atmosphere_score_cmt = scrapy.Field()
    Position_score_cmt = scrapy.Field()
    Price_score_cmt = scrapy.Field()
    Total_reviews = scrapy.Field()
    Followers = scrapy.Field()
