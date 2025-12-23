# Chennai Local Guide

A specialized tool that helps content creators navigate Chennai authentically by providing local slang translation and neighborhood recommendations with Google Maps integration.

## Features

- **Slang Translation**: Identify and translate Chennai slang terms with cultural context
- **Neighborhood Recommendations**: Get content-type aware neighborhood suggestions
- **Google Maps Integration**: Direct links to recommended locations
- **Content Creator Tips**: Specific advice for authentic content creation

## Project Structure

```
chennai_guide/
├── models/          # Data models (SlangTerm, Neighborhood, etc.)
├── parsers/         # Context file parsers and interfaces
├── api/             # Query processing and response generation
└── __init__.py

tests/
├── property_tests/  # Property-based tests using Hypothesis
├── conftest.py      # Test configuration and fixtures
└── test_models.py   # Unit tests for data models
```

## Installation

```bash
pip install -r requirements.txt
```

## Testing

Run unit tests:
```bash
pytest tests/test_models.py
```

Run property-based tests:
```bash
pytest tests/property_tests/ -m property
```

Run all tests:
```bash
pytest
```

## Development

The system is designed around two core functions:
1. **Slang Translation** - Identifies Chennai slang and provides definitions with cultural context
2. **Neighborhood Recommendations** - Suggests areas based on content type preferences

All local knowledge comes from a single `product.md` context file that serves as the source of truth for Chennai cultural information.