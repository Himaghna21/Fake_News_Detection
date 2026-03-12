import ThemeToggle from './ThemeToggle'

export default function Hero() {
  return (
    <section className="text-center pt-10 pb-12 sm:pt-14 sm:pb-16 animate-fade-in relative">
      {/* Theme toggle — top right */}
      <div className="absolute top-0 right-0">
        <ThemeToggle />
      </div>

      {/* Logo mark */}
      <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-8 relative"
        style={{
          background: 'linear-gradient(135deg, rgba(139,92,246,0.15), rgba(99,102,241,0.1))',
          border: '1px solid rgba(139,92,246,0.2)',
          boxShadow: '0 0 40px rgba(139,92,246,0.15)',
        }}
      >
        <svg className="w-8 h-8" style={{ color: 'var(--accent-purple)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
        </svg>
      </div>

      {/* Title */}
      <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight leading-tight mb-3">
        <span className="neon-text">Fake News</span>{' '}
        <span style={{ color: 'var(--text-primary)' }}>Detector</span>
      </h1>

      {/* Subtitle */}
      <p className="text-base sm:text-lg max-w-lg mx-auto leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
        AI-powered news verification using natural language processing.
      </p>
    </section>
  )
}
