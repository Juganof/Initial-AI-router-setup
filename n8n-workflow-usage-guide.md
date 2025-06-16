# 🎯 n8n AI Rotation Workflow Usage Guide

## 📁 Ready-to-Import Workflows

I've created ready-to-use n8n workflows that demonstrate your AI rotation system:

### **1. Main Demo Workflow** 
**File:** [`n8n-ai-demo-workflow.json`](n8n-ai-demo-workflow.json:1)

This is your main demonstration workflow that shows how to use the AI rotation system in n8n.

## 🚀 How to Import and Use

### **Step 1: Import the Workflow**

1. **Start your AI rotation system:**
   ```bash
   python simple-ai-router.py
   ```

2. **Open n8n** (either via Docker or n8n Cloud)
   - Docker: http://localhost:5678
   - n8n Cloud: https://app.n8n.cloud

3. **Import the workflow:**
   - Click **"+ Add workflow"**
   - Click **"Import from file"**
   - Select [`n8n-ai-demo-workflow.json`](n8n-ai-demo-workflow.json:1)
   - Click **"Import"**

### **Step 2: Activate the Workflow**

1. Click the **"Activate"** toggle in the top right
2. The webhook will be automatically created

### **Step 3: Test the Workflow**

The workflow creates a webhook endpoint you can call with different AI request types:

#### **Basic Chat Request**
```bash
curl -X POST [YOUR_WEBHOOK_URL] \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "type": "chat"
  }'
```

#### **Code Generation Request**
```bash
curl -X POST [YOUR_WEBHOOK_URL] \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to validate email addresses",
    "type": "code"
  }'
```

#### **Creative Writing Request**
```bash
curl -X POST [YOUR_WEBHOOK_URL] \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short story about a robot learning to paint",
    "type": "creative"
  }'
```

#### **Email Writing Request**
```bash
curl -X POST [YOUR_WEBHOOK_URL] \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a professional email declining a meeting invitation",
    "type": "email"
  }'
```

#### **Document Summary Request**
```bash
curl -X POST [YOUR_WEBHOOK_URL] \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Summarize this report: [paste your document text here]",
    "type": "summary"
  }'
```

## 📊 Response Format

The workflow returns structured responses:

### **Success Response:**
```json
{
  "success": true,
  "data": {
    "request_type": "chat",
    "ai_response": "Quantum computing is a revolutionary technology...",
    "provider_used": "github_models",
    "model_used": "gpt-4o",
    "tokens_consumed": 145,
    "processing_time": 2.3,
    "request_id": "abc123"
  },
  "metadata": {
    "timestamp": "2024-01-01T12:00:00.000Z",
    "workflow": "ai-rotation-demo"
  }
}
```

### **Error Response:**
```json
{
  "success": false,
  "error": {
    "message": "All providers are rate limited",
    "provider_attempted": "github_models",
    "request_id": "def456"
  },
  "data": {
    "request_type": "chat",
    "original_prompt": "Your original prompt"
  },
  "metadata": {
    "timestamp": "2024-01-01T12:00:00.000Z",
    "workflow": "ai-rotation-demo"
  }
}
```

## 🎨 Request Types Available

The workflow automatically optimizes AI requests based on type:

| Type | Model Type | Temperature | System Prompt | Best For |
|------|------------|-------------|---------------|----------|
| `chat` | chat | 0.7 | Helpful AI assistant | Q&A, general conversation |
| `code` | code | 0.3 | Expert programmer | Code generation, debugging |
| `creative` | creative | 0.9 | Creative writer | Stories, poems, marketing copy |
| `email` | chat | 0.6 | Professional email assistant | Business emails, responses |
| `summary` | chat | 0.4 | Expert summarizer | Document summaries, reports |

## 🔧 Customizing the Workflow

### **Modifying Request Types**

Edit the **"Prepare AI Request"** node to add new request types:

```javascript
case 'translation':
  aiRequest.model_type = 'chat';
  aiRequest.temperature = 0.5;
  aiRequest.system_prompt = 'You are a professional translator. Provide accurate translations.';
  break;

case 'analysis':
  aiRequest.model_type = 'chat';
  aiRequest.temperature = 0.3;
  aiRequest.max_tokens = 800;
  aiRequest.system_prompt = 'You are a data analyst. Provide detailed analysis and insights.';
  break;
```

### **Changing AI Router URL**

If your AI rotation system runs on a different URL, update the **"Call AI Rotation System"** node:
- Change `http://localhost:5000/ai-request` to your URL
- For n8n Cloud, use a public URL or ngrok tunnel

### **Adding Error Handling**

The workflow already includes comprehensive error handling, but you can add:
- Retry logic for failed requests
- Fallback responses
- Notification systems

## 🌐 Using with n8n Cloud

If you're using n8n Cloud, you need to make your AI rotation system accessible:

### **Option 1: Use ngrok (Recommended for testing)**
```bash
# Install ngrok
npm install -g ngrok

# Start your AI router
python simple-ai-router.py

# In another terminal, expose it
ngrok http 5000
```

Then update the workflow URL to use your ngrok URL: `https://xyz.ngrok.io/ai-request`

### **Option 2: Deploy to Cloud**
Deploy your `simple-ai-router.py` to:
- Heroku
- Railway
- DigitalOcean App Platform
- AWS Lambda (with modifications)

## 🔄 Integration Patterns

### **Pattern 1: Direct Integration**
Use the HTTP Request node directly in any workflow:
```json
{
  "url": "http://localhost:5000/ai-request",
  "method": "POST",
  "body": {
    "prompt": "{{ $json.your_data }}",
    "model_type": "chat"
  }
}
```

### **Pattern 2: Subworkflow**
Create the demo workflow as a subworkflow and call it from other workflows using the "Execute Workflow" node.

### **Pattern 3: Function Node**
Create a reusable function node that formats AI requests:

```javascript
function callAI(prompt, type = 'chat', maxTokens = 500) {
  return {
    url: 'http://localhost:5000/ai-request',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: {
      prompt: prompt,
      model_type: type,
      max_tokens: maxTokens
    }
  };
}

// Usage
return callAI($json.user_message, 'chat');
```

## 📈 Monitoring and Analytics

The workflow tracks:
- Provider usage (which AI service was used)
- Token consumption
- Processing times
- Success/failure rates

You can extend this by:
- Logging to databases
- Creating dashboards
- Setting up alerts for failures

## 🎯 Real-World Use Cases

1. **Customer Support Bot**: Auto-respond to customer emails
2. **Content Generator**: Create social media posts from RSS feeds
3. **Code Review Assistant**: Analyze GitHub pull requests
4. **Document Processor**: Summarize uploaded documents
5. **Translation Service**: Multi-language content translation
6. **Data Analyzer**: Generate insights from CSV/JSON data

Your AI rotation system is now fully integrated with n8n and ready to power sophisticated automation workflows!