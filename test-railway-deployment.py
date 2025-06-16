#!/usr/bin/env python3
"""
Simple AI Router Test Script
Test your Railway deployment
"""

import requests
import json

def test_railway_deployment(base_url):
    """Test the deployed Railway app"""
    
    print(f"🧪 Testing Railway deployment at: {base_url}")
    print("=" * 60)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test 2: Status endpoint
    try:
        response = requests.get(f"{base_url}/status")
        if response.status_code == 200:
            status = response.json()
            print("✅ Status endpoint working")
            print(f"   Providers available: {len([p for p, s in status['providers'].items() if s['available']])}/3")
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Status endpoint error: {e}")
    
    # Test 3: AI request
    test_request = {
        "prompt": "Hello! This is a test message from your AI rotation system.",
        "model_type": "chat",
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai-request",
            headers={"Content-Type": "application/json"},
            json=test_request,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI request successful!")
            print(f"   Provider used: {result.get('provider')}")
            print(f"   Model: {result.get('model')}")
            print(f"   Response: {result.get('response', '')[:100]}...")
            print(f"   Processing time: {result.get('processing_time')}s")
        else:
            print(f"❌ AI request failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ AI request error: {e}")
    
    print("\n🎉 Testing complete!")
    print(f"🔗 Your AI router is ready at: {base_url}")
    print("\n📝 Example n8n Cloud usage:")
    print(f"   URL: {base_url}/ai-request")
    print("   Method: POST")
    print("   Body: " + json.dumps(test_request, indent=2))

if __name__ == "__main__":
    # Replace with your Railway URL
    railway_url = input("Enter your Railway URL (e.g., https://your-app.railway.app): ").strip()
    
    if railway_url:
        test_railway_deployment(railway_url)
    else:
        print("❌ Please provide a valid Railway URL")
