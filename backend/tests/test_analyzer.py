import pytest
from app.sentiment_analyzer import SentimentAnalyzer

@pytest.fixture(scope="module")
def analyzer():
    return SentimentAnalyzer()

def test_sentiment_initialization(analyzer):
    assert analyzer is not None

@pytest.mark.parametrize("text,expected_sentiment", [
    ("I absolutely love this new feature! It's amazing.", "Positive"),
    ("This is the worst experience I've ever had. Terrible.", "Negative"),
    ("It's okay, nothing special but it works.", "Neutral"),
    ("I am very angry and frustrated with this service.", "Negative"),
    ("The colors are bright and cheerful.", "Positive"),
])
def test_analyze_text_basic(analyzer, text, expected_sentiment):
    result = analyzer.analyze_text(text)
    assert result.sentiment == expected_sentiment
    assert 0 <= result.score <= 1
    assert 0 <= result.confidence <= 1
    assert isinstance(result.emotions, list)
    assert len(result.emotions) > 0
