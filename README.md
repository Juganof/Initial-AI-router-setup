# 🤖 n8n AI Model Rotation System

A robust, automated AI model rotation system for n8n that intelligently switches between free AI providers when rate limits are hit. Perfect for powering all your n8n automations with reliable AI responses.

## 🌟 Features

- **Automatic Failover**: Seamlessly switches between providers when rate limits are reached
- **Multiple AI Providers**: GitHub Models (with Pro benefits), OpenRouter, and Google Gemini
- **Smart Recovery**: Automatically re-enables providers when rate limits reset
- **Centralized API**: Single webhook endpoint for all your n8n workflows
- **Usage Analytics**: Track performance and usage across all providers
- **Easy Integration**: Drop-in replacement for direct AI API calls

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo> n8n-ai-router
cd n8n-ai-router
cp .env.example .env
```

### 2. Configure API Keys
Edit `.env` with your API keys:
```env
GITHUB_TOKEN=your_github_token_here
OPENROUTER_API_KEY=your_openrouter_key_here  
GOOGLE_API_KEY=your_google_key_here
```

### 3. Start the System
```bash
docker-compose up -d
```

### 4. Access n8n
Open [http://localhost:5678](http://localhost:5678) and import the workflow files.

### 5. Test the API
```bash
curl -X POST http://localhost:5678/webhook/ai-request \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello! How are you?", "model_type": "chat"}'
```

## 📁 Project Structure

```
n8n-ai-router/
├── 📋 ai-rotation-plan.md           # Detailed architecture plan
├── 🔧 n8n-ai-router-main.json      # Main AI routing workflow
├── 📊 n8n-provider-status-manager.json # Provider status management
├── 🐳 docker-compose.yml           # n8n deployment configuration
├── 🔑 .env.example                 # Environment variables template
├── 📖 setup-guide.md               # Step-by-step setup instructions
├── 💡 api-usage-examples.md        # Integration examples for workflows
├── 🔧 troubleshooting.md           # Common issues and solutions
└── 📄 README.md                    # This file
```

## 🎯 How It Works

### Provider Priority System
1. **GitHub Models** (Primary) - Best quality, enhanced limits with Pro
2. **OpenRouter** (Secondary) - Good fallback with multiple models  
3. **Google Gemini** (Tertiary) - Fast responses for simple tasks

### Automatic Rotation
```
AI Request → GitHub Available? → Use GitHub Models
           ↓ No
           → OpenRouter Available? → Use OpenRouter  
           ↓ No
           → Gemini Available? → Use Google Gemini
           ↓ No
           → All Providers Down (Error)
```

### Rate Limit Recovery
- **GitHub Models**: 1 hour cooldown
- **OpenRouter**: 15 minutes cooldown
- **Google Gemini**: 1 minute cooldown

## 🔌 API Reference

### Request Format
```json
{
  "prompt": "Your AI request here",
  "model_type": "chat|code|creative",
  "max_tokens": 1000,
  "temperature": 0.7,
  "system_prompt": "Optional system instructions"
}
```

### Response Format
```json
{
  "success": true,
  "response": "AI generated response",
  "provider": "github_models",
  "model": "gpt-4o",
  "tokens_used": 150,
  "processing_time": 2.3,
  "request_id": "abc123"
}
```

## 🎨 Model Types

| Type | Best For | Temperature | Example |
|------|----------|-------------|---------|
| `chat` | Q&A, support, conversation | 0.3-0.7 | Customer service responses |
| `code` | Programming, debugging | 0.1-0.4 | Code generation and review |
| `creative` | Writing, marketing | 0.7-1.0 | Content creation |

## 🔗 Integration Examples

### Email Summarizer
```javascript
// n8n HTTP Request node
{
  "url": "http://localhost:5678/webhook/ai-request",
  "method": "POST",
  "body": {
    "prompt": "Summarize this email: {{ $json.emailText }}",
    "model_type": "chat",
    "max_tokens": 200
  }
}
```

### Code Review Bot
```javascript
{
  "prompt": "Review this code: {{ $json.code }}",
  "model_type": "code", 
  "temperature": 0.3,
  "system_prompt": "You are a senior developer. Focus on security and best practices."
}
```

### Content Generator
```javascript
{
  "prompt": "Create social media posts for: {{ $json.blogPost }}",
  "model_type": "creative",
  "temperature": 0.8
}
```

## 📊 Monitoring

### Provider Status
Check provider availability every 5 minutes via logs:
```bash
docker-compose logs -f n8n | grep "Provider Status Check"
```

### Database Queries
```sql
-- Check provider status
SELECT provider, available, total_requests, failed_requests 
FROM provider_status;

-- View recovery times
SELECT provider, recovery_time 
FROM provider_status 
WHERE available = 0;
```

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub Personal Access Token | ✅ |
| `OPENROUTER_API_KEY` | OpenRouter API key | ✅ |
| `GOOGLE_API_KEY` | Google AI Studio API key | ✅ |
| `N8N_USER` | n8n admin username | ✅ |
| `N8N_PASSWORD` | n8n admin password | ✅ |

## 🔧 Troubleshooting

### Quick Diagnostics
```bash
# Check system status
docker-compose ps

# View logs
docker-compose logs -f n8n

# Test webhook
curl -X POST http://localhost:5678/webhook/ai-request \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test", "model_type": "chat"}'
```

### Common Issues
- **Webhook not found**: Ensure workflows are activated
- **API key errors**: Check `.env` file and restart n8n
- **Rate limits**: System automatically handles rotation
- **Database issues**: Reset with `docker-compose down && docker volume rm n8n-ai-router_n8n_data`

See [`troubleshooting.md`](troubleshooting.md) for detailed solutions.

## 📚 Documentation

- [`setup-guide.md`](setup-guide.md) - Complete setup instructions
- [`api-usage-examples.md`](api-usage-examples.md) - Integration examples
- [`troubleshooting.md`](troubleshooting.md) - Common issues and solutions
- [`ai-rotation-plan.md`](ai-rotation-plan.md) - Detailed architecture plan

## 🚀 Getting Started

1. **Follow the [Setup Guide](setup-guide.md)** for step-by-step instructions
2. **Review [API Examples](api-usage-examples.md)** for integration patterns
3. **Test the system** with the provided curl commands
4. **Integrate with your workflows** using the centralized webhook

## 🤝 Contributing

This system is designed to be easily extensible. To add new AI providers:

1. Add provider configuration to the main workflow
2. Update the routing logic in the "Route to Provider" node
3. Add provider-specific API request formatting
4. Update recovery timers in the status manager

## 📄 License

This project is open source. Use it freely for your automation needs!

---

**Ready to supercharge your n8n automations with reliable AI?** Start with the [Setup Guide](setup-guide.md)!