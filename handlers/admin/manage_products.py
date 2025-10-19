from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db import get_session, list_products, delete_product, create_product, create_category, list_categories, get_category_by_slug, list_leads, update_lead_status
from database.models import Product, Category
from config import ADMIN_PASSWORD, ADMIN_USER_IDS

router = Router()


def get_admin_menu() -> InlineKeyboardMarkup:
    """Админ меню"""
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Добавить товар", callback_data="admin:add_product")
    builder.button(text="📋 Список товаров", callback_data="admin:list_products")
    builder.button(text="🗂️ Управление категориями", callback_data="admin:categories")
    builder.button(text="📝 Заявки (лиды)", callback_data="admin:leads")
    builder.button(text="📊 Статистика", callback_data="admin:stats")
    builder.button(text="🔙 Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()


@router.message(Command("admin"))
async def admin_login(message: Message):
    """Вход в админ панель"""
    print(f"Admin command received from user {message.from_user.id}")
    
    # Проверяем, является ли пользователь админом
    if ADMIN_USER_IDS and message.from_user.id not in ADMIN_USER_IDS:
        print(f"Access denied for user {message.from_user.id}")
        await message.answer("❌ У вас нет доступа к админ панели")
        return
        
    print("Access granted, asking for password")
    await message.answer(
        "🔐 Введите пароль для входа в админ панель:",
        reply_markup=None
    )


@router.message(F.text == "/admin")
async def admin_login_alt(message: Message):
    """Альтернативный вход в админ панель"""
    await admin_login(message)


@router.message(Command("start"))
async def start_command(message: Message):
    """Обработчик команды /start для админа"""
    # Если это админ, показываем админ панель
    if ADMIN_USER_IDS and message.from_user.id in ADMIN_USER_IDS:
        await message.answer(
            "🛠️ Админ панель\n\nВыберите действие:",
            reply_markup=get_admin_menu()
        )
    else:
        # Если не админ, перенаправляем в обычный старт
        from handlers.client.start import WELCOME_TEXT
        from keyboards.main_menu import get_main_menu
        await message.answer(WELCOME_TEXT, reply_markup=get_main_menu())


@router.message(F.text == ADMIN_PASSWORD)
async def admin_panel(message: Message):
    """Админ панель"""
    # Проверяем, является ли пользователь админом
    if ADMIN_USER_IDS and message.from_user.id not in ADMIN_USER_IDS:
        await message.answer("❌ У вас нет доступа к админ панели")
        return
        
    await message.answer(
        "🛠️ Админ панель\n\nВыберите действие:",
        reply_markup=get_admin_menu()
    )


@router.callback_query(F.data == "admin:list_products")
async def admin_list_products(callback: CallbackQuery):
    """Список товаров в админ панели"""
    with get_session() as session:
        products = list_products(session)
    
    if not products:
        text = "📋 Товары не найдены"
    else:
        text = "📋 Список товаров:\n\n"
        for i, product in enumerate(products[:10], 1):  # Показываем первые 10
            text += f"{i}. {product.title} - {product.price} ₽\n"
        
        if len(products) > 10:
            text += f"\n... и еще {len(products) - 10} товаров"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data="admin:back")
    builder.button(text="➕ Добавить товар", callback_data="admin:add_product")
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "admin:categories")
async def admin_categories(callback: CallbackQuery):
    """Управление категориями"""
    with get_session() as session:
        categories = list_categories(session)
    
    if not categories:
        text = "🗂️ Категории не найдены"
    else:
        text = "🗂️ Категории:\n\n"
        for i, category in enumerate(categories, 1):
            text += f"{i}. {category.name} ({category.slug})\n"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data="admin:back")
    builder.button(text="➕ Добавить категорию", callback_data="admin:add_category")
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "admin:add_product")
async def admin_add_product(callback: CallbackQuery):
    """Добавление товара"""
    await callback.message.edit_text(
        """➕ Добавление товара

Отправьте данные товара в следующем формате:
```
Название товара
Категория (kitchen/bedroom/beds/sofa/tables/cabinets/mattresses/wardrobes)
Страна (RU/BY)
Цена (только цифры)
Описание
Фото (URL или файл, опционально)
```

Пример:
```
Кухонный гарнитур Nova
kitchen
RU
74990
Модульный кухонный гарнитур, фасады МДФ
https://example.com/photo.jpg
```""",
        reply_markup=InlineKeyboardBuilder().button(text="🔙 Назад", callback_data="admin:back").as_markup()
    )
    await callback.answer()


@router.callback_query(F.data == "admin:add_category")
async def admin_add_category(callback: CallbackQuery):
    """Добавление категории"""
    # TODO: Реализовать форму добавления категории
    await callback.message.edit_text(
        "➕ Добавление категории\n\nФункция в разработке...",
        reply_markup=InlineKeyboardBuilder().button(text="🔙 Назад", callback_data="admin:back").as_markup()
    )
    await callback.answer()


