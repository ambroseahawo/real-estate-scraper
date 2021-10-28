import scrapy
import wget
import os
import re
import uuid
from property_data.items import PropertyDataItem
import random

# 1170 - 1389
# scrapy crawl properties -o properties.csv
# scrapy crawl properties -s SQLITE_LOCATION=properties_data.db


def gen_rand_no():
    used_numbers_lst = []
    for counter in range(5000):
        rand = random.randint(6000, 10000)
        if rand not in used_numbers_lst:
            return rand
        used_numbers_lst.append(rand)


class PropertiesSpider(scrapy.Spider):
    name = 'properties'
    allowed_domains = ['www.myproperty.ph']
    start_urls = ['https://www.myproperty.ph/apartment/buy/?q=Philppines']

    def parse(self, response):
        urls = response.xpath('//a[@class="js-listing-link"]/@href').getall()
        urls = list(dict.fromkeys(urls))
        print(len(urls))

        for each_url in urls:
            # print(urls[each_url])
            yield response.follow(each_url, callback=self.parse_leading_link)

        # next_page_url = response.xpath('//div[@class="next "]/a/@href').get()
        # if next_page_url:
        #     print(next_page_url)
        #     yield response.follow(next_page_url, callback=self.parse)

    def parse_leading_link(self, response):
        item = PropertyDataItem()
        img_url = []
        dict_names = []
        dict_items = []
        item['property_type'] = 'land to buy'
        item['link_to_property'] = response.url
        item['property_title'] = response.xpath('//title/text()').get()

        # property address
        address_string = "".join(response.xpath('//h3//span[@class="Header-title-address-text"]/text()'
                                                ).getall()).strip().replace("\n", " ")
        item['property_address'] = re.sub(r"\s+", " ", address_string)

        item['property_price'] = response.xpath('//span[@class="Overview-main FirstPrice"]/text()').get(
            default="Contact agent for price")

        # property description
        prop_li = []
        property_info = response.xpath('//div[@class="ViewMore-text-description"]/p/text()').getall()
        if not property_info:
            property_info = response.xpath('//div[@class="ViewMore-text-description"]/text()').getall()
            for each_p in property_info:
                prop_li.append(each_p.strip().replace("\n", " "))
            item['property_description'] = "".join(prop_li)
        elif not property_info:
            property_info = response.xpath('//div[@class="ViewMore-text-description"]//ul/li/text()').getall()
            for each_p in property_info:
                prop_li.append(each_p.strip().replace("\n", " "))
            item['property_description'] = " ".join(prop_li)
        else:
            for each_p in property_info:
                prop_li.append(each_p.strip().replace("\n", " "))
            item['property_description'] = "".join(prop_li)

        try:
            am_list = []
            for am in response.xpath('//section[@id="listing-amenities"]//div[@class="ellipsis"]/text()').getall():
                am_list.append(am.strip())

            item['property_amenities'] = "\n".join(am_list)
        except:
            item['property_amenities'] = ''

        try:
            # dict keys
            details_name = response.xpath('//section[@id="listing-details"]//div[@class="ellipsis"]/text()').getall()
            for each_name in details_name:
                if each_name == '':
                    pass
                dict_names.append(each_name.strip())
            for each_name in dict_names:
                dict_names.remove('')

            # dict values
            details_item = response.xpath('//section[@id="listing-details"]//div[@class="last"]/text()').getall()
            for each_item in details_item:
                if each_item == '':
                    pass
                dict_items.append(each_item.strip())

            # full-dict
            full_dict = {dict_names[i]: dict_items[i] for i in range(len(dict_names))}

            if not full_dict:
                item['property_details'] = ''
            else:
                item['property_details'] = full_dict
        except:
            item['property_details'] = ''

        for img_src in response.xpath('//img[@class="swiper-lazy"]/@data-src').getall():
            random_number = gen_rand_no()
            id_ = uuid.uuid4()
            img_name = "{}-{}.jpg".format(id_, random_number)
            img_location = ".\images\{}".format(img_name)
            wget.download(img_src, img_location)
            location_to_append = "\images\{}".format(img_name)
            img_url.append(location_to_append)

        item['property_images'] = img_url

        try:
            item['property_agent'] = response.xpath('//div[@class="Agent-contactName"]/text()').get().strip().replace(
                "\n", " ")
        except:
            item['property_agent'] = ''

        try:
            item['agency_group'] = response.xpath('//div[@class="Agent-name small-9 medium-8 columns"]/text()'
                                                  ).get().strip().replace("\n", " ")
        except:
            item['agency_group'] = ''

        try:
            item['agency_link'] = response.xpath('//div[@class="Agent-link"]/a/@href').get()
        except:
            item['agency_link'] = None

        yield item
