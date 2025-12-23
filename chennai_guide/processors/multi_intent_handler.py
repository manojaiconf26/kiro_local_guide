"""Multi-intent query handler for processing queries with both slang and neighborhood requests."""

from typing import Dict, List, Any, Tuple
from chennai_guide.models.data_models import LocalGuideResponse, SlangTerm, Neighborhood
from chennai_guide.processors.query_processor import NaturalLanguageQueryProcessor


class MultiIntentQueryHandler:
    """Handles queries that contain both slang translation and neighborhood recommendation requests."""
    
    def __init__(self, query_processor: NaturalLanguageQueryProcessor):
        """Initialize with a query processor for intent analysis."""
        self.query_processor = query_processor
    
    def process_multi_intent_query(self, query: str) -> Dict[str, Any]:
        """Process a query that may contain multiple intents and organize results by type."""
        # Check if query actually has multiple intents
        if not self.query_processor.supports_multi_intent(query):
            # Single intent - use regular processing
            intent = self.query_processor.analyze_intent(query)
            keywords = self.query_processor.extract_keywords(query)
            return {
                'is_multi_intent': False,
                'primary_intent': intent,
                'keywords': keywords,
                'components': {}
            }
        
        # Extract components for each intent type
        components = self.query_processor.extract_multi_intent_components(query)
        
        return {
            'is_multi_intent': True,
            'primary_intent': self._determine_primary_intent(components),
            'components': components,
            'keywords': components.get('slang', []) + components.get('neighborhood', [])
        }
    
    def _determine_primary_intent(self, components: Dict[str, List[str]]) -> str:
        """Determine which intent should be considered primary based on component strength."""
        slang_strength = len(components.get('slang', []))
        neighborhood_strength = len(components.get('neighborhood', []))
        
        if slang_strength > neighborhood_strength:
            return 'slang'
        elif neighborhood_strength > slang_strength:
            return 'neighborhood'
        else:
            # Default to neighborhood for ties
            return 'neighborhood'
    
    def organize_multi_intent_results(self, 
                                    slang_results: List[SlangTerm] = None,
                                    neighborhood_results: List[Neighborhood] = None,
                                    query: str = "") -> LocalGuideResponse:
        """Organize results from both slang and neighborhood processing into a unified response."""
        
        # Combine all results
        all_results = []
        maps_links = []
        suggestions = []
        
        # Add slang results
        if slang_results:
            all_results.extend(slang_results)
            suggestions.append("Found slang translations in your query")
        
        # Add neighborhood results
        if neighborhood_results:
            all_results.extend(neighborhood_results)
            # Extract maps links from neighborhoods
            for neighborhood in neighborhood_results:
                if neighborhood.google_maps_link:
                    maps_links.append(neighborhood.google_maps_link)
            suggestions.append("Found neighborhood recommendations for your content needs")
        
        # Determine overall query type
        if slang_results and neighborhood_results:
            query_type = "multi_intent"
        elif slang_results:
            query_type = "slang"
        elif neighborhood_results:
            query_type = "neighborhood"
        else:
            query_type = "unknown"
        
        # Create content creator note
        content_creator_note = self._generate_multi_intent_note(slang_results, neighborhood_results)
        
        return LocalGuideResponse(
            query_type=query_type,
            results=all_results,
            content_creator_note=content_creator_note,
            suggestions=suggestions,
            maps_links=maps_links
        )
    
    def _generate_multi_intent_note(self, 
                                  slang_results: List[SlangTerm] = None,
                                  neighborhood_results: List[Neighborhood] = None) -> str:
        """Generate a helpful note for content creators based on the mixed results."""
        
        notes = []
        
        if slang_results and neighborhood_results:
            notes.append("Your query covered both local language and location recommendations.")
            notes.append(f"Found {len(slang_results)} slang term(s) and {len(neighborhood_results)} neighborhood(s).")
            notes.append("Use the slang authentically in your content while filming in the recommended areas.")
        elif slang_results:
            notes.append(f"Found {len(slang_results)} Chennai slang term(s) to help with authentic local language.")
        elif neighborhood_results:
            notes.append(f"Found {len(neighborhood_results)} neighborhood recommendation(s) for your content creation needs.")
        else:
            notes.append("No specific matches found. Try asking about Chennai slang terms or neighborhood recommendations.")
        
        return " ".join(notes)
    
    def split_query_by_intent(self, query: str) -> Tuple[str, str]:
        """Split a multi-intent query into separate slang and neighborhood components."""
        components = self.query_processor.extract_multi_intent_components(query)
        
        # Reconstruct query parts
        slang_query = ""
        neighborhood_query = ""
        
        if components.get('slang'):
            slang_terms = " ".join(components['slang'])
            slang_query = f"What does {slang_terms} mean?"
        
        if components.get('neighborhood'):
            content_types = " ".join(components['neighborhood'])
            neighborhood_query = f"Recommend neighborhoods for {content_types} content"
        
        return slang_query, neighborhood_query
    
    def merge_single_intent_responses(self, 
                                    slang_response: LocalGuideResponse = None,
                                    neighborhood_response: LocalGuideResponse = None) -> LocalGuideResponse:
        """Merge responses from separate slang and neighborhood processors."""
        
        if not slang_response and not neighborhood_response:
            return LocalGuideResponse(
                query_type="unknown",
                results=[],
                content_creator_note="No results found for your query.",
                suggestions=["Try asking about specific Chennai slang terms or neighborhood recommendations"],
                maps_links=[]
            )
        
        # Combine results
        all_results = []
        all_maps_links = []
        all_suggestions = []
        
        if slang_response:
            all_results.extend(slang_response.results)
            all_suggestions.extend(slang_response.suggestions)
        
        if neighborhood_response:
            all_results.extend(neighborhood_response.results)
            all_maps_links.extend(neighborhood_response.maps_links)
            all_suggestions.extend(neighborhood_response.suggestions)
        
        # Create combined response
        return LocalGuideResponse(
            query_type="multi_intent",
            results=all_results,
            content_creator_note=self._generate_combined_note(slang_response, neighborhood_response),
            suggestions=list(set(all_suggestions)),  # Remove duplicates
            maps_links=all_maps_links
        )
    
    def _generate_combined_note(self, 
                              slang_response: LocalGuideResponse = None,
                              neighborhood_response: LocalGuideResponse = None) -> str:
        """Generate a combined content creator note from separate responses."""
        
        notes = []
        
        if slang_response and neighborhood_response:
            notes.append("Your query included both language and location elements.")
            if slang_response.results:
                notes.append(f"Language: {slang_response.content_creator_note}")
            if neighborhood_response.results:
                notes.append(f"Locations: {neighborhood_response.content_creator_note}")
        elif slang_response:
            notes.append(slang_response.content_creator_note)
        elif neighborhood_response:
            notes.append(neighborhood_response.content_creator_note)
        
        return " ".join(notes) if notes else "Combined results for your Chennai content creation needs."