import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from bot import bot, dp, set_webhook, delete_webhook
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Startup
    logger.info("Starting up...")
    await set_webhook()
    yield
    # Shutdown
    logger.info("Shutting down...")
    await bot.session.close()

# Create FastAPI app
app = FastAPI(
    title="Telegram Bot with aiogram and FastAPI",
    description="A simple Telegram bot using aiogram 3.x and FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Telegram Bot is running!",
        "status": "active",
        "webhook_configured": config.WEBHOOK_URL is not None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post(config.WEBHOOK_PATH)
async def webhook(request: Request):
    """Handle incoming webhook requests from Telegram"""
    try:
        # Get the raw body
        body = await request.body()
        
        # Parse the update
        update = Update.model_validate_json(body)
        
        # Process the update
        await dp.process_update(update, bot=bot)
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=400, detail="Bad request")

@app.get("/webhook/info")
async def webhook_info():
    """Get webhook information"""
    try:
        webhook_info = await bot.get_webhook_info()
        return {
            "url": webhook_info.url,
            "has_custom_certificate": webhook_info.has_custom_certificate,
            "pending_update_count": webhook_info.pending_update_count,
            "last_error_date": webhook_info.last_error_date,
            "last_error_message": webhook_info.last_error_message,
            "max_connections": webhook_info.max_connections,
            "allowed_updates": webhook_info.allowed_updates
        }
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/webhook/set")
async def set_webhook_endpoint():
    """Manually set webhook"""
    try:
        await set_webhook()
        return {"status": "webhook set successfully"}
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        raise HTTPException(status_code=500, detail="Failed to set webhook")

@app.post("/webhook/delete")
async def delete_webhook_endpoint():
    """Delete webhook (switch to polling mode)"""
    try:
        await delete_webhook()
        return {"status": "webhook deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete webhook")

if __name__ == "__main__":
    import uvicorn
    
    # Check if bot token is configured
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN not configured. Please set it in .env file")
        exit(1)
    
    logger.info(f"Starting server on {config.WEB_SERVER_HOST}:{config.WEB_SERVER_PORT}")
    uvicorn.run(
        "main:app",
        host=config.WEB_SERVER_HOST,
        port=config.WEB_SERVER_PORT,
        reload=True
    )