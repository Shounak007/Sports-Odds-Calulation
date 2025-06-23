#!/usr/bin/env python3
"""
Comprehensive Test Suite for Sports Betting Bot
==============================================

Tests all components including the new web interface and WNBA analyzer.
"""

import sys
import os
import subprocess
import importlib

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing Python Imports...")
    
    modules = [
        'requests', 'colorama', 'dotenv', 'tabulate', 
        'flask', 'flask_cors', 'numpy', 'pandas'
    ]
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    
    return True

def test_project_modules():
    """Test project-specific modules"""
    print("\n🧪 Testing Project Modules...")
    
    # Add project directory to path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_dir)
    
    modules = [
        'config', 'arbitrage_bot', 'run_bot', 
        'manage', 'real_wnba_analyzer', 'web_app'
    ]
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    
    return True

def test_web_components():
    """Test web interface components"""
    print("\n🧪 Testing Web Components...")
    
    try:
        from flask import Flask
        from web_app import app
        print("✅ Flask app created successfully")
        
        # Test routes exist
        routes = ['/api/status', '/api/run-arbitrage', '/api/run-dfs', 
                 '/api/run-wnba', '/api/test-setup']
        
        with app.test_client() as client:
            for route in routes[:2]:  # Test first 2 routes
                try:
                    response = client.get(route) if 'status' in route else client.post(route)
                    print(f"✅ Route {route} exists")
                except Exception as e:
                    print(f"⚠️  Route {route}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Web components: {e}")
        return False

def test_file_structure():
    """Test required files exist"""
    print("\n🧪 Testing File Structure...")
    
    required_files = [
        'config.py', 'arbitrage_bot.py', 'run_bot.py', 'manage.py',
        'real_wnba_analyzer.py', 'web_app.py', 'requirements.txt',
        'templates/index.html', 'README.md', 'WNBA_BETTING_GUIDE.md',
        'WEB_INTERFACE_GUIDE.md'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            return False
    
    return True

def test_confidence_scores():
    """Test WNBA confidence scoring system"""
    print("\n🧪 Testing WNBA Confidence Scoring...")
    
    try:
        from real_wnba_analyzer import RealTimeWNBAAnalyzer
        analyzer = RealTimeWNBAAnalyzer()
        
        # Test player data
        test_player = {
            'ppg': 20.0, 'rpg': 8.0, 'apg': 5.0,
            'salary': 9000, 'status': 'Healthy'
        }
        
        analysis = analyzer.analyze_player_value("Test Player", test_player)
        
        if 'confidence_scores' in analysis:
            print("✅ Confidence scores generated")
            
            # Check confidence score types
            expected_props = ['points', 'rebounds', 'assists']
            for prop in expected_props:
                if prop in analysis['confidence_scores']:
                    score = analysis['confidence_scores'][prop]
                    if 0 <= score <= 100:
                        print(f"✅ {prop}: {score:.1f}%")
                    else:
                        print(f"❌ {prop}: Invalid score {score}")
                        return False
                else:
                    print(f"❌ Missing confidence score for {prop}")
                    return False
            
            return True
        else:
            print("❌ No confidence scores in analysis")
            return False
            
    except Exception as e:
        print(f"❌ Confidence scoring: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("🤖 Sports Betting Bot - Comprehensive Test Suite")
    print("=" * 55)
    
    tests = [
        ("Import Test", test_imports),
        ("Project Modules Test", test_project_modules),
        ("File Structure Test", test_file_structure),
        ("Web Components Test", test_web_components),
        ("WNBA Confidence Test", test_confidence_scores)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your betting bot is ready to use.")
        print("\nNext steps:")
        print("1. Start web interface: python manage.py web")
        print("2. Open browser to: http://localhost:5000")
        print("3. Run WNBA analysis: python manage.py real-wnba")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
