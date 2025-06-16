#!/usr/bin/env python3
"""
Simple AI Router - Standalone Version
A lightweight version of the n8n AI rotation system that you can use right now.
"""

import os
import json
import requests
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# Provider status tracking
provider_status = {
    'github_models': {'available': True, 'recovery_time': None, 'requests': 0, 'failures': 0},
    'openrouter': {'available': True, 'recovery_time': None, 'requests': 0, 'failures': 0},
    'google_gemini': {'available': True, 'recovery_time': None, 'requests': 0, 'failures': 0}
}

# Recovery times for each provider (in minutes)
recovery_times = {
    'github_models': 60,  # 1 hour
    'openrouter': 15,     # 15 minutes  
    'google_gemini': 1    # 1 minute
}

def load_env():
    """Load environment variables from .env file or OS environment"""
    env_vars = {}
    
    # Try to load from .env file first (for local development)
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print("ℹ️ .env file not found, using environment variables")
    
    # Override with actual environment variables (for Railway deployment)
    env_vars['GITHUB_TOKEN'] = os.environ.get('GITHUB_TOKEN', env_vars.get('GITHUB_TOKEN'))
    env_vars['OPENROUTER_API_KEY'] = os.environ.get('OPENROUTER_API_KEY', env_vars.get('OPENROUTER_API_KEY'))
    env_vars['GOOGLE_API_KEY'] = os.environ.get('GOOGLE_API_KEY', env_vars.get('GOOGLE_API_KEY'))
    
    # Check if we have all required keys
    if not all([env_vars.get('GITHUB_TOKEN'), env_vars.get('OPENROUTER_API_KEY'), env_vars.get('GOOGLE_API_KEY')]):
        print("❌ Missing required environment variables!")
        return None
    
    return env_vars

