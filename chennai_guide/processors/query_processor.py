"""Query processor implementation for analyzing user input and determining intent."""

import re
from typing import List, Dict, Set, Tuple, Any
from chennai_guide.api.interfaces import QueryProcessorInterface
from chennai_guide.models.data_models import LocalGuideResponse


class NaturalLanguageQueryProcessor(QueryProcessorInterface):
    """Natural language query processor for Chennai Local Guide."""
    
    def __init__(self):
        """Initialize the query processor with keyword patterns."""
        # Keywords that indicate slang translation intent
        self.slang_keywords = {
            'slang', 'translate', 'meaning', 'definition', 'what does', 'what is',
            'explain', 'term', 'phrase', 'word', 'language', 'local language',
            'tamil', 'chennai slang', 'local slang', 'understand', 'means'
        }
        
        # Keywords that indicate neighborhood recommendation intent
        self.neighborhood_keywords = {
            'neighborhood', 'area', 'place', 'location', 'where', 'district',
            'recommend', 'suggestion', 'best place', 'good place', 'filming',
            'content', 'vlog', 'video', 'shoot', 'record', 'visit', 'explore',
            'maps', 'directions', 'google maps'
        }
        
        # Content type keywords for neighborhood preferences
        self.content_type_keywords = {
            'food': {'food', 'restaurant', 'eat', 'dining', 'cuisine', 'street food', 'cooking'},
            'art': {'art', 'gallery', 'museum', 'culture', 'artistic', 'creative', 'painting'},
            'nightlife': {'nightlife', 'bar', 'club', 'night', 'party', 'entertainment', 'drinks'},
            'scenic': {'scenic', 'beautiful', 'view', 'landscape', 'nature', 'photography', 'sunset'},
            'shopping': {'shopping', 'market', 'mall', 'buy', 'store', 'bazaar', 'retail'},
            'historical': {'historical', 'history', 'heritage', 'ancient', 'temple', 'monument', 'old'},
            'beach': {'beach', 'ocean', 'sea', 'water', 'marina', 'coastal', 'shore'},
            'local': {'local', 'authentic', 'traditional', 'genuine', 'real', 'native'}
        }
    
    def analyze_intent(self, query: str) -> str:
        """Determine if query is about slang translation or neighborhood recommendations."""
        query_lower = query.lower()
        
        # Count matches for each intent type
        slang_matches = sum(1 for keyword in self.slang_keywords if keyword in query_lower)
        neighborhood_matches = sum(1 for keyword in self.neighborhood_keywords if keyword in query_lower)
        
        # Check for specific patterns that strongly indicate intent
        
        # Strong slang indicators
        if re.search(r'\b(what does|what is|meaning of|translate|explain)\b.*\b(mean|means)\b', query_lower):
            return 'slang'
        
        if re.search(r'\b(slang|term|phrase|word)\b', query_lower):
            return 'slang'
        
        # Strong neighborhood indicators
        if re.search(r'\b(where|which|recommend|suggest|best place|good place)\b', query_lower):
            return 'neighborhood'
        
        if re.search(r'\b(filming|content|vlog|video|shoot)\b.*\b(place|location|area)\b', query_lower):
            return 'neighborhood'
        
        # If we have clear keyword matches, use the higher count
        if slang_matches > neighborhood_matches:
            return 'slang'
        elif neighborhood_matches > slang_matches:
            return 'neighborhood'
        
        # Default to neighborhood if ambiguous (most queries are likely location-based)
        return 'neighborhood'
    
    def extract_keywords(self, query: str) -> List[str]:
        """Identify relevant terms and content type preferences."""
        query_lower = query.lower()
        keywords = []
        
        # Extract content type preferences
        for content_type, type_keywords in self.content_type_keywords.items():
            if any(keyword in query_lower for keyword in type_keywords):
                keywords.append(content_type)
        
        # Extract specific terms that might be slang
        # Look for quoted terms or terms after "what is/does"
        quoted_terms = re.findall(r'"([^"]+)"', query)
        keywords.extend(quoted_terms)
        
        # Extract terms after common question patterns
        question_patterns = [
            r'what does ([^?]+) mean',
            r'what is ([^?]+)',
            r'meaning of ([^?]+)',
            r'translate ([^?]+)',
            r'explain ([^?]+)'
        ]
        
        for pattern in question_patterns:
            matches = re.findall(pattern, query_lower)
            keywords.extend([match.strip() for match in matches])
        
        # Extract location-related terms
        location_patterns = [
            r'in ([a-zA-Z\s]+)',
            r'near ([a-zA-Z\s]+)',
            r'around ([a-zA-Z\s]+)',
            r'at ([a-zA-Z\s]+)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, query_lower)
            keywords.extend([match.strip() for match in matches if len(match.strip()) > 2])
        
        # Remove duplicates and empty strings
        keywords = list(set([kw for kw in keywords if kw.strip()]))
        
        return keywords
    
    def route_query(self, intent: str, keywords: List[str]) -> str:
        """Direct to slang translator or neighborhood recommender."""
        if intent == 'slang':
            return 'slang_translator'
        elif intent == 'neighborhood':
            return 'neighborhood_recommender'
        else:
            # Default routing
            return 'neighborhood_recommender'
    
    def supports_multi_intent(self, query: str) -> bool:
        """Check if query contains both slang and neighborhood intents."""
        query_lower = query.lower()
        
        # Check for explicit conjunctions that suggest multiple intents
        has_conjunction = any(conj in query_lower for conj in ['and', 'also', 'plus', 'as well as'])
        
        slang_matches = sum(1 for keyword in self.slang_keywords if keyword in query_lower)
        neighborhood_matches = sum(1 for keyword in self.neighborhood_keywords if keyword in query_lower)
        
        # Consider it multi-intent if:
        # 1. Has conjunction AND both types have matches, OR
        # 2. Both types have strong matches (2+ each)
        return (has_conjunction and slang_matches >= 1 and neighborhood_matches >= 1) or \
               (slang_matches >= 2 and neighborhood_matches >= 2)
    
    def extract_multi_intent_components(self, query: str) -> Dict[str, List[str]]:
        """Extract separate components for slang and neighborhood queries."""
        components = {
            'slang': [],
            'neighborhood': []
        }
        
        query_lower = query.lower()
        
        # Split query into sentences or clauses
        clauses = re.split(r'[.;,]|\band\b|\balso\b', query)
        
        for clause in clauses:
            clause = clause.strip()
            if not clause:
                continue
            
            clause_intent = self.analyze_intent(clause)
            clause_keywords = self.extract_keywords(clause)
            
            if clause_intent == 'slang':
                components['slang'].extend(clause_keywords)
            else:
                components['neighborhood'].extend(clause_keywords)
        
        # Remove duplicates
        components['slang'] = list(set(components['slang']))
        components['neighborhood'] = list(set(components['neighborhood']))
        
        return components
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query and return comprehensive analysis including multi-intent support."""
        from chennai_guide.processors.multi_intent_handler import MultiIntentQueryHandler
        
        # Initialize multi-intent handler
        multi_handler = MultiIntentQueryHandler(self)
        
        # Process for multi-intent
        multi_result = multi_handler.process_multi_intent_query(query)
        
        if multi_result['is_multi_intent']:
            return {
                'intent': 'multi_intent',
                'primary_intent': multi_result['primary_intent'],
                'components': multi_result['components'],
                'keywords': multi_result['keywords'],
                'routing': 'multi_intent_handler'
            }
        else:
            # Single intent processing
            intent = self.analyze_intent(query)
            keywords = self.extract_keywords(query)
            routing = self.route_query(intent, keywords)
            
            return {
                'intent': intent,
                'primary_intent': intent,
                'keywords': keywords,
                'routing': routing,
                'components': {}
            }