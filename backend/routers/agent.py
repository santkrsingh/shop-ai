"""AI Shopping Agent router - natural language queries."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.models import Product, ProductListing, Review, PriceHistory
from models.schemas import AgentQueryRequest
from agents.shopping_agents import ShoppingOrchestrator, QueryUnderstandingAgent

router = APIRouter(prefix="/api/agent", tags=["AI Agent"])

orchestrator = ShoppingOrchestrator()
query_agent = QueryUnderstandingAgent()


def _get_all_products_with_data(db: Session, category_filter: str = None) -> list:
    """Load all products with their pricing and rating data for scoring."""
    query = db.query(Product)
    if category_filter:
        query = query.filter(Product.category.ilike(f"%{category_filter}%"))
    
    products = query.all()
    result = []

    for product in products:
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

        from agents.shopping_agents import PriceIntelligenceAgent
        price_intel = PriceIntelligenceAgent().analyze(product.id, listings_data, history_data)

        result.append({
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "subcategory": product.subcategory,
            "description": product.description or "",
            "image_url": product.image_url,
            "specifications": product.specifications or {},
            "best_price": best_price,
            "best_platform": best_listing.platform if best_listing else None,
            "avg_rating": round(avg_rating, 2) if avg_rating else 0,
            "review_count": len(reviews),
            "deal_score": price_intel.get("deal_score", 50),
            "price_intelligence": price_intel,
            "listings": [
                {
                    "id": l.id, "platform": l.platform, "seller": l.seller,
                    "price": l.price, "original_price": l.original_price,
                    "discount_percent": l.discount_percent,
                    "availability": l.availability, "delivery_info": l.delivery_info,
                    "in_stock": l.in_stock
                }
                for l in listings
            ],
        })

    return result


@router.post("/query")
def process_agent_query(request: AgentQueryRequest, db: Session = Depends(get_db)):
    """
    Full AI shopping agent pipeline.
    Parses query → searches products → scores → analyzes → returns ranked results.
    """
    # Parse query first to filter by category
    parsed = query_agent.parse(request.query)
    category = parsed.get("category")

    # Load products (filtered by category if detected)
    products = _get_all_products_with_data(db, category)

    # Run full orchestration
    result = orchestrator.process_query(request.query, products)
    return result


@router.post("/parse")
def parse_query(request: AgentQueryRequest):
    """Parse a natural language query into structured parameters."""
    return query_agent.parse(request.query)


@router.get("/demo-queries")
def get_demo_queries():
    """Return demo queries for the UI."""
    return [
        {
            "query": "Find the best laptop for a CSE student under ₹70,000 with 16GB RAM, SSD and dedicated GPU",
            "description": "Student gaming/coding laptop"
        },
        {
            "query": "Best smartphone under 35000 with great camera",
            "description": "Mid-range camera phone"
        },
        {
            "query": "Premium laptop for video editing with OLED display",
            "description": "Creator professional laptop"
        },
        {
            "query": "Wireless headphones with best noise cancellation",
            "description": "ANC headphones"
        },
        {
            "query": "Gaming laptop under 90000 with RTX GPU",
            "description": "Gaming laptop"
        },
        {
            "query": "Best budget laptop under 40000 for office work",
            "description": "Budget office laptop"
        }
    ]
