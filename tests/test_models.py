"""Unit tests for data models."""

import pytest
from chennai_guide.models.data_models import SlangTerm, Neighborhood, LocalGuideResponse


class TestSlangTerm:
    """Test SlangTerm data model."""
    
    def test_slang_term_creation(self):
        """Test creating a SlangTerm instance."""
        term = SlangTerm(
            term="machaan",
            definition="Friend or buddy",
            usage_example="Hey machaan, let's go to Marina Beach",
            vlogger_tip="Use this casually when addressing friends in your vlogs"
        )
        
        assert term.term == "machaan"
        assert term.definition == "Friend or buddy"
        assert term.usage_example == "Hey machaan, let's go to Marina Beach"
        assert term.vlogger_tip == "Use this casually when addressing friends in your vlogs"


class TestNeighborhood:
    """Test Neighborhood data model."""
    
    def test_neighborhood_creation(self):
        """Test creating a Neighborhood instance."""
        neighborhood = Neighborhood(
            name="T. Nagar",
            vibe="Bustling shopping district",
            best_for_content=["shopping", "street food"],
            insider_tips=["Visit early morning"],
            content_tags=["shopping", "food"],
            google_maps_link="https://maps.google.com/tnagar",
            coordinates={"lat": 13.0418, "lng": 80.2341}
        )
        
        assert neighborhood.name == "T. Nagar"
        assert neighborhood.vibe == "Bustling shopping district"
        assert "shopping" in neighborhood.best_for_content
        assert neighborhood.google_maps_link == "https://maps.google.com/tnagar"
        assert neighborhood.coordinates["lat"] == 13.0418


class TestLocalGuideResponse:
    """Test LocalGuideResponse data model."""
    
    def test_response_creation(self):
        """Test creating a LocalGuideResponse instance."""
        response = LocalGuideResponse(
            query_type="slang",
            results=[],
            content_creator_note="Test note",
            suggestions=["Try this", "Or that"],
            maps_links=[]
        )
        
        assert response.query_type == "slang"
        assert response.content_creator_note == "Test note"
        assert len(response.suggestions) == 2