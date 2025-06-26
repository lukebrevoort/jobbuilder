# 🚀 Deploy JobBuilder + Ollama to Railway

## Step-by-Step Railway Deployment

### 1. Push to GitHub (if you haven't already)

```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/yourusername/jobbuilder.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign up/Login** with GitHub
3. **Click "Deploy from GitHub repo"**
4. **Select your JobBuilder repository**
5. **Railway will automatically detect the docker-compose.yml**

### 3. Configure Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```bash
# Required - Get these from Notion
NOTION_API_KEY=secret_abc123...
NOTION_DATABASE_ID=abc123...

# Security
WEBHOOK_SECRET=your-random-secret-here

# App Settings  
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=false

# Ollama will auto-configure with docker-compose
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:1b
```

### 4. Get Your Webhook URL

After deployment, Railway gives you a URL like:
```
https://jobbuilder-production-xyz.up.railway.app
```

Your webhook endpoint will be:
```
https://jobbuilder-production-xyz.up.railway.app/webhook/notion
```

## 🔧 Important Railway Configuration

Railway will automatically:
- ✅ Build both JobBuilder and Ollama containers
- ✅ Download the Ollama model (llama3.2:1b)
- ✅ Set up internal networking between services
- ✅ Expose your app on port 8000
- ✅ Handle SSL certificates

## 📋 What Happens During Deployment

1. **Railway reads docker-compose.yml**
2. **Builds JobBuilder container** (your Python app)
3. **Pulls Ollama container** (AI service)
4. **Downloads AI model** (llama3.2:1b - about 1GB)
5. **Starts both services** with internal networking
6. **Exposes your app** to the internet

## ⏱️ Deployment Timeline

- **Initial deploy:** 5-10 minutes (downloading AI model)
- **Subsequent deploys:** 2-3 minutes (model cached)
- **Cold start:** 30-60 seconds (AI model loading)

## 🎯 Testing Your Deployment

Once deployed, test these endpoints:

```bash
# Health check
curl https://your-app.railway.app/

# Detailed health (should show Ollama as healthy)
curl https://your-app.railway.app/health

# API docs
# Visit: https://your-app.railway.app/docs
```

## 🚨 Troubleshooting

**If deployment fails:**

1. **Check Railway logs** in the dashboard
2. **Common issues:**
   - Out of memory (model too large)
   - Environment variables missing
   - Docker build timeout
   - Container restart loops

**Solutions:**
- Use smaller model: `OLLAMA_MODEL=llama3.2:1b`
- Check Railway resource limits
- Verify all environment variables are set
- Make sure $PORT is used instead of hardcoded 8000

**Common Error Messages:**

```
WARNING: Notion API key not found in environment variables
```
**Fix:** Add `NOTION_API_KEY` to Railway environment variables

```
WARNING: Templates directory not found: ./templates
```
**Fix:** This is normal - templates are created automatically

```
Container keeps restarting
```
**Fix:** Check Railway variables are set correctly and health check is working

## 📊 Resource Usage

**Railway Free Tier:**
- **Memory:** 8GB (perfect for 1B/3B models)
- **CPU:** Shared
- **Network:** 100GB/month
- **Build time:** 1 hour/month

**Expected usage:**
- **Ollama:** ~2GB RAM (1B model)
- **JobBuilder:** ~100MB RAM
- **Total:** ~2.1GB RAM ✅

## 🎉 You're Live!

Once deployed:
1. **Copy your webhook URL**
2. **Set up Notion automation** (next step)
3. **Test with a real job posting**

Your JobBuilder + Ollama system is now running 24/7 for free! 🚀
