# Chennai Local Guide - Deployment Guide

This guide explains how to set up and run the Chennai Local Guide demo server for content creators.

## Quick Start

### Option 1: One-Click Startup (Recommended)

**Windows:**
```bash
# Double-click start_server.bat or run in Command Prompt:
start_server.bat
```

**macOS/Linux:**
```bash
# Make executable and run:
chmod +x start_server.sh
./start_server.sh
```

**Cross-Platform:**
```bash
python start_server.py
```

### Option 2: Manual Setup

1. **Install Dependencies:**
   ```bash
   pip install -e .
   ```

2. **Start Server:**
   ```bash
   python -m chennai_guide.web.server
   ```

## Server Configuration

### Command Line Options

```bash
python start_server.py [OPTIONS]

Options:
  --port PORT        Port to run server on (default: 8000)
  --no-browser       Don't automatically open browser
  --dev              Development mode with auto-install
  --check            Check if dependencies are installed
```

### Examples

```bash
# Start on custom port
python start_server.py --port 3000

# Start without opening browser
python start_server.py --no-browser

# Development mode (auto-installs dependencies)
python start_server.py --dev

# Check installation status
python start_server.py --check
```

## API Endpoints

The server provides several API endpoints for integration:

### Main Query Endpoint
```
GET  /api/query?q=your_query
POST /api/query
```

**Example:**
```bash
curl "http://localhost:8000/api/query?q=What does semma mean?"
```

### Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "backend_available": true,
  "components": {
    "context_parser": true,
    "query_processor": true,
    "slang_translator": true,
    "neighborhood_recommender": true
  }
}
```

## Web Interface

Once the server is running, access the web interface at:
- **Local:** http://localhost:8000
- **Custom Port:** http://localhost:YOUR_PORT

### Features

1. **Slang Translation:** Enter Chennai slang terms to get definitions and usage tips
2. **Neighborhood Recommendations:** Ask about areas for specific content types
3. **Quick Examples:** Click preset buttons for common queries
4. **Google Maps Integration:** Direct links to recommended locations
5. **Natural Language Processing:** Ask questions in plain English

## File Structure

```
chennai_guide/
├── web/
│   ├── server.py          # Main web server
│   ├── index.html         # Web interface
│   ├── styles.css         # Styling
│   ├── app.js            # Frontend logic
│   ├── browse.js         # Browse functionality
│   └── help.js           # Help system
├── start_server.py        # Cross-platform startup script
├── start_server.bat       # Windows startup script
├── start_server.sh        # Unix/Linux/macOS startup script
├── server_config.json     # Server configuration
└── DEPLOYMENT.md          # This file
```

## Troubleshooting

### Common Issues

**1. "Module not found" errors:**
```bash
# Install in development mode
pip install -e .

# Or use development mode startup
python start_server.py --dev
```

**2. Port already in use:**
```bash
# Use a different port
python start_server.py --port 3000
```

**3. Backend components not loading:**
- Check that all Python files are in place
- Verify product.md exists in the project root
- Run health check: `curl http://localhost:8000/api/health`

**4. Browser doesn't open automatically:**
```bash
# Disable auto-browser opening
python start_server.py --no-browser

# Then manually open: http://localhost:8000
```

### Development Mode

For development and testing:

```bash
# Start in development mode
python start_server.py --dev

# This will:
# - Auto-install dependencies if missing
# - Show detailed error messages
# - Enable hot-reload for some components
```

### Production Deployment

For production deployment (not recommended for this demo):

1. **Use a proper WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn chennai_guide.web.wsgi:application
   ```

2. **Configure reverse proxy (nginx/Apache)**
3. **Set up SSL certificates**
4. **Configure proper logging**

## System Requirements

- **Python:** 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **Memory:** 256MB RAM minimum
- **Storage:** 50MB free space
- **Network:** Internet connection for Google Maps links

## Configuration

Edit `server_config.json` to customize:

- **Port settings**
- **API timeouts**
- **Logging levels**
- **Development vs production modes**

## Support

For issues or questions:

1. Check the health endpoint: `/api/health`
2. Review server logs in the console
3. Verify all files are present and readable
4. Test with simple queries first

## Security Notes

⚠️ **This is a demo server** - not intended for production use:

- No authentication or authorization
- Basic error handling
- Simple HTTP server (not HTTPS)
- No rate limiting
- CORS enabled for all origins

For production use, implement proper security measures.