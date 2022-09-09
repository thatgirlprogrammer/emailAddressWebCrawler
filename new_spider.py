import re

import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.settings.default_settings import CLOSESPIDER_PAGECOUNT
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils import spider
import json

# predefining spider
class EmailtrackSpider(CrawlSpider): # use CrawlSpider
    name = "quotes"
    allowed_domains = ['kennesaw.edu']
    start_urls = ['https://www.kennesaw.edu/',
                  "https://ccse.kennesaw.edu",
                  "https://research.kennesaw.edu"]
    uniqueemail = set()


    rules = [
        Rule(LinkExtractor(), callback='parse', follow=True)
    ]

    custom_settings = {

        'CLOSESPIDER_PAGECOUNT' : 400
    }

    pageid = 0


    def parse(self, response):
        self.pageid += 1

        entry = dict.fromkeys(['pageid', 'url','title','body','emails'])
        entry['pageid'] = self.pageid
        entry['url'] = response.url
        #entry['body'] = response.css('boby::text').getall()
        entry['body'] = response.xpath('//body//p//text()').extract()
        #entry['body'] = response.css('::text').get()
        entry['title'] = response.css('title::text').get()
        entry['emails'] = re.findall(r'[\w\.-]+@[\w\.-]+[\.edu]', response.text)
        yield entry











        
    
