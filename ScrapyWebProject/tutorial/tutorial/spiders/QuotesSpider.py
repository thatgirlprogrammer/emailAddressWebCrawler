# web scraping framework
from scrapy.linkextractors import LinkExtractor

# for regular expression
import re

# for selenium request
from bs4 import BeautifulSoup as BS
from scrapy.spiders import CrawlSpider, Rule
#from scrapy_selenium import SeleniumRequest

# for link extraction
#from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import json
import scrapy


def clean_wordlist(wordlist):
	clean_list = []
	for word in wordlist:
		symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "

		for i in range(len(symbols)):
			word = word.replace(symbols[i], '')

		if len(word) > 0:
			clean_list.append(word)
	# create_dictionary(clean_list)



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
		'CLOSESPIDER_PAGECOUNT': 100,
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
	#
	# def get_requests(self):
	# 	return [SeleniumRequest(url="https://ccse.kennesaw.edu/",
	# 							wait_time=2, screenshot=True,
	# 							callback=self.parse,
	# 							dont_filter=True
	# 							), SeleniumRequest(
	# 		url="https://www.kennesaw.edu/",
	# 		wait_time=2,
	# 		screenshot=True,
	# 		callback=self.parse,
	# 		dont_filter=True
	# 	), SeleniumRequest(
	# 		url="https://datascience.kennesaw.edu/",
	# 		wait_time=2,
	# 		screenshot=True,
	# 		callback=self.parse,
	# 		dont_filter=True
	# 	)
	# 			]
	#
	# # start_requests sends request to given https://www.geeksforgeeks.org/
	# # and parse function is called
	# def start_requests(self):
	# 	for i in range(len(self.get_requests())):
	# 		yield self.get_requests()[i]
	#
	# def parse(self, response):
	# 		# this helps to get all links from source code
	# 		links = LxmlLinkExtractor(allow=()).extract_links(response)
	#
	# 		# Finallinks contains links urk
	# 		Finallinks = [str(link.url) for link in links]
	#
	# 		# links list for url that may have email ids
	# 		links = []
	#
	# 		# filtering and storing only needed url in links list
	# 		# pages that are about us and contact us are the ones that have email ids
	# 		for link in Finallinks:
	# 			links.append(link)
	#
	# 		# current page url also added because few sites have email ids on there main page
	# 		links.append(str(response.url))
	#
	# 		# parse_link function is called for extracting email ids
	# 		l = links[0]
	# 		links.pop(0)
	#
	# 		# meta helps to transfer links list from parse to parse_link
	# 		yield SeleniumRequest(
	# 			url=l,
	# 			wait_time=2,
	# 			screenshot=True,
	# 			callback=self.parse_link,
	# 			dont_filter=True,
	# 			meta={'links': links}
	# 		)
	#
	# def parse_link(self, response):
	# 	# response.meta['links'] this helps to get links list
	# 	links = response.meta['links']
	# 	flag = 0
	# 	emails = []
	# 	wordlist = []
	# 	count_pages = 0
	# 	entry = dict.fromkeys(['pageid', 'url', 'title', 'body', 'emails'])
	#
	# 	# if flag is 1 then no need to get email from
	# 	# that url/page
	# 	if flag != 1:
	# 		html_text = str(response.text)
	# 		# regular expression used for email id
	# 		email_list = re.findall('\w+@\w+\.{1}\w+', html_text)
	#
	# 		if len(email_list) != 0:
	# 			count_pages += 1
	# 			for i in email_list:
	# 				emails.append(i)
	# 				if i not in self.email_freq:
	# 					self.email_freq.update({i: 1})
	# 				else:
	# 					self.email_freq[i] += 1
	#
	# 	# self.get_word_frequencies(links, wordlist)
	#
	# 	if len(links) > 0:
	# 		l = links[0]
	# 		links.pop(0)
	#
	# 		yield SeleniumRequest(
	# 			url=l,
	# 			callback=self.parse_link,
	# 			dont_filter=True,
	# 			meta={'links': links}
	# 		)
	# 	else:
	# 		yield SeleniumRequest(
	# 			url=response.url,
	# 			callback=self.parsed,
	# 			dont_filter=True
	# 		)
	#
	# 	print(self.word_freq)
	# 	with open('KSU100.json', 'w', encoding='utf-8') as f:
	# 		json.dump(self.email_freq, f, ensure_ascii=False, indent=4)
	# 	return entry

	# def get_word_frequencies(self, links, wordlist):
	# 	if len(links) > 0:
	# 		source_code = requests.get(links[0]).text
	# 		soup = BeautifulSoup(source_code, 'html.parser')

			# for each_text in soup.findAll('div', {'class': 'entry-content'}):
			# 	content = each_text.text
			# 	words = content.lower().split()
			# 	for word in words:
			# 		wordlist.append(word)
			#
			# 	for word in wordlist:
			# 		symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "
			#
			# 		for i in range(len(symbols)):
			# 			word = word.replace(symbols[i], '')
			#
			# 		clean_list = []
			# 		if len(word) > 0:
			# 			clean_list.append(word)
			#
			# 		for word in clean_list:
			# 			if word in self.word_freq:
			# 				self.word_freq[word] += 1
			# 			else:
			# 				self.word_freq[word] = 1

	def parsed(self, response):
		# emails list of uniqueemail set
		emails = list(self.uniqueemail)
		finalemail = []

		for email in emails:
			# avoid garbage value by using '.in' and '.com'
			# and append email ids to finalemail
			if ('.in' in email or '.com' in email or 'info' in email or 'org' in email):
				finalemail.append(email)

		# final unique email ids from geeksforgeeks site
		print('\n'*2)
		print("Emails scraped", finalemail)
		print('\n'*2)


