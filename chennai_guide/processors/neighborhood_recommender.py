"""Neighborhood recommender with content-type aware scoring and Google Maps integration."""

import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

from chennai_guide.models.data_models import Neighborhood, LocalGuideResponse
from chennai_guide.parsers.context_parser import ProductMdParser


class NeighborhoodRecommender:
    """Provides content-type aware Chennai neighborhood recommendations with Google Maps integration."""
    
    def __init__(self, context_parser: ProductMdParser):
        """Initialize with context parser for accessing neighborhood data."""
        self.context_parser = context_parser
        self.neighborhoods = self.context_parser.parse_neighborhoods()
        
        # Content type keywords for matching
        self.content_type_keywords = {
            'food': ['food', 'eating', 'restaurant', 'cuisine', 'dining', 'street food', 'snacks', 'coffee', 'dosa', 'biryani'],
            'shopping': ['shopping', 'market', 'bazaar', 'mall', 'stores', 'clothes', 'jewelry', 'silk'],
            'cultural': ['temple', 'culture', 'heritage', 'traditional', 'festival', 'music', 'dance', 'art'],
            'scenic': ['beach', 'scenic', 'views', 'nature', 'sunset', 'photography', 'landscape'],
            'nightlife': ['nightlife', 'evening', 'night', 'bars', 'entertainment'],
            'lifestyle': ['lifestyle', 'modern', 'trendy', 'cafe', 'upscale', 'residential'],
            'historical': ['historical', 'heritage', 'ancient', 'colonial', 'architecture', 'monument']
        }
    
    def score_neighborhoods(self, content_preferences: List[str]) -> List[Tuple[Neighborhood, float]]:
        """
        Create scoring algorithm based on content preferences.
        Rank neighborhoods by relevance to content type.
        Support multiple content type preferences.
        """
        if not content_preferences:
            # Return all neighborhoods with equal score if no preferences
            return [(neighborhood, 1.0) for neighborhood in self.neighborhoods]
        
        scored_neighborhoods = []
        
        for neighborhood in self.neighborhoods:
            score = self._calculate_neighborhood_score(neighborhood, content_preferences)
            scored_neighborhoods.append((neighborhood, score))
        
        # Sort by score in descending order
        scored_neighborhoods.sort(key=lambda x: x[1], reverse=True)
        
        return scored_neighborhoods
    
    def _calculate_neighborhood_score(self, neighborhood: Neighborhood, content_preferences: List[str]) -> float:
        """Calculate relevance score for a neighborhood based on content preferences."""
        total_score = 0.0
        max_possible_score = len(content_preferences)
        
        if max_possible_score == 0:
            return 1.0
        
        # Normalize content preferences to lowercase
        normalized_preferences = [pref.lower().strip() for pref in content_preferences]
        
        for preference in normalized_preferences:
            preference_score = self._score_preference_match(neighborhood, preference)
            total_score += preference_score
        
        # Normalize score to 0-1 range
        return total_score / max_possible_score
    
    def _score_preference_match(self, neighborhood: Neighborhood, preference: str) -> float:
        """Score how well a neighborhood matches a specific content preference."""
        score = 0.0
        
        # Direct match in best_for_content (highest weight)
        for content_type in neighborhood.best_for_content:
            if preference in content_type.lower():
                score += 1.0
                break
        
        # Match in content_tags (high weight)
        for tag in neighborhood.content_tags:
            if preference in tag.lower():
                score += 0.8
                break
        
        # Match in vibe description (medium weight)
        if preference in neighborhood.vibe.lower():
            score += 0.6
        
        # Match in insider tips (medium weight)
        for tip in neighborhood.insider_tips:
            if preference in tip.lower():
                score += 0.5
                break
        
        # Keyword-based matching using content type keywords
        for content_type, keywords in self.content_type_keywords.items():
            if preference in keywords or any(keyword in preference for keyword in keywords):
                # Check if neighborhood supports this content type
                neighborhood_text = (
                    ' '.join(neighborhood.best_for_content) + ' ' +
                    neighborhood.vibe + ' ' +
                    ' '.join(neighborhood.insider_tips)
                ).lower()
                
                for keyword in keywords:
                    if keyword in neighborhood_text:
                        score += 0.4
                        break
        
        # Cap score at 1.0 for any single preference
        return min(score, 1.0)
    
    def get_neighborhood_recommendations(self, content_preferences: List[str], limit: Optional[int] = None) -> List[Neighborhood]:
        """Get ranked neighborhood recommendations based on content preferences."""
        scored_neighborhoods = self.score_neighborhoods(content_preferences)
        
        # Extract just the neighborhoods from scored results
        recommendations = [neighborhood for neighborhood, score in scored_neighborhoods if score > 0]
        
        if limit:
            recommendations = recommendations[:limit]
        
        return recommendations
    
    def match_content_type(self, query: str) -> List[str]:
        """Identify content preferences from natural language query."""
        query_lower = query.lower()
        matched_preferences = []
        
        # Direct content type matching
        for content_type, keywords in self.content_type_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    if content_type not in matched_preferences:
                        matched_preferences.append(content_type)
                    break
        
        # If no specific content types found, try to infer from context
        if not matched_preferences:
            # Look for general activity words
            if any(word in query_lower for word in ['visit', 'see', 'explore', 'go to']):
                matched_preferences.append('cultural')
            if any(word in query_lower for word in ['eat', 'hungry', 'meal']):
                matched_preferences.append('food')
            if any(word in query_lower for word in ['buy', 'purchase', 'shop']):
                matched_preferences.append('shopping')
            if any(word in query_lower for word in ['photo', 'picture', 'shot', 'film']):
                matched_preferences.append('scenic')
        
        return matched_preferences
    
    def generate_maps_link(self, neighborhood: Neighborhood) -> str:
        """
        Create Google Maps URLs for neighborhood locations.
        Validate map links are properly formatted.
        Include coordinates when available.
        """
        # Use existing Google Maps link if available and valid
        if neighborhood.google_maps_link and self._validate_maps_link(neighborhood.google_maps_link):
            return neighborhood.google_maps_link
        
        # Generate link with coordinates if available
        if neighborhood.coordinates and neighborhood.coordinates.get('lat') and neighborhood.coordinates.get('lng'):
            lat = neighborhood.coordinates['lat']
            lng = neighborhood.coordinates['lng']
            return f"https://maps.google.com/maps?q={lat},{lng}"
        
        # Fallback: generate basic Google Maps search link
        search_query = f"{neighborhood.name}, Chennai"
        encoded_query = search_query.replace(' ', '+').replace(',', '%2C')
        return f"https://maps.google.com/maps?q={encoded_query}"
    
    def _validate_maps_link(self, maps_link: str) -> bool:
        """Validate that Google Maps link is properly formatted."""
        if not maps_link:
            return False
        
        # Check if it's a valid Google Maps URL
        valid_patterns = [
            r'https://maps\.google\.com/maps\?q=',
            r'https://www\.google\.com/maps/',
            r'https://goo\.gl/maps/',
            r'https://maps\.app\.goo\.gl/'
        ]
        
        return any(re.match(pattern, maps_link) for pattern in valid_patterns)
    
    def generate_maps_links_batch(self, neighborhoods: List[Neighborhood]) -> List[str]:
        """Generate Google Maps links for multiple neighborhoods efficiently."""
        return [self.generate_maps_link(neighborhood) for neighborhood in neighborhoods]
    
    def get_coordinates_from_maps_link(self, maps_link: str) -> Optional[Dict[str, float]]:
        """Extract coordinates from Google Maps link if possible."""
        if not maps_link:
            return None
        
        # Try to extract coordinates from various Google Maps URL formats
        coordinate_patterns = [
            r'@(-?\d+\.\d+),(-?\d+\.\d+)',  # @lat,lng format
            r'q=(-?\d+\.\d+),(-?\d+\.\d+)',  # q=lat,lng format
            r'll=(-?\d+\.\d+),(-?\d+\.\d+)'   # ll=lat,lng format
        ]
        
        for pattern in coordinate_patterns:
            match = re.search(pattern, maps_link)
            if match:
                lat, lng = match.groups()
                return {'lat': float(lat), 'lng': float(lng)}
        
        return None
    
    def get_neighborhood_profile(self, name: str) -> Optional[Neighborhood]:
        """
        Return complete neighborhood information with maps.
        Include vibe, content suitability, insider tips, and Google Maps links.
        """
        for neighborhood in self.neighborhoods:
            if neighborhood.name.lower() == name.lower():
                # Ensure the neighborhood has a valid Google Maps link
                if not neighborhood.google_maps_link or not self._validate_maps_link(neighborhood.google_maps_link):
                    neighborhood.google_maps_link = self.generate_maps_link(neighborhood)
                
                # Extract coordinates if not already present
                if not neighborhood.coordinates and neighborhood.google_maps_link:
                    coords = self.get_coordinates_from_maps_link(neighborhood.google_maps_link)
                    if coords:
                        neighborhood.coordinates = coords
                
                return neighborhood
        return None
    
    def get_comprehensive_neighborhood_profiles(self, neighborhoods: List[Neighborhood]) -> List[Neighborhood]:
        """
        Return complete neighborhood information with maps for multiple neighborhoods.
        Include vibe, content suitability, insider tips, and Google Maps links.
        """
        comprehensive_profiles = []
        
        for neighborhood in neighborhoods:
            # Create a copy to avoid modifying the original
            profile = Neighborhood(
                name=neighborhood.name,
                vibe=neighborhood.vibe,
                best_for_content=neighborhood.best_for_content.copy(),
                insider_tips=neighborhood.insider_tips.copy(),
                content_tags=neighborhood.content_tags.copy(),
                google_maps_link=neighborhood.google_maps_link,
                coordinates=neighborhood.coordinates.copy() if neighborhood.coordinates else {}
            )
            
            # Ensure valid Google Maps link
            if not profile.google_maps_link or not self._validate_maps_link(profile.google_maps_link):
                profile.google_maps_link = self.generate_maps_link(profile)
            
            # Extract coordinates if not present
            if not profile.coordinates and profile.google_maps_link:
                coords = self.get_coordinates_from_maps_link(profile.google_maps_link)
                if coords:
                    profile.coordinates = coords
            
            comprehensive_profiles.append(profile)
        
        return comprehensive_profiles
    
    def format_neighborhood_profile(self, neighborhood: Neighborhood) -> str:
        """Format a neighborhood profile for display with all comprehensive information."""
        profile_lines = [
            f"**{neighborhood.name}**",
            f"Vibe: {neighborhood.vibe}",
            f"Best for content: {', '.join(neighborhood.best_for_content)}",
        ]
        
        if neighborhood.insider_tips:
            profile_lines.append(f"Insider tips: {'; '.join(neighborhood.insider_tips)}")
        
        if neighborhood.content_tags:
            profile_lines.append(f"Content tags: {', '.join(neighborhood.content_tags)}")
        
        if neighborhood.google_maps_link:
            profile_lines.append(f"Google Maps: {neighborhood.google_maps_link}")
        
        if neighborhood.coordinates and neighborhood.coordinates.get('lat') and neighborhood.coordinates.get('lng'):
            lat = neighborhood.coordinates['lat']
            lng = neighborhood.coordinates['lng']
            profile_lines.append(f"Coordinates: {lat}, {lng}")
        
        return '\n'.join(profile_lines)
    
    def create_neighborhood_response(self, neighborhoods: List[Neighborhood], query: str) -> LocalGuideResponse:
        """Create a comprehensive response with neighborhood recommendations."""
        # Get comprehensive profiles with complete information
        comprehensive_neighborhoods = self.get_comprehensive_neighborhood_profiles(neighborhoods)
        
        # Generate maps links from comprehensive profiles
        maps_links = [neighborhood.google_maps_link for neighborhood in comprehensive_neighborhoods]
        
        # Generate content creator note
        if comprehensive_neighborhoods:
            content_creator_note = f"Found {len(comprehensive_neighborhoods)} neighborhoods perfect for your content creation needs!"
        else:
            content_creator_note = "No specific neighborhoods found, but Chennai has many great spots for content creation."
        
        # Generate suggestions based on available neighborhoods
        suggestions = []
        if len(comprehensive_neighborhoods) > 3:
            suggestions.append("Consider visiting multiple neighborhoods for diverse content")
        if any('food' in ' '.join(n.best_for_content).lower() for n in comprehensive_neighborhoods):
            suggestions.append("Don't miss the local street food scenes")
        if any('temple' in n.vibe.lower() or 'cultural' in ' '.join(n.best_for_content).lower() for n in comprehensive_neighborhoods):
            suggestions.append("Remember to dress modestly when visiting temples")
        if any('beach' in n.vibe.lower() or 'scenic' in ' '.join(n.best_for_content).lower() for n in comprehensive_neighborhoods):
            suggestions.append("Golden hour (6-7pm) is perfect for scenic shots")
        
        return LocalGuideResponse(
            query_type="neighborhood",
            results=comprehensive_neighborhoods,
            content_creator_note=content_creator_note,
            suggestions=suggestions,
            maps_links=maps_links
        )