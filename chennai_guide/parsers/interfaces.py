"""Interface definitions for context parsers."""

from abc import ABC, abstractmethod
from typing import List, Dict
from chennai_guide.models.data_models import SlangTerm, Neighborhood


class ContextParserInterface(ABC):
    """Interface for parsing context data from product.md file."""
    
    @abstractmethod
    def parse_slang_dictionary(self) -> List[SlangTerm]:
        """Extract Chennai slang terms with definitions, usage examples, and content creator tips."""
        pass
    
    @abstractmethod
    def parse_neighborhoods(self) -> List[Neighborhood]:
        """Extract Chennai neighborhood profiles with vibes, content suitability, and Google Maps coordinates."""
        pass
    
    @abstractmethod
    def reload_context(self) -> None:
        """Refresh data from updated product.md file."""
        pass
    
    @abstractmethod
    def extract_maps_data(self) -> Dict[str, Dict[str, float]]:
        """Parse Google Maps links and location coordinates from product.md."""
        pass