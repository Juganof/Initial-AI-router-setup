# AI Model Rotation System - Setup Guide

This guide will walk you through setting up the complete AI model rotation system using n8n, Docker, and multiple AI providers.

## 📋 Prerequisites

- Docker and Docker Compose installed
- GitHub account with Pro for Students (you already have this!)
- Internet connection for API access

## 🔑 Step 1: Get API Keys

### GitHub Personal Access Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Set token name: `n8n-ai-router`
4. Select scopes:
   - ✅ `repo` (for repository access)
   - ✅ `read:org` (for organization access)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)

### OpenRouter API Key

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to [API Keys](https://openrouter.ai/keys)
4. Click **"Create Key"**
5. Set name: `n8n-ai-router`
6. Copy the API key (starts with `sk-or-...`)

### Google AI Studio API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Select existing project or create new one
5. Copy the API key (starts with `AIza...`)

## 🚀 Step 2: Setup Environment

### Clone/Download Files

```bash
# If you have the files in a directory, navigate there
cd /path/to/your/ai-router-project

# Or create a new directory
mkdir n8n-ai-router
cd n8n-ai-router
```

### Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your API keys:
```bash
# Use your preferred text editor
notepad .env
# or
code .env
# or
nano .env
```

3. Replace the placeholder values with your actual API keys:
```env
# N8N Configuration
N8N_USER=admin
N8N_PASSWORD=your_secure_password_here

# AI Provider API Keys
GITHUB_TOKEN=ghp_your_github_token_here
OPENROUTER_API_KEY=sk-or-your_openrouter_key_here
GOOGLE_API_KEY=AIza_your_google_key_here
```

⚠️ **Important**: Never commit the `.env` file to version control!

## 🐳 Step 3: Start n8n with Docker

### Start the Services

```bash
# Start n8n in the background
docker-compose up -d

# Check if it's running
docker-compose ps

# View logs (optional)
docker-compose logs -f n8n
```

### Access n8n

1. Open your browser and go to: [http://localhost:5678](http://localhost:5678)
2. Login with:
   - **Username**: `admin` (or what you set in `.env`)
   - **Password**: `your_secure_password_here`

## 📥 Step 4: Import Workflows

### Method 1: Import via n8n UI

1. In n8n, click **"Workflows"** in the sidebar
2. Click **"Import from File"**
3. Upload these files one by one:
   - `n8n-ai-router-main.json`
   - `n8n-provider-status-manager.json`

### Method 2: Copy to Workflows Directory

```bash
# Create workflows directory if it doesn't exist
mkdir -p ./workflows

# Copy workflow files
cp n8n-ai-router-main.json ./workflows/
cp n8n-provider-status-manager.json ./workflows/

# Restart n8n to pick up the workflows
docker-compose restart n8n
```

## ⚙️ Step 5: Configure Workflows

### Activate the Provider Status Manager

1. Go to **"AI Router - Main"** workflow
2. Click **"Activate"** toggle in the top right
3. Go to **"Provider Status Manager"** workflow  
4. Click **"Activate"** toggle in the top right

The Provider Status Manager will:
- Create the SQLite database table
- Initialize all three providers as available
- Check and recover providers every 5 minutes

### Test the Setup

1. In the **"AI Router - Main"** workflow
2. Click on the **"AI Request Webhook"** node
3. Copy the webhook URL (something like: `http://localhost:5678/webhook/ai-request`)
4. Test with curl or Postman:

```bash
curl -X POST http://localhost:5678/webhook/ai-request \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello! Please introduce yourself.",
    "model_type": "chat",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

Expected response:
```json
{
  "success": true,
  "response": "Hello! I'm an AI assistant...",
  "provider": "github_models",
  "model": "gpt-4o",
  "tokens_used": 45,
  "processing_time": 2.1,
  "request_id": "abc123"
}
```

## 🔗 Step 6: Use from Other Workflows

### Create a Test Workflow

1. Create a new workflow in n8n
2. Add a **"Manual Trigger"** node
3. Add an **"HTTP Request"** node with:
   - **Method**: POST
   - **URL**: `http://localhost:5678/webhook/ai-request`
   - **Headers**: `Content-Type: application/json`
   - **Body**: 
   ```json
   {
     "prompt": "Write a short poem about automation",
     "model_type": "creative",
     "max_tokens": 200,
     "temperature": 0.9
   }
   ```

### Integration Pattern

For any workflow that needs AI:

```json
{
  "prompt": "Your AI request here",
  "model_type": "chat|code|creative",
  "max_tokens": 1000,
  "temperature": 0.7,
  "system_prompt": "Optional system instructions"
}
```

## 📊 Step 7: Monitoring

### Check Provider Status

The Provider Status Manager logs provider status every 5 minutes. To view:

```bash
# View n8n logs
docker-compose logs -f n8n

# Look for lines like:
# === Provider Status Check - 2024-01-01T12:00:00.000Z ===
# GITHUB_MODELS:
#   Status: Available
#   Priority: 1
#   Requests: 45 (2.22% error rate)
#   Recovery: Active
```

### Database Access (Advanced)

```bash
# Access the n8n container
docker exec -it n8n-ai-router sh

# Query the database
sqlite3 /home/node/.n8n/database.sqlite "SELECT * FROM provider_status;"
```

## 🐛 Troubleshooting

### Common Issues

**1. Webhook not responding**
```bash
# Check if n8n is running
docker-compose ps

# Check logs for errors
docker-compose logs n8n
```

**2. API key errors**
- Verify keys are correctly set in `.env`
- Restart n8n: `docker-compose restart n8n`
- Check that GitHub token has correct permissions

**3. Rate limiting issues**
- The system automatically handles rate limits
- Check provider status in logs
- Wait for recovery timers to reset

**4. Database issues**
```bash
# Restart with fresh database
docker-compose down
docker volume rm n8n-ai-router_n8n_data
docker-compose up -d
```

### Getting Help

1. Check n8n logs: `docker-compose logs -f n8n`
2. Verify environment variables: `docker exec n8n-ai-router env | grep -E "(GITHUB|OPENROUTER|GOOGLE)"`
3. Test individual API keys with curl commands

## 🔄 Usage Examples

### Basic Chat Request
```bash
curl -X POST http://localhost:5678/webhook/ai-request \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "model_type": "chat"
  }'
```

### Code Generation
```bash
curl -X POST http://localhost:5678/webhook/ai-request \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to calculate fibonacci numbers",
    "model_type": "code",
    "system_prompt": "You are a expert Python developer. Write clean, well-commented code."
  }'
```

### Creative Writing
```bash
curl -X POST http://localhost:5678/webhook/ai-request \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a haiku about artificial intelligence",
    "model_type": "creative",
    "temperature": 0.9
  }'
```

## 🚀 Next Steps

1. **Test all three providers** by making requests until you hit rate limits
2. **Integrate with your existing workflows** by replacing direct AI API calls with calls to your router
3. **Monitor usage patterns** through the logs to optimize provider selection
4. **Add more providers** by following the pattern in the workflow files

## 🛡️ Security Notes

- Keep your `.env` file secure and never commit it to version control
- Use strong passwords for n8n basic auth
- Consider setting up HTTPS if deploying to production
- Regularly rotate your API keys
- Monitor usage to stay within provider limits

Your AI rotation system is now ready to serve all your n8n automations with automatic failover and rate limit handling!