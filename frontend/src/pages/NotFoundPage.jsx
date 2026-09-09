import { useNavigate } from 'react-router-dom'
import { Home, Search, Bot } from 'lucide-react'

export default function NotFoundPage() {
  const navigate = useNavigate()
  return (
    <div className="empty-state" style={{ minHeight: 'calc(100vh - 200px)' }}>
      <div className="empty-state-icon">🔍</div>
      <h3>404 — Page Not Found</h3>
      <p>The page you're looking for doesn't exist or has been moved.</p>
      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', justifyContent: 'center' }}>
        <button className="btn btn-primary" onClick={() => navigate('/')}>
          <Home size={15} /> Go Home
        </button>
        <button className="btn btn-secondary" onClick={() => navigate('/search')}>
          <Search size={15} /> Browse Products
        </button>
        <button className="btn btn-secondary" onClick={() => navigate('/agent')}>
          <Bot size={15} /> Ask AI Agent
        </button>
      </div>
    </div>
  )
}
