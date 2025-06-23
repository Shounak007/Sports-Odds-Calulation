#!/usr/bin/env python3
"""
Sports Betting Bot Web Interface
===============================

A simple Flask web application to interact with the betting bot tools.
Provides a user-friendly interface to run arbitrage analysis, DFS analysis,
and WNBA betting recommendations.

Author: GitHub Copilot
Date: June 2025
"""

from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import subprocess
import os
import sys
import json
import threading
import time
from datetime import datetime
import io
import contextlib

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Configuration
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Use appropriate Python executable for the environment
if os.path.exists(os.path.join(PROJECT_DIR, "betting_bot", "bin", "python")):
    # Local development with virtual environment
    VENV_PYTHON = os.path.join(PROJECT_DIR, "betting_bot", "bin", "python")
else:
    # Production environment (Render, Railway, etc.)
    VENV_PYTHON = "python"

class OutputCapture:
    """Capture stdout for web display"""
    def __init__(self):
        self.output = []
        
    def write(self, text):
        self.output.append(text)
        
    def flush(self):
        pass
        
    def get_output(self):
        return ''.join(self.output)

def run_command_safely(command, description):
    """Run a command safely and capture output"""
    try:
        print(f"🔧 {description}...")
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=PROJECT_DIR,
            capture_output=True, 
            text=True,
            timeout=60  # 60 second timeout
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"
            
        return {
            'success': result.returncode == 0,
            'output': output,
            'error': result.stderr if result.returncode != 0 else None
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'output': '',
            'error': 'Command timed out after 60 seconds'
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'error': str(e)
        }

def build_python_command(script_with_args):
    """Build a Python command with the correct executable"""
    if VENV_PYTHON == "python":
        return f"python {script_with_args}"
    else:
        return f'"{VENV_PYTHON}" {script_with_args}'

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get project status"""
    cmd = build_python_command('manage.py status')
    result = run_command_safely(cmd, "Getting project status")
    return jsonify(result)

@app.route('/api/run-arbitrage', methods=['POST'])
def run_arbitrage():
    """Run arbitrage analysis"""
    data = request.get_json() or {}
    sport = data.get('sport', 'basketball_nba')
    bet_size = data.get('bet_size', 100)
    
    cmd = build_python_command(f'run_bot.py --mode arbitrage --sport {sport} --bet-size {bet_size}')
    result = run_command_safely(cmd, f"Running arbitrage analysis for {sport}")
    return jsonify(result)

@app.route('/api/run-dfs')
def run_dfs():
    """Run DFS analysis"""
    cmd = build_python_command('run_bot.py --mode dfs')
    result = run_command_safely(cmd, "Running DFS analysis")
    return jsonify(result)

@app.route('/api/run-wnba')
def run_wnba():
    """Run WNBA betting analysis"""
    cmd = build_python_command('run_bot.py --mode wnba')
    result = run_command_safely(cmd, "Running WNBA betting analysis")
    return jsonify(result)

@app.route('/api/run-backtest', methods=['POST'])
def run_backtest():
    """Run backtest analysis"""
    data = request.get_json() or {}
    date = data.get('date', '2024-01-15')
    sport = data.get('sport', 'basketball_nba')
    
    cmd = build_python_command(f'backtest_strategy.py --date "{date}" --sport {sport}')
    result = run_command_safely(cmd, f"Running backtest for {date}")
    return jsonify(result)

@app.route('/api/available-options')
def get_available_options():
    """Get available sports, regions, and markets"""
    cmd = build_python_command('run_bot.py --list-options')
    result = run_command_safely(cmd, "Getting available options")
    return jsonify(result)

@app.route('/api/test-setup')
def test_setup():
    """Run setup tests"""
    cmd = build_python_command('test_setup.py')
    result = run_command_safely(cmd, "Running setup tests")
    return jsonify(result)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🌐 Starting Sports Betting Bot Web Interface...")
    print(f"📡 Server will be available at: http://localhost:{port}")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
