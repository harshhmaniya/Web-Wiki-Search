try:
    from langchain_groq import ChatGroq
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_community.document_loaders import WikipediaLoader
    from langchain_community.tools import TavilySearchResults
    from langgraph.graph import START, END, StateGraph
    from typing_extensions import TypedDict
    from typing import Annotated, List, Dict, Any, Optional
    import operator
    import logging
    import time
    import os
    from dotenv import load_dotenv
    load_dotenv()
except ImportError as e:
    import logging
    logging.error(f"Import error: {e}")
    raise

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Check for API keys
if not os.environ.get("GROQ_API_KEY"):
    logger.error("GROQ_API_KEY not found in environment variables")
    raise ValueError("GROQ_API_KEY not set. Please set it in your environment or .env file")

if not os.environ.get("TAVILY_API_KEY"):
    logger.error("TAVILY_API_KEY not found in environment variables")
    raise ValueError("TAVILY_API_KEY not set. Please set it in your environment or .env file")

# Try to access Streamlit secrets if running in Streamlit Cloud
try:
    import streamlit as st
    # If we have secrets, use them
    if hasattr(st, "secrets"):
        if "GROQ_API_KEY" in st.secrets and not os.environ.get("GROQ_API_KEY"):
            os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
            logger.info("Using GROQ_API_KEY from Streamlit secrets")
        
        if "TAVILY_API_KEY" in st.secrets and not os.environ.get("TAVILY_API_KEY"):
            os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
            logger.info("Using TAVILY_API_KEY from Streamlit secrets")
except ImportError:
    logger.info("Not running in Streamlit environment")

# Initialize LLM with error handling
try:
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    logger.info("LLM initialized successfully")
except Exception as e:
    logger.error(f"Error initializing LLM: {e}")
    raise

class Source:
    def __init__(self, title: str, url: Optional[str] = None, content_preview: Optional[str] = None):
        self.title = title
        self.url = url
        self.content_preview = content_preview
        
    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "content_preview": self.content_preview
        }

class State(TypedDict):
    question: str
    answer: str
    context: Annotated[list, operator.add]
    sources: Annotated[list, operator.add]

def search_web(state):
    """ Retrieve docs from web search with enhanced source tracking """
    start_time = time.time()
    logger.info(f"Initiating web search for: {state['question']}")
    
    try:
        tavily_search = TavilySearchResults(max_results=3)
        search_docs = tavily_search.invoke(state['question'])
        
        # Track sources
        sources = []
        for doc in search_docs:
            # Extract domain from URL
            url = doc.get("url", "")
            title = doc.get("title", url.split("/")[2] if "/" in url else "Web Source")
            
            # Create truncated content preview (first 150 chars)
            content_preview = doc.get("content", "")[:150] + "..." if doc.get("content") else None
            
            sources.append(Source(title=title, url=url, content_preview=content_preview).to_dict())
        
        # Format for context
        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document href="{doc["url"]}" title="{doc.get("title", "Web Document")}">\n{doc["content"]}\n</Document>'
                for doc in search_docs
            ]
        )
        
        logger.info(f"Web search completed in {time.time() - start_time:.2f} seconds. Found {len(search_docs)} documents.")
        return {"context": [formatted_search_docs], "sources": [sources]}
    
    except Exception as e:
        logger.error(f"Error during web search: {e}")
        return {"context": ["<Error: Web search failed>"], "sources": []}


def search_wikipedia(state):
    """ Retrieve docs from wikipedia with enhanced source tracking """
    start_time = time.time()
    logger.info(f"Initiating Wikipedia search for: {state['question']}")
    
    try:
        search_docs = WikipediaLoader(query=state['question'],
                                      load_max_docs=2).load()
        
        # Track sources
        sources = []
        for doc in search_docs:
            source_url = doc.metadata.get("source", "")
            title = source_url.split("/")[-1].replace("_", " ") if source_url else "Wikipedia Article"
            
            # Create truncated content preview
            content_preview = doc.page_content[:150] + "..." if doc.page_content else None
            
            sources.append(Source(title=title, url=source_url, content_preview=content_preview).to_dict())
        
        # Format for context
        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document source="Wikipedia" title="{doc.metadata.get("source", "").split("/")[-1].replace("_", " ")}" url="{doc.metadata.get("source", "")}">\n{doc.page_content}\n</Document>'
                for doc in search_docs
            ]
        )
        
        logger.info(f"Wikipedia search completed in {time.time() - start_time:.2f} seconds. Found {len(search_docs)} articles.")
        return {"context": [formatted_search_docs], "sources": [sources]}
    
    except Exception as e:
        logger.error(f"Error during Wikipedia search: {e}")
        return {"context": ["<Error: Wikipedia search failed>"], "sources": []}


def generate_answer(state):
    """ Node to answer a question with improved prompt engineering """
    start_time = time.time()
    logger.info("Generating answer from context")
    
    try:
        context = state.get("context", [])
        question = state.get("question", "")
        
        # Enhanced prompt template with better instructions
        answer_template = """
You are an AI assistant providing accurate and helpful answers based on the provided context.
        
QUESTION: {question}

CONTEXT:
{context}

INSTRUCTIONS:
1. Answer the question accurately based ONLY on the provided context
2. If the context doesn't contain enough information to answer the question fully, acknowledge this limitation
3. Present your answer in a clear, concise manner
4. If the context contains conflicting information, present both perspectives
5. Use bullet points or numbered lists where appropriate to organize information
6. DO NOT make up information that isn't in the context
7. DO NOT cite sources that aren't in the context
8. Write in a helpful, informative tone

Your response should be comprehensive yet focused on answering the user's question directly.
"""
        answer_instructions = answer_template.format(question=question, context=context)
        
        answer = llm.invoke([
            SystemMessage(content=answer_instructions),
            HumanMessage(content="Please provide a well-structured answer to this question based only on the provided context.")
        ])
        
        logger.info(f"Answer generated in {time.time() - start_time:.2f} seconds")
        return {"answer": answer}
    
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        error_msg = f"I apologize, but I encountered an error while processing your question. Error details: {str(e)}"
        return {"answer": error_msg}


# Setup graph with error handling
def create_workflow_graph():
    try:
        builder = StateGraph(State)
        
        builder.add_node("Web_Search", search_web)
        builder.add_node("Wikipedia_Search", search_wikipedia)
        builder.add_node("Generate_Answer", generate_answer)
        
        builder.add_edge(START, "Web_Search")
        builder.add_edge(START, "Wikipedia_Search")
        builder.add_edge("Web_Search", "Generate_Answer")
        builder.add_edge("Wikipedia_Search", "Generate_Answer")
        builder.add_edge("Generate_Answer", END)
        
        return builder.compile()
    
    except Exception as e:
        logger.error(f"Error creating workflow graph: {e}")
        raise

# Create the graph
graph = create_workflow_graph()

# Only run the example if this file is executed directly
if __name__ == "__main__":
    test_question = "What is Machine Learning?"
    logger.info(f"Testing with question: {test_question}")
    
    response = graph.invoke({"question": test_question})
    
    print("\n--- ANSWER ---")
    print(response.get('answer', {}).content)
    
    # Print sources if available
    if 'sources' in response:
        print("\n--- SOURCES ---")
        for source_list in response['sources']:
            for source in source_list:
                print(f"- {source.get('title')} ({source.get('url', 'No URL')})")
