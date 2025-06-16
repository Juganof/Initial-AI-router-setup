# Troubleshooting Guide - AI Model Rotation System

This guide helps you diagnose and resolve common issues with the n8n AI rotation system.

## 🚨 Quick Diagnostics

### System Health Check

Run these commands to check system status:

```bash
# Check if n8n is running
docker-compose ps

# Check n8n logs
docker-compose logs -f n8n

# Check database
docker exec n8n-ai-router sqlite3 /home/node/.n8n/database.sqlite "SELECT * FROM provider_status;"

# Test webhook endpoint
curl -X POST http://localhost:5678/webhook/ai-request \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test", "model_type": "chat"}'
```

## ❌ Common Error Messages

### 1. "Workflow not found" or "Webhook not responding"

**Symptoms:**
- HTTP 404 when calling webhook
- "Cannot GET /webhook/ai-request" error

**Causes & Solutions:**

**A. Workflow not activated:**
```bash
# Solution: Activate workflows in n8n UI
# 1. Go to n8n web interface (http://localhost:5678)
# 2. Open "AI Router - Main" workflow
# 3. Click the "Activate" toggle (should turn blue)
# 4. Do the same for "Provider Status Manager"
```

**B. Webhook URL changed:**
```bash
# Check webhook URL in n8n UI
# Go to "AI Router - Main" workflow
# Click on "AI Request Webhook" node
# Copy the correct webhook URL
```

**C. n8n not running:**
```bash
# Restart n8n
docker-compose restart n8n

# Or start fresh
docker-compose down && docker-compose up -d
```

### 2. "Authentication failed" or API Key Errors

**Symptoms:**
- "Invalid API key" in logs
- "Unauthorized" responses from providers
- All providers failing immediately

**Solutions:**

**A. Check environment variables:**
```bash
# Verify API keys are loaded
docker exec n8n-ai-router env | grep -E "(GITHUB|OPENROUTER|GOOGLE)"

# If empty, check your .env file
cat .env
```

**B. Restart after .env changes:**
```bash
# Always restart after changing .env
docker-compose down
docker-compose up -d
```

**C. Validate individual API keys:**

**GitHub Token:**
```bash
curl -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  https://api.github.com/user
```

**OpenRouter Key:**
```bash
curl -H "Authorization: Bearer YOUR_OPENROUTER_KEY" \
  https://openrouter.ai/api/v1/models
```

**Google API Key:**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_GOOGLE_KEY"
```

### 3. "All providers failed or rate limited"

**Symptoms:**
- HTTP 503 responses
- "All providers failed" message
- Long response times

**Diagnosis:**
```bash
# Check provider status
docker-compose logs n8n | grep "Provider Status Check"

# Check database directly
docker exec n8n-ai-router sqlite3 /home/node/.n8n/database.sqlite \
  "SELECT provider, available, last_failed, recovery_time FROM provider_status;"
```

**Solutions:**

**A. Wait for recovery:**
- GitHub Models: 1 hour
- OpenRouter: 15 minutes  
- Google Gemini: 1 minute

**B. Reset provider status:**
```sql
-- Reset all providers to available
UPDATE provider_status SET available = 1, recovery_time = NULL;
```

**C. Check rate limits:**
- Reduce request frequency
- Use lower max_tokens
- Implement delays between requests

### 4. Database Issues

**Symptoms:**
- "Database locked" errors
- "Table doesn't exist" errors
- Provider status not persisting

**Solutions:**

**A. Reset database:**
```bash
# Stop n8n
docker-compose down

# Remove database volume
docker volume rm n8n-ai-router_n8n_data

# Start fresh
docker-compose up -d
```

**B. Fix permissions:**
```bash
# Check database file permissions
docker exec n8n-ai-router ls -la /home/node/.n8n/

# Fix if needed
docker exec n8n-ai-router chown node:node /home/node/.n8n/database.sqlite
```

### 5. Memory/Performance Issues

**Symptoms:**
- Slow responses
- n8n crashes
- High CPU usage

**Solutions:**

**A. Increase Docker memory:**
```yaml
# In docker-compose.yml, add to n8n service:
services:
  n8n:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

**B. Optimize requests:**
- Use smaller max_tokens values
- Reduce request frequency
- Implement request queuing

## 🔍 Debugging Techniques

### Enable Debug Logging

**Method 1: Environment Variable**
```bash
# Add to .env file
N8N_LOG_LEVEL=debug

# Restart n8n
docker-compose restart n8n
```

**Method 2: Temporary Debug**
```bash
# Restart with debug logging
docker-compose down
N8N_LOG_LEVEL=debug docker-compose up -d
```

### Monitor Workflow Execution

**In n8n UI:**
1. Go to "Executions" tab
2. Click on failed executions
3. Examine each node's input/output
4. Look for error messages in red nodes

