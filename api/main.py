from fastapi import FastAPI
from google.cloud import bigquery

# Create the FastAPI application instance
app = FastAPI()

# Initialize the BigQuery client using the service account credentials
client = bigquery.Client.from_service_account_json("../credentials/credentials.json")

# BigQuery table where the scraped articles are stored
TABLE = "scrapy-489900.scrapydata.articles"

# Create the FastAPI application instance (redeclared here as in the original code)
app = FastAPI()


# Define an API endpoint that allows users to search articles by keyword
# The keyword will be passed as a path parameter
@app.get("/search/{key_word}")
def search_articles(key_word : str):

    # SQL query that searches the keyword in both the headline and the article text
    # REGEXP_CONTAINS with (?i) makes the search case-insensitive
    # \b ensures the keyword is matched as a complete word
    query = f"""
        SELECT headline, author, url, article_text
        FROM `{TABLE}`
        WHERE REGEXP_CONTAINS(headline, r'(?i)\b{key_word}\b') or REGEXP_CONTAINS(article_text, r'(?i)\b{key_word}\b')
    """

    # Execute the query in BigQuery
    results = client.query(query).result()

    # List that will store the formatted articles returned by the API
    articles = []

    # Iterate through the query results
    for row in results:

        # Append each article to the response list
        articles.append({
            "headline": row.headline,
            "author": row.author,
            "url": row.url,
            "text": row.article_text,
        })

    # Return the list of articles as a JSON response
    return articles
