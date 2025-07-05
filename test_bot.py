#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы бота
"""

import asyncio
from app.bot.bot import bot, setup_bot

async def test_bot():
    """Тестирование бота"""
    print("🤖 Запуск тестирования бота...")
    
    try:
        # Инициализация диспетчера
        dp = setup_bot()
        print("✅ Диспетчер инициализирован")
        
        # Получение информации о боте
        bot_info = await bot.get_me()
        print(f"✅ Бот: @{bot_info.username} (ID: {bot_info.id})")
        
        print("🎉 Бот готов к работе!")
        print("💡 Для остановки нажмите Ctrl+C")
        
        # Запуск бота
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot()) 