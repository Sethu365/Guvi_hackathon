import os
import re
from typing import List, Dict, Any
from dataclasses import dataclass
import pdfplumber
import fitz  # PyMuPDF
import markdown
import html2text
from bs4 import BeautifulSoup

@dataclass
class DocumentChunk:
    text: str
    chunk_id: str
    page: int = None
    metadata: Dict[str, Any] = None

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True

    def process_document(self, file_path: str, file_type: str) -> List[DocumentChunk]:
        """Process a document and return chunks"""
        try:
            if file_type == '.pdf':
                return self._process_pdf(file_path)
            elif file_type == '.md':
                return self._process_markdown(file_path)
            elif file_type == '.html':
                return self._process_html(file_path)
            elif file_type == '.txt':
                return self._process_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")

    def _process_pdf(self, file_path: str) -> List[DocumentChunk]:
        """Process PDF file using pdfplumber"""
        chunks = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                full_text = ""
                page_texts = []
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        page_text = self._clean_text(page_text)
                        page_texts.append((page_text, page_num))
                        full_text += f"\n\n--- Page {page_num} ---\n\n" + page_text

                # Create chunks with page information
                text_chunks = self._create_chunks(full_text)
                
                for i, chunk_text in enumerate(text_chunks):
                    # Try to determine which page this chunk belongs to
                    page_num = self._find_page_for_chunk(chunk_text, page_texts)
                    
                    chunk = DocumentChunk(
                        text=chunk_text,
                        chunk_id=f"chunk_{i}",
                        page=page_num,
                        metadata={"source": "pdf", "chunk_index": i}
                    )
                    chunks.append(chunk)

        except Exception as e:
            # Fallback to PyMuPDF if pdfplumber fails
            try:
                chunks = self._process_pdf_pymupdf(file_path)
            except Exception as fallback_error:
                raise Exception(f"Failed to process PDF with both libraries: {str(e)}, {str(fallback_error)}")

        return chunks

    def _process_pdf_pymupdf(self, file_path: str) -> List[DocumentChunk]:
        """Fallback PDF processing using PyMuPDF"""
        chunks = []
        
        doc = fitz.open(file_path)
        full_text = ""
        page_texts = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            if page_text:
                page_text = self._clean_text(page_text)
                page_texts.append((page_text, page_num + 1))
                full_text += f"\n\n--- Page {page_num + 1} ---\n\n" + page_text

        doc.close()

        text_chunks = self._create_chunks(full_text)
        
        for i, chunk_text in enumerate(text_chunks):
            page_num = self._find_page_for_chunk(chunk_text, page_texts)
            
            chunk = DocumentChunk(
                text=chunk_text,
                chunk_id=f"chunk_{i}",
                page=page_num,
                metadata={"source": "pdf_pymupdf", "chunk_index": i}
            )
            chunks.append(chunk)

        return chunks

    def _process_markdown(self, file_path: str) -> List[DocumentChunk]:
        """Process Markdown file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Convert markdown to HTML then to text for better structure preservation
        html = markdown.markdown(content)
        text = self.html_converter.handle(html)
        text = self._clean_text(text)

        return self._create_document_chunks(text, "markdown")

    def _process_html(self, file_path: str) -> List[DocumentChunk]:
        """Process HTML file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse HTML and extract text
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text and clean it
        text = soup.get_text()
        text = self._clean_text(text)

        return self._create_document_chunks(text, "html")

    def _process_text(self, file_path: str) -> List[DocumentChunk]:
        """Process plain text file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        text = self._clean_text(text)
        return self._create_document_chunks(text, "text")

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        return text

    def _create_chunks(self, text: str) -> List[str]:
        """Create overlapping chunks from text"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            chunks.append(chunk_text)
            
            # Break if we've reached the end
            if i + self.chunk_size >= len(words):
                break
                
        return chunks

    def _create_document_chunks(self, text: str, source_type: str) -> List[DocumentChunk]:
        """Create document chunks without page information"""
        text_chunks = self._create_chunks(text)
        chunks = []
        
        for i, chunk_text in enumerate(text_chunks):
            chunk = DocumentChunk(
                text=chunk_text,
                chunk_id=f"chunk_{i}",
                metadata={"source": source_type, "chunk_index": i}
            )
            chunks.append(chunk)
            
        return chunks

    def _find_page_for_chunk(self, chunk_text: str, page_texts: List[tuple]) -> int:
        """Try to determine which page a chunk belongs to"""
        # Look for page markers first
        page_match = re.search(r'--- Page (\d+) ---', chunk_text)
        if page_match:
            return int(page_match.group(1))
        
        # If no page marker, try to match content to pages
        chunk_words = set(chunk_text.lower().split()[:20])  # Use first 20 words
        
        best_match_page = 1
        best_match_score = 0
        
        for page_text, page_num in page_texts:
            page_words = set(page_text.lower().split())
            overlap = len(chunk_words.intersection(page_words))
            
            if overlap > best_match_score:
                best_match_score = overlap
                best_match_page = page_num
        
        return best_match_page