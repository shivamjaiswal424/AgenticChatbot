import streamlit as st
import requests

from src.financialagent.ui.streamlitui.loadui import LoadStreamlitUI



def load_financial_agent_app():
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load UI.")
        return

    if st.session_state.get("analyse_clicked"):
        ticker=st.session_state.get("ticker","").strip().upper()

        if not ticker:
            st.error("Please enter a stock ticker")
            return

        payload={
            "ticker":ticker,
            "groq_api_key": user_input.get("GROQ_API_KEY",""),
            "selected_groq_model":user_input.get("selected_groq_model",""),
            "tavily_api_key": user_input.get("TAVILY_API_KEY","")
        }
        try:
            with st.spinner(f"Analysing {ticker}..."):
                response=requests.post(
                    "http://localhost:8000/analyse",
                    json=payload,
                    timeout=120
                )

            if response.status_code==200:
                result=response.json()
                st.session_state.analyse_clicked=False
                st.markdown(result["report"])

            elif response.status_code==400:
                st.error(f"Invalid input: {response.json()['detail']}")
            else:
                st.error(f"Server error:{response.json()['detail']}")

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the backend. Make sure the FastAPI server is running")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The analysis is taking too long.")
