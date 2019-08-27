# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import dateparser

class DalhousieSpider(scrapy.Spider):
    name = 'dalhousie_stfx'
    start_urls = ['https://www.goxgo.ca/sports/xc/2019-20/schedule',
    'http://www.daltigers.ca/sports/xc/2019-20/schedule']

    def parse(self, response):
        # 'odd' and 'even' parent tr's for this site
        for race in response.css('table tr.odd'):
            if race.css('.e_date::text').get():
                # this seems to be getting needlessly complicated
                # basically below looks for the first month header above where the date is and use that later for date parsing
                month = response.xpath("//*[@class='e_date'][text()=\"" + race.css('.e_date::text').get() + "\"]/../preceding-sibling::tr[@class='month-title'][1]/td/text()").get()
                yield {
                    'date': dateparser.parse(month + ' ' + race.css('.e_date::text').get()), # dateparser having a hard time understanding only 'Sat. 5'
                    'raceLocation': race.css('.e_neutralsite::text').get(), # .split(' ')[1:], # can remove the @ sign if need be
                    'raceDescriptor': race.css('.e_teamname.e_opponent_name::text').get(),
                    'travellingSchool': response.css('meta[property="og:site_name"]::attr(content)').get()
                }
        for race in response.css('table tr.even'):
            if race.css('.e_date::text').get():
                month = response.xpath("//*[@class='e_date'][text()=\"" + race.css('.e_date::text').get() + "\"]/../preceding-sibling::tr[@class='month-title'][1]/td/text()").get()
                yield {
                    'date': dateparser.parse(month + ' ' + race.css('.e_date::text').get()),
                    'raceLocation': race.css('.e_neutralsite::text').get(), # .split(' ')[1:], # can remove the @ sign if need be
                    'raceDescriptor': race.css('.e_teamname.e_opponent_name::text').get(),
                    'travellingSchool': response.css('meta[property="og:site_name"]::attr(content)').get()
                }