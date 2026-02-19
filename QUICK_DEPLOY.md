# ⚡ Quick Deploy - 5 Minute Guide

**TL;DR**: Deploy Nanobot to Render in 5 minutes

---

## 🔥 Super Quick Steps

### 1. Push Code (1 min)
```bash
cd C:\Users\QUINTANA\sistemas\NANOBOT
git add .
git commit -m "Fase 3: Ready for Render deployment"
git push origin main
```

### 2. Create Render Service (2 min)

Go to: https://dashboard.render.com

- Click **"New +"** → **"Web Service"**
- Select repository: **`nanobot-cloud`**
- Name: **`nanobot`**
- Build: **`pip install poetry && poetry install`**
- Start: **`python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`**

### 3. Add Secrets (1 min)

In Render dashboard, click "Environment":

```
TELEGRAM_TOKEN     = your_token_from_botfather
GROQ_API_KEY      = your_key_from_groq
ANTHROPIC_API_KEY = your_key_from_anthropic
ENVIRONMENT       = production
```

### 4. Deploy (1 min)

Click **"Create Web Service"**

Wait ~3-5 minutes...

### 5. Verify (0 min)

When it says "Live", test:

```bash
# Health check
curl https://nanobot.onrender.com/api/status

# Open Telegram and send a message to your bot
# It should respond in < 5 seconds!
```

---

## 🎉 Done!

Your bot is now **24/7 live on the internet** 🚀

**Dashboard**: https://nanobot.onrender.com
**Bot**: Open Telegram and send a message

---

## 🆘 If Something Goes Wrong

### Health check fails
```bash
# Check Render logs:
# https://dashboard.render.com → nanobot → Logs
# Look for: "NANOBOT IS RUNNING"
```

### Bot doesn't respond
1. Check TELEGRAM_TOKEN is correct (from @BotFather)
2. Verify Render service status is "Live"
3. Check logs for errors

### Build fails
1. Make sure Python 3.11+
2. Run locally: `poetry install`
3. Check Dockerfile: `docker build -t test .`

---

## 📚 Need More Help?

- **Setup Guide**: `RENDER_SETUP_GUIDE.md` (detailed)
- **Checklist**: `FASE_3_CHECKLIST.md` (step-by-step)
- **Full Guide**: `FASE_3_DEPLOYMENT.md` (comprehensive)

---

**Time to Live**: 5-10 minutes ⏱️
**Difficulty**: Easy ✅
**Support**: Claude Haiku 4.5 is ready to help! 🤖
