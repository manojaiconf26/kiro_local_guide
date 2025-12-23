# Chennai Local Guide Design Document

## Overview

The Chennai Local Guide is a specialized tool that helps content creators navigate Chennai authentically by focusing on local slang translation and neighborhood recommendations with Google Maps integration. **The system exclusively relies on a custom context file (product.md) to teach Kiro about Chennai's local nuances** - all cultural knowledge, slang definitions, and neighborhood information comes from this single curated source. The architecture emphasizes simplicity, accuracy, and practical value for content creators exploring Tamil Nadu's capital city.

## Architecture

The system follows a streamlined architecture focused on two core functions: slang translation and neighborhood recommendations:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Interface │    │  Query Processor │    │ Context Parser  │
│                 │◄──►│                  │◄──►│                 │
│ - Web Interface │    │ - Intent Analysis│    │ - product.md    │
│ - CLI Interface │    │ - Query Routing  │    │ - Slang Extract │
└─────────────────┘    └──────────────────┘    │ - Neighborhood  │
                                │               │   Extract       │
                                ▼               └─────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                    Core Response Generators                     │
│                                                                 │
│ ┌─────────────────────────┐ ┌─────────────────────────────────┐ │
│ │    Slang Translator     │ │   Neighborhood Recommender      │ │
│ │                         │ │                                 │ │
│ │ - Term Identification   │ │ - Content-Type Matching         │ │
│ │ - Definition Lookup     │ │ - Vibe Analysis                 │ │
│ │ - Vlogger Tips          │ │ - Ranking Algorithm             │ │
│ └─────────────────────────┘ └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Context Parser
**Purpose**: Extracts slang and neighborhood information exclusively from product.md (the single source of truth for Chennai local knowledge)
**Key Methods**:
- `parse_slang_dictionary()` - Extracts Chennai slang terms with definitions, usage examples, and content creator tips
- `parse_neighborhoods()` - Extracts Chennai neighborhood profiles with vibes, content suitability, and Google Maps coordinates
- `reload_context()` - Refreshes data from updated product.md file
- `extract_maps_data()` - Parses Google Maps links and location coordinates from product.md

### Query Processor
**Purpose**: Analyzes user input and determines if it's a slang or neighborhood query
**Key Methods**:
- `analyze_intent(query)` - Determines if query is about slang translation or neighborhood recommendations
- `extract_keywords(query)` - Identifies relevant terms and content type preferences
- `route_query(intent, keywords)` - Directs to slang translator or neighborhood recommender

### Core Response Generators

#### Slang Translator
**Purpose**: Identifies Chennai slang terms and provides comprehensive translation with local context (all data sourced from product.md)
**Key Methods**:
- `identify_slang_terms(text)` - Finds all Chennai slang in input text
- `get_slang_definition(term)` - Returns definition, usage example, and content creator tips from product.md
- `format_slang_response(terms)` - Organizes multiple slang results for presentation

#### Neighborhood Recommender
**Purpose**: Provides content-type aware Chennai neighborhood suggestions with Google Maps integration (all data from product.md)
**Key Methods**:
- `score_neighborhoods(content_preferences)` - Ranks neighborhoods by relevance to content type
- `get_neighborhood_profile(name)` - Returns detailed neighborhood information with Google Maps links from product.md
- `generate_maps_link(neighborhood)` - Creates Google Maps URLs for neighborhood locations
- `match_content_type(query)` - Identifies content preferences from natural language

## Data Models

### SlangTerm
```python
class SlangTerm:
    term: str
    definition: str
    usage_example: str
    vlogger_tip: str
```

### Neighborhood
```python
class Neighborhood:
    name: str
    vibe: str
    best_for_content: List[str]
    insider_tips: List[str]
    content_tags: List[str]  # food, art, nightlife, scenic, etc.
    google_maps_link: str  # Direct link to Google Maps location
    coordinates: Dict[str, float]  # lat, lng for mapping
```

### LocalGuideResponse
```python
class LocalGuideResponse:
    query_type: str  # "slang" or "neighborhood"
    results: List[Any]  # SlangTerm or Neighborhood objects
    content_creator_note: str
    suggestions: List[str]
    maps_links: List[str]  # Google Maps links for neighborhoods
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Core Properties for Vlogger's Local Guide

**Property 1: Slang Term Identification**
*For any* text input containing valid NYC slang terms, the system should identify all slang terms present in the text
**Validates: Requirements 1.1**

**Property 2: Slang Information Completeness**
*For any* identified slang term, the system should return complete information including definition, usage example, and vlogger tip
**Validates: Requirements 1.2, 1.4**

**Property 3: Slang Term Ordering**
*For any* text input containing multiple slang terms, the system should return results in the order the terms appear in the original text
**Validates: Requirements 1.3**

**Property 4: Neighborhood Recommendation Relevance**
*For any* content type preference, returned neighborhood recommendations should be relevant to that content type and ranked by suitability
**Validates: Requirements 2.1**

**Property 5: Neighborhood Information Completeness with Maps**
*For any* neighborhood recommendation, the system should include name, vibe description, content suitability information, insider tips, and Google Maps link
**Validates: Requirements 2.2**

**Property 6: Google Maps Integration**
*For any* neighborhood result, the system should provide a valid Google Maps link that directly opens the location
**Validates: Requirements 2.2**

**Property 7: Multi-Content Type Ranking**
*For any* query specifying multiple content types, neighborhoods that support more of the specified types should rank higher than those supporting fewer types
**Validates: Requirements 2.4**

**Property 8: Context File Parsing Completeness**
*For any* valid product.md file, the system should successfully extract all slang terms, neighborhood information, and Google Maps links
**Validates: Requirements 4.1**

**Property 9: Intent Classification Accuracy**
*For any* natural language query, the system should correctly classify it as either a slang translation request or neighborhood recommendation request
**Validates: Requirements 5.1**

## Error Handling

The system implements focused error handling for the two core features:

### Context File Errors
- **Missing product.md**: Graceful degradation with built-in sample data
- **Malformed Slang Section**: Partial parsing with error reporting for affected terms
- **Missing Neighborhood Data**: Default responses with guidance for content creation

### Query Processing Errors
- **Ambiguous Intent**: Present both slang and neighborhood results when unclear
- **No Slang Detected**: Suggest related NYC terms and provide examples
- **No Matching Neighborhoods**: Offer alternative content types and general recommendations

## Testing Strategy

The Vlogger's Local Guide requires both unit testing and property-based testing focused on the two core features.

### Unit Testing Approach
Unit tests will focus on:
- Specific slang term parsing from known product.md formats
- Individual neighborhood recommendation scenarios
- Error handling for malformed context data
- Integration between query processor and response generators

### Property-Based Testing Approach
Property-based tests will verify universal behaviors using **Hypothesis** (Python's property-based testing library). Each property-based test will run a minimum of 100 iterations.

Property-based tests will focus on:
- Slang identification across randomly generated text inputs
- Neighborhood ranking consistency across varied content type combinations  
- Context file parsing robustness across formatting variations
- Intent classification accuracy across natural language query variations

Each property-based test will be tagged with comments explicitly referencing the correctness property from this design document using the format: **Feature: local-guide, Property {number}: {property_text}**

### Test Configuration
- Property-based tests configured for minimum 100 iterations per test
- Input generators for text with slang, content preferences, and context variations
- Assertion libraries for validating slang and neighborhood data structures
- Performance benchmarks for response time requirements