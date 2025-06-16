# AI Router API - Usage Examples

This document provides practical examples of how to use the AI rotation system from your other n8n workflows.

## 📋 Basic API Reference

### Endpoint
```
POST http://localhost:5678/webhook/ai-request
```

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

### Response Format (Success)
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

### Response Format (Error)
```json
{
  "success": false,
  "error": "Error description",
  "provider": "github_models",
  "request_id": "abc123",
  "message": "All providers failed or rate limited. Please try again later."
}
```

## 🔧 n8n Integration Examples

### Example 1: Email Summary Automation

**Use Case**: Automatically summarize incoming emails

```json
{
  "name": "Email Summarizer",
  "nodes": [
    {
      "parameters": {
        "pollTimes": {
          "item": [
            {
              "mode": "everyMinute",
              "minute": 5
            }
          ]
        }
      },
      "name": "Email Trigger",
      "type": "n8n-nodes-base.emailReadImap"
    },
    {
      "parameters": {
        "url": "http://localhost:5678/webhook/ai-request",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "prompt",
              "value": "Summarize this email in 2-3 sentences: {{ $json.text }}"
            },
            {
              "name": "model_type",
              "value": "chat"
            },
            {
              "name": "max_tokens",
              "value": 200
            },
            {
              "name": "system_prompt",
              "value": "You are an expert email assistant. Create concise, professional summaries."
            }
          ]
        }
      },
      "name": "AI Summary",
      "type": "n8n-nodes-base.httpRequest"
    }
  ]
}
```

### Example 2: Code Review Bot

**Use Case**: Automatically review code commits

```json
{
  "name": "Code Review Bot",
  "nodes": [
    {
      "parameters": {
        "events": ["push"],
        "repository": "your-repo"
      },
      "name": "GitHub Webhook",
      "type": "n8n-nodes-base.githubTrigger"
    },
    {
      "parameters": {
        "url": "http://localhost:5678/webhook/ai-request",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "prompt",
              "value": "Review this code for bugs, security issues, and best practices:\n\n{{ $json.commits[0].message }}\n\n{{ $json.head_commit.diff }}"
            },
            {
              "name": "model_type",
              "value": "code"
            },
            {
              "name": "max_tokens",
              "value": 1000
            },
            {
              "name": "temperature",
              "value": 0.3
            },
            {
              "name": "system_prompt",
              "value": "You are a senior software engineer. Provide constructive code review focusing on security, performance, and maintainability."
            }
          ]
        }
      },
      "name": "AI Code Review",
      "type": "n8n-nodes-base.httpRequest"
    }
  ]
}
```

### Example 3: Content Generator

**Use Case**: Generate social media content from blog posts

```json
{
  "name": "Social Media Generator",
  "nodes": [
    {
      "parameters": {
        "url": "{{ $json.blog_url }}",
        "options": {
          "redirect": "follow"
        }
      },
      "name": "Fetch Blog Post",
      "type": "n8n-nodes-base.httpRequest"
    },
    {
      "parameters": {
        "url": "http://localhost:5678/webhook/ai-request",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "prompt",
              "value": "Create 3 engaging social media posts (Twitter, LinkedIn, Instagram) based on this blog post:\n\n{{ $json.data }}"
            },
            {
              "name": "model_type",
              "value": "creative"
            },
            {
              "name": "max_tokens",
              "value": 800
            },
            {
              "name": "temperature",
              "value": 0.8
            },
            {
              "name": "system_prompt",
              "value": "You are a social media expert. Create platform-specific content that drives engagement."
            }
          ]
        }
      },
      "name": "Generate Social Posts",
      "type": "n8n-nodes-base.httpRequest"
    }
  ]
}
```

### Example 4: Customer Support Assistant

**Use Case**: Auto-respond to customer inquiries

```json
{
  "name": "Support Assistant",
  "nodes": [
    {
      "parameters": {
        "pollTimes": {
          "item": [
            {
              "mode": "everyMinute",
              "minute": 2
            }
          ]
        }
      },
      "name": "Support Ticket Trigger",
      "type": "n8n-nodes-base.webhook"
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "{{ $json.priority }}",
              "operation": "notEqual",
              "value2": "urgent"
            }
          ]
        }
      },
      "name": "Filter Non-Urgent",
      "type": "n8n-nodes-base.if"
    },
    {
      "parameters": {
        "url": "http://localhost:5678/webhook/ai-request",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "prompt",
              "value": "Customer inquiry: {{ $json.message }}\n\nCustomer context: {{ $json.customer_info }}\n\nProvide a helpful, professional response."
            },
            {
              "name": "model_type",
              "value": "chat"
            },
            {
              "name": "max_tokens",
              "value": 500
            },
            {
              "name": "temperature",
              "value": 0.4
            },
            {
              "name": "system_prompt",
              "value": "You are a customer support specialist. Be helpful, professional, and solution-oriented. If you cannot resolve the issue, escalate to a human agent."
            }
          ]
        }
      },
      "name": "Generate Response",
      "type": "n8n-nodes-base.httpRequest"
    }
  ]
}
```

## 🎯 Model Type Guidelines

### `chat` - Conversational AI
- **Best for**: Q&A, customer support, general conversation
- **Temperature**: 0.3-0.7
- **Providers**: All (GitHub Models preferred for quality)
- **Example prompts**:
  - "Explain how to use this API"
  - "What are the benefits of automation?"
  - "Help me troubleshoot this issue"

