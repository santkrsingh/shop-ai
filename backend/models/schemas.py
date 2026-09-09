"""Pydantic schemas for API request/response validation."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ProductListingOut(BaseModel):
    id: int
    platform: str
    seller: Optional[str]
    price: float
    original_price: Optional[float]
    discount_percent: Optional[float]
    url: Optional[str]
    availability: str
    delivery_info: Optional[str]
    emi_options: Optional[Dict]
    bank_offers: Optional[List]
    in_stock: bool

    class Config:
        from_attributes = True


class ReviewOut(BaseModel):
    id: int
    platform: Optional[str]
    reviewer_name: Optional[str]
    rating: Optional[float]
    title: Optional[str]
    body: Optional[str]
    verified_purchase: bool
    helpful_votes: int
    review_date: Optional[str]

    class Config:
        from_attributes = True


class PriceHistoryOut(BaseModel):
    platform: str
    price: float
    date: str

    class Config:
        from_attributes = True


class ProductSummaryOut(BaseModel):
    id: int
    name: str
    brand: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    image_url: Optional[str]
    specifications: Optional[Dict]
    best_price: Optional[float]
    best_platform: Optional[str]
    avg_rating: Optional[float]
    review_count: int
    deal_score: Optional[int]
    recommendation_score: Optional[float]
    verdict: Optional[str]
    listings: List[ProductListingOut]

    class Config:
        from_attributes = True


class ProductDetailOut(BaseModel):
    id: int
    name: str
    brand: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    specifications: Optional[Dict]
    listings: List[ProductListingOut]
    reviews: List[ReviewOut]
    review_analysis: Optional[Dict]
    price_intelligence: Optional[Dict]

    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    budget_max: Optional[float] = None
    budget_min: Optional[float] = None
    brands: Optional[List[str]] = None
    sort_by: Optional[str] = "recommendation_score"
    page: int = 1
    page_size: int = 12


class AgentQueryRequest(BaseModel):
    query: str


class CompareRequest(BaseModel):
    product_ids: List[int]
