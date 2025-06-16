# 🚀 Deploy Your AI Router to Railway

Follow these steps to deploy your AI rotation system to Railway:

## 🔗 Step 1: Push to GitHub

1. **Create a new GitHub repository** (or use existing one)
2. **Push your code**:
   ```bash
   git init
   git add .
   git commit -m "Initial AI router setup"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

## 🚂 Step 2: Deploy to Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up/Login** with your GitHub account
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository** with the AI router code
6. **Railway will automatically detect** it's a Python app

## ⚙️ Step 3: Set Environment Variables

In your Railway project dashboard:

1. **Go to Variables tab**
2. **Add these environment variables**:
   ```
   GITHUB_TOKEN=your_github_token_here
   OPENROUTER_API_KEY=your_openrouter_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 🎯 Step 4: Get Your Public URL

1. **Railway will automatically deploy** your app
2. **Copy the public URL** (something like: `https://your-app-name.railway.app`)
3. **Test your deployment**:
   ```bash
   curl -X POST https://your-app-name.railway.app/ai-request \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello! Test message", "model_type": "chat"}'
   ```

## 🌐 Step 5: Use in n8n Cloud

Now in any n8n Cloud workflow:

1. **Add HTTP Request node**
2. **Set URL**: `https://your-app-name.railway.app/ai-request`
3. **Set Method**: `POST`
4. **Set Headers**: `Content-Type: application/json`
5. **Set Body**:
   ```json
   {
     "prompt": "{{ $json.your_prompt }}",
     "model_type": "chat",
     "max_tokens": 500,
     "temperature": 0.7
   }
   ```

## 📊 Monitoring

- **Railway Dashboard**: Check logs and usage
- **Status Endpoint**: `https://your-app-name.railway.app/status`
- **Logs**: Monitor provider rotation and rate limits

## 💡 Tips

- **Free Tier**: Railway gives you 500 hours/month free
- **Auto-Sleep**: App sleeps after inactivity (wakes up automatically)
- **Scaling**: Railway handles traffic spikes automatically
- **Custom Domain**: You can add your own domain if needed

Your AI rotation system is now globally accessible and ready to power all your n8n Cloud workflows! 🎉
