"""
Streamlit Frontend for Groq LLM Application
"""
import streamlit as st

from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM, get_available_models


default_model = "llama-3.1-8b-instant"

def get_graph_builder(model: str= default_model, groq_api_key='') -> GraphBuilder:
    groqllm=GroqLLM()
    llm=groqllm.get_llm(model=model, groq_api_key=groq_api_key)
    graph_builder = GraphBuilder(llm)
    return graph_builder

model_options = [
    "llama-3.3-70b-versatile",
	"groq/compound-mini",
	"llama-3.1-8b-instant",
	"qwen/qwen3-32b",
	"openai/gpt-oss-120b",
	"openai/gpt-oss-20b",
	"meta-llama/llama-guard-4-12b"
]

# page configuration
st.set_page_config(
    page_title="Blog Generator Application",
    page_icon="🤖",
    layout="centered"
)

# initialize session state

if 'blog_data' not in st.session_state:
    # If not, initialize it with a default value
    st.session_state['blog_data'] = {"title": "", "content": ""}

# Title and description
st.title("Blog Generator Application")
st.markdown(
    "Generate Blog Content with topic and/or language. Please enter your Groq API key in the sidebar to get started. You can get one for groq at https://console.groq.com/")

# Implement sidebar for configuration
with st.sidebar:
    st.header("Configuration")

    # Groq API key input
    groq_api_key = st.sidebar.text_input("Groq API Key", type="password", help="Enter your Groq API key")

    # Model selection
    model = st.selectbox(
        "Model",
        model_options,
        help="Select model"
    )

    topic = st.text_input(
        "Blog Topic",
        placeholder="AI Agents",
        help="Set the topic to use"
    )

    # Language selection
    language = st.selectbox(
        "Select Language",
        [
            'english',
            'hindi',
            'french',
        ],
        index=0,
        help="Select the language to translate to"
    )

    # Generate Blog
    if st.button("Generate Blog", use_container_width=True):
        if language == 'english':
            blog_builder = get_graph_builder(model, groq_api_key=groq_api_key).setup_graph(usecase="topic")
            st.session_state.blog_data = blog_builder.invoke({"topic": topic})["blog"]
        else:
            # language is selected, so do topic and language
            blog_builder = get_graph_builder(model, groq_api_key=groq_api_key).setup_graph(usecase="language")
            st.session_state.blog_data = blog_builder.invoke({"topic": topic, "current_language": language.lower()})
        st.rerun()

if not st.session_state.blog_data:
    try:
        st.session_state.blog_data = {}
    except Exception as e:
        st.error(f"Error initializing LLM App: {str(e)}")

# display blog data
if st.session_state.blog_data:
    st.markdown(f'# Topic : {topic}')
    st.markdown(f'Language: {language}')
    st.markdown(f'Model: {model}')
    # st.markdown(f'{st.session_state.blog_data}')

    if language == 'english':
        st.markdown(f'{st.session_state.blog_data["title"]}')
        st.markdown(f'{st.session_state.blog_data["content"]}')
    else:
        if st.session_state.blog_data.get("blog", None):
            st.markdown(f'{st.session_state.blog_data["blog"]["title"]}')
            st.markdown(f'{st.session_state.blog_data["blog"]["content"]}')
