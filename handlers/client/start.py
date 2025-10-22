from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.main_menu import get_main_menu, get_subcategory_menu, get_back_to_menu
from services.messages import (
    WELCOME_MESSAGE, ABOUT_COMPANY, 
    COOPERATION_MESSAGE, NO_FURNITURE_MESSAGE
)
from database.models import User

router = Router()

@router.message(F.text == "/start")
async def start_command(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        text=WELCOME_MESSAGE,
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    """Возврат в главное меню"""
    await callback.message.edit_text(
        text=WELCOME_MESSAGE,
        reply_markup=get_main_menu()
    )
    await callback.answer()


@router.callback_query(F.data == "about_company")
async def about_company(callback: CallbackQuery):
    """Информация о компании"""
    about_text = ABOUT_COMPANY
    
    await callback.message.edit_text(
        text=about_text,
        reply_markup=get_back_to_menu()
    )
    await callback.answer()


@router.callback_query(F.data == "cooperation")
async def cooperation(callback: CallbackQuery):
    """Информация о сотрудничестве"""
    cooperation_text = COOPERATION_MESSAGE
    await callback.message.edit_text(
        text=cooperation_text,
        reply_markup=get_back_to_menu()
    )
    await callback.answer()



    await callback.answer()