@router.callback_query(F.data == "admin:leads")
async def admin_leads(callback: CallbackQuery):
    """Управление заявками"""
    with get_session() as session:
        leads = list_leads(session, limit=20)
    
    if not leads:
        text = "📝 Заявок пока нет"
    else:
        text = "📝 Последние заявки:\n\n"
        for i, lead in enumerate(leads[:10], 1):
            status_emoji = {"new": "🆕", "in_progress": "🔄", "closed": "✅"}.get(lead.status, "❓")
            type_emoji = {"order": "🛒", "consultation": "📞", "question": "💬"}.get(lead.interest_type, "❓")
            
            product_name = lead.product.title if lead.product else "Не указан"
            text += f"{i}. {status_emoji} {type_emoji} #{lead.id}\n"
            text += f"   👤 {lead.name} | 📞 {lead.phone}\n"
            text += f"   📦 {product_name}\n"
            text += f"   📅 {lead.created.strftime('%d.%m.%Y %H:%M')}\n\n"
        
        if len(leads) > 10:
            text += f"... и еще {len(leads) - 10} заявок"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🆕 Новые", callback_data="admin:leads_new")
    builder.button(text="🔄 В работе", callback_data="admin:leads_progress")
    builder.button(text="✅ Закрытые", callback_data="admin:leads_closed")
    builder.button(text="🔙 Назад", callback_data="admin:back")
    builder.adjust(2, 1, 1)
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("admin:leads_"))
async def admin_leads_filtered(callback: CallbackQuery):
    """Фильтрация заявок по статусу"""
    status = callback.data.split("_")[-1]
    status_names = {"new": "Новые", "progress": "В работе", "closed": "Закрытые"}
    status_name = status_names.get(status, "Все")
    
    with get_session() as session:
        leads = list_leads(session, status=status if status != "progress" else "in_progress", limit=20)
    
    if not leads:
        text = f"📝 {status_name} заявок пока нет"
    else:
        text = f"📝 {status_name} заявки:\n\n"
        for i, lead in enumerate(leads[:10], 1):
            type_emoji = {"order": "🛒", "consultation": "📞", "question": "💬"}.get(lead.interest_type, "❓")
            product_name = lead.product.title if lead.product else "Не указан"
            
            text += f"{i}. {type_emoji} #{lead.id}\n"
            text += f"   👤 {lead.name} | 📞 {lead.phone}\n"
            text += f"   📦 {product_name}\n"
            text += f"   💬 {lead.comment[:50]}{'...' if len(lead.comment) > 50 else ''}\n"
            text += f"   📅 {lead.created.strftime('%d.%m.%Y %H:%M')}\n\n"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🆕 Новые", callback_data="admin:leads_new")
    builder.button(text="🔄 В работе", callback_data="admin:leads_progress")
    builder.button(text="✅ Закрытые", callback_data="admin:leads_closed")
    builder.button(text="🔙 Назад", callback_data="admin:back")
    builder.adjust(2, 1, 1)
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "admin:stats")
async def admin_stats(callback: CallbackQuery):
    """Статистика"""
    with get_session() as session:
        products = list_products(session)
        categories = list_categories(session)
        leads = list_leads(session)
        new_leads = list_leads(session, status="new")
        in_progress_leads = list_leads(session, status="in_progress")
        closed_leads = list_leads(session, status="closed")
    
    avg_price = sum(float(p.price) for p in products if p.price) / len([p for p in products if p.price]) if products else 0
    
    text = f"""📊 Статистика:

📦 Товаров: {len(products)}
🗂️ Категорий: {len(categories)}
💰 Средняя цена: {avg_price:.2f} ₽

📝 Заявки:
🆕 Новые: {len(new_leads)}
🔄 В работе: {len(in_progress_leads)}
✅ Закрытые: {len(closed_leads)}
📋 Всего: {len(leads)}"""
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data="admin:back")
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "admin:back")
async def admin_back(callback: CallbackQuery):
    """Возврат в админ меню"""
    await callback.message.edit_text(
        "🛠️ Админ панель\n\nВыберите действие:",
        reply_markup=get_admin_menu()
    )
    await callback.answer()


@router.message(F.text.startswith("Кухонный") | F.text.startswith("Кровать") | F.text.startswith("Шкаф") | F.text.startswith("Стол") | F.text.startswith("Диван"))
async def parse_product_data(message: Message):
    """Парсинг данных товара из сообщения"""
    # Проверяем, является ли пользователь админом
    if ADMIN_USER_IDS and message.from_user.id not in ADMIN_USER_IDS:
        return
    
    try:
        lines = message.text.strip().split('\n')
        if len(lines) < 5:
            await message.answer("❌ Недостаточно данных. Нужно минимум 5 строк.")
            return
            
        title = lines[0].strip()
        category_slug = lines[1].strip()
        country = lines[2].strip()
        price = float(lines[3].strip())
        description = lines[4].strip()
        photo = lines[5].strip() if len(lines) > 5 and lines[5].strip() else None
        
        with get_session() as session:
            # Находим или создаем категорию
            category = get_category_by_slug(session, category_slug)
            if not category:
                # Создаем новую категорию
                category_names = {
                    "kitchen": "Кухонная мебель",
                    "bedroom": "Спальная мебель",
                    "beds": "Кровати",
                    "sofa": "Мягкая мебель",
                    "tables": "Столы и стулья",
                    "cabinets": "Тумбы и комоды",
                    "mattresses": "Матрасы",
                    "wardrobes": "Шкафы"
                }
                category_name = category_names.get(category_slug, category_slug.title())
                category = create_category(session, slug=category_slug, name=category_name)
            
            # Создаем товар
            product = create_product(
                session,
                category=category,
                country=country,
                title=title,
                description=description,
                price=price,
                photo=photo
            )
            
        await message.answer(
            f"✅ Товар успешно добавлен!\n\n"
            f"📦 {product.title}\n"
            f"💰 Цена: {price} ₽\n"
            f"🏷️ Категория: {category.name}\n"
            f"🌍 Страна: {country}",
            reply_markup=get_admin_menu()
        )
        
    except ValueError as e:
        await message.answer(f"❌ Ошибка в данных: {e}")
    except Exception as e:
        await message.answer(f"❌ Произошла ошибка: {e}")