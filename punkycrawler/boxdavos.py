# -*- coding: utf-8 -*-
import scrapy
import re
import datetime


class BoxdavosSpider(scrapy.Spider):
    name = 'boxdavos'
    allowed_domains = ['http://boxdavos.ch']
    start_urls = ['http://boxdavos.ch/konzerte.html']

    date_regex = re.compile(r"(\d{1,2}).(\d{1,2}).(\d{2,4})")

    def get_bandlinks(self, bandlinks, band):
        return [
            link.xpath('@href').get()
            for link in bandlinks
            if link.xpath('text()').get().strip() == band
        ]


    def parse(self, response):
        texts = response.xpath('//body//table//th//div/div[@class="Stil27"]//text()')
        bandlinks = response.xpath('//body//table//th//div/div[@class="Stil27"]//a')

        event = {}
        for text_node in texts:
            text = text_node.get()
            if text is None:
                continue
            text = text.strip()
            if text == '':
                continue
            if text == "events":
                continue

            # a new date signifies a new event
            match  = self.date_regex.search(text)
            if match is not None:
                if event != {}:
                    yield event

                start_date = datetime.date(int(match[3]), int(match[2]), int(match[1]))
                event = {
                    'eventname': 'Konzert ',
                    'venue': 'Box Davos',
                    'start_date': start_date,
                    'links': self.start_urls,
                }
            else:
                # add bands to event
                event['eventname'] += text + ' '
                event['links'] = event['links'] + self.get_bandlinks(bandlinks, text)


        yield event
