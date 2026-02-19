# 📖 Implementation Guide - Nanobot Cloud

## Quick Navigation

### Phase 1: Structure ✅
- **Status**: Completado
- **Files**: `PHASE_1_COMPLETE.md`
- **Summary**: 37 archivos, estructura base, Docker, CI/CD

### Phase 2: Agent Loop ✅
- **Status**: Completado
- **Files**: `PHASE_2_COMPLETE.md`
- **Summary**: Agent loop, LLM providers, tools, sessions

### Phase 3: Deployment 🚀
- **Status**: Próximo
- **Target**: Render cloud platform
- **Steps**: GitHub push → Render deploy

---

## 🚀 Quick Start - Local Development

### 1. Clone Repository
```bash
git clone https://github.com/JULIANJUAREZMX01/nanobot-cloud.git
cd nanobot-cloud
```

### 2. Setup Environment
```bash
# Copy env template
cp .env.example .env

# Edit .env with your API keys
# TELEGRAM_TOKEN=your_token
# GROQ_API_KEY=your_key
# ANTHROPIC_API_KEY=your_key
```

### 3. Install Dependencies
```bash
poetry install
```

### 4. Run Locally

**Option A: Docker Compose**
```bash
docker-compose up -d
# Access: http://localhost:8000
```

**Option B: Direct with Uvicorn**
```bash
poetry run python -m uvicorn app.main:app --reload
# Access: http://localhost:8000
```

### 5. Test Telegram Bot
1. Start your Telegram app
2. Find your bot by token
3. Send `/start` command
4. Send a message
5. Bot responds with agent loop

---

## 📚 Architecture Overview

### Core Components

```
app/
├── main.py              # FastAPI entry point
├── config/
│   └── schema.py        # Pydantic settings
├── core/
│   ├── loop.py         # ✅ Agent loop
│   ├── tools.py        # ✅ Tool executor
│   ├── memory.py       # Memory management
│   └── context.py      # Agent context
├── cloud/
│   ├── telegram_bot.py # ✅ Telegram integration
│   ├── providers.py    # ✅ LLM providers
│   ├── sessions.py     # ✅ Session manager
│   ├── dashboard.py    # Dashboard API
│   ├── backup_service.py
│   └── mcp_server.py
└── utils/
    └── logger.py       # Logging setup
```

### Flow Diagram

```
Telegram Message
    ↓
telegram_bot.py (handle_message)
    ↓
Load/Create AgentContext
    ↓
AgentLoop.process_message()
    ├─ Call LLM (Groq primary, Claude fallback)
    ├─ Parse tool calls
    ├─ Execute tools via ToolExecutor
    └─ Generate response
    ↓
SessionManager.save_session()
    ↓
Send response to Telegram
```

---

## 🛠️ Key Features

### Agent Loop (`app/core/loop.py`)
- Iterative message processing (max 10 iterations)
- LLM integration with fallback logic
- Tool execution orchestration
- Context and history management
- Error handling and timeouts

### LLM Providers (`app/cloud/providers.py`)
- **Groq** (Primary): Fast, free, Llama 3.3 70B
- **Anthropic** (Fallback): Powerful, reliable Claude
- Retry logic with exponential backoff
- Timeout management (30s per call)

### Tool Executor (`app/core/tools.py`)
1. **execute_shell** - Run commands
2. **read_file** - Read files
3. **write_file** - Write files
4. **list_files** - List directories
5. **git_command** - Git operations
6. **web_fetch** - HTTP requests

### Session Manager (`app/cloud/sessions.py`)
- JSONL-based persistence
- Automatic session loading
- Cleanup of old sessions (7+ days)
- Session statistics

---

## 🧪 Testing

### Run All Tests
```bash
poetry run pytest tests/ -v
```

### Run Specific Test Suite
```bash
poetry run pytest tests/test_agent_loop.py -v
poetry run pytest tests/test_providers.py -v
poetry run pytest tests/test_tools.py -v
```

