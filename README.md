📰 Public Web Event & News Sentiment Monitor
An automated end-to-end Data Engineering and Natural Language Processing (NLP) pipeline designed to ingest, process, store, and visualize real-time web news and public events.

The system continuously scrapes multi-source RSS feeds, evaluates headline/snippet sentiment using NLTK's VADER model, extracts trending themes using Scikit-Learn's TF-IDF vectorization, stores time-series data in DuckDB with deduplication, and serves an interactive dashboard built with Streamlit.

🚀 Features
📡 Automated Data Ingestion: Scrapes live RSS news feeds using feedparser and BeautifulSoup with SHA-256 URL hashing for strict primary key deduplication.

🧠 Real-Time NLP Sentiment Analysis: Computes continuous compound polarity scores (-1.0 to +1.0) and assigns qualitative labels (Positive, Neutral, Negative) using NLTK VADER.

⚡ High-Performance SQL Engine: Implements an embedded time-series database architecture powered by DuckDB (ON CONFLICT DO NOTHING).

⏰ Background Pipeline Scheduler: Runs continuous background ingestion loops using Python's schedule library.

📊 Interactive Streamlit UI: Visualizes sentiment distributions, real-time metrics, and filterable article tables.

🏗️ Architecture Overview
Plaintext
  [ Web / RSS Feeds ]
           │
           ▼
  ┌─────────────────┐
  │   src/scraper   │  ──► Parses HTML & cleans content
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ src/nlp_pipeline│  ──► Runs VADER Sentiment & TF-IDF Keyphrase Extraction
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │     src/db      │  ──► Insert & Deduplicate via SHA-256 Hashes
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ data/monitor.db │ (DuckDB Embedded Database)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │     app.py      │ (Interactive Streamlit Analytics Dashboard)
  └─────────────────┘
📂 Repository Structure
Plaintext
news-sentiment-monitor/
├── data/
│   └── sentiment_monitor.db  # DuckDB local time-series database
├── src/
│   ├── __init__.py
│   ├── db.py                 # DuckDB connection & schema operations
│   ├── nlp_pipeline.py       # VADER sentiment analysis & TF-IDF extraction
│   └── scraper.py            # RSS parsing & web cleaning logic
├── app.py                    # Streamlit web visualization interface
├── scheduler.py              # Ingestion engine & automated scheduler
├── requirements.txt          # Python dependencies
└── README.md
🛠️ Tech Stack & Dependencies
Language: Python 3.10+

Data Processing: Pandas, NumPy

NLP & ML: NLTK (VADER), Scikit-Learn (TfidfVectorizer)

Storage: DuckDB

Web & Ingestion: Feedparser, BeautifulSoup4, Requests

Visualization & Framework: Streamlit, Plotly

Automation: Schedule

⚡ Quickstart Guide
1. Clone the Repository
Bash
git clone https://github.com/YOUR_GITHUB_USERNAME/news-sentiment-monitor.git
cd news-sentiment-monitor
2. Set Up Virtual Environment & Install Dependencies
Bash
# Windows (Git Bash / PowerShell)
python -m venv venv
source venv/Scripts/activate   # Powershell: .\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
3. Run the Automated Ingestion Scheduler
To trigger an initial data pull and keep the 30-minute automated ingestion loop running:

Bash
python scheduler.py
4. Launch the Streamlit Dashboard
Open a second terminal window, activate the environment, and start the app:

Bash
streamlit run app.py
The dashboard will open automatically at http://localhost:8501.

📊 Database Schema
SQL
CREATE TABLE articles (
    article_id VARCHAR PRIMARY KEY,   -- SHA-256 hash of article URL
    title VARCHAR,                    -- Headline text
    url VARCHAR,                      -- Source URL
    published_at TIMESTAMP,           -- Publication timestamp
    source VARCHAR,                   -- Feed publisher source
    snippet VARCHAR,                  -- Cleaned article summary
    sentiment_score DOUBLE,           -- VADER compound score (-1.0 to +1.0)
    sentiment_label VARCHAR,          -- Positive, Neutral, or Negative
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
🤝 Contributing
Contributions, suggestions, and pull requests are welcome! Feel free to open an issue if you encounter bugs or have feature requests.

📄 License
Distributed under the MIT License. See LICENSE for more details.
