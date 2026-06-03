from pathlib import Path
import chromadb

from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)

class ChromaManager:

    def __init__(
        self,
        collection_name="pubmed_articles"
    ):

        BASE_DIR = Path(__file__).resolve().parent.parent

        db_path = str(
            BASE_DIR / "chroma_db"
        )

        self.client = chromadb.PersistentClient(
            path=db_path
        )

        self.embedding_function = (
            SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    def add_documents(self, articles):

        documents = []
        ids = []
        metadatas = []

        for article in articles:

            abstract_text = " ".join(
                article["abstract"].values()
            )

            document = f"""
            Title: {article['title']}

            Abstract:
            {abstract_text}
            """

            documents.append(document)

            ids.append(article["pmid"])

            metadatas.append(
                {
                    "journal": article["journal"],
                    "publication_date": article["publication_date"]
                }
            )

        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

        print(f"{len(documents)} documents added")

    def retrieve(
        self,
        query,
        n_results=5
    ):

        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
    
    def count(self):

        return self.collection.count()
    
    def add_selected_documents(self, articles):

        documents = []
        ids = []
        metadatas = []

        for article in articles:

            abstract_text = " ".join(
                article.get("abstract", {}).values()
            )

            document = f"""
    Title: {article['title']}

    Abstract:
    {abstract_text}
    """

            documents.append(document)

            ids.append(article["pmid"])

            metadatas.append(
                {
                    "journal": article.get(
                        "journal",
                        "Unknown"
                    ),
                    "publication_date": article.get(
                        "publication_date",
                        "Unknown"
                    )
                }
            )

        existing_ids = set()

        try:
            existing = self.collection.get()

            existing_ids = set(
                existing["ids"]
            )

        except:
            pass

        new_docs = []
        new_ids = []
        new_meta = []

        for doc, doc_id, meta in zip(
            documents,
            ids,
            metadatas
        ):

            if doc_id not in existing_ids:

                new_docs.append(doc)
                new_ids.append(doc_id)
                new_meta.append(meta)

        if len(new_docs) > 0:

            self.collection.add(
                documents=new_docs,
                ids=new_ids,
                metadatas=new_meta
            )

        return len(new_docs)