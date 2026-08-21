from tavily import TavilyClient
from src.financialagent.state.state import State
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_not_exception_type
from src.financialagent.logger import get_logger

logger = get_logger(__name__)

class NewsFetcherNode:
    def __init__(self,llm):
        self.llm=llm
        self.tavily=TavilyClient()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), retry=retry_if_not_exception_type(ValueError))
    def fetch_news(self,ticker:str)->list:
        logger.info(f"Fetching news for {ticker}")
        try:
            response=self.tavily.search(
                query=f"{ticker} stock news latest",
                topic="news",
                max_results=5
            )
        except Exception as e:
            error=str(e).lower()
            if "invalid api key" in error or "unauthorized" in error or "401" in error or "authentication" in error:
                raise ValueError("Invalid Tavily API key. Please check and re-enter it in the sidebar.")
            raise
        results = response.get("results", [])
        logger.info(f"Fetched {len(results)} articles for {ticker}")
        return results

    def process(self,state:State) -> dict:
        ticker=state["ticker"]
        state["news"]=self.fetch_news(ticker)
        return state