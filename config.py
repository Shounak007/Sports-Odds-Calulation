# Configuration file for the Sports Betting Arbitrage Bot
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_KEY = os.getenv('ODDS_API_KEY', '0256eec25a95eaabcc609212e27a3a8a')
BASE_URL = 'https://api.the-odds-api.com'

# Betting Configuration
SPORT = 'soccer_epl'  # Default sport (English Premier League)
REGIONS = ['us', 'uk', 'eu']  # Regions to check for odds
MARKETS = ['h2h']  # Markets to analyze (head-to-head, totals, spreads)
ODDS_FORMAT = 'decimal'  # Use decimal odds for calculations
BET_SIZE = 100  # Total amount to bet for profit calculation

# API Request Configuration
REQUEST_TIMEOUT = 30  # Request timeout in seconds
MAX_RETRIES = 3  # Maximum number of retries for API requests
RETRY_DELAY = 5  # Delay between retries in seconds

# Display Configuration
MIN_PROFIT_MARGIN = 0.5  # Minimum profit margin percentage to display
DECIMAL_PLACES = 4  # Number of decimal places for calculations

# Rate Limiting Configuration
MIN_REQUESTS_REMAINING = 10  # Minimum requests before warning

# Available sports (common ones)
AVAILABLE_SPORTS = {
    'soccer_epl': 'English Premier League',
    'soccer_uefa_champs_league': 'UEFA Champions League',
    'basketball_nba': 'NBA',
    'basketball_wnba': 'WNBA',
    'americanfootball_nfl': 'NFL',
    'baseball_mlb': 'MLB',
    'icehockey_nhl': 'NHL',
    'tennis_wta': 'WTA Tennis',
    'tennis_atp': 'ATP Tennis',
    'mma_mixed_martial_arts': 'MMA',
    'boxing_boxing': 'Boxing'
}

# Available regions
AVAILABLE_REGIONS = {
    'us': 'United States',
    'uk': 'United Kingdom',
    'eu': 'Europe',
    'au': 'Australia'
}

# Available markets
AVAILABLE_MARKETS = {
    'h2h': 'Head to Head (Moneyline)',
    'spreads': 'Point Spreads',
    'totals': 'Over/Under Totals',
    'outrights': 'Tournament Winner',
    'player_points': 'Player Points',
    'player_rebounds': 'Player Rebounds',
    'player_assists': 'Player Assists',
    'player_threes': 'Player Three-Pointers',
    'player_blocks': 'Player Blocks',
    'player_steals': 'Player Steals',
    'player_turnovers': 'Player Turnovers',
    'player_points_rebounds_assists': 'Player Points + Rebounds + Assists'
}
