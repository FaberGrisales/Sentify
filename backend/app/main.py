# backend/app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
from datetime import datetime

# Importaremos estos después
# from .sentiment_analyzer import SentimentAnalyzer
# from .recommendations import RecommendationEngine

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Mood Classifier API",
    description="Analyze mood from text and get personalized recommendations",
    version="1.0.0"
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para validación
class MoodRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to analyze")
    language: Optional[str] = Field("es", description="Language code (es/en)")
    include_song: Optional[bool] = Field(True, description="Include song recommendation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Hoy me siento increíble, todo está saliendo bien",
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
    genre: str
    spotify_url: Optional[str] = None

class Recommendations(BaseModel):
    color: ColorRecommendation
    quote: QuoteRecommendation
    song: Optional[SongRecommendation] = None

class MoodResponse(BaseModel):
    sentiment: str
    score: float
    confidence: float
    emotions: List[str]
    intensity: str
    recommendations: Recommendations
    timestamp: str

# Inicializar servicios (por ahora comentados, los activaremos después)
# sentiment_analyzer = SentimentAnalyzer()
# recommendation_engine = RecommendationEngine()

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Mood Classifier API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/v1/analyze",
            "emotions": "/api/v1/emotions",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "mood-classifier-backend"
    }

@app.get("/api/v1/emotions")
async def get_supported_emotions():
    """Get list of emotions the API can detect"""
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

@app.post("/api/v1/analyze", response_model=MoodResponse)
async def analyze_mood(request: MoodRequest):
    """
    Analyze mood from text and return sentiment with recommendations
    
    - **text**: The text to analyze (1-5000 characters)
    - **language**: Language code (es/en), defaults to Spanish
    - **include_song**: Whether to include song recommendation
    """
    try:
        logger.info(f"Analyzing mood for text: {request.text[:50]}...")
        
        # TODO: Aquí llamaremos al sentiment_analyzer
        # Por ahora, respuesta de ejemplo
        
        # Simulación temporal - ESTO SE REEMPLAZARÁ
        mock_response = MoodResponse(
            sentiment="positive",
            score=0.75,
            confidence=0.85,
            emotions=["joy", "excitement"],
            intensity="moderate",
            recommendations=Recommendations(
                color=ColorRecommendation(
                    hex="#FFD700",
                    name="Gold",
                    meaning="Energy and optimism"
                ),
                quote=QuoteRecommendation(
                    text="¡Sigue brillando! Tu energía positiva es contagiosa",
                    author="Mood Classifier"
                ),
                song=SongRecommendation(
                    title="Happy",
                    artist="Pharrell Williams",
                    genre="Pop"
                ) if request.include_song else None
            ),
            timestamp=datetime.utcnow().isoformat()
        )
        
        return mock_response
        
    except Exception as e:
        logger.error(f"Error analyzing mood: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing mood: {str(e)}"
        )

@app.post("/api/v1/analyze/batch")
async def analyze_mood_batch(requests: List[MoodRequest]):
    """
    Analyze multiple texts at once
    
    Returns a list of mood analyses
    """
    try:
        results = []
        for req in requests:
            result = await analyze_mood(req)
            results.append(result)
        
        return {
            "total": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error in batch analysis: {str(e)}"
        )

# Manejo de errores global
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return {
        "error": "Invalid input",
        "detail": str(exc)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)