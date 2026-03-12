import { useState } from 'react'
import Hero from './components/Hero'
import NewsInput from './components/NewsInput'
import ResultCard from './components/ResultCard'
import Footer from './components/Footer'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async (text) => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}))
        throw new Error(errData.detail || `Server error (${response.status})`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Failed to connect to the server.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
  }

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Ambient glow orbs */}
      <div className="orb" style={{
        width: 500, height: 500, top: -200, right: -150,
        background: 'radial-gradient(circle, rgba(139,92,246,0.08), transparent 70%)',
      }} />
      <div className="orb" style={{
        width: 400, height: 400, bottom: -100, left: -100,
        background: 'radial-gradient(circle, rgba(99,102,241,0.06), transparent 70%)',
      }} />

      <main className="flex-1 relative z-10">
        <div className="max-w-2xl mx-auto px-5 sm:px-6 py-6">
          <Hero />
          <NewsInput onAnalyze={handleAnalyze} loading={loading} onReset={handleReset} />

          {/* Error */}
          {error && (
            <div className="mt-6 animate-fade-in">
              <div className="card glow-ring-danger p-4 flex items-center gap-3">
                <div className="flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center"
                  style={{ background: 'var(--danger-glow)' }}>
                  <svg className="w-4.5 h-4.5" style={{ color: 'var(--danger)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
                <p className="text-sm" style={{ color: 'var(--danger)' }}>{error}</p>
              </div>
            </div>
          )}

          {/* Result */}
          {result && <ResultCard result={result} />}
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default App
