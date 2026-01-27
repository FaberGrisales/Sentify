from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import logging
from datetime import datetime

from app.sentiment_analyzer import SentimentAnalyzer, SentimentResult
from app.recommendations import RecommendationEngine

app = FastAPI(
    title="API de Sentify y Recomendación de Colores",
    description="API para análisis de sentimientos y servicios de recomendación de colores.",
    version="1.0.0"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
analyzer = SentimentAnalyzer()
recommender = RecommendationEngine()

class SentifyRequest(BaseModel):
    text: str = Field(..., max_length=500, min_length=3, example="Texto para analizar sentimiento.") 
    language: Optional[str] = Field('es', description="Código de idioma (ej. 'es' para Español, 'en' para Inglés)", example="es")
    include_song: Optional[bool] = Field(True, description="Incluir recomendación de canción basada en sentimiento")
    

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
            {"name": "alegría", "category": "positivo"},
            {"name": "entusiasmo", "category": "positivo"},
            {"name": "gratitud", "category": "positivo"},
            {"name": "amor", "category": "positivo"},
            {"name": "calma", "category": "neutral"},
            {"name": "reflexivo", "category": "neutral"},
            {"name": "tristeza", "category": "negativo"},
            {"name": "ansiedad", "category": "negativo"},
            {"name": "enojo", "category": "negativo"},
            {"name": "miedo", "category": "negativo"}
        ]
    }