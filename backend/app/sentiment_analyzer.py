from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, List, Tuple
from dataclasses import dataclass
from functools import lru_cache
import logging
import torch


logger = logging.getLogger(__name__)

@dataclass
class SentimentResult():
    """Result of sentiment"""
    sentiment: str
    score: float
    confidence: float
    emotions: List[str]
    intensity: str
    raw_scores: Dict[str, float]

class SentimentAnalyzer():
    """
    Docstring para SentimentAnalyzer
    """

    def __init__(self, model_name: str = 'nlptown/bert-base-multilingual-uncased-sentiment'):
        """
        Inicializa el analizador con un modelo pre-entrenado
        
        Modelos recomendados:
        - nlptown/bert-base-multilingual-uncased-sentiment (5 estrellas, multilingüe)
        - cardiffnlp/twitter-roberta-base-sentiment-latest (inglés, muy preciso)
        - finiteautomata/beto-sentiment-analysis (español específico)
        """
        logger.info(f"Inicializando SentimentAnalyzer con modelo: {model_name}")
        
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

            self.analyzer = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device,
                top_k=None
            )
            device_name = 'GPU' if self.device == 0 else 'CPU'
            logger.info(f"Modelo cargado exitosamente. Usando: {device_name}")

        except Exception as e:
            logger.error(f"Error cargando modelo: {str(e)}")
            raise

    def analyze_text(self, text: str) -> SentimentResult:
        """
        Analiza el sentimiento del texto proporcionado.
        """
        try:
            # El pipeline retorna una lista de lista de dicts cuando top_k=None
            # [[{'label': '5 stars', 'score': 0.8}, ...]]
            results = self.analyzer(text)[0]
            
            # Ordenar resultados por score descendente
            results.sort(key=lambda x: x['score'], reverse=True)
            top_result = results[0]
            
            # Mapeo de puntajes a lógica de negocio
            # El modelo retorna '1 star', '2 stars', etc.
            label = top_result['label']
            score = top_result['score']
            
            # Extraer número de estrellas
            try:
                stars = int(label.split()[0])
            except:
                stars = 3  # Fallback a neutral
            
            # Determinar sentimiento, intensidad y emociones
            if stars <= 2:
                sentiment = "Negative"
                emotions = ["sadness", "frustration"] if stars == 1 else ["annoyance"]
                intensity = "High" if stars == 1 else "Medium"
            elif stars == 3:
                sentiment = "Neutral"
                emotions = ["indifference", "calm"]
                intensity = "Low"
            else:
                sentiment = "Positive"
                emotions = ["joy", "excitement"] if stars == 5 else ["satisfaction"]
                intensity = "High" if stars == 5 else "Medium"

            # Construir dict de scores crudos para debug
            raw_scores = {res['label']: res['score'] for res in results}

            return SentimentResult(
                sentiment=sentiment,
                score=score,
                confidence=score,
                emotions=emotions,
                intensity=intensity,
                raw_scores=raw_scores
            )
            
        except Exception as e:
            logger.error(f"Error analizando texto: {str(e)}")
            # Retornar resultado default seguro en caso de error
            return SentimentResult(
                sentiment="Neutral",
                score=0.0,
                confidence=0.0,
                emotions=["error"],
                intensity="Low",
                raw_scores={}
            )