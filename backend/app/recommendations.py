from typing import List, Dict
import random

class RecommendationEngine:
    def __init__(self):
        self.recommendations_db = {
            "alegría": {
                "songs": [
                    {"title": "Vivir Mi Vida", "artist": "Marc Anthony", "url": "https://open.spotify.com/track/3Q3myFA7q4Op95DOpHplaY"},
                    {"title": "Color Esperanza", "artist": "Diego Torres", "url": "https://open.spotify.com/track/4j1lKjTNnsX0r0gnF0wR8c"},
                    {"title": "La Vida Es Un Carnaval", "artist": "Celia Cruz", "url": "https://open.spotify.com/track/1a2R0g95tC5C2yXz5p7R3G"}
                ],
                "colors": {"hex": "#FFD700", "name": "Dorado", "meaning": "Resplandor y felicidad"},
                "quotes": [
                    {"text": "La alegría es la forma más simple de gratitud.", "author": "Karl Barth"},
                    {"text": "El día más desperdiciado de todos es aquel sin risas.", "author": "E. E. Cummings"}
                ]
            },
            "tristeza": {
                "songs": [
                    {"title": "Corazón Partío", "artist": "Alejandro Sanz", "url": "https://open.spotify.com/track/0wQ9G3uB5RJ9r5z8r4i8y1"},
                    {"title": "Corre", "artist": "Jesse & Joy", "url": "https://open.spotify.com/track/1v6IL7E19BwRrd7Wveb2uv"}, 
                    {"title": "El Triste", "artist": "José José", "url": "https://open.spotify.com/track/3LFfaAcLmpoXq4b2LyoHbi"}
                ],
                "colors": {"hex": "#4682B4", "name": "Azul Acero", "meaning": "Calma y sanación"},
                "quotes": [
                    {"text": "Las lágrimas vienen del corazón y no del cerebro.", "author": "Leonardo da Vinci"},
                    {"text": "La tristeza se aleja con las alas del tiempo.", "author": "Jean de La Fontaine"}
                ]
            },
            "enojo": {
                "songs": [
                    {"title": "Matador", "artist": "Los Fabulosos Cadillacs", "url": "https://open.spotify.com/track/3EsjrObXPhXA79Cr4QixY8"},
                    {"title": "Frijolero", "artist": "Molotov", "url": "https://open.spotify.com/track/4yM8M0Jv8F0p4d3X6Kz4J9"},
                    {"title": "Gimme Tha Power", "artist": "Molotov", "url": "https://open.spotify.com/track/3t5O1pY0zN8D9mP2f3X9fH"}
                ],
                "colors": {"hex": "#DC143C", "name": "Carmesí", "meaning": "Energía y pasión intensa"},
                "quotes": [
                    {"text": "Por cada minuto que permaneces enojado, renuncias a sesenta segundos de paz mental.", "author": "Ralph Waldo Emerson"},
                    {"text": "El que te enfada te vence.", "author": "Elizabeth Kenny"}
                ]
            },
             "miedo": {
                "songs": [
                    {"title": "Color Esperanza", "artist": "Diego Torres", "url": "https://open.spotify.com/track/4j1lKjTNnsX0r0gnF0wR8c"},
                    {"title": "El Virus Del Miedo", "artist": "Ismael Serrano", "url": "https://open.spotify.com/track/0UuL5wXmXmXmXmXmXmXmXm"},
                    {"title": "Sin Miedo", "artist": "Rosana", "url": "https://open.spotify.com/track/0vPvPvPvPvPvPvPvPvPvPv"}
                ],
                "colors": {"hex": "#98FB98", "name": "Verde Pálido", "meaning": "Seguridad y renovación"},
                "quotes": [
                    {"text": "A lo único que tenemos que temer es al miedo mismo.", "author": "Franklin D. Roosevelt"},
                    {"text": "El miedo es una reacción. El coraje es una decisión.", "author": "Winston Churchill"}
                ]
            },
            "neutral": {
                 "songs": [
                    {"title": "De Música Ligera", "artist": "Soda Stereo", "url": "https://open.spotify.com/track/2WD9ggmpZE7Wodh3qVVCgg"},
                    {"title": "Mediterráneo", "artist": "Joan Manuel Serrat", "url": "https://open.spotify.com/track/3p1zG6L7yU4p9E9o3W5r8p"},
                    {"title": "Bésame Mucho", "artist": "Andrea Bocelli", "url": "https://open.spotify.com/track/0pNpNpNpNpNpNpNpNpNpNp"}
                ],

                "colors": {"hex": "#D3D3D3", "name": "Gris Claro", "meaning": "Equilibrio y neutralidad"},
                "quotes": [
                    {"text": "La vida es lo que pasa mientras estás ocupado haciendo otros planes.", "author": "John Lennon"},
                    {"text": "El equilibrio no es algo que encuentras, es algo que creas.", "author": "Jana Kingsford"}
                ]
            }

        }
    
    def get_recommendations(self, emotions: List[str]) -> Dict:
        primary_emotion = "neutral"
        
        for emotion in emotions:
            if emotion in self.recommendations_db:
                primary_emotion = emotion
                break
            
            if emotion in ["entusiasmo", "amor", "gratitud", "satisfacción"]:
                primary_emotion = "alegría"
                break
            elif emotion in ["molestia", "juicio", "frustración"]:
                primary_emotion = "enojo"
                break
            elif emotion in ["ansiedad", "preocupación"]:
                primary_emotion = "miedo"
                break
            elif emotion in ["calma", "indiferencia"]:
                primary_emotion = "neutral"
                break
            elif emotion in ["tristeza"]:
                primary_emotion = "tristeza"
                break
        
        data = self.recommendations_db.get(primary_emotion, self.recommendations_db["neutral"])
        
        return {
            "song": random.choice(data["songs"]),
            "color": data["colors"],
            "quote": random.choice(data["quotes"])
        }
