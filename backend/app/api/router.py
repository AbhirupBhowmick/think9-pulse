from fastapi import APIRouter
from app.api.routes import health, brands, signals, trends, opportunities, pipeline

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(brands.router, tags=["Brands"])
api_router.include_router(signals.router, tags=["Signals"])
api_router.include_router(trends.router, tags=["Trends"])
api_router.include_router(opportunities.router, tags=["Opportunities"])
api_router.include_router(pipeline.router, tags=["Pipeline Execution"])
