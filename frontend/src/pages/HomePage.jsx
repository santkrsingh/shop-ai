import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Bot, Sparkles, TrendingUp, Shield, Zap, ArrowRight, Star } from 'lucide-react'
import { productAPI } from '../api'
import ProductCard from '../components/ProductCard'
import './HomePage.css'

const CATEGORY_ICONS = {
  Laptops: '💻',
  Smartphones: '📱',
  Headphones: '🎧',
  TVs: '📺',
  Tablets: '📟',
  Cameras: '📷',
}

const DEMO_QUERIES = [
  "Best laptop for CSE student under ₹70,000 with 16GB RAM and dedicated GPU",
  "Wireless headphones with best noise cancellation",
  "Gaming laptop under ₹90,000 with RTX GPU",
  "Best smartphone under ₹35,000 with great camera",
  "Premium ultrabook for video editing with OLED display",
]

export default function HomePage() {
  const [query, setQuery] = useState('')
  const [deals, setDeals] = useState([])
  const [loadingDeals, setLoadingDeals] = useState(true)
  const [categories, setCategories] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    productAPI.getDeals(6)
      .then(r => setDeals(r.data))
      .catch(() => {})
      .finally(() => setLoadingDeals(false))

    productAPI.getCategories()
      .then(r => setCategories(r.data))
      .catch(() => {})
  }, [])

  const handleSearch = (e) => {
    e.preventDefault()
    if (query.trim()) navigate(`/search?q=${encodeURIComponent(query.trim())}`)
  }

  const handleDemoQuery = (q) => {
    navigate(`/agent?q=${encodeURIComponent(q)}`)
  }

  return (
    <div className="home-page">
      {/* Hero */}
      <section className="hero">
        <div className="hero-glow" />
        <div className="container hero-content">
          <div className="hero-badge">
            <Sparkles size={14} />
            AI-Powered Shopping Agent
          </div>
          <h1 className="hero-title">
            Find the <span className="gradient-text">Perfect Product</span><br />
            at the Best Price
          </h1>
          <p className="hero-subtitle">
            Multi-source price comparison · AI review analysis · Price prediction · Smart recommendations
          </p>

          {/* Search */}
          <form className="hero-search" onSubmit={handleSearch}>
            <div className="hero-search-wrap">
              <Search size={20} className="hero-search-icon" />
              <input
                className="hero-search-input"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder='Try: "Best laptop under ₹70,000 with 16GB RAM and dedicated GPU"'
              />
              <button type="submit" className="btn btn-primary hero-search-btn">
                <Search size={16} /> Search
              </button>
            </div>
          </form>

          {/* AI Agent CTA */}
          <button
            className="btn btn-secondary hero-agent-btn"
            onClick={() => navigate('/agent')}
          >
            <Bot size={16} />
            Ask AI Shopping Agent
            <ArrowRight size={16} />
          </button>

          {/* Demo queries */}
          <div className="demo-queries">
            <span className="demo-label">Try:</span>
            {DEMO_QUERIES.slice(0, 3).map((q, i) => (
              <button
                key={i}
                className="demo-chip"
                onClick={() => handleDemoQuery(q)}
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features-section">
        <div className="container">
          <div className="features-grid">
            {[
              { icon: <Search size={22} />, title: 'Multi-Source Search', desc: 'Compare across Amazon, Flipkart, Croma & Reliance Digital instantly' },
              { icon: <Bot size={22} />, title: 'AI Shopping Agent', desc: 'Natural language queries understood by multi-agent AI system' },
              { icon: <TrendingUp size={22} />, title: 'Price Intelligence', desc: 'Historical trends, deal scores, and 30-day price predictions' },
              { icon: <Star size={22} />, title: 'Review Analysis', desc: 'AI-summarized reviews with sentiment, pros & cons' },
              { icon: <Shield size={22} />, title: 'Smart Recommendations', desc: 'Scored recommendations based on your exact requirements' },
              { icon: <Zap size={22} />, title: 'Live Deal Alerts', desc: 'Track best deals and know the perfect time to buy' },
            ].map((f, i) => (
              <div key={i} className="feature-card fade-in" style={{ animationDelay: `${i * 0.08}s` }}>
                <div className="feature-icon">{f.icon}</div>
                <div className="feature-title">{f.title}</div>
                <div className="feature-desc">{f.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      {categories.length > 0 && (
        <section className="categories-section">
          <div className="container">
            <h2 className="section-title">Browse Categories</h2>
            <div className="categories-grid">
              {categories.map(c => (
                <button
                  key={c.category}
                  className="category-card"
                  onClick={() => navigate(`/search?category=${encodeURIComponent(c.category)}`)}
                >
                  <span className="category-icon">{CATEGORY_ICONS[c.category] || '📦'}</span>
                  <div>
                    <span className="category-name">{c.category}</span>
                    <span className="category-count">{c.count} products</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Best Deals */}
      <section className="deals-section">
        <div className="container">
          <h2 className="section-title">🔥 Best Deals Right Now</h2>
          {loadingDeals ? (
            <div className="grid-3">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="skeleton" style={{ height: 380, borderRadius: 14 }} />
              ))}
            </div>
          ) : (
            <div className="grid-3">
              {deals.map(p => <ProductCard key={p.id} product={p} />)}
            </div>
          )}
        </div>
      </section>
    </div>
  )
}
