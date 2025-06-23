#!/usr/bin/env python3
"""
Test script to validate the Sports Betting Arbitrage Bot setup
============================================================

This script tests the basic functionality without making API calls.

Author: GitHub Copilot
Date: June 2025
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        import colorama
        print("✅ colorama imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import colorama: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    try:
        import tabulate
        print("✅ tabulate imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import tabulate: {e}")
        return False
    
    return True


def test_config():
    """Test configuration loading"""
    print("\n⚙️  Testing configuration...")
    
    try:
        import config
        print("✅ config.py loaded successfully")
        
        # Test required configuration variables
        required_vars = ['API_KEY', 'SPORT', 'REGIONS', 'MARKETS', 'BET_SIZE']
        for var in required_vars:
            if hasattr(config, var):
                print(f"✅ {var} is configured")
            else:
                print(f"❌ {var} is missing from config")
                return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import config: {e}")
        return False


def test_main_modules():
    """Test if main modules can be imported"""
    print("\n📦 Testing main modules...")
    
    try:
        from arbitrage_bot import OddsAPIClient, ArbitrageCalculator, ArbitrageFinder
        print("✅ arbitrage_bot modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import arbitrage_bot modules: {e}")
        return False
    
    try:
        import run_bot
        print("✅ run_bot imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import run_bot: {e}")
        return False
    
    try:
        import backtest_strategy
        print("✅ backtest_strategy imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import backtest_strategy: {e}")
        return False
    
    return True


def test_calculator():
    """Test the arbitrage calculator with sample data"""
    print("\n🧮 Testing arbitrage calculator...")
    
    try:
        from arbitrage_bot import ArbitrageCalculator
        
        # Test case 1: Arbitrage opportunity (profit)
        odds1 = [2.10, 2.05]  # Should result in arbitrage
        calc = ArbitrageCalculator()
        
        arb_pct = calc.calculate_arbitrage_percentage(odds1)
        print(f"✅ Arbitrage percentage calculation: {arb_pct:.4f}")
        
        if arb_pct < 1.0:
            print(f"✅ Arbitrage opportunity detected (profit margin: {(1-arb_pct)*100:.2f}%)")
        else:
            print(f"ℹ️  No arbitrage opportunity (loss margin: {(arb_pct-1)*100:.2f}%)")
        
        stakes = calc.calculate_stakes(odds1, 100)
        print(f"✅ Stakes calculation: {stakes}")
        
        profit = calc.calculate_guaranteed_profit(odds1, 100)
        print(f"✅ Profit calculation: ${profit:.2f}")
        
        # Test case 2: No arbitrage opportunity
        odds2 = [1.90, 1.90]  # Should not result in arbitrage
        arb_pct2 = calc.calculate_arbitrage_percentage(odds2)
        print(f"✅ No arbitrage test: {arb_pct2:.4f} (should be > 1.0)")
        
        return True
        
    except Exception as e:
        print(f"❌ Calculator test failed: {e}")
        return False


def test_api_client_creation():
    """Test if API client can be created"""
    print("\n🌐 Testing API client creation...")
    
    try:
        from arbitrage_bot import OddsAPIClient
        
        # Test with dummy API key
        client = OddsAPIClient("test_api_key")
        print("✅ OddsAPIClient created successfully")
        
        # Test session creation
        if hasattr(client, 'session') and client.session:
            print("✅ HTTP session initialized")
        else:
            print("❌ HTTP session not initialized")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API client test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🤖 Sports Betting Arbitrage Bot - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("Main Modules Test", test_main_modules),
        ("Calculator Test", test_calculator),
        ("API Client Test", test_api_client_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Add your API key to config.py or create a .env file")
        print("2. Run: python arbitrage_bot.py")
        print("3. Or use: python run_bot.py --list-options")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
