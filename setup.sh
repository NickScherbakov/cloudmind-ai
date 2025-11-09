#!/bin/bash

# CloudMind AI Setup Script
# This script helps set up the development environment

set -e

echo "=================================="
echo "CloudMind AI Setup"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed (V2 or V1)
DOCKER_COMPOSE_CMD=""
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
else
    echo "❌ Docker Compose is not installed. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit the .env file to add your cloud provider credentials"
    echo "   before running the application with actual cloud resources."
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Create credentials directory if it doesn't exist
if [ ! -d credentials ]; then
    echo "📁 Creating credentials directory..."
    mkdir -p credentials
    echo "✓ credentials directory created"
    echo ""
fi

# Ask user what they want to do
echo "What would you like to do?"
echo "1) Start in production mode (optimized, no hot-reload)"
echo "2) Start in development mode (with hot-reload)"
echo "3) Run tests"
echo "4) Build Docker images only"
echo "5) Stop all services"
echo "6) Clean up (remove containers, images, volumes)"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting CloudMind AI in production mode..."
        $DOCKER_COMPOSE_CMD up -d --build
        echo ""
        echo "✓ CloudMind AI is running!"
        echo "  API: http://localhost:8000"
        echo "  API Docs: http://localhost:8000/docs"
        echo ""
        echo "To view logs: $DOCKER_COMPOSE_CMD logs -f"
        echo "To stop: $DOCKER_COMPOSE_CMD down"
        ;;
    2)
        echo ""
        echo "🚀 Starting CloudMind AI in development mode..."
        $DOCKER_COMPOSE_CMD -f docker-compose.dev.yml up --build
        echo ""
        echo "✓ CloudMind AI is running in development mode!"
        echo "  API: http://localhost:8000"
        echo "  API Docs: http://localhost:8000/docs"
        echo "  Changes to source code will trigger auto-reload"
        ;;
    3)
        echo ""
        echo "🧪 Running tests..."
        $DOCKER_COMPOSE_CMD -f docker-compose.dev.yml up --build cloudmind-test
        ;;
    4)
        echo ""
        echo "🔨 Building Docker images..."
        $DOCKER_COMPOSE_CMD build
        $DOCKER_COMPOSE_CMD -f docker-compose.dev.yml build
        echo "✓ Docker images built successfully"
        ;;
    5)
        echo ""
        echo "🛑 Stopping all services..."
        $DOCKER_COMPOSE_CMD down
        $DOCKER_COMPOSE_CMD -f docker-compose.dev.yml down
        echo "✓ All services stopped"
        ;;
    6)
        echo ""
        echo "🧹 Cleaning up..."
        read -p "This will remove all containers, images, and volumes. Continue? (y/N): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            $DOCKER_COMPOSE_CMD down -v --rmi all
            $DOCKER_COMPOSE_CMD -f docker-compose.dev.yml down -v --rmi all
            echo "✓ Cleanup complete"
        else
            echo "Cleanup cancelled"
        fi
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