### Test Coverage
```bash
poetry run pytest tests/ --cov=app
```

---

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Dashboard UI |
| GET | `/api/status` | Health check |
| GET | `/api/sessions` | List sessions |
| GET | `/api/memory` | Get memory content |
| POST | `/api/memory` | Update memory |
| GET | `/api/skills` | List skills |
| GET | `/api/logs` | View logs |

---

## 🔐 Environment Variables

**Required:**
```
TELEGRAM_TOKEN=your_bot_token
GROQ_API_KEY=your_groq_key
ANTHROPIC_API_KEY=your_anthropic_key
```

**Optional:**
```
AWS_ACCESS_KEY_ID=for_s3_backups
AWS_SECRET_ACCESS_KEY=for_s3_backups
S3_BUCKET=bucket_name
ENVIRONMENT=production|development
LOG_LEVEL=INFO|DEBUG
```

---

## 🚀 Deployment to Render

### 1. Push to GitHub
```bash
git add .
git commit -m "Phase 2: Agent Loop + LLM Integration"
git push origin main
```

### 2. Create Render Service
1. Go to https://render.com
2. New Web Service
3. Connect GitHub repo
4. Configure:
   - **Build Command**: `pip install poetry && poetry install`
   - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`

### 3. Set Environment Variables
In Render dashboard:
- TELEGRAM_TOKEN
- TELEGRAM_USER_ID
- GROQ_API_KEY
- ANTHROPIC_API_KEY
- ENVIRONMENT=production

### 4. Deploy
- Push to main branch
- Render auto-deploys
- Access at: https://nanobot.onrender.com

---

## 📊 Monitoring

### Logs
```bash
# Local
docker logs nanobot-cloud

# Render
# View in Render dashboard
```

### Health Check
```bash
curl http://localhost:8000/api/status
```

### Session Stats
```bash
curl http://localhost:8000/api/sessions
```

---

## 🐛 Troubleshooting

### Telegram Bot Not Responding
1. Check `TELEGRAM_TOKEN` in `.env`
2. Verify bot is running: `docker logs nanobot-cloud`
3. Test with curl: `curl http://localhost:8000/api/status`

### LLM Provider Errors
1. Verify API keys: `GROQ_API_KEY`, `ANTHROPIC_API_KEY`
2. Check rate limits
3. Try fallback: Claude should kick in if Groq fails

### File Permissions
1. Ensure `./workspace/` is writable
2. Check `./data/sessions/` exists
3. Run with proper permissions

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

---

## 📞 Support

### Documentation Files
- `README.md` - Quick start
- `PHASE_1_COMPLETE.md` - Phase 1 details
- `PHASE_2_COMPLETE.md` - Phase 2 details
- `DEPLOYMENT_STRUCTURE.md` - Architecture
- `NEXT_STEPS.md` - Development guide

### Code Comments
All main functions have docstrings explaining their purpose and parameters.

---

## 📈 Performance Tips

1. **LLM Calls**
   - Groq is faster (use as primary)
   - Claude fallback for complex tasks
   - Adjust max_tokens based on needs

2. **Tool Execution**
   - Commands timeout after 30s
   - Files limited to workspace directory
   - Git commands only safe operations

3. **Sessions**
   - Cleanup runs hourly (7+ days old)
   - JSONL format is efficient
   - Consider archiving old sessions

---

## 🎓 Learning Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- Groq API: https://groq.com/groundedness-institute/
- Anthropic API: https://docs.anthropic.com
- Telegram Bot API: https://core.telegram.org/bots/api

---

## 📝 Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Make changes
3. Run tests: `poetry run pytest`
4. Commit: `git commit -am "message"`
5. Push: `git push origin feature/name`
6. Create PR

---

## 📄 License

MIT - See LICENSE file

---

**Version**: 0.2.0  
**Author**: Julian Juarez (QUINTANA)  
**Repository**: https://github.com/JULIANJUAREZMX01/nanobot-cloud
