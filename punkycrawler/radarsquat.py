# -*- coding: utf-8 -*-
import scrapy
import json

# API INFO ON WEBSITE:  https://radar.squat.net/api#api`
# FORMAT SPECIFICATION: https://0xacab.org/radar/drupal-make/-/wikis/api/1.2/notes


class RadarsquatSpider(scrapy.Spider):
    name = 'radarsquat'
    allowed_domains = ['radar.squat.net']
    start_urls = [
        'https://radar.squat.net/api/1.2/search/events.json'
        + '?language=de'
        + '&fields=body,date_time,image,link,title,offline'
        + '&facets[country][]=CH'
        + '&facets[category][]=music-concert'
        # + '&facets[category][]=party'
        # + '&facets[tag][]=konzert-0'
        + '&facets[tag][]=punk-hardcore-crust'
        # + '&facets[tag][]=punk'
        # + '&facets[tag][]=music'
        # + '&facets[tag][]=hardcore'
        # + '&facets[tag][]=metal'
        # + '&facets[tag][]=crust'
        # + '&facets[date][]=1579370400'
    ]

    def parse_venue(self, result):
        return [
            offline['title']
            for offline in result['offline']
            if offline['resource'] == "location"
        ][0]

    def parse(self, response):
        """
        @scrapes eventname start_date links venue description
        """
        jsonresponse = json.loads(response.body_as_unicode())
        results = jsonresponse['result']

        for id, result in results.items():
            for event_times in result['date_time']:
                yield {
                    'eventname': result['title'],
                    'links': [ link['url'] for link in result['link'] ],
                    'start_date': event_times['time_start'],
                    'end_date': event_times['time_start'],
                    'image': result['image'],
                    'venue': self.parse_venue(result),
                    'description': result['body']['value']
                }

