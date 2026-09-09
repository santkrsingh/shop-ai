import { useState, useEffect, useRef, useCallback } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Bot, Send, User, Sparkles, ChevronRight, Cpu, Search, BarChart2, Star, TrendingUp, Award } from 'lucide-react'
import { agentAPI } from '../api'
import ProductCard from '../components/ProductCard'
import './AgentPage.css'

const DEMO_QUERIES = [
  "Best laptop for CSE student under ₹70,000 with 16GB RAM, SSD and dedicated GPU",
  "Best smartphone under ₹35,000 with great camera and long battery",
  "Gaming laptop under ₹90,000 with RTX GPU",
  "Premium ultrabook for video editing with OLED display",
  "Wireless headphones with best noise cancellation under ₹30,000",
  "Best budget laptop under ₹40,000 for office work",
  "Best smartphone with 5G under ₹65,000",
  "Compare OnePlus and Samsung flagship phones",
]

const AGENT_PIPELINE = [
  { icon: <Cpu size={11} />,      label: 'Query Understanding Agent' },
  { icon: <Search size={11} />,   label: 'Product Search Agent' },
  { icon: <Star size={11} />,     label: 'Review Analysis Agent' },
  { icon: <TrendingUp size={11} />, label: 'Price Intelligence Agent' },
  { icon: <Award size={11} />,    label: 'Recommendation Agent' },
  { icon: <BarChart2 size={11} />, label: 'Shopping Orchestrator' },
]

function renderMarkdown(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br/>')
}

function ParsedQueryCard({ parsed }) {
  const items = [
    parsed.category       && { label: 'Category',   value: parsed.category },
    parsed.budget_max     && { label: 'Budget Max',  value: `₹${parsed.budget_max.toLocaleString('en-IN')}` },
    parsed.budget_min     && { label: 'Budget Min',  value: `₹${parsed.budget_min.toLocaleString('en-IN')}` },
    parsed.brands?.length && { label: 'Brands',      value: parsed.brands.join(', ') },
    parsed.use_cases?.length && { label: 'Use Cases', value: parsed.use_cases.join(', ') },
    parsed.specs?.min_ram_gb  && { label: 'Min RAM',  value: `${parsed.specs.min_ram_gb}GB` },
    parsed.specs?.gpu_type    && { label: 'GPU',       value: parsed.specs.gpu_type.replace(/_/g, ' ') },
    parsed.specs?.storage_type && { label: 'Storage', value: parsed.specs.storage_type },
    { label: 'Sort By', value: (parsed.sort_by || '').replace(/_/g, ' ') },
    { label: 'Intent',  value: parsed.intent },
  ].filter(Boolean)

  return (
    <div className="parsed-card">
      <div className="parsed-title">
        <Cpu size={12} /> Query Understanding
      </div>
      <div className="parsed-grid">
        {items.map((item, i) => (
          <div key={i} className="parsed-item">
            <span className="parsed-key">{item.label}</span>
            <strong className="parsed-val">{item.value}</strong>
          </div>
        ))}
      </div>
    </div>
  )
}

function PipelineSteps() {
  const [visibleCount, setVisibleCount] = useState(0)
  useEffect(() => {
    let i = 0
    const t = setInterval(() => {
      i++
      setVisibleCount(i)
      if (i >= AGENT_PIPELINE.length) clearInterval(t)
    }, 180)
    return () => clearInterval(t)
  }, [])

  return (
    <div className="agent-pipeline">
      {AGENT_PIPELINE.map((step, i) => (
        <div key={i} className={`pipeline-step ${i < visibleCount ? 'done' : 'pending'}`}>
          {i < visibleCount ? '✓' : <span className="step-num">{i + 1}</span>}
          {step.icon} {step.label}
        </div>
      ))}
    </div>
  )
}

function AgentMessage({ msg, isLatestAgent }) {
  if (msg.role === 'user') {
    return (
      <div className="msg-wrap user-msg">
        <div className="msg-bubble user-bubble">{msg.content}</div>
        <div className="msg-avatar user-avatar"><User size={15} /></div>
      </div>
    )
  }

  if (msg.role === 'thinking') {
    return (
      <div className="msg-wrap agent-msg">
        <div className="msg-avatar agent-avatar"><Bot size={15} /></div>
        <div className="msg-bubble agent-bubble thinking-bubble">
          <div className="thinking-dots">
            <span /><span /><span />
          </div>
          <span>Running 6 agents...</span>
        </div>
      </div>
    )
  }

  const { parsed_query: parsed, narrative, results, top_picks } = msg.data || {}
  const isWelcome = !parsed && !top_picks?.length

  return (
    <div className="msg-wrap agent-msg">
      <div className="msg-avatar agent-avatar"><Bot size={15} /></div>
      <div className="msg-bubble agent-bubble agent-result">

        {/* Narrative */}
        {narrative && (
          <div
            className="agent-narrative"
            dangerouslySetInnerHTML={{ __html: renderMarkdown(narrative) }}
          />
        )}

        {!isWelcome && parsed && <ParsedQueryCard parsed={parsed} />}
        {!isWelcome && isLatestAgent && <PipelineSteps />}

        {/* Results */}
        {top_picks?.length > 0 && (
          <div className="top-picks-section">
            <div className="top-picks-header">
              <Sparkles size={14} />
              Top {top_picks.length} Recommendations
              <span className="total-found">({results?.length} products analyzed)</span>
            </div>
            <div className="agent-products-grid">
              {top_picks.map(p => <ProductCard key={p.id} product={p} />)}
            </div>
          </div>
        )}

        {/* No results */}
        {!isWelcome && top_picks?.length === 0 && (
          <div className="no-results-msg">
            No products matched your criteria. Try adjusting budget or removing specific requirements.
          </div>
        )}
      </div>
    </div>
  )
}

