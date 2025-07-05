from aiogram import types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from datetime import datetime
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services.schedule import ScheduleService
from .bot import dp

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот для просмотра расписания занятий.\n\n"
        "📅 Нажмите на кнопку ниже, чтобы открыть расписание:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="📚 Открыть расписание",
                web_app=WebAppInfo(url="http://localhost:8000")
            )
        ]])
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
🤖 *Доступные команды:*

/start - Открыть расписание
/groups - Список всех групп
/schedule [ID группы] - Расписание на сегодня
/help - Показать эту справку

📱 *Как использовать:*
1. Нажмите кнопку "Открыть расписание"
2. Выберите свою группу
3. Просматривайте расписание по дням
    """
    await message.answer(help_text, parse_mode="Markdown")

@dp.message(Command("groups"))
async def cmd_groups(message: types.Message):
    try:
        db = next(get_db())
        groups = ScheduleService.get_all_groups(db)
        if groups:
            groups_text = "\n".join([f"• {g['name']} (ID: {g['id']})" for g in groups])
            await message.answer(
                "📋 *Доступные группы:*\n\n"
                f"{groups_text}\n\n"
                "💡 Используйте ID группы в команде /schedule [ID]",
                parse_mode="Markdown"
            )
        else:
            await message.answer("❌ Группы не найдены в базе данных")
    except Exception as e:
        await message.answer("❌ Ошибка при получении списка групп")

@dp.message(Command("schedule"))
async def cmd_schedule(message: types.Message):
    try:
        cmd_parts = message.text.split()
        if len(cmd_parts) != 2:
            await message.answer(
                "❌ Пожалуйста, укажите ID группы.\n"
                "📝 *Пример:* `/schedule 1`\n\n"
                "💡 Используйте /groups для просмотра списка групп",
                parse_mode="Markdown"
            )
            return
        
        group_id = int(cmd_parts[1])
        today = datetime.now().strftime("%Y-%m-%d")
        
        db = next(get_db())
        schedule = ScheduleService.get_schedule_by_date(db, group_id, today)
        
        if not schedule:
            await message.answer(f"📅 Расписание на {today} не найдено")
            return
            
        lessons = schedule.get('lessons', [])
        if not lessons:
            await message.answer("📭 На этот день пар нет")
            return
            
        lessons_text = "\n\n".join([
            f"🕒 *{lesson['time']}*\n"
            f"📚 {lesson['subject']}\n"
            f"👨‍🏫 {lesson['teacher']}\n"
            f"🏛 Аудитория: {lesson['classroom']}"
            for lesson in lessons
        ])
            
        await message.answer(
            f"📅 *Расписание на {today}:*\n\n"
            f"{lessons_text}",
            parse_mode="Markdown"
        )
            
    except ValueError:
        await message.answer("❌ ID группы должен быть числом")
    except Exception as e:
        await message.answer("❌ Произошла ошибка при получении расписания")

@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    """Обработка данных из Mini App"""
    try:
        data = message.web_app_data.data
        await message.answer(f"📱 Данные из Mini App: {data}")
    except Exception as e:
        await message.answer("❌ Ошибка при обработке данных из Mini App")