### `code` - Programming Assistant
- **Best for**: Code generation, debugging, technical documentation
- **Temperature**: 0.1-0.4 (lower for more precise code)
- **Providers**: GitHub Models (best), OpenRouter (good for open-source models)
- **Example prompts**:
  - "Write a Python function to validate email addresses"
  - "Debug this JavaScript error: [error details]"
  - "Convert this SQL query to MongoDB syntax"

### `creative` - Content Generation
- **Best for**: Writing, marketing copy, creative content
- **Temperature**: 0.7-1.0 (higher for more creativity)
- **Providers**: All (varies by use case)
- **Example prompts**:
  - "Write a product description for [product]"
  - "Create a blog post outline about [topic]"
  - "Generate social media captions for [content]"

## 🔄 Error Handling Patterns

### Pattern 1: Retry with Exponential Backoff

```json
{
  "parameters": {
    "jsCode": "// Check if AI request failed\nconst response = $input.first().json;\n\nif (!response.success) {\n  const attempt = $node.getWorkflowStaticData('node', 'attempt') || 1;\n  \n  if (attempt <= 3) {\n    // Exponential backoff: 2^attempt seconds\n    const delay = Math.pow(2, attempt) * 1000;\n    \n    $node.setWorkflowStaticData('node', 'attempt', attempt + 1);\n    \n    setTimeout(() => {\n      // Retry the request\n      $node.trigger();\n    }, delay);\n    \n    return { retry: true, attempt, delay };\n  } else {\n    // Max retries reached\n    $node.setWorkflowStaticData('node', 'attempt', 1);\n    return { failed: true, error: response.error };\n  }\n} else {\n  // Success - reset attempt counter\n  $node.setWorkflowStaticData('node', 'attempt', 1);\n  return response;\n}"
  },
  "name": "Retry Logic",
  "type": "n8n-nodes-base.code"
}
```

### Pattern 2: Fallback to Human

```json
{
  "parameters": {
    "conditions": {
      "boolean": [
        {
          "value1": "{{ $json.success }}",
          "operation": "equal",
          "value2": false
        }
      ]
    }
  },
  "name": "Check AI Success",
  "type": "n8n-nodes-base.if"
}
```

## 📊 Usage Analytics

### Track API Usage

```json
{
  "parameters": {
    "jsCode": "// Log AI usage for analytics\nconst response = $input.first().json;\n\nconst usage = {\n  timestamp: new Date().toISOString(),\n  provider: response.provider,\n  model: response.model,\n  tokens_used: response.tokens_used,\n  processing_time: response.processing_time,\n  success: response.success,\n  workflow_name: $workflow.name,\n  request_type: $('AI Request').first().json.model_type\n};\n\n// Store in database or send to analytics service\nconsole.log('AI Usage:', JSON.stringify(usage));\n\nreturn usage;"
  },
  "name": "Track Usage",
  "type": "n8n-nodes-base.code"
}
```

## 🛠️ Advanced Integration Techniques

### Conditional Model Selection

```json
{
  "parameters": {
    "jsCode": "// Choose model type based on content\nconst content = $json.input_text;\nconst length = content.length;\n\nlet modelType = 'chat';\nlet temperature = 0.7;\n\n// Code detection\nif (content.includes('function') || content.includes('def ') || content.includes('SELECT')) {\n  modelType = 'code';\n  temperature = 0.3;\n}\n// Creative content detection\nelse if (content.includes('write') || content.includes('creative') || content.includes('story')) {\n  modelType = 'creative';\n  temperature = 0.9;\n}\n\n// Adjust max_tokens based on content length\nconst maxTokens = Math.min(Math.max(length * 2, 200), 2000);\n\nreturn {\n  prompt: content,\n  model_type: modelType,\n  temperature: temperature,\n  max_tokens: maxTokens\n};"
  },
  "name": "Smart Model Selection",
  "type": "n8n-nodes-base.code"
}
```

### Batch Processing

```json
{
  "parameters": {
    "jsCode": "// Process multiple requests efficiently\nconst items = $input.all();\nconst results = [];\n\nfor (const item of items) {\n  // Add delay between requests to respect rate limits\n  if (results.length > 0) {\n    await new Promise(resolve => setTimeout(resolve, 1000));\n  }\n  \n  const aiRequest = {\n    prompt: item.json.text,\n    model_type: 'chat',\n    max_tokens: 300\n  };\n  \n  // Make request to AI router\n  const response = await fetch('http://localhost:5678/webhook/ai-request', {\n    method: 'POST',\n    headers: { 'Content-Type': 'application/json' },\n    body: JSON.stringify(aiRequest)\n  });\n  \n  const result = await response.json();\n  results.push({ original: item.json, ai_response: result });\n}\n\nreturn results;"
  },
  "name": "Batch AI Processing",
  "type": "n8n-nodes-base.code"
}
```

## 🚀 Performance Tips

1. **Choose appropriate max_tokens**: Don't request more tokens than needed
2. **Use temperature wisely**: Lower for factual, higher for creative content
3. **Implement caching**: Store common responses to reduce API calls
4. **Monitor provider performance**: Check logs to see which providers work best for your use cases
5. **Use system prompts**: They help guide the AI for better, more consistent results

## 🔒 Security Considerations

1. **Validate inputs**: Always sanitize user inputs before sending to AI
2. **Rate limiting**: Implement your own rate limiting for user-facing workflows
3. **Content filtering**: Consider adding content filters for sensitive applications
4. **Audit logging**: Keep logs of AI interactions for compliance

Your AI rotation system is now ready to power all your n8n automations with reliable, intelligent responses!