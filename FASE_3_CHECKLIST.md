# ✅ Fase 3: Deployment Checklist - Quick Reference

**Status**: 🟡 Ready for Deployment
**Date**: 18 Febrero 2025

---

## 📋 Pre-Deployment (Local Machine)

### Environment Setup

- [ ] Python 3.11+ installed
- [ ] Poetry installed: `pip install poetry`
- [ ] Git configured: `git config user.email "your@email.com"`
- [ ] Docker installed (optional but recommended)

### Code Verification

- [ ] All files in place:
  ```
  ✓ app/main.py
  ✓ app/core/loop.py
  ✓ app/cloud/providers.py
  ✓ infrastructure/Dockerfile
  ✓ infrastructure/render.yaml
  ✓ pyproject.toml
  ```
- [ ] `.env.example` has NO real secrets
- [ ] `README.md` is updated
- [ ] Tests pass: `pytest tests/ -v`

### Docker Verification

- [ ] Docker image builds: `docker build -t nanobot -f infrastructure/Dockerfile .`
- [ ] No build errors or warnings

### Dependencies

- [ ] `poetry install` completes without errors
- [ ] `poetry lock` file is updated
- [ ] All imports resolve in `app/`

---

## 🔐 Secrets Management

### Verify You Have These Values

- [ ] **TELEGRAM_TOKEN** - From @BotFather
  - Format: [BOT_TOKEN_FORMAT]
  - Test: Send `/getMe` to @BotFather

- [ ] **GROQ_API_KEY** - From console.groq.com
  - Format: [GROQ_KEY_FORMAT]
  - Test: Can access https://api.groq.com

- [ ] **ANTHROPIC_API_KEY** - From console.anthropic.com
  - Format: [ANTHROPIC_KEY_FORMAT]
  - Test: Can access https://api.anthropic.com

- [ ] **TELEGRAM_USER_ID** - Already set to `8247886073`

### Security Checklist

- [ ] Never commit these values to git
- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` only has placeholders
- [ ] Secrets will be set in Render dashboard (not in code)

---

## 📤 GitHub Push

### Prepare Repository

- [ ] `git status` shows clean working tree (or staged changes)
- [ ] No uncommitted changes that you want to keep
- [ ] Latest main branch: `git pull origin main`

### Create Commit

```bash
git add .
git commit -m "Fase 3: Deploy en Render - setup"
git push origin main
```

### Verify Push

- [ ] No errors in push output
- [ ] Check: https://github.com/JULIANJUAREZMX01/nanobot-cloud
- [ ] Verify code is updated on GitHub

---

## 🎯 Render Setup

### Account & Connection

- [ ] Render account created: https://render.com
- [ ] GitHub connected to Render
- [ ] `nanobot-cloud` repo visible in Render

### Create Web Service (Step-by-Step)

1. [ ] Click "New +" → "Web Service"
2. [ ] Select `nanobot-cloud` repository
3. [ ] Set Name: `nanobot`
4. [ ] Set Environment: `Python 3`
5. [ ] Set Region: `Oregon (us-west)`
6. [ ] Set Branch: `main`

### Build & Start Commands

```
Build Command:
pip install --upgrade pip && pip install poetry && poetry install --only main

Start Command:
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- [ ] Copied exactly (no changes)

### Environment Variables (in Render Dashboard)

Add each one using "Add Environment Variable":

```
TELEGRAM_TOKEN         = [TOKEN_DEL_BOT]
TELEGRAM_USER_ID       = 8247886073
GROQ_API_KEY          = [CLAVE_DE_GROQ]
ANTHROPIC_API_KEY     = [CLAVE_DE_ANTHROPIC]
ENVIRONMENT           = production
LOG_LEVEL             = INFO
AWS_REGION            = us-east-1
S3_BUCKET             = (leave empty)
AWS_ACCESS_KEY_ID     = (leave empty)
AWS_SECRET_ACCESS_KEY = (leave empty)
```

- [ ] All required variables set
- [ ] No typos in variable names
- [ ] Values are correct

### Deploy

- [ ] Click "Create Web Service"
- [ ] Wait for build to complete (~3-5 minutes)
- [ ] Check status: should be "Live"
- [ ] URL generated: `https://nanobot.onrender.com`

---

## ✨ Post-Deployment Verification

### Health Check

