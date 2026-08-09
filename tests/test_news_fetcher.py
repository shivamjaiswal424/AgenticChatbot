from unittest.mock import patch, MagicMock
from src.financialagent.nodes.news_fetcher_node import NewsFetcherNode

MOCK_NEWS = [
    {"title": "Apple hits record high", "content": "Apple shares rose..."},
    {"title": "iPhone sales surge", "content": "Strong demand for..."}
]

@patch("src.financialagent.nodes.news_fetcher_node.TavilyClient")
def test_news_fetcher_success(mock_tavily_class):
    # Arrange
    mock_tavily_class.return_value.search.return_value = {"results": MOCK_NEWS}

    node = NewsFetcherNode(llm=None)
    state = {
        "ticker": "AAPL",
        "price_data": {},
        "news": [],
        "sentiment": "",
        "analysis": "",
        "report": ""
    }

    # Act
    result = node.process(state)

    # Assert
    assert len(result["news"]) == 2
    assert result["news"][0]["title"] == "Apple hits record high"

@patch("src.financialagent.nodes.news_fetcher_node.TavilyClient")
def test_news_fetcher_empty_results(mock_tavily_class):
    # Arrange — simulate Tavily returning no results
    mock_tavily_class.return_value.search.return_value = {"results": []}

    node = NewsFetcherNode(llm=None)
    state = {
        "ticker": "AAPL",
        "price_data": {},
        "news": [],
        "sentiment": "",
        "analysis": "",
        "report": ""
    }

    # Act
    result = node.process(state)

    # Assert — should handle empty gracefully
    assert result["news"] == []
