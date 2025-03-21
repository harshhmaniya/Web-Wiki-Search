import streamlit as st
import sys
import importlib
import os
import traceback

st.set_page_config(
    page_title="AI Search Diagnostics",
    page_icon="🔧",
    layout="centered"
)

st.title("🔧 AI Search Deployment Diagnostics")

# Check Python version
python_version = ".".join(map(str, sys.version_info[:3]))
st.write(f"Python version: {python_version}")

# Check environment variables
st.write("### Environment Variables")
has_groq_key = bool(os.environ.get("GROQ_API_KEY"))
has_tavily_key = bool(os.environ.get("TAVILY_API_KEY"))

st.write(f"GROQ_API_KEY present: {'✅' if has_groq_key else '❌'}")
st.write(f"TAVILY_API_KEY present: {'✅' if has_tavily_key else '❌'}")

# Check imports
st.write("### Library Imports")
libraries = [
    "streamlit",
    "langchain_groq",
    "langchain_core",
    "langchain_community",
    "langgraph",
    "typing_extensions",
    "wikipedia",
    "tavily_python",
    "dotenv"
]

for lib_name in libraries:
    try:
        lib = importlib.import_module(lib_name)
        if hasattr(lib, "__version__"):
            st.write(f"{lib_name}: ✅ (version {lib.__version__})")
        else:
            st.write(f"{lib_name}: ✅ (installed)")
    except ImportError as e:
        st.write(f"{lib_name}: ❌ (not installed or import error)")

# Try specific problematic imports
st.write("### Testing Specific Imports")

try:
    from langchain_groq import ChatGroq
    st.write("ChatGroq: ✅")
except Exception as e:
    st.write(f"ChatGroq: ❌ - {str(e)}")
    with st.expander("Traceback"):
        st.code(traceback.format_exc())

try:
    from langchain_community.document_loaders import WikipediaLoader
    st.write("WikipediaLoader: ✅")
except Exception as e:
    st.write(f"WikipediaLoader: ❌ - {str(e)}")
    with st.expander("Traceback"):
        st.code(traceback.format_exc())

try:
    from langchain_community.tools import TavilySearchResults
    st.write("TavilySearchResults: ✅")
except Exception as e:
    st.write(f"TavilySearchResults: ❌ - {str(e)}")
    with st.expander("Traceback"):
        st.code(traceback.format_exc())

try:
    from langgraph.graph import START, END, StateGraph
    st.write("StateGraph: ✅")
except Exception as e:
    st.write(f"StateGraph: ❌ - {str(e)}")
    with st.expander("Traceback"):
        st.code(traceback.format_exc())

# Test if web_wiki_search module can be imported
st.write("### Testing web_wiki_search Module")

try:
    import web_wiki_search
    st.write("web_wiki_search module: ✅")
    try:
        from web_wiki_search import graph
        st.write("web_wiki_search.graph: ✅")
    except Exception as e:
        st.write(f"web_wiki_search.graph: ❌ - {str(e)}")
        with st.expander("Traceback"):
            st.code(traceback.format_exc())
except Exception as e:
    st.write(f"web_wiki_search module: ❌ - {str(e)}")
    with st.expander("Traceback"):
        st.code(traceback.format_exc())

st.write("### Next Steps")
st.write("""
Once you've identified the specific issues above:

1. For missing libraries, update requirements.txt and redeploy
2. For API key issues, add them to Streamlit secrets
3. For import conflicts, adjust the versions in requirements.txt
""") 