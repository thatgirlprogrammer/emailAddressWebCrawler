import scrapy


class EmailtrackSpider(scrapy.Spider):
    name = "ksuEmail"

    start_urls = [
        'https://www.kennesaw.edu'
    ]

    def parse(self, response):
        page = response.url
        filename = 'ksuEmail.html'
        with open(filename, 'wb') as f:
            f.write(response.body)






