# -*- coding: utf-8 -*-
import scrapy
import re
import logging
import datetime


class KuzebSpider(scrapy.Spider):
    name = 'kuzeb'
    allowed_domains = ['kuzeb.ch']
    start_urls = ['https://www.kuzeb.ch/newsticker.rdf'] # https://kuzeb.ch/veransta.htm']

    date_regex = re.compile(r"(\d{1,2}).(\d{1,2}).(\d{2,4})")


    def parse(self, response):
        """
        @scrapes eventname start_date links venue description
        """
        response.selector.register_namespace('n', 'http://my.netscape.com/rdf/simple/0.9/') 
        response.selector.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns') 
        items = response.xpath('//n:item')
        for item in items:
            title = item.xpath('n:title/text()').get()
            if title is None:
                raise ValueError("Item has no title")
            match = self.date_regex.search(title)
            if match is None:
                logging.warning('WARNING: Event item with title contains no date "' + title + '"')
                continue
            start_date = datetime.date(int(match[3]), int(match[2]), int(match[1]))
            yield {
                'eventname': title,
                'links': [ item.xpath('n:link/text()').get() ],
                'venue': 'Kulturzentrum Bremgarten',
                'start_date': start_date,
                'description': item.xpath('n:description/text()').get()
            }
