import { Link } from 'react-router-dom'
import { TrendingDown, TrendingUp } from 'lucide-react'
import './ProductCard.css'

function Stars({ rating }) {
  const full = Math.floor(rating)
  const empty = 5 - Math.ceil(rating)
  const half = 5 - full - empty
  return (
    <span className="stars" title={`${rating}/5`}>
      {'★'.repeat(full)}{'½'.repeat(half)}{'☆'.repeat(empty)}
    </span>
  )
}

function DealBadge({ score }) {
  if (score >= 75) return <span className="badge badge-green">Hot Deal</span>
  if (score >= 55) return <span className="badge badge-yellow">Good Deal</span>
  return null
}

const PLATFORM_COLORS = {
  Amazon: '#f90',
  Flipkart: '#2874f0',
  Croma: '#ef7f1a',
  'Reliance Digital': '#c41e3a',
}

export default function ProductCard({ product, onCompare, compareList = [] }) {
  const isInCompare = compareList.includes(product.id)
  const bestListing = product.listings?.find(l => l.price === product.best_price) || product.listings?.[0]
  const discountPct = bestListing?.discount_percent
  const pi = product.price_intelligence || {}

  return (
    <div className="product-card fade-in">
      {/* Image */}
      <div className="pc-image-wrap">
        <img
          src={product.image_url || 'https://placehold.co/400x250/1e2535/9aa3b8?text=No+Image'}
          alt={product.name}
          className="pc-image"
          onError={e => { e.target.src = 'https://placehold.co/400x250/1e2535/9aa3b8?text=No+Image' }}
        />
        <div className="pc-badges">
          {discountPct > 0 && (
            <span className="badge badge-red">-{discountPct}%</span>
          )}
          <DealBadge score={product.deal_score} />
        </div>
        {onCompare && (
          <button
            className={`pc-compare-btn ${isInCompare ? 'active' : ''}`}
            onClick={() => onCompare(product.id)}
            title={isInCompare ? 'Remove from compare' : 'Add to compare'}
          >
            {isInCompare ? '✓ Added' : '+ Compare'}
          </button>
        )}
      </div>

      {/* Body */}
      <div className="pc-body">
        <div className="pc-brand">{product.brand}</div>
        <Link to={`/product/${product.id}`} className="pc-name">{product.name}</Link>

        {/* Rating */}
        {product.avg_rating > 0 && (
          <div className="pc-rating">
            <Stars rating={product.avg_rating} />
            <span className="pc-rating-val">{product.avg_rating.toFixed(1)}</span>
            <span className="pc-review-count">({product.review_count} reviews)</span>
          </div>
        )}

        {/* Recommendation score bar */}
        {product.recommendation_score != null && (
          <div className="pc-rec-score">
            <div className="rec-bar-bg">
              <div
                className="rec-bar-fill"
                style={{ width: `${product.recommendation_score}%` }}
              />
            </div>
            <span className="rec-label">{product.verdict || `Score: ${product.recommendation_score}`}</span>
          </div>
        )}

        {/* Price */}
        <div className="pc-price-row">
          <div>
            <div className="price-current">
              ₹{product.best_price?.toLocaleString('en-IN')}
            </div>
            {bestListing?.original_price > product.best_price && (
              <div className="price-original">
                ₹{bestListing.original_price?.toLocaleString('en-IN')}
              </div>
            )}
          </div>
          <div
            className="pc-platform-badge"
            style={{ borderColor: PLATFORM_COLORS[product.best_platform] || 'var(--border)', color: PLATFORM_COLORS[product.best_platform] || 'var(--text2)' }}
          >
            {product.best_platform}
          </div>
        </div>

        {/* Trend note */}
        {pi.price_trend === 'falling' && (
          <div className="pc-trend-note falling">
            <TrendingDown size={12} /> Price falling — good time to buy
          </div>
        )}
        {pi.price_trend === 'rising' && (
          <div className="pc-trend-note rising">
            <TrendingUp size={12} /> Price rising — buy soon
          </div>
        )}

        {/* Deal score meter */}
        {product.deal_score != null && (
          <div className="pc-deal-meter">
            <span className="deal-label">Deal Score</span>
            <div className="deal-bar-bg">
              <div
                className="deal-bar-fill"
                style={{
                  width: `${product.deal_score}%`,
                  background: product.deal_score >= 70 ? 'var(--green)' : product.deal_score >= 50 ? 'var(--yellow)' : 'var(--red)'
                }}
              />
            </div>
            <span className="deal-score-val">{product.deal_score}/100</span>
          </div>
        )}

        {/* Action */}
        <Link to={`/product/${product.id}`} className="btn btn-primary btn-sm pc-cta">
          View Details
        </Link>
      </div>
    </div>
  )
}
