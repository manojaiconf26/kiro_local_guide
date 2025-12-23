"""Core data models for Chennai Local Guide."""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SlangTerm:
    """Represents a Chennai slang term with its definition and usage context."""
    term: str
    definition: str
    usage_example: str
    vlogger_tip: str


@dataclass
class Neighborhood:
    """Represents a Chennai neighborhood with content creation information."""
    name: str
    vibe: str
    best_for_content: List[str]
    insider_tips: List[str]
    content_tags: List[str]  # food, art, nightlife, scenic, etc.
    google_maps_link: str  # Direct link to Google Maps location
    coordinates: Dict[str, float]  # lat, lng for mapping


@dataclass
class CulturalInsight:
    """Represents cultural tips, etiquette, and local customs."""
    category: str  # filming_etiquette, local_phrases, transportation, etc.
    title: str
    content: List[str]
    tips: List[str]


@dataclass
class SeasonalContent:
    """Represents seasonal content recommendations and ideas."""
    season: str  # winter, summer, monsoon, festival_seasons
    period: str  # time period like "Dec-Feb"
    content_ideas: List[str]
    special_notes: List[str]


@dataclass
class LocalGuideResponse:
    """Response object containing results from Chennai Local Guide queries."""
    query_type: str  # "slang" or "neighborhood"
    results: List[Any]  # SlangTerm or Neighborhood objects
    content_creator_note: str
    suggestions: List[str]
    maps_links: List[str]  # Google Maps links for neighborhoods