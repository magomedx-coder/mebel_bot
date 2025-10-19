from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.order_states import OrderForm, ConsultationForm, QuestionForm
from services.validators import validate_name, validate_phone, validate_text, format_phone
from database.db import get_session, get_product, create_lead
from keyboards.main_menu import get_back_to_menu

router = Router()


# Обработчики для заказа товара
@router.callback_query(F.data.startswith("order:"))
async def start_order_form(callback: CallbackQuery, state: FSMContext):
    """Начало формы заказа"""
    product_id = int(callback.data.split(":", 1)[1])
    
    with get_session() as session:
        product = get_product(session, product_id)
        if not product:
            await callback.message.edit_text(
                "❌ Товар не найден",
                reply_markup=get_back_to_menu()
            )
            await callback.answer()
            return
    
    # Сохраняем ID товара в состоянии
    await state.update_data(product_id=product_id, product_title=product.title)
    
    await callback.message.edit_text(
        f"🛒 Оформление заказа\n\n"
        f"Товар: <b>{product.title}</b>\n\n"
        f"📝 Введите ваше имя:",
    )
    
    await state.set_state(OrderForm.waiting_for_name)
    await callback.answer()


@router.message(OrderForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Обработка имени"""
    name = message.text.strip()
    
    if not validate_name(name):
        await message.answer(
            "❌ Некорректное имя. Введите имя (только буквы, минимум 2 символа):"
        )
        return
    
    await state.update_data(name=name)
    await message.answer(
        "📞 Введите ваш номер телефона:"
    )
    
    await state.set_state(OrderForm.waiting_for_phone)


@router.message(OrderForm.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """Обработка телефона"""
    phone = message.text.strip()
    
    if not validate_phone(phone):
        await message.answer(
            "❌ Некорректный номер телефона. Введите номер в формате:\n"
            "+7XXXXXXXXXX, 8XXXXXXXXXX или XXXXXXXXXX"
        )
        return
    
    formatted_phone = format_phone(phone)
    await state.update_data(phone=formatted_phone)
    
    await message.answer(
        "💬 Добавьте комментарий к заказу (необязательно):"
    )
    
    await state.set_state(OrderForm.waiting_for_comment)


@router.message(OrderForm.waiting_for_comment)
async def process_comment(message: Message, state: FSMContext):
    """Обработка комментария и завершение заказа"""
    comment = message.text.strip() if message.text else ""
    
    # Получаем данные из состояния
    data = await state.get_data()
    
    # Сохраняем заказ в базу данных
    with get_session() as session:
        lead = create_lead(
            session,
            name=data['name'],
            phone=data['phone'],
            product_id=data['product_id'],
            interest_type="order",
            comment=comment
        )
    
    # Отправляем подтверждение
    await message.answer(
        f"✅ Заказ успешно оформлен!\n\n"
        f"📦 Товар: {data['product_title']}\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"💬 Комментарий: {comment if comment else 'Не указан'}\n\n"
        f"📋 Номер заказа: #{lead.id}\n\n"
        f"Наш менеджер свяжется с вами в ближайшее время для подтверждения заказа.",
        reply_markup=get_back_to_menu()
    )
    
    await state.clear()


# Обработчики для консультации
@router.callback_query(F.data.startswith("consultation:"))
async def start_consultation_form(callback: CallbackQuery, state: FSMContext):
    """Начало формы консультации"""
    product_id = int(callback.data.split(":", 1)[1])
    
    with get_session() as session:
        product = get_product(session, product_id)
        if not product:
            await callback.message.edit_text(
                "❌ Товар не найден",
                reply_markup=get_back_to_menu()
            )
            await callback.answer()
            return
    
    await state.update_data(product_id=product_id, product_title=product.title)
    
    await callback.message.edit_text(
        f"📞 Заказ консультации\n\n"
        f"Товар: <b>{product.title}</b>\n\n"
        f"📝 Введите ваше имя:",
    )
    
    await state.set_state(ConsultationForm.waiting_for_name)
    await callback.answer()


@router.message(ConsultationForm.waiting_for_name)
async def process_consultation_name(message: Message, state: FSMContext):
    """Обработка имени для консультации"""
    name = message.text.strip()
    
    if not validate_name(name):
        await message.answer(
            "❌ Некорректное имя. Введите имя (только буквы, минимум 2 символа):"
        )
        return
    
    await state.update_data(name=name)
    await message.answer(
        "📞 Введите ваш номер телефона:"
    )
    
    await state.set_state(ConsultationForm.waiting_for_phone)


@router.message(ConsultationForm.waiting_for_phone)
async def process_consultation_phone(message: Message, state: FSMContext):
    """Обработка телефона для консультации"""
    phone = message.text.strip()
    
    if not validate_phone(phone):
        await message.answer(
            "❌ Некорректный номер телефона. Введите номер в формате:\n"
            "+7XXXXXXXXXX, 8XXXXXXXXXX или XXXXXXXXXX"
        )
        return
    
    formatted_phone = format_phone(phone)
    await state.update_data(phone=formatted_phone)
    
    await message.answer(
        "💬 Опишите ваш вопрос или что вас интересует:"
    )
    
    await state.set_state(ConsultationForm.waiting_for_question)


@router.message(ConsultationForm.waiting_for_question)
async def process_consultation_question(message: Message, state: FSMContext):
    """Обработка вопроса и завершение консультации"""
    question = message.text.strip()
    
    if not validate_text(question, min_length=5, max_length=500):
        await message.answer(
            "❌ Вопрос слишком короткий или длинный (5-500 символов). Попробуйте еще раз:"
        )
        return
    
    data = await state.get_data()
    
    with get_session() as session:
        lead = create_lead(
            session,
            name=data['name'],
            phone=data['phone'],
            product_id=data['product_id'],
            interest_type="consultation",
            comment=question
        )
    
    await message.answer(
        f"✅ Заявка на консультацию отправлена!\n\n"
        f"📦 Товар: {data['product_title']}\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"💬 Вопрос: {question}\n\n"
        f"📋 Номер заявки: #{lead.id}\n\n"
        f"Наш менеджер свяжется с вами для консультации.",
        reply_markup=get_back_to_menu()
    )
    
    await state.clear()


# Обработчики для вопросов
@router.callback_query(F.data.startswith("question:"))
async def start_question_form(callback: CallbackQuery, state: FSMContext):
    """Начало формы вопроса"""
    product_id = int(callback.data.split(":", 1)[1])
    
    with get_session() as session:
        product = get_product(session, product_id)
        if not product:
            await callback.message.edit_text(
                "❌ Товар не найден",
                reply_markup=get_back_to_menu()
            )
            await callback.answer()
            return
    
    await state.update_data(product_id=product_id, product_title=product.title)
    
    await callback.message.edit_text(
        f"💬 Задать вопрос\n\n"
        f"Товар: <b>{product.title}</b>\n\n"
        f"💬 Напишите ваш вопрос:",
    )
    
    await state.set_state(QuestionForm.waiting_for_question)
    await callback.answer()


@router.message(QuestionForm.waiting_for_question)
async def process_question(message: Message, state: FSMContext):
    """Обработка вопроса"""
    question = message.text.strip()
    
    if not validate_text(question, min_length=5, max_length=500):
        await message.answer(
            "❌ Вопрос слишком короткий или длинный (5-500 символов). Попробуйте еще раз:"
        )
        return
    
    data = await state.get_data()
    
    with get_session() as session:
        lead = create_lead(
            session,
            name="Анонимный пользователь",
            phone="Не указан",
            product_id=data['product_id'],
            interest_type="question",
            comment=question
        )
    
    await message.answer(
        f"✅ Вопрос отправлен!\n\n"
        f"📦 Товар: {data['product_title']}\n"
        f"💬 Вопрос: {question}\n\n"
        f"📋 Номер вопроса: #{lead.id}\n\n"
        f"Мы ответим на ваш вопрос в ближайшее время.",
        reply_markup=get_back_to_menu()
    )
    
    await state.clear()