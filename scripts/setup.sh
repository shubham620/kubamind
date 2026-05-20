#!/bin/bash

# KubeMind AI Setup Script

echo "🚀 KubeMind AI - Infrastructure Setup"
echo "======================================"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"

# Create .env file if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file from .env.example"
fi

# Create necessary directories
mkdir -p logs
mkdir -p data

echo "✓ Created necessary directories"

# Build backend
echo ""
echo "Building KubeMind backend..."
docker-compose build backend

# Start services
echo ""
echo "Starting services..."
docker-compose up -d

# Wait for services to be ready
echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check health
echo ""
echo "Checking service health..."

if curl -s http://localhost:8000/health > /dev/null; then
    echo "✓ Backend is healthy"
else
    echo "❌ Backend is not responding"
fi

if curl -s http://localhost:9090/-/healthy > /dev/null; then
    echo "✓ Prometheus is healthy"
else
    echo "❌ Prometheus is not responding"
fi

if curl -s http://localhost:3000/api/health > /dev/null; then
    echo "✓ Grafana is healthy"
else
    echo "❌ Grafana is not responding"
fi

echo ""
echo "======================================"
echo "✅ KubeMind AI setup complete!"
echo ""
echo "Services are running:"
echo "- Backend API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs"
echo "- Prometheus: http://localhost:9090"
echo "- Grafana: http://localhost:3000"
echo "- Loki: http://localhost:3100"
echo ""
echo "To stop services: docker-compose down"
