"""Content inspiration engine for Chennai Local Guide."""

import random
from typing import List, Dict, Optional, Set, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from chennai_guide.models.data_models import (
    SlangTerm, Neighborhood, CulturalInsight, SeasonalContent, LocalGuideResponse
)
from chennai_guide.parsers.context_parser import ProductMdParser


@dataclass
class ContentIdea:
    """Represents a content creation idea."""
    title: str
    description: str
    category: str
    content_type: str
    location_suggestions: List[str]
    slang_to_use: List[str]
    timing_tips: List[str]
    difficulty: str  # 'beginner', 'intermediate', 'advanced'
    estimated_duration: str
    tags: List[str]


@dataclass
class TrendingTopic:
    """Represents a trending content topic."""
    topic: str
    description: str
    why_trending: str
    content_angles: List[str]
    best_locations: List[str]
    seasonal_relevance: Optional[str]


class ContentInspirationEngine:
    """Engine for generating diverse content suggestions and trending topics."""
    
    def __init__(self, context_parser: ProductMdParser):
        """Initialize inspiration engine with context parser."""
        self.context_parser = context_parser
        self._slang_terms: List[SlangTerm] = []
        self._neighborhoods: List[Neighborhood] = []
        self._cultural_insights: List[CulturalInsight] = []
        self._seasonal_content: List[SeasonalContent] = []
        self._content_ideas: List[ContentIdea] = []
        self._trending_topics: List[TrendingTopic] = []
        self._load_all_data()
        self._generate_content_ideas()
        self._generate_trending_topics()
    
    def _load_all_data(self) -> None:
        """Load all cultural data from product.md."""
        self._slang_terms = self.context_parser.parse_slang_dictionary()
        self._neighborhoods = self.context_parser.parse_neighborhoods()
        self._cultural_insights = self.context_parser.parse_cultural_insights()
        self._seasonal_content = self.context_parser.parse_seasonal_content()
    
    def _generate_content_ideas(self) -> None:
        """Generate diverse content creation ideas based on available data."""
        self._content_ideas = []
        
        # Food content ideas
        food_neighborhoods = [n for n in self._neighborhoods 
                            if any('food' in tag.lower() for tag in n.content_tags)]
        food_slang = [s for s in self._slang_terms 
                     if 'food' in s.definition.lower() or 'eat' in s.definition.lower()]
        
        self._content_ideas.extend([
            ContentIdea(
                title="Chennai Street Food Challenge",
                description="Try authentic Chennai street food while learning local food slang",
                category="food",
                content_type="challenge",
                location_suggestions=[n.name for n in food_neighborhoods[:3]],
                slang_to_use=[s.term for s in food_slang[:3]] + ['semma', 'vera level'],
                timing_tips=["Lunch time (12-2pm) for authentic food culture", "Evening (5-7pm) for street food energy"],
                difficulty="beginner",
                estimated_duration="2-3 hours",
                tags=["food", "street food", "challenge", "authentic", "local"]
            ),
            ContentIdea(
                title="Filter Coffee Culture Deep Dive",
                description="Explore Chennai's iconic filter coffee culture and traditions",
                category="food",
                content_type="educational",
                location_suggestions=["T. Nagar", "Mylapore", "Adyar"],
                slang_to_use=["thala", "semma", "machaan"],
                timing_tips=["Morning (7-10am) for traditional coffee culture", "Afternoon (3-5pm) for cafe culture"],
                difficulty="intermediate",
                estimated_duration="1-2 hours",
                tags=["coffee", "culture", "traditional", "educational", "morning"]
            )
        ])
        
        # Cultural content ideas
        cultural_neighborhoods = [n for n in self._neighborhoods 
                                if any(tag in ['cultural', 'traditional', 'spiritual'] 
                                      for tag in n.content_tags)]
        
        self._content_ideas.extend([
            ContentIdea(
                title="Temple Architecture Storytelling",
                description="Showcase Chennai's stunning temple architecture with cultural context",
                category="cultural",
                content_type="educational",
                location_suggestions=[n.name for n in cultural_neighborhoods[:3]],
                slang_to_use=["vera level", "gethu", "thala"],
                timing_tips=["Early morning (6-8am) for peaceful temple visits", "Festival seasons for vibrant content"],
                difficulty="intermediate",
                estimated_duration="3-4 hours",
                tags=["temples", "architecture", "cultural", "spiritual", "heritage"]
            ),
            ContentIdea(
                title="Local Slang Integration Challenge",
                description="Create content naturally incorporating Chennai slang in conversations",
                category="cultural",
                content_type="challenge",
                location_suggestions=["Marina Beach Area", "T. Nagar", "Besant Nagar"],
                slang_to_use=[s.term for s in self._slang_terms[:5]],
                timing_tips=["Evening (5-8pm) for maximum local activity", "Weekend for casual interactions"],
                difficulty="advanced",
                estimated_duration="4-6 hours",
                tags=["slang", "language", "interaction", "challenge", "social"]
            )
        ])
        
        # Scenic content ideas
        scenic_neighborhoods = [n for n in self._neighborhoods 
                              if any(tag in ['scenic', 'beach', 'nature'] 
                                    for tag in n.content_tags)]
        
        self._content_ideas.extend([
            ContentIdea(
                title="Chennai Sunrise/Sunset Series",
                description="Capture Chennai's beautiful golden hours at iconic locations",
                category="scenic",
                content_type="photography",
                location_suggestions=[n.name for n in scenic_neighborhoods],
                slang_to_use=["semma", "vera level", "gethu"],
                timing_tips=["Golden hour (6-7:30am and 5:30-7pm)", "Avoid midday heat"],
                difficulty="beginner",
                estimated_duration="2-3 hours",
                tags=["photography", "scenic", "golden hour", "beautiful", "nature"]
            )
        ])
        
        # Lifestyle content ideas
        trendy_neighborhoods = [n for n in self._neighborhoods 
                              if any(tag in ['trendy', 'modern', 'cafe'] 
                                    for tag in n.content_tags)]
        
        self._content_ideas.extend([
            ContentIdea(
                title="Modern Chennai Lifestyle Tour",
                description="Explore contemporary Chennai culture, cafes, and young lifestyle",
                category="lifestyle",
                content_type="lifestyle",
                location_suggestions=[n.name for n in trendy_neighborhoods],
                slang_to_use=["scene", "gethu", "semma"],
                timing_tips=["Weekend mornings for cafe culture", "Evenings for social scenes"],
                difficulty="beginner",
                estimated_duration="3-4 hours",
                tags=["modern", "lifestyle", "cafes", "young", "contemporary"]
            )
        ])
        
        # Seasonal content ideas based on current season
        current_season = self._determine_current_season()
        seasonal_ideas = self._generate_seasonal_content_ideas(current_season)
        self._content_ideas.extend(seasonal_ideas)
    
    def _generate_seasonal_content_ideas(self, season: str) -> List[ContentIdea]:
        """Generate season-specific content ideas."""
        seasonal_ideas = []
        
        if season == "winter":
            seasonal_ideas.extend([
                ContentIdea(
                    title="Chennai Music Season Experience",
                    description="Immerse in Chennai's classical music season with cultural insights",
                    category="cultural",
                    content_type="cultural",
                    location_suggestions=["Mylapore", "T. Nagar"],
                    slang_to_use=["gethu", "vera level", "semma"],
                    timing_tips=["December-January for music season", "Evening concerts for best atmosphere"],
                    difficulty="intermediate",
                    estimated_duration="4-5 hours",
                    tags=["music", "classical", "cultural", "winter", "festivals"]
                ),
                ContentIdea(
                    title="Pleasant Weather Outdoor Adventures",
                    description="Take advantage of Chennai's best weather for outdoor content",
                    category="scenic",
                    content_type="adventure",
                    location_suggestions=["Marina Beach Area", "Adyar", "Besant Nagar"],
                    slang_to_use=["semma", "vera level", "machaan"],
                    timing_tips=["All day outdoor shooting possible", "Perfect for long-form content"],
                    difficulty="beginner",
                    estimated_duration="6-8 hours",
                    tags=["outdoor", "weather", "adventure", "winter", "pleasant"]
                )
            ])
        elif season == "summer":
            seasonal_ideas.extend([
                ContentIdea(
                    title="Beat the Heat: Indoor Chennai Culture",
                    description="Explore Chennai's indoor cultural attractions during hot season",
                    category="cultural",
                    content_type="educational",
                    location_suggestions=["Mylapore", "T. Nagar"],
                    slang_to_use=["vera level", "semma", "mokka"],
                    timing_tips=["Early morning (6-9am)", "Late evening (6-8pm)", "Indoor locations preferred"],
                    difficulty="intermediate",
                    estimated_duration="3-4 hours",
                    tags=["indoor", "culture", "summer", "heat", "museums"]
                ),
                ContentIdea(
                    title="Mango Season Special",
                    description="Celebrate Chennai's mango season with local varieties and culture",
                    category="food",
                    content_type="seasonal",
                    location_suggestions=["T. Nagar", "Royapettah"],
                    slang_to_use=["semma", "vera level", "gethu"],
                    timing_tips=["March-May for mango season", "Morning markets for best selection"],
                    difficulty="beginner",
                    estimated_duration="2-3 hours",
                    tags=["mango", "seasonal", "summer", "food", "markets"]
                )
            ])
        elif season == "monsoon":
            seasonal_ideas.extend([
                ContentIdea(
                    title="Monsoon Mood: Cozy Chennai",
                    description="Capture Chennai's monsoon atmosphere with food and indoor culture",
                    category="lifestyle",
                    content_type="atmospheric",
                    location_suggestions=["T. Nagar", "Mylapore", "Besant Nagar"],
                    slang_to_use=["semma", "scene", "apdiye"],
                    timing_tips=["Rainy days for dramatic content", "Indoor locations for comfort"],
                    difficulty="intermediate",
                    estimated_duration="3-4 hours",
                    tags=["monsoon", "rain", "cozy", "atmospheric", "indoor"]
                )
            ])
        
        return seasonal_ideas
    
    def _generate_trending_topics(self) -> None:
        """Generate trending content topics based on current context."""
        self._trending_topics = [
            TrendingTopic(
                topic="Authentic Local Language Integration",
                description="Content creators are focusing on naturally incorporating local slang",
                why_trending="Audiences appreciate authentic cultural representation",
                content_angles=[
                    "Learning slang through local interactions",
                    "Slang translation and cultural context",
                    "Using slang in different social situations"
                ],
                best_locations=["Marina Beach Area", "T. Nagar", "Besant Nagar"],
                seasonal_relevance=None
            ),
            TrendingTopic(
                topic="Heritage vs Modern Chennai",
                description="Contrasting traditional and contemporary aspects of the city",
                why_trending="Shows the dynamic nature of Chennai's cultural evolution",
                content_angles=[
                    "Traditional temples vs modern cafes",
                    "Classical music vs contemporary culture",
                    "Street food vs upscale dining"
                ],
                best_locations=["Mylapore", "Besant Nagar", "T. Nagar"],
                seasonal_relevance=None
            ),
            TrendingTopic(
                topic="Food Culture Deep Dives",
                description="Exploring the stories and traditions behind Chennai's food",
                why_trending="Food content performs well and Chennai has rich culinary heritage",
                content_angles=[
                    "Filter coffee culture and traditions",
                    "Street food vendor stories",
                    "Traditional cooking methods"
                ],
                best_locations=["T. Nagar", "Royapettah", "Mylapore"],
                seasonal_relevance=None
            )
        ]
        
        # Add seasonal trending topics
        current_season = self._determine_current_season()
        seasonal_trending = self._generate_seasonal_trending_topics(current_season)
        self._trending_topics.extend(seasonal_trending)
    
    def _generate_seasonal_trending_topics(self, season: str) -> List[TrendingTopic]:
        """Generate season-specific trending topics."""
        seasonal_trending = []
        
        if season == "winter":
            seasonal_trending.append(
                TrendingTopic(
                    topic="Chennai Music Season Coverage",
                    description="Classical music and dance performances during peak season",
                    why_trending="December-January is Chennai's premier cultural season",
                    content_angles=[
                        "Behind-the-scenes at classical concerts",
                        "Learning about Carnatic music",
                        "Festival atmosphere and cultural immersion"
                    ],
                    best_locations=["Mylapore", "T. Nagar"],
                    seasonal_relevance="winter"
                )
            )
        elif season == "summer":
            seasonal_trending.append(
                TrendingTopic(
                    topic="Summer Survival in Chennai",
                    description="How locals cope with and enjoy the hot season",
                    why_trending="Relatable content about dealing with Chennai's heat",
                    content_angles=[
                        "Local cooling traditions and foods",
                        "Early morning and late evening activities",
                        "Indoor cultural experiences"
                    ],
                    best_locations=["Marina Beach Area", "Adyar", "Indoor locations"],
                    seasonal_relevance="summer"
                )
            )
        elif season == "monsoon":
            seasonal_trending.append(
                TrendingTopic(
                    topic="Monsoon Vibes and Food Culture",
                    description="Chennai's cozy monsoon atmosphere and comfort food",
                    why_trending="Monsoon creates unique atmospheric content opportunities",
                    content_angles=[
                        "Rainy day food culture",
                        "Cozy indoor experiences",
                        "Dramatic weather visuals"
                    ],
                    best_locations=["T. Nagar", "Besant Nagar", "Covered areas"],
                    seasonal_relevance="monsoon"
                )
            )
        
        return seasonal_trending
    
    def get_content_inspiration(self, preferences: Optional[Dict[str, Any]] = None) -> LocalGuideResponse:
        """Get personalized content inspiration based on preferences."""
        if not preferences:
            preferences = {}
        
        # Filter content ideas based on preferences
        filtered_ideas = self._filter_content_ideas(preferences)
        
        # Get trending topics
        relevant_trending = self._filter_trending_topics(preferences)
        
        # Generate suggestions
        suggestions = self._generate_inspiration_suggestions(preferences)
        
        # Create content creator note
        content_creator_note = self._generate_inspiration_note(filtered_ideas, relevant_trending)
        
        return LocalGuideResponse(
            query_type="inspiration",
            results={
                'content_ideas': filtered_ideas[:5],  # Top 5 ideas
                'trending_topics': relevant_trending[:3],  # Top 3 trending
                'quick_suggestions': suggestions
            },
            content_creator_note=content_creator_note,
            suggestions=suggestions,
            maps_links=[]
        )
    
    def get_random_inspiration(self, count: int = 3) -> List[ContentIdea]:
        """Get random content inspiration ideas."""
        return random.sample(self._content_ideas, min(count, len(self._content_ideas)))
    
    def get_trending_topics(self, count: int = 5) -> List[TrendingTopic]:
        """Get current trending topics."""
        return self._trending_topics[:count]
    
    def get_seasonal_inspiration(self, season: Optional[str] = None) -> List[ContentIdea]:
        """Get season-specific content inspiration."""
        if not season:
            season = self._determine_current_season()
        
        return [idea for idea in self._content_ideas 
                if season.lower() in [tag.lower() for tag in idea.tags]]
    
    def get_inspiration_by_category(self, category: str) -> List[ContentIdea]:
        """Get content inspiration filtered by category."""
        return [idea for idea in self._content_ideas 
                if idea.category.lower() == category.lower()]
    
    def get_inspiration_by_difficulty(self, difficulty: str) -> List[ContentIdea]:
        """Get content inspiration filtered by difficulty level."""
        return [idea for idea in self._content_ideas 
                if idea.difficulty.lower() == difficulty.lower()]
    
    def _filter_content_ideas(self, preferences: Dict[str, Any]) -> List[ContentIdea]:
        """Filter content ideas based on user preferences."""
        filtered_ideas = self._content_ideas.copy()
        
        # Filter by category
        if 'categories' in preferences and preferences['categories']:
            filtered_ideas = [idea for idea in filtered_ideas 
                            if idea.category in preferences['categories']]
        
        # Filter by content type
        if 'content_types' in preferences and preferences['content_types']:
            filtered_ideas = [idea for idea in filtered_ideas 
                            if idea.content_type in preferences['content_types']]
        
        # Filter by difficulty
        if 'difficulty' in preferences and preferences['difficulty']:
            filtered_ideas = [idea for idea in filtered_ideas 
                            if idea.difficulty == preferences['difficulty']]
        
        # Filter by tags
        if 'tags' in preferences and preferences['tags']:
            filtered_ideas = [idea for idea in filtered_ideas 
                            if any(tag in idea.tags for tag in preferences['tags'])]
        
        # Sort by relevance (random for now, could be improved with scoring)
        random.shuffle(filtered_ideas)
        
        return filtered_ideas
    
    def _filter_trending_topics(self, preferences: Dict[str, Any]) -> List[TrendingTopic]:
        """Filter trending topics based on preferences."""
        filtered_trending = self._trending_topics.copy()
        
        # Filter by seasonal relevance
        current_season = self._determine_current_season()
        if 'include_seasonal' in preferences and preferences['include_seasonal']:
            # Include both seasonal and non-seasonal
            pass
        else:
            # Include current season and non-seasonal
            filtered_trending = [topic for topic in filtered_trending 
                               if not topic.seasonal_relevance or 
                                  topic.seasonal_relevance == current_season]
        
        return filtered_trending
    
    def _generate_inspiration_suggestions(self, preferences: Dict[str, Any]) -> List[str]:
        """Generate quick inspiration suggestions."""
        suggestions = []
        current_season = self._determine_current_season()
        
        # Season-based suggestions
        if current_season == "winter":
            suggestions.extend([
                "Explore Chennai's classical music season",
                "Take advantage of pleasant weather for outdoor content",
                "Capture Pongal festival celebrations"
            ])
        elif current_season == "summer":
            suggestions.extend([
                "Focus on early morning and late evening content",
                "Explore indoor cultural attractions",
                "Create mango season special content"
            ])
        elif current_season == "monsoon":
            suggestions.extend([
                "Capture dramatic monsoon atmosphere",
                "Explore cozy indoor food culture",
                "Create rain-themed lifestyle content"
            ])
        
        # General suggestions
        suggestions.extend([
            "Learn and use local Chennai slang naturally",
            "Contrast traditional and modern aspects of the city",
            "Explore neighborhood-specific food cultures"
        ])
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _generate_inspiration_note(self, ideas: List[ContentIdea], trending: List[TrendingTopic]) -> str:
        """Generate content creator note for inspiration."""
        if not ideas and not trending:
            return "Chennai offers endless content opportunities. Explore local culture, learn the language, and connect with the community for authentic content."
        
        current_season = self._determine_current_season()
        
        if current_season == "winter":
            return "Winter is Chennai's golden season for content creation. Take advantage of pleasant weather and rich cultural events like the music season."
        elif current_season == "summer":
            return "Summer in Chennai requires strategic timing, but offers unique opportunities like mango season and indoor cultural experiences."
        elif current_season == "monsoon":
            return "Monsoon season brings dramatic visuals and cozy indoor culture - perfect for atmospheric content and food experiences."
        else:
            return "Chennai's diverse culture offers year-round content opportunities. Focus on authenticity and local connections for the best results."
    
    def _determine_current_season(self) -> str:
        """Determine current Chennai season based on month."""
        current_month = datetime.now().month
        
        if current_month in [12, 1, 2]:  # Dec-Feb
            return "winter"
        elif current_month in [3, 4, 5]:  # Mar-May
            return "summer"
        elif current_month in [6, 7, 8, 9, 10, 11]:  # Jun-Nov
            return "monsoon"
        else:
            return "winter"  # Default fallback
    
    def reload_data(self) -> None:
        """Reload all data and regenerate content ideas."""
        self.context_parser.reload_context()
        self._load_all_data()
        self._generate_content_ideas()
        self._generate_trending_topics()