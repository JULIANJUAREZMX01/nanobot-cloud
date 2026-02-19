# 🚀 Fase 3: Deploy en Render + Sincronización GitHub

**Fecha**: 18 Febrero 2025
**Status**: 🔄 En Progreso
**Objetivo**: Desplegar Nanobot en Render (cloud) y sincronizar con GitHub

---

## 📋 Tareas de Fase 3

### 1. Preparación Pre-Deployment

- [x] Verificar estructura de archivos
- [ ] Crear `.env` con variables de configuración
- [ ] Verificar `render.yaml` válido
- [ ] Validar `Dockerfile`
- [ ] Limpiar archivos innecesarios

### 2. GitHub Repository

- [x] Repositorio existente: https://github.com/JULIANJUAREZMX01/nanobot-cloud
- [ ] Push de código Phase 2
- [ ] Sincronización de ramas
- [ ] Configurar GitHub Secrets

### 3. Configuración de Render

- [ ] Conectar repositorio GitHub a Render
- [ ] Crear aplicación en Render.com
- [ ] Configurar variables de entorno
- [ ] Configurar dominio
- [ ] Establecer auto-deploy

### 4. Testing en Cloud

- [ ] Verificar startup del bot
- [ ] Enviar mensaje de prueba en Telegram
- [ ] Verificar logging en Render
- [ ] Probar dashboard en cloud

### 5. Sincronización y Backups

- [ ] Configurar S3 bucket (opcional)
- [ ] Verificar GitHub Actions workflows
- [ ] Ejecutar primer backup automático
- [ ] Documentar procedimientos

---

## 🔐 Variables de Entorno Necesarias

```bash
# Telegram
TELEGRAM_TOKEN=[BOT_TOKEN]

# LLM Providers
GROQ_API_KEY=[GROQ_KEY]
ANTHROPIC_API_KEY=[ANTHROPIC_KEY]

# AWS S3 (Opcional)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
S3_BUCKET=nanobot-backups-quintana

# App Config
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
```

---

## 📁 Estructura de Directorios Validada

```
C:\Users\QUINTANA\sistemas\NANOBOT/
├── .github/
│   └── workflows/              ← CI/CD pipelines
├── app/
│   ├── cloud/                  ← Dashboard, MCP, backups
│   ├── core/                   ← Agent loop, tools
│   ├── config/                 ← Configuration
│   ├── utils/                  ← Utilities
│   └── main.py                 ← Entry point ✅
├── config/                     ← YAML configs
├── infrastructure/
│   ├── Dockerfile              ← Docker build ✅
│   ├── docker-compose.yml      ← Local dev ✅
│   └── render.yaml             ← Render deployment ✅
├── tests/                      ← Test suite
├── workspace/                  ← Agent workspace
├── web/                        ← Dashboard frontend
├── pyproject.toml              ← Poetry config ✅
└── README.md                   ← Documentation
```

---

## 🔗 GitHub Repository Status

**Repo**: https://github.com/JULIANJUAREZMX01/nanobot-cloud
**Rama Principal**: `main`
**Última Actualización**: Phase 2 completada localmente

### Próximos Pasos:

1. Sincronizar código Phase 2 (app/ completo)
2. Push a GitHub
3. Verificar Actions workflows

---

## 🎯 Render Deployment Checklist

### Pre-Deployment

- [ ] Crear cuenta en https://render.com (si no existe)
- [ ] Conectar GitHub account a Render
- [ ] Generar GitHub Personal Access Token (si necesario)

### En Render Dashboard

- [ ] New → Web Service
- [ ] Conectar repositorio: `nanobot-cloud`
- [ ] Configurar build command: `pip install poetry && poetry install`
- [ ] Configurar start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Secrets en Render

```
TELEGRAM_TOKEN         → Tu token de bot Telegram
GROQ_API_KEY          → API key de Groq
ANTHROPIC_API_KEY     → API key de Anthropic
ENVIRONMENT           → production
S3_BUCKET             → (opcional)
AWS_ACCESS_KEY_ID     → (opcional)
AWS_SECRET_ACCESS_KEY → (opcional)
```

