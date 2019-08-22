# -*- coding: utf-8 -*-
import scrapy


class XcSidearmSpider(scrapy.Spider):
    name = 'xc_sidearm'
    allowed_domains = ['queens']
    start_urls = ['https://gogaelsgo.com/schedule.aspx?path=cross']

    def parse(self, response):
        for race in response.css('li.sidearm-schedule-game'):
            yield {
                'date': race.css('.sidearm-schedule-game-opponent-date>span::text').get()
            }
