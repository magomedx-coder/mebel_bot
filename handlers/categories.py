from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.main_menu import get_subcategory_menu, get_products_menu, get_back_to_menu
from keyboards.product_kb import get_product_actions
from database.db import get_session, get_category_by_slug, list_products, get_product

router = Router()

NO_PRODUCTS_TEXT = """📭 К сожалению, по данной категории пока нет добавленной мебели.

Но не переживайте! Наш ассортимент постоянно пополняется новыми моделями.
Рекомендуем периодически возвращаться и смотреть обновления."""


def _format_price(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ")


def _product_card_text(product) -> str:
    stock = "✅ В наличии" if product.in_stock else "❌ Нет в наличии"
    
    text = f"<b>{product.title}</b>\n\n"
    text += f"{product.description}\n\n"
    
    if product.price:
        text += f"💰 Цена: <b>{_format_price(float(product.price))} ₽</b>\n"
    
    if product.dimensions:
        text += f"📏 Размеры: {product.dimensions}\n"
    
    if product.country:
        text += f"🌍 Страна: {product.country}\n"
    
    text += f"📦 Статус: {stock}"
    
    return text


@router.callback_query(F.data.startswith("category:"))
async def handle_category_selection(callback: CallbackQuery):
    """Обработчик выбора категории мебели"""
    category_slug = callback.data.split(":", 1)[1]
    
    with get_session() as session:
        category = get_category_by_slug(session, category_slug)
        if not category:
            await callback.message.edit_text(
                "❌ Категория не найдена",
                reply_markup=get_back_to_menu()
            )
            await callback.answer()
            return
        
        # Проверяем, есть ли подкатегории
        from database.db import list_categories
        subcategories = list_categories(session, parent_id=category.id)
        
        if subcategories:
            # Если есть подкатегории, показываем их
            await callback.message.edit_text(
                f"🛋️ {category.name}\n\nВыберите подкатегорию:",
                reply_markup=get_subcategory_menu(category_slug)
            )
        else:
            # Если подкатегорий нет, проверяем товары
            products = list_products(session, category_id=category.id)
            if products:
                await callback.message.edit_text(
                    f"🛋️ {category.name}\n\nНайдено товаров: {len(products)}",
                    reply_markup=get_products_menu(category_slug)
                )
            else:
                await callback.message.edit_text(
                    f"🛋️ {category.name}\n\n{NO_PRODUCTS_TEXT}",
                    reply_markup=get_back_to_menu()
                )
    
    await callback.answer()


@router.callback_query(F.data.startswith("subcategory:"))
async def handle_subcategory_selection(callback: CallbackQuery):
    """Обработчик выбора подкатегории"""
    subcategory_slug = callback.data.split(":", 1)[1]
    
    with get_session() as session:
        subcategory = get_category_by_slug(session, subcategory_slug)
        if not subcategory:
            await callback.message.edit_text(
                "❌ Подкатегория не найдена",
                reply_markup=get_back_to_menu()
            )
            await callback.answer()
            return
        
        products = list_products(session, category_id=subcategory.id)
        if products:
            await callback.message.edit_text(
                f"🛋️ {subcategory.name}\n\nНайдено товаров: {len(products)}",
                reply_markup=get_products_menu(subcategory_slug)
            )
        else:
            await callback.message.edit_text(
                f"🛋️ {subcategory.name}\n\n{NO_PRODUCTS_TEXT}",
                reply_markup=get_back_to_menu()
            )
    
    await callback.answer()


@router.callback_query(F.data.startswith("products:"))
async def handle_products_list(callback: CallbackQuery):
    """Обработчик списка товаров с пагинацией"""
    parts = callback.data.split(":")
    category_slug = parts[1]
    page = int(parts[2]) if len(parts) > 2 else 0
    
    with get_session() as session:
        category = get_category_by_slug(session, category_slug)
        if not category:
            await callback.message.edit_text(
                "❌ Категория не найдена",
                reply_markup=get_back_to_menu()
            )
            await callback.answer()
            return
        
        products = list_products(session, category_id=category.id)
        limit = 5
        start_idx = page * limit
        end_idx = start_idx + limit
        page_products = products[start_idx:end_idx]
        
        if not page_products and page == 0:
            await callback.message.edit_text(
                f"🛋️ {category.name}\n\n{NO_PRODUCTS_TEXT}",
                reply_markup=get_back_to_menu()
            )
        else:
            text = f"🛋️ {category.name}\n\n"
            if len(products) > 1:
                text += f"Страница {page + 1} из {(len(products) + limit - 1) // limit}\n"
            text += f"Показано: {len(page_products)} из {len(products)} товаров"
            
            await callback.message.edit_text(
                text,
                reply_markup=get_products_menu(category_slug, page, limit)
            )
    
    await callback.answer()


@router.callback_query(F.data.startswith("product:"))
async def handle_product_detail(callback: CallbackQuery):
    """Обработчик детального просмотра товара"""
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
        
        text = _product_card_text(product)
        
        # Определяем callback для кнопки назад
        back_callback = "main_menu"
        if product.category.parent_id:
            # Если товар в подкатегории, возвращаемся к подкатегории
            back_callback = f"products:{product.category.slug}"
        else:
            # Если товар в основной категории, возвращаемся к категории
            back_callback = f"products:{product.category.slug}"
        
        await callback.message.edit_text(
            text,
            reply_markup=get_product_actions(product_id, back_callback)
        )
    
    await callback.answer()
