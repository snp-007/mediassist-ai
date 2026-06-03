from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "pubmed_articles.json"


def load_articles():

    with open(
        DATA_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def search_articles(
    search_term,
    limit=20
):

    articles = load_articles()

    results = []

    search_term = search_term.lower()

    for article in articles:

        title = article.get(
            "title",
            ""
        ).lower()

        if search_term in title:

            results.append(article)

        if len(results) >= limit:
            break

    return results