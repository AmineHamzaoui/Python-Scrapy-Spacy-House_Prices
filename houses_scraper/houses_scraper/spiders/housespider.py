import scrapy
import spacy
from spacy.matcher import Matcher
import re
from houses_scraper.items import HouseItem

class HousespiderSpider(scrapy.Spider):
    name = "housespider"
    allowed_domains = ["www.mubawab.tn"]
    start_urls = ["https://www.mubawab.tn/en/sc/houses-for-sale"]
   #crawl function
   #1 : it goes into the url
    def parse(self, response):
        houses = response.css('li.listingBox')
        for house in houses:
            relative_url = house.css('div p a::attr(href)').get(default='n/a')
            if relative_url is not None:
                house_url = relative_url
                #2 : it goes into the callback function
                #4ther's a loop here where it goes into multiple houses in the same page
                yield response.follow(house_url, callback=self.parse_house_page)
#4 : it goes into the next page 
#5 : Repeats

        next_page = response.css(
            'div a.arrowDot:has(i.icon-right-open.rotate180)::attr(href)').get()
        if next_page is not None:
            next_page_url = next_page
            yield response.follow(next_page_url, callback=self.parse)
#3 : it parses the page 
    def parse_house_page(self, response):
        #RegEx way to extract features from descriptions
        descriptions = ''.join(response.xpath('/html/body/section/div[2]/div/div[6]/p//text()').getall()).strip()
        
        
      
        patterns = {'living areas': r"([0-9]+)\ (?:living areas?)",
                    'bathrooms': r"([0-9]+)\ (?:bathrooms?)",
                    'rooms': r"([0-9]+)\ (?:rooms?)",
                    'size': r"([0-9]+)\ (?:m²|sqm|square meters?)",
                    'bedrooms': r"([0-9]+)\ (?:bedrooms?)",
                    'type': r"house|residence|apartment|land"}
        rooms = re.findall(patterns['rooms'], descriptions, re.M | re.I)
        size = re.findall(patterns['size'], descriptions, re.M | re.I)
        bathrooms = re.findall(patterns['bathrooms'], descriptions, re.M | re.I)
        living_areas = re.findall(patterns['living areas'], descriptions, re.M | re.I)
        bedrooms = re.findall(patterns['bedrooms'], descriptions, re.M | re.I)
        type_of_property = re.findall(patterns['type'], descriptions, re.M | re.I)
        rooms_value = None
        size_value = None
        bathrooms_value = None
        living_areas_value = None
        bedrooms_value = None
        type_of_property_value = None
        if len(rooms) > 0:
            if len(rooms) > 1:
                numbers = [int(num) for num in rooms]
                # Get the maximum value
                rooms_value = max(numbers)
            else:
                rooms_value = rooms[-1]

        if len(size) > 0:
            size_value = size[-1]

        if len(bathrooms) > 0:
            bathrooms_value = bathrooms[-1]

        if len(living_areas) > 0:
            living_areas_value = living_areas[-1]

        if len(bedrooms) > 0:
            bedrooms_value = bedrooms[-1]

        if len(type_of_property) > 0:
            if 'house' in type_of_property and 'residence' in type_of_property:
                type_of_property_value = 'apartment'
            else:
                type_of_property_value = type_of_property[0]
        house_item=HouseItem()
    

        
        house_item['url']= response.url,
        house_item['price']= response.css('div h3::text').get().strip(),
        house_item['city_region']= response.css('div h3.greyTit::text').get().strip(),
        house_item['description']= descriptions,
        house_item[ 'rooms']= rooms_value,
        house_item['size']= size_value,
        house_item['bathrooms']= bathrooms_value,
        house_item['living_areas']= living_areas_value,
        house_item['bedrooms']= bedrooms_value,
        house_item['type_of_property']= type_of_property_value 
            
        yield house_item

        #the spacy way to extract features but it needs to be fixed
""" 
        nlp = spacy.load('en_core_web_sm')
        patterns = [
            [{"IS_DIGIT": True}, {"LOWER": {"IN": ["room", "rooms"]}}],
            [{"IS_DIGIT": True}, {"LOWER": {"IN": ["m²", "sqm", "square meters"]}}],
            [{"IS_DIGIT": True},{"LOWER": {"IN": ["bathroom", "bathrooms"]}}],
            [{"IS_DIGIT": True},{"LOWER": {"IN": ["living", "living areas"]}}],
            [{"IS_DIGIT": True},{"LOWER": {"IN": ["bedroom", "bedrooms"]}}],
            [{"LOWER": {"IN": ["house", "apartment", "residence", "land"]}}]
        ]
        matcher = Matcher(nlp.vocab)
        for pattern in patterns:
            matcher.add("FEATURE", [pattern])
            
        doc = nlp(''.join(response.xpath('/html/body/section/div[2]/div/div[6]/p//text()').getall()).strip())
        matches = matcher(doc)
       
        features = {
            'rooms': None,
            'size': None,
            'bathrooms': None,
            'living_areas': None,
            'bedrooms': None,
            'type_of_property': None

        }
        match_text = None
            for match_id, start, end in matches:
                match_text = doc[start:end].text.lower()
                
                if match_text == "rooms":
                    value = doc[start + 1].text
                    print(f"Raw Value: {value}")
                    value = re.sub("[^0-9]", "", value)
                    print(f"Cleaned Value: {value}")
                    if value.isdigit():
                        features['rooms'] = int(value)
                elif match_text.startswith(("size", "area")):
                    value = doc[start + 1].text
                    print(f"Raw Value: {value}")
                    value = re.sub("[^0-9]", "", value)
                    print(f"Cleaned Value: {value}")
                    if value.isdigit():
                        features['size'] = int(value)
                elif match_text == "bathrooms":
                    value = doc[start + 1].text
                    print(f"Raw Value: {value}")
                    value = re.sub("[^0-9]", "", value)
                    print(f"Cleaned Value: {value}")
                    if value.isdigit():
                        features['bathrooms'] = int(value)
                elif match_text.startswith("living areas"):
                    value = doc[start + 1].text
                    print(f"Raw Value: {value}")
                    value = re.sub("[^0-9]", "", value)
                    print(f"Cleaned Value: {value}")
                    if value.isdigit():
                        features['living_areas'] = int(value)
                elif match_text.startswith("bedrooms"):
                    value = doc[start + 1].text
                    print(f"Raw Value: {value}")
                    value = re.sub("[^0-9]", "", value)
                    print(f"Cleaned Value: {value}")
                    if value.isdigit():
                        features['bedrooms'] = int(value)
                elif match_text == "property":
                    value = doc[start + 1].text.capitalize()
                    print(f"Value: {value}")
                    features['type_of_property'] = value """

