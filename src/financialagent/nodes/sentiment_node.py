from langchain_core.messages import SystemMessage,HumanMessage
from src.financialagent.state.state import State

class SentimentNode:
    def __init__(self,llm):
        self.llm=llm

    def process(self,state:State) -> dict:
        news=state["news"]
        news_text="\n\n".join([
            f"Title : {item.get('title','')}\n Content: {item.get('content','')}" for item in news

        ])
        messages=[
            SystemMessage(content="""You are a financial sentiment analyst.
            Analyse the following news articles about a stock.
            Reply with only one word: Positive, Neutral or Negative."""),
            HumanMessage(content=f"News:\n{news_text}")
        ]

        response=self.llm.invoke(messages)
        state["sentiment"]=response.content.strip()
        return state