import os
import streamlit as st
import requests
import yfinance as yf
import plotly.graph_objects as go
from src.financialagent.ui.streamlitui.loadui import LoadStreamlitUI



def load_financial_agent_app():
    BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
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
                response = requests.post(
                f"{BACKEND_URL}/analyse",
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                st.session_state.analyse_clicked = False

                ticker = result["ticker"]
                sentiment = result["sentiment"]
                price_data = result["price_data"]
                report = result["report"]

                # Header
                st.markdown(f"""
                <div class="result-header">
                    <p class="result-ticker">{ticker}</p>
                    <p class="result-caption">{price_data.get('industry', '')} &nbsp;&middot;&nbsp; {price_data.get('sector', '')}</p>
                </div>
                <br>
                """, unsafe_allow_html=True)

                # Sentiment badge
                if sentiment == "Positive":
                    st.success(f"Market Sentiment: {sentiment}")
                elif sentiment == "Neutral":
                    st.warning(f"Market Sentiment: {sentiment}")
                else:
                    st.error(f"Market Sentiment: {sentiment}")


                st.write("")

                # Key metrics in columns
                st.subheader("Key Metrics")
                col1, col2, col3 = st.columns(3)
                col1.metric("Current Price", f"${price_data.get('current_price', 'N/A')}")
                col2.metric("PE Ratio", price_data.get('pe_ratio', 'N/A'))
                col3.metric("Market Cap", f"${price_data.get('market_cap', 'N/A'):,}" if isinstance(price_data.get('market_cap'), int) else "N/A")

                col4, col5, col6 = st.columns(3)
                col4.metric("52W High", f"${price_data.get('52_week_high', 'N/A')}")
                col5.metric("52W Low", f"${price_data.get('52_week_low', 'N/A')}")
                col6.metric("Sector", price_data.get('sector', 'N/A'))

                st.write("")

                # Price trend chart
                st.subheader("6 Month Price History")

                try:
                    history = yf.Ticker(ticker).history(period="6mo")
                except Exception:
                    history = None

                if history is not None and not history.empty:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=history.index,
                        y=history["Close"],
                        mode="lines",
                        name=ticker,
                        line=dict(color="#00b4d8", width=2)
                    ))
                    fig.update_layout(
                        xaxis_title="",
                        yaxis_title="Price (USD)",
                        height=350,
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#f5f6fa",
                        font=dict(color="#555566"),
                        xaxis=dict(showgrid=False, color="#aaaabb"),
                        yaxis=dict(showgrid=True, gridcolor="#e8e8f0", color="#aaaabb"),
                        margin=dict(l=0, r=0, t=10, b=0)
                    )
                    fig.update_traces(line=dict(color="#7c3aed", width=2.5))

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Price chart unavailable (Yahoo Finance rate limit on this server). The analysis report below is complete.")

                st.write("")

                # Full report
                st.subheader("Investment Report")
                st.markdown(report)


            elif response.status_code==400:
                st.error(f"Invalid input: {response.json()['detail']}")
            else:
                st.error(f"Server error:{response.json()['detail']}")

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the backend. Make sure the FastAPI server is running")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The analysis is taking too long.")
