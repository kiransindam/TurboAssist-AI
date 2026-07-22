"""Generate embeddings using OpenAI."""
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings
from src.config import settings
import logging

logger = logging.getLogger(__name__)


class Embedder:
    """Generate embeddings for text chunks."""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.openai_embedding_model,
            openai_api_key=settings.openai_api_key,
        )
        
    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Generate embeddings for all chunks.
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            List of chunks with added 'embedding' field
        """
        texts = [chunk["text"] for chunk in chunks]
        
        # Generate embeddings in batches
        embeddings = self.embeddings.embed_documents(texts)
        
        # Add embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding
            
        logger.info(f"Generated {len(embeddings)} embeddings")
        return chunks
