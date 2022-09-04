from scrapy.linkextractors import LinkExtractor
import re
from bs4 import BeautifulSoup as BS
from scrapy.spiders import CrawlSpider, Rule
import json
import scrapy


"""def clean_wordlist(wordlist):
	clean_list = []
	for word in wordlist:
		symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "

		for i in range(len(symbols)):
			word = word.replace(symbols[i], '')

		if len(word) > 0:
			clean_list.append(word)
"""

class EmailtrackSpider(CrawlSpider):
	# name of spider
	name = 'ksubot'
	start_urls = [
		'https://www.kennesaw.edu',
		'https://ccse.kennesaw.edu',
		'https://research.kennesaw.edu'
	]
	custom_settings = {
		'USER_AGENT': "KSU-CS4422-IRbot/0.1",
		'CLOSESPIDER_PAGECOUNT': 200,
	}
	rules = [
		Rule(
			LinkExtractor(
				allow_domains=['kennesaw.edu'],
				unique=True
			),
			follow=True,
			callback='parse_items'
		)
	]
	pageid = 0
	regex = r"\b[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\b"

	def parse_items(self, response):
		self.pageid += 1
		entry = {
			'pageid': self.pageid,
			'url': response.url,
			'title': response.xpath('//title/text()').getall()[0],
			'body': ' '.join(BS(response.text).get_text(separator=' ').split()),
		}

		entry['emails'] = re.findall(self.regex, entry['body'])
		yield entry

	def parsed(self, response):
		# emails list of uniqueemail set
		emails = list(self.uniqueemail)
		finalemail = []

		for email in emails:
			if ('.in' in email or '.com' in email or 'info' in email or 'org' in email):
				finalemail.append(email)

		# final unique email ids from geeksforgeeks site
		print('\n'*2)
		print("Emails scraped", finalemail)
		print('\n'*2)


