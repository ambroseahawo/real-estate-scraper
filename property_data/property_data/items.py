# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class PropertyDataItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link_to_property = Field()
    property_title = Field()
    property_type = Field()
    property_address = Field()
    property_price = Field()
    property_description = Field()
    property_amenities = Field()
    property_details = Field()
    property_images = Field()
    property_agent = Field()
    agency_group = Field()
    agency_link = Field()
