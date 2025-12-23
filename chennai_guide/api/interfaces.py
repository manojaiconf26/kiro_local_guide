"""Interface definitions for query processing and response generation."""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any
from chennai_guide.models.data_models import SlangTerm, Neighborhood, LocalGuideResponse


class QueryProcessorInterface(ABC):
    """Interface for analyzing user input and determining query intent."""
    
    @abstractmethod
    def analyze_intent(self, query: str) -> str:
        """Determine if query is about slang translation or neighborhood recommendations."""
        pass
    
    @abstractmethod
    def extract_keywords(self, query: str) -> List[str]:
        """Identify relevant terms and content type preferences."""
        pass
    
    @abstractmethod
    def route_query(self, intent: str, keywords: List[str]) -> str:
        """Direct to slang translator or neighborhood recommender."""
        pass


class SlangTranslatorInterface(ABC):
    """Interface for Chennai slang translation and context provision."""
    
    @abstractmethod
    def identify_slang_terms(self, text: str) -> List[str]:
        """Find all Chennai slang in input text."""
        pass
    
    @abstractmethod
    def get_slang_definition(self, term: str) -> SlangTerm:
        """Return definition, usage example, and content creator tips from product.md."""
        pass
    
    @abstractmethod
    def format_slang_response(self, terms: List[SlangTerm]) -> LocalGuideResponse:
        """Organize multiple slang results for presentation."""
        pass


class NeighborhoodRecommenderInterface(ABC):
    """Interface for content-type aware Chennai neighborhood suggestions."""
    
    @abstractmethod
    def score_neighborhoods(self, content_preferences: List[str]) -> List[Tuple[Neighborhood, float]]:
        """Rank neighborhoods by relevance to content type."""
        pass
    
    @abstractmethod
    def get_neighborhood_profile(self, name: str) -> Neighborhood:
        """Return detailed neighborhood information with Google Maps links from product.md."""
        pass
    
    @abstractmethod
    def generate_maps_link(self, neighborhood: Neighborhood) -> str:
        """Create Google Maps URLs for neighborhood locations."""
        pass
    
    @abstractmethod
    def match_content_type(self, query: str) -> List[str]:
        """Identify content preferences from natural language."""
        pass