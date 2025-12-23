#!/usr/bin/env python3
"""
Chennai Local Guide - Demo Server Startup Script

This script provides an easy way to start the Chennai Local Guide web server
with various configuration options.
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import chennai_guide
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install the package in development mode."""
    print("Installing Chennai Local Guide in development mode...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
        print("SUCCESS: Installation completed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install dependencies")
        return False

def start_server(port=8000, no_browser=False, dev_mode=False):
    """Start the Chennai Local Guide server."""
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("WARNING: Chennai Local Guide package not found.")
        if dev_mode:
            if not install_dependencies():
                print("ERROR: Cannot start server without dependencies")
                return False
        else:
            print("Please install the package first:")
            print("  pip install -e .")
            return False
    
    # Import and start the server
    try:
        from chennai_guide.web.server import start_server as web_start_server
        print("Starting Chennai Local Guide Demo Server...")
        print(f"Project root: {project_root}")
        web_start_server(port=port, open_browser=not no_browser)
        return True
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        return True
    except Exception as e:
        print(f"ERROR: Error starting server: {e}")
        return False

def main():
    """Main entry point for the startup script."""
    parser = argparse.ArgumentParser(
        description='Chennai Local Guide Demo Server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_server.py                    # Start on default port 8000
  python start_server.py --port 3000       # Start on port 3000
  python start_server.py --no-browser      # Don't open browser automatically
  python start_server.py --dev             # Development mode with auto-install
        """
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=8000, 
        help='Port to run the server on (default: 8000)'
    )
    
    parser.add_argument(
        '--no-browser', 
        action='store_true', 
        help='Don\'t automatically open browser'
    )
    
    parser.add_argument(
        '--dev', 
        action='store_true', 
        help='Development mode - auto-install dependencies if needed'
    )
    
    parser.add_argument(
        '--check', 
        action='store_true', 
        help='Check if dependencies are installed and exit'
    )
    
    args = parser.parse_args()
    
    if args.check:
        if check_dependencies():
            print("SUCCESS: Chennai Local Guide is properly installed")
            sys.exit(0)
        else:
            print("ERROR: Chennai Local Guide is not installed")
            print("Run: pip install -e .")
            sys.exit(1)
    
    success = start_server(
        port=args.port,
        no_browser=args.no_browser,
        dev_mode=args.dev
    )
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()