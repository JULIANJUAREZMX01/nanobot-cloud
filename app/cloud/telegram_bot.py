"""Telegram bot integration for Nanobot with Agent Loop"""

import asyncio
from typing import Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from app.config import Settings
from app.utils import get_logger
from app.core.context import AgentContext

logger = get_logger(__name__)

_app: Optional[Application] = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    message = update.message

    await message.reply_text(
        f"Hola {user.first_name}! 👋\n\n"
        "Soy Nanobot, tu asistente personal de desarrollo.\n"
        "¿En qué puedo ayudarte?\n\n"
        "Puedo:\n"
        "• Ejecutar comandos\n"
        "• Leer/escribir archivos\n"
        "• Operaciones Git\n"
        "• Responder preguntas técnicas"
    )
    logger.info(f"User {user.id} started bot")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages with agent loop"""
    user = update.effective_user
    message = update.message

    if not message or not message.text:
        return

    logger.info(f"Message from {user.id}: {message.text[:50]}...")

    # Show typing indicator
    await update.message.chat.send_action("typing")

    try:
        # Import here to avoid circular imports
        from app.main import _agent_loop, _session_manager

        if not _agent_loop:
            await message.reply_text("❌ Agent loop no iniciado")
            return

        # Create session context
        session_id = f"telegram_{user.id}"
        
        # Load previous session or create new
        ctx = await _session_manager.load_session(session_id)
        if not ctx:
            ctx = AgentContext(
                session_id=session_id,
                user_id=str(user.id),
                channel="telegram"
            )

        # Add user message
        ctx.add_message("user", message.text)

        # Process with agent loop
        response = await _agent_loop.process_message(ctx)

        # Save session
        await _session_manager.save_session(ctx)

        # Send response (split if too long)
        if len(response) > 4096:
            # Send in chunks
            for i in range(0, len(response), 4096):
                await message.reply_text(response[i:i+4096])
        else:
            await message.reply_text(response)

        logger.info(f"Response sent to {user.id}")

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        error_msg = f"❌ Error: {str(e)[:100]}\n\nPor favor, intenta de nuevo."
        await message.reply_text(error_msg)


async def start_telegram_bot(settings: Settings) -> None:
    """Start Telegram bot"""
    global _app

    logger.info("🟢 Starting Telegram bot polling...")

    try:
        # Create application
        _app = Application.builder().token(settings.telegram_token).build()

        # Add handlers
        from app.cloud.telegram_bot import start, handle_message  # Import handlers locally to avoid circular imports? No, they are in this file.

        _app.add_handler(CommandHandler("start", start))
        _app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Start polling (non-blocking way for integration with FastAPI)
        await _app.initialize()
        await _app.start()
        await _app.updater.start_polling()
        
        logger.info("🟢 Telegram bot polling started")

    except Exception as e:
        logger.error(f"Telegram bot error: {e}", exc_info=True)


async def stop_telegram_bot() -> None:
    """Stop Telegram bot"""
    global _app
    if _app:
        try:
            await _app.stop()
            logger.info("🛑 Telegram bot stopped")
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
