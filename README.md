# Sports Betting Arbitrage Bot 🤖

A comprehensive Python application that identifies arbitrage betting opportunities using The Odds API. An arbitrage opportunity exists when odds from different bookmakers allow a guaranteed profit regardless of the outcome.

## 🚀 Features

- **Real-time Arbitrage Detection**: Automatically finds arbitrage opportunities across multiple bookmakers
- **DFS Player Props Analysis**: Analyzes Daily Fantasy Sports value opportunities with simulated player data
- **Multiple Sports Support**: Works with NFL, NBA, Premier League, Champions League, and more
- **Historical Backtesting**: Analyze past opportunities using historical data
- **DFS Lineup Optimization**: Creates optimal DFS lineups based on value analysis
- **Configurable Parameters**: Customize sports, regions, markets, and bet sizes
- **Rate Limiting Handling**: Built-in API rate limiting and retry mechanisms
- **Colored Console Output**: Beautiful, easy-to-read terminal output
- **Comprehensive Error Handling**: Robust error handling for network and API issues

## 📋 Requirements

- Python 3.7+
- The Odds API key (get one at [the-odds-api.com](https://the-odds-api.com/))
- Internet connection

## 🛠 Installation

1. **Clone or download the project files**

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv betting_bot
   source betting_bot/bin/activate  # On Windows: betting_bot\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**:
   
   **Option 1: Using .env file (recommended)**
   ```bash
   cp .env.example .env
   # Edit .env file and add your API key
   ```
   
   **Option 2: Direct configuration**
   Edit `config.py` and replace `'YOUR_API_KEY_HERE'` with your actual API key.

## 🎯 Quick Start

### Basic Usage

Run the bot with default settings:
```bash
python arbitrage_bot.py
```

### Using the CLI Runner

The CLI runner provides an easy way to customize settings:

```bash
# Show available options
python run_bot.py --list-options

# Run arbitrage bot with custom sport
python run_bot.py --sport basketball_nba

# Run DFS analysis tool
python run_bot.py --mode dfs

# Run with custom bet size
python run_bot.py --bet-size 200

# Run with multiple regions
python run_bot.py --regions us uk eu

# Combine multiple options
python run_bot.py --sport soccer_epl --bet-size 500 --regions us uk --min-profit 1.0
```

### Historical Backtesting

Analyze past arbitrage opportunities:

```bash
# Single date analysis
python backtest_strategy.py --date "2024-01-15"

# Date range analysis
python backtest_strategy.py --start-date "2024-01-01" --end-date "2024-01-07"

# Custom sport and bet size
python backtest_strategy.py --date "2024-01-15" --sport basketball_nba --bet-size 200
```

### DFS Analysis & Demo

Analyze Daily Fantasy Sports opportunities:

```bash
# Run DFS analysis with simulated data
python run_bot.py --mode dfs

# Direct DFS demo tool
python dfs_demo_tool.py

# Using the management utility
python manage.py dfs
```

### **NEW: Real-Time WNBA Betting Analyzer**

Get actionable betting recommendations for tomorrow's WNBA games with confidence scores:

```bash
# Quick start - analyze tomorrow's WNBA games
python real_wnba_analyzer.py

# Via CLI
python run_bot.py --mode wnba

# Via project manager  
python manage.py real-wnba
```

**Features:**
- **Tomorrow's Game Schedule**: Real WNBA matchups with times
- **Player Prop Analysis**: Detailed prop bets with confidence scores (80%+ = high confidence)
- **DFS Value Rankings**: Top value players for daily fantasy
- **Live Betting Integration**: Real-time odds and arbitrage opportunities
- **Comprehensive Documentation**: See [WNBA_BETTING_GUIDE.md](WNBA_BETTING_GUIDE.md)

**Sample Output:**
```
🏀 Tomorrow's Games: June 24, 2025
   1. New York Liberty @ Las Vegas Aces (7:00 PM ET)
   
💰 HIGH CONFIDENCE BETS:
   ✅ A'ja Wilson OVER 26.5 Points | 🟢 Confidence: 85.2%
   ✅ Las Vegas Aces -4.5 | 🟢 Confidence: 82.1%

🎯 PLAYER PROPS:
   📊 Breanna Stewart UNDER 7.5 Rebounds | 🟡 Confidence: 73.1%
```

## 🌐 **NEW: Beautiful Web Dashboard**

Access all betting analysis tools through a modern web interface:

```bash
# Start the web dashboard
python manage.py web

# Or use the quick launcher
./start_web.sh

# Then open: http://localhost:8080
```

**Web Features:**
- **🎯 One-Click Analysis**: Run all tools with beautiful UI
- **📊 Real-Time Output**: See analysis results as they happen
- **📱 Mobile Friendly**: Works on phones, tablets, and desktops
- **🎨 Modern Design**: Bootstrap-powered responsive interface
- **⚡ Fast & Secure**: Local-only, no data sent to external servers

**Dashboard Tools:**
- **Arbitrage Finder**: Click to find guaranteed profit opportunities
- **DFS Optimizer**: Daily fantasy sports analysis and lineup building
- **WNBA Betting**: Tomorrow's games with confidence-scored props
- **Historical Backtest**: Analyze past opportunities by date
- **System Status**: Health checks and configuration validation

---

## ⚙️ Configuration

Edit `config.py` to customize default settings:

### API Configuration
- `API_KEY`: Your Odds API key
- `SPORT`: Default sport to analyze
- `REGIONS`: List of regions to check
- `MARKETS`: List of markets to analyze
- `BET_SIZE`: Total amount to bet for calculations

### Display Configuration
- `MIN_PROFIT_MARGIN`: Minimum profit margin to display (%)
- `DECIMAL_PLACES`: Precision for calculations

## 🏈 Supported Sports

| Sport Key | Description |
|-----------|-------------|
| `soccer_epl` | English Premier League |
| `soccer_uefa_champs_league` | UEFA Champions League |
| `basketball_nba` | NBA |
| `americanfootball_nfl` | NFL |
| `baseball_mlb` | MLB |
| `icehockey_nhl` | NHL |
| `tennis_wta` | WTA Tennis |
| `tennis_atp` | ATP Tennis |
| `mma_mixed_martial_arts` | MMA |
| `boxing_boxing` | Boxing |

## 🌍 Supported Regions

- `us` - United States
- `uk` - United Kingdom  
- `eu` - Europe
- `au` - Australia

## 📊 Supported Markets

- `h2h` - Head to Head (Moneyline)
- `spreads` - Point Spreads
- `totals` - Over/Under Totals
- `outrights` - Tournament Winner

## 📈 Understanding the Output

When arbitrage opportunities are found, the bot displays:

```
🎯 ARBITRAGE OPPORTUNITIES FOUND: 2
================================================================================

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

## 🔬 How Arbitrage Works

Arbitrage betting involves placing bets on all possible outcomes of an event with different bookmakers to guarantee a profit. The key is finding odds that, when combined, have an arbitrage percentage less than 1.0.

**Formula for 2-way markets:**
```
Arbitrage % = (1 / Odds_A) + (1 / Odds_B)
```

If the result is less than 1.0, an arbitrage opportunity exists.

**Example:**
- Team A: 2.10 odds at Bookmaker 1
- Team B: 2.05 odds at Bookmaker 2
- Arbitrage % = (1/2.10) + (1/2.05) = 0.476 + 0.488 = 0.964

Since 0.964 < 1.0, this is a profitable arbitrage opportunity with a 3.6% profit margin.

## 💎 DFS Analysis Features

The bot now includes comprehensive Daily Fantasy Sports analysis:

### DFS Value Analysis
- **Player Projections**: Simulated player statistics and DFS point projections
- **Salary Analysis**: Value scoring based on projected points per salary dollar
- **Position Optimization**: Analysis across all NBA positions (PG, SG, SF, PF, C)
- **Confidence Scoring**: Reliability metrics for each player projection

### Sample DFS Output
```
💎 TOP DFS VALUE PLAYERS

🏀 # 1 Karl-Anthony Towns (C)
     Orlando Magic vs Brooklyn Nets
     Salary: $6,729  |  Projected: 39.2pts  |  Value: 5.82
     Confidence: 85%
     Points: 18.4 | Rebounds: 11.2 | Assists: 1.5
```

### DFS Lineup Optimization
- **Optimal Lineup Creation**: Generates lineups that maximize projected points within salary constraints
- **Position Requirements**: Respects DFS site position requirements (DraftKings format)
- **Multiple Lineup Types**: Cash game, GPP, and balanced lineup strategies
- **CSV Export**: Export lineups for upload to DFS sites

## 🚨 Important Notes

### API Usage Costs
- **Regular endpoints**: 1 request per API call
- **Historical endpoints**: 5+ requests per API call
- Monitor your usage with the displayed "requests remaining" information

### Risk Considerations
- **Account Limits**: Bookmakers may limit or close accounts of arbitrage bettors
- **Odds Changes**: Odds can change quickly; act fast on opportunities
- **Market Availability**: Not all markets may be available at all bookmakers
- **Bet Limits**: Some bookmakers have minimum/maximum bet limits

### Legal Considerations
- Arbitrage betting is legal but may violate bookmaker terms of service
- Check local laws and regulations regarding sports betting
- This tool is for educational and research purposes

## 🛡️ Error Handling

The bot includes comprehensive error handling for:
- Network connectivity issues
- API rate limiting (with automatic retry)
- Invalid API responses
- Missing or malformed data
- Bookmaker-specific oddities

## 📝 File Structure

```
BettingBot/
├── arbitrage_bot.py         # Main arbitrage detection script
├── backtest_strategy.py     # Historical backtesting script
├── dfs_demo_tool.py        # DFS analysis with simulated data
├── dfs_props_analyzer.py   # Advanced DFS player props analyzer
├── dfs_lineup_optimizer.py # DFS lineup optimization engine
├── run_bot.py              # CLI runner with options
├── manage.py               # Project management utility
├── test_setup.py           # Setup validation and testing
├── config.py               # Configuration file
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
└── IMPLEMENTATION.md      # Technical implementation details
```

## 🔧 Advanced Configuration

### Custom Sports
To add custom sports, update the `AVAILABLE_SPORTS` dictionary in `config.py`:

```python
AVAILABLE_SPORTS = {
    'custom_sport_key': 'Custom Sport Name',
    # ... existing sports
}
```

### API Request Optimization
Adjust these settings in `config.py` for better performance:

```python
REQUEST_TIMEOUT = 30        # Request timeout
MAX_RETRIES = 3            # Maximum retries
RETRY_DELAY = 5            # Delay between retries
MIN_REQUESTS_REMAINING = 10 # Warning threshold
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**: Verify your API key is correctly set in `.env` or `config.py`

3. **No Opportunities Found**: This is normal! Arbitrage opportunities are rare and disappear quickly

4. **Rate Limiting**: The bot handles this automatically, but you can adjust `RETRY_DELAY` if needed

### Debug Mode
For detailed debugging, you can modify the code to add more verbose logging or use Python's built-in `logging` module.

## 📄 License

This project is for educational purposes. Please ensure compliance with local laws and bookmaker terms of service.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📞 Support

For API-related issues, visit [The Odds API Documentation](https://the-odds-api.com/liveapi/guides/v4/).

For bot-related issues, please check the troubleshooting section above.

---

**Disclaimer**: This tool is for educational and research purposes only. Gambling involves risk, and you should never bet more than you can afford to lose. The authors are not responsible for any losses incurred through the use of this software.
