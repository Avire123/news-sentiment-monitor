import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.db import init_db, load_articles
from src.nlp_pipeline import extract_trending_keywords

st.set_page_config(page_title="News Sentiment Monitor", layout="wide")

init_db()

st.title(" Public Web Event & News Sentiment Monitor")

# Refresh button
if st.sidebar.button("Refresh Data"):
    st.rerun()

df = load_articles()

if df.empty:
    st.warning("No data found in DuckDB. Run `python scheduler.py` to ingest initial data.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter Options")
sources = st.sidebar.multiselect("Select Sources", options=df["source"].unique(), default=df["source"].unique())
search_query = st.sidebar.text_input("Filter by Keyword", "")

# Apply Filters
filtered_df = df[df["source"].isin(sources)].copy()
if search_query:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_query, case=False, na=False) |
        filtered_df["snippet"].str.contains(search_query, case=False, na=False)
    ]

# Top Metrics
col1, col2, col3 = st.columns(3)
avg_sentiment = filtered_df["sentiment_score"].mean() if not filtered_df.empty else 0.0

col1.metric("Total Articles", len(filtered_df))
col2.metric("Average Sentiment Score", f"{avg_sentiment:.2f}")
col3.metric("Positive Coverage Ratio", f"{(filtered_df['sentiment_label'] == 'Positive').mean() * 100:.1f}%" if not filtered_df.empty else "0%")

st.markdown("---")

# Visualizations
c1, c2 = st.columns([1, 2])

with c1:
    st.subheader("Sentiment Distribution")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_sentiment,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [-1.0, 1.0]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-1.0, -0.05], 'color': "lightcoral"},
                {'range': [-0.05, 0.05], 'color': "lightgray"},
                {'range': [0.05, 1.0], 'color': "lightgreen"}
            ]
        }
    ))
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

with c2:
    st.subheader("Sentiment Trendline Over Time")
    filtered_df["published_date"] = pd.to_datetime(filtered_df["published_at"]).dt.date
    trend_df = filtered_df.groupby("published_date")["sentiment_score"].mean().reset_index()
    fig_trend = px.line(trend_df, x="published_date", y="sentiment_score", markers=True, range_y=[-1, 1])
    fig_trend.update_layout(height=300)
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# Keyword Frequency / Trending
st.subheader("Trending Keywords (TF-IDF)")
if not filtered_df.empty:
    corpus = (filtered_df["title"].fillna('') + " " + filtered_df["snippet"].fillna('')).tolist()
    kw_df = extract_trending_keywords(corpus)
    fig_kw = px.bar(kw_df, x="score", y="keyword", orientation="h", title="Top Keywords")
    fig_kw.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_kw, use_container_width=True)

# Feed Table
st.subheader("Latest Coverage Feed")
st.dataframe(
    filtered_df[["published_at", "source", "title", "sentiment_score", "sentiment_label", "url"]],
    use_container_width=True
)