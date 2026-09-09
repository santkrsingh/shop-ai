import axios from 'axios'

// In production (Vercel), set VITE_API_URL to your Render backend URL.
// In development, Vite proxy handles /api → localhost:8000.
const BASE_URL = import.meta.env.VITE_API_URL || ''

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 20000,
})

export const productAPI = {
  getAll: (params = {}) => api.get('/api/products/', { params }),
  getById: (id) => api.get(`/api/products/${id}`),
  compare: (ids) => api.post('/api/products/compare', ids),
  getCategories: () => api.get('/api/products/categories'),
  getBrands: () => api.get('/api/products/brands'),
  getDeals: (limit = 6) => api.get('/api/products/deals', { params: { limit } }),
}

export const agentAPI = {
  query: (query) => api.post('/api/agent/query', { query }),
  parse: (query) => api.post('/api/agent/parse', { query }),
  getDemoQueries: () => api.get('/api/agent/demo-queries'),
}

export const dashboardAPI = {
  getStats: () => api.get('/api/dashboard/stats'),
  getPriceTrends: (id) => api.get(`/api/dashboard/price-trends/${id}`),
  getMarketTrends: () => api.get('/api/dashboard/market-trends'),
  getPlatformComparison: () => api.get('/api/dashboard/platform-comparison'),
  getSentimentOverview: () => api.get('/api/dashboard/sentiment-overview'),
}

export default api
