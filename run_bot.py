#!/usr/bin/env python3
"""
Simple CLI Runner for the Sports Betting Arbitrage Bot
=====================================================

This script provides an easy way to run the arbitrage bot with
different configurations.

Author: GitHub Copilot
Date: June 2025
"""

import sys
import argparse
from typing import List, Optional

# Import configuration and main components
import config
from arbitrage_bot import main as run_arbitrage_bot
from dfs_demo_tool import main as run_dfs_analyzer

def display_available_options():
    """Display available sports, regions, and markets"""
    print("\n📋 AVAILABLE OPTIONS:")
    print("=" * 40)
    
    print("\n🏈 Sports:")
    for key, name in config.AVAILABLE_SPORTS.items():
        print(f"  {key:<30} - {name}")
    
    print("\n🌍 Regions:")
    for key, name in config.AVAILABLE_REGIONS.items():
        print(f"  {key:<10} - {name}")
    
    print("\n📊 Markets:")
    for key, name in config.AVAILABLE_MARKETS.items():
        print(f"  {key:<20} - {name}")


def update_config(sport: Optional[str] = None, regions: Optional[List[str]] = None, 
                 markets: Optional[List[str]] = None, bet_size: Optional[float] = None,
                 min_profit: Optional[float] = None):
    """
    Update configuration values
    
    Args:
        sport: Sport key to analyze
        regions: List of regions
        markets: List of markets
        bet_size: Total bet size
        min_profit: Minimum profit margin
    """
    if sport:
        config.SPORT = sport
    if regions:
        config.REGIONS = regions
    if markets:
        config.MARKETS = markets
    if bet_size:
        config.BET_SIZE = bet_size
    if min_profit:
        config.MIN_PROFIT_MARGIN = min_profit


def run_wnba_analyzer():
    """Run the real-time WNBA betting analyzer"""
    try:
        from real_wnba_analyzer import main as wnba_main
        wnba_main()
    except ImportError as e:
        print(f"❌ Could not import WNBA analyzer: {e}")
    except Exception as e:
        print(f"❌ Error running WNBA analyzer: {e}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Sports Betting Arbitrage Bot CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run arbitrage bot with default settings
  python run_bot.py
  
  # Run DFS player props analyzer
  python run_bot.py --mode dfs
  
  # Run real-time WNBA betting analyzer
  python run_bot.py --mode wnba
  
  # Run with custom sport and bet size
  python run_bot.py --sport basketball_nba --bet-size 200
  
  # Run with multiple regions and markets
  python run_bot.py --regions us uk eu --markets h2h totals
  
  # Show available options
  python run_bot.py --list-options
        """
    )
    
    parser.add_argument('--mode', type=str, choices=['arbitrage', 'dfs', 'wnba'], default='arbitrage',
                       help='Analysis mode: arbitrage betting, DFS player props, or WNBA real-time analysis (default: arbitrage)')
    parser.add_argument('--sport', type=str, 
                       help='Sport to analyze (default: {})'.format(config.SPORT))
    parser.add_argument('--regions', nargs='+', 
                       help='Regions to check (default: {})'.format(config.REGIONS))
    parser.add_argument('--markets', nargs='+',
                       help='Markets to analyze (default: {})'.format(config.MARKETS))
    parser.add_argument('--bet-size', type=float,
                       help='Total bet size (default: {})'.format(config.BET_SIZE))
    parser.add_argument('--min-profit', type=float,
                       help='Minimum profit margin percentage (default: {})'.format(config.MIN_PROFIT_MARGIN))
    parser.add_argument('--list-options', action='store_true',
                       help='Show available sports, regions, and markets')
    
    args = parser.parse_args()
    
    if args.list_options:
        display_available_options()
        return
    
    # Validate sport
    if args.sport and args.sport not in config.AVAILABLE_SPORTS:
        print(f"❌ Invalid sport: {args.sport}")
        print("Available sports:")
        for key, name in config.AVAILABLE_SPORTS.items():
            print(f"  {key} - {name}")
        return
    
    # Validate regions
    if args.regions:
        invalid_regions = [r for r in args.regions if r not in config.AVAILABLE_REGIONS]
        if invalid_regions:
            print(f"❌ Invalid regions: {', '.join(invalid_regions)}")
            print("Available regions:")
            for key, name in config.AVAILABLE_REGIONS.items():
                print(f"  {key} - {name}")
            return
    
    # Validate markets
    if args.markets:
        invalid_markets = [m for m in args.markets if m not in config.AVAILABLE_MARKETS]
        if invalid_markets:
            print(f"❌ Invalid markets: {', '.join(invalid_markets)}")
            print("Available markets:")
            for key, name in config.AVAILABLE_MARKETS.items():
                print(f"  {key} - {name}")
            return
    
    # Update configuration with command line arguments
    update_config(
        sport=args.sport,
        regions=args.regions,
        markets=args.markets,
        bet_size=args.bet_size,
        min_profit=args.min_profit
    )
    
    # Run the appropriate analyzer
    if args.mode == 'dfs':
        print("🚀 Running DFS Player Props Analyzer...")
        run_dfs_analyzer()
    elif args.mode == 'wnba':
        print("🚀 Running Real-Time WNBA Betting Analyzer...")
        run_wnba_analyzer()
    else:
        print("🚀 Running Arbitrage Bot...")
        run_arbitrage_bot()


if __name__ == "__main__":
    main()
