import streamlit as st
from web_wiki_search import graph
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="AI Search Engine",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS to make the app look nicer
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
        padding: 0.75rem;
    }
    .stButton > button {
        background-color: #0284c7;
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .stButton > button:hover {
        background-color: #0369a1;
    }
    h1 {
        color: #1e293b;
        font-weight: 800;
    }
    h2 {
        color: #0284c7;
        font-weight: 600;
    }
    .result-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        color: #1e293b;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .source-card {
        background-color: #f8fafc;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border-left: 3px solid #0284c7;
        margin-bottom: 0.5rem;
    }
    .source-title {
        font-weight: 600;
        color: #0284c7;
    }
    .source-url {
        font-size: 0.8rem;
        color: #64748b;
        word-break: break-all;
    }
    .source-preview {
        margin-top: 0.5rem;
        font-size: 0.9rem;
        color: #475569;
        font-style: italic;
    }
    .timer {
        font-size: 0.9rem;
        color: #64748b;
        text-align: right;
        margin-top: 0.5rem;
    }
    .query-history {
        background-color: #f1f5f9;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .query-chip {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        margin: 0.25rem;
        font-size: 0.9rem;
        cursor: pointer;
    }
    .query-chip:hover {
        background-color: #bae6fd;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for query history
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

# Function to extract and format sources
def format_sources(response):
    all_sources = []
    
    if 'sources' in response:
        for source_list in response['sources']:
            all_sources.extend(source_list)
    
    return all_sources

# Function to safely extract answer text
def extract_answer(response):
    answer_obj = response.get('answer', {})
    
    # Try various methods to extract the answer content
    if hasattr(answer_obj, 'content'):
        return answer_obj.content
    elif isinstance(answer_obj, dict) and 'content' in answer_obj:
        return answer_obj['content']
    elif isinstance(answer_obj, str):
        return answer_obj
    else:
        # Last resort - convert to string
        return str(answer_obj) if answer_obj else "No answer found"

# App header
st.title("🔍 AI-Powered Search Engine")
st.write("Get comprehensive answers from the web and Wikipedia using advanced AI")

# Search input
with st.form(key="search_form"):
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("Enter your question", placeholder="E.g., What is machine learning?")
    with col2:
        search_button = st.form_submit_button("Search")

# Query history (if there are previous queries)
if st.session_state.query_history and not query:
    st.markdown("### 📚 Recent Searches")
    with st.container(height=100, border=False):
        for past_query in st.session_state.query_history[-5:]:  # Show last 5 queries
            st.markdown(
                f'<div class="query-chip" onclick="document.querySelector(\'input[aria-label*=\'Enter your question\']\').value=\'{past_query}\';document.querySelector(\'input[aria-label*=\'Enter your question\']\').dispatchEvent(new Event(\'input\', {{ bubbles: true }}))">{past_query}</div>', 
                unsafe_allow_html=True
            )

# Feature highlights (only show when no query is in progress)
if not query:
    st.markdown("### 🌟 Features")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("##### 🌐 Web Search")
        st.write("Get relevant information from across the internet")
    with col2:
        st.markdown("##### 📚 Wikipedia")
        st.write("Access structured knowledge from Wikipedia")
    with col3:
        st.markdown("##### 🤖 AI Analysis")
        st.write("LLM-powered answers synthesized from multiple sources")
    
    st.markdown("### 💡 Try asking about:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- History and historical events")
        st.markdown("- Science and technology")
        st.markdown("- Current affairs")
    with col2:
        st.markdown("- Famous people and places")
        st.markdown("- Concepts and ideas")
        st.markdown("- How things work")

# Handle search
if search_button and query:
    # Add query to history if it's new
    if query not in st.session_state.query_history:
        st.session_state.query_history.append(query)
        # Keep only the last 10 queries
        if len(st.session_state.query_history) > 10:
            st.session_state.query_history.pop(0)
    
    # Start timer
    start_time = time.time()
    
    with st.spinner("🔍 Searching web and Wikipedia..."):
        try:
            # Process the search query using the graph from web_wiki_search.py
            response = graph.invoke({"question": query})
            
            # Calculate time taken
            time_taken = time.time() - start_time
            
            # Extract answer and sources
            answer = extract_answer(response)
            sources = format_sources(response)
            
            # Display results
            st.markdown("### 📝 Results")
            
            # Fix for answer display - use container and write for better visibility
            with st.container(border=True):
                st.subheader("Answer")
                st.write(answer)
                st.markdown(f'<div class="timer">⏱️ Answer generated in {time_taken:.2f} seconds</div>', unsafe_allow_html=True)
            
            # Display sources if available
            if sources:
                with st.expander("📚 View Sources", expanded=False):
                    st.markdown("The answer was generated using information from these sources:")
                    
                    for source in sources:
                        title = source.get('title', 'Unknown Source')
                        url = source.get('url', '')
                        preview = source.get('content_preview', 'No preview available')
                        
                        st.markdown(f"""
                        <div class="source-card">
                            <div class="source-title">{title}</div>
                            <div class="source-url">{url}</div>
                            <div class="source-preview">{preview}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            st.error(f"An error occurred: {str(e)}")
            st.write("Please try again with a different question.")

# Footer removed 