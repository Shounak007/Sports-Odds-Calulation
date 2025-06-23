"""
Sports Betting Arbitrage Bot
==========================

This bot identifies arbitrage betting opportunities using The Odds API.
An arbitrage opportunity exists when odds from different bookmakers allow
a guaranteed profit regardless of the outcome.

Author: GitHub Copilot
Date: June 2025
"""

import requests
import time
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json

# Import configuration
import config

try:
    from colorama import init, Fore, Style
    init()  # Initialize colorama for cross-platform colored output
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False


@dataclass
class ArbitrageOpportunity:
    """Data class to represent an arbitrage opportunity"""
    event_id: str
    sport: str
    home_team: str
    away_team: str
    commence_time: str
    outcomes: List[Dict]
    arbitrage_percentage: float
    profit_margin: float
    guaranteed_profit: float
    total_stake: float


class OddsAPIClient:
    """Client for interacting with The Odds API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = config.BASE_URL
        self.session = requests.Session()
        self.requests_remaining = None
        self.requests_used = None
        
    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        Make a request to The Odds API with error handling and rate limiting
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            
        Returns:
            JSON response data or None if request fails
        """
        url = f"{self.base_url}{endpoint}"
        params['apiKey'] = self.api_key
        
        for attempt in range(config.MAX_RETRIES):
            try:
                response = self.session.get(
                    url, 
                    params=params, 
                    timeout=config.REQUEST_TIMEOUT
                )
                
                # Update rate limit information
                self.requests_remaining = response.headers.get('x-requests-remaining')
                self.requests_used = response.headers.get('x-requests-used')
                
                # Check rate limiting
                if response.status_code == 429:
                    print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}⚠️  Rate limit exceeded. Retrying in {config.RETRY_DELAY} seconds...{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
                    time.sleep(config.RETRY_DELAY)
                    continue
                    
                response.raise_for_status()
                
                # Warn if requests are running low
                if self.requests_remaining and int(self.requests_remaining) < config.MIN_REQUESTS_REMAINING:
                    print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}⚠️  Warning: Only {self.requests_remaining} API requests remaining!{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
                
                return response.json()
                
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Request failed (attempt {attempt + 1}/{config.MAX_RETRIES}): {e}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
                if attempt < config.MAX_RETRIES - 1:
                    time.sleep(config.RETRY_DELAY)
                else:
                    return None
                    
        return None
    
    def get_sports(self) -> Optional[List[Dict]]:
        """
        Get list of available sports
        
        Returns:
            List of sports data or None if request fails
        """
        return self._make_request('/v4/sports', {})
    
    def get_odds(self, sport: str, regions: List[str], markets: List[str], 
                 odds_format: str = 'decimal') -> Optional[List[Dict]]:
        """
        Get odds for a specific sport
        
        Args:
            sport: Sport key
            regions: List of regions
            markets: List of markets
            odds_format: Format for odds (decimal, american)
            
        Returns:
            List of events with odds or None if request fails
        """
        params = {
            'regions': ','.join(regions),
            'markets': ','.join(markets),
            'oddsFormat': odds_format,
            'dateFormat': 'iso'
        }
        
        return self._make_request(f'/v4/sports/{sport}/odds', params)
    
    def get_historical_odds(self, sport: str, regions: List[str], markets: List[str], 
                           date: str, odds_format: str = 'decimal') -> Optional[List[Dict]]:
        """
        Get historical odds for a specific sport and date
        
        Args:
            sport: Sport key
            regions: List of regions
            markets: List of markets
            date: Date in ISO format (YYYY-MM-DDTHH:MM:SSZ)
            odds_format: Format for odds (decimal, american)
            
        Returns:
            List of events with historical odds or None if request fails
        """
        params = {
            'regions': ','.join(regions),
            'markets': ','.join(markets),
            'oddsFormat': odds_format,
            'dateFormat': 'iso',
            'date': date
        }
        
        return self._make_request(f'/v4/historical/sports/{sport}/odds', params)


class ArbitrageCalculator:
    """Calculator for finding arbitrage opportunities"""
    
    @staticmethod
    def calculate_arbitrage_percentage(odds: List[float]) -> float:
        """
        Calculate arbitrage percentage for given odds
        
        Args:
            odds: List of decimal odds for all outcomes
            
        Returns:
            Arbitrage percentage (< 1.0 indicates arbitrage opportunity)
        """
        return sum(1.0 / odd for odd in odds)
    
    @staticmethod
    def calculate_stakes(odds: List[float], total_stake: float) -> List[float]:
        """
        Calculate optimal stakes for each outcome to guarantee profit
        
        Args:
            odds: List of decimal odds for all outcomes
            total_stake: Total amount to stake
            
        Returns:
            List of stakes for each outcome
        """
        arbitrage_percentage = ArbitrageCalculator.calculate_arbitrage_percentage(odds)
        stakes = []
        
        for odd in odds:
            stake = (total_stake / arbitrage_percentage) * (1.0 / odd)
            stakes.append(round(stake, 2))
            
        return stakes
    
    @staticmethod
    def calculate_guaranteed_profit(odds: List[float], total_stake: float) -> float:
        """
        Calculate guaranteed profit from arbitrage opportunity
        
        Args:
            odds: List of decimal odds for all outcomes
            total_stake: Total amount to stake
            
        Returns:
            Guaranteed profit amount
        """
        arbitrage_percentage = ArbitrageCalculator.calculate_arbitrage_percentage(odds)
        
        if arbitrage_percentage >= 1.0:
            return 0.0
            
        stakes = ArbitrageCalculator.calculate_stakes(odds, total_stake)
        
        # Calculate profit for any outcome (should be the same for all)
        profit = (stakes[0] * odds[0]) - total_stake
        return round(profit, 2)


class ArbitrageFinder:
    """Main class for finding arbitrage opportunities"""
    
    def __init__(self, api_key: str):
        self.client = OddsAPIClient(api_key)
        self.calculator = ArbitrageCalculator()
        
    def find_arbitrage_opportunities(self, sport: str, regions: List[str], 
                                   markets: List[str], bet_size: float) -> List[ArbitrageOpportunity]:
        """
        Find arbitrage opportunities for a given sport
        
        Args:
            sport: Sport key
            regions: List of regions to check
            markets: List of markets to analyze
            bet_size: Total amount to bet
            
        Returns:
            List of arbitrage opportunities
        """
        print(f"{Fore.BLUE if COLORS_AVAILABLE else ''}🔍 Fetching odds data for {config.AVAILABLE_SPORTS.get(sport, sport)}...{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        events_data = self.client.get_odds(sport, regions, markets)
        
        if not events_data:
            print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Failed to fetch odds data{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return []
            
        if not events_data:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}⚠️  No events found for {sport}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return []
            
        print(f"{Fore.GREEN if COLORS_AVAILABLE else ''}✅ Found {len(events_data)} events{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        opportunities = []
        
        for event in events_data:
            event_opportunities = self._analyze_event(event, bet_size)
            opportunities.extend(event_opportunities)
            
        return opportunities
    
    def _analyze_event(self, event: Dict, bet_size: float) -> List[ArbitrageOpportunity]:
        """
        Analyze a single event for arbitrage opportunities
        
        Args:
            event: Event data from API
            bet_size: Total amount to bet
            
        Returns:
            List of arbitrage opportunities for this event
        """
        opportunities = []
        
        if not event.get('bookmakers'):
            return opportunities
            
        # Group outcomes by market
        markets_data = {}
        
        for bookmaker in event['bookmakers']:
            bookmaker_key = bookmaker['key']
            bookmaker_title = bookmaker['title']
            
            for market in bookmaker.get('markets', []):
                market_key = market['key']
                
                if market_key not in markets_data:
                    markets_data[market_key] = {}
                    
                for outcome in market.get('outcomes', []):
                    outcome_name = outcome['name']
                    price = float(outcome['price'])
                    
                    # Keep track of best odds for each outcome
                    if outcome_name not in markets_data[market_key]:
                        markets_data[market_key][outcome_name] = {
                            'best_odds': price,
                            'bookmaker': bookmaker_title,
                            'bookmaker_key': bookmaker_key
                        }
                    elif price > markets_data[market_key][outcome_name]['best_odds']:
                        markets_data[market_key][outcome_name] = {
                            'best_odds': price,
                            'bookmaker': bookmaker_title,
                            'bookmaker_key': bookmaker_key
                        }
        
        # Check each market for arbitrage opportunities
        for market_key, outcomes_data in markets_data.items():
            if len(outcomes_data) < 2:  # Need at least 2 outcomes
                continue
                
            # Extract odds and check for arbitrage
            outcome_names = list(outcomes_data.keys())
            odds = [outcomes_data[name]['best_odds'] for name in outcome_names]
            
            arbitrage_percentage = self.calculator.calculate_arbitrage_percentage(odds)
            
            if arbitrage_percentage < 1.0:  # Arbitrage opportunity found
                profit_margin = (1.0 - arbitrage_percentage) * 100
                
                if profit_margin >= config.MIN_PROFIT_MARGIN:
                    guaranteed_profit = self.calculator.calculate_guaranteed_profit(odds, bet_size)
                    stakes = self.calculator.calculate_stakes(odds, bet_size)
                    
                    # Create outcome details
                    outcomes = []
                    for i, name in enumerate(outcome_names):
                        outcomes.append({
                            'name': name,
                            'odds': odds[i],
                            'bookmaker': outcomes_data[name]['bookmaker'],
                            'bookmaker_key': outcomes_data[name]['bookmaker_key'],
                            'stake': stakes[i]
                        })
                    
                    opportunity = ArbitrageOpportunity(
                        event_id=event['id'],
                        sport=event['sport_key'],
                        home_team=event['home_team'],
                        away_team=event['away_team'],
                        commence_time=event['commence_time'],
                        outcomes=outcomes,
                        arbitrage_percentage=arbitrage_percentage,
                        profit_margin=profit_margin,
                        guaranteed_profit=guaranteed_profit,
                        total_stake=bet_size
                    )
                    
                    opportunities.append(opportunity)
        
        return opportunities
    
    def display_opportunities(self, opportunities: List[ArbitrageOpportunity]):
        """
        Display arbitrage opportunities in a formatted way
        
        Args:
            opportunities: List of arbitrage opportunities to display
        """
        if not opportunities:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}📊 No arbitrage opportunities found.{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return
            
        print(f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}🎯 ARBITRAGE OPPORTUNITIES FOUND: {len(opportunities)}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print("=" * 80)
        
        for i, opp in enumerate(opportunities, 1):
            print(f"\n{Fore.CYAN if COLORS_AVAILABLE else ''}📋 OPPORTUNITY #{i}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            print(f"Event: {opp.home_team} vs {opp.away_team}")
            print(f"Sport: {config.AVAILABLE_SPORTS.get(opp.sport, opp.sport)}")
            print(f"Commence Time: {datetime.fromisoformat(opp.commence_time.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"Arbitrage Margin: {opp.arbitrage_percentage:.{config.DECIMAL_PLACES}f}")
            print(f"Profit Margin: {opp.profit_margin:.2f}%")
            print(f"Guaranteed Profit: ${opp.guaranteed_profit:.2f}")
            print(f"Total Stake: ${opp.total_stake:.2f}")
            
            print(f"\n{Fore.YELLOW if COLORS_AVAILABLE else ''}💰 BETTING STRATEGY:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            for outcome in opp.outcomes:
                print(f"  • Bet ${outcome['stake']:.2f} on {outcome['name']}")
                print(f"    Odds: {outcome['odds']:.{config.DECIMAL_PLACES}f} at {outcome['bookmaker']}")
            
            print("-" * 80)


def main():
    """Main function to run the arbitrage finder"""
    print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}🤖 Sports Betting Arbitrage Bot{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}================================{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    
    # Check if API key is configured
    if config.API_KEY == 'YOUR_API_KEY_HERE' or not config.API_KEY:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Please configure your API key in config.py or .env file{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print("You can get an API key from: https://the-odds-api.com/")
        return
    
    # Initialize the arbitrage finder
    finder = ArbitrageFinder(config.API_KEY)
    
    # Display configuration
    print(f"\n{Fore.BLUE if COLORS_AVAILABLE else ''}⚙️  Configuration:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    print(f"Sport: {config.AVAILABLE_SPORTS.get(config.SPORT, config.SPORT)}")
    print(f"Regions: {', '.join([config.AVAILABLE_REGIONS.get(r, r) for r in config.REGIONS])}")
    print(f"Markets: {', '.join([config.AVAILABLE_MARKETS.get(m, m) for m in config.MARKETS])}")
    print(f"Bet Size: ${config.BET_SIZE}")
    print(f"Min Profit Margin: {config.MIN_PROFIT_MARGIN}%")
    
    try:
        # Find arbitrage opportunities
        opportunities = finder.find_arbitrage_opportunities(
            config.SPORT,
            config.REGIONS,
            config.MARKETS,
            config.BET_SIZE
        )
        
        # Display results
        finder.display_opportunities(opportunities)
        
        # Display API usage information
        if finder.client.requests_remaining:
            print(f"\n{Fore.BLUE if COLORS_AVAILABLE else ''}📊 API Usage: {finder.client.requests_remaining} requests remaining{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW if COLORS_AVAILABLE else ''}⏹️  Bot stopped by user{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    except Exception as e:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ An error occurred: {e}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")


if __name__ == "__main__":
    main()
