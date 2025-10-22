from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from database.db import get_session
from database.models import User


class AdminMiddleware(BaseMiddleware):
    """Проверяет, является ли пользователь администратором"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Получаем user_id в зависимости от типа события
        user_id = event.from_user.id
        
        async with get_session() as session:
            user = await session.get(User, user_id)
            
            # Если пользователь не админ и пытается получить доступ к админ-панели,
            # отменяем обработку
            if not user or not user.is_admin:
                if isinstance(event, CallbackQuery):
                    if event.data.startswith("admin_"):
                        await event.answer(
                            "У вас нет прав администратора",
                            show_alert=True
                        )
                        return
                elif isinstance(event, Message):
                    if event.text and event.text.startswith("/admin"):
                        await event.answer(
                            "У вас нет прав администратора"
                        )
                        return
            
            # Если пользователь админ или это не админ-действие,
            # продолжаем обработку
            return await handler(event, data)