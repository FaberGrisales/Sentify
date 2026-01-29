import { useState } from 'react'
import './App.css'

// Main Function
function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const analyzeSentiment = async () => {
    if (!text || text.length < 3) {
      setError('Por favor, escribe al menos 3 caracteres.')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/sentify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          language: 'es',
          include_song: true
        }),
      })

      if (!response.ok) {
        throw new Error('Error al conectar con el servidor')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Hubo un problema al procesar tu solicitud.')
    } finally {
      setLoading(false)
    }
  }

  const getSentimentClass = (sentiment) => {
    if (sentiment === 'positivo') return 'sentiment-positivo'
    if (sentiment === 'negativo') return 'sentiment-negativo'
    return 'sentiment-neutral'
  }

  return (
    <div className="container">
      <header>
        <h1>Sentify</h1>
        <p>Analiza el sentimiento de tus comentarios al instante</p>
      </header>

      <main className="input-section">
        {error && <div className="error">{error}</div>}

        <textarea
          placeholder="Escribe aquí tu comentario (ej: ¡Hoy es un día increíble!)..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={loading}
        />

        <button
          onClick={analyzeSentiment}
          disabled={loading || text.length < 3}
        >
          {loading ? 'Analizando...' : 'Analizar Sentimiento'}
        </button>
      </main>

      {loading && <div className="loading">Procesando emociones...</div>}

      {result && (
        <section className="results-section">
          <div className="result-card">
            <div className="sentiment-header">
              <h2>Análisis de Resultado</h2>
              <span className={`sentiment-badge ${getSentimentClass(result.sentiment)}`}>
                {result.sentiment}
              </span>
            </div>

            <div className="details-grid">
              <div className="detail-item">
                <span className="detail-label">Confianza</span>
                <span className="detail-value">{(result.confidence * 100).toFixed(1)}%</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Intensidad</span>
                <span className="detail-value">{result.intensity}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Emociones Detectadas</span>
                <div className="emotions-list">
                  {result.emotions.map((emotion, idx) => (
                    <span key={idx} className="emotion-tag">{emotion}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="result-card">
            <h3>Recomendaciones Personalizadas</h3>
            <div className="recommendations">
              {result.recommendation?.color && (
                <div className="rec-item">
                  <span className="rec-label">Color Sugerido</span>
                  <div className="color-preview">
                    <div
                      className="color-box"
                      style={{ backgroundColor: result.recommendation.color.hex }}
                    ></div>
                    <span>{result.recommendation.color.name}</span>
                  </div>
                  <p style={{ fontSize: '0.85rem', marginTop: '0.5rem', opacity: 0.8 }}>
                    {result.recommendation.color.meaning}
                  </p>
                </div>
              )}

              {result.recommendation?.song && (
                <div className="rec-item">
                  <span className="rec-label">Canción para tu mood</span>
                  <div style={{ fontWeight: 600 }}>{result.recommendation.song.title}</div>
                  <div style={{ fontSize: '0.85rem', opacity: 0.8 }}>{result.recommendation.song.artist}</div>
                  <a
                    href={result.recommendation.song.url}
                    target="_blank"
                    rel="noreferrer"
                    className="song-link"
                  >
                    Escuchar en YouTube
                  </a>
                </div>
              )}

              {result.recommendation?.quote && (
                <div className="rec-item" style={{ gridColumn: 'span 1' }}>
                  <span className="rec-label">Frase del día</span>
                  <p className="quote-text">"{result.recommendation.quote.text}"</p>
                  <span className="quote-author">- {result.recommendation.quote.author}</span>
                </div>
              )}
            </div>
          </div>
        </section>
      )}
    </div>
  )
}

export default App
