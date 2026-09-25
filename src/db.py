import duckdb
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/sentiment_monitor.db")

def get_db_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH))

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            article_id VARCHAR PRIMARY KEY,
            title VARCHAR,
            url VARCHAR,
            published_at TIMESTAMP,
            source VARCHAR,
            snippet VARCHAR,
            sentiment_score DOUBLE,
            sentiment_label VARCHAR,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.close()

def save_articles(df: pd.DataFrame):
    if df.empty:
        return 0

    conn = get_db_connection()
    # Insert non-duplicate records based on article_id
    conn.execute("""
        INSERT INTO articles
        SELECT * FROM df
        ON CONFLICT (article_id) DO NOTHING;
    """)
    inserted_rows = conn.changes()
    conn.close()
    return inserted_rows

def load_articles():
    conn = get_db_connection()
    df = conn.execute("SELECT * FROM articles ORDER BY published_at DESC").fetchdf()
    conn.close()
    return df

if __name__ =="__main__":
    init_db()
    print("Database Initialized Successfully.")

