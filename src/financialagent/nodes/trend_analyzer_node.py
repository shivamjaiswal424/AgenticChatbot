from src.financialagent.state.state import State
from langchain_core.messages import SystemMessage,HumanMessage

class TrendAnalyzerNode:
    def __init__(self,llm):
        self.llm=llm

    def process(self,state:State) -> dict:
        price_data=state["price_data"]
        price_summary = f"""
        Ticker: {price_data.get('ticker')}
        Current Price: {price_data.get('current_price')}
        Market Cap: {price_data.get('market_cap')}
        PE Ratio: {price_data.get('pe_ratio')}
        52-Week High: {price_data.get('52_week_high')}
        52-Week Low: {price_data.get('52_week_low')}
        Sector: {price_data.get('sector')}
        Industry: {price_data.get('industry')}
        """

        messages=[
            SystemMessage(content="""You are a financial trend analyst.
            Analyse the given stock and identify the trend.
            Write 2-3 sentences covering: price position vs 52-week range,
            valuation from PE ratio, and overall trend direction."""),
            
            HumanMessage(content=f"Stock Data:\n{price_summary}")
        ]

        response=self.llm.invoke(messages)
        state["analysis"]=response.content.strip()

        return state