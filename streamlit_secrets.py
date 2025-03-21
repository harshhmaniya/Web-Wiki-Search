import streamlit as st
import json
import os

st.set_page_config(
    page_title="Streamlit Secrets Setup",
    page_icon="🔑",
    layout="centered"
)

st.title("🔑 API Keys Setup Guide")
st.write("""
This page will help you set up the necessary API keys for your Streamlit deployment.
The web-wiki-search app requires two API keys to function properly.
""")

st.markdown("### Required API Keys")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Groq API Key")
    st.markdown("""
    1. Go to [console.groq.com](https://console.groq.com/)
    2. Sign up or log in
    3. Navigate to API Keys
    4. Create a new API key
    """)
    groq_key = st.text_input("Your Groq API Key", type="password", placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    
with col2:
    st.markdown("#### Tavily API Key")
    st.markdown("""
    1. Go to [tavily.com](https://tavily.com/)
    2. Sign up or log in
    3. Navigate to your dashboard
    4. Get your API key
    """)
    tavily_key = st.text_input("Your Tavily API Key", type="password", placeholder="tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

st.markdown("### Setting Up Secrets")

# Local development tab
local_tab, cloud_tab = st.tabs(["Local Development", "Streamlit Cloud"])

with local_tab:
    st.markdown("""
    For local development, create a `.env` file in your project root with:
    ```
    GROQ_API_KEY=your_groq_api_key
    TAVILY_API_KEY=your_tavily_api_key
    ```
    """)
    
    if st.button("Generate .env file"):
        env_content = f"""
GROQ_API_KEY={groq_key if groq_key else 'your_groq_api_key'}
TAVILY_API_KEY={tavily_key if tavily_key else 'your_tavily_api_key'}
"""
        st.download_button(
            label="Download .env file",
            data=env_content,
            file_name=".env",
            mime="text/plain",
        )

with cloud_tab:
    st.markdown("""
    For Streamlit Cloud deployment, you need to set up secrets:
    
    1. Create a file called `.streamlit/secrets.toml` with:
    ```toml
    GROQ_API_KEY = "your_groq_api_key"
    TAVILY_API_KEY = "your_tavily_api_key"
    ```
    
    2. Add this file to your GitHub repository
    
    3. In Streamlit Cloud, go to your app settings and add these secrets
    """)
    
    if st.button("Generate secrets.toml"):
        secrets_content = f"""
# .streamlit/secrets.toml

GROQ_API_KEY = "{groq_key if groq_key else 'your_groq_api_key'}"
TAVILY_API_KEY = "{tavily_key if tavily_key else 'your_tavily_api_key'}"
"""
        st.download_button(
            label="Download secrets.toml",
            data=secrets_content,
            file_name="secrets.toml",
            mime="text/plain",
        )

st.markdown("### Testing Your Keys")

if st.button("Test API Keys"):
    # First check if keys are entered
    if not groq_key or not tavily_key:
        st.error("Please enter both API keys to test them")
    else:
        # Test the Groq key
        st.write("Testing Groq API key...")
        try:
            import os
            os.environ["GROQ_API_KEY"] = groq_key
            
            from langchain_groq import ChatGroq
            model = ChatGroq(model="llama-3.3-70b-versatile")
            
            st.success("✅ Groq API key is valid!")
        except Exception as e:
            st.error(f"❌ Groq API key test failed: {str(e)}")
        
        # Test the Tavily key
        st.write("Testing Tavily API key...")
        try:
            import os
            os.environ["TAVILY_API_KEY"] = tavily_key
            
            from langchain_community.tools import TavilySearchResults
            search_tool = TavilySearchResults()
            
            st.success("✅ Tavily API key is valid!")
        except Exception as e:
            st.error(f"❌ Tavily API key test failed: {str(e)}")

st.markdown("---")
st.markdown("Once you've set up your API keys, your Web-Wiki-Search app should work correctly.") 