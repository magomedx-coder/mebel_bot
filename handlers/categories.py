from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.main_menu import get_subcategory_menu, get_back_to_menu, get_products_menu, get_product_actions
from database.db import get_session, get_category_by_slug, list_products, get_product
from keyboards.product_kb import get_product_actions
router = Router()

NO_PRODUCTS_TEXT = """📭 К сожалению, по данной категории пока нет добавленной мебели.

Но не переживайте! Наш ассортимент постоянно пополняется новыми моделями.
Рекомендуем периодически возвращаться и смотреть обновления."""


@router.callback_query(F.data.startswith("category:"))
async def handle_category_selection(callback: CallbackQuery):
    """Обработчик выбора категории мебели"""
    category_slug = callback.data.split(":", 1)[1]
    
    # Проверяем, есть ли подкатегории
    keyboard = get_subcategory_menu(category_slug)
    if keyboard:
        await callback.message.edit_text(
            "Выберите тип:",
            reply_markup=keyboard
        )
        await callback.answer()
        return

    # Если нет подкатегорий, пытаемся показать товары
    async with get_session() as session:
        category = await get_category_by_slug(session, category_slug)
        if not category:
            await callback.message.edit_text(
                "❌ Категория не найдена",
                reply_markup=get_back_to_menu()
            )
            await callback.answer()
            return
    
    if products.country:

        from aiogram import Router, F
        from aiogram.types import CallbackQuery
        from keyboards.main_menu import get_subcategory_menu, get_back_to_menu
        from database.db import get_session, get_category_by_slug, list_products

        router = Router()

        NO_PRODUCTS_TEXT = """📭 К сожалению, по данной категории пока нет добавленной мебели.\n\nНо не переживайте! Наш ассортимент постоянно пополняется новыми моделями.\nРекомендуем периодически возвращаться и смотреть обновления."""

        @router.callback_query(F.data.startswith("category:"))
        async def handle_category_selection(callback: CallbackQuery):
            """Обработчик выбора категории мебели"""
            category_slug = callback.data.split(":", 1)[1]
            keyboard = get_subcategory_menu(category_slug)
            if keyboard:
                await callback.message.edit_text(
                    "Выберите тип:",
                    reply_markup=keyboard
                )
                await callback.answer()
                return
            async with get_session() as session:
                category = await get_category_by_slug(session, category_slug)
                if not category:
                    await callback.message.edit_text(
                        "❌ Категория не найдена",
                        reply_markup=get_back_to_menu()
                    )
                    await callback.answer()
                    return
                products = await list_products(session, category_slug=category_slug)
                if not products:
                    await callback.message.edit_text(
                        NO_PRODUCTS_TEXT,
                        reply_markup=get_back_to_menu()
                    )
                else:
                    await callback.message.edit_text(
                        NO_PRODUCTS_TEXT,  # Временно, пока не реализован показ товаров
                        reply_markup=get_back_to_menu()
                    )
            await callback.answer()

        @router.callback_query(F.data.startswith("subcategory:"))
        async def handle_subcategory_selection(callback: CallbackQuery):
            """Обработчик выбора подкатегории мебели"""
            _, category_slug, subcategory = callback.data.split(":")
            async with get_session() as session:
                products = await list_products(session, category_slug=category_slug, subcategory=subcategory)
                if not products:
                    await callback.message.edit_text(
                        NO_PRODUCTS_TEXT,
                        reply_markup=get_back_to_menu()
                    )
                else:
                    await callback.message.edit_text(
                        NO_PRODUCTS_TEXT,  # Временно, пока не реализован показ товаров
                        reply_markup=get_back_to_menu()
                    )
            await callback.answer()
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
                reply_markup=get(category_slug, page, limit)
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
        
        text = product_card_text(product)
        
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
