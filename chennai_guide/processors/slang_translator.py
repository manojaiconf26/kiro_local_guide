"""Slang translator component for Chennai Local Guide."""

import re
from typing import List, Dict, Tuple, Optional
from chennai_guide.models.data_models import SlangTerm
from chennai_guide.parsers.context_parser import ProductMdParser


class SlangTranslator:
    """Handles slang term identification and translation for Chennai terms."""
    
    def __init__(self, context_parser: Optional[ProductMdParser] = None):
        """Initialize slang translator with context parser."""
        self.context_parser = context_parser or ProductMdParser()
        self._slang_terms: List[SlangTerm] = []
        self._slang_dict: Dict[str, SlangTerm] = {}
        self._load_slang_data()
    
    def _load_slang_data(self) -> None:
        """Load slang terms from context parser and build lookup dictionary."""
        self._slang_terms = self.context_parser.parse_slang_dictionary()
        self._slang_dict = {term.term.lower(): term for term in self._slang_terms}
    
    def identify_slang_terms(self, text: str) -> List[Tuple[str, int]]:
        """
        Identify all Chennai slang terms in the input text.
        
        Args:
            text: Input text to analyze for slang terms
            
        Returns:
            List of tuples containing (slang_term, position) in order of appearance
        """
        if not text:
            return []
        
        found_terms = []
        text_lower = text.lower()
        
        # Track positions to maintain order of appearance
        for slang_term in self._slang_dict.keys():
            # Find all occurrences of this slang term
            start_pos = 0
            while True:
                # Look for word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(slang_term) + r'\b'
                match = re.search(pattern, text_lower[start_pos:], re.IGNORECASE)
                
                if not match:
                    break
                
                # Calculate actual position in original text
                actual_pos = start_pos + match.start()
                found_terms.append((slang_term, actual_pos))
                
                # Move start position past this match
                start_pos = actual_pos + len(slang_term)
        
        # Sort by position to maintain order of appearance
        found_terms.sort(key=lambda x: x[1])
        
        # Remove duplicates while preserving order
        seen_terms = set()
        unique_terms = []
        for term, pos in found_terms:
            if term not in seen_terms:
                unique_terms.append((term, pos))
                seen_terms.add(term)
        
        return unique_terms
    
    def get_slang_definition(self, term: str) -> Optional[SlangTerm]:
        """
        Get comprehensive slang information for a specific term.
        
        Args:
            term: The slang term to look up
            
        Returns:
            SlangTerm object with definition, usage, and vlogger tip, or None if not found
        """
        return self._slang_dict.get(term.lower())
    
    def reload_slang_data(self) -> None:
        """Reload slang data from updated context file."""
        self.context_parser.reload_context()
        self._load_slang_data()
    
    def get_all_slang_terms(self) -> List[str]:
        """Get list of all available slang terms."""
        return list(self._slang_dict.keys())
    
    def suggest_related_terms(self, query: str) -> List[str]:
        """
        Suggest related slang terms based on partial matches or context.
        
        Args:
            query: Search query or partial term
            
        Returns:
            List of suggested slang terms
        """
        if not query:
            return []
        
        query_lower = query.lower()
        suggestions = []
        
        # Find terms that contain the query as substring
        for term in self._slang_dict.keys():
            if query_lower in term:
                suggestions.append(term)
        
        # If no substring matches, find terms with similar starting letters
        if not suggestions:
            for term in self._slang_dict.keys():
                if term.startswith(query_lower[:2]) and len(query) >= 2:
                    suggestions.append(term)
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def format_slang_response(self, terms: List[str]) -> Dict[str, any]:
        """
        Format comprehensive slang information for multiple terms.
        
        Args:
            terms: List of slang terms to format
            
        Returns:
            Formatted response with definitions, usage, and content creator tips
        """
        if not terms:
            return {
                "found_terms": [],
                "message": "No Chennai slang terms detected in your text.",
                "suggestions": self.get_popular_terms()
            }
        
        formatted_terms = []
        for term in terms:
            slang_info = self.get_slang_definition(term)
            if slang_info:
                formatted_terms.append({
                    "term": slang_info.term,
                    "definition": slang_info.definition,
                    "usage_example": slang_info.usage_example,
                    "vlogger_tip": slang_info.vlogger_tip
                })
        
        return {
            "found_terms": formatted_terms,
            "count": len(formatted_terms),
            "message": f"Found {len(formatted_terms)} Chennai slang term{'s' if len(formatted_terms) != 1 else ''} in your text!",
            "content_creator_note": "These terms will help you connect authentically with Chennai locals in your content."
        }
    
    def format_single_term_response(self, term: str) -> Dict[str, any]:
        """
        Format comprehensive information for a single slang term lookup.
        
        Args:
            term: Single slang term to format
            
        Returns:
            Detailed formatted response for the term
        """
        slang_info = self.get_slang_definition(term)
        
        if not slang_info:
            suggestions = self.suggest_related_terms(term)
            return {
                "found": False,
                "term": term,
                "message": f"'{term}' is not in our Chennai slang dictionary.",
                "suggestions": suggestions,
                "tip": "Try one of the suggested terms or browse our complete slang dictionary."
            }
        
        return {
            "found": True,
            "term": slang_info.term,
            "definition": slang_info.definition,
            "usage_example": slang_info.usage_example,
            "vlogger_tip": slang_info.vlogger_tip,
            "content_creator_note": f"Using '{slang_info.term}' authentically will help you connect with Chennai locals.",
            "pronunciation_tip": f"Practice saying '{slang_info.term}' naturally - locals appreciate the effort!"
        }
    
    def get_popular_terms(self) -> List[str]:
        """Get a list of popular/commonly used slang terms for suggestions."""
        # Return first 5 terms as popular suggestions
        # In a real implementation, this could be based on usage frequency
        popular = ["machaan", "semma", "vera level", "gethu", "thala"]
        return [term for term in popular if term in self._slang_dict]
    
    def translate_text_with_slang(self, text: str) -> Dict[str, any]:
        """
        Comprehensive slang translation for input text.
        
        Args:
            text: Input text containing potential slang terms
            
        Returns:
            Complete translation response with all found terms and formatting
        """
        # Identify slang terms in order of appearance
        found_terms_with_pos = self.identify_slang_terms(text)
        
        if not found_terms_with_pos:
            return {
                "original_text": text,
                "slang_detected": False,
                "message": "No Chennai slang detected in your text.",
                "suggestions": self.get_popular_terms(),
                "tip": "Try using some Chennai slang to connect better with locals!"
            }
        
        # Extract just the terms for formatting
        found_terms = [term for term, pos in found_terms_with_pos]
        
        # Get formatted response
        response = self.format_slang_response(found_terms)
        
        # Add original text and additional context
        response.update({
            "original_text": text,
            "slang_detected": True,
            "terms_in_order": found_terms,
            "authenticity_tip": "Using these terms naturally in your content will help you sound like a local Chennai creator!"
        })
        
        return response