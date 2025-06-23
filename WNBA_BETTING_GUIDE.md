# WNBA Betting & DFS Analysis Documentation
## Real-Time Data Analysis for Tomorrow's Games

### 🎯 **Overview**

The WNBA Real-Time Analyzer provides actionable betting recommendations for tomorrow's WNBA games using:
- Current player statistics and performance data
- Real-time injury reports and player status
- Live betting odds from multiple sportsbooks
- Advanced confidence scoring system
- DFS value analysis with salary cap optimization

---

## 🚀 **Quick Start Guide**

### **1. Basic Usage**
```bash
# Run real-time WNBA analysis for tomorrow's games
python real_wnba_analyzer.py

# Via CLI with mode selection
python run_bot.py --mode wnba

# Via project manager
python manage.py wnba
```

### **2. What You'll Get**
- **Tomorrow's Game Schedule**: Actual WNBA games with times and matchups
- **Player Value Rankings**: Top DFS value plays with salary and projections
- **Betting Recommendations**: Specific bets with confidence scores
- **Player Props**: Individual prop bets with detailed confidence analysis

---

## 📊 **Understanding the Output**

### **Game Information**
```
🏀 Game 1: New York Liberty @ Las Vegas Aces
   🕒 7:00 PM ET
   🌟 Key Players to Watch:
      ✅ A'ja Wilson (C) - 44.9 proj pts
      ✅ Breanna Stewart (F) - 45.6 proj pts
```

### **DFS Value Analysis**
```
🏀 #1 A'ja Wilson (C) - LV
     ✅ Salary: $11,500 | Proj: 44.9pts | Value: 3.90
     Stats: 27.3pts, 11.9reb, 2.5ast
```

**Key Metrics:**
- **Salary**: DFS platform cost
- **Projection**: Expected fantasy points
- **Value**: Points per $1000 salary (higher = better value)
- **Status**: ✅ Healthy, ⚠️ Questionable, ❌ Out

---

## 🎯 **Betting Recommendations**

### **Confidence Score System**

| Score | Color | Meaning | Action |
|-------|-------|---------|---------|
| 🟢 80%+ | Green | High Confidence | **Strong Bet** |
| 🟡 65-79% | Yellow | Medium Confidence | Moderate Bet |
| 🔴 <65% | Red | Low Confidence | **Avoid** |

### **Bet Types Analyzed**

#### **1. Point Spreads**
```
📊 Point Spread: Las Vegas Aces -4.5
    🟢 Confidence: 82%
    💡 Aces have strong recent form and favorable matchup
```

#### **2. Total Points (Over/Under)**
```
📊 Total Points: OVER 165.5
    🟡 Confidence: 71%
    💡 Both teams average pace suggests over total
```

#### **3. Player Props**
```
🏀 A'ja Wilson - Points
   📊 OVER 26.5 | 🟢 Confidence: 85.2%
   Season Average: 27.3pts

🏀 Breanna Stewart - Rebounds  
   📊 UNDER 7.5 | 🟡 Confidence: 73.1%
   Season Average: 7.5reb
```

---

## 🏀 **Player Prop Confidence Factors**

### **How Confidence is Calculated**

1. **Base Confidence by Stat Type**:
   - Points: 75% (most predictable)
   - Rebounds: 70% 
   - Assists: 65%
   - Steals: 60%
   - Blocks: 55%

2. **Adjustments**:
   - **Player Consistency**: ±20%
   - **Recent Form**: ±30%
   - **Injury Status**: -15% if Questionable
   - **Matchup**: ±10%

3. **Final Score**: Capped at 95% maximum

### **Prop Types Available**

#### **Individual Props**
- **Points**: Over/under scoring totals
- **Rebounds**: Total rebounds (offensive + defensive)
- **Assists**: Assist totals
- **Steals**: Defensive steals
- **Blocks**: Shot blocks

#### **Combination Props** 
- **Points + Rebounds + Assists**: Popular "triple" prop
- **Double-Doubles**: 10+ in two categories
- **Player vs. Player**: Head-to-head comparisons

---

## 📋 **Daily Workflow**

### **Morning Routine (Best Time: 9-11 AM)**
1. **Run Analysis**:
   ```bash
   python real_wnba_analyzer.py
   ```

2. **Review Output**:
   - Check tomorrow's games and times
   - Note key player statuses (injuries)
   - Identify high-confidence bets

3. **Cross-Reference**:
   - Compare with sportsbook lines
   - Look for value discrepancies
   - Check for line movement

