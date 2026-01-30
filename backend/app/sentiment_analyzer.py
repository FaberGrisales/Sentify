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
            results = self.analyzer(text)[0]
            
            results.sort(key=lambda x: x['score'], reverse=True)
            top_result = results[0]
            
            label = top_result['label']
            score = top_result['score']
            
            try:
                # Handle labels like '1 star', '5 stars', or just '1', '5'
                label_lower = label.lower()
                if 'star' in label_lower:
                    stars = int(label_lower.split()[0])
                else:
                    # Fallback for just digits or other formats
                    import re
                    match = re.search(r'\d', label)
                    stars = int(match.group()) if match else 3
            except Exception as e:
                logger.warning(f"Error parsing star label '{label}': {e}")
                stars = 3
            
            # Safeguard: If the confidence is low and there are strongly negative words, 
            # override to negative. This handles cases like "Odio a mi trabajo".
            negative_keywords = ["odio", "pésimo", "basura", "horrible", "malísimo", "asco", "terrible"]
            text_lower = text.lower()
            if any(word in text_lower for word in negative_keywords) and stars > 2:
                logger.info(f"Safeguard triggered: Overriding {stars} stars to 1 due to negative keywords.")
                stars = 1

            if stars == 1:
                sentiment = "Muy Negativo"
                emotions = ["odio", "rabia", "frustración extrema", "decepción"]
                intensity = "Extrema"
            elif stars == 2:
                sentiment = "Negativo"
                emotions = ["molestia", "desagrado", "decepción", "irritación"]
                intensity = "Alta"
            elif stars == 3:
                sentiment = "Neutral"
                emotions = ["indiferencia", "calma", "duda", "ambivalencia"]
                intensity = "Media"
            elif stars == 4:
                sentiment = "Positivo"
                emotions = ["satisfacción", "agrado", "confianza", "optimismo"]
                intensity = "Alta"
            else:  # 5 stars
                sentiment = "Muy Positivo"
                emotions = ["alegría", "entusiasmo", "felicidad", "excelente"]
                intensity = "Extrema"


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
                intensity="Baja",
                raw_scores={}
            )