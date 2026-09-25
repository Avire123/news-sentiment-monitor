# 📰 Public Web Event & News Sentiment Monitor

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![DuckDB](https://img.shields.io/badge/DuckDB-1.0%2B-FFF000.svg)](https://duckdb.org/)
[![NLTK](https://img.shields.io/badge/NLTK-VADER-green.svg)](https://www.nltk.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated, end-to-end Data Engineering and Natural Language Processing (NLP) pipeline designed to ingest, process, store, and visualize real-time public web events and news sentiment. 

The system continuously scrapes multi-source RSS news feeds, evaluates headline/snippet sentiment using NLTK's VADER engine, extracts key phrases using Scikit-Learn's TF-IDF vectorization, persists time-series records in an embedded DuckDB database with strict primary-key deduplication, and renders an interactive dashboard via Streamlit.

---

## 🚀 Key Features

- **📡 Live Data Ingestion:** Automated RSS feed parsing (`feedparser`, `BeautifulSoup`) equipped with SHA-256 URL hashing for deterministic primary key generation and record deduplication.
- **🧠 Real-Time NLP & Sentiment Engine:** Computes continuous VADER compound polarity scores (-1.0 to +1.0) and assigns qualitative categorical labels (*Positive*, *Neutral*, *Negative*).
- **🔑 TF-IDF Keyword Extraction:** Dynamically identifies trending phrases and bi-grams across ingested news corpora using `TfidfVectorizer`.
- **⚡ Embedded Time-Series Store:** Powered by DuckDB (`ON CONFLICT (article_id) DO NOTHING`) to guarantee zero write duplicate overhead and instant SQL analytical queries.
- **⏰ Automated Scheduler:** Ingestion runtime (`scheduler.py`) supporting continuous background execution on fixed polling intervals (e.g., every 30 minutes).
- **📊 Interactive Streamlit UI:** Rich analytical web application featuring summary metrics, dynamic charts, and filterable data tables.

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[Web / RSS Feeds] -->|Raw XML/HTML| B[src/scraper.py]
    B -->|Clean Text + SHA256 ID| C[src/nlp_pipeline.py]
    C -->|VADER Scores + TF-IDF Keywords| D[src/db.py]
    D -->|SQL Storage / Deduplication| E[(data/sentiment_monitor.db)]
    E -->|Time-Series Queries| F[app.py - Streamlit Dashboard]
    
    G[scheduler.py] -->|Triggers Loop Every 30m| B
