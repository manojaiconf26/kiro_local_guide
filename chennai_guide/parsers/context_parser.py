"""Context parser implementation for extracting data from product.md."""

import re
import threading
import time
from typing import List, Dict, Optional, Callable
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from chennai_guide.parsers.interfaces import ContextParserInterface
from chennai_guide.models.data_models import SlangTerm, Neighborhood, CulturalInsight, SeasonalContent


class ProductMdFileHandler(FileSystemEventHandler):
    """File system event handler for product.md changes."""
    
    def __init__(self, parser_instance, callback: Optional[Callable] = None):
        """Initialize handler with parser instance and optional callback."""
        self.parser_instance = parser_instance
        self.callback = callback
        super().__init__()
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and event.src_path.endswith('product.md'):
            print(f"Detected change in {event.src_path}, reloading context...")
            try:
                self.parser_instance.reload_context()
                if self.callback:
                    self.callback()
                print("Context reloaded successfully")
            except Exception as e:
                print(f"Error reloading context: {e}")


class ProductMdParser(ContextParserInterface):
    """Parser for extracting Chennai local knowledge from product.md file."""
    
    def __init__(self, product_md_path: str = "product.md", enable_hot_reload: bool = False):
        """Initialize parser with path to product.md file and optional hot-reload."""
        self.product_md_path = Path(product_md_path)
        self._content = ""
        self._observer = None
        self._file_handler = None
        self._hot_reload_enabled = enable_hot_reload
        self._reload_callbacks = []
        self._load_content()
        
        if enable_hot_reload:
            self.start_file_watching()
    
    def _load_content(self) -> None:
        """Load content from product.md file with graceful error handling."""
        try:
            if self.product_md_path.exists():
                with open(self.product_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content.strip():
                        print(f"Warning: {self.product_md_path} is empty, using fallback data")
                        self._content = self._get_fallback_content()
                    else:
                        self._content = content
            else:
                print(f"Warning: {self.product_md_path} not found, using fallback data")
                self._content = self._get_fallback_content()
        except UnicodeDecodeError as e:
            print(f"Warning: Encoding error reading {self.product_md_path}: {e}")
            print("Using fallback data")
            self._content = self._get_fallback_content()
        except PermissionError as e:
            print(f"Warning: Permission denied reading {self.product_md_path}: {e}")
            print("Using fallback data")
            self._content = self._get_fallback_content()
        except Exception as e:
            print(f"Warning: Unexpected error reading {self.product_md_path}: {e}")
            print("Using fallback data")
            self._content = self._get_fallback_content()
    
    def _get_fallback_content(self) -> str:
        """Provide minimal fallback content when product.md is unavailable or corrupted."""
        return """# Chennai Local Guide - Fallback Content

## Local Slang Dictionary

- **"Machaan"** - Friend, buddy (used between close friends)
  - Usage: "Machaan, let's go to Marina Beach"
  - Content Creator tip: Perfect for showing local friendship culture

- **"Semma"** - Awesome, excellent, amazing
  - Usage: "That dosa was semma!"
  - Content Creator tip: Great for food reactions

## Content Creator-Friendly Neighborhoods

### Marina Beach Area
**Vibe**: Scenic coastline, evening hangout spot
**Best for content**: Sunset shots, local lifestyle, street food
**Google Maps**: https://maps.google.com/maps?q=Marina+Beach,+Chennai
**Insider tip**: Golden hour (6-7pm) is magical
"""
    
    def start_file_watching(self) -> None:
        """Start watching the product.md file for changes."""
        if self._observer is not None:
            return  # Already watching
        
        self._file_handler = ProductMdFileHandler(self, self._notify_reload_callbacks)
        self._observer = Observer()
        
        # Watch the directory containing the product.md file
        watch_directory = self.product_md_path.parent
        self._observer.schedule(self._file_handler, str(watch_directory), recursive=False)
        self._observer.start()
        print(f"Started watching {self.product_md_path} for changes")
    
    def stop_file_watching(self) -> None:
        """Stop watching the product.md file for changes."""
        if self._observer is not None:
            self._observer.stop()
            self._observer.join()
            self._observer = None
            self._file_handler = None
            print(f"Stopped watching {self.product_md_path}")
    
    def add_reload_callback(self, callback: Callable) -> None:
        """Add a callback function to be called when the file is reloaded."""
        self._reload_callbacks.append(callback)
    
    def remove_reload_callback(self, callback: Callable) -> None:
        """Remove a callback function."""
        if callback in self._reload_callbacks:
            self._reload_callbacks.remove(callback)
    
    def _notify_reload_callbacks(self) -> None:
        """Notify all registered callbacks that the file has been reloaded."""
        for callback in self._reload_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in reload callback: {e}")
    
    def __del__(self):
        """Cleanup file watching when parser is destroyed."""
        self.stop_file_watching()
    
    def parse_slang_dictionary(self) -> List[SlangTerm]:
        """Extract Chennai slang terms with definitions, usage examples, and content creator tips."""
        slang_terms = []
        
        try:
            # Find the Local Slang Dictionary section
            slang_section_match = re.search(
                r'## Local Slang Dictionary\s*\n(.*?)(?=\n## |\Z)', 
                self._content, 
                re.DOTALL
            )
            
            if not slang_section_match:
                print("Warning: No Local Slang Dictionary section found in product.md")
                return slang_terms
            
            slang_section = slang_section_match.group(1)
            
            # Extract individual slang terms using regex
            # Pattern matches: - **"Term"** - Definition
            term_pattern = r'- \*\*"([^"]+)"\*\* - ([^\n]+)\n\s*- Usage: "([^"]+)"\n\s*- Content Creator tip: ([^\n]+)'
            
            matches = re.findall(term_pattern, slang_section, re.MULTILINE)
            
            for match in matches:
                try:
                    term, definition, usage, tip = match
                    slang_term = SlangTerm(
                        term=term.strip(),
                        definition=definition.strip(),
                        usage_example=usage.strip(),
                        vlogger_tip=tip.strip()
                    )
                    slang_terms.append(slang_term)
                except Exception as e:
                    print(f"Warning: Error parsing slang term {match}: {e}")
                    continue
            
            if not slang_terms:
                print("Warning: No valid slang terms found, providing fallback terms")
                # Provide fallback slang terms
                slang_terms = [
                    SlangTerm(
                        term="Machaan",
                        definition="Friend, buddy (used between close friends)",
                        usage_example="Machaan, let's go to Marina Beach",
                        vlogger_tip="Perfect for showing local friendship culture"
                    ),
                    SlangTerm(
                        term="Semma",
                        definition="Awesome, excellent, amazing",
                        usage_example="That dosa was semma!",
                        vlogger_tip="Great for food reactions"
                    )
                ]
        
        except Exception as e:
            print(f"Warning: Error parsing slang dictionary: {e}")
            print("Providing fallback slang terms")
            # Provide fallback slang terms
            slang_terms = [
                SlangTerm(
                    term="Machaan",
                    definition="Friend, buddy (used between close friends)",
                    usage_example="Machaan, let's go to Marina Beach",
                    vlogger_tip="Perfect for showing local friendship culture"
                ),
                SlangTerm(
                    term="Semma",
                    definition="Awesome, excellent, amazing",
                    usage_example="That dosa was semma!",
                    vlogger_tip="Great for food reactions"
                )
            ]
        
        return slang_terms
    
    def parse_neighborhoods(self) -> List[Neighborhood]:
        """Extract Chennai neighborhood profiles with vibes, content suitability, and Google Maps coordinates."""
        neighborhoods = []
        
        try:
            # Find the Content Creator-Friendly Neighborhoods section
            neighborhoods_section_match = re.search(
                r'## Content Creator-Friendly Neighborhoods\s*\n(.*?)(?=\n## |\Z)', 
                self._content, 
                re.DOTALL
            )
            
            if not neighborhoods_section_match:
                print("Warning: No Content Creator-Friendly Neighborhoods section found in product.md")
                return self._get_fallback_neighborhoods()
            
            neighborhoods_section = neighborhoods_section_match.group(1)
            
            # Handle the case where the first ### appears immediately after the section header
            if neighborhoods_section.strip().startswith('### '):
                # Add a newline before the first ### to make the split work correctly
                neighborhoods_section = '\n' + neighborhoods_section
            
            # Split by neighborhood headers (### Name)
            neighborhood_blocks = re.split(r'\n### ([^\n]+)', neighborhoods_section)
            
            # Skip the first empty element (before the first ###)
            if neighborhood_blocks and not neighborhood_blocks[0].strip():
                neighborhood_blocks = neighborhood_blocks[1:]
            
            # Process pairs of (name, content)
            for i in range(0, len(neighborhood_blocks), 2):
                if i + 1 >= len(neighborhood_blocks):
                    break
                
                try:
                    name = neighborhood_blocks[i].strip()
                    content = neighborhood_blocks[i + 1]
                    
                    # Extract neighborhood data with fallbacks
                    vibe_match = re.search(r'\*\*Vibe\*\*: ([^\n]+)', content)
                    vibe = vibe_match.group(1).strip() if vibe_match else "Local neighborhood"
                    
                    best_for_match = re.search(r'\*\*Best for content\*\*: ([^\n]+)', content)
                    best_for_content = []
                    if best_for_match:
                        best_for_content = [item.strip() for item in best_for_match.group(1).split(',')]
                    else:
                        best_for_content = ["general content"]
                    
                    maps_match = re.search(r'\*\*Google Maps\*\*: ([^\n]+)', content)
                    google_maps_link = maps_match.group(1).strip() if maps_match else ""
                    
                    # Extract insider tips
                    insider_tip_match = re.search(r'\*\*Insider tip\*\*: ([^\n]+)', content)
                    insider_tips = []
                    if insider_tip_match:
                        insider_tips = [insider_tip_match.group(1).strip()]
                    else:
                        insider_tips = ["Great for exploring local culture"]
                    
                    # Extract content tags from best_for_content and local spots
                    content_tags = []
                    if best_for_content:
                        content_tags.extend(best_for_content)
                    
                    # Extract coordinates from Google Maps link (basic implementation)
                    coordinates = {}
                    # Note: For now, we'll leave coordinates empty as extracting from Google Maps URLs 
                    # requires more complex parsing or API calls
                    
                    neighborhood = Neighborhood(
                        name=name,
                        vibe=vibe,
                        best_for_content=best_for_content,
                        insider_tips=insider_tips,
                        content_tags=content_tags,
                        google_maps_link=google_maps_link,
                        coordinates=coordinates
                    )
                    neighborhoods.append(neighborhood)
                
                except Exception as e:
                    print(f"Warning: Error parsing neighborhood {neighborhood_blocks[i] if i < len(neighborhood_blocks) else 'unknown'}: {e}")
                    continue
            
            if not neighborhoods:
                print("Warning: No valid neighborhoods found, providing fallback neighborhoods")
                return self._get_fallback_neighborhoods()
        
        except Exception as e:
            print(f"Warning: Error parsing neighborhoods: {e}")
            print("Providing fallback neighborhoods")
            return self._get_fallback_neighborhoods()
        
        return neighborhoods
    
    def _get_fallback_neighborhoods(self) -> List[Neighborhood]:
        """Provide fallback neighborhood data when parsing fails."""
        return [
            Neighborhood(
                name="Marina Beach Area",
                vibe="Scenic coastline, evening hangout spot",
                best_for_content=["sunset shots", "local lifestyle", "street food"],
                insider_tips=["Golden hour (6-7pm) is magical"],
                content_tags=["scenic", "lifestyle", "food"],
                google_maps_link="https://maps.google.com/maps?q=Marina+Beach,+Chennai",
                coordinates={}
            ),
            Neighborhood(
                name="T. Nagar",
                vibe="Bustling shopping paradise, traditional meets modern",
                best_for_content=["shopping", "street food", "cultural immersion"],
                insider_tips=["Early morning for less crowded shots"],
                content_tags=["shopping", "food", "culture"],
                google_maps_link="https://maps.google.com/maps?q=T.+Nagar,+Chennai",
                coordinates={}
            )
        ]
    
    def reload_context(self) -> None:
        """Refresh data from updated product.md file with graceful error handling."""
        try:
            old_content = self._content
            self._load_content()
            print(f"Successfully reloaded context from {self.product_md_path}")
        except Exception as e:
            print(f"Failed to reload context: {e}")
            print("Continuing with previous content")
            # Don't raise the exception - continue with old content
            if not hasattr(self, '_content') or not self._content:
                print("No previous content available, using fallback")
                self._content = self._get_fallback_content()
    
    def extract_maps_data(self) -> Dict[str, Dict[str, float]]:
        """Parse Google Maps links and location coordinates from product.md."""
        maps_data = {}
        
        try:
            # Find neighborhoods section and extract maps data with neighborhood names
            neighborhoods_section_match = re.search(
                r'## Content Creator-Friendly Neighborhoods\s*\n(.*?)(?=\n## |\Z)', 
                self._content, 
                re.DOTALL
            )
            
            if not neighborhoods_section_match:
                print("Warning: No neighborhoods section found for maps data extraction")
                return maps_data
            
            neighborhoods_section = neighborhoods_section_match.group(1)
            
            # Split by neighborhood headers and extract maps links
            neighborhood_blocks = re.split(r'\n### ([^\n]+)', neighborhoods_section)[1:]
            
            for i in range(0, len(neighborhood_blocks), 2):
                if i + 1 >= len(neighborhood_blocks):
                    break
                
                try:
                    name = neighborhood_blocks[i].strip()
                    content = neighborhood_blocks[i + 1]
                    
                    # Extract Google Maps link
                    maps_match = re.search(r'\*\*Google Maps\*\*: (https://maps\.google\.com/[^\n]+)', content)
                    if maps_match:
                        maps_link = maps_match.group(1).strip()
                        # For now, store the link with empty coordinates
                        # In a real implementation, we could use geocoding APIs to get coordinates
                        maps_data[name] = {
                            "lat": 0.0, 
                            "lng": 0.0, 
                            "maps_link": maps_link
                        }
                except Exception as e:
                    print(f"Warning: Error extracting maps data for neighborhood: {e}")
                    continue
        
        except Exception as e:
            print(f"Warning: Error extracting maps data: {e}")
        
        return maps_data
    
    def validate_slang_completeness(self, slang_terms: List[SlangTerm]) -> List[str]:
        """Validate that slang terms have complete information."""
        validation_errors = []
        
        try:
            for term in slang_terms:
                if not term.term:
                    validation_errors.append("Missing term name")
                if not term.definition:
                    validation_errors.append(f"Missing definition for term: {term.term}")
                if not term.usage_example:
                    validation_errors.append(f"Missing usage example for term: {term.term}")
                if not term.vlogger_tip:
                    validation_errors.append(f"Missing vlogger tip for term: {term.term}")
        except Exception as e:
            validation_errors.append(f"Error validating slang terms: {e}")
        
        return validation_errors
    
    def validate_neighborhood_completeness(self, neighborhoods: List[Neighborhood]) -> List[str]:
        """Validate that neighborhoods have complete information."""
        validation_errors = []
        
        try:
            for neighborhood in neighborhoods:
                if not neighborhood.name:
                    validation_errors.append("Missing neighborhood name")
                if not neighborhood.vibe:
                    validation_errors.append(f"Missing vibe for neighborhood: {neighborhood.name}")
                if not neighborhood.best_for_content:
                    validation_errors.append(f"Missing content suitability for neighborhood: {neighborhood.name}")
                if not neighborhood.google_maps_link:
                    validation_errors.append(f"Missing Google Maps link for neighborhood: {neighborhood.name}")
        except Exception as e:
            validation_errors.append(f"Error validating neighborhoods: {e}")
        
        return validation_errors
    
    def parse_cultural_insights(self) -> List[CulturalInsight]:
        """Extract cultural tips, etiquette, and content creator advice."""
        cultural_insights = []
        
        try:
            # Define sections to parse for cultural insights
            cultural_sections = [
                ("Content Creator Tips", r'## Content Creator Tips\s*\n(.*?)(?=\n## |\Z)'),
                ("Authenticity Markers", r'## Authenticity Markers for Content\s*\n(.*?)(?=\n## |\Z)'),
                ("Transportation Tips", r'## Transportation Tips for Content\s*\n(.*?)(?=\n## |\Z)'),
                ("Food Content Gold", r'## Food Content Gold\s*\n(.*?)(?=\n## |\Z)')
            ]
            
            for category, pattern in cultural_sections:
                try:
                    section_match = re.search(pattern, self._content, re.DOTALL)
                    if section_match:
                        section_content = section_match.group(1)
                        
                        # Extract subsections
                        subsections = re.split(r'\n### ([^\n]+)', section_content)[1:]
                        
                        for i in range(0, len(subsections), 2):
                            if i + 1 >= len(subsections):
                                break
                            
                            try:
                                title = subsections[i].strip()
                                content = subsections[i + 1]
                                
                                # Extract bullet points and tips
                                content_items = []
                                tips = []
                                
                                # Find bullet points
                                bullet_points = re.findall(r'^- (.+)$', content, re.MULTILINE)
                                content_items.extend(bullet_points)
                                
                                # Find numbered items
                                numbered_items = re.findall(r'^\d+\. (.+)$', content, re.MULTILINE)
                                content_items.extend(numbered_items)
                                
                                # Extract quoted phrases as tips
                                quoted_phrases = re.findall(r'"([^"]+)"', content)
                                tips.extend(quoted_phrases)
                                
                                if content_items or tips:
                                    cultural_insight = CulturalInsight(
                                        category=category,
                                        title=title,
                                        content=content_items,
                                        tips=tips
                                    )
                                    cultural_insights.append(cultural_insight)
                            except Exception as e:
                                print(f"Warning: Error parsing cultural insight subsection: {e}")
                                continue
                except Exception as e:
                    print(f"Warning: Error parsing cultural section {category}: {e}")
                    continue
        
        except Exception as e:
            print(f"Warning: Error parsing cultural insights: {e}")
        
        return cultural_insights
    
    def parse_seasonal_content(self) -> List[SeasonalContent]:
        """Extract seasonal content recommendations and ideas."""
        seasonal_content = []
        
        try:
            # Find the Seasonal Content Ideas section
            seasonal_section_match = re.search(
                r'## Seasonal Content Ideas\s*\n(.*?)(?=\n## |\Z)', 
                self._content, 
                re.DOTALL
            )
            
            if not seasonal_section_match:
                print("Warning: No Seasonal Content Ideas section found")
                return seasonal_content
            
            seasonal_section = seasonal_section_match.group(1)
            
            # Handle the case where the first ### appears immediately after the section header
            if seasonal_section.strip().startswith('### '):
                # Add a newline before the first ### to make the split work correctly
                seasonal_section = '\n' + seasonal_section
            
            # Split by season headers (### Season)
            season_blocks = re.split(r'\n### ([^\n]+)', seasonal_section)
            
            # Skip the first empty element (before the first ###)
            if season_blocks and not season_blocks[0].strip():
                season_blocks = season_blocks[1:]
            
            # Process pairs of (name, content)
            for i in range(0, len(season_blocks), 2):
                if i + 1 >= len(season_blocks):
                    break
                
                try:
                    season_header = season_blocks[i].strip()
                    content = season_blocks[i + 1]
                    
                    # Extract period from header (e.g., "Winter (Dec-Feb)")
                    period_match = re.search(r'\(([^)]+)\)', season_header)
                    period = period_match.group(1) if period_match else ""
                    season = season_header.split('(')[0].strip()
                    
                    # Extract content ideas (bullet points)
                    content_ideas = re.findall(r'^- (.+)$', content, re.MULTILINE)
                    
                    # Extract special notes (quoted phrases)
                    special_notes = re.findall(r'"([^"]+)"', content)
                    
                    if content_ideas or special_notes:
                        seasonal_item = SeasonalContent(
                            season=season,
                            period=period,
                            content_ideas=content_ideas,
                            special_notes=special_notes
                        )
                        seasonal_content.append(seasonal_item)
                except Exception as e:
                    print(f"Warning: Error parsing seasonal content for season: {e}")
                    continue
        
        except Exception as e:
            print(f"Warning: Error parsing seasonal content: {e}")
        
        return seasonal_content