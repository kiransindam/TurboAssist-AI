"""Retriever with re-ranking and metadata filtering."""
from typing import List, Dict, Optional
from langchain.schema import Document
from src.retrieval.vector_store import VectorStore
import logging

logger = logging.getLogger(__name__)


class Retriever:
    """Advanced retriever with filtering and re-ranking."""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        
    def retrieve(
        self,
        query: str,
        k: int = 5,
        doc_id_filter: Optional[str] = None,
    ) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            k: Number of results
            doc_id_filter: Optional filter by document ID
            
        Returns:
            List of relevant Document objects
        """
        # Initial retrieval
        results = self.vector_store.similarity_search(query, k=k * 2)
        
        # Apply filters
        if doc_id_filter:
            results = [
                doc for doc in results
                if doc.metadata.get("doc_id") == doc_id_filter
            ]
        
        # Take top k
        results = results[:k]
        
        logger.info(f"Retrieved {len(results)} documents for query: {query[:50]}...")
        return results
        
    def format_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into context string.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, doc in enumerate(documents, 1):
            metadata = doc.metadata
            source = f"{metadata.get('file_name', 'Unknown')}, Page {metadata.get('page', '?')}"
            context_parts.append(f"[{i}] Source: {source}\n{doc.page_content}")
            
        return "\n\n".join(context_parts)
