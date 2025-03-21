# Web-Wiki-Search

An AI-powered search application that combines web search results and Wikipedia information to provide comprehensive answers to user queries.

## Features

- Dual-source search combining web results and Wikipedia articles
- Source tracking for transparency and verification
- Error handling and robust search capabilities
- Clean, intuitive Streamlit interface

## Setup

1. Ensure Python 3.9+ is installed
2. Create a `.env` file with your API keys:
```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
streamlit run app.py
```
Alternatively, use the included batch file:
```bash
run_app.bat
```

## Project Structure

- `app.py`: Streamlit frontend application
- `web_wiki_search.py`: Core search functionality using LangChain and LangGraph
- `requirements.txt`: Project dependencies

## Technologies

- Streamlit for the user interface
- LangChain for LLM integration
- LangGraph for workflow orchestration
- Groq for LLM access (Llama-3.3-70b-versatile)
- Tavily Search API for web search
- Wikipedia API for knowledge base access 