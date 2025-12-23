#!/usr/bin/env python3
"""
Vlogger's Local Guide - NYC Edition
A tool for content creators to get authentic local slang translations and neighborhood recommendations
"""

import re
import json
from typing import Dict, List, Tuple, Optional

class VloggerLocalGuide:
    def __init__(self, context_file: str = "product.md"):
        """Initialize the guide with local context from product.md"""
        self.context = self._load_context(context_file)
        self.slang_dict = self._parse_slang()
        self.neighborhoods = self._parse_neighborhoods()
        
    def _load_context(self, filename: str) -> str:
        """Load the local context from product.md"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Context file not found. Please create product.md with local information."
    
    def _parse_slang(self) -> Dict[str, Dict[str, str]]:
        """Parse slang dictionary from context"""
        slang_dict = {}
        
        # Extract slang entries using regex
        slang_pattern = r'\*\*"([^"]+)"\*\* - ([^\n]+)\n(?:.*?Usage: "([^"]+)".*?Vlogger tip: ([^\n]+))?'
        matches = re.findall(slang_pattern, self.context, re.DOTALL)
        
        for match in matches:
            term, definition, usage, tip = match
            slang_dict[term.lower()] = {
                'definition': definition,
                'usage': usage if usage else '',
                'vlogger_tip': tip if tip else ''
            }
        
        return slang_dict
    
    def _parse_neighborhoods(self) -> Dict[str, Dict[str, str]]:
        """Parse neighborhood information from context"""
        neighborhoods = {}
        
        # Extract neighborhood sections
        neighborhood_pattern = r'### ([^\n]+)\n\*\*Vibe\*\*: ([^\n]+)\n\*\*Best for vlogs\*\*: ([^\n]+)'
        matches = re.findall(neighborhood_pattern, self.context)
        
        for match in matches:
            name, vibe, best_for = match
            neighborhoods[name.lower()] = {
                'name': name,
                'vibe': vibe,
                'best_for_vlogs': best_for
            }
        
        return neighborhoods
    
    def translate_slang(self, text: str) -> Dict[str, any]:
        """Translate slang terms found in text and provide vlogger context"""
        found_slang = []
        text_lower = text.lower()
        
        for term, info in self.slang_dict.items():
            if term in text_lower:
                found_slang.append({
                    'term': term,
                    'definition': info['definition'],
                    'usage_example': info['usage'],
                    'vlogger_tip': info['vlogger_tip']
                })
        
        return {
            'original_text': text,
            'slang_found': found_slang,
            'translation_help': len(found_slang) > 0
        }
    
    def get_neighborhood_recommendations(self, content_type: str = "") -> List[Dict[str, str]]:
        """Get neighborhood recommendations based on content type"""
        recommendations = []
        
        content_keywords = {
            'food': ['food', 'eating', 'restaurant', 'cafe'],
            'art': ['art', 'creative', 'street art', 'culture'],
            'nightlife': ['night', 'party', 'bar', 'club'],
            'scenic': ['view', 'photo', 'scenic', 'skyline'],
            'authentic': ['local', 'authentic', 'real', 'culture']
        }
        
        for neighborhood, info in self.neighborhoods.items():
            score = 0
            
            # Score based on content type match
            if content_type:
                for category, keywords in content_keywords.items():
                    if any(keyword in content_type.lower() for keyword in keywords):
                        if any(keyword in info['best_for_vlogs'].lower() for keyword in keywords):
                            score += 2
                        if any(keyword in info['vibe'].lower() for keyword in keywords):
                            score += 1
            
            recommendations.append({
                'neighborhood': info['name'],
                'vibe': info['vibe'],
                'best_for_vlogs': info['best_for_vlogs'],
                'relevance_score': score
            })
        
        # Sort by relevance score
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        return recommendations[:3]  # Top 3 recommendations
    
    def vlogger_session(self, query: str) -> Dict[str, any]:
        """Main interface for vloggers - handles both slang and neighborhood queries"""
        query_lower = query.lower()
        
        # Determine query type
        if any(word in query_lower for word in ['neighborhood', 'area', 'where', 'visit', 'film', 'shoot']):
            # Neighborhood recommendation query
            content_hints = []
            if 'food' in query_lower:
                content_hints.append('food')
            if any(word in query_lower for word in ['art', 'creative', 'street']):
                content_hints.append('art')
            if any(word in query_lower for word in ['night', 'bar', 'party']):
                content_hints.append('nightlife')
            if any(word in query_lower for word in ['view', 'photo', 'scenic']):
                content_hints.append('scenic')
            
            content_type = ' '.join(content_hints) if content_hints else query
            recommendations = self.get_neighborhood_recommendations(content_type)
            
            return {
                'query_type': 'neighborhood_recommendation',
                'query': query,
                'recommendations': recommendations,
                'vlogger_note': "These neighborhoods are ranked by relevance to your content needs!"
            }
        
        else:
            # Slang translation query
            translation = self.translate_slang(query)
            
            return {
                'query_type': 'slang_translation',
                'query': query,
                'translation': translation,
                'vlogger_note': "Use these translations to sound more authentic in your vlogs!"
            }

def main():
    """Interactive CLI for the Vlogger's Local Guide"""
    guide = VloggerLocalGuide()
    
    print("🎬 Welcome to the Vlogger's Local Guide - NYC Edition!")
    print("Ask me about local slang or where to film content.")
    print("Type 'quit' to exit.\n")
    
    while True:
        query = input("Vlogger Query: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Happy vlogging! 🎥")
            break
        
        if not query:
            continue
        
        result = guide.vlogger_session(query)
        
        print(f"\n📱 {result['vlogger_note']}")
        
        if result['query_type'] == 'slang_translation':
            translation = result['translation']
            if translation['translation_help']:
                print("\n🗣️ Slang Found:")
                for slang in translation['slang_found']:
                    print(f"  • '{slang['term']}' = {slang['definition']}")
                    if slang['usage_example']:
                        print(f"    Example: \"{slang['usage_example']}\"")
                    if slang['vlogger_tip']:
                        print(f"    💡 Vlogger Tip: {slang['vlogger_tip']}")
                    print()
            else:
                print("No local slang detected. Try asking about NYC terms!")
        
        elif result['query_type'] == 'neighborhood_recommendation':
            print("\n🏙️ Top Neighborhood Recommendations:")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"  {i}. {rec['neighborhood']}")
                print(f"     Vibe: {rec['vibe']}")
                print(f"     Best for: {rec['best_for_vlogs']}")
                print()
        
        print("-" * 50)

if __name__ == "__main__":
    main()