# Web Interface User Guide
## Sports Betting Bot Dashboard

### 🌐 **Overview**

The Sports Betting Bot now includes a beautiful, user-friendly web interface that makes it easy to run all analyses without using the command line. The dashboard provides real-time access to arbitrage detection, DFS analysis, WNBA betting recommendations, and historical backtesting.

---

## 🚀 **Quick Start**

### **Method 1: Using the Start Script**
```bash
# Make script executable (one time only)
chmod +x start_web.sh

# Launch the web interface
./start_web.sh
```

### **Method 2: Using Project Manager**
```bash
python manage.py web
```

### **Method 3: Direct Launch**
```bash
python web_app.py
```

### **Access the Dashboard**
Once started, open your browser to: **http://localhost:8080**

---

## 🎯 **Dashboard Features**

### **Main Action Cards**

#### **1. 🔄 Arbitrage Analysis**
- **Purpose**: Find guaranteed profit opportunities across sportsbooks
- **What it does**: Scans multiple bookmakers for price discrepancies
- **Output**: Shows profitable betting combinations with stakes
- **When to use**: Daily, especially before major games

#### **2. 🏆 DFS Analysis** 
- **Purpose**: Daily Fantasy Sports optimization
- **What it does**: Analyzes player values and creates optimal lineups
- **Output**: Top value players with projections and salary info
- **When to use**: Daily for DFS contests

#### **3. 🏀 WNBA Betting**
- **Purpose**: Tomorrow's WNBA betting recommendations
- **What it does**: Analyzes player props with confidence scores
- **Output**: High-confidence betting recommendations
- **When to use**: Daily morning routine (9-11 AM)

#### **4. 📈 Backtest**
- **Purpose**: Historical analysis of arbitrage opportunities
- **What it does**: Shows what opportunities existed on past dates
- **Output**: Historical arbitrage data and profit potential
- **When to use**: Strategy development and validation

---

## 🎛️ **Advanced Controls**

### **System Status Panel**
- **Check Status**: Verify system health and API connectivity
- **Test Setup**: Run comprehensive system tests
- **Available Options**: View all supported sports and markets

### **Custom Arbitrage Panel**
- **Sport Selection**: Choose from NBA, WNBA, NFL, Premier League, MLB
- **Bet Size**: Set custom bet amount for calculations
- **Custom Analysis**: Run arbitrage analysis with your parameters

### **Confidence Score System**

| Color | Confidence | Action | Description |
|-------|------------|---------|-------------|
| 🟢 Green | 80%+ | **STRONG BET** | High probability, bet 3-5% of bankroll |
| 🟡 Yellow | 65-79% | **MODERATE BET** | Good opportunity, bet 1-3% of bankroll |
| 🔴 Red | <65% | **AVOID** | Too risky, skip this bet |

---

## 📊 **Understanding the Output**

### **Arbitrage Analysis Output**
```
🎯 ARBITRAGE OPPORTUNITIES FOUND: 1
===============================================

📋 OPPORTUNITY #1
Event: Lakers vs Warriors
Sport: NBA
Arbitrage Margin: 0.9734
Profit Margin: 2.66%
Guaranteed Profit: $5.32
Total Stake: $200.00

💰 BETTING STRATEGY:
• Bet $97.34 on Lakers
  Odds: 2.05 at DraftKings
• Bet $102.66 on Warriors  
  Odds: 1.95 at FanDuel
```

### **WNBA Analysis Output**
```
🏀 TOMORROW'S WNBA GAMES (June 24, 2025)
============================================
1. New York Liberty @ Las Vegas Aces (7:00 PM ET)

💰 HIGH CONFIDENCE BETS:
✅ A'ja Wilson OVER 26.5 Points | 🟢 Confidence: 85.2%
✅ Las Vegas Aces -4.5 | 🟢 Confidence: 82.1%

🎯 PLAYER PROPS:
📊 Breanna Stewart UNDER 7.5 Rebounds | 🟡 Confidence: 73.1%
```

### **DFS Analysis Output**
```
💎 TOP DFS VALUE PLAYERS
========================================

🏀 #1 Luka Doncic (PG)
     Salary: $8,497 | Projected: 51.6pts | Value: 6.08
     Confidence: 68%
     Points: 25.9 | Rebounds: 4.9 | Assists: 11.3
```

---

## ⚙️ **Configuration & Settings**

