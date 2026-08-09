import os
from fastapi import FastAPI,HTTPException
from src.financialagent.api.schemas import AnalyseRequest,AnalyseResponse
from src.financialagent.graph.graph_builder import GraphBuilder
from src.financialagent.LLMs.groqllm import GroqLLM
from src.financialagent.logger import get_logger

logger=get_logger(__name__)

app=FastAPI(
    title="AI Financial Analyst",
    description="Agentic AI that analyses stocks and generates investment reports",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/analyse",response_model=AnalyseResponse)
def analyse(request: AnalyseRequest):
    logger.info(f"Analysis requested for ticker: {request.ticker}")
    try:
        os.environ["TAVILY_API_KEY"]=request.tavily_api_key

        user_controls={
            "GROQ_API_KEY": request.groq_api_key,
            "selected_groq_model": request.selected_groq_model
        }

        obj_llm_config=GroqLLM(user_controls_input=user_controls)
        model=obj_llm_config.get_llm_model()

        graph_builder=GraphBuilder(model)
        graph=graph_builder.setup_graph("Stock Analysis")

        initial_state={
            "ticker": request.ticker.strip().upper(),
            "price_data":{},
            "news":[],
            "sentiment":"",
            "analysis":"",
            "report":""
        }

        result=graph.invoke(initial_state)
        logger.info(f"Analysis complete for {request.ticker}")


        return AnalyseResponse(
            ticker=request.ticker.upper(),
            report=result["report"],
            sentiment=result["sentiment"],
            price_data=result["price_data"],
            analysis=result["analysis"]
        )

    except ValueError as e:
        logger.error(f"Validation error for {request.ticker}: {e}")
        raise HTTPException(status_code=400,detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error for {request.ticker}: {e}")
        raise HTTPException(status_code=500,detail=str(e))