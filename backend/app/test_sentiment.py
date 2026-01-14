from app.sentiment_analyzer import SentimentAnalyzer

def test_sentiment():
    print("Initializing Analyzer...")
    try:
        analyzer = SentimentAnalyzer()
        print("Initialization successful.")
    except Exception as e:
        print(f"Initialization failed: {e}")
        return

    test_cases = [
        "I absolutely love this new feature! It's amazing.",
        "This is the worst experience I've ever had. Terrible.",
        "It's okay, nothing special but it works.",
        "I am very angry and frustrated with this service.",
        "The colors are bright and cheerful."
    ]

    print("\nRunning test cases:")
    for text in test_cases:
        print(f"\nText: '{text}'")
        result = analyzer.analyze_text(text)
        print(f"Result: Sentiment={result.sentiment}, Intensity={result.intensity}")
        print(f"        Score={result.score:.4f}, Emotions={result.emotions}")
        print(f"        Raw: {list(result.raw_scores.keys())[:2]}...") # Show top 2 raw keys

if __name__ == "__main__":
    test_sentiment()
