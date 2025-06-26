# 🚀 JobBuilder Deployment Guide

## 🎯 Quick Deploy (5 minutes)

### Option 1: Railway (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial JobBuilder setup"
   git branch -M main
   git remote add origin https://github.com/yourusername/jobbuilder.git
   git push -u origin main
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - "Deploy from GitHub repo"
   - Select your JobBuilder repo
   - Add environment variables:
     ```
     NOTION_API_KEY=your_notion_key
     NOTION_DATABASE_ID=your_database_id
     WEBHOOK_SECRET=your_secret
     ```

3. **Get webhook URL:**
   - Copy your Railway domain: `https://your-app.railway.app`
   - Webhook endpoint: `https://your-app.railway.app/webhook/notion`

### Option 2: Render

1. **Connect GitHub repo** to Render
2. **Set build command:** `pip install -r requirements.txt`
3. **Set start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Add environment variables** (same as Railway)

### Option 3: Fly.io

1. **Install Fly CLI:** `curl -L https://fly.io/install.sh | sh`
2. **Login:** `flyctl auth login`
3. **Initialize:** `flyctl launch`
4. **Deploy:** `flyctl deploy`

## 🔧 Environment Variables

Required for production:
```bash
# Notion Integration
NOTION_API_KEY=secret_abc123...
NOTION_DATABASE_ID=abc123...

# Security
WEBHOOK_SECRET=your-random-secret-string

# App Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=false

# AI Configuration (optional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

## 🎯 Notion Automation Setup

### 1. Create Notion Database

**Required Properties:**
- `Job Title` (Title)
- `Company` (Text) 
- `Job Description` (Text)
- `Status` (Select): Not Started, In Progress, Applied, Generated
- `Application Generated` (Checkbox)
- `Generated Date` (Date)
- `Generated Files` (Text) - optional

### 2. Set Up Integration

1. Go to https://www.notion.so/my-integrations
2. Create "New integration"
3. Name: "JobBuilder"
4. Copy the API key → add to environment variables
5. Share your database with the integration

### 3. Create Automation

**Trigger:** "When Status changes to In Progress"

**Action:** "Make HTTP request"
- URL: `https://your-domain.com/webhook/notion`
- Method: POST
- Headers: `Content-Type: application/json`

## 🤖 AI Setup Options

### Option A: Local AI (Free)

**On your server/computer:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3.2

# Set environment variables
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

### Option B: Cloud AI (Paid)

**OpenAI Integration:**
```python
# In ai_service.py, replace ollama calls with:
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
```

## 🔄 Complete Workflow Test

1. **Add test job** to Notion database
2. **Set status** to "In Progress"
3. **Check webhook** receives request (check logs)
4. **Verify generation** - PDFs created
5. **Check Notion** - status updated to "Generated"

## 📊 Production Checklist

- [ ] Environment variables configured
- [ ] Personal data files updated
- [ ] Notion integration working
- [ ] Webhook endpoint accessible
- [ ] AI service configured
- [ ] PDF generation working
- [ ] Error monitoring set up
- [ ] Backup strategy in place

## 🚨 Troubleshooting

### Common Issues:

**Webhook not triggered:**
- Check Notion automation is active
- Verify webhook URL is correct
- Check integration permissions

**PDF generation fails:**
- Ensure `reportlab` is installed
- Check file permissions for output directory
- Verify template rendering works

**AI not generating content:**
- Check Ollama is running (`ollama ps`)
- Verify model is pulled (`ollama list`)
- Check API keys if using cloud AI

### Debug Commands:

```bash
# Check logs
flyctl logs  # Fly.io
railway logs  # Railway

# Test webhook locally
curl -X POST http://localhost:8000/webhook/notion \
  -H "Content-Type: application/json" \
  -d '{"id": "test", "properties": {...}}'

# Health check
curl http://localhost:8000/health
```

## 📈 Scaling & Optimization

### For High Volume:

1. **Add Redis caching**
2. **Implement job queues** (Celery)
3. **Use database** for job tracking
4. **Add rate limiting**
5. **Implement retries**

### Cost Optimization:

1. **Use smaller AI models** for development
2. **Implement caching** for repeated requests
3. **Optimize PDF generation**
4. **Monitor usage** and set limits

## 🛡️ Security Best Practices

1. **Use environment variables** for secrets
2. **Implement webhook signature validation**
3. **Add rate limiting**
4. **Use HTTPS** only
5. **Regular security updates**

## 📝 Monitoring

### Key Metrics:
- Webhook success rate
- PDF generation time
- AI response time
- Error rates
- Storage usage

### Logging:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🎉 You're Live!

Your JobBuilder is now running in production! 

**Next steps:**
1. Add first real job to Notion
2. Test the complete workflow
3. Customize templates as needed
4. Set up monitoring alerts
5. Share your success! 🎯

---

**Need help?** Check the logs, test components individually, or review the troubleshooting guide.
