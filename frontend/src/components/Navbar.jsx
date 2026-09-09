import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { Search, BarChart3, GitCompare, Bot, Zap, Menu, X } from 'lucide-react'
import './Navbar.css'

export default function Navbar() {
  const [q, setQ] = useState('')
  const navigate = useNavigate()
  const location = useLocation()

  const [mobileOpen, setMobileOpen] = useState(false)

  const handleSearch = (e) => {
    e.preventDefault()
    if (q.trim()) {
      navigate(`/search?q=${encodeURIComponent(q.trim())}`)
      setMobileOpen(false)
    }
  }

  const isActive = (path) => location.pathname === path ? 'active' : ''

  const NAV_LINKS = [
    { to: '/', icon: <Search size={15} />, label: 'Home' },
    { to: '/agent', icon: <Bot size={15} />, label: 'AI Agent' },
    { to: '/compare', icon: <GitCompare size={15} />, label: 'Compare' },
    { to: '/dashboard', icon: <BarChart3 size={15} />, label: 'Dashboard' },
  ]

  return (
    <nav className="navbar">
      <div className="container navbar-inner">
        {/* Logo */}
        <Link to="/" className="navbar-logo" onClick={() => setMobileOpen(false)}>
          <div className="logo-icon"><Zap size={18} /></div>
          <span className="logo-text">Shop<span className="logo-accent">AI</span></span>
        </Link>

        {/* Desktop Search */}
        <form className="navbar-search" onSubmit={handleSearch}>
          <div className="search-wrap">
            <Search size={16} className="search-icon" />
            <input
              className="search-input"
              value={q}
              onChange={e => setQ(e.target.value)}
              placeholder="Search products, brands, categories..."
            />
            <button type="submit" className="search-btn">Search</button>
          </div>
        </form>

        {/* Desktop Nav links */}
        <div className="navbar-links">
          {NAV_LINKS.map(l => (
            <Link key={l.to} to={l.to} className={`nav-link ${isActive(l.to)}`}>
              {l.icon} {l.label}
            </Link>
          ))}
        </div>

        {/* Mobile hamburger */}
        <button
          className="mobile-menu-btn"
          onClick={() => setMobileOpen(o => !o)}
          aria-label="Toggle menu"
        >
          {mobileOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="mobile-drawer">
          <form className="mobile-search" onSubmit={handleSearch}>
            <div className="search-wrap">
              <Search size={16} className="search-icon" />
              <input
                className="search-input"
                value={q}
                onChange={e => setQ(e.target.value)}
                placeholder="Search products..."
                autoFocus
              />
              <button type="submit" className="search-btn">Go</button>
            </div>
          </form>
          <div className="mobile-nav-links">
            {NAV_LINKS.map(l => (
              <Link
                key={l.to}
                to={l.to}
                className={`mobile-nav-link ${isActive(l.to)}`}
                onClick={() => setMobileOpen(false)}
              >
                {l.icon} {l.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  )
}
