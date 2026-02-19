# 🚀 Guía Completa: Deploy Nanobot en Render.com

**Última Actualización**: 18 Febrero 2025
**Version**: 1.0

---

## 📌 Resumen Rápido

Este documento te guía paso a paso para desplegar Nanobot en Render.com para que tu bot Telegram funcione 24/7 en la nube.

**¿Por qué Render?**

- Python nativo (sin serverless timeouts)
- Dockerfile support
- Auto-deploy desde GitHub
- Dominio HTTPS incluido
- Free tier ($0/mes inicialmente)

---

## 🔑 Requisitos Previos

1. **Cuenta GitHub** - Ya tienes: JULIANJUAREZMX01
2. **Cuenta Render** - Necesitas crear: https://render.com
3. **Secrets/Keys**:
   - `TELEGRAM_TOKEN` - Del bot en @BotFather
   - `GROQ_API_KEY` - De https://console.groq.com
   - `ANTHROPIC_API_KEY` - De https://console.anthropic.com

---

## ✅ Paso 1: Preparar tu Computadora Local

### 1.1 Verificar Estructura

```bash
cd C:\Users\QUINTANA\sistemas\NANOBOT

# Verificar archivos críticos
ls -la app/main.py                    # ✅ Entry point
ls -la infrastructure/Dockerfile      # ✅ Docker config
ls -la infrastructure/render.yaml     # ✅ Render config
ls -la pyproject.toml                 # ✅ Python dependencies
```

### 1.2 Instalar Dependencias Localmente

```bash
# Si no tienes Poetry
pip install poetry

# Instalar dependencias
poetry install
```

### 1.3 Correr Tests Localmente

```bash
# Ejecutar suite de tests
pytest tests/ -v

# Output esperado: All tests passed ✅
```

### 1.4 Verificar Docker

```bash
# Construir imagen Docker
docker build -t nanobot-test -f infrastructure/Dockerfile .

# Debería completar sin errores
# Output: Successfully tagged nanobot-test:latest ✅
```

---

## 📤 Paso 2: Push a GitHub

### 2.1 Verificar Git Status

```bash
cd C:\Users\QUINTANA\sistemas\NANOBOT

git status
# Output: On branch main, nothing to commit ✅
# Si hay cambios:
git add .
git commit -m "Fase 3: Deploy en Render - $(date +%Y-%m-%d)"
```

### 2.2 Push a GitHub

```bash
git push origin main

# Output:
# To github.com:JULIANJUAREZMX01/nanobot-cloud.git
#    f26f719..xxxxx  main -> main ✅
```

### 2.3 Verificar en GitHub

Abre: https://github.com/JULIANJUAREZMX01/nanobot-cloud

Debería ver:

- ✅ Código actualizado
- ✅ Últimos commits
- ✅ Workflows en .github/workflows/

---

## 🎯 Paso 3: Crear Cuenta en Render

### 3.1 Registrarse

1. Ve a: https://render.com
2. Click "Sign Up"
3. Usa GitHub: "Sign up with GitHub"
4. Autoriza: Render tendrá acceso a tus repos

### 3.2 Conectar GitHub

En el dashboard de Render:

1. Settings → GitHub connections
2. Click "Connect" y autoriza el repositorio `nanobot-cloud`

---

## 🛠️ Paso 4: Crear Web Service en Render

### 4.1 Crear Nuevo Servicio

