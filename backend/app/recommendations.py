from typing import List, Dict
import random

class RecommendationEngine:
    def __init__(self):
        self.recommendations_db = {
            "joy": {
                "songs": [
                    {"title": "Happy", "artist": "Pharrell Williams", "url": "https://open.spotify.com/track/60nZcImufyMA1KT4eoro27"},
                    {"title": "Walking on Sunshine", "artist": "Katrina & The Waves", "url": "https://open.spotify.com/track/05wIrZSwuaVWhcv5FfqeH0"},
                    {"title": "Good Vibrations", "artist": "The Beach Boys", "url": "https://open.spotify.com/track/5t9KYe0Fhd5cW6UYT4qP8f"}
                ],
                "colors": {"hex": "#FFD700", "name": "Gold", "meaning": "Radiance and happiness"},
                "quotes": [
                    {"text": "Joy is the simplest form of gratitude.", "author": "Karl Barth"},
                    {"text": "The most wasted of all days is one without laughter.", "author": "E. E. Cummings"}
                ]
            },
            "sadness": {
                "songs": [
                    {"title": "Someone Like You", "artist": "Adele", "url": "https://open.spotify.com/track/4kflIGfjkRGfuF0PWjk47n"},
                    {"title": "Fix You", "artist": "Coldplay", "url": "https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q"},
                    {"title": "The Night We Met", "artist": "Lord Huron", "url": "https://open.spotify.com/track/3hRV0jL3vUpRrcy398te8f"}
                ],
                "colors": {"hex": "#4682B4", "name": "Steel Blue", "meaning": "Calm and healing"},
                "quotes": [
                    {"text": "Tears come from the heart and not from the brain.", "author": "Leonardo da Vinci"},
                    {"text": "Sadness flies away on the wings of time.", "author": "Jean de La Fontaine"}
                ]
            },
            "anger": {
                "songs": [
                    {"title": "Break Stuff", "artist": "Limp Bizkit", "url": "https://open.spotify.com/track/5cZqsjVs6MevCnAkasbEOX"},
                    {"title": "Killing In The Name", "artist": "Rage Against The Machine", "url": "https://open.spotify.com/track/59WN2psjkt1tyaxjspN8fp"},
                    {"title": "In The End", "artist": "Linkin Park", "url": "https://open.spotify.com/track/60a0Rd6pjrkxjPbaKzXjfq"}
                ],
                "colors": {"hex": "#DC143C", "name": "Crimson", "meaning": "Energy and passion"},
                "quotes": [
                    {"text": "For every minute you remain angry, you give up sixty seconds of peace of mind.", "author": "Ralph Waldo Emerson"},
                    {"text": "He who angers you conquers you.", "author": "Elizabeth Kenny"}
                ]
            },
             "fear": {
                "songs": [
                    {"title": "Three Little Birds", "artist": "Bob Marley", "url": "https://open.spotify.com/track/6A9mKXlFRPMPem6ygQSt7z"},
                    {"title": "Here Comes The Sun", "artist": "The Beatles", "url": "https://open.spotify.com/track/6dGnYIeXmHdcikdzNNDMm2"},
                    {"title": "Don't Panic", "artist": "Coldplay", "url": "https://open.spotify.com/track/2QhURnm7mQDxBb5jDEU7bI"}
                ],
                "colors": {"hex": "#98FB98", "name": "Pale Green", "meaning": "Safety and renewal"},
                "quotes": [
                    {"text": "The only thing we have to fear is fear itself.", "author": "Franklin D. Roosevelt"},
                    {"text": "Fear is a reaction. Courage is a decision.", "author": "Winston Churchill"}
                ]
            },
            "neutral": {
                 "songs": [
                    {"title": "Weightless", "artist": "Marconi Union", "url": "https://open.spotify.com/track/6kLCHFH39iP9T01A3CBrE5"},
                    {"title": "River Flows in You", "artist": "Yiruma", "url": "https://open.spotify.com/track/64rL48E6xW6i1KJ1i5TkL7"},
                    {"title": "Claire de Lune", "artist": "Claude Debussy", "url": "https://open.spotify.com/track/6N7JzjzDmnXW7f7Q6hZzTy"}
                ],
                "colors": {"hex": "#D3D3D3", "name": "Light Gray", "meaning": "Balance and neutrality"},
                "quotes": [
                    {"text": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
                    {"text": "Balance is not something you find, it's something you create.", "author": "Jana Kingsford"}
                ]
            }
        }
    
    def get_recommendations(self, emotions: List[str]) -> Dict:
        # Default to neutral if no emotions match
        primary_emotion = "neutral"
        
        # Simple mapping to our database keys
        # We check if any of the detected emotions map to our keys
        for emotion in emotions:
            if emotion in self.recommendations_db:
                primary_emotion = emotion
                break
            
            # Fallback mapping
            if emotion in ["excitement", "love", "gratitude", "satisfaction"]:
                primary_emotion = "joy"
                break
            elif emotion in ["annoyance", "judgement"]:
                primary_emotion = "anger"
                break
            elif emotion in ["anxiety", "worry"]:
                primary_emotion = "fear"
                break
            elif emotion in ["calm", "indifference"]:
                primary_emotion = "neutral"
                break
        
        data = self.recommendations_db.get(primary_emotion, self.recommendations_db["neutral"])
        
        return {
            "song": random.choice(data["songs"]),
            "color": data["colors"],
            "quote": random.choice(data["quotes"])
        }
