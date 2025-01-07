import streamlit as st
import requests
import pandas as pd

from utils import truncate_text
from settings import BASE_URL, HEADERS


def get_articles(page: int = 1, page_size: int = 5, language: str = 'ENG'):
    params = {"page": page, "page_size": page_size, "language": language}
    response = requests.get(f"{BASE_URL}/article", headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch articles")
        return {"articles": []}

def get_article_by_id(article_id):
    response = requests.get(f"{BASE_URL}/article/{article_id}/training_data", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch article with ID {article_id}")
        return {"article": {}}

if "page" not in st.session_state:
    st.session_state.page = 1
if "total_pages" not in st.session_state:
    st.session_state.total_pages = 100
if "articles" not in st.session_state:
    st.session_state.articles = get_articles(page=st.session_state.page)

st.title("Articles")

articles = st.session_state.articles

if articles and "articles" in articles:
    df = pd.DataFrame(articles['articles'])
    df['article'] = df['article'].apply(lambda x: truncate_text(x, 50))
    st.table(df)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous Page") and st.session_state.page > 1:
            st.session_state.page -= 1
            st.session_state.articles = get_articles(page=st.session_state.page)
            st.rerun()

    with col2:
        if st.button("Next Page") and st.session_state.page < st.session_state.total_pages:
            st.session_state.page += 1
            st.session_state.articles = get_articles(page=st.session_state.page)
            st.rerun()

    article_ids = df['id'].tolist()
    selected_article_id = st.selectbox("Select an article to view details", article_ids)
    
    st.subheader("Article Details")

    if selected_article_id:
        article_details = get_article_by_id(selected_article_id)
        print(article_details)
        st.write(article_details)
        if article_details and "trainnig_data" in article_details:
            with st.expander(f"Details for Article {selected_article_id}"):
                st.json(article_details['training_data'])