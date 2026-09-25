import schedule
import time
from src.db import init_db, save_articles
from src.scraper import fetch_rss_data
from src.nlp_pipeline import process_nlp_features

def run_pipeline():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting ETL pipeline...")

    # 1. Fetch
    raw_df = fetch_rss_data()
    print(f"Fetched {len(raw_df)} articles from seeds.")

    if not raw_df.empty:
        # 2. Transform & Score
        processed_df = process_nlp_features(raw_df)

        # 3. Load
        inserted = save_articles(processed_df)
        print(f"Pipeline complete. Inserted {inserted} new articles.")
    else:
        print("No articles fetched.")

if __name__ == "__main__":
    init_db()
    # Run once immediately
    run_pipeline()

    # Schedule Every 30 mins
    schedule.every(30).minutes.do(run_pipeline)

    print("Scheduler running. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(1)