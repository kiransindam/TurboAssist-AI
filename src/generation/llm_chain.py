"""LLM chain for answer generation."""
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from src.config import settings
from src.generation.prompt_templates import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from src.retrieval.retriever import Retriever
import logging

logger = logging.getLogger(__name__)


class LLMChain:
    """Orchestrate LLM calls for RAG."""
    
    def __init__(self, retriever: Retriever):
        self.retriever = retriever
        self.llm = ChatOpenAI(
            model=settings.openai_llm_model,
            openai_api_key=settings.openai_api_key,
            temperature=0.1,
        )
        
    def generate_answer(
        self,
        question: str,
        k: int = 5,
    ) -> Dict:
        """
        Generate an answer for the given question.
        
        Args:
            question: User question
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with answer, citations, and metadata
        """
        # Retrieve relevant documents
        documents = self.retriever.retrieve(question, k=k)
        
        # Format context
        context = self.retriever.format_context(documents)
        
        # Build prompt
        user_prompt = USER_PROMPT_TEMPLATE.format(
            context=context,
            question=question,
        )
        
        # Generate answer
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_prompt),
        ]
        
        response = self.llm.invoke(messages)
        answer = response.content
        
        # Extract citations
        citations = self._extract_citations(documents)
        
        logger.info(f"Generated answer for: {question[:50]}...")
        
        return {
            "answer": answer,
            "citations": citations,
            "sources": [
                {
                    "doc_id": doc.metadata.get("doc_id"),
                    "file_name": doc.metadata.get("file_name"),
                    "page": doc.metadata.get("page"),
                    "chunk_id": doc.metadata.get("chunk_id"),
                }
                for doc in documents
            ],
        }
        
    def _extract_citations(self, documents: List) -> List[str]:
        """Extract citation strings from documents."""
        citations = []
        for doc in documents:
            doc_id = doc.metadata.get("doc_id", "unknown")
            page = doc.metadata.get("page", "?")
            citations.append(f"[{doc_id}:{page}]")
        return citations
