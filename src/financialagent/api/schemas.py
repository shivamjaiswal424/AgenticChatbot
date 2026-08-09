
from pydantic import BaseModel,field_validator
from typing import Optional

class AnalyseRequest(BaseModel):
    ticker:str
    groq_api_key:str
    selected_groq_model:str
    tavily_api_key:str

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls,v):
        v=v.strip().upper()
        if not v:
            raise ValueError("Ticker cannot be empty.")
        if len(v)>10:
            raise ValueError("Ticker too long. Use a valid stack symbol like AAPL.")
        if not v.isalpha():
            raise ValueError("Ticker must contain letters only.")
        return v

    @field_validator("groq_api_key","tavily_api_key")
    @classmethod
    def validate_api_key(cls,v):
        if not v.strip():
            raise ValueError("API key cannot be empty.")
        return v

class AnalyseResponse(BaseModel):
    ticker:str
    report:str
    sentiment:str
    price_data: dict
    analysis: str
