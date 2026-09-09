import { useState, useEffect } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
  PieChart, Pie, Cell, LineChart, Line, Legend
} from 'recharts'
import { dashboardAPI, productAPI } from '../api'
import './DashboardPage.css'

const COLORS = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']

function StatCard({ title, value, subtitle, color = 'var(--accent)' }) {
  return (
    <div className="stat-card">
      <div className="stat-title">{title}</div>
      <div className="stat-value" style={{ color }}>{value}</div>
      {subtitle && <div className="stat-sub">{subtitle}</div>}
    </div>
  )
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div style={{ background: 'var(--bg2)', border: '1px solid var(--border)', borderRadius: 8, padding: '10px 14px', fontSize: 13 }}>
      <div style={{ color: 'var(--text2)', marginBottom: 4 }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color }}>
          {p.name}: <strong>{typeof p.value === 'number' && p.value > 1000 ? `₹${p.value.toLocaleString('en-IN')}` : p.value}</strong>
        </div>
      ))}
    </div>
  )
}

export default function DashboardPage() {
  const [stats, setStats] = useState(null)
  const [market, setMarket] = useState([])
  const [platforms, setPlatforms] = useState([])
  const [sentiment, setSentiment] = useState([])
  const [deals, setDeals] = useState([])
  const [selectedProductId, setSelectedProductId] = useState(null)
  const [priceHistory, setPriceHistory] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      dashboardAPI.getStats(),
      dashboardAPI.getMarketTrends(),
      dashboardAPI.getPlatformComparison(),
      dashboardAPI.getSentimentOverview(),
      productAPI.getDeals(8),
    ]).then(([s, m, p, sent, d]) => {
      setStats(s.data)
      setMarket(m.data)
      setPlatforms(p.data)
      setSentiment(sent.data)
      setDeals(d.data)
      if (d.data[0]?.id) setSelectedProductId(d.data[0].id)
    }).finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (selectedProductId) {
      dashboardAPI.getPriceTrends(selectedProductId)
        .then(r => setPriceHistory(r.data.price_history || {}))
        .catch(() => {})
    }
  }, [selectedProductId])

  if (loading) {
    return (
      <div className="page container" style={{ display: 'flex', justifyContent: 'center', paddingTop: 80 }}>
        <div className="spinner" />
      </div>
    )
  }

  // Sentiment radar data
  const radarData = sentiment.map(s => ({
    category: s.category,
    rating: s.avg_rating * 20, // scale to 100
    reviews: Math.min(100, s.review_count * 5),
  }))

  // Price trend chart data for selected product
  const selectedProductName = deals.find(d => d.id === selectedProductId)?.name || ''
  const priceChartData = Object.entries(priceHistory).flatMap(([platform, data]) =>
    data.map(d => ({ date: d.date.slice(5), price: d.price, platform }))
  ).reduce((acc, cur) => {
    const existing = acc.find(d => d.date === cur.date)
    if (existing) { existing[cur.platform] = cur.price }
    else { acc.push({ date: cur.date, [cur.platform]: cur.price }) }
    return acc
  }, []).slice(-30)

  const platformNames = Object.keys(priceHistory)

  return (
    <div className="page container fade-in">
      <h1 className="section-title" style={{ fontSize: 24, marginBottom: 4 }}>
        Smart Shopping Pulse Dashboard
      </h1>
      <p style={{ color: 'var(--text2)', marginBottom: 28 }}>
        Real-time market intelligence across platforms
      </p>

      {/* Stats row */}
      {stats && (
        <div className="stats-row">
          <StatCard title="Products Tracked" value={stats.total_products} subtitle="Across all categories" />
          <StatCard title="Total Reviews" value={stats.total_reviews.toLocaleString()} subtitle="Analyzed by AI" />
          <StatCard title="Platform Listings" value={stats.total_listings.toLocaleString()} subtitle="Multi-source" />
          <StatCard title="Avg Rating" value={`${stats.avg_rating}★`} subtitle="Across all products" color="var(--yellow)" />
          <StatCard title="Avg Discount" value={`${stats.avg_discount_percent}%`} subtitle="Platform average" color="var(--green)" />
        </div>
      )}

      {/* Row 1: Category avg price + Platform comparison */}
      <div className="dash-row-2">
        <div className="card dash-chart-card">
          <div className="card-header">📊 Average Price by Category</div>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={market} margin={{ left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="category" stroke="var(--text2)" tick={{ fontSize: 11 }} />
              <YAxis stroke="var(--text2)" tick={{ fontSize: 11 }}
                tickFormatter={v => `₹${(v/1000).toFixed(0)}k`} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="avg_price" name="Avg Price" radius={[4, 4, 0, 0]}>
                {market.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card dash-chart-card">
          <div className="card-header">🏪 Platform Avg Discount (%)</div>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={platforms}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="platform" stroke="var(--text2)" tick={{ fontSize: 11 }} />
              <YAxis stroke="var(--text2)" tick={{ fontSize: 11 }} tickFormatter={v => `${v}%`} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="avg_discount" name="Avg Discount %" radius={[4, 4, 0, 0]}>
                {platforms.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Row 2: Category ratings + Sentiment */}
      <div className="dash-row-2">
        <div className="card dash-chart-card">
          <div className="card-header">⭐ Avg Rating by Category</div>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={market.sort((a, b) => b.avg_rating - a.avg_rating)} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis type="number" domain={[0, 5]} stroke="var(--text2)" tick={{ fontSize: 11 }} />
              <YAxis type="category" dataKey="category" stroke="var(--text2)" tick={{ fontSize: 11 }} width={100} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="avg_rating" name="Rating" radius={[0, 4, 4, 0]}>
                {market.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card dash-chart-card">
          <div className="card-header">🥧 Product Distribution by Category</div>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={stats?.categories || []} cx="50%" cy="50%" outerRadius={90}
                dataKey="count" nameKey="category" label={({ category, percent }) => `${category} ${(percent * 100).toFixed(0)}%`}
                labelLine={false}
              >
                {(stats?.categories || []).map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip formatter={(v) => [v, 'Products']} contentStyle={{ background: 'var(--bg2)', border: '1px solid var(--border)', borderRadius: 8 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Price trend chart for selected product */}
      <div className="card dash-wide-card">
        <div className="card-header-row">
          <div className="card-header">📈 Price Trend Tracker</div>
          <select
            className="input"
            style={{ width: 300 }}
            value={selectedProductId || ''}
            onChange={e => setSelectedProductId(Number(e.target.value))}
          >
            {deals.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>
        <p className="chart-note">Showing price history across platforms for: <strong>{selectedProductName.substring(0, 60)}...</strong></p>
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={priceChartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis dataKey="date" stroke="var(--text2)" tick={{ fontSize: 11 }} interval={4} />
            <YAxis stroke="var(--text2)" tick={{ fontSize: 11 }} tickFormatter={v => `₹${(v/1000).toFixed(0)}k`} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            {platformNames.map((name, i) => (
              <Line key={name} type="monotone" dataKey={name} stroke={COLORS[i % COLORS.length]}
                strokeWidth={2} dot={false} activeDot={{ r: 5 }} />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Sentiment overview */}
      <div className="dash-row-2">
        <div className="card dash-chart-card">
          <div className="card-header">🎯 Review Sentiment by Category</div>
          <div className="sentiment-list">
            {sentiment.map(s => (
              <div key={s.category} className="sentiment-row">
                <div className="sentiment-cat">{s.category}</div>
                <div className="sentiment-stars">
                  {'★'.repeat(Math.floor(s.avg_rating))}{'☆'.repeat(5 - Math.floor(s.avg_rating))}
                  <span style={{ marginLeft: 6 }}>{s.avg_rating.toFixed(1)}</span>
                </div>
                <div className={`sentiment-badge ${s.sentiment === 'positive' ? 'pos' : s.sentiment === 'negative' ? 'neg' : 'neu'}`}>
                  {s.sentiment}
                </div>
                <div style={{ fontSize: 11, color: 'var(--text2)' }}>{s.review_count} reviews</div>
              </div>
            ))}
          </div>
        </div>

        <div className="card dash-chart-card">
          <div className="card-header">🔥 Best Deals Right Now</div>
          <div className="deals-list">
            {deals.map(p => (
              <div key={p.id} className="deal-row">
                <img
                  src={p.image_url}
                  alt={p.name}
                  className="deal-img"
                  onError={e => { e.target.src = 'https://via.placeholder.com/40?text=?' }}
                />
                <div className="deal-info">
                  <div className="deal-name">{p.name}</div>
                  <div className="deal-meta">
                    <span>₹{p.best_price?.toLocaleString('en-IN')}</span>
                    <span style={{ color: 'var(--accent)' }}>{p.best_platform}</span>
                  </div>
                </div>
                <div className={`deal-score-chip ${p.deal_score >= 70 ? 'hot' : p.deal_score >= 50 ? 'good' : ''}`}>
                  {p.deal_score}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Platform avg price comparison */}
      <div className="card dash-wide-card">
        <div className="card-header">💱 Platform Pricing Overview</div>
        <div className="platform-table">
          <div className="ptable-header">
            <span>Platform</span><span>Listings</span><span>Avg Price</span><span>Avg Discount</span><span>Relative Price</span>
          </div>
          {platforms.map(p => {
            const maxAvg = Math.max(...platforms.map(x => x.avg_price))
            const pct = (p.avg_price / maxAvg) * 100
            return (
              <div key={p.platform} className="ptable-row">
                <span className="ptable-platform">{p.platform}</span>
                <span>{p.listings}</span>
                <span>₹{p.avg_price.toLocaleString('en-IN')}</span>
                <span className="text-green">{p.avg_discount}%</span>
                <span style={{ flex: 1 }}>
                  <div className="progress-bar" style={{ maxWidth: 200 }}>
                    <div className="progress-fill" style={{ width: `${pct}%`, background: 'var(--accent)' }} />
                  </div>
                </span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
