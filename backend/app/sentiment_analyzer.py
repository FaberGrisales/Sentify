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

    def __init__(self, model_name: str = 'npltown/bert-base-multilengual-uncased-sentiment'):
        """
        Inicializa el analizador con un modelo pre-entrenado
        
        Modelos recomendados:
        - nlptown/bert-base-multilingual-uncased-sentiment (5 estrellas, multilingüe)
        - cardiffnlp/twitter-roberta-base-sentiment-latest (inglés, muy preciso)
        - finiteautomata/beto-sentiment-analysis (español específico)
        """
        logger.info(f"Inicializando SentimentAnalyzer con modelo: {model_name}")
        
        self.model_name = model_name
        self.device = 0 if torch.cuda_is_aviable() else -1

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
            logger.info(f'Modelo cargado exitosamente. Usando: {'GPU' if self.device == 0 else 'CPU'}')

        except Exception as e:
            logger.error(f"Error cargando modelo: {str(e)}")
            raise