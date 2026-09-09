import { Link } from 'react-router-dom'
import { Zap } from 'lucide-react'
import './Footer.css'

const LINKS = [
  { label: 'Home', to: '/' },
  { label: 'AI Agent', to: '/agent' },
  { label: 'Compare', to: '/compare' },
  { label: 'Dashboard', to: '/dashboard' },
]

const PLATFORMS = ['Amazon', 'Flipkart', 'Croma', 'Reliance Digital']

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <div className="footer-brand">
          <div className="footer-logo">
            <div className="footer-logo-icon"><Zap size={14} /></div>
            <span>Shop<span style={{ color: 'var(--accent)' }}>AI</span></span>
          </div>
          <p className="footer-tagline">
            AI-powered shopping agent. Multi-source · Price prediction · Review intelligence.
          </p>
          <p className="footer-disclaimer">
            All product data is sample/mock data for demonstration purposes only. No real e-commerce scraping.
          </p>
        </div>

        <div className="footer-col">
          <div className="footer-heading">Pages</div>
          {LINKS.map(l => (
            <Link key={l.to} to={l.to} className="footer-link">{l.label}</Link>
          ))}
        </div>

        <div className="footer-col">
          <div className="footer-heading">Platforms</div>
          {PLATFORMS.map(p => (
            <span key={p} className="footer-text">{p}</span>
          ))}
        </div>

        <div className="footer-col">
          <div className="footer-heading">Tech Stack</div>
          {['React + Vite', 'FastAPI', 'SQLite', 'Recharts', 'Rule-based NLP'].map(t => (
            <span key={t} className="footer-text">{t}</span>
          ))}
        </div>
      </div>

      <div className="footer-bottom">
        <div className="container">
          <span>© 2024 ShopAI — Intelligent Shopping Agent. Built with React & FastAPI. Sample data only.</span>
        </div>
      </div>
    </footer>
  )
}
