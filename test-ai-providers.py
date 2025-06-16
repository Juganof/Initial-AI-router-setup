#!/usr/bin/env python3
"""
Standalone AI Provider Test Script
Tests the three AI providers directly to verify your API keys work.
"""

import os
import json
import requests
import time
from datetime import datetime

# Load environment variables from .env file
def load_env():
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print("❌ .env file not found!")
        return None
    return env_vars

def test_github_models(token, prompt="Hello! Please introduce yourself briefly."):
    """Test GitHub Models API"""
    print("\n🔧 Testing GitHub Models...")
    
    if not token or token == "your_github_token_here":
        print("❌ GitHub token not set in .env file")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "model": "gpt-4o",
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and result['choices']:
                print("✅ GitHub Models: SUCCESS")
                print(f"   Response: {result['choices'][0]['message']['content'][:100]}...")
                print(f"   Model: {result.get('model', 'gpt-4o')}")
                return True
        
        print(f"❌ GitHub Models failed: {response.status_code} - {response.text}")
        return False
        
    except Exception as e:
        print(f"❌ GitHub Models error: {str(e)}")
        return False

def test_openrouter(api_key, prompt="Hello! Please introduce yourself briefly."):
    """Test OpenRouter API"""
    print("\n🔧 Testing OpenRouter...")
    
    if not api_key or api_key == "your_openrouter_key_here":
        print("❌ OpenRouter API key not set in .env file")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://n8n-ai-test.local",
        "X-Title": "N8N AI Test",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and result['choices']:
                print("✅ OpenRouter: SUCCESS")
                print(f"   Response: {result['choices'][0]['message']['content'][:100]}...")
                print(f"   Model: {result.get('model', 'llama-3.1-8b')}")
                return True
        
        print(f"❌ OpenRouter failed: {response.status_code} - {response.text}")
        return False
        
    except Exception as e:
        print(f"❌ OpenRouter error: {str(e)}")
        return False

def test_google_gemini(api_key, prompt="Hello! Please introduce yourself briefly."):
    """Test Google Gemini API"""
    print("\n🔧 Testing Google Gemini...")
    
    if not api_key or api_key == "your_google_key_here":
        print("❌ Google API key not set in .env file")
        return False
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 100,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}",
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and result['candidates']:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    print("✅ Google Gemini: SUCCESS")
                    print(f"   Response: {candidate['content']['parts'][0]['text'][:100]}...")
                    print(f"   Model: gemini-1.5-flash")
                    return True
        
        print(f"❌ Google Gemini failed: {response.status_code} - {response.text}")
        return False
        
    except Exception as e:
        print(f"❌ Google Gemini error: {str(e)}")
        return False

def main():
    print("🚀 AI Provider Test Script")
    print("=" * 50)
    print(f"Started at: {datetime.now()}")
    
    # Load environment variables
    env_vars = load_env()
    if not env_vars:
        return
    
    # Test each provider
    github_success = test_github_models(env_vars.get('GITHUB_TOKEN', ''))
    time.sleep(2)  # Rate limiting courtesy
    
    openrouter_success = test_openrouter(env_vars.get('OPENROUTER_API_KEY', ''))
    time.sleep(2)  # Rate limiting courtesy
    
    gemini_success = test_google_gemini(env_vars.get('GOOGLE_API_KEY', ''))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"  GitHub Models: {'✅ Working' if github_success else '❌ Failed'}")
    print(f"  OpenRouter:    {'✅ Working' if openrouter_success else '❌ Failed'}")
    print(f"  Google Gemini: {'✅ Working' if gemini_success else '❌ Failed'}")
    
    working_count = sum([github_success, openrouter_success, gemini_success])
    print(f"\n🎯 {working_count}/3 providers are working!")
    
    if working_count > 0:
        print("\n✅ Your AI rotation system will work! At least one provider is functional.")
        print("💡 You can proceed with setting up n8n once Docker Desktop is fixed.")
    else:
        print("\n❌ No providers are working. Please check your API keys in the .env file.")
    
    print("\n🔧 Next steps:")
    if working_count > 0:
        print("  1. Fix Docker Desktop (restart, reinstall, or update)")
        print("  2. Run 'docker-compose up -d' to start n8n")
        print("  3. Import the workflow files in n8n UI")
        print("  4. Test the full system")
    else:
        print("  1. Check your API keys in .env file")
        print("  2. Verify your accounts have the correct permissions")
        print("  3. Try the individual provider websites to test keys")

if __name__ == "__main__":
    main()