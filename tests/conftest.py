"""Test configuration and fixtures for Chennai Local Guide tests."""

import pytest
from hypothesis import settings, Verbosity

# Configure Hypothesis for property-based testing
# Set minimum iterations to 100 as specified in design document
settings.register_profile("default", max_examples=100, verbosity=Verbosity.normal)
settings.load_profile("default")


@pytest.fixture
def sample_slang_data():
    """Sample Chennai slang data for testing."""
    return [
        {
            "term": "machaan",
            "definition": "Friend or buddy",
            "usage_example": "Hey machaan, let's go to Marina Beach",
            "vlogger_tip": "Use this casually when addressing friends in your vlogs"
        },
        {
            "term": "semma",
            "definition": "Awesome or excellent",
            "usage_example": "That biryani was semma!",
            "vlogger_tip": "Perfect for expressing excitement about food or experiences"
        }
    ]


@pytest.fixture
def sample_neighborhood_data():
    """Sample Chennai neighborhood data for testing."""
    return [
        {
            "name": "T. Nagar",
            "vibe": "Bustling shopping district",
            "best_for_content": ["shopping", "street food", "cultural"],
            "insider_tips": ["Visit early morning to avoid crowds", "Try the local street food"],
            "content_tags": ["shopping", "food", "culture"],
            "google_maps_link": "https://maps.google.com/tnagar-chennai",
            "coordinates": {"lat": 13.0418, "lng": 80.2341}
        },
        {
            "name": "Marina Beach",
            "vibe": "Scenic waterfront with local life",
            "best_for_content": ["scenic", "lifestyle", "sunset"],
            "insider_tips": ["Best lighting during golden hour", "Watch local fishermen"],
            "content_tags": ["scenic", "lifestyle", "beach"],
            "google_maps_link": "https://maps.google.com/marina-beach-chennai",
            "coordinates": {"lat": 13.0475, "lng": 80.2824}
        }
    ]