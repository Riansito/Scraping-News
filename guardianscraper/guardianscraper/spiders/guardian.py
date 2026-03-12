import scrapy


# Spider responsible for crawling articles from The Guardian website
class GuardianSpider(scrapy.Spider):

    # Unique name used by Scrapy to run this spider
    name = "guardian"

    # Restrict crawling to this domain
    allowed_domains = ["theguardian.com"]

    # Initial URL where the crawling process starts
    start_urls = ["https://theguardian.com/au"]


    # This method parses the content of each individual article page
    def parse_article(self, response):

        # Retrieve metadata passed from the previous request
        headline = response.meta["headline"]
        category = response.meta["category"]
        url = response.meta["url"]
        time = response.meta["time"]

        # Extract the author's name from the article page
        author = response.css('a[rel="author"]::text').get()

        # Extract all paragraph texts from the article body
        paragraphs = response.css('div[data-gu-name="body"] p::text').getall()

        # Join all paragraphs into a single string representing the full article text
        article_text = " ".join(paragraphs)

        # Yield the structured data as a dictionary item
        yield{
            "headline": headline, 
            "category": category, 
            "author": author, 
            "published_time": time, 
            "article_text": article_text, 
            "url": url
        }
        

    # This method parses the main news page and extracts article links
    def parse(self, response):

        # Select all article containers from the page
        articles = response.css("div.dcr-mwwxk")

        # Iterate through each article block
        for article in articles:

            # Extract article headline
            headline = article.css("span.headline-text::text").get()

            # Extract article category
            category = article.css("h3 div::text").get()

            # Extract article URL
            url = article.css("a::attr(href)").get()

            # Extract publication time
            time = article.css("time::attr(datetime)").get()

            # Ensure the URL exists before creating a request
            if(url):

                # Convert relative URLs into absolute URLs
                url = response.urljoin(url)

                # Send a request to the article page for further parsing
                yield scrapy.Request(
                    url,

                    # Define the callback that will process the article page
                    callback = self.parse_article,

                    # Pass metadata to the next request
                    meta = {
                        "headline" : headline,
                        "category" : category,
                        "url" : url,
                        "time" : time 
                    }
                )
