"""Product search and listing router."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List
from database import get_db
from models.models import Product, ProductListing, Review, PriceHistory
from models.schemas import SearchRequest, ProductDetailOut
from agents.shopping_agents import ReviewAnalysisAgent, PriceIntelligenceAgent

router = APIRouter(prefix="/api/products", tags=["Products"])

review_agent = ReviewAnalysisAgent()
price_agent = PriceIntelligenceAgent()


def _build_product_summary(product, db: Session) -> dict:
    """Build a compact product summary with best price and ratings."""
    listings = db.query(ProductListing).filter(
        ProductListing.product_id == product.id,
        ProductListing.in_stock == True
    ).all()

    reviews = db.query(Review).filter(Review.product_id == product.id).all()
    history = db.query(PriceHistory).filter(PriceHistory.product_id == product.id).all()

    prices = [l.price for l in listings if l.price]
    best_price = min(prices) if prices else None
    best_listing = min(listings, key=lambda x: x.price) if listings else None

    avg_rating = None
    if reviews:
        avg_rating = sum(r.rating for r in reviews if r.rating) / len([r for r in reviews if r.rating])

    history_data = [{"price": h.price, "date": h.date, "platform": h.platform} for h in history]
    listings_data = [{"price": l.price, "platform": l.platform, "original_price": l.original_price} for l in listings]

    price_intel = price_agent.analyze(product.id, listings_data, history_data)
    deal_score = price_intel.get("deal_score", 50)

    return {
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "category": product.category,
        "subcategory": product.subcategory,
        "description": product.description,
        "image_url": product.image_url,
        "specifications": product.specifications or {},
        "best_price": best_price,
        "best_platform": best_listing.platform if best_listing else None,
        "avg_rating": round(avg_rating, 2) if avg_rating else None,
        "review_count": len(reviews),
        "deal_score": deal_score,
        "listings": [
            {
                "id": l.id, "platform": l.platform, "seller": l.seller,
                "price": l.price, "original_price": l.original_price,
                "discount_percent": l.discount_percent, "url": l.url,
                "availability": l.availability, "delivery_info": l.delivery_info,
                "emi_options": l.emi_options, "bank_offers": l.bank_offers,
                "in_stock": l.in_stock
            }
            for l in listings
        ],
        "price_intelligence": price_intel,
    }


@router.get("/")
def get_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    budget_max: Optional[float] = None,
    budget_min: Optional[float] = None,
    sort_by: str = "recommendation_score",
    page: int = 1,
    page_size: int = 12,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))

    products = query.all()

    results = []
    for product in products:
        summary = _build_product_summary(product, db)

        # Budget filter
        if budget_max and summary["best_price"] and summary["best_price"] > budget_max:
            continue
        if budget_min and summary["best_price"] and summary["best_price"] < budget_min:
            continue

        results.append(summary)

    # Sort
    if sort_by == "price_asc":
        results.sort(key=lambda x: x["best_price"] or float("inf"))
    elif sort_by == "price_desc":
        results.sort(key=lambda x: x["best_price"] or 0, reverse=True)
    elif sort_by == "rating_desc":
        results.sort(key=lambda x: x["avg_rating"] or 0, reverse=True)
    elif sort_by == "deal_score":
        results.sort(key=lambda x: x["deal_score"] or 0, reverse=True)

    # Pagination
    total = len(results)
    start = (page - 1) * page_size
    paginated = results[start: start + page_size]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "products": paginated
    }


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Product.category, func.count(Product.id)).group_by(Product.category).all()
    return [{"category": c[0], "count": c[1]} for c in categories]


@router.get("/brands")
def get_brands(db: Session = Depends(get_db)):
    brands = db.query(Product.brand, func.count(Product.id)).group_by(Product.brand).all()
    return [{"brand": b[0], "count": b[1]} for b in brands]


@router.get("/deals")
def get_best_deals(limit: int = 6, db: Session = Depends(get_db)):
    """Return products with the best deal scores."""
    products = db.query(Product).all()
    results = [_build_product_summary(p, db) for p in products]
    results.sort(key=lambda x: x.get("deal_score", 0), reverse=True)
    return results[:limit]


@router.get("/{product_id}")
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    listings = db.query(ProductListing).filter(ProductListing.product_id == product_id).all()
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    history = db.query(PriceHistory).filter(PriceHistory.product_id == product_id).all()

    reviews_data = [
        {"rating": r.rating, "title": r.title, "body": r.body,
         "reviewer_name": r.reviewer_name, "platform": r.platform,
         "verified_purchase": r.verified_purchase, "helpful_votes": r.helpful_votes,
         "review_date": r.review_date}
        for r in reviews
    ]

    history_data = [{"price": h.price, "date": h.date, "platform": h.platform} for h in history]
    listings_data = [{"price": l.price, "platform": l.platform, "original_price": l.original_price} for l in listings]

    review_analysis = review_agent.analyze(reviews_data)
    price_intel = price_agent.analyze(product_id, listings_data, history_data)

    return {
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "category": product.category,
        "subcategory": product.subcategory,
        "description": product.description,
        "image_url": product.image_url,
        "specifications": product.specifications,
        "listings": [
            {
                "id": l.id, "platform": l.platform, "seller": l.seller,
                "price": l.price, "original_price": l.original_price,
                "discount_percent": l.discount_percent, "url": l.url,
                "availability": l.availability, "delivery_info": l.delivery_info,
                "emi_options": l.emi_options, "bank_offers": l.bank_offers,
                "in_stock": l.in_stock
            }
            for l in listings
        ],
        "reviews": reviews_data,
        "review_analysis": review_analysis,
        "price_intelligence": price_intel,
        "price_history": history_data,
    }


@router.post("/compare")
def compare_products(product_ids: List[int], db: Session = Depends(get_db)):
    """Compare multiple products side by side."""
    results = []
    for pid in product_ids[:4]:  # Max 4 products
        product = db.query(Product).filter(Product.id == pid).first()
        if product:
            summary = _build_product_summary(product, db)
            results.append(summary)
    return results
