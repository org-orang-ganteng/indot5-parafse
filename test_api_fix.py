#!/usr/bin/env python3
"""
Test script untuk memverifikasi perbaikan JSON response
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    """Test health check endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Health check passed\n")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}\n")
        return False

def test_paraphrase_endpoint():
    """Test paraphrase endpoint with valid data"""
    print("Testing /paraphrase endpoint with valid data...")
    try:
        data = {
            "text": "Ini adalah contoh kalimat untuk diparafrasekan.",
            "method": "hybrid",
            "num_variations": 3,
            "min_quality": 0.6,
            "max_length": 200,
            "temperature": 1.0
        }
        response = requests.post(
            f"{BASE_URL}/paraphrase",
            headers={"Content-Type": "application/json"},
            json=data
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response keys: {result.keys()}")
        if response.status_code == 200:
            print(f"Generated {len(result.get('paraphrases', []))} paraphrases")
            print("✅ Paraphrase test passed\n")
            return True
        else:
            print(f"❌ Error: {result.get('error')}\n")
            return False
    except Exception as e:
        print(f"❌ Paraphrase test failed: {e}\n")
        return False

def test_paraphrase_empty_text():
    """Test paraphrase endpoint with empty text"""
    print("Testing /paraphrase endpoint with empty text...")
    try:
        data = {
            "text": "",
            "method": "hybrid"
        }
        response = requests.post(
            f"{BASE_URL}/paraphrase",
            headers={"Content-Type": "application/json"},
            json=data
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if response.status_code == 400 and 'error' in result:
            print("✅ Empty text validation passed\n")
            return True
        else:
            print("❌ Should return 400 error\n")
            return False
    except Exception as e:
        print(f"❌ Empty text test failed: {e}\n")
        return False

def test_paraphrase_no_json():
    """Test paraphrase endpoint without JSON data"""
    print("Testing /paraphrase endpoint without JSON...")
    try:
        response = requests.post(
            f"{BASE_URL}/paraphrase",
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if response.status_code == 400 and 'error' in result:
            print("✅ No JSON validation passed\n")
            return True
        else:
            print("❌ Should return 400 error\n")
            return False
    except Exception as e:
        print(f"❌ No JSON test failed: {e}\n")
        return False

def test_invalid_endpoint():
    """Test invalid endpoint"""
    print("Testing invalid endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/invalid-endpoint")
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if response.status_code == 404 and 'error' in result:
            print("✅ 404 handler passed\n")
            return True
        else:
            print("❌ Should return 404 error\n")
            return False
    except Exception as e:
        print(f"❌ Invalid endpoint test failed: {e}\n")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Testing API JSON Response Fixes")
    print("="*60 + "\n")
    
    tests = [
        test_health_endpoint,
        test_paraphrase_endpoint,
        test_paraphrase_empty_text,
        test_paraphrase_no_json,
        test_invalid_endpoint
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("="*60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("="*60)
    
    if all(results):
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")

if __name__ == "__main__":
    main()
