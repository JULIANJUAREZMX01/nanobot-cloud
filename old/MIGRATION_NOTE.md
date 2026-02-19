# ⚠️ Nota de Migración: Versiones de Nanobot

Este repositorio incluye componentes para dos arquitecturas diferentes. Es importante que elijas cuál vas a usar para evitar confusiones.

## 1. Arquitectura Cloud (Recomendada Actual) ☁️

**Tecnología**: Python + FastAPI + Telegram Bot (Webhook/Polling) + Render.com
**Estado**: ✅ Producción (Fase 3 Completa)
**Característica**: Funciona 24/7 en la nube, no requiere tu PC encendida.
**Archivos Relevantes**:

- `START_HERE.md`
- `RENDER_SETUP_GUIDE.md`
- `app/main.py`
- `infrastructure/Dockerfile`

## 2. Arquitectura Legacy Local (WhatsApp) 📱

**Tecnología**: Node.js Bridge + Python Gateway (Local)
**Estado**: ⚠️ Mantenimiento / Deprecado para Cloud
**Característica**: Requiere una terminal abierta en tu PC y vincular WhatsApp Web.
**Archivos Relevantes (NO USAR en Cloud)**:

- `start-nanobot.bat`
- `start-bridge.bat`
- `start-gateway.bat`

## Instrucción de Uso

Si estás siguiendo la guía `START_HERE.md` para desplegar en Render y usar Telegram, **puedes ignorar o borrar los archivos `.bat`**.

Si deseas usar la versión local de WhatsApp, ignora las guías de Render y usa `start-nanobot.bat` (requiere Node.js instalado).
