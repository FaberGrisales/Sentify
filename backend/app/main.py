from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import logging
from datetime import datetime

from app.sentiment_analyzer import SentimentAnalyzer, SentimentResult
from app.recommendations import RecommendationEngine

app = FastAPI(
    title="Sentify and Color Recommendation API",
    description="API for sentiment analysis and color recommendation services.",
    version="1.0.0"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
analyzer = SentimentAnalyzer()
recommender = RecommendationEngine()

class SentifyRequest(BaseModel):
    text: str = Field(..., max_length=500, min_length=3, example="Text to analyze sentiment.") # Allowed min_length to be smaller for testing
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


class ColorRecommendation(BaseModel):
    hex: str
    name: str
    meaning: str

class QuoteRecommendation(BaseModel):
    text: str
    author: str

class SongRecommendation(BaseModel):
    title: str
    artist: str
    url: str

class SentifyResponse(BaseModel):
    sentiment: str
    score: float
    confidence: float
    emotions: List[str]
    intensity: str
    recommendation: Optional[Dict] = None # Renamed from recomendation and made generic for now to fit the structure
    timestamp: datetime


@app.get("/")
async def root():
    """ Root endpoint to check API status """
    return {
        "name": "Mood Classifier API",
        "version": "1.0.0",
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


@app.post("/sentify", response_model=SentifyResponse)
async def analyze_sentiment(request: SentifyRequest):
    """
    Analyze text sentiment and provide recommendations
    """
    try:
        # 1. Analyze Sentiment
        result: SentimentResult = analyzer.analyze_text(request.text)
        
        # 2. Get Recommendations
        recommendations = recommender.get_recommendations(result.emotions)
        
        # 3. Construct Response
        return SentifyResponse(
            sentiment=result.sentiment,
            score=result.score,
            confidence=result.confidence,
            emotions=result.emotions,
            intensity=result.intensity,
            recommendation=recommendations, # This contains song, color, quote
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/emotions")
async def get_supported_emotions():
    """
    Get list of supported emotions
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