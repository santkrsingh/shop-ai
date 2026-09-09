import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { productAPI } from '../api'
import './ComparePage.css'

function Stars({ rating }) {
  return <span className="stars">{Array.from({ length: 5 }, (_, i) => i < Math.round(rating) ? '★' : '☆').join('')}</span>
}

export default function ComparePage() {
  const [searchParams] = useSearchParams()
  const ids = (searchParams.get('ids') || '').split(',').map(Number).filter(Boolean)
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchId, setSearchId] = useState('')
  const [compareIds, setCompareIds] = useState(ids)

  useEffect(() => {
    if (compareIds.length === 0) return
    setLoading(true)
    productAPI.compare(compareIds)
      .then(r => setProducts(r.data))
      .finally(() => setLoading(false))
  }, [compareIds])

  const addProduct = () => {
    const num = parseInt(searchId)
    if (num && !compareIds.includes(num) && compareIds.length < 4) {
      setCompareIds([...compareIds, num])
      setSearchId('')
    }
  }

  const removeProduct = (id) => {
    setCompareIds(compareIds.filter(x => x !== id))
    setProducts(products.filter(p => p.id !== id))
  }

  // All spec keys across products
  const allSpecKeys = [...new Set(products.flatMap(p => Object.keys(p.specifications || {})))]

  return (
    <div className="page container fade-in">
      <h1 className="section-title" style={{ fontSize: 24, marginBottom: 8 }}>Product Comparison</h1>
      <p style={{ color: 'var(--text2)', marginBottom: 24 }}>Compare up to 4 products side by side</p>

      {/* Add product */}
      <div className="compare-add">
        <input
          className="input"
          style={{ width: 240 }}
          placeholder="Enter product ID to add..."
          value={searchId}
          onChange={e => setSearchId(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && addProduct()}
        />
        <button className="btn btn-primary" onClick={addProduct}>Add</button>
        <span style={{ color: 'var(--text2)', fontSize: 13 }}>
          (IDs visible in product URL or search results — max 4)
        </span>
      </div>

      {loading && (
        <div style={{ display: 'flex', justifyContent: 'center', padding: 40 }}>
          <div className="spinner" />
        </div>
      )}

      {!loading && products.length === 0 && (
        <div className="compare-empty">
          <div style={{ fontSize: 40 }}>⚖️</div>
          <h3>No products to compare</h3>
          <p>Search for products and click "+" to add them to comparison, or enter product IDs above.</p>
        </div>
      )}

      {!loading && products.length > 0 && (
        <div className="compare-table-wrap">
          <table className="compare-table">
            <thead>
              <tr>
                <th className="compare-label-col">Feature</th>
                {products.map(p => (
                  <th key={p.id} className="compare-product-col">
                    <div className="cmp-product-header">
                      <img
                        src={p.image_url}
                        alt={p.name}
                        className="cmp-product-img"
                        onError={e => { e.target.src = 'https://via.placeholder.com/100?text=?' }}
                      />
                      <div className="cmp-product-name">{p.name}</div>
                      <div className="cmp-product-brand">{p.brand}</div>
                      <button
                        className="btn btn-ghost btn-sm cmp-remove"
                        onClick={() => removeProduct(p.id)}
                      >✕</button>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {/* Price */}
              <tr className="compare-section-row">
                <td colSpan={products.length + 1}>💰 Pricing</td>
              </tr>
              <tr>
                <td className="compare-label">Best Price</td>
                {products.map(p => {
                  const isBest = p.best_price === Math.min(...products.map(x => x.best_price || Infinity))
                  return (
                    <td key={p.id} className={isBest ? 'best-value' : ''}>
                      ₹{p.best_price?.toLocaleString('en-IN')}
                      {isBest && <span className="best-badge">BEST</span>}
                    </td>
                  )
                })}
              </tr>
              <tr>
                <td className="compare-label">Platform</td>
                {products.map(p => <td key={p.id}>{p.best_platform}</td>)}
              </tr>
              <tr>
                <td className="compare-label">Deal Score</td>
                {products.map(p => {
                  const isBest = p.deal_score === Math.max(...products.map(x => x.deal_score || 0))
                  return (
                    <td key={p.id} className={isBest ? 'best-value' : ''}>
                      <div className="deal-score-bar">
                        <div className="progress-bar" style={{ width: 80 }}>
                          <div className="progress-fill" style={{ width: `${p.deal_score}%`, background: p.deal_score >= 70 ? 'var(--green)' : p.deal_score >= 50 ? 'var(--yellow)' : 'var(--red)' }} />
                        </div>
                        <span>{p.deal_score}/100</span>
                      </div>
                    </td>
                  )
                })}
              </tr>

              {/* Rating */}
              <tr className="compare-section-row">
                <td colSpan={products.length + 1}>⭐ Ratings</td>
              </tr>
              <tr>
                <td className="compare-label">Avg Rating</td>
                {products.map(p => {
                  const isBest = p.avg_rating === Math.max(...products.map(x => x.avg_rating || 0))
                  return (
                    <td key={p.id} className={isBest ? 'best-value' : ''}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <Stars rating={p.avg_rating || 0} />
                        <strong>{p.avg_rating?.toFixed(1)}</strong>
                      </div>
                    </td>
                  )
                })}
              </tr>
              <tr>
                <td className="compare-label">Reviews</td>
                {products.map(p => <td key={p.id}>{p.review_count}</td>)}
              </tr>

              {/* Specs */}
              <tr className="compare-section-row">
                <td colSpan={products.length + 1}>🔧 Specifications</td>
              </tr>
              {allSpecKeys.map(key => (
                <tr key={key}>
                  <td className="compare-label">{key}</td>
                  {products.map(p => (
                    <td key={p.id}>{p.specifications?.[key] || '—'}</td>
                  ))}
                </tr>
              ))}

              {/* Listings count */}
              <tr className="compare-section-row">
                <td colSpan={products.length + 1}>🛒 Availability</td>
              </tr>
              <tr>
                <td className="compare-label">Available On</td>
                {products.map(p => (
                  <td key={p.id}>
                    {p.listings?.map(l => l.platform).join(', ')}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
