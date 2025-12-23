"""Cultural guide processor for Chennai Local Guide."""

from typing import List, Dict, Optional
from datetime import datetime
from chennai_guide.models.data_models import CulturalInsight, LocalGuideResponse, SeasonalContent
from chennai_guide.parsers.context_parser import ProductMdParser


class CulturalGuideProcessor:
    """Processor for cultural context retrieval and guidance."""
    
    def __init__(self, context_parser: ProductMdParser):
        """Initialize with context parser."""
        self.context_parser = context_parser
        self._cultural_insights: List[CulturalInsight] = []
        self._seasonal_content: List[SeasonalContent] = []
        self._load_cultural_data()
        self._load_seasonal_data()
    
    def _load_cultural_data(self) -> None:
        """Load cultural insights from product.md."""
        self._cultural_insights = self.context_parser.parse_cultural_insights()
    
    def _load_seasonal_data(self) -> None:
        """Load seasonal content recommendations from product.md."""
        self._seasonal_content = self.context_parser.parse_seasonal_content()
    
    def get_cultural_guidance(self, query: str) -> LocalGuideResponse:
        """Provide cultural guidance based on query context."""
        query_lower = query.lower()
        relevant_insights = []
        
        # Keywords to match against cultural categories and content
        etiquette_keywords = ['etiquette', 'manners', 'respect', 'behavior', 'customs', 'tradition']
        filming_keywords = ['filming', 'camera', 'video', 'content', 'shoot', 'record']
        food_keywords = ['food', 'eat', 'restaurant', 'cuisine', 'meal', 'dining']
        transport_keywords = ['transport', 'travel', 'auto', 'train', 'bus', 'move', 'get around']
        authenticity_keywords = ['authentic', 'local', 'real', 'genuine', 'avoid', 'do', 'dont']
        
        # Search through cultural insights
        for insight in self._cultural_insights:
            insight_text = f"{insight.category} {insight.title} {' '.join(insight.content)} {' '.join(insight.tips)}".lower()
            
            # Check if query matches this insight
            if (any(keyword in query_lower for keyword in etiquette_keywords) and 
                any(keyword in insight_text for keyword in ['etiquette', 'respect', 'behavior'])):
                relevant_insights.append(insight)
            elif (any(keyword in query_lower for keyword in filming_keywords) and 
                  any(keyword in insight_text for keyword in ['filming', 'content', 'creator'])):
                relevant_insights.append(insight)
            elif (any(keyword in query_lower for keyword in food_keywords) and 
                  any(keyword in insight_text for keyword in ['food', 'eat', 'meal'])):
                relevant_insights.append(insight)
            elif (any(keyword in query_lower for keyword in transport_keywords) and 
                  any(keyword in insight_text for keyword in ['transport', 'auto', 'travel'])):
                relevant_insights.append(insight)
            elif (any(keyword in query_lower for keyword in authenticity_keywords) and 
                  any(keyword in insight_text for keyword in ['authentic', 'avoid', 'respect'])):
                relevant_insights.append(insight)
        
        # If no specific matches, provide general cultural tips
        if not relevant_insights:
            relevant_insights = [insight for insight in self._cultural_insights 
                               if 'authenticity' in insight.category.lower() or 
                                  'etiquette' in insight.title.lower()][:3]
        
        # Generate suggestions based on available cultural categories
        suggestions = self._generate_cultural_suggestions(query_lower)
        
        # Create content creator note
        content_creator_note = self._generate_cultural_note(relevant_insights)
        
        return LocalGuideResponse(
            query_type="cultural",
            results=relevant_insights,
            content_creator_note=content_creator_note,
            suggestions=suggestions,
            maps_links=[]
        )
    
    def get_etiquette_guidance(self) -> List[CulturalInsight]:
        """Get specific etiquette and customs guidance."""
        return [insight for insight in self._cultural_insights 
                if 'etiquette' in insight.title.lower() or 
                   'authenticity' in insight.category.lower()]
    
    def get_filming_tips(self) -> List[CulturalInsight]:
        """Get filming and content creation specific tips."""
        return [insight for insight in self._cultural_insights 
                if 'filming' in insight.title.lower() or 
                   'content' in insight.category.lower()]
    
    def get_food_culture_tips(self) -> List[CulturalInsight]:
        """Get food culture and dining etiquette tips."""
        return [insight for insight in self._cultural_insights 
                if 'food' in insight.title.lower() or 
                   'food' in insight.category.lower()]
    
    def get_transportation_culture(self) -> List[CulturalInsight]:
        """Get transportation culture and etiquette."""
        return [insight for insight in self._cultural_insights 
                if 'transport' in insight.title.lower() or 
                   'transport' in insight.category.lower()]
    
    def _generate_cultural_suggestions(self, query: str) -> List[str]:
        """Generate relevant cultural suggestions based on query."""
        suggestions = []
        
        if 'food' in query:
            suggestions.extend([
                "Learn about traditional meal etiquette",
                "Understand filter coffee culture",
                "Explore street food customs"
            ])
        elif 'filming' in query or 'content' in query:
            suggestions.extend([
                "Check temple photography rules",
                "Learn respectful filming practices",
                "Understand local consent customs"
            ])
        elif 'transport' in query:
            suggestions.extend([
                "Master auto-rickshaw etiquette",
                "Learn local train culture",
                "Understand bargaining customs"
            ])
        else:
            suggestions.extend([
                "Explore general etiquette tips",
                "Learn authentic local phrases",
                "Understand cultural do's and don'ts"
            ])
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def _generate_cultural_note(self, insights: List[CulturalInsight]) -> str:
        """Generate a content creator note based on cultural insights."""
        if not insights:
            return "Chennai has rich cultural traditions. Always show respect for local customs and ask permission when filming people or in sacred spaces."
        
        categories = [insight.category for insight in insights]
        
        if any('authenticity' in cat.lower() for cat in categories):
            return "Authenticity is key in Chennai. Locals appreciate when visitors show genuine interest in their culture and traditions."
        elif any('filming' in cat.lower() for cat in categories):
            return "When creating content in Chennai, always be respectful of local customs and ask permission before filming people closely."
        elif any('food' in cat.lower() for cat in categories):
            return "Chennai's food culture is deeply rooted in tradition. Show respect for dining customs and be open to trying authentic local experiences."
        else:
            return "Understanding local culture will make your Chennai experience more authentic and meaningful for both you and your audience."
    
    def get_seasonal_recommendations(self, query: str = "", specific_month: Optional[int] = None) -> LocalGuideResponse:
        """Get seasonal content recommendations based on current time or specific month."""
        current_month = specific_month if specific_month else datetime.now().month
        current_season = self._determine_season(current_month)
        
        # Get seasonal content for current season
        relevant_seasonal = [content for content in self._seasonal_content 
                           if content.season.lower() == current_season.lower()]
        
        # If query provided, filter by relevant keywords
        if query:
            query_lower = query.lower()
            filtered_seasonal = []
            for content in relevant_seasonal:
                content_text = f"{' '.join(content.content_ideas)} {' '.join(content.special_notes)}".lower()
                if any(keyword in content_text for keyword in query_lower.split()):
                    filtered_seasonal.append(content)
            if filtered_seasonal:
                relevant_seasonal = filtered_seasonal
        
        # Generate seasonal suggestions
        suggestions = self._generate_seasonal_suggestions(current_season, query)
        
        # Create content creator note
        content_creator_note = self._generate_seasonal_note(current_season, relevant_seasonal)
        
        return LocalGuideResponse(
            query_type="seasonal",
            results=relevant_seasonal,
            content_creator_note=content_creator_note,
            suggestions=suggestions,
            maps_links=[]
        )
    
    def get_current_season_content(self) -> List[SeasonalContent]:
        """Get content recommendations for the current season."""
        current_month = datetime.now().month
        current_season = self._determine_season(current_month)
        return [content for content in self._seasonal_content 
                if content.season.lower() == current_season.lower()]
    
    def get_weather_based_recommendations(self, weather_condition: str) -> List[SeasonalContent]:
        """Get content recommendations based on weather conditions."""
        weather_lower = weather_condition.lower()
        relevant_content = []
        
        for content in self._seasonal_content:
            content_text = f"{' '.join(content.content_ideas)} {' '.join(content.special_notes)}".lower()
            
            # Match weather conditions to seasonal content
            if weather_lower in ['hot', 'summer', 'heat'] and 'summer' in content.season.lower():
                relevant_content.append(content)
            elif weather_lower in ['rain', 'monsoon', 'wet'] and 'monsoon' in content.season.lower():
                relevant_content.append(content)
            elif weather_lower in ['cool', 'winter', 'pleasant'] and 'winter' in content.season.lower():
                relevant_content.append(content)
            elif weather_lower in ['festival', 'celebration'] and 'festival' in content.season.lower():
                relevant_content.append(content)
        
        return relevant_content
    
    def _determine_season(self, month: int) -> str:
        """Determine Chennai season based on month."""
        if month in [12, 1, 2]:  # Dec-Feb
            return "winter"
        elif month in [3, 4, 5]:  # Mar-May
            return "summer"
        elif month in [6, 7, 8, 9, 10, 11]:  # Jun-Nov
            return "monsoon"
        else:
            return "winter"  # Default fallback
    
    def _generate_seasonal_suggestions(self, season: str, query: str = "") -> List[str]:
        """Generate seasonal content suggestions."""
        suggestions = []
        
        if season == "winter":
            suggestions.extend([
                "Explore classical music season concerts",
                "Capture pleasant weather outdoor content",
                "Film Pongal festival celebrations"
            ])
        elif season == "summer":
            suggestions.extend([
                "Create early morning content to avoid heat",
                "Focus on mango season experiences",
                "Film indoor cultural attractions"
            ])
        elif season == "monsoon":
            suggestions.extend([
                "Capture dramatic rain content",
                "Explore bajji and tea culture",
                "Film cozy indoor food experiences"
            ])
        
        # Add query-specific suggestions
        if query:
            query_lower = query.lower()
            if 'food' in query_lower:
                suggestions.append(f"Try seasonal {season} food specialties")
            elif 'festival' in query_lower:
                suggestions.append(f"Look for {season} festival celebrations")
            elif 'outdoor' in query_lower and season != 'summer':
                suggestions.append(f"Perfect {season} weather for outdoor shoots")
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def _generate_seasonal_note(self, season: str, seasonal_content: List[SeasonalContent]) -> str:
        """Generate content creator note for seasonal recommendations."""
        if not seasonal_content:
            return f"Chennai's {season} season offers unique content opportunities. Check local events and weather patterns for best filming times."
        
        if season == "winter":
            return "Winter is Chennai's golden season for content creation - pleasant weather and rich cultural events make it perfect for outdoor filming."
        elif season == "summer":
            return "Summer in Chennai requires strategic timing - early mornings and late evenings are best, but indoor cultural content thrives."
        elif season == "monsoon":
            return "Monsoon season brings dramatic visuals and cozy indoor culture - perfect for food content and cultural immersion."
        else:
            return f"The {season} season in Chennai offers unique content creation opportunities with distinct local experiences."

    def reload_cultural_data(self) -> None:
        """Reload cultural data from updated product.md."""
        self.context_parser.reload_context()
        self._load_cultural_data()
        self._load_seasonal_data()