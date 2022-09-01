# web scraping framework
import scrapy

# for regular expression
import re

# for selenium request
from scrapy_selenium import SeleniumRequest

# for link extraction
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import json


def get_requests(spider):
	return [SeleniumRequest(url="https://ccse.kennesaw.edu/",
							wait_time=3, screenshot=True,
							callback=spider.parse,
							dont_filter=True
							), SeleniumRequest(
		url="https://www.kennesaw.edu/",
		wait_time=2,
		screenshot=True,
		callback=spider.parse,
		dont_filter=True
	), SeleniumRequest(
		url="https://datascience.kennesaw.edu/",
		wait_time=2,
		screenshot=True,
		callback=spider.parse,
		dont_filter=True
	)
			]


class EmailtrackSpider(scrapy.Spider):
	# name of spider
	name = "KSU-CS4422-IRbot/0.1"

	# to have unique email ids
	uniqueemail = set()

	# start_requests sends request to given https://www.geeksforgeeks.org/
	# and parse function is called
	def start_requests(self):
		for i in range(len(get_requests(self))):
			yield get_requests(self)[i]


	def parse(self, response):
			# this helps to get all links from source code
			links = LxmlLinkExtractor(allow=()).extract_links(response)

			# Finallinks contains links urk
			Finallinks = [str(link.url) for link in links]

			# links list for url that may have email ids
			links = []

			# filtering and storing only needed url in links list
			# pages that are about us and contact us are the ones that have email ids
			for link in Finallinks:
				if ('Contact' in link or 'contact' in link or 'About' in link or 'about' in link or 'CONTACT' in link or 'ABOUT' in link):
					links.append(link)

			# current page url also added because few sites have email ids on there main page
			links.append(str(response.url))

			# parse_link function is called for extracting email ids
			l = links[0]
			links.pop(0)

			# meta helps to transfer links list from parse to parse_link
			yield SeleniumRequest(
				url=l,
				wait_time=2,
				screenshot=True,
				callback=self.parse_link,
				dont_filter=True,
				meta={'links': links}
			)

	def parse_link(self, response):
		# response.meta['links'] this helps to get links list
		links = response.meta['links']
		flag = 0
		emails = []
		count_pages = 0

		# links that contains following bad words are discarded
		bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki', 'linkedin']
		entry = dict.fromkeys(['pageid', 'url', 'title', 'body', 'emails'])

		for word in bad_words:
			# if any bad word is found in the current page url
			# flag is assigned to 1
			if word in str(response.url):
				flag = 1
				break

		# if flag is 1 then no need to get email from
		# that url/page
		if (flag != 1):
			html_text = str(response.text)
			# regular expression used for email id
			email_list = re.findall('\w+@\w+\.{1}\w+', html_text)
			# set of email_list to get unique
			email_list = set(email_list)

			if (len(email_list) != 0):
				count_pages += 1
				for i in email_list:
					emails.append(i)
					# adding email ids to final uniqueemail
					self.uniqueemail.add(i)

		# parse_link function is called till
		# if condition satisfy
		# else move to parsed function
		if (len(links) > 0):
			l = links[0]
			links.pop(0)

			yield SeleniumRequest(
				url=l,
				callback=self.parse_link,
				dont_filter=True,
				meta={'links': links}
			)
		else:
			yield SeleniumRequest(
				url=response.url,
				callback=self.parsed,
				dont_filter=True
			)

		with open('KSU100.json', 'a', encoding='utf-8') as f:
			json.dump(emails, f, ensure_ascii=False, indent=4)
			json.dump("\n"+str(count_pages)+"\n", f, ensure_ascii=False, indent=4)
			json.dump(response.url, f, ensure_ascii=False, indent=4)

		return entry

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


