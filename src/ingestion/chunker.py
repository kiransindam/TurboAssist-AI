"""Text chunking with semantic awareness."""
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """Chunk text while preserving metadata."""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        
    def chunk_pages(self, pages: List[Dict]) -> List[Dict]:
        """
        Chunk pages into smaller segments.
        
        Args:
            pages: List of page dictionaries from PDFParser
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        
        for page in pages:
            text = page["text"]
            metadata = page["metadata"]
            
            # Split text into chunks
            text_chunks = self.text_splitter.split_text(text)
            
            for i, chunk_text in enumerate(text_chunks):
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        **metadata,
                        "chunk_id": f"{metadata['doc_id']}_p{metadata['page']}_c{i}",
                        "chunk_index": i,
                    }
                })
        
        logger.info(f"Created {len(chunks)} chunks from {len(pages)} pages")
        return chunks
