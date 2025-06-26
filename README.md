# JobBuilder - Automated Job Application System

## 🎯 Quick Start

JobBuilder automates the creation of personalized job applications using Notion as a trigger and AI for content generation.

### 🚀 Setup (5 minutes)

1. **Run setup script:**
   ```bash
   ./setup.sh
   ```

2. **Configure your information:**
   - Edit `.env` with your Notion API credentials
   - Update `data/personal_info.json` with your details
   - Update `data/base_resume.json` with your resume

3. **Start the server:**
   ```bash
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

### 🔧 Notion Setup

1. **Create a Notion Integration:**
   - Go to https://www.notion.so/my-integrations
   - Create new integration, copy the API key
   - Add to `.env` file

2. **Create Job Database:**
   - Create a new database in Notion
   - Add these properties:
     - Job Title (Title)
     - Company (Text)
     - Job Description (Text)
     - Status (Select: Not Started, In Progress, Applied)
     - Application Generated (Checkbox)
     - Generated Date (Date)

3. **Share database with your integration**

4. **Set up Notion Automation:**
   - Create automation: "When Status changes to In Progress"
   - Action: "Make HTTP request to your webhook URL"
   - URL: `https://your-domain.com/webhook/notion`

### 📁 Project Structure

```
JobBuilder/
├── app/                     # Main application
│   ├── main.py             # FastAPI app
│   ├── models/             # Data models
│   └── services/           # Business logic
├── data/                   # Your personal data
│   ├── personal_info.json  # Your contact info
│   └── base_resume.json    # Your resume data
├── output/                 # Generated documents
└── templates/              # Document templates
```

### 🔄 How It Works

1. **Add job** to your Notion database
2. **Change status** to "In Progress" 
3. **Notion automation** triggers webhook
4. **JobBuilder processes** the job description
5. **AI generates** personalized cover letter and resume
6. **PDFs created** and saved to output folder
7. **Notion updated** with completion status

### 🆓 Free Hosting Options

Deploy for free on:
- **Railway:** Connect GitHub repo, automatic deployments
- **Render:** Great Python support, 750 hours/month free
- **Fly.io:** Good performance, generous free tier

### 💰 Cost: $0
- Notion API: Free for personal use
- Local AI (Ollama): Free, runs on your computer/server
- Hosting: Free tier sufficient for personal use

### 🤖 AI Options

**Recommended (Free):**
- Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
- Pull model: `ollama pull llama3.2`
- Update `.env` with Ollama settings

**Alternative:** OpenAI API (paid but higher quality)

### 📝 API Endpoints

- `GET /` - Health check
- `POST /webhook/notion` - Notion webhook
- `GET /jobs/status/{page_id}` - Check job status
- `GET /files/{filename}` - Download generated files
- `GET /docs` - API documentation

### 🧪 Testing

Run the test to verify everything works:
```bash
python test_setup.py
```

### 🎨 Customization

**Cover Letter Template:**
Edit `templates/cover_letter.j2`

**Resume Template:**
Edit `templates/resume.j2`

**AI Prompts:**
Modify prompts in `app/services/ai_service.py`

### 🔍 Troubleshooting

**Common Issues:**
- PDF generation fails: Install `reportlab` with `pip install reportlab`
- Notion webhook not working: Check integration permissions
- AI not working: Verify Ollama is running or check API keys

**Logs:**
Check application logs for detailed error information.

### 🚀 Production Deployment

1. **Environment Variables:**
   ```bash
   NOTION_API_KEY=your_key
   NOTION_DATABASE_ID=your_db_id
   APP_HOST=0.0.0.0
   APP_PORT=8000
   ```

2. **Deploy to Railway:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   # Connect to Railway and deploy
   ```

### 📈 Next Steps

Once basic system is working:
- Add company research integration
- Implement multiple resume templates
- Add email notifications
- Create mobile app for reviews
- Add application tracking
- Integrate with job boards

### 🛠️ Development

**Add new features:**
1. Create new service in `app/services/`
2. Add endpoints in `app/main.py`
3. Update models in `app/models/`
4. Test with `python test_setup.py`

**Local development:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

---

**Questions?** Check the logs, review the code, or create an issue!

**Goal:** Get your job applications automated in the next hour! 🎯
