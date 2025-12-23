#!/usr/bin/env python3
"""
Simple demo server for the Vlogger's Local Guide
Serves the HTML interface and provides API endpoints
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import json
import urllib.parse
from pathlib import Path

class LocalGuideHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def start_server(port=8000):
    """Start the demo server"""
    try:
        with socketserver.TCPServer(("", port), LocalGuideHandler) as httpd:
            print(f"🎬 Vlogger's Local Guide Demo Server")
            print(f"🌐 Server running at: http://localhost:{port}")
            print(f"📱 Opening in your browser...")
            print(f"🛑 Press Ctrl+C to stop the server")
            
            # Open browser after a short delay
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{port}')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Demo server stopped. Thanks for trying the Vlogger's Local Guide!")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use. Trying port {port + 1}...")
            start_server(port + 1)
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    # Check if index.html exists
    if not Path("index.html").exists():
        print("❌ index.html not found. Please make sure you're in the correct directory.")
        exit(1)
    
    start_server()