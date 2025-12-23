/**
 * Help system and user guidance for Chennai Local Guide
 * Provides contextual help, examples, and error recovery suggestions
 */

class ChennaiGuideHelp {
    constructor() {
        this.helpExamples = {
            slang: [
                "What does semma mean?",
                "Explain machaan",
                "What is vera level?",
                "Translate gethu",
                "What does thala mean?",
                "Define apdiye"
            ],
            neighborhood: [
                "Where to film food content in Chennai?",
                "Best cultural neighborhoods?",
                "Scenic spots for content creation?",
                "Traditional areas in Chennai?",
                "Where to shoot street food videos?",
                "Best neighborhoods for temple content?"
            ],
            mixed: [
                "What does semma mean and where to film food content?",
                "Explain machaan and recommend cultural areas",
                "Best neighborhoods for using gethu in content"
            ]
        };
        
        this.commonMistakes = {
            'madras': 'Chennai (locals prefer "Chennai" over "Madras")',
            'bombay': 'Mumbai (you might be thinking of a different city)',
            'delhi': 'New Delhi (this guide is specifically for Chennai)',
            'bangalore': 'Bengaluru (this guide is specifically for Chennai)',
            'kolkata': 'Kolkata (this guide is specifically for Chennai)'
        };
        
        this.suggestionPatterns = {
            food: ['food', 'eat', 'restaurant', 'dosa', 'biryani', 'coffee', 'meal'],
            culture: ['culture', 'temple', 'traditional', 'heritage', 'classical'],
            beach: ['beach', 'ocean', 'sea', 'water', 'marina', 'coastal'],
            shopping: ['shopping', 'market', 'buy', 'bazaar', 'mall'],
            modern: ['modern', 'trendy', 'cafe', 'hip', 'contemporary']
        };
    }
    
    analyzeQuery(query) {
        const queryLower = query.toLowerCase();
        const analysis = {
            hasSlangIntent: false,
            hasNeighborhoodIntent: false,
            detectedTopics: [],
            commonMistakes: [],
            suggestions: []
        };
        
        // Check for slang intent
        const slangKeywords = ['meaning', 'what does', 'what is', 'translate', 'explain', 'definition', 'define'];
        analysis.hasSlangIntent = slangKeywords.some(keyword => queryLower.includes(keyword));
        
        // Check for neighborhood intent
        const neighborhoodKeywords = ['where', 'neighborhood', 'area', 'place', 'location', 'film', 'shoot', 'visit'];
        analysis.hasNeighborhoodIntent = neighborhoodKeywords.some(keyword => queryLower.includes(keyword));
        
        // Detect topics
        for (const [topic, keywords] of Object.entries(this.suggestionPatterns)) {
            if (keywords.some(keyword => queryLower.includes(keyword))) {
                analysis.detectedTopics.push(topic);
            }
        }
        
        // Check for common mistakes
        for (const [mistake, correction] of Object.entries(this.commonMistakes)) {
            if (queryLower.includes(mistake)) {
                analysis.commonMistakes.push({ mistake, correction });
            }
        }
        
        return analysis;
    }
    
    generateSuggestions(query, analysis) {
        const suggestions = [];
        
        // If no clear intent, suggest both types
        if (!analysis.hasSlangIntent && !analysis.hasNeighborhoodIntent) {
            suggestions.push({
                type: 'intent_clarification',
                title: 'What are you looking for?',
                options: [
                    { text: 'Learn Chennai slang meanings', examples: this.helpExamples.slang.slice(0, 3) },
                    { text: 'Find neighborhoods for content', examples: this.helpExamples.neighborhood.slice(0, 3) },
                    { text: 'Both slang and locations', examples: this.helpExamples.mixed.slice(0, 2) }
                ]
            });
        }
        
        // Topic-based suggestions
        if (analysis.detectedTopics.length > 0) {
            const topicSuggestions = this.getTopicSuggestions(analysis.detectedTopics);
            if (topicSuggestions.length > 0) {
                suggestions.push({
                    type: 'topic_suggestions',
                    title: 'Related suggestions based on your interests:',
                    options: topicSuggestions
                });
            }
        }
        
        // Common mistakes corrections
        if (analysis.commonMistakes.length > 0) {
            suggestions.push({
                type: 'corrections',
                title: 'Did you mean:',
                options: analysis.commonMistakes.map(mistake => ({
                    text: mistake.correction,
                    note: `Instead of "${mistake.mistake}"`
                }))
            });
        }
        
        return suggestions;
    }
    
