"""
DFS Player Props Analyzer for Sports Betting
==========================================

This module analyzes player props for Daily Fantasy Sports (DFS) optimization.
It identifies value opportunities by comparing player prop odds with projected
performance and DFS pricing.

Author: GitHub Copilot
Date: June 2025
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np
import pandas as pd

# Import configuration and existing components
import config
from arbitrage_bot import OddsAPIClient

try:
    from colorama import init, Fore, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False


@dataclass
class PlayerProp:
    """Data class representing a player prop bet"""
    player_name: str
    team: str
    opponent: str
    sport: str
    market: str  # e.g., 'player_points', 'player_rebounds', 'player_assists'
    line: float  # The betting line (e.g., 25.5 points)
    over_odds: float
    under_odds: float
    bookmaker: str
    game_time: str
    
    
@dataclass
class DFSPlayerValue:
    """Data class representing DFS player value analysis"""
    player_name: str
    team: str
    opponent: str
    sport: str
    position: str
    salary: int  # DFS salary (simulated)
    projected_points: float  # Projected DFS points
    prop_analysis: Dict[str, PlayerProp]  # Various prop bets for this player
    value_score: float  # Points per dollar ratio
    confidence_score: float  # Confidence in projections (0-100)
    recommended_exposure: float  # Recommended exposure percentage (0-100)


class DFSPlayerPropsAnalyzer:
    """Analyzer for DFS player props and value opportunities"""
    
    def __init__(self, api_key: str):
        self.client = OddsAPIClient(api_key)
        
        # DFS scoring systems (NBA example)
        self.dfs_scoring = {
            'basketball_nba': {
                'points': 1.0,
                'rebounds': 1.2,
                'assists': 1.5,
                'steals': 3.0,
                'blocks': 3.0,
                'turnovers': -1.0,
                'three_pointers': 0.5
            },
            'americanfootball_nfl': {
                'passing_yards': 0.04,
                'passing_tds': 4.0,
                'rushing_yards': 0.1,
                'rushing_tds': 6.0,
                'receiving_yards': 0.1,
                'receiving_tds': 6.0,
                'receptions': 1.0,
                'interceptions': -1.0,
                'fumbles': -1.0
            }
        }
        
        # Simulated DFS salaries (in real implementation, these would come from DFS sites)
        self.player_salaries = {}
        
    def get_player_props(self, sport: str, regions: List[str]) -> List[PlayerProp]:
        """
        Fetch player prop odds for a specific sport
        
        Args:
            sport: Sport key
            regions: List of regions to check
            
        Returns:
            List of player prop bets
        """
        print(f"{Fore.BLUE if COLORS_AVAILABLE else ''}🔍 Fetching player props for {config.AVAILABLE_SPORTS.get(sport, sport)}...{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        # Get player props markets
        player_markets = [
            'player_points', 'player_rebounds', 'player_assists',
            'player_threes', 'player_blocks', 'player_steals',
            'player_turnovers', 'player_points_rebounds_assists'
        ]
        
        events_data = self.client.get_odds(sport, regions, player_markets)
        
        if not events_data:
            print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Failed to fetch player props data{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return []
        
        player_props = []
        
        for event in events_data:
            if not event.get('bookmakers'):
                continue
                
            home_team = event['home_team']
            away_team = event['away_team']
            game_time = event['commence_time']
            
            for bookmaker in event['bookmakers']:
                bookmaker_name = bookmaker['title']
                
                for market in bookmaker.get('markets', []):
                    market_key = market['key']
                    
                    if not market_key.startswith('player_'):
                        continue
                    
                    for outcome in market.get('outcomes', []):
                        # Parse player name from outcome
                        if 'name' in outcome and 'point' in outcome.get('name', '').lower():
                            player_name = self._extract_player_name(outcome['name'])
                            
                            # Determine which team the player is on (simplified)
                            team = home_team if len(player_name) > 0 else away_team
                            opponent = away_team if team == home_team else home_team
                            
                            # Get over/under odds
                            over_odds = None
                            under_odds = None
                            line = outcome.get('point', 0)
                            
                            if outcome['name'].lower().startswith('over'):
                                over_odds = float(outcome['price'])
                            else:
                                under_odds = float(outcome['price'])
                            
                            # Create player prop
                            prop = PlayerProp(
                                player_name=player_name,
                                team=team,
                                opponent=opponent,
                                sport=sport,
                                market=market_key,
                                line=line,
                                over_odds=over_odds or 2.0,
                                under_odds=under_odds or 2.0,
                                bookmaker=bookmaker_name,
                                game_time=game_time
                            )
                            
                            player_props.append(prop)
        
        return player_props
    
    def _extract_player_name(self, outcome_name: str) -> str:
        """Extract player name from outcome string"""
        # This is a simplified extraction - in real implementation,
        # you'd need more sophisticated parsing
        parts = outcome_name.split()
        if len(parts) >= 2:
            return f"{parts[0]} {parts[1]}"
        return outcome_name
    
    def _simulate_player_salary(self, player_name: str, sport: str) -> int:
        """Simulate DFS salary for a player"""
        # In real implementation, this would fetch from DFS sites
        base_salary = {
            'basketball_nba': 8000,
            'americanfootball_nfl': 7000
        }.get(sport, 6000)
        
        # Add some variance based on player name hash
        variance = hash(player_name) % 3000
        return base_salary + variance
    
    def _calculate_projected_points(self, player_props: List[PlayerProp]) -> float:
        """
        Calculate projected DFS points based on player props
        
        Args:
            player_props: List of props for a player
            
        Returns:
            Projected DFS points
        """
        if not player_props:
            return 0.0
            
        sport = player_props[0].sport
        scoring = self.dfs_scoring.get(sport, {})
        
        projected_points = 0.0
        
        for prop in player_props:
            # Convert prop line to expected value
            if prop.market == 'player_points':
                expected_value = prop.line
                points_multiplier = scoring.get('points', 1.0)
            elif prop.market == 'player_rebounds':
                expected_value = prop.line
                points_multiplier = scoring.get('rebounds', 1.2)
            elif prop.market == 'player_assists':
                expected_value = prop.line
                points_multiplier = scoring.get('assists', 1.5)
            elif prop.market == 'player_threes':
                expected_value = prop.line
                points_multiplier = scoring.get('three_pointers', 0.5)
            else:
                continue
                
            projected_points += expected_value * points_multiplier
        
        return projected_points
    
    def analyze_dfs_value(self, sport: str, regions: List[str]) -> List[DFSPlayerValue]:
        """
        Analyze DFS value opportunities for players
        
        Args:
            sport: Sport key
            regions: List of regions to check
            
        Returns:
            List of DFS player value analyses
        """
        player_props = self.get_player_props(sport, regions)
        
        if not player_props:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}⚠️  No player props found for {sport}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return []
        
        print(f"{Fore.GREEN if COLORS_AVAILABLE else ''}✅ Found {len(player_props)} player props{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        # Group props by player
        players_props = {}
        for prop in player_props:
            player_key = f"{prop.player_name}_{prop.team}"
            if player_key not in players_props:
                players_props[player_key] = []
            players_props[player_key].append(prop)
        
        dfs_values = []
        
        for player_key, props in players_props.items():
            if not props:
                continue
                
            player_name = props[0].player_name
            team = props[0].team
            opponent = props[0].opponent
            sport = props[0].sport
            
            # Calculate metrics
            salary = self._simulate_player_salary(player_name, sport)
            projected_points = self._calculate_projected_points(props)
            value_score = projected_points / (salary / 1000) if salary > 0 else 0
            
            # Calculate confidence score based on prop consistency
            confidence_score = self._calculate_confidence_score(props)
            
            # Calculate recommended exposure
            recommended_exposure = min(100, max(0, (value_score - 2.5) * 20))
            
            # Group props by market
            prop_analysis = {}
            for prop in props:
                prop_analysis[prop.market] = prop
            
            dfs_value = DFSPlayerValue(
                player_name=player_name,
                team=team,
                opponent=opponent,
                sport=sport,
                position=self._get_player_position(player_name, sport),
                salary=salary,
                projected_points=projected_points,
                prop_analysis=prop_analysis,
                value_score=value_score,
                confidence_score=confidence_score,
                recommended_exposure=recommended_exposure
            )
            
            dfs_values.append(dfs_value)
        
        # Sort by value score
        dfs_values.sort(key=lambda x: x.value_score, reverse=True)
        
        return dfs_values
    
    def _calculate_confidence_score(self, props: List[PlayerProp]) -> float:
        """Calculate confidence score based on prop consistency"""
        if len(props) < 2:
            return 50.0
        
        # Simple confidence calculation based on number of props
        base_confidence = min(90, 30 + len(props) * 15)
        return base_confidence
    
    def _get_player_position(self, player_name: str, sport: str) -> str:
        """Get player position (simplified)"""
        # In real implementation, this would come from a player database
        positions = {
            'basketball_nba': ['PG', 'SG', 'SF', 'PF', 'C'],
            'americanfootball_nfl': ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
        }
        
        sport_positions = positions.get(sport, ['FLEX'])
        return sport_positions[hash(player_name) % len(sport_positions)]
    
    def find_prop_arbitrage(self, player_props: List[PlayerProp]) -> List[Dict]:
        """
        Find arbitrage opportunities in player props
        
        Args:
            player_props: List of player props
            
        Returns:
            List of arbitrage opportunities
        """
        arbitrage_opportunities = []
        
        # Group props by player and market
        prop_groups = {}
        for prop in player_props:
            key = f"{prop.player_name}_{prop.market}"
            if key not in prop_groups:
                prop_groups[key] = []
            prop_groups[key].append(prop)
        
        for key, props in prop_groups.items():
            if len(props) < 2:
                continue
            
            # Find best over and under odds
            best_over = max(props, key=lambda x: x.over_odds)
            best_under = max(props, key=lambda x: x.under_odds)
            
            # Calculate arbitrage
            arbitrage_pct = (1 / best_over.over_odds) + (1 / best_under.under_odds)
            
            if arbitrage_pct < 1.0:
                profit_margin = (1 - arbitrage_pct) * 100
                
                opportunity = {
                    'player_name': best_over.player_name,
                    'market': best_over.market,
                    'line': best_over.line,
                    'over_odds': best_over.over_odds,
                    'over_bookmaker': best_over.bookmaker,
                    'under_odds': best_under.under_odds,
                    'under_bookmaker': best_under.bookmaker,
                    'arbitrage_percentage': arbitrage_pct,
                    'profit_margin': profit_margin
                }
                
                arbitrage_opportunities.append(opportunity)
        
        return arbitrage_opportunities
    
    def display_dfs_analysis(self, dfs_values: List[DFSPlayerValue], top_n: int = 10):
        """
        Display DFS value analysis results
        
        Args:
            dfs_values: List of DFS player values
            top_n: Number of top players to display
        """
        if not dfs_values:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}📊 No DFS value analysis available.{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return
        
        print(f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}💎 TOP DFS VALUE PLAYERS{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print("=" * 80)
        
        for i, player in enumerate(dfs_values[:top_n], 1):
            print(f"\n{Fore.CYAN if COLORS_AVAILABLE else ''}🏀 PLAYER #{i}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            print(f"Name: {player.player_name} ({player.position})")
            print(f"Team: {player.team} vs {player.opponent}")
            print(f"Salary: ${player.salary:,}")
            print(f"Projected Points: {player.projected_points:.2f}")
            print(f"Value Score: {player.value_score:.2f} (pts per $1K)")
            print(f"Confidence: {player.confidence_score:.0f}%")
            print(f"Recommended Exposure: {player.recommended_exposure:.0f}%")
            
            if player.prop_analysis:
                print(f"\n{Fore.YELLOW if COLORS_AVAILABLE else ''}📈 Player Props:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
                for market, prop in player.prop_analysis.items():
                    market_display = market.replace('player_', '').replace('_', ' ').title()
                    print(f"  • {market_display}: {prop.line} (O/U: {prop.over_odds:.2f}/{prop.under_odds:.2f})")
            
            print("-" * 80)
    
    def display_prop_arbitrage(self, arbitrage_opportunities: List[Dict]):
        """
        Display player prop arbitrage opportunities
        
        Args:
            arbitrage_opportunities: List of arbitrage opportunities
        """
        if not arbitrage_opportunities:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}📊 No player prop arbitrage opportunities found.{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return
        
        print(f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}🎯 PLAYER PROP ARBITRAGE OPPORTUNITIES: {len(arbitrage_opportunities)}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print("=" * 80)
        
        for i, opp in enumerate(arbitrage_opportunities, 1):
            print(f"\n{Fore.CYAN if COLORS_AVAILABLE else ''}📋 PROP ARBITRAGE #{i}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            print(f"Player: {opp['player_name']}")
            print(f"Market: {opp['market'].replace('player_', '').replace('_', ' ').title()}")
            print(f"Line: {opp['line']}")
            print(f"Profit Margin: {opp['profit_margin']:.2f}%")
            
            print(f"\n{Fore.YELLOW if COLORS_AVAILABLE else ''}💰 BETTING STRATEGY:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            print(f"  • Bet OVER {opp['line']} at odds {opp['over_odds']:.2f} with {opp['over_bookmaker']}")
            print(f"  • Bet UNDER {opp['line']} at odds {opp['under_odds']:.2f} with {opp['under_bookmaker']}")
            
            print("-" * 80)


def main():
    """Main function for DFS player props analysis"""
    print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}💎 DFS Player Props Analyzer{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}============================={Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    
    # Check if API key is configured
    if config.API_KEY == 'YOUR_API_KEY_HERE' or not config.API_KEY:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Please configure your API key in config.py or .env file{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        return
    
    # Initialize analyzer
    analyzer = DFSPlayerPropsAnalyzer(config.API_KEY)
    
    # Analyze NBA by default (most common for DFS)
    sport = 'basketball_nba'
    regions = ['us']
    
    print(f"\n{Fore.BLUE if COLORS_AVAILABLE else ''}⚙️  Configuration:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    print(f"Sport: {config.AVAILABLE_SPORTS.get(sport, sport)}")
    print(f"Regions: {', '.join(regions)}")
    print(f"Analysis: DFS Value + Prop Arbitrage")
    
    try:
        # Get DFS value analysis
        dfs_values = analyzer.analyze_dfs_value(sport, regions)
        analyzer.display_dfs_analysis(dfs_values)
        
        # Get player props for arbitrage analysis
        player_props = analyzer.get_player_props(sport, regions)
        arbitrage_opportunities = analyzer.find_prop_arbitrage(player_props)
        analyzer.display_prop_arbitrage(arbitrage_opportunities)
        
        # Display API usage
        if analyzer.client.requests_remaining:
            print(f"\n{Fore.BLUE if COLORS_AVAILABLE else ''}📊 API Usage: {analyzer.client.requests_remaining} requests remaining{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW if COLORS_AVAILABLE else ''}⏹️  Analysis stopped by user{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    except Exception as e:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ An error occurred: {e}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")


if __name__ == "__main__":
    main()