```bash
# Should return 200 OK
curl https://nanobot.onrender.com/api/status

# Expected response:
{
  "status": "ok",
  "version": "0.2.0",
  "phase": "2-agent-loop",
  "telegram": true
}
```

- [ ] Health check returns 200
- [ ] All fields present in response

### Check Logs

In Render Dashboard → Logs:

```
✓ STARTING NANOBOT CLOUD DEPLOYMENT
✓ Memory initialized
✓ Session manager initialized
✓ Starting Telegram bot
✓ NANOBOT IS RUNNING
```

- [ ] No errors in logs
- [ ] See "NANOBOT IS RUNNING" message
- [ ] No connection timeout errors

### Test Telegram Bot

1. [ ] Open Telegram
2. [ ] Find your bot (@YourBotName)
3. [ ] Send message: "Hola"
4. [ ] Receive response within 5 seconds
5. [ ] No error messages

### Test Dashboard

- [ ] Access: https://nanobot.onrender.com
- [ ] Page loads without errors
- [ ] CSS/styling applied correctly

---

## 🔄 Auto-Deploy Verification

### Trigger Auto-Deploy

```bash
echo "# Test deploy" >> README.md
git add README.md
git commit -m "Test auto-deploy"
git push origin main
```

- [ ] Render automatically detects push
- [ ] Build starts (visible in Render dashboard)
- [ ] New version deployed
- [ ] No downtime during deploy

### Verify Auto-Deploy Worked

- [ ] Bot still responds after deploy
- [ ] No "service restarting" messages
- [ ] New code is live

---

## 📊 Performance Baseline

Measure these metrics for future reference:

```
Response Time (Telegram):       _______ seconds
Memory Usage:                   _______ MB
CPU Usage:                      _______ %
Uptime:                         _______ hours
Build Time:                     _______ minutes
```

Expected ranges:

- Response Time: 1-5 seconds
- Memory: 50-150 MB
- CPU: 5-15%
- Uptime: 99%+
- Build Time: 2-4 minutes

---

## 🚨 Troubleshooting Decision Tree

### "Build failed"

- [ ] Check Render logs for errors
- [ ] Verify `pyproject.toml` is valid
- [ ] Try `poetry install` locally
- [ ] Check Python version (3.11+)

### "Service is restarting"

- [ ] Check logs for crashes
- [ ] Verify all env vars are set correctly
- [ ] Check for null pointer exceptions
- [ ] Increase memory if needed

### "Telegram bot not responding"

- [ ] Verify health check works
- [ ] Check TELEGRAM_TOKEN is correct
- [ ] Check logs for Telegram connection errors
- [ ] Verify @BotFather settings

### "Dashboard won't load"

- [ ] Check `/api/status` endpoint first
- [ ] Verify web/index.html exists
- [ ] Check browser console for JS errors
- [ ] Clear browser cache

### "High memory usage"

- [ ] Check for memory leaks in logs
- [ ] Increase Render plan to Starter
- [ ] Enable session cleanup (auto-hourly)
- [ ] Check for infinite loops

---

## 📞 Support Resources

### If Something Goes Wrong

1. **Check Logs First**
   - Render Dashboard → Your Service → Logs
   - Look for `ERROR`, `EXCEPTION`, `Traceback`

2. **Common Issues**
   - GitHub not connecting: Reconnect in Render settings
   - Env vars wrong: Double-check spelling and values
   - Build slow: First deploy is slower, normal

3. **Rollback**
   - In Render: Click "Redeploy" last successful version
   - On GitHub: Revert commit and push

4. **Get Help**
   - Render Docs: https://render.com/docs
   - Render Status: https://status.render.com
   - GitHub Issues: Open issue in your repo

---

## 🎉 Success Criteria

**Phase 3 is COMPLETE when:**

- ✅ Code pushed to GitHub main branch
- ✅ Render service is "Live"
- ✅ Health check returns 200 OK
- ✅ Telegram bot responds to messages
- ✅ Dashboard accessible at /
- ✅ Logs show "NANOBOT IS RUNNING"
- ✅ Zero errors in deployment logs
- ✅ Auto-deploy triggers on git push

---

## 📈 Next Phase

Once Phase 3 is complete:

- **Phase 4**: Testing E2E + Validación
  - Load testing
  - Error scenarios
  - Message persistence
  - Multi-user testing

---

**Generated**: 18 Febrero 2025
**For**: Julian Juarez (QUINTANA)
**Status**: 🟢 Ready to Deploy
