#!/usr/bin/env python3
"""Test script for Chennai Local Guide integration."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

try:
    from chennai_guide.local_guide import create_chennai_guide
    
    print("🎬 Chennai Local Guide - Integration Test")
    print("=" * 50)
    
    # Test 1: Create guide instance
    print("Test 1: Creating guide instance...")
    guide = create_chennai_guide(log_level="ERROR")  # Reduce log noise
    print("✓ Guide created successfully")
    
    # Test 2: Check system status
    print("\nTest 2: Checking system status...")
    status = guide.get_system_status()
    print(f"Status: {status['status']}")
    print(f"Components ready: {sum(1 for comp in status['components'].values() if comp['ready'])}/{len(status['components'])}")
    
    # Test 3: Process a simple query
    print("\nTest 3: Processing test query...")
    response = guide.process_query("What does machaan mean?")
    print(f"Query type: {response.query_type}")
    print(f"Results count: {len(response.results)}")
    print(f"Content creator note: {response.content_creator_note[:100]}...")
    
    # Test 4: Process neighborhood query
    print("\nTest 4: Processing neighborhood query...")
    response = guide.process_query("Best places for food content")
    print(f"Query type: {response.query_type}")
    print(f"Results count: {len(response.results)}")
    print(f"Maps links: {len(response.maps_links)}")
    
    print("\n✅ All integration tests passed!")
    print(f"Total queries processed: {guide.query_count}")
    
except Exception as e:
    print(f"❌ Integration test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)