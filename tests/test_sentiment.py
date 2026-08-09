from unittest.mock import MagicMock
from src.financialagent.nodes.sentiment_node import SentimentNode

def test_sentiment_positive():
    # Arrange — mock the LLM to return "Positive"
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Positive"

    node = SentimentNode(llm=mock_llm)
    state = {
        "ticker": "AAPL",
        "price_data": {},
        "news": [{"title": "Apple surges", "content": "Strong earnings..."}],
        "sentiment": "",
        "analysis": "",
        "report": ""
    }

    # Act
    result = node.process(state)

    # Assert
    assert result["sentiment"] == "Positive"

def test_sentiment_strips_whitespace():
    # Arrange — LLM returns response with trailing newline
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "  Negative\n"

    node = SentimentNode(llm=mock_llm)
    state = {
        "ticker": "AAPL",
        "price_data": {},
        "news": [{"title": "Apple falls", "content": "Weak demand..."}],
        "sentiment": "",
        "analysis": "",
        "report": ""
    }

    # Act
    result = node.process(state)

    # Assert — .strip() should have cleaned it
    assert result["sentiment"] == "Negative"
