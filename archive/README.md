# 🎬 Vlogger's Local Guide - NYC Edition

A hackathon project for "The Local Guide" theme - helping content creators navigate NYC like a local!

## What It Does

This tool helps vloggers and content creators:
- **Translate NYC slang** with context and usage tips
- **Find perfect neighborhoods** for different types of content
- **Get insider tips** for authentic, engaging vlogs

## Perfect For Vloggers Who Want To:
- Sound authentic when using local slang
- Find the best spots for food, art, or lifestyle content
- Understand local culture for better storytelling
- Create content that resonates with both locals and tourists

## Quick Start

```bash
python vlogger_guide.py
```

## Example Interactions

**Slang Translation:**
```
Vlogger Query: What does "deadass" mean and when should I use it?
🗣️ Slang Found:
  • 'deadass' = Seriously, for real. Used to emphasize truth or agreement.
    Example: "Deadass, that pizza spot is fire"
    💡 Vlogger Tip: Great for authentic reactions, use when genuinely surprised
```

**Neighborhood Recommendations:**
```
Vlogger Query: Where should I film food content?
🏙️ Top Neighborhood Recommendations:
  1. Chinatown
     Vibe: Authentic, bustling, food paradise
     Best for: Cultural immersion, street food, markets
  
  2. Lower East Side (LES)
     Vibe: Trendy, artsy, nightlife
     Best for: Street art, vintage shopping, food tours
```

## The Secret Sauce

All local knowledge comes from `product.md` - a curated guide that teaches Kiro about:
- NYC slang with vlogger-specific usage tips
- Neighborhood vibes and content opportunities
- Cultural nuances and filming etiquette
- Seasonal content ideas

## Why This Wins

1. **Solves Real Problems** - Vloggers actually need this authentic local knowledge
2. **Showcases Kiro's Context Learning** - Demonstrates how well Kiro can absorb and apply local culture
3. **Simple but Powerful** - Easy to demo, immediate value
4. **Scalable Concept** - Framework works for any city with the right product.md

## Technical Approach

- Python CLI tool that parses `product.md` for local context
- Smart query detection (slang vs. neighborhood requests)
- Relevance scoring for neighborhood recommendations
- Vlogger-specific tips and cultural insights

Built for the AWS Kiro IDE hackathon challenge! 🏆