# Nanobot Cloud Deployment 🤖

AI Assistant for QUINTANA - Deployed on Render with Telegram, Dashboard, MCP Server, and S3 Backups.

## Quick Start

```bash
# Clone
git clone https://github.com/JULIANJUAREZMX01/nanobot-cloud.git
cd nanobot-cloud

# Setup
cp .env.example .env
poetry install

# Run locally
docker-compose up -d

# Or with uvicorn
poetry run python -m uvicorn app.main:app --reload
```

## Architecture

```
Telegram Bot (polling) → FastAPI (8000) → Groq/Anthropic LLM
                     ↓
              Dashboard UI
              MCP Server
              S3 Backups
```

## Documentation

- **README.md** - This file
- **DEPLOYMENT_STRUCTURE.md** - Architecture overview
- **PHASE_1_SUMMARY.md** - Phase 1 completion summary
- **NEXT_STEPS.md** - Phase 2 implementation guide

## Status

🟢 **Phase 1**: Structure & scaffolding - ✅ Complete  
⏳ **Phase 2**: Agent loop & LLM integration - In progress  
⏳ **Phase 3**: Cloud deployment - Planned  
⏳ **Phase 4**: Testing & validation - Planned  
⏳ **Phase 5**: Polish & optimization - Planned  

## License

MIT

## Author

Julian Juarez (QUINTANA)
