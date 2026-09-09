# 🛒 ShopAI — Intelligent Shopping Agent

An end-to-end AI-powered shopping agent that solves product overload, scattered reviews, and dynamic pricing across multiple e-commerce platforms.

**No API keys required. Runs fully offline with mock data.**

---

## Architecture

```
Multi-Source Data → Multi-Modal Search → Predictive Shopping Agent → Smart Shopping Pulse
```

```
shopping-agent/
├── backend/               # FastAPI + SQLite
│   ├── main.py            # App entry point
│   ├── database.py        # SQLAlchemy setup
│   ├── agents/
│   │   └── shopping_agents.py   # 6 AI agents + orchestrator
│   ├── routers/
│   │   ├── products.py    # Product search & listing API
│   │   ├── agent.py       # AI agent query API
│   │   └── dashboard.py   # Analytics API
│   ├── models/
│   │   ├── models.py      # DB models
│   │   └── schemas.py     # Pydantic schemas
│   └── data/
│       └── seed_data.py   # 14 products, 4 platforms, reviews, price history
└── frontend/              # React + Vite
    └── src/
        ├── pages/
        │   ├── HomePage.jsx
        │   ├── SearchResultsPage.jsx
        │   ├── ProductDetailPage.jsx
        │   ├── ComparePage.jsx
        │   ├── AgentPage.jsx         # AI chat interface
        │   └── DashboardPage.jsx     # Smart Shopping Pulse
        └── components/
            ├── Navbar.jsx
            └── ProductCard.jsx
```

---

## Quick Start

### Prerequisites
- Python 3.10+ (already installed)
- Node.js 18+ (install from https://nodejs.org)

---

### Step 1 — Backend Setup

```bash
cd shopping-agent/backend

# Install Python dependencies
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic pandas numpy scikit-learn python-multipart aiofiles httpx python-dotenv

# Seed the database (creates shopping_agent.db with 14 products)
python data/seed_data.py

# Start the API server
uvicorn main:app --reload --port 8000
```

API runs at: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

---

### Step 2 — Frontend Setup

```bash
cd shopping-agent/frontend

# Install Node dependencies
npm install

# Start the dev server (proxies /api → localhost:8000)
npm run dev
```

App runs at: http://localhost:3000

---

## Demo Flow

Open the **AI Agent** page and try:

```
"Find the best laptop for a CSE student under ₹70,000 with 16GB RAM, SSD and dedicated GPU"
```

What happens:
1. **Query Understanding Agent** — parses budget (₹70k), RAM (16GB), GPU (dedicated), category (Laptops), use-case (student)
2. **Product Search Agent** — fetches all matching products from SQLite
3. **Review Analysis Agent** — runs sentiment analysis on all reviews
4. **Price Intelligence Agent** — calculates deal scores, trends, 30-day predictions
5. **Recommendation Agent** — scores each product (0–100) against your requirements
6. **Shopping Orchestrator** — ranks results, generates narrative explanation

---

## AI Agents (No API Key)

| Agent | What it does |
|---|---|
| `QueryUnderstandingAgent` | Regex + keyword NLP: extracts budget, RAM, GPU, brand, use-case |
| `ReviewAnalysisAgent` | Aspect-level sentiment, pros/cons, AI summary |
| `PriceIntelligenceAgent` | Historical trend, deal score (0–100), 30-day prediction |
| `RecommendationAgent` | Weighted scoring: budget fit + rating + specs + use-case + deal |
| `ShoppingOrchestrator` | Coordinates all agents, produces ranked results + narrative |

---

## Sample Data

14 products × 4 platforms × 90 days price history:

| Category | Products |
|---|---|
| Laptops | ASUS ROG G15, Lenovo IdeaPad Slim 5, HP Omen 16, Dell XPS 15, Acer Aspire Lite |
| Smartphones | Samsung S24 Ultra, OnePlus 12, iPhone 15 Pro, Redmi Note 13 Pro+ |
| Headphones | Sony WH-1000XM5, Apple AirPods Pro 2 |
| TVs | Samsung 65" QLED |
| Tablets | Apple iPad Air M2 |
| Cameras | Sony ZV-E10 II |

Platforms: **Amazon · Flipkart · Croma · Reliance Digital**

---

## API Endpoints

```
GET  /api/products/              # All products (filters: category, brand, budget_max, sort_by)
GET  /api/products/{id}          # Product detail + reviews + price intelligence
GET  /api/products/deals         # Best deal score products
POST /api/products/compare       # Side-by-side comparison (up to 4)
GET  /api/products/categories    # Category list
GET  /api/products/brands        # Brand list

POST /api/agent/query            # Full AI agent pipeline (natural language)
POST /api/agent/parse            # Query understanding only
GET  /api/agent/demo-queries     # Sample queries

GET  /api/dashboard/stats        # Overall stats
GET  /api/dashboard/market-trends
GET  /api/dashboard/platform-comparison
GET  /api/dashboard/price-trends/{id}
GET  /api/dashboard/sentiment-overview
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, FastAPI, SQLAlchemy, SQLite |
| AI/ML | Rule-based NLP, Statistical analysis (no API key) |
| Frontend | React 18, Vite, React Router, Recharts, Lucide |
| Charts | Recharts (Line, Bar, Pie charts) |
| Data | Mock/sample data — legally safe, no scraping |

---

## Pages

| Page | URL | Description |
|---|---|---|
| Home | `/` | Hero search + best deals + categories |
| Search Results | `/search?q=...` | Filtered grid with sidebar filters |
| Product Detail | `/product/:id` | Full detail, price chart, reviews, specs |
| Compare | `/compare?ids=1,2,3` | Side-by-side spec & price table |
| AI Agent | `/agent` | Chat interface with full agent pipeline |
| Dashboard | `/dashboard` | Smart Shopping Pulse with 6 charts |
