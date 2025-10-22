from aiogram import Router, F
from aiogram.types import Message
from database.models import User
from database.db import get_session
from datetime import datetime

router = Router()

@router.message(F.text == "/profile")
async def cmd_profile(message: Message):
    """Показывает профиль пользователя"""
    async with get_session() as session:
        user = await session.get(User, message.from_user.id)
        
        if not user:
            await message.answer("Профиль не найден. Пожалуйста, начните с команды /start")
            return
        
        # Форматируем дату регистрации
        reg_date = user.created_at.strftime("%d.%m.%Y %H:%M")
        
        profile_text = f"""👤 Профиль пользователя @{message.from_user.username or "без username"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧾 Основное
├ 🆔 ID: {user.id}
├ 📱 Telegram ID: {message.from_user.id}
├ 👤 Username: @{message.from_user.username or "—"}
├ 🧑 Имя: {message.from_user.first_name or "."}
├ 👨‍👩‍👧 Фамилия: {message.from_user.last_name or "—"}
├ 🗓 Зарегистрирован: {reg_date}
└ 🛡 Админ: {"✅ Да" if user.is_admin else "❌ Нет"}"""

        await message.answer(profile_text)