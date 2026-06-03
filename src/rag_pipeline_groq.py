from chroma_manager import ChromaManager
from groq_llm import GroqLLM

class RAGPipeline:

    def __init__(self):

        self.vector_db = ChromaManager(
            collection_name="pubmed_articles_filtered"
        )

        self.llm = GroqLLM()

    def retrieve_context(
        self,
        query,
        n_results=5
    ):

        results = self.vector_db.retrieve(
            query=query,
            n_results=n_results
        )

        context = ""

        for doc in results["documents"][0]:

            context += doc
            context += "\n\n"

        return context
    
    def answer_question(
        self,
        question,
        n_results=5
    ):

        context = self.retrieve_context(
            query=question,
            n_results=n_results
        )

        prompt = f"""
You are MediAssist AI, an evidence-based healthcare research assistant.

Use ONLY the information contained in the provided context.

Context:
{context}

Question:
{question}

Instructions:
- Summarize the retrieved evidence.
- Mention the study/article title when discussing findings.
- Use findings directly from the context.
- Include numerical results only when explicitly present.
- Do not invent facts.
- Include numerical results when explicitly present in the retrieved context.
- Mention participant counts when available.
- Mention study type (meta-analysis, RCT, systematic review, etc.).
- When numerical effect sizes are present in the context, include them in the evidence summary.

Format:

## Short Answer

## Evidence Summary
- Bullet points

## Clinical Considerations
- Bullet points

## Limitations of Evidence

## Sources Used
- List article titles used
"""

        return self.llm.generate(prompt)