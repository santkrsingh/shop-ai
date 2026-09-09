"""Dashboard analytics router."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.models import Product, ProductListing, Review, PriceHistory

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Overall marketplace statistics."""
    total_products = db.query(Product).count()
    total_reviews = db.query(Review).count()
    total_listings = db.query(ProductListing).count()

    avg_rating_row = db.query(func.avg(Review.rating)).scalar()
    avg_discount_row = db.query(func.avg(ProductListing.discount_percent)).scalar()

    # Category breakdown
    categories = db.query(
        Product.category,
        func.count(Product.id).label("count"),
        func.avg(ProductListing.price).label("avg_price")
    ).join(ProductListing, Product.id == ProductListing.product_id)\
     .group_by(Product.category).all()

    return {
        "total_products": total_products,
        "total_reviews": total_reviews,
        "total_listings": total_listings,
        "avg_rating": round(avg_rating_row or 0, 2),
        "avg_discount_percent": round(avg_discount_row or 0, 1),
        "categories": [
            {"category": c[0], "count": c[1], "avg_price": round(c[2] or 0)}
            for c in categories
        ],
    }


@router.get("/price-trends/{product_id}")
def get_price_trends(product_id: int, db: Session = Depends(get_db)):
    """Price history data for charts."""
    history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id
    ).order_by(PriceHistory.date).all()

    # Group by platform
    by_platform = {}
    for h in history:
        if h.platform not in by_platform:
            by_platform[h.platform] = []
        by_platform[h.platform].append({"date": h.date, "price": h.price})

    return {"product_id": product_id, "price_history": by_platform}


@router.get("/market-trends")
def get_market_trends(db: Session = Depends(get_db)):
    """Market trends by category - avg price, ratings, deal scores."""
    products = db.query(Product).all()

    category_data = {}
    for product in products:
        cat = product.category
        if cat not in category_data:
            category_data[cat] = {
                "products": 0,
                "prices": [],
                "ratings": [],
                "discounts": []
            }

        category_data[cat]["products"] += 1

        listings = db.query(ProductListing).filter(
            ProductListing.product_id == product.id
        ).all()
        reviews = db.query(Review).filter(Review.product_id == product.id).all()

        for l in listings:
            if l.price:
                category_data[cat]["prices"].append(l.price)
            if l.discount_percent:
                category_data[cat]["discounts"].append(l.discount_percent)
        for r in reviews:
            if r.rating:
                category_data[cat]["ratings"].append(r.rating)

    result = []
    for cat, data in category_data.items():
        result.append({
            "category": cat,
            "product_count": data["products"],
            "avg_price": round(sum(data["prices"]) / len(data["prices"])) if data["prices"] else 0,
            "avg_rating": round(sum(data["ratings"]) / len(data["ratings"]), 2) if data["ratings"] else 0,
            "avg_discount": round(sum(data["discounts"]) / len(data["discounts"]), 1) if data["discounts"] else 0,
        })

    return result


@router.get("/platform-comparison")
def get_platform_comparison(db: Session = Depends(get_db)):
    """Compare prices across platforms."""
    platforms = db.query(
        ProductListing.platform,
        func.count(ProductListing.id).label("listings"),
        func.avg(ProductListing.price).label("avg_price"),
        func.avg(ProductListing.discount_percent).label("avg_discount"),
    ).group_by(ProductListing.platform).all()

    return [
        {
            "platform": p[0],
            "listings": p[1],
            "avg_price": round(p[2] or 0),
            "avg_discount": round(p[3] or 0, 1),
        }
        for p in platforms
    ]


@router.get("/sentiment-overview")
def get_sentiment_overview(db: Session = Depends(get_db)):
    """Review sentiment by category."""
    from agents.shopping_agents import ReviewAnalysisAgent
    agent = ReviewAnalysisAgent()

    products = db.query(Product).all()
    category_reviews = {}

    for product in products:
        cat = product.category
        reviews = db.query(Review).filter(Review.product_id == product.id).all()
        if cat not in category_reviews:
            category_reviews[cat] = []
        category_reviews[cat].extend([
            {"rating": r.rating, "title": r.title, "body": r.body}
            for r in reviews
        ])

    result = []
    for cat, reviews in category_reviews.items():
        if reviews:
            analysis = agent.analyze(reviews)
            result.append({
                "category": cat,
                "avg_rating": analysis["average_rating"],
                "sentiment": analysis["overall_sentiment"],
                "review_count": analysis["total_reviews"],
                "top_pros": analysis["pros"][:2],
                "top_cons": analysis["cons"][:1],
            })

    return result
