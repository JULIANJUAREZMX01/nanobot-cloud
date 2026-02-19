#!/bin/bash
# Initialize cloud deployment on Render

set -e

echo "🚀 Initializing Nanobot Cloud Deployment"

# Check environment variables
check_env() {
    if [ -z "${!1}" ]; then
        echo "❌ Missing environment variable: $1"
        exit 1
    fi
}

check_env "TELEGRAM_TOKEN"
check_env "GROQ_API_KEY"
check_env "ANTHROPIC_API_KEY"

echo "✅ Environment variables verified"

# Create directories
mkdir -p data/sessions
mkdir -p workspace/memory
mkdir -p workspace/skills

echo "✅ Directories created"

# Install dependencies
echo "📦 Installing dependencies..."
pip install poetry
poetry install

echo "✅ Dependencies installed"

# Run initial setup
echo "🔧 Running initial setup..."
python -c "from app.main import app; print('✅ Application initialized')"

echo "🎉 Cloud deployment initialized successfully"
echo ""
echo "Next steps:"
echo "1. Set environment variables in Render dashboard"
echo "2. Deploy with: git push origin main"
echo "3. Access dashboard at: https://nanobot.onrender.com"
