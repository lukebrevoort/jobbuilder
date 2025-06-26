# 🤖 AI Configuration Guide

## 🎯 Three Ways to Run JobBuilder

### 1. 📝 Template Mode (Works Now - No AI Needed)
**Best for:** Immediate use, testing, reliability
**Cost:** Free
**Quality:** Good (smart templates based on job analysis)

```bash
# Just run it - works immediately!
./setup.sh
python notionapi.py
```

### 2. 🏠 Local AI Mode (Ollama)
**Best for:** Best quality, no API costs, full control
**Cost:** Free (needs more server resources)
**Quality:** Excellent

#### Option A: Same Server (Railway)
```bash
# Deploy with included docker-compose.yml
git push origin main
# Railway auto-deploys JobBuilder + Ollama together
```

#### Option B: Separate Ollama Server
```bash
# On your Ollama server (VPS/home server)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:1b  # 1GB model
ollama serve --host 0.0.0.0

# Update your .env
OLLAMA_BASE_URL=http://your-server-ip:11434
```

### 3. ☁️ Cloud AI Mode (OpenAI/Anthropic)
**Best for:** Guaranteed uptime, no server management
**Cost:** ~$0.01 per application
**Quality:** Excellent

```bash
# Add to .env
OPENAI_API_KEY=sk-...
# System automatically uses OpenAI when Ollama unavailable
```

## 🚀 Hosting Platform Guide

### Railway (Recommended for Ollama)
- **Free tier:** 8GB RAM ✅
- **Docker compose:** Full support
- **Ollama support:** ✅ Can run 3B model
- **Setup:** `git push` → auto-deploy

### Render 
- **Free tier:** 512MB RAM
- **Ollama support:** ❌ Too small
- **Best for:** Template mode only
- **Setup:** Connect repo → deploy

### Fly.io
- **Free tier:** 256MB × 3 VMs
- **Ollama support:** ❌ (could split across VMs but complex)
- **Best for:** JobBuilder only + external Ollama

## 💡 Recommended Path

### Phase 1: Start Today (5 minutes)
```bash
./setup.sh
# Edit your personal data
# Deploy to any platform
# Works with smart templates
```

### Phase 2: Add AI Later (optional)
```bash
# If you want AI, choose:
# - Railway deployment (includes Ollama)
# - Or add OpenAI API key
# - Or set up separate Ollama server
```

## 🔧 Resource Calculator

**For Ollama hosting, you need:**

| Model | RAM | Speed | Quality |
|-------|-----|-------|---------|
| llama3.2:1b | 1GB | Fast | Good |
| llama3.2:3b | 3GB | Medium | Better |
| llama3.2 | 8GB | Slow | Best |

**Platform capacity:**
- Railway Free: Up to 3B model ✅
- Render Free: Template mode only
- $5 VPS: Up to 3B model ✅
- $10 VPS: Full 8B model ✅

## 🎯 Decision Tree

**Need it working now?** → Deploy anywhere, template mode
**Want free AI?** → Railway with docker-compose
**Have existing server?** → Add Ollama there
**Want guaranteed uptime?** → Add OpenAI API key
**Budget for VPS?** → $5 VPS + free hosting split

The system I built automatically handles all these scenarios!
