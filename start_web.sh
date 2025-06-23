#!/bin/bash

# Sports Betting Bot - Web Interface Launcher
# Quick script to start the web dashboard

echo "🚀 Starting Sports Betting Bot Web Interface..."
echo "=================================================="

# Check if virtual environment exists
if [ ! -f "betting_bot/bin/python" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python manage.py install"
    exit 1
fi

# Check if API key is configured
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Please configure your API key:"
    echo "python manage.py setup-env"
    echo ""
    echo "Continuing anyway... (some features may not work)"
fi

echo "🌐 Starting web server..."
echo "📱 Open your browser to: http://localhost:8080"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the web application
./betting_bot/bin/python web_app.py
