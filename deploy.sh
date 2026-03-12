#!/bin/bash
# Quick Deployment Script for CLPP Risk Prediction System
# This script prepares the project for deployment to Render (Backend) + Vercel (Frontend)

set -e  # Exit on error

echo "================================"
echo "CLPP Risk Prediction System"
echo "Production Deployment Preparation"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${BLUE}[1/6]${NC} Checking prerequisites..."
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}Git not found. Please install Git.${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Node.js not found. Please install Node.js.${NC}"
    exit 1
fi

if ! command -v python &> /dev/null; then
    echo -e "${YELLOW}Python not found. Please install Python.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ All prerequisites found${NC}"
echo ""

# Step 2: Verify and build frontend
echo -e "${BLUE}[2/6]${NC} Building frontend for production..."
cd frontend
npm run build
cd ..
echo -e "${GREEN}✓ Frontend build complete${NC}"
echo ""

# Step 3: Verify backend model
echo -e "${BLUE}[3/6]${NC} Verifying backend model..."
if [ -f "backend/trained_model.pkl" ] && [ -f "backend/scaler.pkl" ]; then
    echo -e "${GREEN}✓ Model files found${NC}"
else
    echo -e "${YELLOW}⚠ Model files not found. Training model...${NC}"
    cd backend
    python model.py
    cd ..
fi
echo ""

# Step 4: Check Git status
echo -e "${BLUE}[4/6]${NC} Checking Git status..."
if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git repository initialized${NC}"
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo -e "${YELLOW}⚠ You have uncommitted changes${NC}"
        read -p "Commit changes before deployment? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git add .
            read -p "Enter commit message: " commit_message
            git commit -m "$commit_message"
        fi
    fi
else
    echo -e "${YELLOW}Git repository not found${NC}"
fi
echo ""

# Step 5: Display deployment information
echo -e "${BLUE}[5/6]${NC} Deployment information..."
echo -e "${GREEN}Backend:${NC}"
echo "  - Framework: FastAPI"
echo "  - Location: ./backend"
echo "  - Deploy to: Render"
echo "  - Model: Logistic Regression (98.33% accuracy)"
echo ""
echo -e "${GREEN}Frontend:${NC}"
echo "  - Framework: React + Vite"
echo "  - Build: ./frontend/dist"
echo "  - Deploy to: Vercel"
echo ""

# Step 6: Deployment instructions
echo -e "${BLUE}[6/6]${NC} Next steps..."
echo ""
echo -e "${GREEN}1. Deploy Backend to Render:${NC}"
echo "   a) Go to https://render.com"
echo "   b) Create new Web Service"
echo "   c) Connect GitHub repository"
echo "   d) Set Build Command:"
echo "      pip install -r backend/requirements.txt && python backend/model.py"
echo "   e) Set Start Command:"
echo "      uvicorn backend.app:app --host 0.0.0.0 --port \$PORT"
echo "   f) Set Environment Variables:"
echo "      CORS_ORIGINS=https://your-app.vercel.app"
echo "   g) Deploy and note the API URL"
echo ""
echo -e "${GREEN}2. Deploy Frontend to Vercel:${NC}"
echo "   a) Go to https://vercel.com"
echo "   b) Import your GitHub repository"
echo "   c) Set Root Directory to 'frontend'"
echo "   d) Set Environment Variable:"
echo "      VITE_API_URL=https://your-backend-api.onrender.com"
echo "   e) Deploy"
echo ""
echo -e "${GREEN}3. Update Configuration:${NC}"
echo "   a) Update frontend/.env.production with backend API URL"
echo "   b) Commit and push to trigger auto-deploy"
echo ""

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Deployment Preparation Complete!${NC}"
echo -e "${GREEN}================================${NC}"
