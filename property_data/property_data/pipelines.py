# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from property_data.items import PropertyDataItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

sqlite_ddl = """
CREATE TABLE IF NOT EXISTS {} ( 
    link_to_property VARCHAR(255),
    property_title LONGTEXT,
    property_type VARCHAR(255),
    property_address VARCHAR(255),
    property_price VARCHAR(255),
    property_description LONGTEXT,
    property_amenities LONGTEXT,
    property_details LONGTEXT,
    property_images LONGTEXT,
    property_agent VARCHAR(255),
    agency_group VARCHAR(255),
    agency_link VARCHAR(255)
)
"""

sqlite_insert = """
INSERT OR REPLACE INTO properties values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


class PropertyDataPipeline:
    def __init__(self, database_location, table_name):
        self.database_location = database_location
        self.table_name = table_name
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_location=crawler.settings.get('SQLITE_LOCATION'),
            table_name=crawler.settings.get('SQLITE_TABLE', 'properties'),
        )
    
    def open_spider(self, spider):
        self.db = sqlite3.connect(self.database_location)
        self.db.execute(sqlite_ddl.format(self.table_name))
        
    def close_spider(self, spider):
        if self.db:
            self.db.close()

    def process_item(self, item, spider):
        if type(item) == PropertyDataItem:
            self.db.execute(sqlite_insert.format(self.table_name),
                            (
                                item['link_to_property'], item['property_title'], item['property_type'],
                                str(item['property_address']), str(item['property_price']), item['property_description'],
                                str(item['property_amenities']), str(item['property_details']),
                                str(item['property_images']), item['property_agent'], item['agency_group'],
                                item['agency_link']
                            ))
            self.db.commit()

# from itemadapter import ItemAdapter
# import csv
# from property_data.items import PropertyDataItem


# class PropertyDataPipeline:
#     fieldnames_standard = ['link_to_property', 'property_title', 'property_type', 
#                            'property_address', 'property_price', 'property_description',                                                                                   'bullet_points',
#                            'property_amenities', 'property_details', 'property_images',
#                            'property_agent', 'agency_group', 'agency_link']

#     def __init__(self, csv_filename):
#         self.items = []
#         self.csv_filename = csv_filename

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(csv_filename=crawler.settings.get('CSV_FILENAME', 'properties.csv'))

#     def open_spider(self, spider):
#         pass

#     def close_spider(self, spider):
#         with open(self.csv_filename, 'w', encoding='utf-8') as outfile:
#             spamwriter = csv.DictWriter(
#                 outfile, fieldnames=self.get_fieldnames(), lineterminator='\n')

#     def process_item(self, item, spider):
#         return item

#     def get_fieldnames(self):
#         field_names = set()
#         for product in self.items:
#             for key in product.keys():
#                 if key not in self.fieldnames_standard:
#                     field_names.add(key)
#         return self.fieldnames_standard + list(field_names)
