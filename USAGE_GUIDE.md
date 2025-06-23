# Complete Usage Guide - Sports Betting Arbitrage & DFS Bot

## 🎯 Quick Start Guide

### 1. Basic Arbitrage Analysis
```bash
# Run with default settings (English Premier League)
python arbitrage_bot.py

# Use CLI for custom settings
python run_bot.py --sport basketball_nba --bet-size 200
```

### 2. DFS Analysis  
```bash
# Run DFS value analysis with simulated NBA data
python run_bot.py --mode dfs

# Direct DFS tool
python dfs_demo_tool.py
```

### 3. Historical Backtesting
```bash
# Analyze a specific date
python backtest_strategy.py --date "2024-01-15"

# Analyze a date range
python backtest_strategy.py --start-date "2024-01-01" --end-date "2024-01-07"
```

### 4. Real-Time WNBA Betting Analysis
```bash
# Analyze tomorrow's WNBA games with betting recommendations
python real_wnba_analyzer.py

# Via CLI mode
python run_bot.py --mode wnba

# Via project manager
python manage.py real-wnba
```

## 🔧 Advanced Usage

### Project Management Commands
```bash
# Check project status
python manage.py status

# Install dependencies
python manage.py install

# Run tests
python manage.py test

# Set up environment file
python manage.py setup-env

# Run different modes
python manage.py run        # Arbitrage bot
python manage.py dfs        # DFS analysis  
python manage.py cli        # CLI with options
python manage.py backtest   # Historical analysis
```

### CLI Options Reference
```bash
# Mode selection
--mode arbitrage    # Run arbitrage analysis (default)
--mode dfs         # Run DFS analysis

# Sport selection
--sport soccer_epl              # English Premier League
--sport basketball_nba          # NBA
--sport americanfootball_nfl    # NFL
--sport soccer_uefa_champs_league  # Champions League

# Region selection
--regions us       # United States bookmakers
--regions uk       # United Kingdom bookmakers  
--regions eu       # European bookmakers
--regions us uk eu # Multiple regions

# Market selection
--markets h2h               # Head-to-head (moneyline)
--markets spreads           # Point spreads
--markets totals            # Over/under totals
--markets h2h totals spreads # Multiple markets

# Betting parameters
--bet-size 100      # Total amount to bet ($100)
--bet-size 500      # Higher stake ($500)
--min-profit 1.0    # Minimum 1.0% profit margin
--min-profit 2.5    # Higher profit threshold

# Information
--list-options      # Show all available options
```

## 📊 Understanding the Output

### Arbitrage Opportunities
```
🎯 ARBITRAGE OPPORTUNITIES FOUND: 1
📋 OPPORTUNITY #1
Event: Manchester City vs Liverpool
Sport: English Premier League
Commence Time: 2024-01-15 15:00:00 UTC
Arbitrage Margin: 0.9750
Profit Margin: 2.50%
Guaranteed Profit: $2.41
Total Stake: $100.00

💰 BETTING STRATEGY:
  • Bet $48.78 on Manchester City
    Odds: 2.05 at Bet365
  • Bet $51.22 on Liverpool
    Odds: 1.95 at FanDuel
```

**Key Metrics:**
- **Arbitrage Margin**: Values < 1.0 indicate profit opportunity
- **Profit Margin**: Percentage profit guaranteed
- **Guaranteed Profit**: Dollar amount profit regardless of outcome
- **Betting Strategy**: Exact amounts to bet with each bookmaker

### DFS Value Analysis
```
💎 TOP DFS VALUE PLAYERS
🏀 # 1 Karl-Anthony Towns (C)
     Orlando Magic vs Brooklyn Nets
     Salary: $6,729  |  Projected: 39.2pts  |  Value: 5.82
     Confidence: 85%
     Points: 18.4 | Rebounds: 11.2 | Assists: 1.5
```

**Key Metrics:**
- **Value Score**: Projected points per $1K salary (higher is better)
- **Projected Points**: Expected DFS points based on statistical projections
- **Confidence**: Reliability of the projection (0-100%)
- **Key Stats**: Primary statistical categories for DFS scoring

### Real-Time WNBA Betting Analysis
```
🏀 A'ja Wilson - Points Prop
   📊 OVER 26.5 | 🟢 Confidence: 85.2%
   Season Average: 27.3 points
   Recommendation: STRONG BET (3-5% bankroll)
```

**Confidence Scores:**
- 🟢 **80%+ = High Confidence**: Strong betting recommendation
- 🟡 **65-79% = Medium Confidence**: Moderate betting opportunity  
- 🔴 **<65% = Low Confidence**: Avoid these bets

