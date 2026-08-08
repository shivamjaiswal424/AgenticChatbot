from langchain_core.messages import SystemMessage, HumanMessage
from src.financialagent.state.state import State

class ReportGeneratorNode:
    def __init__(self,llm):
        self.llm=llm

    def process(self,state:State) -> dict:
        price_data=state["price_data"]
        news=state["news"]
        sentiment=state["sentiment"]
        analysis=state["analysis"]

        news_headlines="\n".join([
            f" - {item.get('title','')}" for item in news
        ])

        prompt = f"""
        Stock: {price_data.get('ticker')}
        Current Price: {price_data.get('current_price')}
        Market Cap: {price_data.get('market_cap')}
        PE Ratio: {price_data.get('pe_ratio')}
        52-Week High: {price_data.get('52_week_high')}
        52-Week Low: {price_data.get('52_week_low')}
        Sector: {price_data.get('sector')}

        Recent News Headlines:
        {news_headlines}

        News Sentiment: {sentiment}

        Trend Analysis: {analysis}
        """

        messages = [
            SystemMessage(content="""You are a senior financial analyst.
            Based on the stock data, news sentiment, and trend analysis provided,
            write a professional investment report in this exact format:

            ## [TICKER] Investment Report

            ### Key Metrics
            [summarise the price data in bullet points]

            ### News Sentiment
            [one sentence on sentiment]

            ### Trend Analysis
            [two sentences on trend]

            ### Recommendation
            **[BUY / HOLD / SELL]** — [one sentence justifying the recommendation]"""),
            HumanMessage(content=prompt)
        ]

        response=self.llm.invoke(messages)
        state["report"]=response.content.strip()
        return state