import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import SearchResultsPage from './pages/SearchResultsPage'
import ProductDetailPage from './pages/ProductDetailPage'
import ComparePage from './pages/ComparePage'
import AgentPage from './pages/AgentPage'
import DashboardPage from './pages/DashboardPage'
import NotFoundPage from './pages/NotFoundPage'

// Footer is hidden on full-height pages (Agent)
const NO_FOOTER_PATHS = ['/agent']

function Layout() {
  const location = useLocation()
  const showFooter = !NO_FOOTER_PATHS.some(p => location.pathname.startsWith(p))

  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchResultsPage />} />
        <Route path="/product/:id" element={<ProductDetailPage />} />
        <Route path="/compare" element={<ComparePage />} />
        <Route path="/agent" element={<AgentPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
      {showFooter && <Footer />}
    </>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  )
}
