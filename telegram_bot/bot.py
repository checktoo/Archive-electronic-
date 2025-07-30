import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command"""
    await message.answer(
        f"Hello, {message.from_user.full_name}! 👋\n"
        f"I'm a simple bot created with aiogram and FastAPI.\n"
        f"Try these commands:\n"
        f"/help - Show available commands\n"
        f"/echo <text> - Echo your message\n"
        f"/info - Get your user info"
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
/echo <text> - Echo your message
/info - Get your user information
    """
    await message.answer(help_text)

@dp.message(Command("echo"))
async def cmd_echo(message: Message):
    """Handle /echo command"""
    # Extract text after /echo command
    text = message.text.split(' ', 1)
    if len(text) > 1:
        await message.answer(f"Echo: {text[1]}")
    else:
        await message.answer("Please provide text to echo. Usage: /echo <your text>")

@dp.message(Command("info"))
async def cmd_info(message: Message):
    """Handle /info command"""
    user = message.from_user
    info_text = f"""
Your information:
👤 Name: {user.full_name}
🆔 ID: {user.id}
👤 Username: @{user.username if user.username else 'Not set'}
🌐 Language: {user.language_code if user.language_code else 'Not set'}
    """
    await message.answer(info_text)

@dp.message()
async def echo_message(message: Message):
    """Echo any other message"""
    await message.answer(f"You said: {message.text}")

# Function to set webhook
async def set_webhook():
    """Set webhook for the bot"""
    if config.WEBHOOK_URL:
        await bot.set_webhook(config.WEBHOOK_URL)
        logger.info(f"Webhook set to {config.WEBHOOK_URL}")
    else:
        logger.warning("WEBHOOK_URL not configured")

# Function to delete webhook (for polling mode)
async def delete_webhook():
    """Delete webhook for the bot"""
    await bot.delete_webhook()
    logger.info("Webhook deleted")