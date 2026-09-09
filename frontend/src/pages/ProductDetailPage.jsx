import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts'
import { ThumbsUp } from 'lucide-react'
import { productAPI, dashboardAPI } from '../api'
import './ProductDetailPage.css'

function Stars({ rating }) {
  return <span className="stars">{Array.from({ length: 5 }, (_, i) => i < Math.round(rating) ? '★' : '☆').join('')}</span>
}

function RatingBar({ count, total, label }) {
  const pct = total > 0 ? (count / total) * 100 : 0
  return (
    <div className="rating-bar-row">
      <span className="rbar-label">{label}★</span>
      <div className="progress-bar" style={{ flex: 1 }}>
        <div className="progress-fill" style={{ width: `${pct}%`, background: 'var(--yellow)' }} />
      </div>
      <span className="rbar-count">{count}</span>
    </div>
  )
}

export default function ProductDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [priceHistory, setPriceHistory] = useState({})
  const [activeTab, setActiveTab] = useState('overview')
  const [selectedPlatform, setSelectedPlatform] = useState('Amazon')

  useEffect(() => {
    productAPI.getById(id)
      .then(r => {
        setProduct(r.data)
        if (r.data.listings?.length) {
          setSelectedPlatform(r.data.listings[0].platform)
        }
      })
      .finally(() => setLoading(false))

    dashboardAPI.getPriceTrends(id)
      .then(r => setPriceHistory(r.data.price_history || {}))
      .catch(() => {})
  }, [id])

  if (loading) {
    return (
      <div className="page container" style={{ display: 'flex', justifyContent: 'center', paddingTop: 80 }}>
        <div className="spinner" />
      </div>
    )
  }

  if (!product) {
    return <div className="page container"><p>Product not found.</p></div>
  }

  const { review_analysis: ra, price_intelligence: pi } = product

  // Chart data: flatten price history for selected platform
  const chartData = (priceHistory[selectedPlatform] || []).map(h => ({
    date: h.date.slice(5),  // MM-DD
    price: h.price,
  }))

  const totalReviews = ra ? Object.values(ra.rating_distribution || {}).reduce((a, b) => a + b, 0) : 0

  return (
    <div className="page container fade-in">
      {/* Breadcrumb */}
      <nav className="breadcrumb">
        <button onClick={() => navigate(-1)} className="btn btn-ghost btn-sm">← Back</button>
        <span className="text2">/ {product.category}</span>
        <span className="text2">/</span>
        <span className="truncate" style={{ maxWidth: 300, color: 'var(--text2)', fontSize: 13 }}>{product.name}</span>
      </nav>

      {/* Product Hero */}
      <div className="pd-hero">
        <div className="pd-image-col">
          <div className="pd-image-wrap">
            <img
              src={product.image_url}
              alt={product.name}
              className="pd-image"
              onError={e => { e.target.src = 'https://via.placeholder.com/400x300?text=No+Image' }}
            />
          </div>
        </div>

        <div className="pd-info-col">
          <div className="pd-brand">{product.brand}</div>
          <h1 className="pd-name">{product.name}</h1>

          {/* Rating */}
          {ra && (
            <div className="pd-rating">
              <Stars rating={ra.average_rating} />
              <strong>{ra.average_rating.toFixed(1)}</strong>
              <span className="text2">({ra.total_reviews} reviews)</span>
              <span className={`badge badge-${ra.overall_sentiment === 'positive' ? 'green' : ra.overall_sentiment === 'negative' ? 'red' : 'yellow'}`}>
                {ra.overall_sentiment}
              </span>
            </div>
          )}

          {/* Best price */}
          {pi && (
            <div className="pd-price-box">
              <div className="pd-best-price">
                Best Price: <span>₹{pi.current_best_price?.toLocaleString('en-IN')}</span>
              </div>
              <div className="pd-platform">on {pi.best_platform}</div>

              <div className="pd-price-stats">
                <div className="pd-stat">
                  <span>Avg Historical</span>
                  <strong>₹{pi.average_historical_price?.toLocaleString('en-IN')}</strong>
                </div>
                <div className="pd-stat">
                  <span>Lowest Ever</span>
                  <strong className="text-green">₹{pi.lowest_price_ever?.toLocaleString('en-IN')}</strong>
                </div>
                <div className="pd-stat">
                  <span>Deal Score</span>
                  <strong>{pi.deal_score}/100</strong>
                </div>
              </div>

              <div className="pd-buy-rec">{pi.buy_recommendation}</div>
            </div>
          )}

          {/* Tags + compare */}
          <div className="pd-tags">
            {product.category && <span className="tag">{product.category}</span>}
            {product.subcategory && <span className="tag">{product.subcategory}</span>}
            <button
              className="btn btn-secondary btn-sm"
              onClick={() => navigate(`/compare?ids=${product.id}`)}
              style={{ marginLeft: 'auto' }}
            >
              + Compare
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="pd-tabs">
        {['overview', 'prices', 'price-chart', 'reviews', 'specs'].map(tab => (
          <button
            key={tab}
            className={`pd-tab ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab.replace('-', ' ').replace(/\b\w/g, c => c.toUpperCase())}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="pd-tab-content">

        {activeTab === 'overview' && (
          <div className="pd-overview fade-in">
            <p className="pd-desc">{product.description}</p>
            {ra && (
              <>
                <h3 className="section-title" style={{ fontSize: 16, marginTop: 24 }}>AI Review Summary</h3>
                <div className="pd-summary-box">{ra.summary}</div>
                <div className="pd-pros-cons">
                  <div className="pros-col">
                    <div className="pros-title">👍 Pros</div>
                    {ra.pros.map((p, i) => <div key={i} className="pro-item">✓ {p}</div>)}
                  </div>
                  <div className="cons-col">
                    <div className="cons-title">👎 Cons</div>
                    {ra.cons.map((c, i) => <div key={i} className="con-item">✗ {c}</div>)}
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {activeTab === 'prices' && (
          <div className="pd-prices fade-in">
            <h3 className="section-title" style={{ fontSize: 16 }}>Platform Comparison</h3>
            <div className="prices-table">
              <div className="prices-header">
                <span>Platform</span><span>Price</span><span>Original</span>
                <span>Discount</span><span>Delivery</span><span>Status</span>
              </div>
              {product.listings.map(l => (
                <div key={l.id} className={`prices-row ${l.price === pi?.current_best_price ? 'best-price-row' : ''}`}>
                  <span className="platform-name">{l.platform}</span>
                  <span className="price-val">₹{l.price?.toLocaleString('en-IN')}</span>
                  <span className="orig-val">₹{l.original_price?.toLocaleString('en-IN')}</span>
                  <span className="disc-val">-{l.discount_percent}%</span>
                  <span className="deliv-val">{l.delivery_info}</span>
                  <span>
                    <span className={`badge ${l.in_stock ? 'badge-green' : 'badge-red'}`}>
                      {l.in_stock ? 'In Stock' : 'Out of Stock'}
                    </span>
                  </span>
                </div>
              ))}
            </div>
            {product.listings[0]?.bank_offers && (
              <div className="bank-offers">
                <h4 className="section-title" style={{ fontSize: 14, marginTop: 20 }}>💳 Bank Offers</h4>
                {product.listings[0].bank_offers.map((o, i) => (
                  <div key={i} className="bank-offer-item">✓ {o}</div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'price-chart' && (
          <div className="pd-chart fade-in">
            <div className="chart-controls">
              <h3 className="section-title" style={{ fontSize: 16 }}>Price History (90 Days)</h3>
              <div className="platform-tabs">
                {Object.keys(priceHistory).map(p => (
                  <button
                    key={p}
                    className={`platform-tab ${selectedPlatform === p ? 'active' : ''}`}
                    onClick={() => setSelectedPlatform(p)}
                  >{p}</button>
                ))}
              </div>
            </div>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="date" stroke="var(--text2)" tick={{ fontSize: 11 }} interval={6} />
                <YAxis stroke="var(--text2)" tick={{ fontSize: 11 }}
                  tickFormatter={v => `₹${(v/1000).toFixed(0)}k`} />
                <Tooltip
                  contentStyle={{ background: 'var(--bg2)', border: '1px solid var(--border)', borderRadius: 8 }}
                  formatter={(v) => [`₹${v.toLocaleString('en-IN')}`, 'Price']}
                />
                <Line type="monotone" dataKey="price" stroke="var(--accent)" strokeWidth={2}
                  dot={false} activeDot={{ r: 5 }} />
              </LineChart>
            </ResponsiveContainer>

            {pi && (
              <div className="price-prediction-box">
                <div className="pred-header">🔮 Price Prediction (Next 30 Days) — <em>Estimated</em></div>
                <div className="pred-stats">
                  <div>
                    <span>Current</span>
                    <strong>₹{pi.current_best_price?.toLocaleString('en-IN')}</strong>
                  </div>
                  <div>
                    <span>Predicted</span>
                    <strong className={pi.predicted_price_30d < pi.current_best_price ? 'text-green' : 'text-red'}>
                      ₹{pi.predicted_price_30d?.toLocaleString('en-IN')}
                    </strong>
                  </div>
                  <div>
                    <span>Trend</span>
                    <strong>{pi.price_trend?.replace('_', ' ')}</strong>
                  </div>
                  <div>
                    <span>Deal Score</span>
                    <strong>{pi.deal_score}/100</strong>
                  </div>
                </div>
                <div className="pred-note">⚠️ Price predictions are estimates based on historical patterns. Not financial advice.</div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'reviews' && ra && (
          <div className="pd-reviews fade-in">
            <div className="reviews-summary">
              <div className="big-rating">
                <div className="big-number">{ra.average_rating.toFixed(1)}</div>
                <Stars rating={ra.average_rating} />
                <div className="text2">{ra.total_reviews} reviews</div>
              </div>
              <div className="rating-bars">
                {[5, 4, 3, 2, 1].map(n => (
                  <RatingBar
                    key={n}
                    label={n}
                    count={ra.rating_distribution?.[n] || 0}
                    total={totalReviews}
                  />
                ))}
              </div>
              <div className="aspect-grid">
                {ra.aspect_analysis?.slice(0, 6).map(a => (
                  <div key={a.aspect} className={`aspect-badge ${a.sentiment}`}>
                    {a.aspect}: <strong>{a.sentiment}</strong>
                  </div>
                ))}
              </div>
            </div>

            <div className="review-list">
              {product.reviews?.map((r, i) => (
                <div key={i} className="review-item">
                  <div className="review-header">
                    <div>
                      <div className="reviewer-name">{r.reviewer_name}</div>
                      <Stars rating={r.rating} />
                    </div>
                    <div className="review-meta">
                      <span className="badge badge-blue">{r.platform}</span>
                      {r.verified_purchase && <span className="badge badge-green">✓ Verified</span>}
                      <span className="text2 review-date">{r.review_date}</span>
                    </div>
                  </div>
                  <div className="review-title">{r.title}</div>
                  <p className="review-body">{r.body}</p>
                  {r.helpful_votes > 0 && (
                    <div className="review-helpful">
                      <ThumbsUp size={12} /> {r.helpful_votes} found helpful
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'specs' && product.specifications && (
          <div className="pd-specs fade-in">
            <h3 className="section-title" style={{ fontSize: 16 }}>Specifications</h3>
            <div className="specs-grid">
              {Object.entries(product.specifications).map(([k, v]) => (
                <div key={k} className="spec-row">
                  <span className="spec-key">{k}</span>
                  <span className="spec-val">{v}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