    getTopicSuggestions(topics) {
        const suggestions = [];
        
        if (topics.includes('food')) {
            suggestions.push({
                text: 'Best food neighborhoods in Chennai',
                query: 'Where to film food content in Chennai?'
            });
            suggestions.push({
                text: 'Learn food-related Chennai slang',
                query: 'What does semma mean?'
            });
        }
        
        if (topics.includes('culture')) {
            suggestions.push({
                text: 'Cultural neighborhoods for content',
                query: 'Best cultural neighborhoods in Chennai?'
            });
            suggestions.push({
                text: 'Traditional Chennai expressions',
                query: 'What does thala mean?'
            });
        }
        
        if (topics.includes('beach')) {
            suggestions.push({
                text: 'Beach areas for filming',
                query: 'Marina Beach filming spots'
            });
            suggestions.push({
                text: 'Coastal neighborhoods',
                query: 'Besant Nagar content creation'
            });
        }
        
        if (topics.includes('shopping')) {
            suggestions.push({
                text: 'Shopping districts for content',
                query: 'T Nagar shopping content'
            });
        }
        
        if (topics.includes('modern')) {
            suggestions.push({
                text: 'Trendy neighborhoods',
                query: 'Modern Chennai neighborhoods for content'
            });
        }
        
        return suggestions;
    }
    
    getErrorRecoveryHelp(errorType, originalQuery) {
        const help = {
            type: errorType,
            suggestions: []
        };
        
        switch (errorType) {
            case 'no_slang_found':
                help.title = 'No Chennai slang detected';
                help.message = 'Try asking about specific Tamil/Chennai terms or phrases you\'ve heard.';
                help.suggestions = [
                    { text: 'Popular Chennai slang terms', examples: this.helpExamples.slang },
                    { text: 'How to ask about slang', examples: ['What does [term] mean?', 'Explain [phrase]', 'Translate [word]'] }
                ];
                break;
                
            case 'no_neighborhoods_found':
                help.title = 'No matching neighborhoods found';
                help.message = 'Try being more specific about the type of content you want to create.';
                help.suggestions = [
                    { text: 'Content type examples', examples: this.helpExamples.neighborhood },
                    { text: 'Specific neighborhood queries', examples: ['Marina Beach content', 'T Nagar filming', 'Mylapore temples'] }
                ];
                break;
                
            case 'ambiguous_query':
                help.title = 'Your query could mean several things';
                help.message = 'Try being more specific about what you\'re looking for.';
                help.suggestions = [
                    { text: 'For slang translation', examples: this.helpExamples.slang.slice(0, 3) },
                    { text: 'For location recommendations', examples: this.helpExamples.neighborhood.slice(0, 3) }
                ];
                break;
                
            case 'server_error':
                help.title = 'Something went wrong';
                help.message = 'There was a technical issue. You can still use the basic features.';
                help.suggestions = [
                    { text: 'Try these working examples', examples: [...this.helpExamples.slang.slice(0, 2), ...this.helpExamples.neighborhood.slice(0, 2)] }
                ];
                break;
                
            default:
                help.title = 'Need help?';
                help.message = 'Here are some things you can try:';
                help.suggestions = [
                    { text: 'Ask about Chennai slang', examples: this.helpExamples.slang.slice(0, 3) },
                    { text: 'Find content creation spots', examples: this.helpExamples.neighborhood.slice(0, 3) }
                ];
        }
        
        return help;
    }
    
    generateHelpHTML(helpData) {
        let html = `
            <div class="help-container">
                <h4>${helpData.title}</h4>
                <p>${helpData.message}</p>
        `;
        
        helpData.suggestions.forEach(suggestion => {
            html += `
                <div class="help-section">
                    <h5>${suggestion.text}</h5>
                    <div class="help-examples">
            `;
            
            if (suggestion.examples) {
                suggestion.examples.forEach(example => {
                    if (typeof example === 'string') {
                        html += `<div class="help-example" onclick="app.setQuery('${example}')">${example}</div>`;
                    } else {
                        html += `<div class="help-example" onclick="app.setQuery('${example.query || example}')">${example.text || example}</div>`;
                    }
                });
            }
            
            html += `
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        return html;
    }
    
    showContextualHelp(query) {
        const analysis = this.analyzeQuery(query);
        const suggestions = this.generateSuggestions(query, analysis);
        
        if (suggestions.length > 0) {
            return this.generateSuggestionsHTML(suggestions);
        }
        
        return null;
    }
    
    generateSuggestionsHTML(suggestions) {
        let html = '<div class="contextual-help">';
        
        suggestions.forEach(suggestion => {
            html += `
                <div class="suggestion-group">
                    <h4>${suggestion.title}</h4>
            `;
            
            suggestion.options.forEach(option => {
                if (option.examples) {
                    html += `
                        <div class="suggestion-category">
                            <h5>${option.text}</h5>
                            <div class="suggestion-examples">
                    `;
                    option.examples.forEach(example => {
                        html += `<div class="suggestion-item" onclick="app.setQuery('${example}')">${example}</div>`;
                    });
                    html += '</div></div>';
                } else {
                    const query = option.query || option.text;
                    html += `<div class="suggestion-item" onclick="app.setQuery('${query}')">${option.text}</div>`;
                    if (option.note) {
                        html += `<div class="suggestion-note">${option.note}</div>`;
                    }
                }
            });
            
            html += '</div>';
        });
        
        html += '</div>';
        return html;
    }
}

// Export for use in main app
window.ChennaiGuideHelp = ChennaiGuideHelp;