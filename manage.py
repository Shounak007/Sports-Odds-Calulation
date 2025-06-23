#!/usr/bin/env python3
"""
Project Management Utility for Sports Betting Arbitrage Bot
==========================================================

This utility script helps manage the ar    parser.add_argument('command', 
                       choices=['status', 'install', 'test', 'setup-env', 'run', 'cli', 'dfs', 'wnba', 'backtest'],
                       help='Command to execute')rage bot project with
common tasks like testing, running, and updating configuration.

Author: GitHub Copilot
Date: June 2025
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Get the project directory
PROJECT_DIR = Path(__file__).parent.absolute()
VENV_PYTHON = PROJECT_DIR / "betting_bot" / "bin" / "python"

def get_python_executable():
    """Get the correct Python executable for the current environment"""
    if VENV_PYTHON.exists():
        return f'"{VENV_PYTHON}"'
    else:
        return "python"

def run_command(command, description):
    """Run a shell command with description"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=PROJECT_DIR, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def install_dependencies():
    """Install project dependencies"""
    print("📦 Installing dependencies...")
    python_exec = get_python_executable()
    return run_command(f'{python_exec} -m pip install -r requirements.txt', 
                      "Installing Python packages")

def run_tests():
    """Run the setup tests"""
    print("🧪 Running setup tests...")
    python_exec = get_python_executable()
    return run_command(f'{python_exec} test_setup.py', "Running tests")

def run_bot(args=None):
    """Run the main arbitrage bot"""
    python_exec = get_python_executable()
    cmd = f'{python_exec} arbitrage_bot.py'
    if args:
        cmd += f" {args}"
    return run_command(cmd, "Running arbitrage bot")

def run_cli_bot(args=None):
    """Run the CLI version of the bot"""
    python_exec = get_python_executable()
    cmd = f'{python_exec} run_bot.py'
    if args:
        cmd += f" {args}"
    return run_command(cmd, "Running CLI bot")

def run_dfs_analyzer(args=None):
    """Run the DFS props analyzer"""
    python_exec = get_python_executable()
    cmd = f'{python_exec} dfs_props_analyzer.py'
    if args:
        cmd += f" {args}"
    return run_command(cmd, "Running DFS props analyzer")

def run_backtest(args=None):
    """Run historical backtesting"""
    python_exec = get_python_executable()
    cmd = f'{python_exec} backtest_strategy.py'
    if args:
        cmd += f" {args}"
    return run_command(cmd, "Running backtest")

def run_real_wnba_analyzer(args=None):
    """Run the real-time WNBA analyzer"""
    python_exec = get_python_executable()
    cmd = f'{python_exec} real_wnba_analyzer.py'
    if args:
        cmd += f" {args}"
    return run_command(cmd, "Running real-time WNBA analyzer")

def run_web_app(args=None):
    """Run the web interface"""
    python_exec = get_python_executable()
    cmd = f'{python_exec} web_app.py'
    if args:
        cmd += f" {args}"
    return run_command(cmd, "Starting web interface")

def show_status():
    """Show project status"""
    print("📊 Project Status")
    print("=" * 30)
    
    # Detect environment type
    is_production = not VENV_PYTHON.exists()
    python_executable = "python" if is_production else str(VENV_PYTHON)
    
    if is_production:
        print("✅ Environment: Production (Deployed)")
        print("✅ Python: System Python with packages")
    else:
        print("✅ Environment: Local Development")
        print("✅ Virtual environment: Ready")
    
    # Check Python version
    try:
        result = subprocess.run([python_executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✅ Python version: {result.stdout.strip()}")
    except:
        print("❌ Python version: Cannot determine")
    
    # Check if dependencies are installed
    try:
        subprocess.run([python_executable, "-c", "import requests, colorama, dotenv, tabulate, flask"], 
                      check=True, capture_output=True)
        print("✅ Dependencies: Installed")
    except:
        print("❌ Dependencies: Missing or incomplete")
    
    # Check configuration
    config_file = PROJECT_DIR / "config.py"
    if config_file.exists():
        print("✅ Configuration file: Found")
        
        # Check for API key
        try:
            sys.path.insert(0, str(PROJECT_DIR))
            import config
            if config.API_KEY and config.API_KEY != 'YOUR_API_KEY_HERE':
                print("✅ API key: Configured")
            else:
                print("⚠️  API key: Not configured")
        except:
            print("❌ Configuration: Cannot read")
    else:
        print("❌ Configuration file: Not found")
    
    # Check for .env file
    env_file = PROJECT_DIR / ".env"
    if env_file.exists():
        print("✅ Environment file: Found")
    else:
        print("ℹ️  Environment file: Not found (optional)")

def setup_env_file():
    """Interactive setup of .env file"""
    print("🔐 Setting up environment file...")
    
    api_key = input("Enter your Odds API key: ").strip()
    if not api_key:
        print("❌ No API key provided")
        return False
    
    env_content = f"ODDS_API_KEY={api_key}\n"
    
    env_file = PROJECT_DIR / ".env"
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Environment file created: {env_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to create environment file: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Project management utility for Sports Betting Arbitrage Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  status       Show project status
  install      Install dependencies
  test         Run setup tests
  setup-env    Interactive setup of .env file
  run          Run the main arbitrage bot
  cli          Run the CLI version (with options)
  dfs          Run the DFS player props analyzer
  backtest     Run historical backtesting
  real-wnba    Run the real-time WNBA analyzer
  web          Run the web interface
  
Examples:
  python manage.py status
  python manage.py install
  python manage.py test
  python manage.py run
  python manage.py cli --sport basketball_nba
  python manage.py dfs
  python manage.py backtest --date "2024-01-15"
  python manage.py real-wnba --live
  python manage.py web
        """
    )
    
    parser.add_argument('command', 
                       choices=['status', 'install', 'test', 'setup-env', 'run', 'cli', 'dfs', 'backtest', 'real-wnba', 'web'],
                       help='Command to execute')
    parser.add_argument('--args', type=str, 
                       help='Additional arguments to pass to the command')
    
    args = parser.parse_args()
    
    print("🤖 Sports Betting Arbitrage Bot - Project Manager")
    print("=" * 55)
    
    if args.command == 'status':
        show_status()
    elif args.command == 'install':
        install_dependencies()
    elif args.command == 'test':
        run_tests()
    elif args.command == 'setup-env':
        setup_env_file()
    elif args.command == 'run':
        run_bot(args.args)
    elif args.command == 'cli':
        run_cli_bot(args.args)
    elif args.command == 'dfs':
        run_dfs_analyzer(args.args)
    elif args.command == 'backtest':
        run_backtest(args.args)
    elif args.command == 'real-wnba':
        run_real_wnba_analyzer(args.args)
    elif args.command == 'web':
        run_web_app(args.args)

if __name__ == "__main__":
    main()
