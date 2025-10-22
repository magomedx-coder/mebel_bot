from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_admin_panel_kb() -> InlineKeyboardMarkup:
    """Создает клавиатуру панели администратора"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="Добавить категорию", callback_data="admin_add_category")
    builder.button(text="Добавить мебель", callback_data="admin_add_furniture")
    builder.button(text="Удалить мебель", callback_data="admin_delete_furniture")
    builder.button(text="Список категорий", callback_data="admin_list_categories")
    builder.button(text="Заявки", callback_data="admin_orders")
    builder.button(text="« Назад", callback_data="back_to_main")
    
    builder.adjust(2, 2, 2)  # По 2 кнопки в ряд
    return builder.as_markup()