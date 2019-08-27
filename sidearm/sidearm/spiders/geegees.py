# -*- coding: utf-8 -*-
import scrapy
import dateparser

class GeegeesSpider(scrapy.Spider):
    name = 'geegees'
    start_urls = ['https://equipes.geegees.ca/sports/xc/2019-20/schedule']
    
    def parse(self, response):
        date, race_location, race_descriptor = (False,False,False)

        for tr in response.css('.schedule-content table tr'):
            # this is kind of hacky, but since there isn't one parent td, div, etc containing all the data
            #   on a specific competition date, I'm collecting individual rows under the assumption that the 
            #   dates, locations, and descriptions will be in order. Once we have a value for each, yeild the data.
            date_selector = tr.css('.e_date::text')
            race_location_selector = tr.css('.e_notes::text')
            race_descriptor_selector = tr.css('.e_opponent_name::text')

            if date_selector.get():
                date = date_selector.get()

            if race_location_selector.get():
                race_location = race_location_selector.get()

            if race_descriptor_selector.get():
                race_descriptor = race_descriptor_selector.get()

            if date and race_location and race_descriptor:
                yield {
                    'date': dateparser.parse(date),
                    'raceLocation': race_location,
                    'raceDescriptor': race_descriptor,
                    'travellingSchool': 'uOttawa Gee-Gees'
                }

                # Remember to reset the collectors after a full set of competition details is found
                date, race_location, race_descriptor = (False,False,False)