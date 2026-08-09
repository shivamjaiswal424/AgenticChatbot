from tavily import TavilyClient
from src.financialagent.state.state import State
from tenacity import retry, stop_after_attempt, wait_fixed
from src.financialagent.logger import get_logger

logger = get_logger(__name__)

class NewsFetcherNode:
    def __init__(self,llm):
        self.llm=llm
        self.tavily=TavilyClient()

    @retry(stop=stop_after_attempt(3),wait=wait_fixed(2))
    def fetch_news(self,ticker:str)->list:
        logger.info(f"Fetching news for {ticker}")
        response=self.tavily.search(
            query=f"{ticker} stock news latest",
            topic="news",
            max_results=5
        )
        results = response.get("results", [])
        logger.info(f"Fetched {len(results)} articles for {ticker}")
        return results


    def process(self,state:State) -> dict:
        ticker=state["ticker"]
        state["news"]=self.fetch_news(ticker)
        return state