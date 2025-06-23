"""
Historical Backtesting Script for Sports Betting Arbitrage
========================================================

This script uses The Odds API historical endpoint to analyze past
arbitrage opportunities for backtesting strategies.

Note: Historical endpoints have higher usage costs!

Author: GitHub Copilot
Date: June 2025
"""

import sys
import argparse
from datetime import datetime, timedelta
from typing import List, Dict

# Import the main arbitrage finder components
from arbitrage_bot import ArbitrageFinder, ArbitrageOpportunity
import config

try:
    from colorama import init, Fore, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False


class HistoricalArbitrageFinder(ArbitrageFinder):
    """Extended arbitrage finder for historical data analysis"""
    
    def find_historical_opportunities(self, sport: str, regions: List[str], 
                                    markets: List[str], bet_size: float, 
                                    date: str) -> List[ArbitrageOpportunity]:
        """
        Find arbitrage opportunities for a specific historical date
        
        Args:
            sport: Sport key
            regions: List of regions to check
            markets: List of markets to analyze
            bet_size: Total amount to bet
            date: Date in ISO format (YYYY-MM-DDTHH:MM:SSZ)
            
        Returns:
            List of arbitrage opportunities
        """
        print(f"{Fore.BLUE if COLORS_AVAILABLE else ''}🔍 Fetching historical odds data for {config.AVAILABLE_SPORTS.get(sport, sport)} on {date}...{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}⚠️  Note: Historical endpoints consume more API requests!{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        events_data = self.client.get_historical_odds(sport, regions, markets, date)
        
        if not events_data:
            print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Failed to fetch historical odds data{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return []
            
        if not events_data:
            print(f"{Fore.YELLOW if COLORS_AVAILABLE else ''}⚠️  No historical events found for {sport} on {date}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            return []
            
        print(f"{Fore.GREEN if COLORS_AVAILABLE else ''}✅ Found {len(events_data)} historical events{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        opportunities = []
        
        for event in events_data:
            event_opportunities = self._analyze_event(event, bet_size)
            opportunities.extend(event_opportunities)
            
        return opportunities
    
    def backtest_date_range(self, sport: str, regions: List[str], markets: List[str], 
                           bet_size: float, start_date: str, end_date: str, 
                           interval_hours: int = 24) -> Dict:
        """
        Backtest arbitrage opportunities over a date range
        
        Args:
            sport: Sport key
            regions: List of regions to check
            markets: List of markets to analyze
            bet_size: Total amount to bet
            start_date: Start date in ISO format
            end_date: End date in ISO format
            interval_hours: Hours between each check
            
        Returns:
            Dictionary with backtesting results
        """
        print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}📈 Starting backtesting from {start_date} to {end_date}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}⚠️  WARNING: This will consume many API requests!{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        results = {
            'total_opportunities': 0,
            'total_profit': 0.0,
            'dates_checked': 0,
            'dates_with_opportunities': 0,
            'best_opportunity': None,
            'daily_results': []
        }
        
        current_dt = start_dt
        
        while current_dt <= end_dt:
            date_str = current_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            
            try:
                opportunities = self.find_historical_opportunities(
                    sport, regions, markets, bet_size, date_str
                )
                
                daily_profit = sum(opp.guaranteed_profit for opp in opportunities)
                
                daily_result = {
                    'date': date_str,
                    'opportunities_count': len(opportunities),
                    'total_profit': daily_profit,
                    'opportunities': opportunities
                }
                
                results['daily_results'].append(daily_result)
                results['total_opportunities'] += len(opportunities)
                results['total_profit'] += daily_profit
                results['dates_checked'] += 1
                
                if opportunities:
                    results['dates_with_opportunities'] += 1
                    
                    # Track best opportunity
                    best_daily = max(opportunities, key=lambda x: x.profit_margin)
                    if (results['best_opportunity'] is None or 
                        best_daily.profit_margin > results['best_opportunity'].profit_margin):
                        results['best_opportunity'] = best_daily
                
                print(f"{Fore.CYAN if COLORS_AVAILABLE else ''}📅 {date_str}: {len(opportunities)} opportunities, ${daily_profit:.2f} profit{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
                
            except Exception as e:
                print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Error processing {date_str}: {e}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            
            current_dt += timedelta(hours=interval_hours)
            
        return results
    
    def display_backtest_summary(self, results: Dict):
        """
        Display summary of backtesting results
        
        Args:
            results: Backtesting results dictionary
        """
        print(f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}📊 BACKTESTING SUMMARY{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print("=" * 50)
        print(f"Dates Checked: {results['dates_checked']}")
        print(f"Dates with Opportunities: {results['dates_with_opportunities']}")
        print(f"Total Opportunities Found: {results['total_opportunities']}")
        print(f"Total Potential Profit: ${results['total_profit']:.2f}")
        
        if results['dates_checked'] > 0:
            avg_opportunities = results['total_opportunities'] / results['dates_checked']
            avg_profit = results['total_profit'] / results['dates_checked']
            success_rate = (results['dates_with_opportunities'] / results['dates_checked']) * 100
            
            print(f"Average Opportunities per Day: {avg_opportunities:.2f}")
            print(f"Average Profit per Day: ${avg_profit:.2f}")
            print(f"Success Rate: {success_rate:.1f}%")
        
        if results['best_opportunity']:
            best = results['best_opportunity']
            print(f"\n{Fore.YELLOW if COLORS_AVAILABLE else ''}🏆 BEST OPPORTUNITY:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            print(f"Event: {best.home_team} vs {best.away_team}")
            print(f"Profit Margin: {best.profit_margin:.2f}%")
            print(f"Guaranteed Profit: ${best.guaranteed_profit:.2f}")


def parse_date(date_string: str) -> str:
    """
    Parse and validate date string
    
    Args:
        date_string: Date in various formats
        
    Returns:
        ISO formatted date string
    """
    try:
        # Try parsing different date formats
        formats = [
            '%Y-%m-%d',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S'
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_string, fmt)
                return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                continue
                
        raise ValueError("Invalid date format")
        
    except ValueError:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Invalid date format: {date_string}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        print("Supported formats:")
        print("- YYYY-MM-DD")
        print("- YYYY-MM-DDTHH:MM:SS")
        print("- YYYY-MM-DDTHH:MM:SSZ")
        print("- YYYY-MM-DD HH:MM:SS")
        sys.exit(1)


def main():
    """Main function for historical backtesting"""
    parser = argparse.ArgumentParser(
        description="Backtest arbitrage opportunities using historical data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single date analysis
  python backtest_strategy.py --date "2024-01-15"
  
  # Date range analysis
  python backtest_strategy.py --start-date "2024-01-01" --end-date "2024-01-07"
  
  # Custom sport and bet size
  python backtest_strategy.py --date "2024-01-15" --sport basketball_nba --bet-size 200
        """
    )
    
    parser.add_argument('--date', type=str, help='Single date to analyze (YYYY-MM-DD format)')
    parser.add_argument('--start-date', type=str, help='Start date for range analysis')
    parser.add_argument('--end-date', type=str, help='End date for range analysis')
    parser.add_argument('--sport', type=str, default=config.SPORT, 
                       help=f'Sport to analyze (default: {config.SPORT})')
    parser.add_argument('--bet-size', type=float, default=config.BET_SIZE,
                       help=f'Total bet size (default: {config.BET_SIZE})')
    parser.add_argument('--regions', nargs='+', default=config.REGIONS,
                       help=f'Regions to check (default: {config.REGIONS})')
    parser.add_argument('--markets', nargs='+', default=config.MARKETS,
                       help=f'Markets to analyze (default: {config.MARKETS})')
    parser.add_argument('--interval', type=int, default=24,
                       help='Hours between checks for range analysis (default: 24)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.date and not (args.start_date and args.end_date):
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Please provide either --date or both --start-date and --end-date{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        parser.print_help()
        sys.exit(1)
    
    if args.date and (args.start_date or args.end_date):
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Cannot use --date with --start-date/--end-date{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        sys.exit(1)
    
    # Check API key
    if config.API_KEY == 'YOUR_API_KEY_HERE' or not config.API_KEY:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ Please configure your API key in config.py or .env file{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
        return
    
    print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}🔬 Historical Arbitrage Backtesting{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    print(f"{Fore.MAGENTA if COLORS_AVAILABLE else ''}===================================={Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    
    # Initialize historical finder
    finder = HistoricalArbitrageFinder(config.API_KEY)
    
    try:
        if args.date:
            # Single date analysis
            date_iso = parse_date(args.date)
            
            print(f"\n{Fore.BLUE if COLORS_AVAILABLE else ''}⚙️  Analysis Configuration:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            print(f"Date: {date_iso}")
            print(f"Sport: {config.AVAILABLE_SPORTS.get(args.sport, args.sport)}")
            print(f"Bet Size: ${args.bet_size}")
            
            opportunities = finder.find_historical_opportunities(
                args.sport, args.regions, args.markets, args.bet_size, date_iso
            )
            
            finder.display_opportunities(opportunities)
            
            if opportunities:
                total_profit = sum(opp.guaranteed_profit for opp in opportunities)
                print(f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}💰 Total potential profit on {args.date}: ${total_profit:.2f}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            
        else:
            # Date range analysis
            start_iso = parse_date(args.start_date)
            end_iso = parse_date(args.end_date)
            
            print(f"\n{Fore.BLUE if COLORS_AVAILABLE else ''}⚙️  Backtesting Configuration:{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            print(f"Date Range: {start_iso} to {end_iso}")
            print(f"Sport: {config.AVAILABLE_SPORTS.get(args.sport, args.sport)}")
            print(f"Bet Size: ${args.bet_size}")
            print(f"Check Interval: {args.interval} hours")
            
            results = finder.backtest_date_range(
                args.sport, args.regions, args.markets, args.bet_size,
                start_iso, end_iso, args.interval
            )
            
            finder.display_backtest_summary(results)
        
        # Display API usage
        if finder.client.requests_remaining:
            print(f"\n{Fore.BLUE if COLORS_AVAILABLE else ''}📊 API Usage: {finder.client.requests_remaining} requests remaining{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW if COLORS_AVAILABLE else ''}⏹️  Backtesting stopped by user{Style.RESET_ALL if COLORS_AVAILABLE else ''}")
    except Exception as e:
        print(f"{Fore.RED if COLORS_AVAILABLE else ''}❌ An error occurred: {e}{Style.RESET_ALL if COLORS_AVAILABLE else ''}")


if __name__ == "__main__":
    main()
