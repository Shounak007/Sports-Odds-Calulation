#!/bin/bash

# Sports Betting Bot - Quick Deployment Script
# This script helps prepare your app for deployment

echo "🚀 Preparing Sports Betting Bot for Deployment"
echo "=============================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Sports Betting Bot"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository found"
fi

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Check if Procfile exists
if [ -f "Procfile" ]; then
    echo "✅ Procfile found"
else
    echo "❌ Procfile not found"
    exit 1
fi

# Check if .env file exists (should not be committed)
if [ -f ".env" ]; then
    echo "⚠️  .env file found - make sure it's in .gitignore"
    if [ ! -f ".gitignore" ] || ! grep -q ".env" .gitignore; then
        echo ".env" >> .gitignore
        echo "✅ Added .env to .gitignore"
    fi
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << EOL
# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
betting_bot/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOL
    echo "✅ Created .gitignore"
fi

echo ""
echo "🎯 Deployment Options:"
echo "====================="
echo ""
echo "1. 🔥 Railway (Recommended - Free tier available)"
echo "   → Go to: https://railway.app"
echo "   → Deploy from GitHub repo"
echo "   → Set ODDS_API_KEY environment variable"
echo ""
echo "2. 🎨 Render (Free tier - 750 hours/month)"
echo "   → Go to: https://render.com"
echo "   → Create Web Service from GitHub"
echo "   → Set ODDS_API_KEY environment variable"
echo ""
echo "3. ⚡ Vercel (Serverless)"
echo "   → Install: npm i -g vercel"
echo "   → Run: vercel --prod"
echo ""
echo "4. 🌊 DigitalOcean App Platform (\$5/month)"
echo "   → Go to: https://digitalocean.com"
echo "   → Create App from GitHub"
echo ""
echo "📚 Full deployment guide: ./DEPLOYMENT_GUIDE.md"
echo ""
echo "🔑 Don't forget to:"
echo "   1. Get API key from: https://the-odds-api.com"
echo "   2. Set ODDS_API_KEY as environment variable"
echo "   3. Push your code to GitHub first"
echo ""
echo "✅ Your app is ready for deployment!"
