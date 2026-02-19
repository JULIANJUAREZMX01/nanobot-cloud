# 🛠️ Personalización Avanzada de Nanobot

Esta guía te permite adaptar a Nanobot a tus necesidades específicas, modificando su personalidad, memoria y capacidades.

---

## 1. Identidad y Personalidad (`workspace/SOUL.md`)

El archivo `SOUL.md` define "quién" es el bot.

**Qué puedes editar:**

- **Personalidad**: Cambia de "Directo y eficiente" a "Amable y didáctico" si prefieres explicaciones largas.
- **Valores**: Prioriza velocidad sobre precisión si lo necesitas.
- **Estilo**: Define si quieres emojis, código siempre, o respuestas cortas.

**Ejemplo de cambio:**

```markdown
# Antes

- Concisión: Máximo 4 líneas

# Después

- Concisión: Explicaciones detalladas con ejemplos
```

## 2. Perfil de Usuario (`workspace/USER.md`)

El archivo `USER.md` es lo que el bot sabe de TI. Mantenlo actualizado.

**Información Clave:**

- **Proyectos**: Lista tus proyectos actuales para que el bot tenga contexto (ej. "Estoy trabajando en CATALYST").
- **Preferencias**: Si cambias de IDE o lenguaje favorito, ponlo aquí.
- **Stack**: Si empiezas a usar Rust, añádelo para que el bot sugiera código en Rust.

## 3. Memoria a Largo Plazo (`workspace/MEMORY.md`)

Este archivo se actualiza automáticamente, pero puedes editarlo manualmente.

- **Uso**: Añade notas permanentes que quieres que el bot nunca olvide.
- **Formato**: Markdown estándar.
- **Limpieza**: Si el bot recuerda cosas obsoletas, bórralas de aquí.

## 4. Skills y Herramientas

Nanobot usa el protocolo MCP (Model Context Protocol).

### Añadir Nuevas Skills

Para enseñar nuevas habilidades (ej. buscar en Google, analizar PDFs), necesitas configurar un servidor MCP o editar `app/core/tools.py` (usuario avanzado).

### Scripts Personalizados

Puedes poner scripts en la carpeta `scripts/` y pedirle al bot que los ejecute (si tiene permisos de shell).

---

## 5. Mantenimiento y Actualizaciones

### Actualizar desde el Repositorio Oficial

Si sale una nueva versión de Nanobot:

```bash
git pull origin main
poetry install
```

_Tus archivos en `workspace/` no deberían sobrescribirse si están en `.gitignore` o si los gestionas con cuidado._

### Logs y Depuración

- **Ver logs en tiempo real (Local):**
  ```bash
  docker-compose logs -f
  ```
- **Ver logs en Render:**
  Ve al Dashboard -> Logs.

### Copias de Seguridad

Tu carpeta `workspace/` es lo más valioso.

- Configura copias automáticas a S3 (ver `.env`).
- O haz commit de `workspace/` en un repositorio privado separado si prefieres.

---

## ⚠️ Nota Importante sobre Versiones

Si ves archivos `.bat` antiguos (ej. `start-nanobot.bat`) que mencionan WhatsApp, **ignóralos** si estás usando la versión Cloud/Telegram. Esta versión está optimizada para telegram y despliegue en servidor.
