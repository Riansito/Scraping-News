import scrapy


class GuardianSpider(scrapy.Spider):
    name = "guardian"
    allowed_domains = ["theguardian.com"]
    start_urls = ["https://theguardian.com"]

    def parse(self, response):
        pass
