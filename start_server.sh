#!/bin/bash
# Chennai Local Guide - Unix/Linux/macOS Startup Script
# This script provides an easy way to start the server on Unix-like systems

set -e

echo "🎬 Chennai Local Guide - Demo Server"
echo "====================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "start_server.py" ]; then
    echo "❌ start_server.py not found"
    echo "Please run this script from the Chennai Local Guide project directory"
    exit 1
fi

# Make the script executable if it isn't already
chmod +x start_server.py

# Start the server with default settings
echo "🚀 Starting Chennai Local Guide server..."
python3 start_server.py --dev

echo "👋 Server stopped"