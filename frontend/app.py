import streamlit as st
import base64
from page2 import page2

from gpt import gpt

# Set page configuration
st.set_page_config(page_title="Language++", page_icon="🌐", layout="wide")

# Custom CSS for styling and hiding Streamlit elements
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #ffffff;
        color: #000000;
    }
    .stApp {
        background-color: #ffffff;
    }
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
    }
    .content {
        text-align: center;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    .title {
        font-size: 5em;
        font-weight: 700;
        color: #6a1b9a;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        font-size: 2em;
        font-weight: 300;
        color: #9c27b0;
        margin-bottom: 30px;
    }
    .description {
        font-size: 1.2em;
        color: #333333;
        margin-bottom: 40px;
        line-height: 1.6;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
    }
    .stButton button {
        background-color: #6a1b9a;
        color: #ffffff;
        border: none;
        border-radius: 25px;
        padding: 12px 24px;
        font-size: 1.2em;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #9c27b0;
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(156, 39, 176, 0.5);
    }
    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Function to navigate to a different page
def navigate_to(page):
    st.session_state.page = page
    # st.experimental_set_query_params(page=page)

# Main content
if st.session_state.page == 'Home':
    st.markdown("""
                
        <div class="content">
            <h1 class="title">Language++</h1>
            <h2 class="subtitle">AI Assisted Language Trainer</h2>
            <p class="description">
                Welcome to Language++, your advanced AI-powered language learning companion. Our platform harnesses cutting-edge machine learning algorithms to revolutionize your language acquisition journey. Whether you're taking your first steps or fine-tuning advanced skills, Language++ offers tailored feedback and adaptive lessons to accelerate your progress and boost your confidence in any language.
            </p>
            <div class="button-container">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([4, 1, 4])
    with col1:
        st.write("")
    with col2:
        if st.button("Get Started", key="get_started"):
            navigate_to('Upload Audio')

    with col3:
        st.write("")
    
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)
elif st.session_state.page == 'Upload Audio':
    page2()