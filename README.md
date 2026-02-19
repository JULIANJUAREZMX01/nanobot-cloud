# Nanobot Cloud Deployment 🤖

AI Assistant for QUINTANA - Deployed on Render with Telegram, Dashboard, MCP Server, and S3 Backups.

## Architecture

```
Telegram Bot (polling) → FastAPI app (8000) → Groq/Anthropic LLM
                      ↓
                Dashboard (web UI)
                MCP Server (Claude Code CLI)
                S3 Backups (scheduled)
```

## Quick Start - Local Development

### Prerequisites
- Python 3.11+
- Poetry
- Docker + Docker Compose (optional)

### Setup

1. **Clone and prepare:**
   ```bash
   cd C:\Users\QUINTANA\sistemas\NANOBOT
   cp .env.example .env
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Run locally:**
   ```bash
   poetry run python -m uvicorn app.main:app --reload
   ```

   Or with Docker:
   ```bash
   docker-compose up -d
   ```

4. **Access:**
   - Dashboard: http://localhost:8000
   - API: http://localhost:8000/api/status

## Cloud Deployment - Render

### 1. Connect Repository
```bash
git push origin main
```

### 2. Create Render Service
1. Go to https://render.com
2. Create new Web Service
3. Connect this repository
4. Build command: `pip install poetry && poetry install`
5. Start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`

### 3. Configure Environment Variables
In Render dashboard, set:
- `TELEGRAM_TOKEN` - Telegram bot token
- `TELEGRAM_USER_ID` - Your Telegram ID (8247886073)
- `GROQ_API_KEY` - Groq API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `AWS_ACCESS_KEY_ID` - (optional) For S3 backups
- `AWS_SECRET_ACCESS_KEY` - (optional) For S3 backups
- `S3_BUCKET` - (optional) S3 bucket name
- `ENVIRONMENT` - Set to `production`

### 4. Deploy
Push changes to main branch:
```bash
git push origin main
```

## File Structure

```
NANOBOT/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── core/                # Agent loop & context
│   ├── cloud/               # Telegram, dashboard, MCP, backups
│   ├── config/              # Settings & schemas
│   └── utils/               # Logging, helpers
├── web/                     # Dashboard UI (HTML + JS)
├── infrastructure/          # Docker, Render config
├── config/                  # YAML configuration templates
├── workspace/               # Workspace templates (SOUL, USER, AGENTS, MEMORY)
├── scripts/                 # Utility scripts
├── tests/                   # Test suite
├── .github/workflows/       # CI/CD workflows
├── pyproject.toml           # Python dependencies
├── Dockerfile               # Docker image
├── docker-compose.yml       # Local development
└── render.yaml              # Render deployment config
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard (HTML) |
| GET | `/api/status` | Health check |
| GET | `/api/sessions` | List sessions |
| GET | `/api/memory` | Get MEMORY.md |
| POST | `/api/memory` | Update MEMORY.md |
| GET | `/api/skills` | List skills |
| GET | `/api/logs` | Recent logs |

## Telegram Bot Commands

- `/start` - Initialize conversation
- Send message → Agent responds

## CI/CD Workflows

### deploy.yml
Auto-deploys to Render on push to `main`

### test.yml
Runs pytest, black, ruff on every push

### backup.yml
Scheduled backup to S3 every 6 hours

## MCP Server Integration

Access Nanobot from Claude Code CLI:

```bash
mcp connect app/cloud/mcp_server.py
```

### Available Tools
- `read_nanobot_memory(key)` - Read memory
- `add_nanobot_skill(name, content)` - Create skill
- `list_sessions()` - List conversations
- `get_nanobot_status()` - Health check

## Configuration

### Environment Variables (`.env`)
```
TELEGRAM_TOKEN=your_token_here
TELEGRAM_USER_ID=8247886073
GROQ_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
AWS_ACCESS_KEY_ID=optional
AWS_SECRET_ACCESS_KEY=optional
S3_BUCKET=optional
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Workspace Files
- `workspace/SOUL.md` - Agent identity & personality
- `workspace/USER.md` - User profile & preferences
- `workspace/AGENTS.md` - Operating instructions
- `workspace/MEMORY.md` - Persistent memory
- `workspace/skills/` - Custom skills

## Development

### Run Tests
```bash
poetry run pytest tests/ -v
```

### Format Code
```bash
poetry run black app/
```

### Lint
```bash
poetry run ruff check app/
```

## Troubleshooting

### Telegram Bot Not Responding
1. Verify `TELEGRAM_TOKEN` in `.env`
2. Check logs: `docker logs nanobot-cloud`
3. Ensure Telegram channel is enabled in config

### Dashboard Not Loading
1. Check port 8000 is accessible
2. Verify web files in `./web/`
3. Check browser console for errors

### S3 Backups Failing
1. Verify AWS credentials in Render dashboard
2. Ensure S3 bucket exists and is writable
3. Check backup logs: `docker logs nanobot-cloud`

## Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Make changes
3. Run tests: `poetry run pytest`
4. Commit: `git commit -am "message"`
5. Push: `git push origin feature/name`
6. Open PR

## Security

- Telegram token and API keys are environment secrets (never in repo)
- S3 credentials use IAM roles (when possible)
- HTTPS enforced on Render
- Sessions stored locally (not exposed)

## License

MIT - See LICENSE file

## Author

Julian Juarez (QUINTANA)

---

**Status**: 🟢 Production Ready