### **Pre-Game Check (2-3 hours before)**
1. **Update Player Status**:
   - Rerun analysis for injury updates
   - Check starting lineups
   - Monitor line movements

2. **Final Bet Selection**:
   - Focus on 80%+ confidence bets
   - Avoid questionable players unless line adjusted
   - Consider live betting opportunities

---

## 🎲 **Bankroll Management**

### **Recommended Bet Sizing**

| Confidence | Bet Size | Risk Level |
|-----------|----------|------------|
| 🟢 85%+ | 3-5% of bankroll | **High** |
| 🟢 80-84% | 2-3% of bankroll | Medium-High |
| 🟡 70-79% | 1-2% of bankroll | Medium |
| 🟡 65-69% | 0.5-1% of bankroll | Low-Medium |
| 🔴 <65% | **AVOID** | Too Risky |

### **Daily Limits**
- **Maximum 3-4 bets per day**
- **Total daily risk: <10% of bankroll**
- **Track results for 30+ days before increasing**

---

## ⚙️ **Advanced Configuration**

### **Customizing Analysis**

#### **Player Pool Adjustment**
```python
# In real_wnba_analyzer.py, modify:
self.current_players = {
    'Player Name': {
        'team': 'TEAM', 'pos': 'G/F/C', 
        'ppg': 20.0, 'rpg': 5.0, 'apg': 4.0,
        'salary': 9000, 'status': 'Healthy'
    }
}
```

#### **Confidence Thresholds**
```python
# Adjust base confidence levels:
base_confidence = {
    'points': 0.80,      # Increase for more conservative
    'rebounds': 0.75,    # Decrease for more aggressive
    'assists': 0.70,
}
```

### **Integration with Sportsbooks**

#### **Line Shopping Workflow**
1. Run analyzer to get recommendations
2. Check lines at multiple books:
   - DraftKings
   - FanDuel  
   - BetMGM
   - Caesars
3. Take best available odds for high-confidence plays

#### **Live Betting Integration**
- Monitor line movements during games
- Look for middle opportunities
- Use confidence scores to guide in-game decisions

---

## 📈 **Performance Tracking**

### **What to Track**

#### **Daily Records**
```
Date: 2025-06-24
Games Analyzed: 4
Bets Made: 3
High Confidence (80%+): 2 wins, 0 losses
Medium Confidence (65-79%): 0 wins, 1 loss
Total P&L: +$150
```

#### **Weekly/Monthly Analysis**
- Win rate by confidence level
- ROI by bet type
- Best performing players/teams
- Worst performing matchups

### **Success Metrics**
- **Target Win Rate**: 55%+ overall
- **High Confidence Win Rate**: 65%+ 
- **Monthly ROI**: 5-15%
- **Maximum Drawdown**: <20%

---

## 🚨 **Important Warnings**

### **Risk Factors**
1. **Player Availability**: Always verify starting lineups
2. **Line Movement**: Significant movement may indicate insider info
3. **Back-to-Back Games**: Fatigue affects performance
4. **Playoff Context**: Regular season stats may not apply

### **Best Practices**
- ✅ Always bet within your means
- ✅ Track all bets for analysis
- ✅ Take breaks after losing streaks
- ✅ Never chase losses with bigger bets
- ❌ Don't bet on games you're emotionally invested in
- ❌ Don't override system with gut feelings
- ❌ Don't bet more than recommended percentages

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **No Games Found**
```bash
# Solution: Check if WNBA is in season
python real_wnba_analyzer.py --force-demo
```

#### **API Errors**
```bash
# Check API key
python manage.py status

# Verify API limits
# Odds API: 500 requests/month free tier
```

#### **Outdated Player Data**
```bash
# Update player statistics manually in real_wnba_analyzer.py
# Or wait for next season data update
```

### **Support Resources**
- **Project Documentation**: README.md, USAGE_GUIDE.md
- **API Documentation**: the-odds-api.com/docs
- **WNBA Stats**: wnba.com/stats
- **Injury Reports**: espn.com/wnba/injuries

---

## 📞 **Contact & Updates**

### **Getting Help**
1. Check documentation first
2. Run diagnostics: `python manage.py status`
3. Review error logs in terminal output
4. Update dependencies: `pip install -r requirements.txt`

### **Staying Updated**
- WNBA season runs May-October
- Player stats update nightly during season
- Playoff adjustments may be needed
- Monitor for rule changes affecting props

---

*Remember: This tool provides analysis and suggestions. All betting decisions and risks are your own. Always gamble responsibly.*
