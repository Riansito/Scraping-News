import scrapy


class GuardianSpider(scrapy.Spider):
    name = "guardian"
    allowed_domains = ["theguardian.com"]
    start_urls = ["https://theguardian.com/au"]

    def parse_article(self, response):
        title = response.meta["title"]
        category = response.meta["category"]
        url = response.meta["url"]
        time = response.meta["time"]
        author = response.css('a[rel="author"]::text').get()
        paragraphs = response.css('div[data-gu-name="body"] p::text').getall()
        article_text = " ".join(paragraphs)
        yield{
            "headline": title, 
            "category": category, 
            "author": author, 
            "published_time": time, 
            "article_text": article_text, 
            "url": url
        }
        
    def parse(self, response):
        articles = response.css("div.dcr-mwwxk")
        for article in articles:
            title = article.css("span.headline-text::text").get()
            category = article.css("h3 div::text").get()
            url = article.css("a::attr(href)").get()
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
