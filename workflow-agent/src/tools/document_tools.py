"""
Document processing utilities for service monitoring system.
Provides tools to extract text from PDFs and search for monitoring documentation.
"""

import os
import pdfplumber
from typing import List, Dict, Optional, Tuple
import re
import warnings
import logging

# Suppress PDF processing warnings and errors
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*FontBBox.*")
warnings.filterwarnings("ignore", message=".*gray.*color.*")
warnings.filterwarnings("ignore", message=".*invalid float.*")

# Set pdfplumber and pdfminer logging to ERROR level to suppress warnings
logging.getLogger('pdfminer').setLevel(logging.ERROR)
logging.getLogger('pdfplumber').setLevel(logging.ERROR)
logging.getLogger('pypdfium2').setLevel(logging.ERROR)

class DocumentProcessor:
    """Handles PDF document processing for monitoring-related documents."""
    
    def __init__(self, documents_dir: str = None):
        if documents_dir is None:
            # Default to documents folder in same directory as this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            documents_dir = os.path.join(current_dir, "documents")
        
        self.documents_dir = documents_dir
        self.document_cache = {}
        self._load_documents()
    
    def _load_documents(self):
        """Load all PDF documents from the documents directory."""
        if not os.path.exists(self.documents_dir):
            print(f"⚠️  Warning: Documents directory not found: {self.documents_dir}")
            return
        
        # Temporarily redirect stderr to suppress PDF parsing warnings
        import sys
        import contextlib
        from io import StringIO
        
        stderr_buffer = StringIO()
        
        for filename in os.listdir(self.documents_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.documents_dir, filename)
                try:
                    # Capture stderr during PDF processing
                    with contextlib.redirect_stderr(stderr_buffer):
                        text = self._extract_text_from_pdf(file_path)
                    
                    self.document_cache[filename] = {
                        'text': text,
                        'path': file_path,
                        'title': filename.replace('.pdf', '').replace('_', ' ')
                    }
                    print(f"✅ Loaded document: {filename}")
                except Exception as e:
                    print(f"❌ Error loading {filename}: {e}")
        
        # Clear the stderr buffer
        stderr_buffer.getvalue()  # This clears it
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text content from a PDF file."""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            # Suppress common PDF parsing errors but still handle real issues
            if "FontBBox" not in str(e) and "gray" not in str(e) and "invalid float" not in str(e):
                print(f"❌ Error extracting text from {file_path}: {e}")
        return text
    
    def search_documents(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """Search for information across all loaded documents."""
        results = []
        query_lower = query.lower()
        
        for filename, doc_info in self.document_cache.items():
            text = doc_info['text'].lower()
            
            # Find all sentences containing query terms
            sentences = self._split_into_sentences(doc_info['text'])
            relevant_sentences = []
            
            for sentence in sentences:
                if any(term in sentence.lower() for term in query_lower.split()):
                    relevant_sentences.append(sentence.strip())
            
            if relevant_sentences:
                results.append({
                    'document': doc_info['title'],
                    'filename': filename,
                    'content': ' '.join(relevant_sentences[:3])  # Top 3 relevant sentences
                })
        
        return results[:max_results]
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences for better search results."""
        # Simple sentence splitting - could be enhanced with NLTK
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 20]
    
    def get_document_list(self) -> List[str]:
        """Get a list of all available documents."""
        return [doc_info['title'] for doc_info in self.document_cache.values()]
    
    def get_document_content(self, filename: str) -> Optional[str]:
        """Get the full content of a specific document."""
        if filename in self.document_cache:
            return self.document_cache[filename]['text']
        
        # Try partial matching
        for doc_filename, doc_info in self.document_cache.items():
            if filename.lower() in doc_filename.lower():
                return doc_info['text']
        
        return None

# Global instance for use in agent tools
_doc_processor = None

def get_document_processor() -> DocumentProcessor:
    """Get the global document processor instance."""
    global _doc_processor
    if _doc_processor is None:
        _doc_processor = DocumentProcessor()
    return _doc_processor

"""
  Method: search_monitoring_documents
  Description: Search monitoring-related documents for information
  Args:
    query (str): The search query (e.g., 'runbook', 'escalation policy', 'alert rules')
  Returns:
    str: Formatted search results from relevant documents
"""
def search_monitoring_documents(query: str) -> str:
    processor = get_document_processor()
    results = processor.search_documents(query)
    
    if not results:
        return f"No information found for '{query}' in available monitoring documents. Available documents: {', '.join(processor.get_document_list())}"
    
    formatted_results = f"📄 Document Search Results for '{query}':\n\n"
    
    for i, result in enumerate(results, 1):
        formatted_results += f"{i}. **{result['document']}**\n"
        formatted_results += f"   {result['content']}\n\n"
    
    return formatted_results.strip()

"""
  Method: list_available_documents
  Description: List all available monitoring documents
  Args:
    None
  Returns:
    str: Formatted list of available documents
"""
def list_available_documents() -> str:
    processor = get_document_processor()
    docs = processor.get_document_list()
    
    if not docs:
        return "No monitoring documents are currently available."
    
    formatted_list = "📚 Available Monitoring Documents:\n\n"
    for i, doc in enumerate(docs, 1):
        formatted_list += f"{i}. {doc}\n"
    
    return formatted_list.strip()

"""
  Method: get_document_excerpt
  Description: Get an excerpt from a specific document, optionally focused on a topic
  Args:
    document_name (str): Name of the document to retrieve
    topic (Optional[str]): Optional topic to focus the excerpt on (defaults to None)
  Returns:
    str: Document excerpt or error message if document not found
"""
def get_document_excerpt(document_name: str, topic: str = None) -> str:
    processor = get_document_processor()
    content = processor.get_document_content(document_name)
    
    if not content:
        available = ', '.join(processor.get_document_list())
        return f"Document '{document_name}' not found. Available documents: {available}"
    
    if topic:
        # Search for topic-specific content
        sentences = processor._split_into_sentences(content)
        relevant = [s for s in sentences if topic.lower() in s.lower()]
        
        if relevant:
            excerpt = ' '.join(relevant[:3])  # First 3 relevant sentences
            return f"📄 Excerpt from '{document_name}' about '{topic}':\n\n{excerpt}"
        else:
            return f"No specific information about '{topic}' found in '{document_name}'"
    
    # Return first few sentences as general excerpt
    sentences = processor._split_into_sentences(content)
    excerpt = ' '.join(sentences[:3]) if sentences else content[:500]
    
    return f"📄 Excerpt from '{document_name}':\n\n{excerpt}..."

# Tool definitions for agent framework
DOCUMENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_monitoring_documents",
            "description": "Search monitoring documentation for information about runbooks, procedures, policies, and troubleshooting guides",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for monitoring documentation (e.g., 'runbook', 'escalation policy', 'alert rules')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_available_documents",
            "description": "List all available monitoring documents",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_document_excerpt",
            "description": "Get an excerpt from a specific monitoring document",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_name": {
                        "type": "string",
                        "description": "Name of the monitoring document to retrieve"
                    },
                    "topic": {
                        "type": "string",
                        "description": "Optional topic to focus the excerpt on"
                    }
                },
                "required": ["document_name"]
            }
        }
    }
]