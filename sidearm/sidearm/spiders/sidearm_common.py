# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import dateparser

class SidearmCommonSpider(scrapy.Spider):
    name = 'sidearm_common'
    start_urls = ['https://gospartans.ca/schedule.aspx?path=mcross'
    'https://huskies.usask.ca/schedule.aspx?path=mcross',
    'https://gothunderbirds.ca/schedule.aspx?path=xc',
    'https://mcgillathletics.ca/schedule.aspx?path=cross',
    'https://gogaelsgo.com/schedule.aspx?path=cross',
    'https://varsityblues.ca/schedule.aspx?path=cross',
    'https://athletics.uwaterloo.ca/schedule.aspx?path=mcross',
    'https://westernmustangs.ca/schedule.aspx?path=mcross',
    'https://golancers.ca/schedule.aspx?path=cross',
    'https://yorkulions.ca/schedule.aspx?path=xcountry',
    'https://gobadgers.ca/schedule.aspx?path=mcross',
    'https://marauders.ca/schedule.aspx?path=mcross',
    ]

    def parse(self, response):
        for race in response.css('li.sidearm-schedule-game'):
            # clean up text-only race descriptions for non hyperlinked races
            descriptor_href = race.css('.sidearm-schedule-game-opponent-name>a::text').get()
            descriptor = descriptor_href if descriptor_href else race.css('.sidearm-schedule-game-opponent-name::text').get().strip()
            date = race.css('.sidearm-schedule-game-opponent-date>span::text').get()
            yield {
                'date': dateparser.parse(date),
                'raceLocation': race.css('.sidearm-schedule-game-location>span::text').get(),
                'raceDescriptor': descriptor,
                'travellingSchool': response.css('meta[property="og:site_name"]::attr(content)').get()
            }
