"""
File Parser Utility for PDF and TXT files
Extracts text and handles chunking for large documents
"""

import os
import logging
from typing import List, Tuple, Optional
import re

logger = logging.getLogger(__name__)

class FileParser:
    """
    Utility class for parsing PDF and TXT files
    Handles text extraction and chunking for large documents
    """
    
    ALLOWED_EXTENSIONS = {'pdf', 'txt'}
    MAX_CHUNK_CHARS = 2000  # ~500 tokens
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB
    
    def __init__(self):
        self.supported_types = self.ALLOWED_EXTENSIONS.copy()
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileParser.ALLOWED_EXTENSIONS
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Get file extension in lowercase"""
        if '.' in filename:
            return filename.rsplit('.', 1)[1].lower()
        return ''
    
    def extract_text_from_pdf(self, file_path: str) -> Tuple[str, dict]:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        try:
            import pdfplumber
            
            text_parts = []
            metadata = {
                'pages': 0,
                'characters': 0,
                'method': 'pdfplumber'
            }
            
            with pdfplumber.open(file_path) as pdf:
                metadata['pages'] = len(pdf.pages)
                
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            
            full_text = '\n\n'.join(text_parts)
            metadata['characters'] = len(full_text)
            
            logger.info(f"✅ Extracted {metadata['characters']} chars from {metadata['pages']} pages")
            return full_text, metadata
            
        except Exception as e:
            logger.error(f"❌ pdfplumber failed: {e}, trying PyPDF2...")
            
            # Fallback to PyPDF2
            try:
                from PyPDF2 import PdfReader
                
                text_parts = []
                reader = PdfReader(file_path)
                metadata = {
                    'pages': len(reader.pages),
                    'characters': 0,
                    'method': 'PyPDF2'
                }
                
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                
                full_text = '\n\n'.join(text_parts)
                metadata['characters'] = len(full_text)
                
                logger.info(f"✅ Extracted {metadata['characters']} chars using PyPDF2")
                return full_text, metadata
                
            except Exception as e2:
                logger.error(f"❌ PyPDF2 also failed: {e2}")
                raise Exception(f"Failed to extract text from PDF: {e2}")
    
    def extract_text_from_txt(self, file_path: str) -> Tuple[str, dict]:
        """
        Extract text from TXT file
        
        Args:
            file_path: Path to TXT file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    
                    metadata = {
                        'encoding': encoding,
                        'characters': len(text),
                        'lines': text.count('\n') + 1
                    }
                    
                    logger.info(f"✅ Read TXT file with {encoding} encoding, {metadata['characters']} chars")
                    return text, metadata
                    
                except UnicodeDecodeError:
                    continue
            
            raise Exception("Could not decode file with any supported encoding")
            
        except Exception as e:
            logger.error(f"❌ Failed to read TXT file: {e}")
            raise
    
    def extract_text(self, file_path: str) -> Tuple[str, dict]:
        """
        Extract text from file based on extension
        
        Args:
            file_path: Path to file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        ext = self.get_file_extension(file_path)
        
        if ext == 'pdf':
            return self.extract_text_from_pdf(file_path)
        elif ext == 'txt':
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove control characters except newlines and tabs
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        text = re.sub(r'\t+', ' ', text)
        
        # Remove page numbers and headers (common patterns)
        text = re.sub(r'\n\d+\n', '\n', text)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Remove common PDF artifacts
        text = re.sub(r'[\uf0b7\u2022\u2023\u2043]', '', text)  # bullets
        text = re.sub(r'\x0c', '', text)  # form feed
        
        # Normalize punctuation spacing
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        text = re.sub(r'([.,!?;:])(?=[^\s])', r'\1 ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Indonesian sentence splitting with better patterns
        # Split on sentence endings followed by space and capital letter or newline
        sentences = re.split(r'(?<=[.!?])(?:\s+(?=[A-Z])|\n+)', text)
        
        # Also split on paragraph breaks
        result = []
        for sent in sentences:
            # If still too long, split on semicolons or commas in long text
            if len(sent) > 500:
                sub_parts = re.split(r'(?<=[;,])\s+', sent)
                result.extend(sub_parts)
            else:
                result.append(sent)
        
        # Filter empty sentences, too short, and clean
        sentences = []
        for s in result:
            s = s.strip()
            # Keep sentences with at least 3 words
            if s and len(s.split()) >= 3:
                sentences.append(s)
        
        return sentences
    
    def chunk_text(self, text: str, max_chars: int = None, overlap: int = 100) -> List[str]:
        """
        Split text into chunks suitable for paraphrasing with overlap for context
        
        Args:
            text: Input text
            max_chars: Maximum characters per chunk (default: MAX_CHUNK_CHARS)
            overlap: Number of characters to overlap between chunks for context
            
        Returns:
            List of text chunks
        """
        if max_chars is None:
            max_chars = self.MAX_CHUNK_CHARS
        
        # Clean text first
        text = self.clean_text(text)
        
        # If text is short enough, return as single chunk
        if len(text) <= max_chars:
            return [text] if text else []
        
        # Split into sentences first
        sentences = self.split_into_sentences(text)
        
        if not sentences:
            # Fallback: split by paragraphs with overlap
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            chunks = []
            current_chunk = ""
            prev_overlap = ""
            
            for para in paragraphs:
                # Add overlap from previous chunk
                chunk_start = prev_overlap + (" " if prev_overlap else "")
                
                if len(chunk_start) + len(para) <= max_chars:
                    current_chunk = chunk_start + para
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = chunk_start + para[:max_chars - len(chunk_start)]
                
                # Save overlap for next chunk (last N chars)
                if len(current_chunk) > overlap:
                    prev_overlap = current_chunk[-overlap:]
                else:
                    prev_overlap = current_chunk
            
            if current_chunk:
                chunks.append(current_chunk)
            
            return chunks
        
        # Group sentences into chunks with overlap
        chunks = []
        current_chunk = ""
        overlap_sentences = []  # Store last few sentences for overlap
        
        for i, sentence in enumerate(sentences):
            # Start with overlap from previous chunk
            if overlap_sentences and not current_chunk:
                current_chunk = " ".join(overlap_sentences)
            
            test_chunk = current_chunk + (" " if current_chunk else "") + sentence
            
            if len(test_chunk) <= max_chars:
                current_chunk = test_chunk
                # Update overlap buffer (keep last 2-3 sentences)
                overlap_sentences.append(sentence)
                if len(overlap_sentences) > 3:
                    overlap_sentences.pop(0)
            else:
                # Current chunk is full, save it
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Start new chunk with overlap
                overlap_text = " ".join(overlap_sentences[-2:]) if len(overlap_sentences) >= 2 else ""
                if len(overlap_text) + len(sentence) + 1 <= max_chars:
                    current_chunk = overlap_text + (" " if overlap_text else "") + sentence
                else:
                    # If sentence too long even with minimal overlap
                    current_chunk = sentence[:max_chars]
                
                overlap_sentences = [sentence]
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Remove duplicate chunks
        unique_chunks = []
        seen = set()
        for chunk in chunks:
            if chunk not in seen and len(chunk.split()) >= 3:
                unique_chunks.append(chunk)
                seen.add(chunk)
        
        logger.info(f"📄 Split text into {len(unique_chunks)} chunks (with overlap for context)")
        return unique_chunks
    
    def process_file(self, file_path: str, chunk: bool = True) -> dict:
        """
        Process file and return extracted text with metadata
        
        Args:
            file_path: Path to file
            chunk: Whether to split into chunks
            
        Returns:
            Dictionary with text, chunks, and metadata
        """
        # Extract text
        text, metadata = self.extract_text(file_path)
        
        # Clean text
        clean = self.clean_text(text)
        
        result = {
            'original_text': text,
            'cleaned_text': clean,
            'metadata': metadata,
            'chunks': [],
            'chunk_count': 0
        }
        
        if chunk:
            chunks = self.chunk_text(clean)
            result['chunks'] = chunks
            result['chunk_count'] = len(chunks)
        
        return result


# Singleton instance
file_parser = FileParser()
