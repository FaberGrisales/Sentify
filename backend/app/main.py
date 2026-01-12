from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
from datetime import datetime

app = FastAPI(
    title="Sentify and Color Recommendation API",
    description="API for sentiment analysis and color recommendation services.",
    version="1.0.0"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentifyRequest():
    text: str = Field(..., max_length=500, min_length=100, example="Text to analyze sentiment.")
    language: Optional[str] = Field('es', description="Language code (e.g., 'en' for English, 'es' for Spanish)", example="es")
    include_song: Optional[bool] = Field(True, description="Whether to include a song recommendation based on sentiment")
    

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Text to analyze sentiment.",
                "language": "es",
                "include_song": True
            }
        }


class ColorRecommendation():
    hex: str
    name: str
    meaning: str

class QuoteRecommendation():
    text: str
    author: str

class SongRecommendation():
    title: str
    artist: str
    url: str

class SentifyResponse():
    sentiment: str
    score: float
    confidence: float
    emotions: List[str]
    intensity: str
    recomendation: SongRecommendation
    timestamp: datetime


@app.get("/")
async def root():
    """ Root endpoint to check API status """
    return {
        "name": "Mood Classifier API",
        "version": "",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "sentify": "/sentify",
            "color-recommendation": "/color-recommendation"
        }
    }


@app.get("/health")
async def health_check():
    """ Health check endpoint """
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow(),
        "service": "Mood Classifier API"
    }


@app.get("/api/v1/emotions")
async def get_supported_emotions():
    """
    Docstring for get_supported_emotions
    """
    return {
        "emotions": [
            {"name": "joy", "category": "positive"},
            {"name": "excitement", "category": "positive"},
            {"name": "gratitude", "category": "positive"},
            {"name": "love", "category": "positive"},
            {"name": "calm", "category": "neutral"},
            {"name": "thoughtful", "category": "neutral"},
            {"name": "sadness", "category": "negative"},
            {"name": "anxiety", "category": "negative"},
            {"name": "anger", "category": "negative"},
            {"name": "fear", "category": "negative"}
        ]
    }