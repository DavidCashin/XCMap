# -*- coding: utf-8 -*-
import scrapy


class XcSidearmSpider(scrapy.Spider):
    name = 'xc_sidearm'
    # TODO: some sites have old sidearm versions, don't scrape well
    start_urls = ['https://gogaelsgo.com/schedule.aspx?path=cross',
    'https://varsityblues.ca/schedule.aspx?path=cross',
    'https://athletics.uwaterloo.ca/schedule.aspx?path=mcross',
    'https://westernmustangs.ca/schedule.aspx?path=mcross',
    'https://golancers.ca/schedule.aspx?path=cross',
    'https://yorkulions.ca/schedule.aspx?path=xcountry',
    'https://gobadgers.ca/schedule.aspx?path=mcross',
    # 'http://www.gryphons.ca/schedule.aspx?path=cross'
    'https://marauders.ca/schedule.aspx?path=mcross',
    # 'https://equipes.geegees.ca/sports/xc/2019-20/schedule'
    ]

    def parse(self, response):
        for race in response.css('li.sidearm-schedule-game'):
            # clean up text-only race descriptions for non hyperlinked races
            descriptor_href = race.css('.sidearm-schedule-game-opponent-name>a::text').get()
            descriptor = descriptor_href if descriptor_href else ' '.join(race.css('.sidearm-schedule-game-opponent-name::text').get().split())

            yield {
                'date': race.css('.sidearm-schedule-game-opponent-date>span::text').get(),
                'raceLocation': race.css('.sidearm-schedule-game-location>span::text').get(),
                'raceDescriptor': descriptor,
                'travellingSchool': response.css('meta[property="og:site_name"]::attr(content)').get()
            }
