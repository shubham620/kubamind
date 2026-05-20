-- KubeMind AI Database Initialization
-- This script initializes the PostgreSQL database for KubeMind AI

-- Create extensions
CREATE EXTENSION IF NOT EXISTS uuid-ossp;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- Create schema
CREATE SCHEMA IF NOT EXISTS kubemind;

-- Set schema search path
ALTER ROLE kubemind_user SET search_path TO kubemind, public;

-- Grant permissions
GRANT CONNECT ON DATABASE kubemind TO kubemind_user;
GRANT USAGE ON SCHEMA kubemind TO kubemind_user;
GRANT CREATE ON SCHEMA kubemind TO kubemind_user;

-- Create basic audit table
CREATE TABLE IF NOT EXISTS kubemind.audit_log (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(255) NOT NULL,
    entity_type VARCHAR(255),
    entity_id UUID,
    changes JSONB,
    created_by VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indices for performance
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON kubemind.audit_log (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_entity ON kubemind.audit_log (entity_type, entity_id);

GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA kubemind TO kubemind_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA kubemind TO kubemind_user;
