import scrapy


class GuardianSpider(scrapy.Spider):
    name = "guardian"
    allowed_domains = ["theguardian.com"]
    start_urls = ["https://theguardian.com"]

    def parse(self, response):
        articles = response.css("div.dcr-mwwxk")
        for article in articles:
            title = article.css("span.headline-text::text").get()
            category = article.css("h3 div::text").get()
            url = article.css("a.attr(href)").get()
            time = article.css("time::attr(datetime)").get()

            if(url):
                url = response.urljoin(url)
                yield scrapy.Request(
                    url,
                    callback = self.parse_article,
                    meta = {
                        "title" : title,
                        "category" : category,
                        "url" : url,
                        "time" : time 
                    }
                )
