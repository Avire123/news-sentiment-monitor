import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Download VADER lexicon if not already present
try:
    sia = SentimentIntensityAnalyzer()
except LookupError:
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> dict:
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
        
    return {"score": compound, "label": label}

def process_nlp_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    
    # Combined text for sentiment evaluation
    df['combined_text'] = df['title'].fillna('') + ". " + df['snippet'].fillna('')
    
    sentiment_results = df['combined_text'].apply(analyze_sentiment)
    df['sentiment_score'] = [r['score'] for r in sentiment_results]
    df['sentiment_label'] = [r['label'] for r in sentiment_results]
    
    df.drop(columns=['combined_text'], inplace=True)
    return df

def extract_trending_keywords(corpus: list, top_n: int = 15) -> pd.DataFrame:
    if not corpus:
        return pd.DataFrame(columns=['keyword', 'score'])
        
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(corpus)
    scores = tfidf_matrix.sum(axis=0).A1
    keywords = vectorizer.get_feature_names_out()
    
    result_df = pd.DataFrame({'keyword': keywords, 'score': scores})
    return result_df.sort_values(by='score', ascending=False)