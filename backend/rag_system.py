import os
import google.generativeai as genai
from typing import List, Tuple
from document_processor import DocumentChunk

class RAGSystem:
    def __init__(self):
        """Initialize RAG system with Gemini"""
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_answer(self, question: str, relevant_chunks: List[Tuple[DocumentChunk, float]]) -> str:
        """Generate an answer with Gemini using retrieved document chunks"""
        if not relevant_chunks:
            return "I couldn't find relevant information to answer your question."

        # Take top 5 chunks as context
        context_chunks = [chunk.text for chunk, _ in relevant_chunks[:5]]
        context = "\n\n".join(context_chunks)

        # Build prompt
        prompt = f"""
        You are a helpful assistant. Use only the context provided to answer the question.
        If the answer is not in the context, say you don't know.

        Context:
        {context}

        Question: {question}

        Answer:
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer with Gemini: {str(e)}"
