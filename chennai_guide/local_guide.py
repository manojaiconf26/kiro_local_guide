"""
Main integration component for Chennai Local Guide.
Wires together Context Parser, Query Processor, and Response Generators.
Implements end-to-end query processing pipeline with comprehensive logging and monitoring.
"""

import logging
import time
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

from chennai_guide.parsers.context_parser import ProductMdParser
from chennai_guide.processors.query_processor import NaturalLanguageQueryProcessor
from chennai_guide.processors.slang_translator import SlangTranslator
from chennai_guide.processors.neighborhood_recommender import NeighborhoodRecommender
from chennai_guide.processors.multi_intent_handler import MultiIntentQueryHandler
from chennai_guide.processors.cultural_guide import CulturalGuideProcessor
from chennai_guide.processors.content_inspiration import ContentInspirationEngine
from chennai_guide.processors.discovery_browser import CulturalDiscoveryBrowser
from chennai_guide.models.data_models import LocalGuideResponse, SlangTerm, Neighborhood


class ChennaiLocalGuide:
    """
    Main integration class for Chennai Local Guide system.
    
    Provides a unified interface for processing queries about Chennai slang and neighborhoods,
    with comprehensive logging, monitoring, and error handling.
    """
    
    def __init__(self, 
                 product_md_path: str = "product.md",
                 enable_hot_reload: bool = True,
                 log_level: str = "INFO"):
        """
        Initialize Chennai Local Guide with all components.
        
        Args:
            product_md_path: Path to the product.md context file
            enable_hot_reload: Whether to enable hot-reload for product.md changes
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        # Set up logging
        self._setup_logging(log_level)
        self.logger = logging.getLogger(__name__)
        
        # Initialize core components
        self.logger.info("Initializing Chennai Local Guide components...")
        
        try:
            # Context Parser - single source of truth for Chennai knowledge
            self.context_parser = ProductMdParser(
                product_md_path=product_md_path,
                enable_hot_reload=enable_hot_reload
            )
            self.logger.info(f"✓ Context parser initialized with {product_md_path}")
            
            # Query Processor - analyzes user intent
            self.query_processor = NaturalLanguageQueryProcessor()
            self.logger.info("✓ Query processor initialized")
            
            # Response Generators
            self.slang_translator = SlangTranslator(self.context_parser)
            self.neighborhood_recommender = NeighborhoodRecommender(self.context_parser)
            self.logger.info("✓ Core response generators initialized")
            
            # Multi-intent handler
            self.multi_intent_handler = MultiIntentQueryHandler(self.query_processor)
            self.logger.info("✓ Multi-intent handler initialized")
            
            # Additional processors
            self.cultural_guide = CulturalGuideProcessor(self.context_parser)
            self.content_inspiration = ContentInspirationEngine(self.context_parser)
            self.discovery_browser = CulturalDiscoveryBrowser(self.context_parser)
            self.logger.info("✓ Additional processors initialized")
            
            # Register reload callbacks for hot-reload
            if enable_hot_reload:
                self.context_parser.add_reload_callback(self._on_context_reload)
                self.logger.info("✓ Hot-reload callbacks registered")
            
            # System status
            self.is_ready = True
            self.initialization_time = time.time()
            self.query_count = 0
            self.error_count = 0
            
            self.logger.info("🎬 Chennai Local Guide initialized successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Chennai Local Guide: {e}")
            self.is_ready = False
            raise
    
    def _setup_logging(self, log_level: str) -> None:
        """Set up comprehensive logging configuration."""
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('chennai_guide.log', encoding='utf-8')
            ]
        )
    
    def _on_context_reload(self) -> None:
        """Callback function called when product.md is reloaded."""
        self.logger.info("📄 Context file reloaded, refreshing components...")
        try:
            # Reload slang data
            self.slang_translator.reload_slang_data()
            
            # Reload neighborhood data
            self.neighborhood_recommender.neighborhoods = self.context_parser.parse_neighborhoods()
            
            # Reload cultural data
            self.cultural_guide.reload_cultural_data()
            
            # Reload content inspiration data
            self.content_inspiration.reload_data()
            
            # Reload discovery data
            self.discovery_browser.reload_data()
            
            self.logger.info("✓ All components refreshed after context reload")
            
        except Exception as e:
            self.logger.error(f"❌ Error refreshing components after context reload: {e}")
    
    def process_query(self, query: str) -> LocalGuideResponse:
        """
        Main query processing pipeline.
        
        Args:
            query: Natural language query from user
            
        Returns:
            LocalGuideResponse with results and metadata
        """
        if not self.is_ready:
            return self._create_error_response("System not ready", query)
        
        if not query or not query.strip():
            return self._create_error_response("Empty query provided", query)
        
        start_time = time.time()
        self.query_count += 1
        
        self.logger.info(f"🔍 Processing query #{self.query_count}: '{query[:50]}{'...' if len(query) > 50 else ''}'")
        
        try:
            # Step 1: Analyze query intent and extract components
            query_analysis = self.query_processor.process_query(query)
            self.logger.debug(f"Query analysis: {query_analysis}")
            
            # Step 2: Route to appropriate processors based on intent
            if query_analysis['intent'] == 'multi_intent':
                response = self._process_multi_intent_query(query, query_analysis)
            elif query_analysis['intent'] == 'slang':
                response = self._process_slang_query(query, query_analysis['keywords'])
            elif query_analysis['intent'] == 'neighborhood':
                response = self._process_neighborhood_query(query, query_analysis['keywords'])
            else:
                # Default to neighborhood processing
                response = self._process_neighborhood_query(query, query_analysis['keywords'])
            
            # Step 3: Add processing metadata
            processing_time = time.time() - start_time
            response = self._add_metadata(response, query, processing_time, query_analysis)
            
            self.logger.info(f"✓ Query processed successfully in {processing_time:.3f}s")
            return response
            
        except Exception as e:
            self.error_count += 1
            processing_time = time.time() - start_time
            self.logger.error(f"❌ Error processing query: {e}")
            return self._create_error_response(str(e), query, processing_time)
    
    def _process_slang_query(self, query: str, keywords: List[str]) -> LocalGuideResponse:
        """Process slang translation queries."""
        self.logger.debug(f"Processing slang query with keywords: {keywords}")
        
        # Check if it's a direct term lookup or text analysis
        if len(keywords) == 1 and not any(word in query.lower() for word in ['in', 'text', 'sentence']):
            # Direct term lookup
            term = keywords[0]
            slang_info = self.slang_translator.get_slang_definition(term)
            
            if slang_info:
                results = [slang_info]
                content_creator_note = f"Found definition for '{term}' - use it authentically in your Chennai content!"
                suggestions = [
                    "Try using this term in your next video",
                    "Practice the pronunciation with locals",
                    "Learn related terms for more authentic content"
                ]
            else:
                results = []
                suggestions = self.slang_translator.suggest_related_terms(term)
                content_creator_note = f"'{term}' not found in our Chennai slang dictionary. Try these related terms:"
        else:
            # Text analysis for multiple terms
            translation_result = self.slang_translator.translate_text_with_slang(query)
            
            if translation_result.get('slang_detected'):
                # Convert found terms to SlangTerm objects
                results = []
                for term_name in translation_result.get('terms_in_order', []):
                    slang_info = self.slang_translator.get_slang_definition(term_name)
                    if slang_info:
                        results.append(slang_info)
                
                content_creator_note = translation_result.get('message', 'Found Chennai slang in your text!')
                suggestions = [
                    "Use these terms naturally in your content",
                    "Practice pronunciation with locals",
                    "Learn the cultural context behind each term"
                ]
            else:
                results = []
                content_creator_note = "No Chennai slang detected in your text."
                suggestions = translation_result.get('suggestions', [])
        
        return LocalGuideResponse(
            query_type="slang",
            results=results,
            content_creator_note=content_creator_note,
            suggestions=suggestions,
            maps_links=[]
        )
    
    def _process_neighborhood_query(self, query: str, keywords: List[str]) -> LocalGuideResponse:
        """Process neighborhood recommendation queries."""
        self.logger.debug(f"Processing neighborhood query with keywords: {keywords}")
        
        # Extract content preferences from query
        content_preferences = self.neighborhood_recommender.match_content_type(query)
        if not content_preferences and keywords:
            content_preferences = keywords
        
        # Get scored neighborhood recommendations
        scored_neighborhoods = self.neighborhood_recommender.score_neighborhoods(content_preferences)
        
        # Take top 5 recommendations
        top_neighborhoods = [neighborhood for neighborhood, score in scored_neighborhoods[:5] if score > 0]
        
        # Create comprehensive response
        return self.neighborhood_recommender.create_neighborhood_response(top_neighborhoods, query)
    
    def _process_multi_intent_query(self, query: str, query_analysis: Dict[str, Any]) -> LocalGuideResponse:
        """Process queries with multiple intents (both slang and neighborhood)."""
        self.logger.debug(f"Processing multi-intent query: {query_analysis}")
        
        components = query_analysis.get('components', {})
        
        # Process slang component
        slang_results = []
        if components.get('slang'):
            slang_response = self._process_slang_query(query, components['slang'])
            slang_results = slang_response.results
        
        # Process neighborhood component
        neighborhood_results = []
        if components.get('neighborhood'):
            neighborhood_response = self._process_neighborhood_query(query, components['neighborhood'])
            neighborhood_results = neighborhood_response.results
        
        # Organize multi-intent results
        return self.multi_intent_handler.organize_multi_intent_results(
            slang_results=slang_results,
            neighborhood_results=neighborhood_results,
            query=query
        )
    
    def _add_metadata(self, 
                     response: LocalGuideResponse, 
                     query: str, 
                     processing_time: float,
                     query_analysis: Dict[str, Any]) -> LocalGuideResponse:
        """Add processing metadata to response."""
        # Add metadata as additional attributes (not part of the dataclass)
        response.processing_time = processing_time
        response.query_count = self.query_count
        response.intent_analysis = query_analysis
        response.timestamp = time.time()
        
        return response
    
    def _create_error_response(self, 
                              error_message: str, 
                              query: str = "", 
                              processing_time: float = 0.0) -> LocalGuideResponse:
        """Create error response with helpful suggestions."""
        return LocalGuideResponse(
            query_type="error",
            results=[],
            content_creator_note=f"Error: {error_message}",
            suggestions=[
                "Try asking about Chennai slang terms",
                "Ask for neighborhood recommendations",
                "Check if your query is clear and specific",
                "Try example queries like 'What does machaan mean?' or 'Best places for food content'"
            ],
            maps_links=[]
        )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status and health information."""
        uptime = time.time() - self.initialization_time if self.is_ready else 0
        
        return {
            "status": "ready" if self.is_ready else "not_ready",
            "uptime_seconds": uptime,
            "query_count": self.query_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.query_count, 1),
            "components": {
                "context_parser": {
                    "ready": hasattr(self, 'context_parser'),
                    "hot_reload_enabled": getattr(self.context_parser, '_hot_reload_enabled', False) if hasattr(self, 'context_parser') else False,
                    "product_md_path": str(getattr(self.context_parser, 'product_md_path', 'unknown')) if hasattr(self, 'context_parser') else 'unknown'
                },
                "query_processor": {"ready": hasattr(self, 'query_processor')},
                "slang_translator": {
                    "ready": hasattr(self, 'slang_translator'),
                    "slang_terms_loaded": len(getattr(self.slang_translator, '_slang_dict', {})) if hasattr(self, 'slang_translator') else 0
                },
                "neighborhood_recommender": {
                    "ready": hasattr(self, 'neighborhood_recommender'),
                    "neighborhoods_loaded": len(getattr(self.neighborhood_recommender, 'neighborhoods', [])) if hasattr(self, 'neighborhood_recommender') else 0
                },
                "multi_intent_handler": {"ready": hasattr(self, 'multi_intent_handler')},
                "cultural_guide": {"ready": hasattr(self, 'cultural_guide')},
                "content_inspiration": {"ready": hasattr(self, 'content_inspiration')},
                "discovery_browser": {"ready": hasattr(self, 'discovery_browser')}
            },
            "last_query_time": getattr(self, '_last_query_time', None),
            "version": "1.0.0"
        }
    
    def reload_context(self) -> Dict[str, Any]:
        """Manually trigger context reload and return status."""
        try:
            self.logger.info("🔄 Manual context reload requested")
            self.context_parser.reload_context()
            self._on_context_reload()
            
            return {
                "success": True,
                "message": "Context reloaded successfully",
                "timestamp": time.time()
            }
        except Exception as e:
            self.logger.error(f"❌ Manual context reload failed: {e}")
            return {
                "success": False,
                "message": f"Context reload failed: {str(e)}",
                "timestamp": time.time()
            }
    
    def get_available_slang_terms(self) -> List[str]:
        """Get list of all available slang terms."""
        if hasattr(self, 'slang_translator'):
            return self.slang_translator.get_all_slang_terms()
        return []
    
    def get_available_neighborhoods(self) -> List[str]:
        """Get list of all available neighborhoods."""
        if hasattr(self, 'neighborhood_recommender'):
            return [n.name for n in self.neighborhood_recommender.neighborhoods]
        return []
    
    def search_slang(self, term: str) -> Optional[SlangTerm]:
        """Direct slang term lookup."""
        if hasattr(self, 'slang_translator'):
            return self.slang_translator.get_slang_definition(term)
        return None
    
    def search_neighborhood(self, name: str) -> Optional[Neighborhood]:
        """Direct neighborhood lookup."""
        if hasattr(self, 'neighborhood_recommender'):
            return self.neighborhood_recommender.get_neighborhood_profile(name)
        return None
    
    def get_content_inspiration(self) -> LocalGuideResponse:
        """Get content creation inspiration."""
        if hasattr(self, 'content_inspiration'):
            return self.content_inspiration.get_content_inspiration()
        return self._create_error_response("Content inspiration not available")
    
    def browse_categories(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Browse available content categories."""
        if hasattr(self, 'discovery_browser'):
            if category:
                return self.discovery_browser.get_category_content(category)
            else:
                return self.discovery_browser.get_all_categories()
        return {"error": "Discovery browser not available"}
    
    def __del__(self):
        """Cleanup when the guide is destroyed."""
        if hasattr(self, 'context_parser'):
            self.context_parser.stop_file_watching()
        
        if hasattr(self, 'logger'):
            self.logger.info("🛑 Chennai Local Guide shutting down")


# Convenience function for quick initialization
def create_chennai_guide(product_md_path: str = "product.md", 
                        enable_hot_reload: bool = True,
                        log_level: str = "INFO") -> ChennaiLocalGuide:
    """
    Create and initialize a Chennai Local Guide instance.
    
    Args:
        product_md_path: Path to the product.md context file
        enable_hot_reload: Whether to enable hot-reload for product.md changes
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Initialized ChennaiLocalGuide instance
    """
    return ChennaiLocalGuide(
        product_md_path=product_md_path,
        enable_hot_reload=enable_hot_reload,
        log_level=log_level
    )


# Example usage and testing
if __name__ == "__main__":
    # Initialize the guide
    guide = create_chennai_guide()
    
    # Test queries
    test_queries = [
        "What does machaan mean?",
        "Best neighborhoods for food content",
        "Where can I film street food and what does semma mean?",
        "Recommend places for cultural content"
    ]
    
    print("🎬 Chennai Local Guide - Integration Test")
    print("=" * 50)
    
    # System status
    status = guide.get_system_status()
    print(f"System Status: {status['status']}")
    print(f"Components Ready: {sum(1 for comp in status['components'].values() if comp['ready'])}/{len(status['components'])}")
    print()
    
    # Process test queries
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query}")
        response = guide.process_query(query)
        print(f"Intent: {response.query_type}")
        print(f"Results: {len(response.results)} items")
        print(f"Note: {response.content_creator_note}")
        if hasattr(response, 'processing_time'):
            print(f"Processing time: {response.processing_time:.3f}s")
        print("-" * 30)
    
    print(f"\nTotal queries processed: {guide.query_count}")
    print(f"Error rate: {guide.error_count}/{guide.query_count}")