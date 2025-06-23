"""
DFS Lineup Optimizer
===================

This module creates optimal DFS lineups based on player props analysis
and value calculations.

Author: GitHub Copilot  
Date: June 2025
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
import itertools
from dfs_props_analyzer import DFSPlayerValue

try:
    from colorama import init, Fore, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False


@dataclass 
class DFSLineup:
    """Represents a DFS lineup"""
    players: List[DFSPlayerValue]
    total_salary: int
    projected_points: float
    value_score: float
    risk_score: float
    lineup_type: str  # 'cash', 'gpp', 'balanced'


class DFSLineupOptimizer:
    """Optimizer for creating DFS lineups"""
    
    def __init__(self):
        # Salary caps and roster requirements by sport
        self.roster_requirements = {
            'basketball_nba': {
                'salary_cap': 50000,
                'positions': {
                    'PG': 1,
                    'SG': 1, 
                    'SF': 1,
                    'PF': 1,
                    'C': 1,
                    'G': 1,  # Guard (PG/SG)
                    'F': 1,  # Forward (SF/PF)
                    'UTIL': 1  # Utility (any position)
                },
                'total_players': 8
            },
            'americanfootball_nfl': {
                'salary_cap': 50000,
                'positions': {
                    'QB': 1,
                    'RB': 2,
                    'WR': 3,
                    'TE': 1,
                    'K': 1,
                    'DEF': 1
                },
                'total_players': 9
            }
        }
    
    def optimize_lineups(self, players: List[DFSPlayerValue], sport: str, 
                        lineup_count: int = 5) -> List[DFSLineup]:
        """
        Generate optimal DFS lineups
        
        Args:
            players: List of player values
            sport: Sport key
            lineup_count: Number of lineups to generate
            
        Returns:
            List of optimized lineups
        """
        if sport not in self.roster_requirements:
            print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Sport {sport} not supported for lineup optimization{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return []
        
        requirements = self.roster_requirements[sport]
        salary_cap = requirements['salary_cap']
        
        print(f"{Fore.BLUE if COLORS_AVAILABLE else ''}🔧 Optimizing {lineup_count} lineups for {sport}...{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print(f"Salary Cap: ${salary_cap:,}")
        
        # Filter players by minimum value threshold
        viable_players = [p for p in players if p.value_score >= 2.0]
        
        if len(viable_players) < requirements['total_players']:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}⚠️  Not enough viable players for lineup optimization{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return []
        
        lineups = []
        
        # Generate different lineup types
        lineup_types = [
            ('cash', 0.8, 0.2),    # 80% value, 20% ceiling
            ('gpp', 0.5, 0.5),     # 50% value, 50% ceiling
            ('balanced', 0.65, 0.35) # 65% value, 35% ceiling
        ]
        
        for lineup_type, value_weight, ceiling_weight in lineup_types:
            for i in range(lineup_count // len(lineup_types) + 1):
                lineup = self._generate_lineup(
                    viable_players, requirements, salary_cap,
                    lineup_type, value_weight, ceiling_weight
                )
                
                if lineup and not self._is_duplicate_lineup(lineup, lineups):
                    lineups.append(lineup)
                    
                if len(lineups) >= lineup_count:
                    break
            
            if len(lineups) >= lineup_count:
                break
        
        # Sort by projected points
        lineups.sort(key=lambda x: x.projected_points, reverse=True)
        
        return lineups[:lineup_count]
    
    def _generate_lineup(self, players: List[DFSPlayerValue], requirements: Dict,
                        salary_cap: int, lineup_type: str, value_weight: float,
                        ceiling_weight: float) -> DFSLineup:
        """Generate a single lineup using greedy optimization"""
        
        # Score players based on lineup type  
        scored_players = []
        for player in players:
            value_score = player.value_score
            ceiling_score = player.projected_points / 10  # Normalize ceiling
            
            composite_score = (value_weight * value_score + 
                             ceiling_weight * ceiling_score)
            
            scored_players.append((composite_score, player))
        
        # Sort by composite score
        scored_players.sort(key=lambda x: x[0], reverse=True)
        
        # Greedy selection with position constraints
        selected_players = []
        total_salary = 0
        position_counts = {pos: 0 for pos in requirements['positions']}
        
        for score, player in scored_players:
            if len(selected_players) >= requirements['total_players']:
                break
                
            if total_salary + player.salary > salary_cap:
                continue
            
            # Check position requirements
            player_pos = player.position
            can_add = False
            
            # Check if player can fill required position
            for pos, required_count in requirements['positions'].items():
                if position_counts[pos] < required_count:
                    if (pos == player_pos or 
                        (pos == 'G' and player_pos in ['PG', 'SG']) or
                        (pos == 'F' and player_pos in ['SF', 'PF']) or
                        pos == 'UTIL'):
                        position_counts[pos] += 1
                        can_add = True
                        break
            
            if can_add:
                selected_players.append(player)
                total_salary += player.salary
        
        if len(selected_players) == requirements['total_players']:
            projected_points = sum(p.projected_points for p in selected_players)
            value_score = projected_points / (total_salary / 1000)
            risk_score = self._calculate_risk_score(selected_players)
            
            return DFSLineup(
                players=selected_players,
                total_salary=total_salary,
                projected_points=projected_points,
                value_score=value_score,
                risk_score=risk_score,
                lineup_type=lineup_type
            )
        
        return None
    
    def _calculate_risk_score(self, players: List[DFSPlayerValue]) -> float:
        """Calculate risk score for a lineup (0-100, lower is safer)"""
        if not players:
            return 50.0
        
        # Base risk on confidence scores
        avg_confidence = sum(p.confidence_score for p in players) / len(players)
        risk_score = 100 - avg_confidence
        
        return max(0, min(100, risk_score))
    
    def _is_duplicate_lineup(self, new_lineup: DFSLineup, existing_lineups: List[DFSLineup]) -> bool:
        """Check if lineup is a duplicate"""
        if not existing_lineups:
            return False
        
        new_player_names = set(p.player_name for p in new_lineup.players)
        
        for existing in existing_lineups:
            existing_player_names = set(p.player_name for p in existing.players)
            
            # Consider duplicate if 75% or more players are the same
            overlap = len(new_player_names & existing_player_names)
            if overlap >= len(new_player_names) * 0.75:
                return True
        
        return False
    
    def display_lineups(self, lineups: List[DFSLineup]):
        """Display optimized lineups"""
        if not lineups:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}📊 No optimized lineups generated.{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return
        
        print(f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}🏆 OPTIMIZED DFS LINEUPS: {len(lineups)}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print("=" * 100)
        
        for i, lineup in enumerate(lineups, 1):
            print(f"\n{Fore.CYAN if COLORS_AVAILABLE else ''}💼 LINEUP #{i} - {lineup.lineup_type.upper()}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            print(f"Total Salary: ${lineup.total_salary:,} / ${50000:,}")
            print(f"Projected Points: {lineup.projected_points:.2f}")
            print(f"Value Score: {lineup.value_score:.2f}")
            print(f"Risk Score: {lineup.risk_score:.0f}/100 (lower is safer)")
            
            print(f"\n{Fore.YELLOW if COLORS_AVAILABLE else ''}👥 ROSTER:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            
            # Sort players by position for display
            sorted_players = sorted(lineup.players, key=lambda x: x.position)
            
            for player in sorted_players:
                print(f"  {player.position:<4} {player.player_name:<20} ${player.salary:>5,} "
                      f"{player.projected_points:>5.1f}pts {player.value_score:>4.2f}val")
            
            print("-" * 100)
    
    def export_lineup_csv(self, lineups: List[DFSLineup], filename: str = 'dfs_lineups.csv'):
        """Export lineups to CSV format for DFS sites"""
        try:
            import csv
            
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Header row (DraftKings format)
                writer.writerow(['PG', 'SG', 'SF', 'PF', 'C', 'G', 'F', 'UTIL'])
                
                for lineup in lineups:
                    # Map players to positions (simplified)
                    position_map = {'PG': '', 'SG': '', 'SF': '', 'PF': '', 'C': '', 'G': '', 'F': '', 'UTIL': ''}
                    
                    for player in lineup.players:
                        if not position_map[player.position]:
                            position_map[player.position] = player.player_name
                        elif player.position in ['PG', 'SG'] and not position_map['G']:
                            position_map['G'] = player.player_name
                        elif player.position in ['SF', 'PF'] and not position_map['F']:
                            position_map['F'] = player.player_name
                        elif not position_map['UTIL']:
                            position_map['UTIL'] = player.player_name
                    
                    writer.writerow(list(position_map.values()))
            
            print(f"{Fore.GREEN if COLORS_AVAILABLE else ''}✅ Lineups exported to {filename}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            
        except Exception as e:
            print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Failed to export lineups: {e}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")


def main():
    """Main function for lineup optimization"""
    from dfs_props_analyzer import DFSPlayerPropsAnalyzer
    import config
    
    print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}🏆 DFS Lineup Optimizer{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}====================={Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    
    if config.API_KEY == 'YOUR_API_KEY_HERE' or not config.API_KEY:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Please configure your API key{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        return
    
    # Get player analysis
    analyzer = DFSPlayerPropsAnalyzer(config.API_KEY)
    sport = 'basketball_nba'
    regions = ['us']
    
    try:
        print(f"{Fore.BLUE if COLORS_AVAILABLE else ''}🔍 Getting player analysis...{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        dfs_values = analyzer.analyze_dfs_value(sport, regions)
        
        if not dfs_values:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}⚠️  No player data available for optimization{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return
        
        # Optimize lineups
        optimizer = DFSLineupOptimizer()
        lineups = optimizer.optimize_lineups(dfs_values, sport, lineup_count=3)
        
        # Display results
        optimizer.display_lineups(lineups)
        
        # Export option
        if lineups:
            export_choice = input(f"\n{Fore.CYAN if COLORS_AVAILABLE else ''}Export lineups to CSV? (y/n): {Style.RESET_ALL if COLORS_AVAILABLE else ''}").lower()
            if export_choice == 'y':
                optimizer.export_lineup_csv(lineups)
        
    except Exception as e:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Error: {e}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")


if __name__ == "__main__":
    main()
