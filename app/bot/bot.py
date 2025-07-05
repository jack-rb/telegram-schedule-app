from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import os

# Инициализация бота
bot = Bot(
    token=os.getenv('BOT_TOKEN', 'your_bot_token_here'), 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

def setup_bot():
    # Импортируем обработчики
    from . import handlers
    return dp
