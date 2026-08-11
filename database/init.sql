-- Think9 Pulse Database Schema Initialization Script
-- Supported Database: PostgreSQL 15+ with pgvector

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Brands Table
CREATE TABLE IF NOT EXISTS brands (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL UNIQUE,
    sector VARCHAR(100) NOT NULL,
    description TEXT,
    target_consumer TEXT,
    positioning TEXT,
    product_categories JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_brands_sector ON brands(sector);

-- 2. Signals Table
CREATE TABLE IF NOT EXISTS signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(100) NOT NULL,
    source_url TEXT,
    title VARCHAR(255),
    content TEXT NOT NULL,
    signal_type VARCHAR(100) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    sentiment FLOAT NOT NULL DEFAULT 0.0,
    signal_strength FLOAT NOT NULL DEFAULT 0.5,
    geography VARCHAR(100) DEFAULT 'US/Global',
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding vector(768)
);

CREATE INDEX IF NOT EXISTS idx_signals_sector ON signals(sector);
CREATE INDEX IF NOT EXISTS idx_signals_source ON signals(source);
CREATE INDEX IF NOT EXISTS idx_signals_detected_at ON signals(detected_at DESC);

-- 3. Trends Table
CREATE TABLE IF NOT EXISTS trends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    sector VARCHAR(100) NOT NULL,
    momentum_score FLOAT NOT NULL DEFAULT 0.0,
    confidence_score FLOAT NOT NULL DEFAULT 0.0,
    growth_rate FLOAT NOT NULL DEFAULT 0.0,
    signal_count INT NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'EMERGING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_trends_sector ON trends(sector);
CREATE INDEX IF NOT EXISTS idx_trends_status ON trends(status);

-- 4. Evidence Table
CREATE TABLE IF NOT EXISTS evidence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trend_id UUID NOT NULL REFERENCES trends(id) ON DELETE CASCADE,
    signal_id UUID NOT NULL REFERENCES signals(id) ON DELETE CASCADE,
    evidence_type VARCHAR(100) NOT NULL,
    relevance_score FLOAT NOT NULL DEFAULT 0.0,
    explanation TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_evidence_trend_id ON evidence(trend_id);
CREATE INDEX IF NOT EXISTS idx_evidence_signal_id ON evidence(signal_id);

-- 5. Opportunities Table
CREATE TABLE IF NOT EXISTS opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trend_id UUID REFERENCES trends(id) ON DELETE SET NULL,
    brand_id UUID REFERENCES brands(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    consumer_need TEXT NOT NULL,
    target_consumer TEXT NOT NULL,
    product_concept TEXT NOT NULL,
    positioning TEXT NOT NULL,
    confidence_score FLOAT NOT NULL DEFAULT 0.0,
    risk_score FLOAT NOT NULL DEFAULT 0.0,
    status VARCHAR(50) NOT NULL DEFAULT 'IN_REVIEW',
    recommended_action TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_opportunities_brand_id ON opportunities(brand_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_trend_id ON opportunities(trend_id);

-- 6. Pipeline Runs Table
CREATE TABLE IF NOT EXISTS pipeline_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scenario_name VARCHAR(150) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    current_stage VARCHAR(100) NOT NULL DEFAULT 'NOT_STARTED',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_pipeline_runs_status ON pipeline_runs(status);
