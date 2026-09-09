"""
FastAPI Main Application - Intelligent Shopping Agent
Production-ready: auto-seeds DB on first start, CORS open for Vercel frontend.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models.models import Base
from routers import products, agent, dashboard

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intelligent Shopping Agent API",
    description="AI-powered multi-source e-commerce shopping assistant",
    version="1.0.0",
)

# CORS — allow all origins so any Vercel/custom domain works
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router)
app.include_router(agent.router)
app.include_router(dashboard.router)


@app.on_event("startup")
def auto_seed():
    """Seed the database on first startup if it's empty."""
    from database import SessionLocal
    from models.models import Product
    db = SessionLocal()
    try:
        count = db.query(Product).count()
        if count == 0:
            print("Database is empty - seeding sample data...")
            from data.seed_data import seed_database
            seed_database()
            print("Seeding complete.")
        else:
            print(f"Database ready - {count} products loaded.")
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "name": "Intelligent Shopping Agent API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "products": "/api/products",
            "agent": "/api/agent/query",
            "dashboard": "/api/dashboard/stats",
        }
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
