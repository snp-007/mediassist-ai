import streamlit as st
import sys

sys.path.append("src")

from article_search import search_articles
from chroma_manager import ChromaManager
from rag_pipeline_groq import RAGPipeline

# ======================
# PAGE CONFIG
# ======================

st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🩺",
    layout="wide"
)

# ======================
# INITIALIZE COMPONENTS
# ======================

vector_db = ChromaManager(
    collection_name="pubmed_articles_filtered"
)

rag = RAGPipeline()

# ======================
# HEADER
# ======================

st.title("🩺 MediAssist AI")
st.subheader("Evidence-Based Healthcare Research Assistant")

# ======================
# SIDEBAR
# ======================

st.sidebar.header("📚 Document Search")

search_term = st.sidebar.text_input(
    "Search PubMed Articles",
    value="intermittent fasting"
)

# ======================
# SEARCH ARTICLES
# ======================

if st.sidebar.button("Search Articles"):

    with st.spinner("Searching articles..."):

        results = search_articles(search_term)

        st.session_state["search_results"] = results

# ======================
# DISPLAY SEARCH RESULTS
# ======================

selected_articles = []

if "search_results" in st.session_state:

    results = st.session_state["search_results"]

    st.sidebar.success(
        f"Found {len(results)} articles"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Select Articles")

    for idx, article in enumerate(results):

        if st.sidebar.checkbox(
            article["title"],
            key=f"article_{idx}"
        ):
            selected_articles.append(article)

# Save selections
st.session_state["selected_articles"] = selected_articles

# ======================
# INGEST ARTICLES
# ======================

if st.sidebar.button("Ingest Selected Articles"):

    selected_articles = st.session_state.get(
        "selected_articles",
        []
    )

    if len(selected_articles) == 0:

        st.sidebar.warning(
            "Please select at least one article."
        )

    else:

        with st.spinner(
            "Ingesting articles into vector store..."
        ):

            added = vector_db.add_selected_documents(
                selected_articles
            )

        st.sidebar.success(
            f"{added} articles ingested successfully."
        )

# ======================
# KNOWLEDGE BASE INFO
# ======================

st.sidebar.info(
    f"Knowledge Base Size: {vector_db.count()} articles"
)

# ======================
# MAIN QUERY AREA
# ======================

st.markdown("---")

question = st.text_input(
    "Ask a Question",
    placeholder="How effective is intermittent fasting for Type 2 Diabetes?"
)

ask_button = st.button(
    "Ask MediAssist AI"
)

# ======================
# GENERATE RESPONSE
# ======================

if ask_button:

    if not question:

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Analyzing evidence and generating answer..."
        ):

            try:

                response = rag.answer_question(
                    question
                )

                st.markdown("## Response")
                st.markdown(response)

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )

# ======================
# FOOTER
# ======================

st.markdown("---")

st.caption(
    "MediAssist AI • Retrieval-Augmented Generation using PubMed, ChromaDB, Groq, and Llama 3"
)