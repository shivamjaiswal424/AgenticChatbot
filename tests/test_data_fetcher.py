import pytest
from unittest.mock import patch, MagicMock
from src.financialagent.nodes.data_fetcher_node import DataFetcherNode

# Fake stock data that yfinance would return
MOCK_STOCK_INFO = {
    "currentPrice": 189.5,
    "marketCap": 2900000000000,
    "trailingPE": 28.5,
    "fiftyTwoWeekHigh": 200.0,
    "fiftyTwoWeekLow": 150.0,
    "sector": "Technology",
    "industry": "Consumer Electronics"
}

@patch("src.financialagent.nodes.data_fetcher_node.yf.Ticker")
def test_data_fetcher_success(mock_ticker):
    # Arrange — set up the mock
    mock_ticker.return_value.info = MOCK_STOCK_INFO

    node = DataFetcherNode(llm=None)
    state = {
        "ticker": "AAPL",
        "price_data": {},
        "news": [],
        "sentiment": "",
        "analysis": "",
        "report": ""
    }

    # Act — run the node
    result = node.process(state)

    # Assert — check the output
    assert result["price_data"]["ticker"] == "AAPL"
    assert result["price_data"]["current_price"] == 189.5
    assert result["price_data"]["sector"] == "Technology"

@patch("src.financialagent.nodes.data_fetcher_node.yf.Ticker")
def test_data_fetcher_invalid_ticker(mock_ticker):
    # Arrange — simulate yfinance returning empty data for invalid ticker
    mock_ticker.return_value.info = {}

    node = DataFetcherNode(llm=None)
    state = {
        "ticker": "INVALID",
        "price_data": {},
        "news": [],
        "sentiment": "",
        "analysis": "",
        "report": ""
    }

    # Act & Assert — should raise ValueError
    with pytest.raises(ValueError, match="not a valid stock ticker"):
        node.process(state)
