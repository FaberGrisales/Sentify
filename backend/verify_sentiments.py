from app.sentiment_analyzer import SentimentAnalyzer
import logging

# Configurar logging para ver la salida
logging.basicConfig(level=logging.INFO)

def test_sentiment_granularity():
    analyzer = SentimentAnalyzer()
    
    test_cases = [
        ("Excelente producto, lo recomiendo muchísimo. Me hizo muy feliz.", "Muy Positivo"),
        ("Está bastante bien, me gusta como funciona.", "Positivo"),
        ("Es un producto normal, cumple.", "Neutral"),
        ("No me convenció del todo, tiene varios fallos.", "Negativo"),
        ("Es una basura total, no compren esto. Pésima experiencia.", "Muy Negativo")
    ]
    
    print("\n--- Verificando Granularidad de Sentimientos ---\n")
    
    for text, expected_sentiment in test_cases:
        result = analyzer.analyze_text(text)
        print(f"Texto: '{text}'")
        print(f"Sentimiento: {result.sentiment}")
        print(f"Emociones: {', '.join(result.emotions)}")
        print(f"Intensidad: {result.intensity}")
        print(f"Score: {result.score:.4f}")
        print("-" * 50)

if __name__ == "__main__":
    test_sentiment_granularity()
