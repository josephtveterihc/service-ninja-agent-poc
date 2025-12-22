"""
Demo of document search capabilities for PTO documents.
Shows how the system can search through PDF documents to answer policy questions.
"""

import asyncio
import os
from typing import Dict, List

# Mock document search results (simulating the real PDF content)
MOCK_DOCUMENT_DATA = {
    "HR & Learning Self-Service - What are the observed holidays for 2025": {
        "content": """
        After carefully reviewing the results of the June 2024 all-caregiver survey, meeting with senior leaders, 
        and considering our operational needs, we have decided to adjust the number of company-observed holidays 
        to eight (8) days per year. Starting in 2025 the holidays are:
        
        • New Year's Day
        • Martin Luther King, Jr Day
        • Memorial Day
        • Independence Day
        • Labor Day
        • Thanksgiving Day
        • Christmas Eve
        • Christmas Day
        
        Will PTO accruals be reduced because of this change? No, PTO accruals will remain the same.
        """
    },
    "Pay & Benefits - Holidays": {
        "content": """
        Intermountain Health observes eight holidays. The eight holidays are:
        • New Year's Day
        • Martin Luther King Jr Day
        • Memorial Day
        • Independence Day
        • Labor Day
        • Thanksgiving Day
        • Christmas Eve
        • Christmas Day
        
        For more information, read our Observed Holiday FAQs and Holiday PTO FAQs.
        """
    },
    "HR & Learning Self-Service - Holiday PTO FAQs": {
        "content": """
        What's the difference between paid time off (PTO) and an observed holiday?
        
        Intermountain Health provides eligible full-time and part-time caregivers with PTO which is intended 
        to cover time away from work that can be used for vacations, holidays, personal time, personal illness, 
        or time off to care for others. Therefore, hours for observed holidays – days when Intermountain closes 
        offices, clinics, and some services – are included in your PTO accrual.
        """
    }
}

def mock_search_documents(query: str) -> str:
    """Mock document search function that simulates searching PDF documents."""
    query_lower = query.lower()
    results = []
    
    for doc_name, doc_info in MOCK_DOCUMENT_DATA.items():
        content = doc_info['content']
        
        # Simple keyword matching
        if any(word in content.lower() for word in query_lower.split()):
            # Extract relevant sentences
            sentences = content.split('.')
            relevant_sentences = [s.strip() for s in sentences if any(word in s.lower() for word in query_lower.split())]
            
            if relevant_sentences:
                results.append({
                    'document': doc_name,
                    'content': '. '.join(relevant_sentences[:2]) + '.'
                })
    
    if not results:
        return f"No information found for '{query}' in available documents."
    
    formatted_results = f"📄 Document Search Results for '{query}':\\n\\n"
    
    for i, result in enumerate(results, 1):
        formatted_results += f"{i}. **{result['document']}**\\n"
        formatted_results += f"   {result['content']}\\n\\n"
    
    return formatted_results.strip()

def mock_list_documents() -> str:
    """Mock function to list available documents."""
    docs = list(MOCK_DOCUMENT_DATA.keys())
    formatted_list = "📚 Available PTO Documents:\\n\\n"
    for i, doc in enumerate(docs, 1):
        formatted_list += f"{i}. {doc}\\n"
    
    return formatted_list.strip()

async def demo_document_search():
    """Demo the document search capabilities."""
    print("🔍 PTO Document Search Demo")
    print("=" * 50)
    print("This demo shows how the AI agents can search through company PTO documents")
    print("to provide accurate policy information.\\n")
    
    # Demo various search queries
    queries = [
        "Christmas holiday",
        "observed holidays 2025", 
        "PTO accrual",
        "vacation time",
        "New Year's Day"
    ]
    
    for query in queries:
        print(f"🔍 Search Query: '{query}'")
        print("-" * 40)
        result = mock_search_documents(query)
        print(result)
        print("\\n" + "=" * 50 + "\\n")
        await asyncio.sleep(0.5)  # Pause for readability
    
    print("📚 Available Documents:")
    print("-" * 25)
    print(mock_list_documents())
    print("\\n" + "=" * 50)
    
    print("✨ Key Benefits of Document Integration:")
    print("• Agents can access real company policy documents")
    print("• Provides accurate, up-to-date information")
    print("• Reduces inconsistencies in policy responses") 
    print("• Sources information from official HR documents")
    print("• Enables complex policy questions to be answered automatically")

if __name__ == "__main__":
    asyncio.run(demo_document_search())