export default function AgentPage() {
  const [searchParams] = useSearchParams()
  const initialQuery = searchParams.get('q') || ''

  const [messages, setMessages] = useState([{
    role: 'agent',
    data: {
      narrative: "**Hi! I'm your AI Shopping Agent.**\n\nI search across Amazon, Flipkart, Croma, and Reliance Digital, then run 6 specialized agents to find the best product for *your exact needs*.\n\nTry: *\"Best laptop for CSE student under 70,000 with 16GB RAM and dedicated GPU\"*",
    }
  }])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendQuery = useCallback(async (q) => {
    const query = (q || '').trim()
    if (!query || loading) return

    setInput('')
    setLoading(true)
    inputRef.current?.focus()

    setMessages(prev => [
      ...prev,
      { role: 'user', content: query },
      { role: 'thinking' }
    ])

    try {
      const res = await agentAPI.query(query)
      setMessages(prev => {
        const without = prev.filter(m => m.role !== 'thinking')
        return [...without, { role: 'agent', data: res.data, isLatest: true }]
      })
    } catch {
      setMessages(prev => {
        const without = prev.filter(m => m.role !== 'thinking')
        return [...without, {
          role: 'agent',
          data: { narrative: '**Error:** Could not reach the backend. Make sure the server is running on port 8000.' }
        }]
      })
    } finally {
      setLoading(false)
    }
  }, [loading])

  // Auto-send initial query from URL param
  useEffect(() => {
    if (initialQuery) sendQuery(initialQuery)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const latestAgentIdx = messages.map((m, i) => m.role === 'agent' ? i : -1).filter(i => i >= 0).at(-1)

  return (
    <div className="agent-page">
      {/* Sidebar */}
      <aside className="agent-sidebar">
        <div className="sidebar-section-title">
          <Sparkles size={12} /> Try These Queries
        </div>
        {DEMO_QUERIES.map((q, i) => (
          <button
            key={i}
            className="demo-query-btn"
            onClick={() => sendQuery(q)}
            disabled={loading}
          >
            <ChevronRight size={11} className="dq-icon" />
            {q}
          </button>
        ))}

        <div className="sidebar-divider" />
        <div className="sidebar-section-title">Agent Pipeline</div>
        {AGENT_PIPELINE.map((step, i) => (
          <div key={i} className="sidebar-pipeline-step">
            <span className="sp-num">{i + 1}</span>
            {step.icon}
            <span>{step.label}</span>
          </div>
        ))}
      </aside>

      {/* Chat */}
      <div className="agent-chat">
        {/* Header */}
        <div className="chat-header">
          <div className="chat-header-icon">
            <Bot size={17} />
          </div>
          <div className="chat-header-text">
            <div className="chat-title">AI Shopping Agent</div>
            <div className="chat-subtitle">6 agents · 14 products · 4 platforms · Price prediction</div>
          </div>
          <div className="chat-status">
            <div className="status-dot" />
            Online
          </div>
        </div>

        {/* Messages */}
        <div className="chat-messages">
          {messages.map((msg, i) => (
            <AgentMessage
              key={i}
              msg={msg}
              isLatestAgent={i === latestAgentIdx && msg.role === 'agent'}
            />
          ))}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <form
          className="chat-input-row"
          onSubmit={e => { e.preventDefault(); sendQuery(input) }}
        >
          <input
            ref={inputRef}
            className="input chat-input"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="e.g. Best laptop under ₹70,000 with 16GB RAM and dedicated GPU..."
            disabled={loading}
          />
          <button
            type="submit"
            className="btn btn-primary send-btn"
            disabled={loading || !input.trim()}
          >
            {loading
              ? <span className="spinner" style={{ width: 16, height: 16, borderWidth: 2 }} />
              : <Send size={16} />
            }
          </button>
        </form>
      </div>
    </div>
  )
}
