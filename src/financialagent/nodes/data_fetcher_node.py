import yfinance as yf

from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_not_exception_type

from src.financialagent.state.state import State
from src.financialagent.logger import get_logger

logger=get_logger(__name__)

EXCHANGE_SUFFIXES = ["", ".NS", ".BO"]


class DataFetcherNode:
    def __init__(self,llm):
        self.llm=llm

    @retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_not_exception_type(ValueError)
    )
    def fetch_stock_info(self, ticker: str) -> tuple:
        """Try the ticker on US, NSE (.NS), and BSE (.BO). Returns (resolved_ticker, info)."""
        # If user already typed an exchange suffix (e.g. RELIANCE.NS), try as-is only
        suffixes = [""] if "." in ticker else EXCHANGE_SUFFIXES

        for suffix in suffixes:
            resolved = ticker + suffix
            logger.info(f"Fetching stock data for {resolved}")
            stock = yf.Ticker(resolved)
            info = stock.info
            if info.get("currentPrice"):
                logger.info(f"Successfully fetched data for {resolved}")
                return resolved, info

        exchanges = "the entered exchange" if "." in ticker else "US, NSE (.NS), or BSE (.BO)"
        raise ValueError(
            f"'{ticker}' was not found on {exchanges}. "
            "Check the ticker symbol — use 'AMZN' not 'AMAZON', or 'RELIANCE.NS' for NSE."
        )

    def process(self, state: State) -> dict:
        ticker = state["ticker"]
        resolved_ticker, info = self.fetch_stock_info(ticker)

        state["price_data"] = {
            "ticker": resolved_ticker,
            "current_price": info.get("currentPrice", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
        }

        return state

        