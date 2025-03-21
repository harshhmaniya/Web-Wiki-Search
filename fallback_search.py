"""
Fallback search module that doesn't rely on external APIs.
This is a simplified version that can be used when the main module fails.
"""

import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def invoke(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simplified invoke function that returns a static response.
    
    Args:
        state: Dictionary containing the question
        
    Returns:
        Dictionary with a static answer
    """
    question = state.get('question', '')
    logger.info(f"Processing question in fallback mode: {question}")
    
    answer = {
        'content': f"""
# API Connection Issue

I couldn't answer your question about "{question}" because there's an issue with connecting to the required APIs.

## Possible causes:
1. Missing API keys for Groq or Tavily
2. Network connectivity issues
3. Package installation problems

## How to fix:
Please check that you've configured GROQ_API_KEY and TAVILY_API_KEY in your environment or Streamlit secrets.
        """
    }
    
    fallback_sources = [
        {
            "title": "Groq API Documentation",
            "url": "https://console.groq.com/docs/quickstart",
            "content_preview": "Sign up for Groq and get your API key from the Groq console..."
        },
        {
            "title": "Tavily API Documentation",
            "url": "https://docs.tavily.com/docs/tavily-api/getting-started",
            "content_preview": "Sign up for Tavily Search API and get your API key..."
        }
    ]
    
    return {
        'answer': answer,
        'sources': [fallback_sources]
    } 