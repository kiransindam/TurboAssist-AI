"""Vector store implementation using FAISS (local) or Azure AI Search."""
from typing import List, Dict, Optional
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from src.config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """Manage vector storage and retrieval."""
    
    def __init__(self, use_azure: bool = False):
        self.use_azure = use_azure
        self.embeddings = OpenAIEmbeddings(
            model=settings.openai_embedding_model,
            openai_api_key=settings.openai_api_key,
        )
        self.vectorstore: Optional[FAISS] = None
        
    def create_from_chunks(self, chunks: List[Dict]) -> None:
        """
        Create vector store from chunks.
        
        Args:
            chunks: List of chunk dictionaries with embeddings
        """
        documents = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk["text"],
                metadata=chunk["metadata"],
            )
            documents.append(doc)
        
        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings,
        )
        
        logger.info(f"Created vector store with {len(documents)} documents")
        
    def save(self, path: str = "./vector_store") -> None:
        """Save vector store to disk."""
        if self.vectorstore:
            self.vectorstore.save_local(path)
            logger.info(f"Saved vector store to {path}")
            
    def load(self, path: str = "./vector_store") -> None:
        """Load vector store from disk."""
        self.vectorstore = FAISS.load_local(
            path,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )
        logger.info(f"Loaded vector store from {path}")
        
    def similarity_search(
        self,
        query: str,
        k: int = 5,
    ) -> List[Document]:
        """
        Perform similarity search.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of Document objects
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Call create_from_chunks() or load() first.")
            
        results = self.vectorstore.similarity_search(query, k=k)
        return results