def generate_request_id():
    """Generate a random request ID"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def check_recovery():
    """Check if any providers should be recovered from rate limiting"""
    current_time = datetime.now()
    for provider, status in provider_status.items():
        if not status['available'] and status['recovery_time']:
            if current_time >= status['recovery_time']:
                status['available'] = True
                status['recovery_time'] = None
                print(f"✅ {provider} recovered and available again")

def mark_provider_failed(provider, is_rate_limit=True):
    """Mark a provider as failed/rate limited"""
    provider_status[provider]['available'] = False
    provider_status[provider]['failures'] += 1
    
    if is_rate_limit:
        recovery_minutes = recovery_times.get(provider, 15)
        provider_status[provider]['recovery_time'] = datetime.now() + timedelta(minutes=recovery_minutes)
        print(f"⏰ {provider} rate limited, will recover in {recovery_minutes} minutes")
    else:
        print(f"❌ {provider} failed with error")

def get_available_provider():
    """Get the next available provider based on priority"""
    check_recovery()
    
    # Priority order
    priority = ['github_models', 'openrouter', 'google_gemini']
    
    for provider in priority:
        if provider_status[provider]['available']:
            return provider
    
    return None

def call_github_models(env_vars, prompt, system_prompt, max_tokens, temperature):
    """Call GitHub Models API"""
    headers = {
        "Authorization": f"Bearer {env_vars['GITHUB_TOKEN']}",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    data = {
        "messages": messages,
        "model": "gpt-4o",
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    response = requests.post(
        "https://models.inference.ai.azure.com/chat/completions",
        headers=headers,
        json=data,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        return {
            'success': True,
            'response': result['choices'][0]['message']['content'],
            'model': result.get('model', 'gpt-4o'),
            'tokens_used': result.get('usage', {}).get('total_tokens', 0)
        }
    else:
        return {'success': False, 'error': response.text, 'status_code': response.status_code}

def call_openrouter(env_vars, prompt, system_prompt, max_tokens, temperature):
    """Call OpenRouter API"""
    headers = {
        "Authorization": f"Bearer {env_vars['OPENROUTER_API_KEY']}",
        "HTTP-Referer": "https://n8n-ai-router.local",
        "X-Title": "N8N AI Router",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    data = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        return {
            'success': True,
            'response': result['choices'][0]['message']['content'],
            'model': result.get('model', 'llama-3.1-8b'),
            'tokens_used': result.get('usage', {}).get('total_tokens', 0)
        }
    else:
        return {'success': False, 'error': response.text, 'status_code': response.status_code}

def call_google_gemini(env_vars, prompt, system_prompt, max_tokens, temperature):
    """Call Google Gemini API"""
    full_prompt = prompt
    if system_prompt:
        full_prompt = f"{system_prompt}\n\n{prompt}"
    
    data = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": temperature
        }
    }
    
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={env_vars['GOOGLE_API_KEY']}",
        json=data,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        return {
            'success': True,
            'response': result['candidates'][0]['content']['parts'][0]['text'],
            'model': 'gemini-1.5-flash',
            'tokens_used': result.get('usageMetadata', {}).get('totalTokenCount', 0)
        }
    else:
        return {'success': False, 'error': response.text, 'status_code': response.status_code}

@app.route('/ai-request', methods=['POST'])
def ai_request():
    """Main AI request endpoint"""
    start_time = time.time()
    request_id = generate_request_id()
    
    try:
        data = request.get_json()
        
        # Extract parameters
        prompt = data.get('prompt', '')
        model_type = data.get('model_type', 'chat')
        max_tokens = min(data.get('max_tokens', 1000), 4000)
        temperature = max(0, min(data.get('temperature', 0.7), 1))
        system_prompt = data.get('system_prompt', '')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt is required',
                'request_id': request_id
            }), 400
        
        # Load environment variables
        env_vars = load_env()
        if not env_vars:
            return jsonify({
                'success': False,
                'error': 'Failed to load environment variables',
                'request_id': request_id
            }), 500
        
        # Try providers in order
        for attempt in range(3):  # Maximum 3 attempts
            provider = get_available_provider()
            
            if not provider:
                return jsonify({
                    'success': False,
                    'error': 'All providers are rate limited',
                    'message': 'Please try again later',
                    'request_id': request_id
                }), 503
            
            print(f"🔄 Attempt {attempt + 1}: Using {provider}")
            provider_status[provider]['requests'] += 1
            
            try:
                # Call the selected provider
                if provider == 'github_models':
                    result = call_github_models(env_vars, prompt, system_prompt, max_tokens, temperature)
                elif provider == 'openrouter':
                    result = call_openrouter(env_vars, prompt, system_prompt, max_tokens, temperature)
                elif provider == 'google_gemini':
                    result = call_google_gemini(env_vars, prompt, system_prompt, max_tokens, temperature)
                
                if result['success']:
                    processing_time = time.time() - start_time
                    return jsonify({
                        'success': True,
                        'response': result['response'],
                        'provider': provider,
                        'model': result['model'],
                        'tokens_used': result['tokens_used'],
                        'processing_time': round(processing_time, 2),
                        'request_id': request_id
                    })
                else:
                    # Check if it's a rate limit error
                    is_rate_limit = (
                        result['status_code'] == 429 or
                        'rate limit' in result['error'].lower() or
                        'quota' in result['error'].lower()
                    )
                    
                    mark_provider_failed(provider, is_rate_limit)
                    print(f"❌ {provider} failed: {result['error']}")
                    
            except Exception as e:
                mark_provider_failed(provider, False)
                print(f"❌ {provider} exception: {str(e)}")
                continue
        
        # All providers failed
        return jsonify({
            'success': False,
            'error': 'All providers failed',
            'message': 'Please try again later',
            'request_id': request_id
        }), 503
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'request_id': request_id
        }), 500

@app.route('/status', methods=['GET'])
def status():
    """Get provider status"""
    check_recovery()
    return jsonify({
        'providers': provider_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def home():
    """Simple home page"""
    return """
    <h1>🤖 AI Router - Simple Version</h1>
    <p>Your AI rotation system is running!</p>
    <h2>Endpoints:</h2>
    <ul>
        <li><strong>POST /ai-request</strong> - Main AI endpoint</li>
        <li><strong>GET /status</strong> - Provider status</li>
    </ul>
    <h2>Example Request:</h2>
    <pre>
curl -X POST http://localhost:5000/ai-request \\
  -H "Content-Type: application/json" \\
  -d '{"prompt": "Hello!", "model_type": "chat"}'
    </pre>
    """

if __name__ == '__main__':
    print("🚀 Starting Simple AI Router...")
    
    # Get port from environment (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    
    print(f"📍 Server will be available at: http://0.0.0.0:{port}")
    print(f"📖 API endpoint: /ai-request")
    print(f"📊 Status endpoint: /status")
    print("\n✅ Ready to serve AI requests!")
    print("🔄 Automatic rotation and rate limit handling enabled")
    print("\nPress Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=port, debug=False)