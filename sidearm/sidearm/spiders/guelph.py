# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import dateparser

class GuelphSpider(scrapy.Spider):
    name = 'guelph'
    allowed_domains = ['http://www.gryphons.ca']
    start_urls = ['http://www.gryphons.ca/schedule.aspx?path=cross']

    def parse(self, response):
        for race in response.css('div.schedule_game'):
            # clean up tournament links
            descriptor_tourney = race.css('.schedule_game_opponent_name>a::text').get()
            descriptor = descriptor_tourney if descriptor_tourney else race.css('.schedule_game_opponent_name>a>span::text').get().strip()
            raceloc_tourney = race.css('.schedule_game_location>span::text').get()
            raceloc = raceloc_tourney.strip() if raceloc_tourney else race.css('.schedule_game_location::text').get().strip()
            date = race.css('.schedule_game_opponent_date::text').get().strip()

            yield {
                'date': dateparser.parse(date), 
                'raceLocation': raceloc,
                'raceDescriptor': descriptor,
                'travellingSchool': response.css('.main-header>h1::text').get()
            }
