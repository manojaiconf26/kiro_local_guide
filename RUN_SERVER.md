# 🎬 Chennai Local Guide - How to Run the Demo Server

This guide provides step-by-step instructions for running the Chennai Local Guide demo server.

## 🚀 Quick Start (Choose One Method)

### Method 1: One-Click Startup Scripts

**Windows Users:**
1. Double-click `start_server.bat`
2. Wait for the browser to open automatically
3. Start exploring Chennai slang and neighborhoods!

**Mac/Linux Users:**
```bash
./start_server.sh
```

**All Platforms:**
```bash
python start_server.py
```

### Method 2: Manual Setup

```bash
# 1. Install dependencies
pip install -e .

# 2. Start the server
python -m chennai_guide.web.server
```

## 🌐 Accessing the Application

Once the server starts, you'll see:
```
🎬 Chennai Local Guide server starting on port 8000
📍 Web interface: http://localhost:8000
🔧 API endpoint: http://localhost:8000/api/query?q=your_query
❤️  Health check: http://localhost:8000/api/health
```

**Open your browser and go to:** http://localhost:8000

## 🎯 How to Use

### Web Interface Features

1. **Main Search Box:**
   - Type any Chennai slang term: "What does semma mean?"
   - Ask about neighborhoods: "Where to film food content?"
   - Multi-intent queries: "What is machaan and where to use it?"

2. **Quick Example Buttons:**
   - Click preset buttons for instant results
   - Examples: "semma meaning?", "food spots?", "Marina Beach?"

3. **Results Display:**
   - **Slang Results:** Definition, usage example, vlogger tips
   - **Neighborhood Results:** Vibe, best content types, Google Maps links
   - **Insider Tips:** Local knowledge for authentic content

### API Usage

**Query Endpoint:**
```bash
# GET request
curl "http://localhost:8000/api/query?q=What does semma mean?"

# POST request
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Where to film cultural content?"}'
```

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

## 🛠️ Configuration Options

### Command Line Arguments

```bash
python start_server.py --help

Options:
  --port PORT        Port number (default: 8000)
  --no-browser       Don't open browser automatically
  --dev              Development mode with auto-install
  --check            Check installation status
```

### Examples

```bash
# Custom port
python start_server.py --port 3000

# No browser opening
python start_server.py --no-browser

# Development mode
python start_server.py --dev
```

## 📁 Project Structure

```
chennai_guide/
├── 🌐 Web Interface
│   ├── server.py          # Main web server
│   ├── index.html         # Frontend interface
│   └── *.js, *.css       # Frontend assets
├── 🧠 Core Components
│   ├── parsers/           # Context parsing
│   ├── processors/        # Query processing
│   └── models/           # Data models
├── 🚀 Startup Scripts
│   ├── start_server.py    # Cross-platform
│   ├── start_server.bat   # Windows
│   └── start_server.sh    # Unix/Linux/macOS
└── 📋 Configuration
    ├── server_config.json # Server settings
    └── DEPLOYMENT.md      # Deployment guide
```

## 🔧 Troubleshooting

### Common Issues & Solutions

**❌ "Module not found" error:**
```bash
# Solution: Install in development mode
pip install -e .
# Or use: python start_server.py --dev
```

**❌ "Port 8000 already in use":**
```bash
# Solution: Use different port
python start_server.py --port 3000
```

**❌ "Backend components not available":**
- Check that `product.md` exists in project root
- Verify all Python files are present
- Run: `python start_server.py --check`

**❌ Browser doesn't open:**
```bash
# Solution: Open manually
python start_server.py --no-browser
# Then visit: http://localhost:8000
```

### Health Check

Always check the health endpoint first:
```bash
curl http://localhost:8000/api/health
```

Expected response:
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

## 🎬 Demo Scenarios

### Scenario 1: Slang Translation
1. Type: "What does machaan mean?"
2. See definition, usage example, and vlogger tip
3. Try: "semma vera level gethu" for multiple terms

### Scenario 2: Neighborhood Discovery
1. Type: "Where to film food content?"
2. Get ranked neighborhood recommendations
3. Click Google Maps links to explore locations

### Scenario 3: Multi-Intent Queries
1. Type: "What is thala and where to use it in Chennai?"
2. Get both slang translation and location suggestions
3. Perfect for comprehensive content planning

## 🐳 Performance Notes

- **Startup Time:** ~2-3 seconds
- **Memory Usage:** ~50-100MB
- **Response Time:** <100ms for most queries
- **Concurrent Users:** Supports 10-20 concurrent users

## 🔒 Security Considerations

⚠️ **This is a demo server** - not production-ready:
- No authentication required
- CORS enabled for all origins
- Basic error handling only
- HTTP only (no HTTPS)

For production use, implement proper security measures.

## 📞 Support

If you encounter issues:

1. **Check Health:** `curl http://localhost:8000/api/health`
2. **Review Logs:** Check console output for errors
3. **Verify Files:** Ensure all required files are present
4. **Test Simple Query:** Try "What does semma mean?"

## 🎉 Success!

When everything is working, you should see:
- ✅ Server starts without errors
- ✅ Browser opens to the interface
- ✅ Health check returns "healthy"
- ✅ Sample queries return results
- ✅ Google Maps links work

**Happy content creating in Chennai! 🎬🌟**