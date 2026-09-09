from sqlalchemy import Column, Integer, String, Float, Text, JSON, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False, index=True)
    brand = Column(String(100), index=True)
    category = Column(String(100), index=True)
    subcategory = Column(String(100))
    description = Column(Text)
    image_url = Column(String(500))
    specifications = Column(JSON)  # dict of spec key-value pairs

    # Multi-source listings
    listings = relationship("ProductListing", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    price_history = relationship("PriceHistory", back_populates="product")

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductListing(Base):
    __tablename__ = "product_listings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # Amazon, Flipkart, Croma, etc.
    platform_product_id = Column(String(200))
    seller = Column(String(200))
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    discount_percent = Column(Float)
    url = Column(String(500))
    availability = Column(String(50), default="in_stock")
    delivery_info = Column(String(200))
    emi_options = Column(JSON)
    bank_offers = Column(JSON)
    in_stock = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="listings")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    platform = Column(String(50))
    reviewer_name = Column(String(200))
    rating = Column(Float)
    title = Column(String(500))
    body = Column(Text)
    verified_purchase = Column(Boolean, default=False)
    helpful_votes = Column(Integer, default=0)
    review_date = Column(String(50))

    product = relationship("Product", back_populates="reviews")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    platform = Column(String(50))
    price = Column(Float, nullable=False)
    date = Column(String(20), nullable=False)

    product = relationship("Product", back_populates="price_history")
