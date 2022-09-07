import re

import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.settings.default_settings import CLOSESPIDER_PAGECOUNT
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils import spider
import json


class EmailtrackSpider(CrawlSpider): # use CrawlSpider
    name = "quotes"
    allowed_domains = ['kennesaw.edu']
    start_urls = ['https://www.kennesaw.edu/']
    uniqueemail = set()


    rules = [
        Rule(LinkExtractor(), callback='parse', follow=True)
    ]

    custom_settings = {

        'CLOSESPIDER_PAGECOUNT' : 100
    }









    def parse(self, response):


        entry = dict.fromkeys(['pageid', 'url','title','body','emails'])
        entry['pageid'] = 0
        entry['url'] = response.url
        #entry['body'] = response.css('boby::text').getall()
        entry['body'] = response.xpath('//body//p//text()').extract()
        #entry['body'] = response.css('::text').get()
        entry['title'] = response.css('title::text').get()
        entry['emails'] = re.findall(r'[\w\.-]+@[\w\.-]+[\.edu]', response.text)


        yield entry











        #emails = response(self)
       ## email = []

        #word = re.findall(r'[\words]]', response.text)
        #e = re.findall(r'[\w\.-]+@[\w\.-]+[\.edu]', response.text)

        #if('.edu' in e or '.com' in e or '.in' in e):
        #email.append(e)
        #yield
        #print(e)


        #print(word)
    #/print(response.url)


##    def parse(self, response):
  #      for quote in response.css('div.quote'):
   ##            'text': quote.css('span.text::text').get(),
     #           'author': quote.css('small.author::text').get(),
      #          'tags': quote.css('div.tags a.tag::text').getall(),
       #     }


            
        
    
