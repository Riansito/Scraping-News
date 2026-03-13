from fastapi import FastAPI
from google.cloud import bigquery

# Create the FastAPI application instance
app = FastAPI()

# Initialize the BigQuery client using the service account credentials
# This allows the API to authenticate and query the BigQuery database
client = bigquery.Client.from_service_account_json("../credentials/credentials.json")

# BigQuery table where the scraped articles are stored
TABLE = "scrapy-489900.scrapydata.articles"


# Define an endpoint that allows users to search for articles by keyword
# The keyword will be passed as a path parameter in the URL
@app.get("/search/{key_word}")
def search_articles(key_word : str):

    # SQL query used to search for the keyword inside the headline or article text
    # REGEXP_CONTAINS is used to perform regex matching in BigQuery
    # (?i) makes the search case-insensitive
    # (^|\W) and (\W|$) ensure that the keyword is matched as a complete word
    # preventing partial matches such as "ai" inside "said"
    query = f"""
        SELECT headline, author, url, article_text
        FROM `{TABLE}`
        WHERE REGEXP_CONTAINS(headline, r'(?i)(^|\\W){key_word}(\\W|$)')
        OR REGEXP_CONTAINS(article_text, r'(?i)(^|\\W){key_word}(\\W|$)')
        """

    # Execute the query in BigQuery and retrieve the results
    results = client.query(query).result()

    # Create a list to store the formatted articles returned by the API
    articles = []

    # Iterate through the query results returned from BigQuery
    for row in results:
        # Append each article as a dictionary to the response list
        articles.append({
            "headline": row.headline,
            "author": row.author,
            "url": row.url,
            "text": row.article_text,
        })

    # Return the list of articles as a JSON response
    return articles
