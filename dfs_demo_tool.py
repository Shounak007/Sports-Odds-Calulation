"""
DFS Demo & Analysis Tool
=======================

This tool provides DFS player props analysis with simulated data when live data
isn't available, plus real arbitrage opportunities for available markets.

Author: GitHub Copilot
Date: June 2025
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json

import config
from arbitrage_bot import OddsAPIClient

try:
    from colorama import init, Fore, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False


@dataclass
class SimulatedPlayer:
    """Simulated DFS player data"""
    name: str
    team: str
    opponent: str
    position: str
    salary: int
    projected_stats: Dict[str, float]
    projected_points: float
    value_score: float
    confidence: float
    game_time: str


class DFSAnalysisTool:
    """Comprehensive DFS analysis tool with demo capabilities"""
    
    def __init__(self, api_key: str):
        self.client = OddsAPIClient(api_key)
        
        # NBA teams for simulation
        self.nba_teams = [
            'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets',
            'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
            'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers',
            'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat',
            'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
            'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns',
            'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors',
            'Utah Jazz', 'Washington Wizards'
        ]
        
        # Sample player pool
        self.sample_players = [
            ('LeBron James', 'SF'), ('Stephen Curry', 'PG'), ('Kevin Durant', 'SF'),
            ('Giannis Antetokounmpo', 'PF'), ('Luka Doncic', 'PG'), ('Jayson Tatum', 'SF'),
            ('Joel Embiid', 'C'), ('Nikola Jokic', 'C'), ('Damian Lillard', 'PG'),
            ('Jimmy Butler', 'SF'), ('Kawhi Leonard', 'SF'), ('Paul George', 'SF'),
            ('Anthony Davis', 'PF'), ('Devin Booker', 'SG'), ('Trae Young', 'PG'),
            ('Ja Morant', 'PG'), ('Zion Williamson', 'PF'), ('Donovan Mitchell', 'SG'),
            ('Russell Westbrook', 'PG'), ('Chris Paul', 'PG'), ('Klay Thompson', 'SG'),
            ('Draymond Green', 'PF'), ('Rudy Gobert', 'C'), ('Karl-Anthony Towns', 'C')
        ]
        
        # DFS scoring system
        self.dfs_scoring = {
            'points': 1.0,
            'rebounds': 1.2,
            'assists': 1.5,
            'steals': 3.0,
            'blocks': 3.0,
            'turnovers': -1.0,
            'three_pointers': 0.5
        }
    
    def generate_simulated_slate(self, num_games: int = 6) -> List[SimulatedPlayer]:
        """Generate a simulated DFS slate with realistic player data"""
        
        print(f"{Fore.BLUE if COLORS_AVAILABLE else ''}🎮 Generating simulated NBA DFS slate with {num_games} games...{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        players = []
        used_teams = set()
        
        # Generate games
        for game_num in range(num_games):
            # Pick two teams that haven't been used
            available_teams = [t for t in self.nba_teams if t not in used_teams]
            if len(available_teams) < 2:
                break
                
            team1, team2 = random.sample(available_teams, 2)
            used_teams.add(team1)
            used_teams.add(team2)
            
            game_time = (datetime.now() + timedelta(hours=random.randint(2, 8))).strftime('%Y-%m-%d %H:%M:%S')
            
            # Generate players for each team
            for team, opponent in [(team1, team2), (team2, team1)]:
                team_players = random.sample(self.sample_players, 4)  # 4 players per team in slate
                
                for player_name, position in team_players:
                    # Generate realistic stats and pricing
                    base_salary = {
                        'PG': 8500, 'SG': 7800, 'SF': 8200, 'PF': 7900, 'C': 8000
                    }.get(position, 7500)
                    
                    # Add variance based on "star power"
                    star_multiplier = 1.0
                    if player_name in ['LeBron James', 'Stephen Curry', 'Kevin Durant', 'Giannis Antetokounmpo']:
                        star_multiplier = 1.3
                    elif player_name in ['Luka Doncic', 'Jayson Tatum', 'Joel Embiid', 'Nikola Jokic']:
                        star_multiplier = 1.2
                    
                    salary = int(base_salary * star_multiplier * random.uniform(0.8, 1.2))
                    salary = min(12000, max(4000, salary))  # Salary range
                    
                    # Generate projected stats
                    stats = self._generate_projected_stats(position, star_multiplier)
                    
                    # Calculate DFS points
                    projected_points = self._calculate_dfs_points(stats)
                    
                    # Calculate value score
                    value_score = projected_points / (salary / 1000)
                    
                    # Generate confidence (higher for stars)
                    confidence = random.uniform(60, 95) * star_multiplier * 0.9
                    confidence = min(95, confidence)
                    
                    player = SimulatedPlayer(
                        name=player_name,
                        team=team,
                        opponent=opponent,
                        position=position,
                        salary=salary,
                        projected_stats=stats,
                        projected_points=projected_points,
                        value_score=value_score,
                        confidence=confidence,
                        game_time=game_time
                    )
                    
                    players.append(player)
        
        return players
    
    def _generate_projected_stats(self, position: str, star_multiplier: float) -> Dict[str, float]:
        """Generate realistic projected stats for a position"""
        
        # Base stats by position
        base_stats = {
            'PG': {'points': 18, 'rebounds': 4, 'assists': 8, 'steals': 1.2, 'blocks': 0.3, 'turnovers': 3, 'three_pointers': 2.5},
            'SG': {'points': 20, 'rebounds': 4, 'assists': 4, 'steals': 1.0, 'blocks': 0.4, 'turnovers': 2.5, 'three_pointers': 2.8},
            'SF': {'points': 19, 'rebounds': 6, 'assists': 5, 'steals': 1.1, 'blocks': 0.8, 'turnovers': 2.8, 'three_pointers': 2.2},
            'PF': {'points': 17, 'rebounds': 8, 'assists': 3, 'steals': 0.8, 'blocks': 1.2, 'turnovers': 2.2, 'three_pointers': 1.5},
            'C': {'points': 16, 'rebounds': 10, 'assists': 2, 'steals': 0.6, 'blocks': 1.8, 'turnovers': 2.0, 'three_pointers': 0.8}
        }
        
        stats = base_stats.get(position, base_stats['SF']).copy()
        
        # Apply star multiplier and variance
        for stat in stats:
            stats[stat] *= star_multiplier * random.uniform(0.7, 1.3)
            stats[stat] = round(stats[stat], 1)
        
        return stats
    
    def _calculate_dfs_points(self, stats: Dict[str, float]) -> float:
        """Calculate DFS points from projected stats"""
        
        total_points = 0
        for stat, value in stats.items():
            multiplier = self.dfs_scoring.get(stat, 0)
            total_points += value * multiplier
        
        return round(total_points, 2)
    
    def analyze_real_arbitrage(self, sport: str = 'basketball_nba') -> List[Dict]:
        """Analyze real arbitrage opportunities from available markets"""
        
        print(f"{Fore.BLUE if COLORS_AVAILABLE else ''}🔍 Checking for real arbitrage opportunities...{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        # Try basic markets first
        basic_markets = ['h2h', 'totals', 'spreads']
        regions = ['us']
        
        events_data = self.client.get_odds(sport, regions, basic_markets)
        
        if not events_data:
            return []
        
        arbitrage_opportunities = []
        
        for event in events_data:
            if not event.get('bookmakers'):
                continue
            
            # Analyze each market
            markets_data = {}
            
            for bookmaker in event['bookmakers']:
                for market in bookmaker.get('markets', []):
                    market_key = market['key']
                    
                    if market_key not in markets_data:
                        markets_data[market_key] = {}
                    
                    for outcome in market.get('outcomes', []):
                        outcome_name = outcome['name']
                        price = float(outcome['price'])
                        
                        if outcome_name not in markets_data[market_key]:
                            markets_data[market_key][outcome_name] = {
                                'best_odds': price,
                                'bookmaker': bookmaker['title']
                            }
                        elif price > markets_data[market_key][outcome_name]['best_odds']:
                            markets_data[market_key][outcome_name] = {
                                'best_odds': price,
                                'bookmaker': bookmaker['title']
                            }
            
            # Check for arbitrage in each market
            for market_key, outcomes in markets_data.items():
                if len(outcomes) >= 2:
                    odds_list = [data['best_odds'] for data in outcomes.values()]
                    arbitrage_pct = sum(1/odd for odd in odds_list)
                    
                    if arbitrage_pct < 1.0:
                        arbitrage_opportunities.append({
                            'event': f"{event['home_team']} vs {event['away_team']}",
                            'market': market_key,
                            'arbitrage_percentage': arbitrage_pct,
                            'profit_margin': (1 - arbitrage_pct) * 100,
                            'outcomes': outcomes
                        })
        
        return arbitrage_opportunities
    
    def create_optimal_lineup(self, players: List[SimulatedPlayer], salary_cap: int = 50000) -> Dict:
        """Create an optimal DFS lineup using simulated players"""
        
        print(f"{Fore.BLUE if COLORS_AVAILABLE else ''}🧮 Creating optimal lineup (salary cap: ${salary_cap:,})...{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        # Simple greedy algorithm for lineup optimization
        # Sort by value score
        sorted_players = sorted(players, key=lambda x: x.value_score, reverse=True)
        
        # Position requirements (DraftKings format)
        position_requirements = {
            'PG': 1, 'SG': 1, 'SF': 1, 'PF': 1, 'C': 1,
            'G': 1, 'F': 1, 'UTIL': 1  # Flex positions
        }
        
        lineup = []
        total_salary = 0
        position_filled = {pos: 0 for pos in position_requirements}
        
        for player in sorted_players:
            if len(lineup) >= 8:  # Max lineup size
                break
            
            if total_salary + player.salary > salary_cap:
                continue
            
            # Check if we can add this player
            pos = player.position
            can_add = False
            
            # Direct position match
            if position_filled[pos] < position_requirements.get(pos, 0):
                position_filled[pos] += 1
                can_add = True
            # Flex guard
            elif pos in ['PG', 'SG'] and position_filled['G'] < position_requirements['G']:
                position_filled['G'] += 1
                can_add = True
            # Flex forward  
            elif pos in ['SF', 'PF'] and position_filled['F'] < position_requirements['F']:
                position_filled['F'] += 1
                can_add = True
            # Utility
            elif position_filled['UTIL'] < position_requirements['UTIL']:
                position_filled['UTIL'] += 1
                can_add = True
            
            if can_add:
                lineup.append(player)
                total_salary += player.salary
        
        if len(lineup) == 8:
            total_projected = sum(p.projected_points for p in lineup)
            avg_value = total_projected / (total_salary / 1000)
            
            return {
                'lineup': lineup,
                'total_salary': total_salary,
                'remaining_salary': salary_cap - total_salary,
                'projected_points': total_projected,
                'value_score': avg_value
            }
        
        return None
    
    def display_dfs_analysis(self, players: List[SimulatedPlayer], top_n: int = 15):
        """Display DFS analysis results"""
        
        print(f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}💎 TOP DFS VALUE PLAYERS{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print("=" * 100)
        
        # Sort by value score
        top_players = sorted(players, key=lambda x: x.value_score, reverse=True)[:top_n]
        
        for i, player in enumerate(top_players, 1):
            print(f"\n{Fore.CYAN if COLORS_AVAILABLE else ''}🏀 #{i:2d} {player.name} ({player.position}){Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            print(f"     {player.team} vs {player.opponent}")
            print(f"     Salary: ${player.salary:,}  |  Projected: {player.projected_points:.1f}pts  |  Value: {player.value_score:.2f}")
            print(f"     Confidence: {player.confidence:.0f}%")
            
            # Show key projected stats
            key_stats = ['points', 'rebounds', 'assists']
            stats_str = " | ".join([f"{stat.title()}: {player.projected_stats.get(stat, 0):.1f}" 
                                   for stat in key_stats])
            print(f"     {stats_str}")
    
    def display_optimal_lineup(self, lineup_data: Dict):
        """Display the optimal lineup"""
        
        if not lineup_data:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}⚠️  Could not create optimal lineup{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return
        
        lineup = lineup_data['lineup']
        
        print(f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}🏆 OPTIMAL DFS LINEUP{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print("=" * 80)
        print(f"Total Salary: ${lineup_data['total_salary']:,} (${lineup_data['remaining_salary']:,} remaining)")
        print(f"Projected Points: {lineup_data['projected_points']:.1f}")
        print(f"Value Score: {lineup_data['value_score']:.2f}")
        
        print(f"\n{Fore.YELLOW if COLORS_AVAILABLE else ''}👥 ROSTER:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        for i, player in enumerate(lineup, 1):
            print(f"{i}. {player.position:<3} {player.name:<20} ${player.salary:>5,} "
                  f"{player.projected_points:>5.1f}pts ({player.value_score:.2f}val)")
    
    def display_arbitrage_opportunities(self, opportunities: List[Dict]):
        """Display real arbitrage opportunities"""
        
        if not opportunities:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}📊 No arbitrage opportunities found in current markets.{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return
        
        print(f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}🎯 LIVE ARBITRAGE OPPORTUNITIES: {len(opportunities)}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print("=" * 80)
        
        for i, opp in enumerate(opportunities, 1):
            print(f"\n{Fore.CYAN if COLORS_AVAILABLE else ''}📋 OPPORTUNITY #{i}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            print(f"Event: {opp['event']}")
            print(f"Market: {opp['market'].upper()}")
            print(f"Profit Margin: {opp['profit_margin']:.2f}%")
            
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}Betting Strategy:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            for outcome_name, data in opp['outcomes'].items():
                print(f"  • {outcome_name}: {data['best_odds']:.2f} at {data['bookmaker']}")


def main():
    """Main function for DFS analysis tool"""
    
    print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}💎 DFS Analysis & Demo Tool{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}============================={Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    
    if config.API_KEY == 'YOUR_API_KEY_HERE' or not config.API_KEY:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Please configure your API key{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        return
    
    tool = DFSAnalysisTool(config.API_KEY)
    
    try:
        # Generate simulated DFS slate
        players = tool.generate_simulated_slate(num_games=5)
        
        # Display top value players
        tool.display_dfs_analysis(players)
        
        # Create optimal lineup
        optimal_lineup = tool.create_optimal_lineup(players)
        tool.display_optimal_lineup(optimal_lineup)
        
        # Check for real arbitrage opportunities
        arbitrage_opportunities = tool.analyze_real_arbitrage()
        tool.display_arbitrage_opportunities(arbitrage_opportunities)
        
        # API usage info
        if tool.client.requests_remaining:
            print(f"\n{Fore.BLUE if COLORS_AVAILABLE else ''}📊 API Usage: {tool.client.requests_remaining} requests remaining{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        print(f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}✨ Analysis complete! This demo shows DFS value analysis with simulated player data{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print(f"{Fore.GREEN if COLORS_AVAILABLE else ''}   plus real arbitrage opportunities from live betting markets.{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
    except Exception as e:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Error: {e}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")


if __name__ == "__main__":
    main()
