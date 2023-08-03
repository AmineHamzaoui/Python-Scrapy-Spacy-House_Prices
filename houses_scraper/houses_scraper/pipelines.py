# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class HousesPipeline:
    def process_item(self, item, spider):
        # remove the \n\t\t\t\t in the city_region column
        adapter = ItemAdapter(item)
        city_regions = adapter.get('city_region')
        for region in city_regions:
            value = [region.replace('\n\t\t\t\t', '').strip()]
        adapter['city_region'] = value
        # divide the city_region column into city and region

        city_regions_2 = adapter.get('city_region')
        for region_0 in city_regions_2:
            match_1 = re.search(r'.*in(.*)', region_0)
            match_2 = re.search(r'(.*)in.*', region_0)
            city = match_1.group(1).strip() if match_1 else None
            region = match_2.group(1).strip() if match_1 else region_0
        adapter['city'] = city
        adapter['region'] = region
        # remove 'TND' and ',' from price column
        # replace wrong data with null
        prices = adapter.get('price')
        for price in prices:
            if not any(char.isdigit() for char in price):
                adapter['price'] = None
            else:
                cleaned_price = float(price.replace(
                    ' TND', '').replace(',', ''))
                adapter['price'] = cleaned_price

            """
        prices = adapter.get('price')
        for price in prices:
            price=float(price.replace(' TND', '').replace(',', ''))
        adapter['price']=price
        """

        """
        cleaned_items = []

        for region in city_regions:
            match = re.search(r'.*in(.*)', region)
            if match:
                region = match.group(1).strip()
                city = match.group(2).strip()
            else:
                city = None

            cleaned_items.append({
                "city": city,
                "region": region
            })
            item = adapter.copy()
            item['city'] = city
            item['region'] = region
            """
        return item
