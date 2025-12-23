"""Hypothesis generators for property-based testing."""

from hypothesis import strategies as st
from chennai_guide.models.data_models import SlangTerm, Neighborhood


# Text generators for slang testing
@st.composite
def slang_text(draw):
    """Generate text that may contain Chennai slang terms."""
    slang_terms = ["machaan", "semma", "thala", "anna", "akka"]
    regular_words = ["hello", "world", "Chennai", "food", "beach", "temple"]
    
    # Generate a mix of slang and regular words
    words = draw(st.lists(
        st.one_of(
            st.sampled_from(slang_terms),
            st.sampled_from(regular_words)
        ),
        min_size=1,
        max_size=10
    ))
    
    return " ".join(words)


# Content type generators
content_types = st.sampled_from([
    "food", "shopping", "scenic", "cultural", "nightlife", 
    "art", "temple", "beach", "street", "lifestyle"
])

content_preferences = st.lists(content_types, min_size=1, max_size=3, unique=True)


# Query generators
@st.composite
def natural_language_query(draw):
    """Generate natural language queries for intent analysis."""
    query_templates = [
        "What does {slang} mean?",
        "Translate {slang} for me",
        "Where should I film {content} content?",
        "Best neighborhoods for {content}",
        "I want to create {content} videos",
        "Show me {content} places in Chennai"
    ]
    
    template = draw(st.sampled_from(query_templates))
    
    if "{slang}" in template:
        slang = draw(st.sampled_from(["machaan", "semma", "thala"]))
        return template.format(slang=slang)
    elif "{content}" in template:
        content = draw(content_types)
        return template.format(content=content)
    
    return template


# Data model generators
@st.composite
def slang_term_generator(draw):
    """Generate valid SlangTerm instances."""
    return SlangTerm(
        term=draw(st.text(min_size=1, max_size=20)),
        definition=draw(st.text(min_size=5, max_size=100)),
        usage_example=draw(st.text(min_size=10, max_size=150)),
        vlogger_tip=draw(st.text(min_size=10, max_size=200))
    )


@st.composite
def neighborhood_generator(draw):
    """Generate valid Neighborhood instances."""
    return Neighborhood(
        name=draw(st.text(min_size=1, max_size=50)),
        vibe=draw(st.text(min_size=5, max_size=100)),
        best_for_content=draw(st.lists(content_types, min_size=1, max_size=5, unique=True)),
        insider_tips=draw(st.lists(st.text(min_size=5, max_size=100), min_size=1, max_size=3)),
        content_tags=draw(st.lists(content_types, min_size=1, max_size=5, unique=True)),
        google_maps_link=draw(st.text(min_size=10, max_size=200)),
        coordinates=draw(st.dictionaries(
            st.sampled_from(["lat", "lng"]),
            st.floats(min_value=-90, max_value=90),
            min_size=2,
            max_size=2
        ))
    )