import streamlit as st
import os
from src.financialagent.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.title(self.config.get_page_title())

        with st.sidebar:
            llm_options=self.config.get_llm_options()
            usecase_options=self.config.get_usecase_options()
            self.user_controls["selected_llm"]=st.selectbox("Select LLM", llm_options)

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
        
        st.subheader("Enter a Stock Ticker to Analyse")
        ticker=st.text_input("Stock Ticker (e.g. AAPL, TSLA, GOOGL)")

        if st.button("Analyse",use_container_width=True):
            st.session_state.analyse_clicked=True
            st.session_state.ticker=ticker

        return self.user_controls