# -*- coding: utf-8 -*-
import scrapy
from ..items import TouristItem

class PlacesSpider(scrapy.Spider):
    name = 'places'
    allowed_domains = ['trawell.in']
    start_urls = ['http://www.trawell.in/rajasthan/jaipur/places-to-visit-things-to-do']

    def parse(self, response):
        ref = response.css('.destDiv')
        for r in ref:
            category = r.css('.destTitleType::text').extract()
            title = r.css('a::text').extract_first()
            url = r.css('a::attr(href)').extract_first()
            item = TouristItem()
            item['category'] = category
            item['title'] = title
            item['url'] = url
            #print("hello")
            s = scrapy.Request(url=response.urljoin(url),callback=self.parsePlaces)
            s.meta['item'] = item
            yield s
            #yield item

    def  parsePlaces(self,response):
        item=response.meta['item']
        t = response.css('.destSubTextNew::text').extract()
        distance = t[1]   #from railway station
        duration = t[3]
        nearby = t[6]
        item['distance'] = distance
        item['duration'] = duration
        item['nearby_places'] = nearby
        #print("....")
        yield item
