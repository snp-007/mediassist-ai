from chroma_manager import ChromaManager
from llm import LlamaModel


class RAGPipeline:

    def __init__(
        self,
        collection_name="pubmed_articles_filtered"
    ):
        self.vector_db = ChromaManager(
            collection_name=collection_name
        )

        self.llm = LlamaModel()

    def retrieve_context(
        self,
        query,
        n_results=3
    ):
        """
        Retrieve the most relevant documents from ChromaDB.
        """

        results = self.vector_db.retrieve(
            query=query,
            n_results=n_results
        )

        context = ""
        sources = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        for doc, metadata in zip(documents, metadatas):

            context += doc
            context += "\n\n"

            journal = metadata.get(
                "journal",
                "Unknown Journal"
            )

            publication_date = metadata.get(
                "publication_date",
                "Unknown Year"
            )

            title = doc.split("Title:")[1].split("Abstract:")[0].strip()

            sources.append(
                {
                    "title": title,
                    "journal": journal,
                    "year": publication_date
                }
            )

        return context, sources

    def answer_question(
        self,
        question,
        n_results=3
    ):
        """
        Retrieve evidence and generate answer using Llama.
        """

        context, sources = self.retrieve_context(
            query=question,
            n_results=n_results
        )

        prompt = f"""
            You are MediAssist AI, an evidence-based clinical research assistant.

            Use ONLY information found in the provided context.

            Context:
            {context}

            Question:
            {question}

            Instructions:
            - Do not use outside knowledge.
            - Do not invent facts.
            - If evidence is conflicting, mention it.
            - If evidence is insufficient, explicitly state it.
            - Keep the answer concise and professional.

            Output Format:

            ## Short Answer

            ## Evidence Summary

            ## Clinical Considerations

            ## Limitations of Evidence
            """

        answer = self.llm.generate(prompt)

        answer += "\n\n## Sources\n"

        for source in sources:
            answer += (
                f"- {source['title']} | "
                f"{source['journal']} ({source['year']})\n"
            )

        return answer