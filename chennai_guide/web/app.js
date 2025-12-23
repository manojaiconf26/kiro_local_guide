/**
 * Enhanced Chennai Local Guide Web Application
 * Provides advanced query processing, error handling, and API integration
 */

class ChennaiLocalGuide {
    constructor() {
        this.apiEndpoint = '/api/query';
        this.healthEndpoint = '/api/health';
        this.isBackendAvailable = false;
        this.queryHistory = [];
        this.maxHistorySize = 10;
        this.helpSystem = new ChennaiGuideHelp();
        
        this.init();
    }
    
    async init() {
        this.setupEventListeners();
        await this.checkBackendHealth();
        this.loadQueryHistory();
        this.setupKeyboardShortcuts();
    }
    
    setupEventListeners() {
        const queryInput = document.getElementById('queryInput');
        const searchButton = document.querySelector('.btn-primary');
        
        // Enter key submission
        queryInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.processQuery();
            }
        });
        
        // Search button click
        searchButton.addEventListener('click', () => {
            this.processQuery();
        });
        
        // Auto-focus on input
        queryInput.focus();
        
        // Clear button (if query is not empty)
        queryInput.addEventListener('input', (e) => {
            this.toggleClearButton(e.target.value);
        });
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K to focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                document.getElementById('queryInput').focus();
            }
            
            // Escape to clear results
            if (e.key === 'Escape') {
                this.clearResults();
            }
        });
    }
    
    async checkBackendHealth() {
        try {
            const response = await fetch(this.healthEndpoint);
            if (response.ok) {
                const health = await response.json();
                this.isBackendAvailable = health.backend_available;
                console.log('Backend health:', health);
            }
        } catch (error) {
            console.log('Backend not available, using frontend-only mode');
            this.isBackendAvailable = false;
        }
    }
    
    toggleClearButton(value) {
        const inputGroup = document.querySelector('.input-group');
        let clearButton = document.getElementById('clearButton');
        
        if (value && !clearButton) {
            clearButton = document.createElement('button');
            clearButton.id = 'clearButton';
            clearButton.className = 'btn btn-secondary';
            clearButton.innerHTML = '✕';
            clearButton.title = 'Clear input';
            clearButton.onclick = () => this.clearInput();
            inputGroup.appendChild(clearButton);
        } else if (!value && clearButton) {
            clearButton.remove();
        }
    }
    
    clearInput() {
        document.getElementById('queryInput').value = '';
        document.getElementById('clearButton')?.remove();
        document.getElementById('queryInput').focus();
    }
    
    clearResults() {
        const resultsDiv = document.getElementById('results');
        resultsDiv.style.display = 'none';
        resultsDiv.innerHTML = '';
    }
    
    setQuery(query) {
        document.getElementById('queryInput').value = query;
        this.processQuery();
    }
    
    async processQuery() {
        const query = document.getElementById('queryInput').value.trim();
        
        // Validate query first
        const validation = this.validateQuery(query);
        if (!validation.isValid) {
            this.showError(validation.errors[0]);
            return;
        }
        
        // Show warnings if any
        if (validation.warnings.length > 0) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            let warningHTML = validation.warnings.map(warning => 
                `<div class="warning-message">⚠️ ${warning}</div>`
            ).join('');
            
            if (validation.suggestions.length > 0) {
                warningHTML += `<div class="info-message">💡 ${validation.suggestions.join(' ')}</div>`;
            }
            
            resultsDiv.innerHTML = warningHTML;
            
            // Still process the query after showing warnings
            setTimeout(() => {
                this.continueProcessing(query);
            }, 2000);
            return;
        }
        
        this.continueProcessing(query);
    }
    
    async continueProcessing(query) {
        this.addToHistory(query);
        this.showLoading();
        
        try {
            let result;
            if (this.isBackendAvailable) {
                result = await this.processWithBackend(query);
            } else {
                result = await this.processWithFrontend(query);
            }
            
            this.displayResults(result, query);
        } catch (error) {
            console.error('Query processing error:', error);
            this.showError('Sorry, there was an error processing your query. Please try again.');
        }
    }
    
    async processWithBackend(query) {
        const response = await fetch(this.apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }
        
        return await response.json();
    }
    
    async processWithFrontend(query) {
        // Simulate processing delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        const queryLower = query.toLowerCase();
        
        // Check for multi-intent queries
        const hasSlangKeywords = ['meaning', 'what does', 'what is', 'translate', 'explain', 'definition'].some(keyword => queryLower.includes(keyword));
        const hasNeighborhoodKeywords = ['neighborhood', 'area', 'where', 'visit', 'film', 'shoot', 'spot', 'place', 'location'].some(keyword => queryLower.includes(keyword));
        
        if (hasSlangKeywords && hasNeighborhoodKeywords) {
            return {
                intent: 'multi_intent',
                slang_results: this.translateSlang(query),
                neighborhood_results: this.getNeighborhoodRecommendations(query)
            };
        } else if (hasSlangKeywords || this.containsKnownSlang(query)) {
            return {
                intent: 'slang',
                results: this.translateSlang(query)
            };
        } else {
            return {
                intent: 'neighborhood',
                results: this.getNeighborhoodRecommendations(query)
            };
        }
    }
    
    containsKnownSlang(query) {
        const queryLower = query.toLowerCase();
        return Object.keys(window.chennaiContext.slang).some(term => queryLower.includes(term));
    }
    
    translateSlang(query) {
        const queryLower = query.toLowerCase();
        const foundSlang = [];
        
        for (const [term, info] of Object.entries(window.chennaiContext.slang)) {
            if (queryLower.includes(term)) {
                foundSlang.push({
                    term: term,
                    ...info
                });
            }
        }
        
        return foundSlang;
    }
    
    getNeighborhoodRecommendations(query) {
        const queryLower = query.toLowerCase();
        const recommendations = [];
        
        // Content type scoring
        const contentTypes = {
            food: ['food', 'eat', 'restaurant', 'cafe', 'dining', 'street food', 'dosa', 'biryani'],
            cultural: ['culture', 'temple', 'heritage', 'traditional', 'classical', 'spiritual'],
            scenic: ['view', 'photo', 'scenic', 'sunset', 'beach', 'beautiful', 'nature'],
            shopping: ['shopping', 'market', 'bazaar', 'buy', 'mall'],
            trendy: ['trendy', 'modern', 'cafe', 'young', 'hip'],
            peaceful: ['peaceful', 'quiet', 'calm', 'nature', 'relax']
        };
        
        for (const [key, neighborhood] of Object.entries(window.chennaiContext.neighborhoods)) {
            let score = 0;
            
            // Direct name match gets highest score
            if (queryLower.includes(key) || queryLower.includes(neighborhood.name.toLowerCase())) {
                score += 10;
            }
            
            // Score based on content type match
            for (const [type, keywords] of Object.entries(contentTypes)) {
                if (keywords.some(keyword => queryLower.includes(keyword))) {
                    if (neighborhood.tags.includes(type) || 
                        keywords.some(keyword => neighborhood.best_for.toLowerCase().includes(keyword))) {
                        score += 3;
                    }
                }
            }
            
            // Score based on vibe match
            const vibeWords = neighborhood.vibe.toLowerCase().split(' ');
            vibeWords.forEach(word => {
                if (queryLower.includes(word)) {
                    score += 2;
                }
            });
            
            if (score > 0) {
                recommendations.push({
                    ...neighborhood,
                    score: score
                });
            }
        }
        
        // If no specific matches, return all neighborhoods sorted by general relevance
        if (recommendations.length === 0) {
            return Object.values(window.chennaiContext.neighborhoods).slice(0, 3);
        }
        
        // Sort by score and return top 3
        return recommendations
            .sort((a, b) => b.score - a.score)
            .slice(0, 3);
    }
    
    showLoading() {
        const resultsDiv = document.getElementById('results');
        resultsDiv.style.display = 'block';
        resultsDiv.innerHTML = '<div class="loading">🔍 Analyzing your Chennai query...</div>';
    }
    
    displayResults(result, originalQuery) {
        const resultsDiv = document.getElementById('results');
        
        if (result.intent === 'multi_intent') {
            let html = '';
            
            if (result.slang_results && result.slang_results.length > 0) {
                html += '<h3>🗣️ Chennai Slang Translation:</h3>';
                result.slang_results.forEach(slang => {
                    html += this.createSlangResultHTML(slang);
                });
            }
            
            if (result.neighborhood_results && result.neighborhood_results.length > 0) {
                html += '<h3 style="margin-top: 30px;">🏙️ Perfect Neighborhoods for Your Content:</h3>';
                result.neighborhood_results.forEach((neighborhood, index) => {
                    html += this.createNeighborhoodResultHTML(neighborhood, index);
                });
            }
            
            resultsDiv.innerHTML = html;
            
        } else if (result.intent === 'slang') {
            if (!result.results || result.results.length === 0) {
                this.showNoSlangResults(originalQuery);
            } else {
                let html = '<h3>🗣️ Chennai Slang Translation:</h3>';
                result.results.forEach(slang => {
                    html += this.createSlangResultHTML(slang);
                });
                resultsDiv.innerHTML = html;
            }
        } else if (result.intent === 'neighborhood') {
            if (!result.results || result.results.length === 0) {
                this.showNoNeighborhoodResults(originalQuery);
            } else {
                let html = '<h3>🏙️ Perfect Chennai Neighborhoods for Your Content:</h3>';
                result.results.forEach((neighborhood, index) => {
                    html += this.createNeighborhoodResultHTML(neighborhood, index);
                });
                resultsDiv.innerHTML = html;
            }
        }
    }
    
    createSlangResultHTML(slang) {
        return `
            <div class="slang-result">
                <div class="slang-term">"${slang.term}"</div>
                <div class="slang-definition">${slang.definition}</div>
                ${slang.usage ? `<div class="slang-usage">💬 Example: "${slang.usage}"</div>` : ''}
                ${slang.vlogger_tip ? `<div class="vlogger-tip">💡 Content Creator Tip: ${slang.vlogger_tip}</div>` : ''}
            </div>
        `;
    }
    
    createNeighborhoodResultHTML(neighborhood, index) {
        return `
            <div class="neighborhood-result">
                <div class="neighborhood-name">${index !== undefined ? (index + 1) + '. ' : ''}${neighborhood.name}</div>
                <div class="neighborhood-vibe">✨ Vibe: ${neighborhood.vibe}</div>
                <div class="neighborhood-best-for">🎬 Perfect for: ${neighborhood.best_for}</div>
                ${neighborhood.insider_tip ? `<div class="insider-tip">💡 Insider Tip: ${neighborhood.insider_tip}</div>` : ''}
                ${neighborhood.google_maps_link ? `<a href="${neighborhood.google_maps_link}" target="_blank" class="maps-link">📍 Open in Google Maps</a>` : ''}
            </div>
        `;
    }
    
    showNoSlangResults(query) {
        const helpData = this.helpSystem.getErrorRecoveryHelp('no_slang_found', query);
        const helpHTML = this.helpSystem.generateHelpHTML(helpData);
        
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `
            <div class="no-results">
                🤔 No Chennai slang detected in your query.
            </div>
            ${helpHTML}
        `;
    }
    
    showNoNeighborhoodResults(query) {
        const helpData = this.helpSystem.getErrorRecoveryHelp('no_neighborhoods_found', query);
        const helpHTML = this.helpSystem.generateHelpHTML(helpData);
        
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `
            <div class="no-results">
                🏙️ No specific neighborhood matches found for your query.
            </div>
            ${helpHTML}
        `;
    }
    
    showError(message) {
        const resultsDiv = document.getElementById('results');
        resultsDiv.style.display = 'block';
        
        // Determine error type based on message
        let errorType = 'general';
        if (message.includes('server') || message.includes('backend') || message.includes('processing')) {
            errorType = 'server_error';
        }
        
        const helpData = this.helpSystem.getErrorRecoveryHelp(errorType, '');
        const helpHTML = this.helpSystem.generateHelpHTML(helpData);
        
        resultsDiv.innerHTML = `
            <div class="error-message">${message}</div>
            ${helpHTML}
        `;
    }
    
    addToHistory(query) {
        // Remove if already exists
        this.queryHistory = this.queryHistory.filter(q => q !== query);
        // Add to beginning
        this.queryHistory.unshift(query);
        // Limit size
        if (this.queryHistory.length > this.maxHistorySize) {
            this.queryHistory = this.queryHistory.slice(0, this.maxHistorySize);
        }
        this.saveQueryHistory();
    }
    
    saveQueryHistory() {
        try {
            localStorage.setItem('chennai_guide_history', JSON.stringify(this.queryHistory));
        } catch (error) {
            console.log('Could not save query history:', error);
        }
    }
    
    loadQueryHistory() {
        try {
            const saved = localStorage.getItem('chennai_guide_history');
            if (saved) {
                this.queryHistory = JSON.parse(saved);
            }
        } catch (error) {
            console.log('Could not load query history:', error);
            this.queryHistory = [];
        }
    }
    
    showHelp() {
        const resultsDiv = document.getElementById('results');
        resultsDiv.style.display = 'block';
        
        const helpData = this.helpSystem.getErrorRecoveryHelp('general', '');
        const helpHTML = this.helpSystem.generateHelpHTML(helpData);
        
        resultsDiv.innerHTML = `
            <div class="info-message">
                <strong>🎬 Welcome to Chennai Local Guide!</strong><br>
                I can help you understand Chennai slang and find perfect neighborhoods for content creation.
            </div>
            ${helpHTML}
        `;
    }
    
    handleAmbiguousQuery(query) {
        const resultsDiv = document.getElementById('results');
        resultsDiv.style.display = 'block';
        
        const helpData = this.helpSystem.getErrorRecoveryHelp('ambiguous_query', query);
        const helpHTML = this.helpSystem.generateHelpHTML(helpData);
        
        resultsDiv.innerHTML = `
            <div class="warning-message">
                Your query "${query}" could mean several things. Let me help you be more specific:
            </div>
            ${helpHTML}
        `;
    }
    
    validateQuery(query) {
        const validation = {
            isValid: true,
            errors: [],
            warnings: [],
            suggestions: []
        };
        
        // Check for empty query
        if (!query || query.trim().length === 0) {
            validation.isValid = false;
            validation.errors.push('Please enter a query to search');
            return validation;
        }
        
        // Check for very short queries
        if (query.trim().length < 2) {
            validation.isValid = false;
            validation.errors.push('Please enter a more detailed query');
            validation.suggestions.push('Try asking "What does [term] mean?" or "Where to film [content type]?"');
            return validation;
        }
        
        // Check for common city name mistakes
        const queryLower = query.toLowerCase();
        const otherCities = ['mumbai', 'delhi', 'bangalore', 'kolkata', 'hyderabad', 'pune'];
        const mentionedCity = otherCities.find(city => queryLower.includes(city));
        
        if (mentionedCity) {
            validation.warnings.push(`This guide is specifically for Chennai, not ${mentionedCity.charAt(0).toUpperCase() + mentionedCity.slice(1)}`);
            validation.suggestions.push('Try asking about Chennai neighborhoods or Tamil slang instead');
        }
        
        // Check for very long queries
        if (query.length > 200) {
            validation.warnings.push('Your query is quite long. Try breaking it into smaller, more specific questions');
        }
        
        return validation;
    }
}

