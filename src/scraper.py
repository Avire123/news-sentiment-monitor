import feedparser
import requests
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
import pandas as pd

RSS_FEEDS = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
    "VentureBeat": "https://feeds.feedburner.com/venturebeat/Sgit"
}

def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def generate_article_id(url: str) -> str:
    return hashlib.md5(url.encode('utf-8')).hexdigest()

def fetch_rss_data() -> pd.DataFrame:
    articles = []  # <--- MUST BE INITIALIZED HERE BEFORE THE LOOP
    
    for source, feed_url in RSS_FEEDS.items():
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", entry.get("description", ""))
            cleaned_snippet = clean_html(summary)[:500]
            
            # Parse timestamp safely
            published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")
            if published_parsed:
                published_at = datetime(*published_parsed[:6])
            else:
                published_at = datetime.utcnow()
                
            article_id = generate_article_id(link)
            
            articles.append({
                "article_id": article_id,
                "title": title,
                "url": link,
                "published_at": published_at,
                "source": source,
                "snippet": cleaned_snippet
            })
            
    return pd.DataFrame(articles)

if __name__ == "__main__":
    print("Fetching RSS feeds...")
    df = fetch_rss_data()
    print(f"Successfully fetched {len(df)} articles!\n")
    if not df.empty:
        print(df[["source", "title", "published_at"]].head())
