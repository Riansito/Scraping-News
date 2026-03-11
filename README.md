

# News Data Pipeline with Scrapy, BigQuery and FastAPI

This project implements a **data pipeline for news collection, storage and retrieval**.  
The pipeline scrapes news articles from the web, processes the content, stores it in a data warehouse, and exposes an API to query the collected articles.

The main goal of this project is to demonstrate **data engineering concepts**, including data extraction, cleaning, deduplication, storage, and API consumption.

---

# Architecture

The pipeline follows the architecture below:

Website → Scrapy Crawler → Data Cleaning & Filtering → Deduplication → BigQuery → FastAPI → Client

1. News articles are scraped from a website using Scrapy.
2. Only relevant article data is extracted.
3. Articles without required fields are removed.
4. Duplicate articles are filtered based on URL.
5. Clean data is stored in BigQuery.
6. A FastAPI service allows querying the stored articles.

---

# Technologies Used

- Python
- Scrapy
- Google BigQuery
- FastAPI
- Google Cloud Client Library
- JSON
- SQL

---

# Data Pipeline Flow

## 1. Data Extraction (Scrapy)

The crawler uses **Scrapy** to navigate through news pages and collect article information.

Each article page is parsed to extract the following fields:

- Headline
- Category
- Author
- Publication time
- Article text
- URL

The spider collects the paragraphs of the article and joins them into a single text field.

---

## 2. Data Cleaning

During the pipeline processing stage, the crawler ensures that the article contains the minimum required fields.

Articles are removed if they do not contain:

- headline
- article text
- url

This guarantees that only valid articles are processed and stored.

---

## 3. Duplicate Detection

Before inserting the data into the database, the pipeline verifies whether the article already exists.

When the spider starts:

1. The pipeline queries BigQuery to retrieve all stored URLs.
2. These URLs are stored in a Python `set`.

During processing:

- If the URL already exists, the article is dropped.
- If the URL is new, the article is added to the batch to be inserted.

This ensures that the dataset does not contain duplicated articles.

---

## 4. Data Storage

Cleaned articles are inserted into **Google BigQuery**.

The following schema is used:

| Field | Description |
|-----|-----|
| headline | Article title |
| category | News category |
| author | Article author |
| published_time | Publication time |
| article_text | Full article text |
| url | Article URL |

Data is inserted in **batch mode when the spider finishes running**.

---

# API Layer

The project also provides a **REST API built with FastAPI** to query stored articles.

The API reads data directly from BigQuery.

---

<img width="1376" height="768" alt="Gemini_Generated_Image_l7h7f6l7h7f6l7h7" src="https://github.com/user-attachments/assets/056e65ff-d532-4409-91b7-72ef3dbd13cf" />


# API Endpoints

## Search Articles

Search for articles containing a specific keyword.

```

GET /search/{keyword}

```

Example:

```

GET /search/ai

````

The API searches the article text and returns related articles.

### Response

```json
[
  {
    "headline": "Example Article Title",
    "author": "John Doe",
    "url": "https://example.com/article",
    "article_text": "Full article text..."
  }
]
````

---

# Project Structure

```
project/
│
├── api/
│   └── main.py
│
├── credentials/
│   └── credentials.json
│
├── guardianscraper/
│   ├── scrapy.cfg
│   └── guardianscraper/
│       ├── spiders/
│       │   └── guardian.py
│       ├── items.py
│       ├── middlewares.py
│       ├── pipelines.py
│       └── settings.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---


# How to Run the Project

## 1 Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2 Run the crawler

```bash
scrapy crawl news_spider
```

This will:

* collect articles
* clean the data
* remove duplicates
* store the data in BigQuery

---

## 3 Run the API

```bash
uvicorn main:app --reload
```

API will be available at:

```
http://localhost:8000
```

---

# Example API Query

```
http://localhost:8000/search/ai
```

Returns articles related to **AI**.

---

# Data Engineering Concepts Demonstrated

This project demonstrates several important concepts in data engineering:

* Web scraping pipelines
* Data cleaning and validation
* Deduplication strategies
* Data warehouse ingestion
* Batch data loading
* API data access layer
* Keyword-based text search

---

# Author


Rian Freires da Costa Silva

