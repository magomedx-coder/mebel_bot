from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.admin_kb import get_admin_panel_kb
from keyboards.main_menu import get_main_menu
from states.admin_states import CategoryForm, FurnitureForm
from database.db import get_session
from database.models import Category, Product

router = Router()

@router.callback_query(F.data == "admin_panel")
async def show_admin_panel(callback: CallbackQuery):
    """Показывает панель администратора"""
    await callback.message.edit_text(
        text="🛠 Панель администратора\n\nВыберите действие:",
        reply_markup=get_admin_panel_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_add_category")
async def add_category_start(callback: CallbackQuery, state: FSMContext):
    """Начало добавления категории"""
    await state.set_state(CategoryForm.waiting_for_name)
    await callback.message.edit_text(
        text="Введите название новой категории:",
        reply_markup=None
    )
    await callback.answer()

@router.callback_query(F.data == "admin_add_furniture")
async def add_furniture_start(callback: CallbackQuery, state: FSMContext):
    """Начало добавления мебели"""
    await state.set_state(FurnitureForm.waiting_for_category)
    # TODO: Show available categories
    await callback.message.edit_text(
        text="Выберите категорию для новой мебели:",
        reply_markup=None  # TODO: Add category selection keyboard
    )
    await callback.answer()

@router.callback_query(F.data == "admin_delete_furniture")
async def delete_furniture_start(callback: CallbackQuery):
    """Начало удаления мебели"""
    # TODO: Show available furniture items
    await callback.message.edit_text(
        text="Выберите мебель для удаления:",
        reply_markup=None  # TODO: Add furniture selection keyboard
    )
    await callback.answer()

@router.callback_query(F.data == "admin_list_categories")
async def list_categories(callback: CallbackQuery):
    """Показывает список категорий"""
    async with get_session() as session:
        categories = await session.query(Category).all()
        
        if not categories:
            text = "📂 Список категорий пуст"
        else:
            text = "📂 Список категорий:\n\n" + "\n".join(
                f"• {cat.name}" for cat in categories
            )
            
    await callback.message.edit_text(
        text=text,
        reply_markup=get_admin_panel_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_orders")
async def show_orders(callback: CallbackQuery):
    """Показывает список заявок"""
    # TODO: Implement orders list view
    await callback.message.edit_text(
        text="📦 Список заявок:\n\nФункционал в разработке",
        reply_markup=get_admin_panel_kb()
    )
    await callback.answer()