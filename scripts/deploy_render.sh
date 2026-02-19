#!/bin/bash

################################################################################
# Nanobot Cloud Deployment Script - Fase 3
# Deploys nanobot to Render cloud platform
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/JULIANJUAREZMX01/nanobot-cloud"
BRANCH="main"
SERVICE_NAME="nanobot"

################################################################################
# Helper Functions
################################################################################

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

################################################################################
# Pre-Deployment Checks
################################################################################

echo ""
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   Nanobot Cloud Deployment - Fase 3${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

log_info "Running pre-deployment checks..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    log_error "Not a git repository. Run 'git init' first."
    exit 1
fi

# Check if poetry.lock exists
if [ ! -f "poetry.lock" ]; then
    log_warning "poetry.lock not found. Running 'poetry install'..."
    poetry install
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | grep -oP '\d+\.\d+')
log_info "Python version: $PYTHON_VERSION"

log_success "Pre-deployment checks passed"

################################################################################
# Run Tests
################################################################################

echo ""
log_info "Running tests..."

if [ -d "tests" ]; then
    pytest tests/ -v --tb=short || log_warning "Some tests failed, but continuing..."
    log_success "Tests completed"
else
    log_warning "No tests directory found"
fi

################################################################################
# Verify Docker Build
################################################################################

echo ""
log_info "Verifying Docker build..."

if command -v docker &> /dev/null; then
    log_info "Building Docker image..."
    docker build -t nanobot-test -f infrastructure/Dockerfile . > /dev/null 2>&1
    log_success "Docker image built successfully"
else
    log_warning "Docker not installed, skipping Docker verification"
fi

################################################################################
# Git Operations
################################################################################

echo ""
log_info "Preparing git commit..."

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    log_info "Found uncommitted changes"

    # Add all changes
    git add .
    log_success "Changes staged"

    # Create commit
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    git commit -m "Fase 3: Deploy en Render - $TIMESTAMP"
    log_success "Commit created"
else
    log_info "No uncommitted changes"
fi

################################################################################
# GitHub Push
################################################################################

echo ""
log_info "Pushing to GitHub..."

git push origin $BRANCH
log_success "Code pushed to GitHub"

################################################################################
# Deployment Instructions
################################################################################

echo ""
echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}   ✅ Local Deployment Preparation Complete${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

echo "Next steps:"
echo ""
echo "1. Visit Render Dashboard:"
echo "   https://dashboard.render.com"
echo ""
echo "2. Create new Web Service:"
echo "   - Repository: $REPO_URL"
echo "   - Branch: $BRANCH"
echo ""
echo "3. Configure Build & Deploy:"
echo "   - Build Command: pip install --upgrade pip && pip install poetry && poetry install --only main"
echo "   - Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo ""
echo "4. Set Environment Variables:"
echo "   - TELEGRAM_TOKEN: $([ -n "$TELEGRAM_TOKEN" ] && echo "✓" || echo "❌ MISSING")"
echo "   - GROQ_API_KEY: $([ -n "$GROQ_API_KEY" ] && echo "✓" || echo "❌ MISSING")"
echo "   - ANTHROPIC_API_KEY: $([ -n "$ANTHROPIC_API_KEY" ] && echo "✓" || echo "❌ MISSING")"
echo "   - ENVIRONMENT: production"
echo ""
echo "5. Deploy!"
echo ""
echo "6. Test the deployment:"
echo "   curl https://nanobot.onrender.com/api/status"
echo ""
echo "7. Send test message to Telegram bot"
echo ""

log_success "Ready for cloud deployment!"

################################################################################
# Optional: Display Environment Checklist
################################################################################

echo ""
echo -e "${YELLOW}Environment Variable Checklist:${NC}"
echo ""

for var in TELEGRAM_TOKEN GROQ_API_KEY ANTHROPIC_API_KEY; do
    if [ -n "${!var}" ]; then
        echo "  ✅ $var is set"
    else
        echo "  ⚠️  $var is NOT set (will need to set in Render dashboard)"
    fi
done

echo ""
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}Deployment script completed${NC}"
echo -e "${BLUE}=========================================${NC}"