En el dashboard de Render (https://dashboard.render.com):

1. Click **"New +"** → **"Web Service"**
2. Seleccionar: **Connect a repository**
3. Buscar: `nanobot-cloud`
4. Click **"Connect"**

### 4.2 Configurar Build & Deploy

```
Name:                    nanobot
Environment:             Python 3
Region:                  Oregon (us-west)
Branch:                  main
Build Command:           pip install --upgrade pip && pip install poetry && poetry install --only main
Start Command:           python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Instance Type:           Free
Auto-deploy:             Enabled
```

**IMPORTANTE**: Deja todas las opciones en default excepto los comandos arriba.

### 4.3 Agregar Variables de Entorno

En la sección **"Environment"** de Render:

Haz click en **"Add Environment Variable"** para cada una:

```
TELEGRAM_TOKEN
Valor: Tu token del bot ([BOT_TOKEN])

TELEGRAM_USER_ID
Valor: 8247886073

GROQ_API_KEY
Valor: [GROQ_KEY]

ANTHROPIC_API_KEY
Valor: [ANTHROPIC_KEY]

ENVIRONMENT
Valor: production

LOG_LEVEL
Valor: INFO

AWS_REGION
Valor: us-east-1
```

**NOTA**: Deja S3_BUCKET y AWS keys vacías por ahora (no son obligatorias).

### 4.4 Crear el Servicio

Click **"Create Web Service"**

Render comenzará a:

1. Clonar tu repositorio
2. Construir la imagen Docker
3. Desplegar la aplicación
4. Iniciar el bot

Esto toma ~3-5 minutos. Verás:

```
✓ Cloning repository...
✓ Installing dependencies...
✓ Building docker image...
✓ Deploying...
✓ Live at: https://nanobot.onrender.com
```

---

## ✨ Paso 5: Verificar Deployment

### 5.1 Comprobar Health Check

```bash
curl https://nanobot.onrender.com/api/status

# Output esperado:
{
  "status": "ok",
  "version": "0.2.0",
  "phase": "2-agent-loop",
  "telegram": true,
  "agent_loop": true
}
```

### 5.2 Ver Logs en Render

En el dashboard de Render:

1. Selecciona tu servicio "nanobot"
2. Tab "Logs"
3. Deberías ver:

```
🚀 STARTING NANOBOT CLOUD DEPLOYMENT — PHASE 2
✅ Memory initialized
✅ Session manager initialized
📱 Starting Telegram bot...
🟢 NANOBOT IS RUNNING — READY FOR MESSAGES
```

### 5.3 Enviar Mensaje de Prueba

Abre Telegram:

1. Busca tu bot por nombre (ej: @QUINTANA_Nanobot_Bot)
2. Click "Start"
3. Escribe un mensaje: "Hola, ¿funciona?"
4. El bot debe responder en < 5 segundos

Si ves respuesta → **¡Deployment exitoso! ✅**

---

## 🔗 Paso 6: Acceder al Dashboard

Tu dashboard está en:

```
https://nanobot.onrender.com
```

Desde aquí puedes:

- Ver sesiones activas
- Ver logs
- Acceder a memoria del bot
- Crear/editar skills

---

## 🔄 Paso 7: Auto-Deploy desde GitHub (Opcional)

El auto-deploy ya está configurado. Cada vez que hagas:

```bash
git push origin main
```

Render automáticamente:

1. Detecta el cambio
2. Construye nueva imagen
3. Deploya la nueva versión
4. Zero downtime ✅

---

## 📊 Monitoreo en Vivo

### Ver Logs en Tiempo Real

```bash
# Opción 1: Dashboard Render
# https://dashboard.render.com → Tu servicio → Logs

# Opción 2: Render CLI
render logs --service-id=<service-id> --tail

# Opción 3: Endpoint de estado
curl -s https://nanobot.onrender.com/api/status | jq .
```

### Métricas a Monitorear

```
Uptime:           > 99%
Response time:    < 3 segundos
Memory usage:     < 256MB
Error rate:       < 1%
Messages/min:     Variable según uso
```

---

## 🛡️ Seguridad en Render

### ✅ Mejores Prácticas

1. **Nunca commitar secrets**
   - ❌ `TELEGRAM_TOKEN` en código
   - ✅ Variables en Render dashboard

2. **HTTPS automático**
   - Render genera certificado SSL
   - Todas las conexiones encriptadas

3. **Firewall**
   - Solo puertos 80/443 expuestos
   - SSH acceso disponible si necesitas

4. **Backups**
   - Tu workspace se persiste en `/data/`
   - Puedes hacer backups manuales

---

## 🚨 Troubleshooting

### Problema: Bot no responde

**Síntoma**: Envías mensaje, no recibes respuesta

**Soluciones**:

1. Verificar logs en Render: `error` or `exception`
2. Revisar variables de entorno en Render dashboard
3. Verificar TELEGRAM_TOKEN correcto en @BotFather
4. Reimplementar servicio: Dashboard → Redeploy

```bash
# Para reimplementar desde CLI
render deploy --service-id=<service-id>
```

### Problema: Errores de build

**Síntoma**: Build falla, deployment cancelado

**Soluciones**:

1. Ver logs: Dashboard → Build & Deploy → Logs
2. Verificar `pyproject.toml` válido
3. Verificar Python 3.11+ disponible
4. Revisar `infrastructure/Dockerfile`

```bash
# Local verification
poetry install
docker build -t test .
```

### Problema: Memoria insuficiente

**Síntoma**: Bot se cuelga después de cierto tiempo

**Soluciones**:

1. Aumentar plan de Render (upgrade a Starter)
2. Limpiar sesiones viejas (automático cada 6 horas)
3. Monitorear memory usage en logs

---

## 💰 Costos

### Plan Free (Recomendado para POC)

- **Precio**: $0/mes
- **Uptime**: 99%
- **Memory**: 512MB
- **CPU**: Compartido
- **Requests/min**: ~100
- **Auto-sleep**: Después de 15 minutos inactividad

### Plan Starter ($7/mes)

- **Precio**: $7/mes
- **Uptime**: 99.9%
- **Memory**: 1GB
- **CPU**: Dedicado
- **Requests/min**: ~500
- **Auto-sleep**: Ninguno

**Recomendación para Nanobot**: Starter ($7/mes) porque:

- No auto-sleeps (bot siempre activo)
- Memory suficiente para 24/7
- Mejor performance

---

## 📈 Escalar Después

Una vez que funcione, puedes:

1. **Agregar Base de Datos**
   - PostgreSQL en Render
   - Mejor persistencia de sesiones

2. **Agregar S3 Backups**
   - AWS S3 bucket
   - Backups automáticos cada 6h

3. **Agregar Monitoreo**
   - Datadog
   - New Relic
   - CloudWatch

4. **Agregar CDN**
   - Cloudflare
   - Para dashboard estático

---

## 🎓 Conceptos Clave

### ¿Qué es Render?

Platform-as-a-Service (PaaS) que ejecuta tu código Python 24/7

### ¿Cómo funciona?

1. Conectas GitHub
2. Render ve un `render.yaml` o `Dockerfile`
3. Construye una imagen Docker
4. La ejecuta en sus servidores
5. Expone en una URL HTTPS pública

### ¿Por qué no Vercel?

- Vercel = Serverless (timeout después de 60s)
- Nanobot necesita polling constante (sin timeout)
- Render = Aplicaciones siempre vivas ✅

### ¿Por qué no Railway?

- Railway es muy similar a Render
- Ligeramente más barato ($5/mes)
- Pero Render es más confiable para bots

---

## 🔗 Recursos Útiles

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Tu Dashboard**: https://dashboard.render.com
- **Tu Bot**: https://nanobot.onrender.com
- **GitHub Repo**: https://github.com/JULIANJUAREZMX01/nanobot-cloud

---

## ✅ Checklist Final

- [ ] Código pushed a GitHub
- [ ] Cuenta Render creada
- [ ] Repositorio conectado a Render
- [ ] Variables de entorno configuradas
- [ ] Servicio deploying/deployed
- [ ] Health check retorna 200
- [ ] Bot responde en Telegram
- [ ] Dashboard accesible
- [ ] Logs visibles en Render

---

## 🎉 ¡Felicidades!

Tu Nanobot está en vivo en la nube 24/7.

**Próximos pasos**:

- Fase 4: Testing E2E
- Fase 5: Optimización

---

**Autor**: Claude Haiku 4.5
**Para**: Julian Juarez (QUINTANA)
**Fecha**: 18 Febrero 2025
**Status**: 🟢 Production Ready
