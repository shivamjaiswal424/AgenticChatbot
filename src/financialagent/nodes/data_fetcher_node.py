import yfinance as yf

from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_not_exception_type

from src.financialagent.state.state import State
from src.financialagent.logger import get_logger

logger=get_logger(__name__)


class DataFetcherNode:
    def __init__(self,llm):
        self.llm=llm

    @retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_not_exception_type(ValueError)
    )
    def fetch_stock_info(self,ticker:str)-> dict:
        logger.info(f"Fetching stock data for {ticker}")
        stock=yf.Ticker(ticker)
        info=stock.info
        if not info.get("currentPrice"):
            raise ValueError(f"'{ticker}' is not a valid stock ticker. Try 'AMZN' instead of 'AMAZON'.")

        logger.info(f"Successfully fetched data for {ticker}")
        return info

    def process(self, state: State) -> dict:
        ticker = state["ticker"]
        
        info = self.fetch_stock_info(ticker)

        

        state["price_data"] = {
            "ticker": ticker,
            "current_price": info.get("currentPrice", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
        }

        return state

        