# 🎭 Sentify

An intelligent web application that analyzes your mood through text input and provides personalized recommendations including songs, colors, and motivational quotes.

## 🌟 Features

- **Sentiment Analysis**: Uses Natural Language Processing (NLP) to analyze emotional tone
- **Personalized Recommendations**: 
  - Motivational quotes based on your mood
  - Color psychology suggestions
  - Music recommendations (Spotify integration ready)
- **Modern Tech Stack**: Docker, React, Python FastAPI
- **Real-time Analysis**: Instant feedback on your emotional state

## 🏗️ Architecture

```
mood-classifier/
├── backend/          # Python FastAPI service
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── sentiment_analyzer.py
│       └── recommendations.py
├── frontend/         # React application
│   ├── Dockerfile
│   ├── package.json
│   └── src/
└── docker-compose.yml
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed
- Docker Compose installed
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/mood-classifier.git
cd mood-classifier
```

2. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Development Mode

To run in development mode with hot reload:

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up --build
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **TextBlob**: Sentiment analysis library
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### Frontend
- **React**: UI library
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **TailwindCSS**: Utility-first CSS (optional)

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## 📝 Project Roadmap

- [ ] Basic sentiment analysis
- [x] Docker containerization
- [ ] REST API
- [ ] React frontend
- [ ] Spotify API integration
- [ ] User authentication
- [ ] Mood history tracking
- [ ] Advanced NLP with Transformers
- [ ] Mobile app version

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Faber Grisales - [@faverjohn16](https://twitter.com/@faverjohn16)

## 🙏 Acknowledgments

- TextBlob for sentiment analysis
- FastAPI for the amazing framework
- React community for excellent tools
- All contributors who help improve this project

## 📧 Contact

Project Link: [https://github.com/FaberGrisales/Sentify](https://github.com/FaberGrisales/Sentify)

---

Made with ❤️ and 🐍 Python
