from google.cloud import bigquery
from scrapy.exceptions import DropItem

class BigQueryPipeline:

    def __init__(self):
        # Initialize the BigQuery client using the service account credentials
        self.client = bigquery.Client.from_service_account_json(
            "../credentials/credentials.json"
        )

        # Full table identifier in BigQuery (project.dataset.table)
        self.table_id = "scrapy-489900.scrapydata.articles"

        # Temporary list used to batch rows before sending them to BigQuery
        self.rows = []

        # Set used to store URLs that already exist in the database
        self.existing_urls = set()

    def open_spider(self, spider):

        # Query BigQuery to retrieve all existing article URLs
        # This will be used to prevent inserting duplicates
        query = f"SELECT url FROM `{self.table_id}`"

        # Execute the query and get the results
        result = self.client.query(query).result()

        # Store all existing URLs in a Python set for fast lookup
        self.existing_urls = {row.url for row in result}

        # Log how many URLs were loaded from the database
        spider.logger.info(f"{len(self.existing_urls)} URLs carregadas do banco")

    def process_item(self, item, spider):
        # Retrieve fields from the scraped item
        article_text = item.get("article_text", "")
        headline = item.get("headline", "")
        url = item.get("url", "")

        # Validate required fields
        # Articles without headline, text or URL are discarded
        if not article_text.strip() or not headline.strip() or not url.strip():
            raise DropItem("Artigo incompleto removido")
        
        # Check if the article URL already exists in the database
        # If it exists, drop the item to avoid duplicates
        if url in self.existing_urls:
            raise DropItem("Artigo repitido!")
        
        # Add the article data to the batch list
        # These rows will be inserted into BigQuery when the spider finishes
        self.rows.append({
            "headline": item["headline"],
            "category": item["category"],
            "author": item["author"],
            "published_time": item["published_time"],
            "article_text": item["article_text"],
            "url": item["url"]
        })

        # Add the new URL to the set to prevent duplicates during the same crawl execution
        self.existing_urls.add(url)

        return item

    def close_spider(self, spider):

        # Load all collected rows into BigQuery as a batch insert
        errors = self.client.load_table_from_json(
            self.rows,
            self.table_id
        )

        # Wait for the job to finish
        errors.result()

        # Log confirmation that the data was successfully sent to BigQuery
        spider.logger.info("Dados enviados para BigQuery")