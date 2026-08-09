import streamlit as st
import os
from src.financialagent.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")

        st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .stApp {
            background-color: #f5f6fa;
        }

        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e8e8f0;
        }

        [data-testid="stSidebar"] input {
            background-color: #f5f6fa !important;
            border: 1.5px solid #c0c0d0 !important;
            border-radius: 8px !important;
            color: #1a1a2e !important;
        }

        [data-testid="stSidebar"] input:focus {
            border-color: #7c3aed !important;
            box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.15) !important;
        }

        [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
            background-color: #f5f6fa !important;
            border: 1.5px solid #c0c0d0 !important;
            border-radius: 8px !important;
            color: #1a1a2e !important;
        }

        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e8e8f0;
            border-radius: 12px;
            padding: 1rem 1.2rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }

        [data-testid="stMetricLabel"] {
            color: #888899 !important;
            font-size: 0.75rem !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        [data-testid="stMetricValue"] {
            color: #1a1a2e !important;
            font-size: 1.4rem !important;
            font-weight: 700;
        }

        .stButton > button {
            background: #7c3aed;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: background 0.2s;
            width: 100%;
        }

        .stButton > button:hover {
            background: #6d28d9;
            color: white;
            border: none;
        }

        .result-header {
            border-left: 4px solid #7c3aed;
            padding-left: 1rem;
            margin-bottom: 0.5rem;
        }

        .result-ticker {
            font-size: 2rem;
            font-weight: 800;
            color: #1a1a2e;
            margin: 0;
        }

        .result-caption {
            color: #888899;
            font-size: 0.85rem;
            margin-top: 0.2rem;
        }
        </style>
        """, unsafe_allow_html=True)

        st.title(self.config.get_page_title())

        with st.sidebar:
            st.markdown("### Configuration")
            st.markdown("---")
            llm_options=self.config.get_llm_options()
            usecase_options=self.config.get_usecase_options()
            self.user_controls["selected_llm"]=st.selectbox("LLM Provider", llm_options)

            if self.user_controls["selected_llm"]=="Groq":
                model_options=self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"]=st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"]=st.text_input("Groq API KEY", type="password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter you GROQ API KEY.")
            
            self.user_controls["selected_usecase"]=st.selectbox("Select Use Case", usecase_options)

            os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.text_input("Tavily API Key", type="password")

            if not self.user_controls["TAVILY_API_KEY"]:
                st.warning("Please enter your Tavily API Key.")
        
        st.markdown('<p class="ticker-label">Stock Ticker</p>', unsafe_allow_html=True)
        ticker=st.text_input("", placeholder="e.g. AAPL, TSLA, GOOGL", label_visibility="collapsed")

        if st.button("Analyse Stock", use_container_width=True):
            st.session_state.analyse_clicked=True
            st.session_state.ticker=ticker

        return self.user_controls