import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add backend and project root directory to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
backend_dir = os.path.join(project_root, "backend")
sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models import Brand, Signal, Trend, Evidence, Opportunity, PipelineRun
import uuid

# In-memory SQLite engine for fast testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Create test Brand
    brand = Brand(
        id=uuid.uuid4(),
        name="NutriPulse Test",
        sector="Food & Beverage",
        description="Functional test nutrition brand",
        target_consumer="Fitness enthusiasts",
        positioning="High protein clean fuel",
        product_categories=["Protein Snacks"]
    )
    db.add(brand)

    # Create test Signal
    signal = Signal(
        id=uuid.uuid4(),
        source="Reddit",
        title="Test savory protein demand",
        content="SIMULATED TEST DATA: Need savory protein options",
        signal_type="consumer_forum_post",
        sector="Food & Beverage",
        sentiment=0.7,
        signal_strength=0.9
    )
    db.add(signal)

    # Create test Trend
    trend = Trend(
        id=uuid.uuid4(),
        name="Savory High-Protein Quick Formats",
        description="Demand for savory protein",
        sector="Food & Beverage",
        momentum_score=88.0,
        confidence_score=90.0,
        growth_rate=120.0,
        signal_count=1,
        status="EMERGING"
    )
    db.add(trend)

    # Create test Evidence
    evidence = Evidence(
        id=uuid.uuid4(),
        trend_id=trend.id,
        signal_id=signal.id,
        evidence_type="DIRECT_MENTION",
        relevance_score=0.95,
        explanation="Test evidence explanation"
    )
    db.add(evidence)

    # Create test Opportunity
    opportunity = Opportunity(
        id=uuid.uuid4(),
        trend_id=trend.id,
        brand_id=brand.id,
        title="ProBite Test Savory Squares",
        description="Test savory egg & cheese bites",
        consumer_need="Quick savory breakfast",
        target_consumer="Urban professionals",
        product_concept="Savory egg bites 4-pack",
        positioning="High protein savory alternative",
        confidence_score=92.0,
        risk_score=15.0,
        status="IN_REVIEW",
        recommended_action="Approve test pilot"
    )
    db.add(opportunity)

    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
