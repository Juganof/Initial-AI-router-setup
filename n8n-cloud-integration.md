# 🌐 Using Your AI Rotation System with n8n Cloud

Yes! You can absolutely use your AI rotation system with n8n's web builder (n8n.cloud). Here are the best approaches:

## 🚀 Option 1: Cloud-Hosted AI Router (Recommended)

### **Deploy Your AI Router to the Cloud**

**A. Using Railway (Free Tier)**
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub account
3. Create new project from your AI router code
4. Set environment variables:
   ```
   GITHUB_TOKEN=your_token
   OPENROUTER_API_KEY=your_key
   GOOGLE_API_KEY=your_key
   PORT=5000
   ```
5. Deploy → Get your public URL (e.g., `https://your-app.railway.app`)

**B. Using Render (Free Tier)**
1. Go to [Render.com](https://render.com)
2. Create new Web Service from GitHub
3. Set build command: `pip install flask requests`
4. Set start command: `python simple-ai-router.py`
5. Add environment variables
6. Deploy → Get your public URL

**C. Using Heroku**
1. Create `requirements.txt`:
   ```
   flask>=2.0.0
   requests>=2.25.0
   ```
2. Create `Procfile`:
   ```
   web: python simple-ai-router.py
   ```
3. Deploy to Heroku → Get your app URL

### **Use in n8n Cloud**

Once deployed, use your public URL in n8n cloud workflows:

```
POST https://your-app.railway.app/ai-request
Content-Type: application/json

{
  "prompt": "Your AI request",
  "model_type": "chat",
  "max_tokens": 500
}
```

## 🔧 Option 2: Direct Integration in n8n Cloud

### **Create HTTP Request Nodes for Each Provider**

Instead of your local router, create n8n workflows that directly call the AI providers with your rotation logic:

**Workflow Structure:**
1. **HTTP Request (GitHub Models)** → Try first
2. **IF Node** → Check if successful
3. **HTTP Request (OpenRouter)** → Fallback 1
4. **IF Node** → Check if successful  
5. **HTTP Request (Google Gemini)** → Fallback 2

### **Example n8n Cloud Workflow:**

**Node 1: Try GitHub Models**
```json
{
  "method": "POST",
  "url": "https://models.inference.ai.azure.com/chat/completions",
  "headers": {
    "Authorization": "Bearer {{$env.GITHUB_TOKEN}}",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "{{$json.prompt}}"}],
    "max_tokens": "{{$json.max_tokens || 500}}"
  }
}
```

**Node 2: Check Success**
```javascript
// IF node condition
return $json.choices && $json.choices.length > 0;
```

**Node 3: Try OpenRouter (if GitHub failed)**
```json
{
  "method": "POST", 
  "url": "https://openrouter.ai/api/v1/chat/completions",
  "headers": {
    "Authorization": "Bearer {{$env.OPENROUTER_API_KEY}}",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "messages": [{"role": "user", "content": "{{$json.prompt}}"}],
    "max_tokens": "{{$json.max_tokens || 500}}"
  }
}
```

## 📝 Quick Setup for n8n Cloud

### **1. Environment Variables in n8n Cloud**

In your n8n cloud workspace settings, add:
- `GITHUB_TOKEN` = your GitHub token
- `OPENROUTER_API_KEY` = your OpenRouter key  
- `GOOGLE_API_KEY` = your Google API key

### **2. Simple HTTP Request Template**

For any workflow in n8n cloud, add an HTTP Request node:

**URL:** `https://your-deployed-app.com/ai-request`
**Method:** `POST`
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "prompt": "{{ $json.your_prompt_field }}",
  "model_type": "chat",
  "max_tokens": 500,
  "temperature": 0.7
}
```

## 🎯 Real-World n8n Cloud Examples

### **Example 1: Email Auto-Responder**
```
Gmail Trigger → HTTP Request (AI Router) → Gmail Send
```

**HTTP Request Configuration:**
- **URL**: `https://your-app.railway.app/ai-request`
- **Body**: 
  ```json
  {
    "prompt": "Write a professional response to this email: {{ $json.snippet }}",
    "model_type": "chat",
    "max_tokens": 300
  }
  ```

### **Example 2: Social Media Content Generator**
```
RSS Trigger → HTTP Request (AI Router) → Twitter Post
```

**HTTP Request Configuration:**
- **URL**: `https://your-app.railway.app/ai-request`
- **Body**:
  ```json
  {
    "prompt": "Create a Twitter post for this article: {{ $json.title }} - {{ $json.link }}",
    "model_type": "creative",
    "max_tokens": 200,
    "temperature": 0.8
  }
  ```

### **Example 3: Customer Support Chatbot**
```
Webhook Trigger → HTTP Request (AI Router) → Slack/Discord Response
```

**HTTP Request Configuration:**
- **URL**: `https://your-app.railway.app/ai-request`
- **Body**:
  ```json
  {
    "prompt": "Customer question: {{ $json.message }}. Please provide a helpful response.",
    "model_type": "chat",
    "max_tokens": 400,
    "system_prompt": "You are a helpful customer support agent."
  }
  ```

## 🔒 Security Considerations for n8n Cloud

### **1. Environment Variables**
