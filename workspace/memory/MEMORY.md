# Memoria Persistente — QUINTANA Dev Assistant

## Información del Usuario

- **Nombre completo**: Julian Juarez
- **ID Telegram**: 8247886073
- **Nombre de trabajo**: QUINTANA
- **Rol**: Desarrollador senior, arquitecto de sistemas
- **Ubicación**: México (UTC-6)
- **Idioma**: español siempre
- **Dispositivos**: PC Windows 10 (principal) + móvil
- **Modelo AI preferido**: Groq (primary) + Anthropic Claude (fallback)

## Intereses & Herramientas

- Explicaciones y respuestas con IA
- Visualización de ideas
- DevOps, cloud deployment
- Automation & productivity

## Proyectos Conocidos (C:/Users/QUINTANA/sistemas/)

- **CATALYST**: proyecto activo — revisar estado actual al preguntar
- **JAJA.DEV**: sitio/app jaja.dev — desarrollo web
- **MueveCancun_PWA**: PWA de transporte en Cancún
- **qdash**: dashboard
- **SAC_V01_427_ADMJAJA**: sistema atención cliente
- **NANOBOT**: el agente mismo (nanobot v0.1.3.post6)
- **tools**: kubectl, helm, minikube, herramientas devops
- **archive**: proyectos archivados

## Setup Actual — Nanobot Cloud + Telegram + Claude

### Canal: Telegram

- **Bot Token**: [REDACTED_TOKEN]
- **User ID**: 8247886073
- **Status**: ✅ Activo en Render
- **Ventaja**: Sin bridge, sin QR, simple

### LLM: Groq + Anthropic

- **Modelo Primary**: groq/llama-3.3-70b-versatile
- **Modelo Fallback**: claude-opus-4-5
- **Tokens**: 8192 (max)
- **Temperatura**: 0.7
- **Tool Iterations**: 30

### Infraestructura Cloud

- **Plataforma**: Render (chosen over Vercel/Railway)
- **Config**: `C:/Users/QUINTANA/sistemas/NANOBOT/`
- **Startup**: Auto-start en Render
- **Backup**: S3 cada 6 horas (vía GitHub Actions)

## Fase 1 Completada ✅

- ✅ Estructura de carpetas organizada (app/, web/, infrastructure/, config/)
- ✅ `pyproject.toml` con todas las dependencias
- ✅ Dockerfile multi-stage + docker-compose.yml
- ✅ FastAPI app + Telegram bot integration
- ✅ Dashboard minimalista (web UI)
- ✅ MCP server para Claude Code CLI
- ✅ Backup service para S3
- ✅ GitHub Actions workflows (deploy, test, backup)
- ✅ Workspace templates (SOUL, USER, AGENTS, MEMORY)
- ✅ README.md con instrucciones completas

## Preferencias de Interacción

- Respuestas en español, concisas
- Directo al grano — no explicaciones básicas
- Confirmar antes de operaciones destructivas
- git commit/push solo si se pide
- Mostrar output real de comandos
- Acceso completo a C:/Users/QUINTANA/sistemas/

## Notas Técnicas

- WhatsApp deshabilitado (problemas con bridge/QR)
- Telegram es mucho más simple y confiable
- nanobot v0.1.3.post6 como referencia
- Groq configurado como primary (más rápido, gratis)
- Anthropic como fallback (más potente)
- Skill `proyectos-sistemas` always-loaded

## Próximos Pasos

1. Fase 2: Implementar agent loop completo
2. Fase 3: Deploy en Render
3. Fase 4: Dashboard web testing
4. Fase 5: MCP server integration
