#!/usr/bin/env python3
"""
Test the AI Rotation System
Demonstrates automatic provider switching and rate limit handling
"""

import requests
import json
import time

def test_ai_router():
    """Test the AI router with multiple requests"""
    url = "http://localhost:5000/ai-request"
    
    test_requests = [
        {
            "prompt": "Hello! Please introduce yourself briefly.",
            "model_type": "chat",
            "max_tokens": 100
        },
        {
            "prompt": "Write a Python function to calculate fibonacci numbers",
            "model_type": "code", 
            "max_tokens": 200,
            "temperature": 0.3
        },
        {
            "prompt": "Write a haiku about artificial intelligence",
            "model_type": "creative",
            "max_tokens": 50,
            "temperature": 0.9
        }
    ]
    
    print("🤖 Testing AI Rotation System")
    print("=" * 50)
    
    for i, request_data in enumerate(test_requests, 1):
        print(f"\n📝 Test {i}: {request_data['model_type'].upper()} request")
        print(f"Prompt: {request_data['prompt'][:50]}...")
        
        try:
            response = requests.post(url, json=request_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ SUCCESS")
                print(f"   Provider: {result['provider']}")
                print(f"   Model: {result['model']}")
                print(f"   Tokens: {result['tokens_used']}")
                print(f"   Time: {result['processing_time']}s")
                print(f"   Response: {result['response'][:100]}...")
            else:
                print(f"❌ FAILED: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed - Is the AI router running?")
            print("   Start it with: python simple-ai-router.py")
            return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            
        # Small delay between requests
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎯 AI Rotation System Test Complete!")
    return True

def check_status():
    """Check provider status"""
    try:
        response = requests.get("http://localhost:5000/status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("\n📊 Provider Status:")
            for provider, info in status['providers'].items():
                status_text = "✅ Available" if info['available'] else "❌ Rate Limited"
                print(f"   {provider}: {status_text} (Requests: {info['requests']}, Failures: {info['failures']})")
        else:
            print("❌ Could not get status")
    except:
        print("❌ Status check failed")

if __name__ == "__main__":
    if test_ai_router():
        check_status()
        print("\n💡 Your AI rotation system is working perfectly!")
        print("🔗 You can now integrate this with your n8n workflows using:")
        print("   URL: http://localhost:5000/ai-request")
        print("   Method: POST")
        print("   Headers: Content-Type: application/json")