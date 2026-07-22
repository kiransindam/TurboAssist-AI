"""PDF document parser using PyMuPDF."""
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class PDFParser:
    """Parse PDF documents and extract text with metadata."""
    
    def __init__(self):
        self.parser = fitz
        
    def parse_pdf(self, file_path: str) -> List[Dict]:
        """
        Parse a PDF file and extract text page by page.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of dictionaries with 'text', 'page', and 'metadata'
        """
        pages = []
        doc_id = Path(file_path).stem
        
        try:
            with self.parser.open(file_path) as doc:
                metadata = {
                    "doc_id": doc_id,
                    "file_name": Path(file_path).name,
                    "total_pages": len(doc),
                }
                
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    text = page.get_text()
                    
                    if text.strip():
                        pages.append({
                            "text": text,
                            "page": page_num + 1,
                            "metadata": {
                                **metadata,
                                "page": page_num + 1,
                            }
                        })
                
                logger.info(f"Parsed {len(pages)} pages from {file_path}")
                
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            raise
            
        return pages
    
    def parse_directory(self, directory: str) -> List[Dict]:
        """Parse all PDFs in a directory."""
        all_pages = []
        pdf_dir = Path(directory)
        
        for pdf_file in pdf_dir.glob("*.pdf"):
            pages = self.parse_pdf(str(pdf_file))
            all_pages.extend(pages)
            
        logger.info(f"Parsed {len(all_pages)} total pages from {directory}")
        return all_pages