---

## 🧪 Testing Strategy

### 1. Local Testing (Pre-Deploy)

```bash
# Build Docker image
docker build -t nanobot-local -f infrastructure/Dockerfile .

# Run locally
docker-compose -f infrastructure/docker-compose.yml up

# Test health check
curl http://localhost:8000/api/status
```

### 2. Cloud Testing (Post-Deploy)

```bash
# Test health check
curl https://nanobot.onrender.com/api/status

# Test Telegram
# Enviar mensaje a bot → recibir respuesta
```

### 3. Dashboard

```bash
# Local: http://localhost:8000
# Cloud: https://nanobot.onrender.com
```

---

## 🔄 Flujo de Deployment

```
1. Código Local (Phase 2 completada)
        ↓
2. Push a GitHub
        ↓
3. GitHub Actions Trigger
   - Run tests
   - Build Docker image
        ↓
4. Render Auto-Deploy
   - Pull latest from GitHub
   - Build container
   - Start uvicorn
   - Expone en HTTPS
        ↓
5. Bot en Vivo 24/7
   - Telegram polling
   - Cloud hosting
   - Auto-restart si falla
```

---

## 📊 Comandos Útiles

### Local Development

```bash
# Instalar dependencias
poetry install

# Ejecutar tests
pytest tests/ -v

# Correr app localmente
python -m uvicorn app.main:app --reload

# Docker build
docker build -t nanobot .

# Docker run
docker run -p 8000:8000 --env-file .env nanobot
```

### GitHub CLI

```bash
# Push de cambios
git add .
git commit -m "Fase 3: Deploy en Render setup"
git push origin main

# Ver status
git status
git log --oneline -10
```

### Render CLI (opcional)

```bash
# Instalar Render CLI
npm install -g @render-oss/render-cli

# Deploy
render deploy --service-id=<service-id>
```

---

## 📝 Archivos Críticos para Fase 3

### `render.yaml`

- Define build & start commands
- Especifica variables de entorno
- Configura región y recursos

### `Dockerfile`

- Multi-stage build
- Python 3.11 + dependencias
- Expone puerto 8000

### `.github/workflows/deploy.yml`

- Trigger: Push a main
- Build y test
- Deploy automático a Render

### `pyproject.toml`

- Dependencias pinned
- Poetry lock file para reproducibilidad

---

## 🚨 Troubleshooting

### Bot no responde

1. Verificar logs en Render dashboard
2. Revisar variables de entorno
3. Verificar Telegram token válido

### Errores de build

1. Revisar Poetry dependencies
2. Verificar Python version (3.11+)
3. Limpiar cache: `poetry cache clear --all`

### Dashboard no carga

1. Verificar web/index.html existe
2. Revisar logs de FastAPI
3. Acceder a `/api/status` primero

---

## ✅ Validación Post-Deployment

```python
# Checklist
✓ Bot responde en < 3 segundos
✓ Dashboard accesible
✓ Logs disponibles en Render
✓ Health check retorna status 200
✓ MCP server corriendo (si aplica)
✓ Backups ejecutados
✓ GitHub Actions workflows activos
```

---

## 🎯 Métricas de Éxito

| Métrica             | Meta    |
| ------------------- | ------- |
| **Uptime**          | > 99%   |
| **Response time**   | < 3s    |
| **Error rate**      | < 1%    |
| **Memory usage**    | < 256MB |
| **Deployment time** | < 5min  |

---

## 📌 Notas Importantes

1. **Telegram Token**: Nunca commitar al repo, usar secrets
2. **S3 Backups**: Opcional en Fase 3, pero recomendado
3. **Dominio**: Render genera \*.onrender.com automáticamente
4. **Auto-restart**: Render reinicia automáticamente si hay crash
5. **Scaling**: Free tier soporta ~100 req/min

---

## 🔗 Recursos Útiles

- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com/
- Docker Hub: https://hub.docker.com/
- GitHub Actions: https://github.com/features/actions

---

**Próxima Fase**: Fase 4 - Testing E2E + Validación
**Status**: 🟡 En Setup
**ETA**: 1-2 horas