**Via Logs:**
```bash
# Watch logs in real-time
docker-compose logs -f n8n | grep -E "(ERROR|WARN|webhook)"
```

### Test Individual Components

**Test Webhook Trigger:**
```bash
curl -X POST http://localhost:5678/webhook/test-trigger \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

**Test Database Connection:**
```bash
docker exec n8n-ai-router sqlite3 /home/node/.n8n/database.sqlite ".tables"
```

**Test API Providers Individually:**

Create temporary test workflows for each provider to isolate issues.

## 🛠️ Advanced Troubleshooting

### Network Issues

**Port Conflicts:**
```bash
# Check if port 5678 is in use
netstat -tlnp | grep 5678

# Use different port if needed
# Change docker-compose.yml: "5679:5678"
```

**DNS/Connectivity:**
```bash
# Test from inside container
docker exec n8n-ai-router curl -I https://api.github.com
docker exec n8n-ai-router curl -I https://openrouter.ai
docker exec n8n-ai-router curl -I https://generativelanguage.googleapis.com
```

### Workflow Import Issues

**JSON Format Errors:**
- Check for trailing commas
- Validate JSON syntax: `cat workflow.json | jq .`
- Re-export workflows from working n8n instance

**Version Compatibility:**
- Ensure n8n version supports all node types
- Update to latest n8n version: `docker-compose pull n8n`

### Provider-Specific Issues

**GitHub Models:**
- Verify GitHub Pro for Students is active
- Check token scopes include repository access
- Ensure using correct API endpoint

**OpenRouter:**
- Verify account has free credits
- Check model availability: some models may be temporarily unavailable
- Try different free models

**Google Gemini:**
- Verify API key is for correct project
- Check quota limits in Google Cloud Console
- Ensure Gemini API is enabled

## 📋 Diagnostic Checklist

When reporting issues, please provide:

- [ ] n8n version: `docker exec n8n-ai-router n8n --version`
- [ ] Docker version: `docker --version`
- [ ] Operating system
- [ ] Complete error messages from logs
- [ ] Steps to reproduce the issue
- [ ] Workflow execution details
- [ ] Provider status from database
- [ ] Environment variable configuration (without actual keys)

### Collect Diagnostic Information

```bash
#!/bin/bash
# diagnostic_report.sh - Run this to collect troubleshooting info

echo "=== n8n AI Router Diagnostic Report ==="
echo "Generated: $(date)"
echo ""

echo "=== Docker Status ==="
docker-compose ps
echo ""

echo "=== n8n Version ==="
docker exec n8n-ai-router n8n --version 2>/dev/null || echo "n8n not responding"
echo ""

echo "=== Environment Check ==="
echo "GitHub Token: $(docker exec n8n-ai-router env | grep GITHUB_TOKEN | cut -d= -f1)=$(docker exec n8n-ai-router env | grep GITHUB_TOKEN | cut -d= -f2 | cut -c1-8)..."
echo "OpenRouter Key: $(docker exec n8n-ai-router env | grep OPENROUTER_API_KEY | cut -d= -f1)=$(docker exec n8n-ai-router env | grep OPENROUTER_API_KEY | cut -d= -f2 | cut -c1-8)..."
echo "Google Key: $(docker exec n8n-ai-router env | grep GOOGLE_API_KEY | cut -d= -f1)=$(docker exec n8n-ai-router env | grep GOOGLE_API_KEY | cut -d= -f2 | cut -c1-8)..."
echo ""

echo "=== Provider Status ==="
docker exec n8n-ai-router sqlite3 /home/node/.n8n/database.sqlite \
  "SELECT provider, available, priority, total_requests, failed_requests, recovery_time FROM provider_status;" 2>/dev/null || echo "Database not accessible"
echo ""

echo "=== Recent Logs (Last 50 lines) ==="
docker-compose logs --tail=50 n8n
echo ""

echo "=== Webhook Test ==="
curl -s -X POST http://localhost:5678/webhook/ai-request \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test", "model_type": "chat", "max_tokens": 10}' | jq . 2>/dev/null || echo "Webhook test failed"
```

## 🆘 Getting Help

If you've tried all troubleshooting steps:

1. **Check the logs first**: Most issues are visible in n8n logs
2. **Verify API keys**: Ensure all three providers have valid keys
3. **Test providers individually**: Use curl to test each API directly
4. **Check provider status pages**: GitHub, OpenRouter, and Google may have outages
5. **Reset and retry**: Sometimes a fresh start resolves issues

### Support Channels

- n8n Community: [community.n8n.io](https://community.n8n.io)
- n8n Documentation: [docs.n8n.io](https://docs.n8n.io)
- GitHub Issues (for provider-specific problems)
- Provider Support (for API key/quota issues)

Remember: This system is designed to be resilient. If one provider fails, others should take over automatically. Focus on getting at least one provider working, then troubleshoot others individually.