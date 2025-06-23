#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from web_app import app

if __name__ == "__main__":
    app.run()
