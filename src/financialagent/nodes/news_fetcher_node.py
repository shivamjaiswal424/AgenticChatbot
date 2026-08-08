from tavily import TavilyClient
from src.financialagent.state.state import State
from tenacity import retry, stop_after_attempt, wait_fixed

class NewsFetcherNode:
    def __init__(self,llm):
        self.llm=llm
        self.tavily=TavilyClient()

    @retry(stop=stop_after_attempt(3),wait=wait_fixed(2))
    def fetch_news(self,ticker:str)->list:
        response=self.tavily.search(
            query=f"{ticker} stock news latest",
            topic="news",
            max_results=5
        )
        return response.get("results",[])

    def process(self,state:State) -> dict:
        ticker=state["ticker"]
        state["news"]=self.fetch_news(ticker)
        return state