### **Default Settings**
- **Default Sport**: NBA (basketball_nba)
- **Default Bet Size**: $100
- **Default Regions**: US, UK, Europe
- **Default Markets**: Head-to-head (moneyline)
- **API Timeout**: 60 seconds per request

### **Customizing Analysis**
1. **Change Sport**: Use the dropdown in Custom Arbitrage panel
2. **Adjust Bet Size**: Enter new amount in the bet size field
3. **Select Date Range**: Use the backtest modal for historical analysis
4. **Multiple Runs**: You can run multiple analyses in sequence

### **Status Indicators**
- **🟢 Online**: System is healthy, API is responding
- **🔴 Offline**: System issues or API problems
- **⏳ Loading**: Analysis in progress (typically 10-60 seconds)

---

## 🕒 **Daily Workflow**

### **Morning Routine (9:00 - 11:00 AM)**
1. **Open Dashboard**: Navigate to http://localhost:8080
2. **Check Status**: Click "Check Status" to verify system health
3. **WNBA Analysis**: Click "WNBA Analysis" for tomorrow's games
4. **Review Recommendations**: Focus on 🟢 high-confidence bets
5. **Cross-reference**: Compare with your sportsbook lines

### **Pre-Game Check (2-3 hours before games)**
1. **Re-run WNBA**: Check for updated injury reports
2. **Arbitrage Scan**: Run arbitrage analysis for live opportunities
3. **Final Decisions**: Place bets on high-confidence recommendations

### **Evening Review**
1. **Backtest**: Run historical analysis to validate strategies
2. **DFS Check**: Prepare tomorrow's DFS lineups
3. **Performance**: Track your betting results

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **"Web page won't load"**
```bash
# Check if server is running
python manage.py status

# Restart web interface
python manage.py web
```

#### **"Analysis times out"**
- Check internet connection
- Verify API key is valid
- Try running analysis with fewer options

#### **"No results found"**
- Normal for arbitrage (opportunities are rare)
- Check if sport is in season
- Try different sport or date range

#### **"API errors"**
```bash
# Check API key configuration
python manage.py status

# Verify API limits
# Free tier: 500 requests/month
```

### **Performance Tips**
1. **Run during off-peak hours** for faster API responses
2. **Limit concurrent requests** - run one analysis at a time
3. **Clear output regularly** to keep interface responsive
4. **Refresh page** if interface becomes unresponsive

---

## 🔐 **Security & Best Practices**

### **Local Use Only**
- **Default binding**: 0.0.0.0:5000 (local network access)
- **No authentication**: Only use on trusted networks
- **API key protection**: Never share your .env file

### **Responsible Usage**
- **API limits**: Monitor usage to avoid hitting rate limits
- **Bet sizing**: Never exceed recommended bankroll percentages
- **Verification**: Always verify lines at actual sportsbooks
- **Record keeping**: Track all bets for tax and analysis purposes

### **Data Privacy**
- **No data storage**: Analysis runs in real-time, no history saved
- **Local processing**: All analysis happens on your computer
- **No telemetry**: No usage data sent to external services

---

## 📈 **Advanced Features**

### **Keyboard Shortcuts**
- **Ctrl+C**: Stop current analysis
- **F5**: Refresh page and clear output
- **Ctrl+Shift+R**: Hard refresh (clear cache)

### **Mobile Friendly**
- **Responsive design**: Works on tablets and phones
- **Touch optimized**: Large buttons for mobile use
- **Fast loading**: Minimal JavaScript for speed

### **Browser Compatibility**
- ✅ **Chrome** (recommended)
- ✅ **Firefox** 
- ✅ **Safari**
- ✅ **Edge**
- ❌ **Internet Explorer** (not supported)

---

## 🆘 **Getting Help**

### **Error Messages**
1. **Read the output**: Error details appear in the analysis output
2. **Check status**: Use "Check Status" button to diagnose issues
3. **Restart**: Close browser tab and restart web interface

### **Support Resources**
- **Documentation**: README.md, USAGE_GUIDE.md, WNBA_BETTING_GUIDE.md
- **Command Line**: All web features available via CLI
- **System Tests**: Run `python test_setup.py` for diagnostics

### **Common Solutions**
```bash
# Full system check
python manage.py status
python manage.py test

# Reset environment
python manage.py install

# Update dependencies
pip install -r requirements.txt
```

---

*The web interface makes sports betting analysis accessible to everyone. Start with small bets, track your results, and always bet responsibly!*