// Global functions for backward compatibility
function setQuery(query) {
    if (window.app) {
        window.app.setQuery(query);
    }
}

function processQuery() {
    if (window.app) {
        window.app.processQuery();
    }
}

function showHelp() {
    if (window.app) {
        window.app.showHelp();
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ChennaiLocalGuide();
});

// Chennai context data (same as in HTML file)
window.chennaiContext = {
    slang: {
        'machaan': {
            definition: 'Friend, buddy (used between close friends)',
            usage: 'Machaan, let\'s go to Marina Beach',
            vlogger_tip: 'Perfect for showing local friendship culture, use when interacting with locals'
        },
        'semma': {
            definition: 'Awesome, excellent, amazing',
            usage: 'That dosa was semma!',
            vlogger_tip: 'Great for food reactions, shows you appreciate local cuisine authentically'
        },
        'vera level': {
            definition: 'Next level, extraordinary',
            usage: 'This temple architecture is vera level',
            vlogger_tip: 'Use for genuine amazement at Chennai\'s culture and landmarks'
        },
        'gethu': {
            definition: 'Style, swag, attitude',
            usage: 'His dance moves have so much gethu',
            vlogger_tip: 'Perfect for cultural content, especially during festivals or performances'
        },
        'thala': {
            definition: 'Leader, boss (term of respect)',
            usage: 'Thala knows the best filter coffee spot',
            vlogger_tip: 'Shows respect for local knowledge, great for interviewing locals'
        },
        'mokka': {
            definition: 'Boring, lame, not interesting',
            usage: 'That movie was total mokka',
            vlogger_tip: 'Use sparingly, shows you understand local criticism culture'
        },
        'scene': {
            definition: 'Situation, what\'s happening',
            usage: 'What\'s the scene at Express Avenue?',
            vlogger_tip: 'Great for asking about local happenings or events'
        },
        'apdiye': {
            definition: 'Just like that, casually',
            usage: 'Apdiye we went to Pondy Bazaar',
            vlogger_tip: 'Shows casual, local way of speaking about activities'
        }
    },
    neighborhoods: {
        't nagar': {
            name: 'T. Nagar',
            vibe: 'Bustling shopping paradise, traditional meets modern',
            best_for: 'Shopping hauls, street food, cultural immersion',
            google_maps_link: 'https://maps.google.com/maps?q=T.+Nagar,+Chennai',
            insider_tip: 'Early morning (7-9am) for less crowded shots, evening (5-7pm) for authentic local energy',
            tags: ['shopping', 'food', 'traditional', 'bustling']
        },
        'marina beach': {
            name: 'Marina Beach Area',
            vibe: 'Scenic coastline, evening hangout spot, local life',
            best_for: 'Sunset shots, local lifestyle, street food',
            google_maps_link: 'https://maps.google.com/maps?q=Marina+Beach,+Chennai',
            insider_tip: 'Golden hour (6-7pm) is magical, avoid midday heat',
            tags: ['scenic', 'beach', 'sunset', 'street food']
        },
        'mylapore': {
            name: 'Mylapore',
            vibe: 'Cultural heart, traditional Tamil culture, spiritual',
            best_for: 'Temple visits, classical arts, heritage walks',
            google_maps_link: 'https://maps.google.com/maps?q=Mylapore,+Chennai',
            insider_tip: 'Festival seasons (Dec-Jan) offer incredible cultural content',
            tags: ['cultural', 'spiritual', 'traditional', 'heritage']
        },
        'besant nagar': {
            name: 'Besant Nagar (Bessy)',
            vibe: 'Coastal, trendy, young crowd, cafe culture',
            best_for: 'Beach lifestyle, cafes, modern Chennai',
            google_maps_link: 'https://maps.google.com/maps?q=Besant+Nagar,+Chennai',
            insider_tip: 'Weekend mornings for joggers and local life, evenings for cafe culture',
            tags: ['trendy', 'cafe', 'beach', 'modern']
        },
        'royapettah': {
            name: 'Royapettah',
            vibe: 'Diverse, multicultural, food paradise',
            best_for: 'Street food tours, cultural diversity',
            google_maps_link: 'https://maps.google.com/maps?q=Royapettah,+Chennai',
            insider_tip: 'Lunch time (12-2pm) for authentic food culture',
            tags: ['diverse', 'food', 'multicultural', 'street food']
        },
        'adyar': {
            name: 'Adyar',
            vibe: 'Upscale residential, river views, peaceful',
            best_for: 'Nature in city, upscale lifestyle, peaceful moments',
            google_maps_link: 'https://maps.google.com/maps?q=Adyar,+Chennai',
            insider_tip: 'Early morning for nature content, evening for upscale dining',
            tags: ['upscale', 'peaceful', 'nature', 'residential']
        }
    }
};