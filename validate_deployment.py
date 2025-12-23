#!/usr/bin/env python3
"""
Chennai Local Guide - Deployment Validation Script

This script validates that the demo server deployment is working correctly.
"""

import sys
import time
import subprocess
import requests
import json
from pathlib import Path

def check_files():
    """Check that all required files are present."""
    required_files = [
        'start_server.py',
        'start_server.bat',
        'start_server.sh',
        'server_config.json',
        'DEPLOYMENT.md',
        'RUN_SERVER.md',
        'chennai_guide/web/server.py',
        'chennai_guide/web/index.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files are present")
    return True

def test_server_startup():
    """Test that the server can start successfully."""
    print("🚀 Testing server startup...")
    
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, 'start_server.py', 
            '--no-browser', '--port', '8002'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False
        
        print("✅ Server started successfully")
        
        # Test health endpoint
        try:
            response = requests.get('http://localhost:8002/api/health', timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Health check passed: {health_data['status']}")
                
                # Test main interface
                response = requests.get('http://localhost:8002/', timeout=5)
                if response.status_code == 200 and 'Chennai Local Guide' in response.text:
                    print("✅ Web interface is accessible")
                else:
                    print("❌ Web interface not accessible")
                    return False
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"❌ Failed to connect to server: {e}")
            return False
        finally:
            # Clean up
            process.terminate()
            process.wait()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints with a temporary server."""
    print("🔧 Testing API endpoints...")
    
    try:
        # Start server
        process = subprocess.Popen([
            sys.executable, 'start_server.py', 
            '--no-browser', '--port', '8003'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        if process.poll() is not None:
            print("❌ Could not start server for API testing")
            return False
        
        base_url = 'http://localhost:8003'
        
        # Test query endpoint
        try:
            response = requests.get(f'{base_url}/api/query?q=test', timeout=5)
            if response.status_code == 200:
                print("✅ Query endpoint responding")
            else:
                print(f"❌ Query endpoint failed: {response.status_code}")
                return False
        except requests.RequestException:
            print("❌ Query endpoint not accessible")
            return False
        
        # Test browse endpoint
        try:
            response = requests.get(f'{base_url}/api/browse', timeout=5)
            if response.status_code == 200:
                print("✅ Browse endpoint responding")
            else:
                print(f"❌ Browse endpoint failed: {response.status_code}")
        except requests.RequestException:
            print("❌ Browse endpoint not accessible")
        
        # Test inspiration endpoint
        try:
            response = requests.get(f'{base_url}/api/inspiration', timeout=5)
            if response.status_code == 200:
                print("✅ Inspiration endpoint responding")
            else:
                print(f"❌ Inspiration endpoint failed: {response.status_code}")
        except requests.RequestException:
            print("❌ Inspiration endpoint not accessible")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False
    finally:
        if 'process' in locals():
            process.terminate()
            process.wait()

def validate_configuration():
    """Validate configuration files."""
    print("⚙️  Validating configuration...")
    
    try:
        with open('server_config.json', 'r') as f:
            config = json.load(f)
        
        required_keys = ['server', 'paths', 'api', 'logging']
        for key in required_keys:
            if key not in config:
                print(f"❌ Missing configuration key: {key}")
                return False
        
        print("✅ Configuration file is valid")
        return True
        
    except json.JSONDecodeError:
        print("❌ Configuration file has invalid JSON")
        return False
    except FileNotFoundError:
        print("❌ Configuration file not found")
        return False

def main():
    """Run all validation tests."""
    print("🎬 Chennai Local Guide - Deployment Validation")
    print("=" * 50)
    
    tests = [
        ("File Presence", check_files),
        ("Configuration", validate_configuration),
        ("Server Startup", test_server_startup),
        ("API Endpoints", test_api_endpoints)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test passed")
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Deployment is ready.")
        print("\n🚀 To start the server:")
        print("   python start_server.py")
        print("   or double-click start_server.bat (Windows)")
        print("   or ./start_server.sh (Unix/Linux/macOS)")
        return True
    else:
        print(f"\n❌ {total - passed} tests failed. Please fix issues before deployment.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)