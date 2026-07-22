"""Data ingestion script."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.pdf_parser import PDFParser
from src.ingestion.chunker import TextChunker
from src.ingestion.embedder import Embedder
from src.retrieval.vector_store import VectorStore
from src.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run the ingestion pipeline."""
    data_dir = "./data/sample_docs"
    
    # Check if data directory exists
    if not Path(data_dir).exists():
        logger.error(f"Data directory not found: {data_dir}")
        logger.info("Please create the directory and add PDF files")
        return
    
    logger.info("Starting ingestion pipeline...")
    
    # Step 1: Parse PDFs
    logger.info("Step 1: Parsing PDFs...")
    parser = PDFParser()
    pages = parser.parse_directory(data_dir)
    logger.info(f"Parsed {len(pages)} pages")
    
    # Step 2: Chunk text
    logger.info("Step 2: Chunking text...")
    chunker = TextChunker(
        chunk_size=settings.max_chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = chunker.chunk_pages(pages)
    logger.info(f"Created {len(chunks)} chunks")
    
    # Step 3: Generate embeddings
    logger.info("Step 3: Generating embeddings...")
    embedder = Embedder()
    chunks = embedder.embed_chunks(chunks)
    
    # Step 4: Create vector store
    logger.info("Step 4: Creating vector store...")
    vector_store = VectorStore()
    vector_store.create_from_chunks(chunks)
    
    # Step 5: Save vector store
    logger.info("Step 5: Saving vector store...")
    vector_store.save("./vector_store")
    
    logger.info("✅ Ingestion complete!")
    logger.info(f"Vector store saved to ./vector_store")
    logger.info(f"Total chunks: {len(chunks)}")


if __name__ == "__main__":
    main()
