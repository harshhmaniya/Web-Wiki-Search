# AI-Powered Search Engine

A Streamlit application that leverages web search and Wikipedia to provide comprehensive answers to user questions using LLMs.

## Features

- **Dual-Source Search**: Combines web search results and Wikipedia articles
- **Source Tracking**: Displays the sources of information used to generate answers
- **Advanced Prompt Engineering**: Ensures accurate, well-structured responses
- **Query History**: Keeps track of your previous searches for easy access
- **Error Handling**: Robust error handling throughout the application
- **Performance Metrics**: Shows how long it takes to generate answers
- **Responsive UI**: Clean and intuitive user interface

## Screenshots

![Application Screenshot](https://via.placeholder.com/800x450.png?text=AI+Search+Engine+Screenshot)

## Setup

1. Ensure you have Python 3.9+ installed
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

## System Architecture

The application is built on a graph-based workflow:

1. **Question Input**: User submits a question through the Streamlit interface
2. **Parallel Search**: The question is sent simultaneously to:
   - Web Search (via Tavily API)
   - Wikipedia Search
3. **Context Assembly**: Results from both sources are formatted and combined
4. **LLM Answer Generation**: Groq's Llama-3.3-70b-versatile model processes the context
5. **Source Documentation**: The application tracks sources throughout the process
6. **Result Presentation**: The answer and sources are displayed in the UI

## Technologies Used

- **Streamlit**: Frontend framework
- **LangChain**: Framework for LLM applications
- **LangGraph**: For orchestrating the multi-step workflow
- **Groq**: Provides the Llama-3.3-70b-versatile LLM
- **Tavily Search API**: Web search capabilities
- **Wikipedia API**: Access to Wikipedia's knowledge base

## Future Improvements

- Add user authentication
- Implement answer rating system
- Enable export of search results
- Add more data sources
- Support for document upload 