import asyncio
import logging
from bot import bot, dp, delete_webhook
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Run bot in polling mode (for local development)"""
    # Check if bot token is configured
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN not configured. Please set it in .env file")
        return
    
    # Delete webhook to use polling
    await delete_webhook()
    
    logger.info("Starting bot in polling mode...")
    
    try:
        # Start polling
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())