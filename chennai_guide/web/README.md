# Chennai Local Guide Web Interface

A responsive web interface for the Chennai Local Guide that helps content creators understand Chennai slang and find perfect neighborhoods for filming.

## Features

### 🗣️ Slang Translation
- Translate Chennai/Tamil slang terms with cultural context
- Get usage examples and content creator tips
- Learn authentic local expressions

### 🏙️ Neighborhood Recommendations
- Find neighborhoods based on content type preferences
- Get Google Maps integration for easy navigation
- Access insider tips for each location

### 🎯 Smart Query Processing
- Natural language understanding
- Multi-intent query support (slang + neighborhoods)
- Contextual suggestions and error recovery

### 🛠️ Enhanced User Experience
- Responsive design for all devices
- Quick example buttons for common queries
- Comprehensive help system
- Error handling with recovery suggestions
- Dark mode support
- Accessibility features

## Files

- `index.html` - Main web interface
- `app.js` - Core application logic and API integration
- `help.js` - Help system and user guidance
- `styles.css` - Enhanced styling and responsive design
- `server.py` - Python web server with API endpoints

## Usage

### Starting the Server

```bash
# Basic usage
python server.py

# Custom port
python server.py --port 8080

# Don't auto-open browser
python server.py --no-browser
```

### API Endpoints

- `GET /` - Main web interface
- `POST /api/query` - Process queries (JSON: `{"query": "your query"}`)
- `GET /api/query?q=your_query` - Process queries via URL parameters
- `GET /api/health` - Health check and component status

### Example Queries

**Slang Translation:**
- "What does semma mean?"
- "Explain machaan"
- "What is vera level?"

**Neighborhood Recommendations:**
- "Where to film food content in Chennai?"
- "Best cultural neighborhoods?"
- "Scenic spots for content creation?"

**Multi-Intent:**
- "What does semma mean and where to film food content?"
- "Explain gethu and recommend trendy areas"

## Error Handling

The interface provides comprehensive error handling:

### Input Validation
- Empty query detection
- Query length validation
- City name mistake detection
- Contextual warnings and suggestions

### Recovery Suggestions
- Alternative query examples
- Topic-based recommendations
- Common mistake corrections
- Help system integration

### Fallback Modes
- Frontend-only mode when backend unavailable
- Graceful degradation of features
- Clear status indicators

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive design
- Progressive enhancement
- Accessibility compliance (WCAG 2.1)

## Development

The interface is built with:
- Vanilla JavaScript (ES6+)
- CSS3 with modern features
- Progressive Web App principles
- No external dependencies

### Key Classes

- `ChennaiLocalGuide` - Main application controller
- `ChennaiGuideHelp` - Help system and user guidance
- Context data embedded for offline functionality

## Integration

The web interface integrates with the Chennai Local Guide backend:
- Context Parser for product.md processing
- Query Processor for intent analysis
- Slang Translator for term definitions
- Neighborhood Recommender for location suggestions

When backend components are unavailable, the interface runs in frontend-only mode with embedded context data.