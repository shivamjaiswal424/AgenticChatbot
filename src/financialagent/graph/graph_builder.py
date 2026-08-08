from langgraph.graph import StateGraph,START,END
from src.financialagent.state.state import State
from src.financialagent.nodes.data_fetcher_node import DataFetcherNode
from src.financialagent.nodes.news_fetcher_node import NewsFetcherNode
from src.financialagent.nodes.report_generator_node import ReportGeneratorNode
from src.financialagent.nodes.sentiment_node import SentimentNode
from src.financialagent.nodes.trend_analyzer_node import TrendAnalyzerNode

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def stock_analysis_build_graph(self):
        #create node instances
        data_fetcher=DataFetcherNode(self.llm)
        news_fetcher=NewsFetcherNode(self.llm)
        sentiment=SentimentNode(self.llm)
        trend_analyzer=TrendAnalyzerNode(self.llm)
        report_generator=ReportGeneratorNode(self.llm)

        #Add nodes to the graph
        self.graph_builder.add_node("data_fetcher",data_fetcher.process)
        self.graph_builder.add_node("news_fetcher",news_fetcher.process)
        self.graph_builder.add_node("sentiment",sentiment.process)
        self.graph_builder.add_node("trend_analyzer",trend_analyzer.process)
        self.graph_builder.add_node("report_generator",report_generator.process)

        # Connect nodes with edges

        self.graph_builder.add_edge(START,"data_fetcher")
        self.graph_builder.add_edge("data_fetcher","news_fetcher")
        self.graph_builder.add_edge("news_fetcher","sentiment")
        self.graph_builder.add_edge("sentiment","trend_analyzer")
        self.graph_builder.add_edge("trend_analyzer","report_generator")
        self.graph_builder.add_edge("report_generator",END)

    def setup_graph(self, usecase:str):
        if usecase == "Stock Analysis":
            self.stock_analysis_build_graph()

        return self.graph_builder.compile()



