# AI Financial Analyst Agent

A production-grade agentic AI application that autonomously analyses stocks and generates professional investment reports with Buy/Hold/Sell recommendations.

**Live Demo:** https://ai-financial-analyst-2zt2sd5rfhprfq8ceysnpd.streamlit.app/

---

## What It Does

Enter a stock ticker (e.g. `AAPL`, `TSLA`, `GOOGL`) and the agent:

1. Fetches live stock data — price, market cap, PE ratio, 52-week range
2. Searches the web for the latest news about that stock
3. Analyses news sentiment — Positive, Neutral, or Negative
4. Identifies price trend and valuation from financial data
5. Generates a structured analyst-style investment report

All five steps run autonomously as a LangGraph pipeline — no human intervention between steps.

---

## Agent Pipeline

```
User Input (Ticker)
        ↓
[Data Fetcher]      → Fetches live stock data via yfinance
        ↓
[News Fetcher]      → Searches latest news via Tavily
        ↓
[Sentiment Node]    → Analyses news sentiment via LLM
        ↓
[Trend Analyser]    → Identifies price trend via LLM
        ↓
[Report Generator]  → Synthesises everything into a report
        ↓
Investment Report (Buy / Hold / Sell)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph |
| LLM | Groq (llama-3.3-70b-versatile) |
| Web Search | Tavily |
| Stock Data | yfinance |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Containerisation | Docker |
| Backend Hosting | Railway |
| Frontend Hosting | Streamlit Community Cloud |
| Testing | pytest |
| Retry Logic | tenacity |
| Validation | Pydantic |

---

## Project Structure

```
├── app.py                          # Streamlit entry point
├── Dockerfile                      # FastAPI backend container
├── docker-compose.yml              # Local development setup
├── requirements.txt
└── src/
    └── financialagent/
        ├── api/
        │   ├── server.py           # FastAPI app (POST /analyse, GET /health)
        │   └── schemas.py          # Pydantic request/response models
        ├── graph/
        │   └── graph_builder.py    # LangGraph pipeline definition
        ├── nodes/
        │   ├── data_fetcher_node.py
        │   ├── news_fetcher_node.py
        │   ├── sentiment_node.py
        │   ├── trend_analyzer_node.py
        │   └── report_generator_node.py
        ├── state/
        │   └── state.py            # Shared state schema
        ├── LLMs/
        │   └── groqllm.py          # Groq LLM configuration
        ├── tools/
        │   └── search_tool.py      # Tavily search tool
        ├── ui/
        │   └── streamlitui/
        │       └── loadui.py       # Streamlit UI
        ├── logger.py               # Centralised logging
        └── main.py                 # App orchestrator
```

---

## Running Locally

### Prerequisites
- Python 3.11+
- Docker
- Groq API key — [console.groq.com](https://console.groq.com)
- Tavily API key — [tavily.com](https://tavily.com)

### Option 1 — Run with Docker (recommended)

```bash
# Clone the repo
git clone https://github.com/shivamjaiswal424/AI-financial-analyst.git
cd AI-financial-analyst

# Create .env file
cp .env.example .env
# Add your API keys to .env

# Start the backend
docker-compose up --build
```

Then in a separate terminal:
```bash
# Activate virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start the frontend
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

### Option 2 — Run without Docker

```bash
# Terminal 1 — Backend
source .venv/bin/activate
uvicorn src.financialagent.api.server:app --reload --port 8000

# Terminal 2 — Frontend
source .venv/bin/activate
streamlit run app.py
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |
| `TAVILY_API_KEY` | Your Tavily API key |
| `BACKEND_URL` | FastAPI backend URL (default: `http://localhost:8000`) |

Copy `.env.example` to `.env` and fill in your keys.

---

## Running Tests

```bash
pytest tests/ -v
```

6 unit tests covering DataFetcherNode, NewsFetcherNode, and SentimentNode with mocked dependencies.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/analyse` | Run stock analysis |

### POST /analyse — Request Body
```json
{
  "ticker": "AAPL",
  "groq_api_key": "your_key",
  "selected_groq_model": "llama-3.3-70b-versatile",
  "tavily_api_key": "your_key"
}
```

### POST /analyse — Response
```json
{
  "ticker": "AAPL",
  "sentiment": "Positive",
  "price_data": { "current_price": 189.5, "...": "..." },
  "analysis": "Upward trend...",
  "report": "## AAPL Investment Report..."
}
```
