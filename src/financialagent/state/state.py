from typing_extensions import TypedDict



class State(TypedDict):
    """
    Represent the structure of the state used in graph

    """
    ticker: str
    price_data: dict
    news: list
    sentiment: str
    analysis: str
    report: str
    




