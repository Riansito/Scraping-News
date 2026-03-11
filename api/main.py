from fastapi import FastAPI
from google.cloud import bigquery

app = FastAPI()

client = bigquery.Client.from_service_account_json("../credentials/credentials.json")

TABLE = "scrapy-489900.scrapydata.articles"

app = FastAPI()

@app.get("/search/{key_word}")
def search_articles(key_word : str):

    query = f"""
        SELECT headline, author, url, article_text
        FROM `{TABLE}`
        WHERE REGEXP_CONTAINS(headline, r'(?i)\b{key_word}\b') or REGEXP_CONTAINS(article_text, r'(?i)\b{key_word}\b')
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
