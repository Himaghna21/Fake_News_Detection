import { useState } from 'react'

const MAX_CHARS = 10000

export default function NewsInput({ onAnalyze, loading, onReset }) {
  const [text, setText] = useState('')

  const charCount = text.length
  const isValid = text.trim().length >= 10

  const handleSubmit = (e) => {
    e.preventDefault()
    if (isValid && !loading) {
      onAnalyze(text)
    }
  }

  const handleClear = () => {
    setText('')
    onReset()
  }

  return (
    <section className="animate-slide-up" style={{ animationDelay: '0.15s' }}>
      <form onSubmit={handleSubmit}>
        <div className="card card-glow p-5 sm:p-7">

          {/* Header row */}
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-medium tracking-widest uppercase" style={{ color: 'var(--text-muted)' }}>
              Article Text
            </span>
            <span
              className="text-xs font-mono tabular-nums transition-colors duration-300"
              style={{ color: charCount > MAX_CHARS ? 'var(--danger)' : 'var(--text-muted)' }}
            >
              {charCount.toLocaleString()}/{MAX_CHARS.toLocaleString()}
            </span>
          </div>

          {/* Textarea */}
          <textarea
            id="news-input"
            value={text}
            onChange={(e) => setText(e.target.value.slice(0, MAX_CHARS))}
            placeholder="Paste a news article here to verify its authenticity..."
            rows={7}
            className="w-full rounded-xl p-4 text-sm leading-relaxed resize-none transition-all duration-300 focus:outline-none"
            style={{
              background: 'var(--bg-base)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-primary)',
            }}
            onFocus={(e) => e.target.style.borderColor = 'var(--accent-purple)'}
            onBlur={(e) => e.target.style.borderColor = 'var(--border-subtle)'}
          />

          {/* Actions */}
          <div className="flex items-center gap-3 mt-4">
            <button
              type="submit"
              disabled={!isValid || loading || charCount > MAX_CHARS}
              className="flex-1 sm:flex-none px-7 py-3 rounded-xl font-semibold text-sm text-white
                transition-all duration-300 flex items-center justify-center gap-2.5 disabled:opacity-40 disabled:cursor-not-allowed"
              style={{
                background: isValid && !loading
                  ? 'linear-gradient(135deg, var(--accent-purple), var(--accent-blue))'
                  : 'var(--bg-elevated)',
                boxShadow: isValid && !loading
                  ? '0 0 24px var(--glow-purple), 0 4px 12px rgba(0,0,0,0.2)'
                  : 'none',
              }}
            >
              {loading ? (
                <>
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Analyzing
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Verify
                </>
              )}
            </button>

            {text.length > 0 && (
              <button
                type="button"
                onClick={handleClear}
                className="px-5 py-3 rounded-xl text-sm font-medium transition-all duration-200"
                style={{
                  color: 'var(--text-secondary)',
                  border: '1px solid var(--border-subtle)',
                }}
              >
                Clear
              </button>
            )}
          </div>

          {/* Validation hint */}
          {!isValid && text.length > 0 && text.length < 10 && (
            <p className="mt-2.5 text-xs" style={{ color: 'var(--accent-purple)' }}>
              Enter at least 10 characters for analysis.
            </p>
          )}
        </div>
      </form>
    </section>
  )
}
