# ⏭️ Próximos Pasos — Fase 2

**Estado**: Fase 1 ✅ Completada  
**Objetivo**: Implementar agent loop funcional  
**Duración Estimada**: 1 día

---

## 🎯 Prioridades Fase 2

### 1. Agent Loop Principal (`app/core/loop.py`)
```python
# Crear archivo: app/core/loop.py
# Implementar:
- class AgentLoop:
    - process_message(ctx: AgentContext)
    - call_llm(messages, model)
    - execute_tools(tool_calls)
    - format_response(llm_output)
    - save_session()
```

### 2. Tool Execution (`app/core/tools.py`)
```python
# Crear archivo: app/core/tools.py
# Implementar:
- execute_shell(command: str) → output
- read_file(path: str) → content
- write_file(path: str, content: str)
- git_operation(cmd: str)
- web_fetch(url: str)
```

### 3. LLM Providers (`app/cloud/providers.py`)
```python
# Crear archivo: app/cloud/providers.py
# Implementar:
- class GroqProvider:
    - call(messages, model, max_tokens)
- class AnthropicProvider:
    - call(messages, model, max_tokens)
- class ProviderManager:
    - get_provider(primary/fallback)
    - retry_logic()
```

### 4. Session Management (`app/cloud/sessions.py`)
```python
# Crear archivo: app/cloud/sessions.py
# Implementar:
- load_session(session_id) → ctx
- save_session(ctx)
- list_sessions()
- cleanup_old_sessions()
```

---

## 📋 Checklist de Implementación

### Core Agent Loop
- [ ] Crear `app/core/loop.py`
- [ ] Integrar con Telegram handler
- [ ] Prueba local: enviar mensaje → respuesta
- [ ] Sesiones guardadas en `data/sessions/*.jsonl`

### Tool Execution
- [ ] Crear `app/core/tools.py`
- [ ] Shell command execution
- [ ] File read/write
- [ ] Git operations
- [ ] Web fetching

### LLM Integration
- [ ] Crear `app/cloud/providers.py`
- [ ] Groq API integration
- [ ] Anthropic fallback
- [ ] Token tracking
- [ ] Error handling

### Session Management
- [ ] Crear `app/cloud/sessions.py`
- [ ] JSONL persistence
- [ ] Context loading
- [ ] Session cleanup

### Testing
- [ ] Update tests in `tests/`
- [ ] Integration tests
- [ ] End-to-end local test

---

## 🔧 Cambios a `app/main.py`

```python
# Actualizar imports
from app.core.loop import AgentLoop
from app.cloud.providers import ProviderManager
from app.cloud.sessions import SessionManager

# En lifespan, inicializar:
_agent_loop = AgentLoop(settings)
_provider_manager = ProviderManager(settings)
_session_manager = SessionManager()

# En Telegram handler, llamar:
response = await _agent_loop.process_message(ctx)
```

---

## 📝 Cambios a `app/cloud/telegram_bot.py`

```python
# Actualizar handle_message()
async def handle_message(update, context):
    # Crear contexto
    ctx = AgentContext(...)
    
    # Obtener sesión previa
    ctx = await _session_manager.load_session(ctx.session_id)
    ctx.add_message("user", message.text)
    
    # Procesar con agent loop
    response = await _agent_loop.process_message(ctx)
    
    # Guardar sesión
    await _session_manager.save_session(ctx)
    
    # Responder
    await message.reply_text(response)
```

---

## 🧪 Testing Local

```bash
# 1. Setup
cd C:\Users\QUINTANA\sistemas\NANOBOT
poetry install

# 2. Copiar .env
cp .env.example .env
# Editar .env con valores reales

# 3. Correr local
poetry run python -m uvicorn app.main:app --reload

# 4. Prueba Dashboard
# http://localhost:8000

# 5. Prueba Telegram
# Enviar mensaje a bot → debe responder

# 6. Verificar sesión
# cat ./data/sessions/telegram_*.jsonl
```

---

## 🐳 Testing con Docker

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f nanobot

# Stop
docker-compose down
```

---

## 📚 Archivos de Referencia

**Para entender la estructura actual:**
- `README.md` — Setup general
- `app/main.py` — Entry point
- `app/cloud/telegram_bot.py` — Telegram integration

**Para copiar código de nanobot original:**
- `nanobot/nanobot/agent/` — Agent loop reference
- `nanobot/nanobot/providers/` — LLM providers reference
- `nanobot/nanobot/tools/` — Tool execution reference

---

## 🎓 Decisiones de Diseño

### Agent Loop
- **Async throughout** — FastAPI/asyncio compatible
- **Context-based** — AgentContext carries all state
- **Tool-agnostic** — Tools pluggable

### LLM Providers
- **Groq first** — Primary (faster, free)
- **Claude fallback** — If Groq fails
- **Retry logic** — Exponential backoff

### Session Storage
- **JSONL format** — One message per line
- **File-based** — No DB dependency
- **Async writes** — Non-blocking

### Error Handling
- **Graceful fallback** — Groq → Claude
- **User-friendly** — "Parece que hay un problema..."
- **Logging** — All errors logged

---

## 🔐 Consideraciones Seguridad

- ✅ Never log API keys
- ✅ Sanitize shell commands
- ✅ Validate file paths (no escape dir)
- ✅ Rate limit tool calls
- ✅ Timeout long-running operations

---

## 🚀 Deploy Timeline

| Milestone | Fecha Estimada | Status |
|-----------|----------------|--------|
| Fase 1 ✅ | 18 Feb | ✅ Completado |
| Fase 2 | 19 Feb | ⏳ En progreso |
| Fase 3 (Deploy) | 20 Feb | ⏳ Próximo |
| Fase 4 (Testing) | 20 Feb | ⏳ Próximo |
| Fase 5 (Polish) | 21 Feb | ⏳ Próximo |
| **Producción** | **21 Feb** | 🎯 Goal |

---

## 📞 Puntos de Contacto

**Para cuestiones:**
- Agent logic → `app/core/loop.py`
- Telegram → `app/cloud/telegram_bot.py`
- LLM → `app/cloud/providers.py`
- Sessions → `app/cloud/sessions.py`
- Testing → `tests/`

---

## 💡 Tips para Implementación

1. **Start small** — Implement basic echo first
2. **Test locally** — Before deploying to Render
3. **Use logging** — Loguru ya está configured
4. **Async everywhere** — No blocking calls
5. **Keep tools simple** — One responsibility each
6. **Error messages** — User-friendly in Spanish

---

## ✅ Definition of Done (Fase 2)

- [ ] Agent loop funcional
- [ ] Groq integration working
- [ ] Claude fallback working
- [ ] Tools executing correctly
- [ ] Sessions persisting
- [ ] Tests passing
- [ ] Local testing successful
- [ ] Ready for Render deploy

---

**Siguiente**: Implementar `app/core/loop.py` + LLM integration
