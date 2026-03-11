from google.cloud import bigquery

class BigQueryPipeline:

    def __init__(self):
        self.client = bigquery.Client.from_service_account_json(
            "../credentials/credentials.json"
        )
        self.table_id = "scrapy-489900.scrapydata.articles"
        self.rows = []

    def process_item(self, item, spider):

        self.rows.append({
            "headline": item["headline"],
            "category": item["category"],
            "author": item["author"],
            "published_time": item["published_time"],
            "article_text": item["article_text"],
            "url": item["url"]
        })

        return item

    def close_spider(self, spider):

        errors = self.client.load_table_from_json(
            self.rows,
            self.table_id
        )

        errors.result()

        spider.logger.info("Dados enviados para BigQuery")