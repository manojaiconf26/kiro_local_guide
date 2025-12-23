"""Discovery and browsing interface for Chennai cultural content."""

from typing import List, Dict, Optional, Set, Any
from dataclasses import dataclass
from chennai_guide.models.data_models import (
    SlangTerm, Neighborhood, CulturalInsight, SeasonalContent, LocalGuideResponse
)
from chennai_guide.parsers.context_parser import ProductMdParser


@dataclass
class BrowsingCategory:
    """Represents a browsable category of Chennai cultural content."""
    name: str
    description: str
    items: List[Any]
    tags: List[str]
    content_types: List[str]


@dataclass
class BrowsingFilter:
    """Filter criteria for browsing cultural content."""
    content_types: List[str] = None
    tags: List[str] = None
    categories: List[str] = None
    season: Optional[str] = None


class CulturalDiscoveryBrowser:
    """Browser interface for organized access to Chennai cultural categories."""
    
    def __init__(self, context_parser: ProductMdParser):
        """Initialize browser with context parser."""
        self.context_parser = context_parser
        self._slang_terms: List[SlangTerm] = []
        self._neighborhoods: List[Neighborhood] = []
        self._cultural_insights: List[CulturalInsight] = []
        self._seasonal_content: List[SeasonalContent] = []
        self._categories: Dict[str, BrowsingCategory] = {}
        self._load_all_data()
        self._organize_categories()
    
    def _load_all_data(self) -> None:
        """Load all cultural data from product.md."""
        self._slang_terms = self.context_parser.parse_slang_dictionary()
        self._neighborhoods = self.context_parser.parse_neighborhoods()
        self._cultural_insights = self.context_parser.parse_cultural_insights()
        self._seasonal_content = self.context_parser.parse_seasonal_content()
    
    def _organize_categories(self) -> None:
        """Organize all content into browsable categories."""
        # Slang categories
        self._categories['slang'] = BrowsingCategory(
            name="Chennai Slang & Local Language",
            description="Essential Tamil slang terms for authentic content creation",
            items=self._slang_terms,
            tags=['language', 'communication', 'authentic', 'local'],
            content_types=['cultural', 'educational', 'social']
        )
        
        # Neighborhood categories by content type
        food_neighborhoods = [n for n in self._neighborhoods 
                            if any('food' in tag.lower() for tag in n.content_tags)]
        cultural_neighborhoods = [n for n in self._neighborhoods 
                                if any(tag in ['cultural', 'traditional', 'spiritual'] 
                                      for tag in n.content_tags)]
        scenic_neighborhoods = [n for n in self._neighborhoods 
                              if any(tag in ['scenic', 'beach', 'nature'] 
                                    for tag in n.content_tags)]
        trendy_neighborhoods = [n for n in self._neighborhoods 
                              if any(tag in ['trendy', 'modern', 'cafe'] 
                                    for tag in n.content_tags)]
        
        self._categories['food_spots'] = BrowsingCategory(
            name="Food & Dining Neighborhoods",
            description="Best areas for food content, street food tours, and culinary experiences",
            items=food_neighborhoods,
            tags=['food', 'dining', 'street food', 'culinary'],
            content_types=['food', 'lifestyle', 'cultural']
        )
        
        self._categories['cultural_areas'] = BrowsingCategory(
            name="Cultural & Heritage Areas",
            description="Traditional neighborhoods for cultural immersion and heritage content",
            items=cultural_neighborhoods,
            tags=['cultural', 'heritage', 'traditional', 'spiritual', 'temples'],
            content_types=['cultural', 'educational', 'spiritual']
        )
        
        self._categories['scenic_locations'] = BrowsingCategory(
            name="Scenic & Photography Spots",
            description="Beautiful locations perfect for visual content and photography",
            items=scenic_neighborhoods,
            tags=['scenic', 'photography', 'beautiful', 'nature', 'beach'],
            content_types=['scenic', 'photography', 'lifestyle']
        )
        
        self._categories['trendy_areas'] = BrowsingCategory(
            name="Modern & Trendy Areas",
            description="Contemporary Chennai with cafes, modern lifestyle, and young culture",
            items=trendy_neighborhoods,
            tags=['trendy', 'modern', 'cafe', 'young', 'contemporary'],
            content_types=['lifestyle', 'modern', 'social']
        )
        
        # Cultural insights categories
        etiquette_insights = [i for i in self._cultural_insights 
                            if 'etiquette' in i.title.lower() or 'authenticity' in i.category.lower()]
        filming_insights = [i for i in self._cultural_insights 
                          if 'filming' in i.title.lower() or 'content' in i.category.lower()]
        food_insights = [i for i in self._cultural_insights 
                       if 'food' in i.title.lower() or 'food' in i.category.lower()]
        transport_insights = [i for i in self._cultural_insights 
                            if 'transport' in i.title.lower()]
        
        self._categories['etiquette_tips'] = BrowsingCategory(
            name="Cultural Etiquette & Authenticity",
            description="Essential do's and don'ts for respectful and authentic content creation",
            items=etiquette_insights,
            tags=['etiquette', 'respect', 'authenticity', 'customs', 'behavior'],
            content_types=['educational', 'cultural', 'social']
        )
        
        self._categories['filming_guidance'] = BrowsingCategory(
            name="Content Creation & Filming Tips",
            description="Professional guidance for creating authentic Chennai content",
            items=filming_insights,
            tags=['filming', 'content', 'tips', 'professional', 'creation'],
            content_types=['educational', 'professional', 'technical']
        )
        
        self._categories['food_culture'] = BrowsingCategory(
            name="Food Culture & Dining Customs",
            description="Understanding Chennai's rich food culture and dining traditions",
            items=food_insights,
            tags=['food', 'culture', 'dining', 'traditions', 'customs'],
            content_types=['food', 'cultural', 'educational']
        )
        
        self._categories['transport_culture'] = BrowsingCategory(
            name="Transportation & Getting Around",
            description="Local transportation culture, etiquette, and practical tips",
            items=transport_insights,
            tags=['transport', 'travel', 'local', 'practical', 'navigation'],
            content_types=['practical', 'educational', 'lifestyle']
        )
        
        # Seasonal content categories
        self._categories['seasonal_ideas'] = BrowsingCategory(
            name="Seasonal Content Opportunities",
            description="Time-specific content ideas based on Chennai's seasons and festivals",
            items=self._seasonal_content,
            tags=['seasonal', 'festivals', 'weather', 'timing', 'opportunities'],
            content_types=['seasonal', 'cultural', 'educational']
        )
    
    def get_all_categories(self) -> Dict[str, BrowsingCategory]:
        """Get all available browsing categories."""
        return self._categories
    
    def get_category_names(self) -> List[str]:
        """Get list of all category names."""
        return list(self._categories.keys())
    
    def get_category(self, category_name: str) -> Optional[BrowsingCategory]:
        """Get specific category by name."""
        return self._categories.get(category_name)
    
    def browse_by_content_type(self, content_types: List[str]) -> Dict[str, BrowsingCategory]:
        """Filter categories by content type preferences."""
        filtered_categories = {}
        
        for cat_name, category in self._categories.items():
            # Check if category supports any of the requested content types
            if any(ct in category.content_types for ct in content_types):
                # Filter items within category if applicable
                if cat_name in ['food_spots', 'cultural_areas', 'scenic_locations', 'trendy_areas']:
                    # For neighborhood categories, filter by content tags
                    filtered_items = []
                    for item in category.items:
                        if hasattr(item, 'content_tags'):
                            if any(ct in item.content_tags for ct in content_types):
                                filtered_items.append(item)
                        else:
                            filtered_items.append(item)  # Include if no tags to filter by
                    
                    if filtered_items:
                        filtered_category = BrowsingCategory(
                            name=category.name,
                            description=category.description,
                            items=filtered_items,
                            tags=category.tags,
                            content_types=category.content_types
                        )
                        filtered_categories[cat_name] = filtered_category
                else:
                    # For other categories, include the whole category
                    filtered_categories[cat_name] = category
        
        return filtered_categories
    
    def browse_by_tags(self, tags: List[str]) -> Dict[str, BrowsingCategory]:
        """Filter categories by tags."""
        filtered_categories = {}
        
        for cat_name, category in self._categories.items():
            # Check if category has any of the requested tags
            if any(tag.lower() in [t.lower() for t in category.tags] for tag in tags):
                filtered_categories[cat_name] = category
        
        return filtered_categories
    
    def browse_with_filter(self, filter_criteria: BrowsingFilter) -> Dict[str, BrowsingCategory]:
        """Apply comprehensive filtering to categories."""
        filtered_categories = self._categories.copy()
        
        # Filter by content types
        if filter_criteria.content_types:
            filtered_categories = self.browse_by_content_type(filter_criteria.content_types)
        
        # Further filter by tags
        if filter_criteria.tags:
            tag_filtered = self.browse_by_tags(filter_criteria.tags)
            # Intersect with existing filtered categories
            filtered_categories = {
                name: cat for name, cat in filtered_categories.items() 
                if name in tag_filtered
            }
        
        # Filter by specific categories
        if filter_criteria.categories:
            filtered_categories = {
                name: cat for name, cat in filtered_categories.items() 
                if name in filter_criteria.categories
            }
        
        # Filter seasonal content by season
        if filter_criteria.season and 'seasonal_ideas' in filtered_categories:
            seasonal_category = filtered_categories['seasonal_ideas']
            filtered_seasonal_items = [
                item for item in seasonal_category.items 
                if hasattr(item, 'season') and item.season.lower() == filter_criteria.season.lower()
            ]
            
            if filtered_seasonal_items:
                filtered_categories['seasonal_ideas'] = BrowsingCategory(
                    name=seasonal_category.name,
                    description=f"{filter_criteria.season.title()} season content opportunities",
                    items=filtered_seasonal_items,
                    tags=seasonal_category.tags,
                    content_types=seasonal_category.content_types
                )
            else:
                # Remove seasonal category if no items match
                del filtered_categories['seasonal_ideas']
        
        return filtered_categories
    
    def get_available_content_types(self) -> List[str]:
        """Get all available content types across categories."""
        content_types = set()
        for category in self._categories.values():
            content_types.update(category.content_types)
        return sorted(list(content_types))
    
    def get_available_tags(self) -> List[str]:
        """Get all available tags across categories."""
        tags = set()
        for category in self._categories.values():
            tags.update(category.tags)
        return sorted(list(tags))
    
    def search_across_categories(self, search_term: str) -> Dict[str, List[Any]]:
        """Search for content across all categories."""
        search_lower = search_term.lower()
        results = {}
        
        for cat_name, category in self._categories.items():
            matching_items = []
            
            for item in category.items:
                # Search in different item types
                if isinstance(item, SlangTerm):
                    if (search_lower in item.term.lower() or 
                        search_lower in item.definition.lower() or
                        search_lower in item.usage_example.lower()):
                        matching_items.append(item)
                
                elif isinstance(item, Neighborhood):
                    if (search_lower in item.name.lower() or 
                        search_lower in item.vibe.lower() or
                        any(search_lower in content.lower() for content in item.best_for_content) or
                        any(search_lower in tag.lower() for tag in item.content_tags)):
                        matching_items.append(item)
                
                elif isinstance(item, CulturalInsight):
                    if (search_lower in item.title.lower() or 
                        search_lower in item.category.lower() or
                        any(search_lower in content.lower() for content in item.content) or
                        any(search_lower in tip.lower() for tip in item.tips)):
                        matching_items.append(item)
                
                elif isinstance(item, SeasonalContent):
                    if (search_lower in item.season.lower() or
                        any(search_lower in idea.lower() for idea in item.content_ideas) or
                        any(search_lower in note.lower() for note in item.special_notes)):
                        matching_items.append(item)
            
            if matching_items:
                results[cat_name] = matching_items
        
        return results
    
    def get_category_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary statistics for all categories."""
        summary = {}
        
        for cat_name, category in self._categories.items():
            summary[cat_name] = {
                'name': category.name,
                'description': category.description,
                'item_count': len(category.items),
                'tags': category.tags,
                'content_types': category.content_types
            }
        
        return summary
    
    def reload_data(self) -> None:
        """Reload all data from updated product.md."""
        self.context_parser.reload_context()
        self._load_all_data()
        self._organize_categories()