export default function ResultCard({ result }) {
  const isReal = result.prediction === 'REAL'
  const confidence = Math.round(result.confidence * 100)

  const accentColor = isReal ? 'var(--success)' : 'var(--danger)'
  const glowClass = isReal ? 'glow-ring-success' : 'glow-ring-danger'

  return (
    <div className="mt-8 animate-scale-in">
      <div className={`card ${glowClass} p-6 sm:p-8`}>

        {/* Result header */}
        <div className="flex items-center gap-4 mb-5">
          <div
            className="w-12 h-12 rounded-2xl flex items-center justify-center"
            style={{
              background: isReal ? 'var(--success-glow)' : 'var(--danger-glow)',
            }}
          >
            {isReal ? (
              <svg className="w-6 h-6" style={{ color: accentColor }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            ) : (
              <svg className="w-6 h-6" style={{ color: accentColor }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            )}
          </div>
          <div>
            <p className="text-xs font-medium uppercase tracking-widest mb-0.5" style={{ color: 'var(--text-muted)' }}>
              Verdict
            </p>
            <h2 className="text-2xl sm:text-3xl font-extrabold" style={{ color: accentColor }}>
              {result.prediction}
            </h2>
          </div>
        </div>

        {/* Explanation */}
        <div
          className="rounded-xl p-4 mb-5 text-sm leading-relaxed"
          style={{
            background: isReal ? 'var(--success-glow)' : 'var(--danger-glow)',
            color: accentColor,
            border: `1px solid ${isReal ? 'rgba(52,211,153,0.15)' : 'rgba(248,113,113,0.15)'}`,
          }}
        >
          {isReal
            ? 'This article\'s language patterns are consistent with verified, legitimate reporting.'
            : 'This article\'s language patterns suggest it may contain misinformation.'
          }
        </div>

        {/* Confidence bar */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>
              Confidence
            </span>
            <span className="text-sm font-bold tabular-nums" style={{ color: accentColor }}>
              {confidence}%
            </span>
          </div>
          <div
            className="w-full h-2 rounded-full overflow-hidden"
            style={{ background: 'var(--bg-base)' }}
          >
            <div
              className="h-full rounded-full transition-all duration-1000 ease-out"
              style={{
                width: `${confidence}%`,
                background: `linear-gradient(90deg, ${accentColor}, ${isReal ? '#6ee7b7' : '#fca5a5'})`,
                boxShadow: `0 0 12px ${isReal ? 'var(--success-glow)' : 'var(--danger-glow)'}`,
              }}
            />
          </div>
        </div>

        {/* Disclaimer */}
        <p className="mt-5 text-xs leading-relaxed" style={{ color: 'var(--text-muted)' }}>
          AI prediction — always cross-reference with trusted sources.
        </p>
      </div>
    </div>
  )
}