## ⚙️ Configuration Options

### config.py Settings
```python
# API Configuration
API_KEY = 'your_api_key_here'
SPORT = 'soccer_epl'           # Default sport
REGIONS = ['us', 'uk', 'eu']   # Regions to check
MARKETS = ['h2h']              # Markets to analyze
BET_SIZE = 100                 # Default bet size
MIN_PROFIT_MARGIN = 0.5        # Minimum profit % to display

# Display Settings
DECIMAL_PLACES = 4             # Calculation precision
MIN_REQUESTS_REMAINING = 10    # API warning threshold
```

### Environment Variables (.env)
```bash
ODDS_API_KEY=your_actual_api_key_here
```

## 🏈 Sport-Specific Usage

### NBA (Basketball)
```bash
# NBA arbitrage
python run_bot.py --sport basketball_nba --regions us

# NBA DFS analysis
python run_bot.py --mode dfs --sport basketball_nba

# NBA player props (when available)
python run_bot.py --sport basketball_nba --markets player_points player_rebounds
```

### NFL (American Football) 
```bash
# NFL arbitrage
python run_bot.py --sport americanfootball_nfl --regions us

# NFL with spreads and totals
python run_bot.py --sport americanfootball_nfl --markets h2h spreads totals
```

### Soccer/Football
```bash
# Premier League
python run_bot.py --sport soccer_epl --regions uk eu

# Champions League
python run_bot.py --sport soccer_uefa_champs_league --regions eu
```

## 🔍 Troubleshooting Guide

### Common Issues

**1. No Opportunities Found**
```
📊 No arbitrage opportunities found.
```
This is normal! Arbitrage opportunities are rare and disappear quickly.

**2. API Errors**
```
❌ Request failed: 422 Client Error
```
- Check if the sport is currently in season
- Verify market availability for the sport
- Try different regions or markets

**3. Rate Limiting**
```
⚠️ Rate limit exceeded. Retrying in 5 seconds...
```
The bot handles this automatically. Historical endpoints use more requests.

**4. Import Errors**
```bash
# Install missing dependencies
pip install -r requirements.txt

# Or use the management utility
python manage.py install
```

### Validation Commands
```bash
# Test entire setup
python test_setup.py

# Check project status  
python manage.py status

# Validate configuration
python -c "import config; print('Config OK')"
```

## 📈 Performance Tips

### Maximizing Opportunities
1. **Multiple Sports**: Check different sports throughout the day
2. **Multiple Regions**: More bookmakers = more opportunities  
3. **Lower Thresholds**: Set `--min-profit 0.5` to catch smaller opportunities
4. **Timing**: Run during peak betting hours (evenings, weekends)

### API Efficiency
1. **Focus on Active Sports**: Check which sports are in season
2. **Limit Markets**: Don't request all markets if you only need h2h
3. **Monitor Usage**: Watch the "requests remaining" counter
4. **Historical Sparingly**: Historical endpoints cost 5x more requests

### DFS Strategy
1. **Value Focus**: Players with value scores > 4.0 are strong plays
2. **Confidence Weighting**: Higher confidence players for cash games
3. **Stacking**: Consider players from the same game for correlation
4. **Salary Balance**: Don't just chase the cheapest players

## 🚨 Important Disclaimers

### Legal Considerations
- Arbitrage betting is mathematically legal but may violate bookmaker terms
- DFS analysis is for educational and research purposes
- Check local laws regarding sports betting and DFS
- This tool is designed for learning, not professional gambling

### Risk Management
- **Bookmaker Limits**: Accounts may be limited for consistent arbitrage betting  
- **Odds Movement**: Opportunities can disappear within minutes
- **Bet Limits**: Some bookmakers have minimum/maximum bet requirements
- **Market Availability**: Not all markets available at all times

### Technical Limitations
- **Simulated DFS Data**: Player props use simulated data when live data unavailable
- **API Dependencies**: Functionality depends on The Odds API availability
- **Rate Limits**: Free API tiers have request limitations
- **Market Coverage**: Not all bookmakers or markets may be available

## 📞 Support Resources

- **The Odds API Documentation**: https://the-odds-api.com/liveapi/guides/v4/
- **Project Issues**: Check troubleshooting section in README.md
- **Configuration Help**: Review config.py comments and examples
- **Setup Validation**: Run `python test_setup.py` for diagnostics

---

**Happy Betting & DFS Analysis!** 🎯💰📊
