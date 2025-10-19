from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def get_product_actions(product_id: int, back_callback: str = "main_menu") -> InlineKeyboardMarkup:
    """Кнопки действий для товара"""
    builder = InlineKeyboardBuilder()
    
    # Основные действия
    builder.button(text="💬 Задать вопрос", callback_data=f"question:{product_id}")
    builder.button(text="📞 Заказать консультацию", callback_data=f"consultation:{product_id}")
    builder.button(text="🛒 Оформить заказ", callback_data=f"order:{product_id}")
    builder.button(text="⬅️ Назад", callback_data=back_callback)
    
    # Располагаем кнопки по 2 в ряду
    builder.adjust(2, 1, 1)
    
    return builder.as_markup()


def get_order_confirmation(product_id: int) -> InlineKeyboardMarkup:
    """Кнопки подтверждения заказа"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="✅ Подтвердить заказ", callback_data=f"confirm_order:{product_id}")
    builder.button(text="❌ Отмена", callback_data=f"cancel_order:{product_id}")
    
    builder.adjust(1)
    
    return builder.as_markup()


def get_consultation_confirmation(product_id: int) -> InlineKeyboardMarkup:
    """Кнопки подтверждения консультации"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="✅ Заказать консультацию", callback_data=f"confirm_consultation:{product_id}")
    builder.button(text="❌ Отмена", callback_data=f"cancel_consultation:{product_id}")
    
    builder.adjust(1)
    
    return builder.as_markup()


def get_question_confirmation(product_id: int) -> InlineKeyboardMarkup:
    """Кнопки подтверждения вопроса"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="✅ Отправить вопрос", callback_data=f"confirm_question:{product_id}")
    builder.button(text="❌ Отмена", callback_data=f"cancel_question:{product_id}")
    
    builder.adjust(1)
    
    return builder.as_markup()