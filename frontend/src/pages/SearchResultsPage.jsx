import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { Filter, X } from 'lucide-react'
import { productAPI } from '../api'
import ProductCard from '../components/ProductCard'
import './SearchResultsPage.css'

const SORT_OPTIONS = [
  { value: 'recommendation_score', label: 'Best Match' },
  { value: 'price_asc', label: 'Price: Low to High' },
  { value: 'price_desc', label: 'Price: High to Low' },
  { value: 'rating_desc', label: 'Highest Rated' },
  { value: 'deal_score', label: 'Best Deals' },
]

export default function SearchResultsPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const q = searchParams.get('q') || ''
  const initCategory = searchParams.get('category') || ''

  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [categories, setCategories] = useState([])
  const [brands, setBrands] = useState([])
  const [compareList, setCompareList] = useState([])

  // Filters
  const [selectedCategory, setSelectedCategory] = useState(initCategory)
  const [selectedBrand, setSelectedBrand] = useState('')
  const [budgetMax, setBudgetMax] = useState('')
  const [sortBy, setSortBy] = useState('recommendation_score')
  const [showFilters, setShowFilters] = useState(false)

  useEffect(() => {
    productAPI.getCategories().then(r => setCategories(r.data)).catch(() => {})
    productAPI.getBrands().then(r => setBrands(r.data)).catch(() => {})
  }, [])

  useEffect(() => {
    setLoading(true)
    const params = {
      sort_by: sortBy,
      ...(selectedCategory && { category: selectedCategory }),
      ...(selectedBrand && { brand: selectedBrand }),
      ...(budgetMax && { budget_max: parseFloat(budgetMax) }),
    }
    productAPI.getAll(params)
      .then(r => {
        let results = r.data.products || r.data || []
        // Client-side text search across name/brand/category/description
        if (q) {
          const ql = q.toLowerCase()
          results = results.filter(p =>
            p.name?.toLowerCase().includes(ql) ||
            p.brand?.toLowerCase().includes(ql) ||
            p.category?.toLowerCase().includes(ql) ||
            p.subcategory?.toLowerCase().includes(ql) ||
            p.description?.toLowerCase().includes(ql)
          )
        }
        // Apply sort after filter
        if (sortBy === 'price_asc') results.sort((a, b) => (a.best_price || 0) - (b.best_price || 0))
        else if (sortBy === 'price_desc') results.sort((a, b) => (b.best_price || 0) - (a.best_price || 0))
        else if (sortBy === 'rating_desc') results.sort((a, b) => (b.avg_rating || 0) - (a.avg_rating || 0))
        else if (sortBy === 'deal_score') results.sort((a, b) => (b.deal_score || 0) - (a.deal_score || 0))
        setProducts(results)
        setTotal(results.length)
      })
      .catch(() => setProducts([]))
      .finally(() => setLoading(false))
  }, [q, selectedCategory, selectedBrand, budgetMax, sortBy])

  const toggleCompare = (id) => {
    setCompareList(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : prev.length < 4 ? [...prev, id] : prev
    )
  }

  const clearFilters = () => {
    setSelectedCategory(''); setSelectedBrand(''); setBudgetMax('')
  }

  return (
    <div className="page container">
      {/* Header */}
      <div className="sr-header">
        <div>
          <h1 className="sr-title">
            {q ? `Results for "${q}"` : selectedCategory || 'All Products'}
          </h1>
          <p className="sr-count">{total} products found</p>
        </div>
        <div className="sr-controls">
          <button className="btn btn-secondary btn-sm" onClick={() => setShowFilters(f => !f)}>
            <Filter size={14} /> Filters
          </button>
          <select
            className="input"
            style={{ width: 180 }}
            value={sortBy}
            onChange={e => setSortBy(e.target.value)}
          >
            {SORT_OPTIONS.map(o => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Compare bar */}
      {compareList.length > 0 && (
        <div className="compare-bar">
          <span>{compareList.length} product(s) selected for comparison</span>
          <button
            className="btn btn-primary btn-sm"
            onClick={() => navigate(`/compare?ids=${compareList.join(',')}`)}
            disabled={compareList.length < 2}
          >
            Compare Now
          </button>
          <button className="btn btn-ghost btn-sm" onClick={() => setCompareList([])}>
            <X size={14} /> Clear
          </button>
        </div>
      )}

      <div className="sr-layout">
        {/* Sidebar filters */}
        <aside className={`sr-sidebar ${showFilters ? 'open' : ''}`}>
          <div className="filter-section">
            <div className="filter-heading">
              Category
              {selectedCategory && (
                <button className="filter-clear" onClick={() => setSelectedCategory('')}>×</button>
              )}
            </div>
            <div className="filter-options">
              {categories.map(c => (
                <label key={c.category} className="filter-option">
                  <input
                    type="radio" name="category" value={c.category}
                    checked={selectedCategory === c.category}
                    onChange={() => setSelectedCategory(c.category)}
                  />
                  {c.category} <span className="filter-count">({c.count})</span>
                </label>
              ))}
            </div>
          </div>

          <div className="filter-section">
            <div className="filter-heading">
              Brand
              {selectedBrand && (
                <button className="filter-clear" onClick={() => setSelectedBrand('')}>×</button>
              )}
            </div>
            <div className="filter-options">
              {brands.slice(0, 10).map(b => (
                <label key={b.brand} className="filter-option">
                  <input
                    type="radio" name="brand" value={b.brand}
                    checked={selectedBrand === b.brand}
                    onChange={() => setSelectedBrand(b.brand)}
                  />
                  {b.brand} <span className="filter-count">({b.count})</span>
                </label>
              ))}
            </div>
          </div>

          <div className="filter-section">
            <div className="filter-heading">Max Budget (₹)</div>
            <input
              className="input"
              type="number"
              placeholder="e.g. 70000"
              value={budgetMax}
              onChange={e => setBudgetMax(e.target.value)}
            />
          </div>

          {(selectedCategory || selectedBrand || budgetMax) && (
            <button className="btn btn-ghost btn-sm" onClick={clearFilters}>
              <X size={14} /> Clear All Filters
            </button>
          )}
        </aside>

        {/* Results */}
        <main className="sr-main">
          {loading ? (
            <div className="grid-3">
              {[...Array(9)].map((_, i) => (
                <div key={i} className="skeleton" style={{ height: 380, borderRadius: 14 }} />
              ))}
            </div>
          ) : products.length === 0 ? (
            <div className="sr-empty">
              <div className="sr-empty-icon">🔍</div>
              <h3>No products found</h3>
              <p>Try adjusting your filters or search query</p>
              <button className="btn btn-secondary" onClick={clearFilters}>Clear Filters</button>
            </div>
          ) : (
            <div className="grid-3">
              {products.map(p => (
                <ProductCard
                  key={p.id}
                  product={p}
                  onCompare={toggleCompare}
                  compareList={compareList}
                />
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
