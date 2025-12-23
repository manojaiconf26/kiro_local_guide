#!/usr/bin/env python3
"""
Simple web server for Chennai Local Guide interface.
Serves the HTML interface and provides API endpoints for backend integration.
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser

# Add the parent directory to the path so we can import chennai_guide modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from chennai_guide.processors.query_processor import NaturalLanguageQueryProcessor
    from chennai_guide.processors.slang_translator import ChennaiSlangTranslator
    from chennai_guide.processors.neighborhood_recommender import ContentAwareNeighborhoodRecommender
    from chennai_guide.parsers.context_parser import ProductMdParser
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Backend components not available: {e}")
    print("Running in frontend-only mode.")
    BACKEND_AVAILABLE = False


class ChennaiGuideHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for Chennai Local Guide web interface."""
    
    def __init__(self, *args, **kwargs):
        # Initialize backend components if available
        if BACKEND_AVAILABLE:
            try:
                self.context_parser = ProductMdParser()
                self.query_processor = NaturalLanguageQueryProcessor()
                self.slang_translator = ChennaiSlangTranslator(self.context_parser)
                self.neighborhood_recommender = ContentAwareNeighborhoodRecommender(self.context_parser)
                self.backend_ready = True
            except Exception as e:
                print(f"Warning: Failed to initialize backend: {e}")
                self.backend_ready = False
        else:
            self.backend_ready = False
        
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            # Serve the main HTML file
            self.serve_html_file()
        elif parsed_path.path == '/api/query':
            # Handle API query requests
            self.handle_api_query(parsed_path.query)
        elif parsed_path.path == '/api/health':
            # Health check endpoint
            self.handle_health_check()
        else:
            # Default file serving
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests for API endpoints."""
        if self.path == '/api/query':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                query = data.get('query', '')
                self.handle_api_query_post(query)
            except json.JSONDecodeError:
                self.send_error_response(400, "Invalid JSON")
        else:
            self.send_error(404)
    
    def serve_html_file(self):
        """Serve the main HTML interface."""
        try:
            html_path = os.path.join(os.path.dirname(__file__), 'index.html')
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(content.encode('utf-8')))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "HTML file not found")
        except Exception as e:
            self.send_error(500, f"Error serving HTML: {str(e)}")
    
    def handle_api_query(self, query_string):
        """Handle API query via GET parameters."""
        params = parse_qs(query_string)
        query = params.get('q', [''])[0]
        
        if not query:
            self.send_error_response(400, "Query parameter 'q' is required")
            return
        
        self.process_query_and_respond(query)
    
    def handle_api_query_post(self, query):
        """Handle API query via POST data."""
        if not query:
            self.send_error_response(400, "Query is required")
            return
        
        self.process_query_and_respond(query)
    
    def process_query_and_respond(self, query):
        """Process the query using backend components and send response."""
        try:
            if self.backend_ready:
                # Use actual backend processing
                result = self.process_with_backend(query)
            else:
                # Fallback to simple processing
                result = self.process_with_fallback(query)
            
            self.send_json_response(result)
        except Exception as e:
            self.send_error_response(500, f"Error processing query: {str(e)}")
    
    def process_with_backend(self, query):
        """Process query using actual backend components."""
        # Analyze query intent
        query_analysis = self.query_processor.process_query(query)
        
        result = {
            'query': query,
            'intent': query_analysis['intent'],
            'results': []
        }
        
        if query_analysis['intent'] == 'slang' or query_analysis['intent'] == 'multi_intent':
            # Process slang translation
            slang_terms = self.slang_translator.identify_slang_terms(query)
            slang_results = []
            for term in slang_terms:
                try:
                    slang_info = self.slang_translator.get_slang_definition(term)
                    slang_results.append({
                        'term': slang_info.term,
                        'definition': slang_info.definition,
                        'usage': slang_info.usage_example,
                        'vlogger_tip': slang_info.vlogger_tip
                    })
                except Exception:
                    continue
            
            if query_analysis['intent'] == 'slang':
                result['results'] = slang_results
            else:
                result['slang_results'] = slang_results
        
        if query_analysis['intent'] == 'neighborhood' or query_analysis['intent'] == 'multi_intent':
            # Process neighborhood recommendations
            content_prefs = self.neighborhood_recommender.match_content_type(query)
            neighborhood_scores = self.neighborhood_recommender.score_neighborhoods(content_prefs)
            
            neighborhood_results = []
            for neighborhood, score in neighborhood_scores[:3]:  # Top 3
                neighborhood_results.append({
                    'name': neighborhood.name,
                    'vibe': neighborhood.vibe,
                    'best_for': neighborhood.best_for,
                    'insider_tips': neighborhood.insider_tips,
                    'google_maps_link': neighborhood.google_maps_link,
                    'score': score
                })
            
            if query_analysis['intent'] == 'neighborhood':
                result['results'] = neighborhood_results
            else:
                result['neighborhood_results'] = neighborhood_results
        
        return result
    
    def process_with_fallback(self, query):
        """Simple fallback processing when backend is not available."""
        return {
            'query': query,
            'intent': 'fallback',
            'results': [],
            'message': 'Backend processing not available. Please use the frontend interface for basic functionality.'
        }
    
    def handle_health_check(self):
        """Handle health check requests."""
        health_status = {
            'status': 'healthy',
            'backend_available': self.backend_ready,
            'components': {
                'context_parser': hasattr(self, 'context_parser'),
                'query_processor': hasattr(self, 'query_processor'),
                'slang_translator': hasattr(self, 'slang_translator'),
                'neighborhood_recommender': hasattr(self, 'neighborhood_recommender')
            }
        }
        self.send_json_response(health_status)
    
    def send_json_response(self, data):
        """Send JSON response."""
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(json_data.encode('utf-8')))
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def send_error_response(self, code, message):
        """Send error response."""
        error_data = {
            'error': True,
            'code': code,
            'message': message
        }
        
        json_data = json.dumps(error_data, ensure_ascii=False, indent=2)
        
        self.send_response(code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(json_data.encode('utf-8')))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to provide cleaner logging."""
        print(f"[{self.address_string()}] {format % args}")


def start_server(port=8000, open_browser=True):
    """Start the Chennai Local Guide web server."""
    # Change to the web directory to serve static files correctly
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, ChennaiGuideHandler)
    
    print(f"Chennai Local Guide server starting on port {port}")
    print(f"Web interface: http://localhost:{port}")
    print(f"API endpoint: http://localhost:{port}/api/query?q=your_query")
    print(f"Health check: http://localhost:{port}/api/health")
    print("Press Ctrl+C to stop the server")
    
    if open_browser:
        # Open browser after a short delay
        def open_browser_delayed():
            import time
            time.sleep(1)
            webbrowser.open(f'http://localhost:{port}')
        
        browser_thread = threading.Thread(target=open_browser_delayed)
        browser_thread.daemon = True
        browser_thread.start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        httpd.server_close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Chennai Local Guide Web Server')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    parser.add_argument('--no-browser', action='store_true', help='Don\'t automatically open browser')
    
    args = parser.parse_args()
    
    start_server(port=args.port, open_browser=not args.no_browser)