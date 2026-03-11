from fastapi import FastAPI
from google.cloud import bigquery

app = FastAPI()

client = bigquery.Client.from_service_account_json("../credentials/credentials.json")

TABLE = "scrapy-489900.scrapydata.articles"

app = FastAPI()

@app.get("/search")
def search_articles():

    query = f"""
        SELECT headline, author, url, article_text
        FROM `{TABLE}`
        LIMIT 5
    """

    results = client.query(query).result()

    articles = []

    for row in results:
        articles.append({
            "headline": row.headline,
            "author": row.author,
            "url": row.url,
            "text": row.article_text,
            
        })

    return articles
